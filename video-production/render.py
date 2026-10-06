#!/usr/bin/env python3
"""Render the 76-second H-JEPA promotional cut using repository footage.
Install requirements.txt, then run: python3 video-production/render.py
The default paths resolve relative to this repository, independently of cwd.
"""
import argparse, pathlib, subprocess, wave, shutil
import numpy as np
from PIL import Image, ImageDraw, ImageFont
import imageio_ffmpeg
P = argparse.ArgumentParser(description=__doc__)
P.add_argument('--repo', type=pathlib.Path, default=pathlib.Path(__file__).resolve().parent.parent,
               help='Repository root; defaults to the parent of this script directory.')
P.add_argument('--out', type=pathlib.Path, help='Output directory; defaults to video-production/output.')
P.add_argument('--teaser', type=pathlib.Path, help='Optional replacement opening teaser.')
P.add_argument('--font-regular', type=pathlib.Path, help='Regular TTF/OTF font (face index 0).')
P.add_argument('--font-semibold', type=pathlib.Path, help='Semibold TTF/OTF font (face index 0).')
P.add_argument('--preview', action='store_true', help='Render a storyboard without the full video.')
P.add_argument('--preview-opening-pareto', action='store_true',
               help='Render only a proposed opening layout with the AntMaze Pareto plot.')
P.add_argument('--preview-opening-decoding', action='store_true',
               help='Render a still of the current opening with decoded subgoals and the Pareto plot.')
A = P.parse_args()
ROOT = A.repo.expanduser().resolve()
PRODUCTION = ROOT / 'video-production'
OUT = (A.out or PRODUCTION / 'output').expanduser().resolve()
A.teaser = (A.teaser or PRODUCTION / 'sources/hierarchical_planning_sliding_new.mp4').expanduser().resolve()
DEFAULT_FONT = pathlib.Path('/System/Library/Fonts/Avenir Next.ttc')
REGULAR_FONT = (A.font_regular or DEFAULT_FONT).expanduser().resolve()
SEMIBOLD_FONT = (A.font_semibold or DEFAULT_FONT).expanduser().resolve()
for font_path in (REGULAR_FONT, SEMIBOLD_FONT):
 if not font_path.is_file():
  P.error('Font not found: ' + str(font_path) +
          '. Exact typography uses macOS Avenir Next. On other systems, pass both '
          '--font-regular and --font-semibold with local TTF/OTF files.')
FF = imageio_ffmpeg.get_ffmpeg_exe()
W,H,FPS=1920,1080,30
INK='#152b3a'; MUTED='#627581'; BG='#f5f6f3'; BLUE='#286494'; TEAL='#158977'; PURPLE='#8056a4'; GOLD='#cf9353'; DARK='#102736'
fonts={}
def font(s,b=False):
 k=(s,b)
 if k not in fonts:
  path = SEMIBOLD_FONT if b else REGULAR_FONT
  custom = A.font_semibold if b else A.font_regular
  fonts[k] = ImageFont.truetype(str(path),s,index=0 if custom else (2 if b else 7))
 return fonts[k]
def tx(d,xy,s,size=34,color=INK,b=False,anchor=None):d.text(xy,s,font=font(size,b),fill=color,anchor=anchor,stroke_width=0)
def ease(t):return 1-(1-max(0,min(1,t)))**3
def line(d,xy,col=INK,width=2):d.line(xy,fill=col,width=width)
def base(chapter,dark=False):
 im=Image.new('RGB',(W,H),DARK if dark else BG);d=ImageDraw.Draw(im)
 tx(d,(96,47),'H–JEPA',30,'#f5f6f3' if dark else INK,True)
 tx(d,(1824,52),chapter.upper(),22,'#9ab0bb' if dark else MUTED,anchor='ra')
 line(d,(96,100,1824,100),'#2d4452' if dark else '#dae0df')
 return im
def appear(im,t,t0,draw,dur=.45,rise=18):
 # Fade an element in from t0 while it rises into place.
 a=ease((t-t0)/dur)
 if a<=0:return im
 layer=im.copy();draw(ImageDraw.Draw(layer),layer,round(rise*(1-a)))
 return layer if a>=1 else Image.blend(im,layer,a)
def supline(d,y,parts,size,col):
 # Centered line of (text, superscript) parts.
 f,fs=font(size),font(size);sw=[d.textlength(p,font=fs)+2 if p else 0 for _,p in parts]
 x=960-sum(d.textlength(s,font=f)+w for (s,_),w in zip(parts,sw))/2
 for (s,p),w in zip(parts,sw):
  d.text((x,y),s,font=f,fill=col);x+=d.textlength(s,font=f)
  if p:d.text((x+1,y),p,font=fs,fill=col)
  x+=w
def footer(im,t):
 d=ImageDraw.Draw(im);d.rectangle((0,1075,round(W*t/DURATION),1079),fill=TEAL)
TITLES={
 'opening':'H-JEPA: Hierarchical World Models for Visual Planning',
 'learn':'Learning Predictive Hierarchies Across Timescales',
 'abstract':'Higher Levels Abstract Away Fast Details',
 'plan':'Hierarchical Planning with H-JEPA',
 'execute':'Planning in Action Across Four Environments',
 'results':'More Successful Planning with Less Compute',
 'idm':'Inverse Dynamics Keeps the Robot in the Latent',
 'droid':'Planning from Real-World Robot Video',
 'ending':'H-JEPA: Learn Abstractions. Plan Ahead.'
}
def heading(im,name):
 # A single headline, with identical typography and placement on every slide.
 tx(ImageDraw.Draw(im),(96,165),TITLES[name],62,INK,True)
def pill(d,x,y,label,col=TEAL,width=None):
 width=width or int(d.textlength(label,font=font(25,True)))+44
 d.rounded_rectangle((x,y,x+width,y+49),radius=24,fill=col);tx(d,(x+22,y+7),label,25,'white',True)
def smallcap(im,s):tx(ImageDraw.Draw(im),(960,1007),s,29,MUTED,anchor='ma')
def headerlabels(im,y,x=456,w=1344):
 d=ImageDraw.Draw(im)
 for j,(s,c) in enumerate([('Start',MUTED),('LeWM · flat',MUTED),('H-JEPA',TEAL),('Goal',MUTED)]):tx(d,(x+j*w/4+12,y),s,27,c,True)
def stepbar(im,labels,active,y=964):
 d=ImageDraw.Draw(im);gap=20; bw=(1728-gap*(len(labels)-1))/len(labels)
 for i,l in enumerate(labels):
  x=96+i*(bw+gap);c=TEAL if i==active else '#e5eae7';d.rounded_rectangle((x,y,x+bw,y+62),radius=13,fill=c)
  tx(d,(x+bw/2,y+13),f'{i+1:02d}  {l}',27,'white' if i==active else MUTED,True,anchor='ma')
class Clip:
 def __init__(self,path,size,seconds,crop=None,speed=1,start=0):
  self.path=str(ROOT/path);self.size=size;self.seconds=seconds;self.crop=crop;self.speed=speed;self.start=start;self.p=None;self.last=None
 def filt(self):
  v=[]
  if self.crop:v.append('crop='+':'.join(map(str,self.crop)))
  v.extend([f'setpts=(PTS-STARTPTS)/{self.speed}',f'fps={FPS}',f'scale={self.size[0]}:{self.size[1]}:flags=lanczos','tpad=stop_mode=clone:stop_duration=20'])
  return ','.join(v)
 def open(self):
  self.p=subprocess.Popen([FF,'-v','error','-ss',str(self.start),'-i',self.path,'-vf',self.filt(),'-t',str(self.seconds),'-f','rawvideo','-pix_fmt','rgb24','-'],stdout=subprocess.PIPE,stderr=subprocess.DEVNULL)
 def frame(self,t=None):
  if t is not None:
   r=subprocess.run([FF,'-v','error','-ss',str(self.start+t*self.speed),'-i',self.path,'-vf',(','.join(['crop='+':'.join(map(str,self.crop))] if self.crop else [])+(',' if self.crop else '')+f'scale={self.size[0]}:{self.size[1]}'),'-frames:v','1','-f','rawvideo','-pix_fmt','rgb24','-'],capture_output=True)
   data=r.stdout
  else:data=self.p.stdout.read(self.size[0]*self.size[1]*3)
  if len(data)!=self.size[0]*self.size[1]*3:
   raise RuntimeError('Could not decode a complete frame from ' + self.path)
  self.last=Image.frombytes('RGB',self.size,data)
  return self.last
 def close(self):
  if self.p:self.p.stdout.close();self.p.terminate();self.p.wait()
SPECS=[('opening',10),('learn',12),('abstract',8),('plan',16),('execute',7),('results',8),('idm',12),('droid',8),('ending',7)]
DURATION=sum(duration for _,duration in SPECS)
def clips(name):
 if name=='opening':return [(Clip(A.teaser,(1606,1080),10,speed=2.5,start=2),(0,0))]
 if name=='idm':return [(Clip(PRODUCTION/'sources/idm-schema.mp4',(1390,663),12,(2340,1116,0,100),speed=17/12),(265,294))]
 if name=='droid':return [(Clip('assets/videos/scene-diversity.mp4',(810,238),8,(784,230,40,318),speed=1),(96,314))]
 if name=='learn':return [(Clip(PRODUCTION/'sources/hjepa-training.mp4',(1390,660),12,(1850,880,35,105),speed=14/12),(265,294))]
 if name=='abstract':return [(Clip('assets/videos/selective_abstraction_lvl4.mp4',(1680,698),8,speed=1),(120,303))]
 if name=='plan':return [(Clip(PRODUCTION/'sources/hjepa-planning.mp4',(1450,666),16,(1850,850,35,110),speed=18/16),(235,287))]
 if name=='execute':return [
  (Clip('assets/videos/executions/fourroom/fourroom_ep28.mp4',(840,269),7,(800,256,272,48),speed=8.5/7),(96,344)),
  (Clip('assets/videos/executions/ant/ant_ep35.mp4',(840,269),7,(800,256,272,48),speed=13.17/7),(984,344)),
  (Clip('assets/videos/executions/pusht/pusht_ep7.mp4',(840,269),7,(800,256,272,48),speed=7.47/7),(96,735)),
  (Clip('assets/videos/executions/cube/cube_30_ep2.mp4',(840,269),7,(800,256,272,48),speed=1),(984,735))]
 return []
figures={}
def figure(name,size,crop=None):
 key=(name,size,crop)
 if key not in figures:
  img=Image.open(ROOT/'assets/figures'/name).convert('RGB')
  if crop:img=img.crop(crop)
  figures[key]=img.resize(size,Image.Resampling.LANCZOS)
 return figures[key]
def opening_arrow(d,x,y):
 line(d,(x,y,x+23,y),MUTED,3)
 line(d,(x+7,y-7,x,y,x+7,y+7),MUTED,3)

def compose_opening(frame):
 im=base('Learn abstractions. Plan ahead.');d=ImageDraw.Draw(im)
 heading(im,'opening')
 tx(d,(560,304),'Decoded subgoals across three levels',31,INK,True,anchor='ma')
 tx(d,(1144,331),'Higher success with less compute',31,INK,True)
 labels=['Shorter horizon','Intermediate horizon','Longer horizon']
 # L1, L2, L3 read left to right; refinement flows leftward from L3 to L1.
 for i,(x,sy) in enumerate(zip((172,448,724),(740,412,84))):
  tx(d,(x+112,352),labels[i],22,MUTED,anchor='ma')
  tile=frame.crop((1282,sy,1578,sy+296))
  im.paste(tile.resize((224,224),Image.Resampling.LANCZOS),(x,386))
  if i<2:opening_arrow(d,x+238,498)
 # All views use one source frame, keeping decoded subgoals and maze in sync.
 maze=frame.crop((32,84,1254,956))
 im.paste(maze.resize((560,400),Image.Resampling.LANCZOS),(280,626))
 im.paste(figure('overview.png',(680,698),crop=(1450,60,2375,1010)),(1144,375))
 tx(d,(1144,295),'VISUAL ANTMAZE',21,MUTED,True)
 tx(d,(96,1033),'Illustrative planning · recorded observations and decoded states · 2.5× playback',20,MUTED)
 return im

def compose(name,t,frames):
 if name=='opening':return compose_opening(frames[0][0])
 dark=False; im=base({'opening':'Hierarchical world models','learn':'01 / Learn','abstract':'02 / Abstract','plan':'03 / Plan','execute':'04 / Execute','results':'05 / Results · Simulation','idm':'06 / Real-world video · Method','droid':'07 / Results · Real-world video','ending':'Explore the project'}[name],dark);d=ImageDraw.Draw(im)
 for f,pos in frames:
  if f is not None and name!='droid':im.paste(f,pos)
 heading(im,name)
 if name=='learn':
  tx(d,(98,247),'Each higher level learns to predict farther ahead.',30,MUTED)
  stepbar(im,['Encode observations + actions','Build the next level','Train jointly'],min(2,int(t/(12/14*4))))
 elif name=='abstract':
  tx(d,(98,249),'AntMaze retains position; FourRoom retains the controlled agent.',30,MUTED)
  # Native labels remain visible; selected columns are outlined gently.
  d=ImageDraw.Draw(im)
  if t>2:
   x=120+round(1250/1560*1680);d.rounded_rectangle((x,308,1795,1000),radius=10,outline=PURPLE,width=3)
  tx(d,(960,1030),'Decoded representations for visualization; decoders are not used for planning.',24,MUTED,anchor='ma')
 elif name=='plan':
  tx(d,(98,247),'High-level predictions become subgoals for the level below.',30,MUTED)
  phase=0 if t<4/1.125 else 1 if t<8/1.125 else 2 if t<14/1.125 else 3
  stepbar(im,['Encode start + goal','Plan toward the goal','Refine a subgoal','Act, observe, replan'],phase)
 elif name=='execute':
  for x,y,label,speed in [(96,264,'FourRoom','1.2× playback'),(984,264,'Visual AntMaze','1.9× playback'),(96,655,'Push-T','1.1× playback'),(984,655,'Cube','Original playback')]:
   tx(d,(x,y),label,30,INK,True);tx(d,(x+840,y+6),speed,23,MUTED,anchor='ra')
   for j,(model,col) in enumerate([('LeWM · flat',MUTED),('H-JEPA',TEAL),('Goal',MUTED)]):
    tx(d,(x+j*285+8,y+44),model,25,col,True)
  line(d,(96,639,1824,639),'#d4dddb')
  tx(d,(96,1025),'Example executions · LeWM and H-JEPA share the same goal within each environment.',23,MUTED)
 elif name=='results':
  tx(d,(98,249),'Success versus planner compute across four simulated environments.',30,MUTED)
  im.paste(figure('planning-results-pareto.png',(1728,514)),(96,348))
  d=ImageDraw.Draw(im)
  tx(d,(96,912),'Three levels lead on navigation and Cube; two levels work best on Push-T.',32,INK,True)
  tx(d,(96,974),'Bold curves show Pareto fronts. Error bars: one standard error over three seeds.',26,MUTED)
  tx(d,(96,1023),'Source: H-JEPA paper · h-jepa.com',23,MUTED)
 elif name=='idm':
  tx(d,(98,247),'Each level also predicts the action linking consecutive states.',30,MUTED)
  phase=sum(t>=s*12/17 for s in (4,8,13))
  stepbar(im,['Build the hierarchy','Pair consecutive states','Regress the action','Add to the objective'],phase)
 elif name=='droid':
  tx(d,(98,249),'DROID · Inverse-dynamics supervision + a learned hierarchy.',30,MUTED)
  clip,pos=frames[0]
  im=appear(im,t,0,lambda d,L,o:L.paste(clip,(pos[0],pos[1]+o)))
  im=appear(im,t,.4,lambda d,L,o:tx(d,(982,325+o),'Diverse scenes. More faithful plans.',38,INK,True))
  im=appear(im,t,.8,lambda d,L,o:(tx(d,(984,393+o),'Offline evaluation of end-effector paths',30,MUTED),tx(d,(984,438+o),'against expert trajectories.',30,MUTED)))
  im=appear(im,t,1.2,lambda d,L,o:tx(d,(984,510+o),'Higher Fréchet fidelity is better.',27,TEAL,True))
  # Ablation bars wipe in left to right: no IDM, + IDM, HWM, H-JEPA.
  fig,AX=figure('droid-ablation.png',(850,366)),118
  im=appear(im,t,1.8,lambda d,L,o:(tx(d,(96,579+o),'Inverse dynamics and hierarchy',29,INK,True),L.paste(fig.crop((0,0,AX,366)),(96,626+o))))
  w=max(0,min(1,(t-2.3)/1.8));w=AX+round((850-AX)*w*w*(3-2*w))
  if t>2.3:im.paste(fig.crop((0,0,w,366)),(96,626))
  im=appear(im,t,4.1,lambda d,L,o:(tx(d,(1000,579+o),'Fidelity versus planner compute',29,INK,True),L.paste(figure('droid-compute.png',(824,407)),(1000,616+o))),dur=.6)
  im=appear(im,t,5.0,lambda d,L,o:tx(d,(96,1034),'IDM: inverse dynamics. Offline path fidelity; frozen-encoder references use their native 1 fps, ours use 5 fps.',22,MUTED),rise=0)
 elif name=='ending':
  tx(d,(960,497),'End-to-End Learning of Hierarchical World Models',36,MUTED,anchor='ma');tx(d,(960,548),'for Visual Planning',36,MUTED,anchor='ma')
  d.rounded_rectangle((656,649,1264,743),radius=20,fill='#77d8c4');tx(d,(960,664),'h-jepa.com',48,DARK,True,anchor='ma')
  tx(d,(960,779),'Paper + code',29,MUTED,anchor='ma')
  supline(d,872,[('Wancong Zhang','*'),(' · Basile Terver','*'),(' · Michael Rabbat','')],28,MUTED)
  supline(d,917,[('Yann LeCun','†'),(' · Randall Balestriero','†')],28,MUTED)
  supline(d,972,[('','*'),('Equal contribution    ',''),('','†'),('Equal advising','')],22,MUTED)
  tx(d,(960,1012),'NYU · Advanced Machine Intelligence · INRIA Paris · Brown University',23,MUTED,anchor='ma')
 return im

def soundtrack():
 sr=48000;dur=DURATION;n=sr*dur;aud=np.zeros((n,2),np.float32)
 def add(sig,start,pan=0):
  i=int(start*sr);end=min(n,i+len(sig));sig=sig[:end-i]
  if i<n:
   aud[i:end,0]+=sig*np.sqrt((1-pan)/2);aud[i:end,1]+=sig*np.sqrt((1+pan)/2)
 def tone(hz,length,kind='pad'):
  t=np.arange(int(length*sr))/sr
  if kind=='pad':
   env=np.minimum(t/1.6,1)*np.minimum((length-t)/2.2,1)
   return .055*env*(np.sin(2*np.pi*hz*t)+.28*np.sin(2*np.pi*hz*2.003*t))
  env=(1-np.exp(-t*70))*np.exp(-t*2.5)
  return .028*env*(np.sin(2*np.pi*hz*t)+.23*np.sin(2*np.pi*hz*2*t))
 chords=[[146.832,220,277.183,329.628],[130.813,196,246.942,293.665],[164.814,246.942,329.628,391.995],[110,164.814,220,277.183]]
 for i,start in enumerate(np.arange(0,dur,7)):
  chord=chords[i%4]
  for j,hz in enumerate(chord):add(tone(hz,9),start,(j-1.5)/4)
 for k,start in enumerate(np.arange(0,dur,.625)):
  chord=chords[int(start//7)%4];add(tone(chord[[0,2,1,3,2,1,3,1][k%8]]*2,2,'pluck'),start,(-.25 if k%2 else .25))
  if start>6 and start<dur-7 and k%2==0:
   t=np.arange(int(.20*sr))/sr;freq=52+45*np.exp(-t*35);sig=.048*np.sin(2*np.pi*np.cumsum(freq)/sr)*np.exp(-t*23);add(sig,start)
 fade=np.minimum(np.arange(n)/sr/3,1)*np.minimum((dur-np.arange(n)/sr)/4,1)
 aud*=fade[:,None]; aud=np.tanh(aud)*.6
 with wave.open(str(OUT/'soundtrack.wav'),'wb') as f:f.setnchannels(2);f.setsampwidth(2);f.setframerate(sr);f.writeframes((aud*32767).astype('<i2').tobytes())

def opening_pareto_preview(include_decoding=False):
 # Share the current layout with the movie so the approved still cannot drift.
 if include_decoding:
  frames = [(clip.frame(t=4.8), pos) for clip, pos in clips('opening')]
  im = compose('opening', 4.8, frames)
  footer(im, 4.8)
  target = OUT / 'opening-pareto-decoding-preview.png'
  im.save(target)
  print('PREVIEW', target, flush=True)
  return
 # Retain the earlier maze-only layout as a preview-only alternative.
 im = base('Hierarchical world models')
 heading(im, 'opening')
 d = ImageDraw.Draw(im)
 tx(d, (596, 269), 'Hierarchical MPC with subgoals across timescales', 23, MUTED, True, anchor='ma')
 # At source t=14s the three subgoal markers and the destination are visible.
 tx(d, (1489, 269), 'Visual AntMaze: Success versus planning compute', 23, MUTED, True, anchor='ma')
 maze = Clip(A.teaser, (1000, 714), 10, (1222, 872, 32, 84), speed=2.5, start=2)
 im.paste(maze.frame(t=4.8), (96, 305))
 im.paste(figure('overview.png', (670, 688), crop=(1450, 60, 2375, 1010)), (1154, 318))
 footer(im, 4.8)
 target = OUT / 'opening-pareto-preview.png'
 im.save(target)
 print('PREVIEW', target, flush=True)

required = {pathlib.Path(clip.path) for name, _ in SPECS for clip, _ in clips(name)}
required.update(ROOT/'assets/figures'/name for name in (
 'overview.png', 'planning-results-pareto.png', 'droid-ablation.png', 'droid-compute.png'))
required.add(PRODUCTION/'captions.srt')
missing = sorted(str(path) for path in required if not path.is_file())
if missing:
 P.error('Missing production inputs:\n' + '\n'.join(missing))
# Fail early if an alternate font would clip one of the approved titles.
for title in TITLES.values():
 if font(62, True).getlength(title) > W - 192:
  P.error('Selected semibold font makes a title too wide: ' + title)
OUT.mkdir(parents=True,exist_ok=True)

if A.preview_opening_decoding:
 opening_pareto_preview(include_decoding=True)
elif A.preview_opening_pareto:
 opening_pareto_preview()
elif A.preview:
 sheet=Image.new('RGB',(960*2,540*4),'white')
 for i,(name,dur) in enumerate(SPECS):
  cc=clips(name);t=dur*.68; im=compose(name,t,[(c.frame(t),pos) for c,pos in cc]);im.save(OUT/f'preview_{name}.jpg',quality=93);sheet.paste(im.resize((960,540)),((i%2)*960,(i//2)*540))
 sheet.save(OUT/'storyboard.jpg',quality=95);print('Preview complete',flush=True)
else:
 start=0
 for name,dur in SPECS:
  target=OUT/f'{name}.mp4'
  cc=clips(name)
  for c,_ in cc:c.open()
  log=open(OUT/f'{name}.log','w')
  enc=subprocess.Popen([FF,'-y','-v','warning','-f','rawvideo','-pix_fmt','rgb24','-s','1920x1080','-r',str(FPS),'-i','-','-an','-c:v','libx264','-preset','fast','-crf','18','-pix_fmt','yuv420p','-movflags','+faststart',str(target)],stdin=subprocess.PIPE,stderr=log)
  print('Rendering',name,dur,'seconds',flush=True)
  for f in range(dur*FPS):
   t=f/FPS;im=compose(name,t,[(c.frame(),pos) for c,pos in cc]);footer(im,start+t)
   # Quick, subtle dip from the section's background; no long blank transitions.
   if t<.23:im=Image.blend(base('',False),im,ease(t/.23))
   enc.stdin.write(im.tobytes())
  enc.stdin.close();code=enc.wait();log.close()
  for c,_ in cc:c.close()
  if code:raise RuntimeError('Encoding failed: '+name)
  start+=dur
 soundtrack()
 (OUT/'concat.txt').write_text('\n'.join("file '"+f'{name}.mp4'+"'" for name,_ in SPECS))
 subprocess.run([FF,'-y','-v','warning','-f','concat','-safe','0','-i',str(OUT/'concat.txt'),'-i',str(OUT/'soundtrack.wav'),'-c:v','copy','-af','volume=9dB','-c:a','aac','-b:a','192k','-t',str(DURATION),'-movflags','+faststart','-metadata','title=H-JEPA | Hierarchical World Models for Visual Planning','-metadata','comment=Repository research footage; original synthesized instrumental soundtrack.',str(OUT/'hjepa_demo.mp4')],check=True)
 shutil.copyfile(PRODUCTION/'captions.srt', OUT/'hjepa_demo.srt')
 print('FINAL',OUT/'hjepa_demo.mp4',flush=True)
