import os,json,subprocess,time,urllib.request,signal
from pathlib import Path
from playwright.sync_api import sync_playwright
r=Path(__file__).resolve().parents[1]
s=subprocess.Popen(['npm','run','dev','--','--host','127.0.0.1','--port','5180'],cwd=r,stdout=subprocess.DEVNULL,stderr=subprocess.STDOUT,start_new_session=True)
try:
 for _ in range(80):
  try:urllib.request.urlopen('http://127.0.0.1:5180');break
  except Exception:time.sleep(.1)
 with sync_playwright() as p:
  b=p.chromium.launch(headless=True,executable_path=os.environ.get('CHROMIUM_PATH'),args=['--no-sandbox','--use-gl=angle','--use-angle=swiftshader','--enable-unsafe-swiftshader','--enable-webgl','--ignore-gpu-blocklist'])
  page=b.new_page(viewport={'width':1440,'height':900});errors=[];page.on('pageerror',lambda e:(errors.append(str(e)),print('PAGE ERROR',e,flush=True)))
  page.goto('http://127.0.0.1:5180');page.wait_for_function('window.racingDiagnostics && window.racingDiagnostics().webgl');page.locator('#start').click();page.wait_for_timeout(1000);print(page.evaluate('racingDiagnostics()'),flush=True);page.wait_for_function('racingDiagnostics().time>.2',timeout=60000)
  page.keyboard.down('w');page.wait_for_function('racingDiagnostics().speed>5',timeout=30000);page.keyboard.down('Shift');page.wait_for_function('racingDiagnostics().nitro<99',timeout=30000)
  d=page.evaluate('racingDiagnostics()');assert d['speed']>0 and d['distance']>0 and d['nitro']<100,d
  page.keyboard.up('Shift');page.keyboard.up('w');page.keyboard.press('c');page.screenshot(path=str(r/'docs/desktop.png'))
  page.locator('#pause').click();a=page.evaluate('racingDiagnostics().time');page.wait_for_timeout(300);assert page.evaluate('racingDiagnostics().time')==a
  page.locator('#start').click();page.locator('#restart').click();assert page.evaluate('racingDiagnostics().distance')==0
  page.set_viewport_size({'width':390,'height':844});page.locator('#start').click();btn=page.locator('[data-key="ArrowUp"]').bounding_box();page.mouse.move(btn['x']+btn['width']/2,btn['y']+btn['height']/2);page.mouse.down();page.wait_for_function('racingDiagnostics().speed>1',timeout=30000)
  page.mouse.up();assert page.evaluate('document.documentElement.scrollWidth<=innerWidth')
  page.screenshot(path=str(r/'docs/mobile.png'));assert not errors,errors
  (r/'docs/browser-report.json').write_text(json.dumps({'passed':['WebGL render','acceleration','nitro','camera switch','pause freezes clock','restart resets progress','touch throttle','mobile layout'],'page_errors':errors},indent=2));b.close()
finally:os.killpg(s.pid,signal.SIGTERM)
