export const LENGTH=1400,LAPS=3;
export function track(s){const a=s/LENGTH*Math.PI*2;return {x:Math.sin(a)*185,z:Math.cos(a)*250,y:2+Math.sin(a*2)*7,heading:Math.atan2(185*Math.cos(a),-250*Math.sin(a))};}
export function createRace(){return {phase:'ready',time:0,lapStart:0,best:null,lap:1,nitro:100,player:{name:'You',s:0,lane:0,speed:0,finish:null},bots:['Ace','Volt','Razor','Shadow','Blaze','Nitro','Falcon'].map((name,i)=>({name,s:12+i*9,lane:(i%3-1)*3,speed:37+i*.8,finish:null})),contact:0};}
export function standings(r){return [r.player,...r.bots].slice().sort((a,b)=>a.finish!==null&&b.finish!==null?a.finish-b.finish:a.finish!==null?-1:b.finish!==null?1:b.s-a.s);}
export function updateRace(r,input,dt){if(!Number.isFinite(dt)||dt<0)throw Error('Invalid timestep');dt=Math.min(dt,.05);if(r.phase!=='racing')return;r.time+=dt;r.contact=Math.max(0,r.contact-dt);
 const p=r.player,boost=input.nitro&&r.nitro>0&&input.throttle&&Math.abs(p.lane)<7;
 r.nitro=Math.max(0,Math.min(100,r.nitro+(boost?-32:9)*dt));
 p.speed=Math.max(0,Math.min(boost?66:52,p.speed+((input.throttle?boost?24:16: -7)-(input.brake?32:0))*dt));
 p.lane=Math.max(-11,Math.min(11,p.lane+(input.steer||0)*(2+p.speed*.14)*dt));
 if(Math.abs(p.lane)>7)p.speed=Math.max(0,p.speed-35*dt);
 const before=p.s;p.s+=p.speed*dt;
 for(const b of r.bots){if(b.finish!==null)continue;b.s+=b.speed*(1+.05*Math.sin(r.time+b.speed))*dt;if(Math.abs(b.s-p.s)<4&&Math.abs(b.lane-p.lane)<1.8){p.speed*=Math.pow(.6,dt*8);r.contact=.4;}if(b.s>=LENGTH*LAPS)b.finish=r.time;}
 if(Math.floor(p.s/LENGTH)>Math.floor(before/LENGTH)){const lapTime=r.time-r.lapStart;r.best=r.best===null?lapTime:Math.min(r.best,lapTime);r.lapStart=r.time;r.lap=Math.min(LAPS,Math.floor(p.s/LENGTH)+1);}
 if(p.s>=LENGTH*LAPS){p.finish=r.time;r.phase='finished';}
}
