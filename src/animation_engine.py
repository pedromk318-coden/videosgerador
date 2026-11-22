#!/usr/bin/env python3
"""Offline procedural 2D/2.5D animation renderer. No AI or paid services."""
from __future__ import annotations
import argparse, hashlib, json, math, random, shutil, subprocess, tempfile
from pathlib import Path
from PIL import Image, ImageDraw, ImageFont

W, H, FPS = 480, 854, 20
PALETTES = {
    "fantasia": ((12, 25, 54), (69, 112, 139), (255, 203, 119)),
    "aventura": ((13, 37, 55), (67, 125, 137), (255, 190, 100)),
    "mistério": ((14, 19, 39), (65, 73, 111), (190, 207, 255)),
    "drama": ((42, 35, 48), (128, 91, 91), (255, 205, 160)),
    "ficção científica": ((5, 18, 43), (26, 82, 112), (101, 231, 255)),
    "sci-fi": ((5, 18, 43), (26, 82, 112), (101, 231, 255)),
    "terror": ((12, 10, 20), (65, 43, 58), (215, 145, 128)),
    "cinematográfico": ((12, 27, 47), (64, 103, 124), (255, 205, 133)),
}
def run(args):
    subprocess.run(args, check=True, stdout=subprocess.DEVNULL, stderr=subprocess.PIPE)
def font(size):
    for p in ("/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf",
              "/usr/share/fonts/truetype/liberation2/LiberationSans-Regular.ttf"):
        if Path(p).exists(): return ImageFont.truetype(p, size)
    return ImageFont.load_default()
def mix(a,b,t):
    return tuple(int(a[i]*(1-t)+b[i]*t) for i in range(3))
def keywords(scene):
    return (str(scene.get("title",""))+" "+str(scene.get("text",""))+" "+
            str(scene.get("narration",""))+" "+str(scene.get("visual_prompt",""))).lower()
def environment(words, genre):
    if any(k in words for k in ("floresta","árvore","bosque","selva","forest")): return "forest"
    if any(k in words for k in ("castelo","reino","dragão","medieval","cavaleiro")): return "castle"
    if any(k in words for k in ("espaço","planeta","nave","robô","futur","galáxia")) or "sci" in genre: return "space"
    if any(k in words for k in ("mar","praia","oceano","navio","água","rio")): return "coast"
    if any(k in words for k in ("cidade","rua","prédio","carro","vila")): return "city"
    return "valley"
def draw_background(im, env, palette, t, rng):
    d=ImageDraw.Draw(im)
    top,bottom,glow=palette
    for y in range(H):
        d.line((0,y,W,y), fill=mix(top,bottom,y/H))
    # distant atmosphere and celestial light
    sunx=int(W*.72 + math.sin(t*.16)*9); suny=int(H*.19)
    for r,alpha in ((92,18),(66,24),(42,35)):
        d.ellipse((sunx-r,suny-r,sunx+r,suny+r), fill=(*glow,alpha))
    d.ellipse((sunx-22,suny-22,sunx+22,suny+22), fill=glow)
    # stars / windows stay deterministic per scene and drift slightly
    for x,y,r in rng.stars:
        xx=int((x-t*3) % W)
        d.ellipse((xx,y,xx+r,y+r), fill=(235,242,255))
    # two distant parallax mountain layers
    for layer, base, amp, col, speed in ((0,H*.56,78,(44,69,91),.35),(1,H*.67,58,(25,45,65),.7)):
        pts=[(0,H)]
        for x in range(-30,W+50,35):
            yy=base+math.sin((x+t*speed)/83)*amp+math.sin((x+t*speed)/31)*amp*.22
            pts.append((x,int(yy)))
        pts.append((W,H))
        d.polygon(pts, fill=col)
    if env=="forest":
        for layer in (0,1):
            shift=int(t*(8+layer*13))%100
            for x in range(-100,W+100,92):
                xx=x-shift
                base=int(H*(.82 if layer else .73)); ht=180 if layer else 135
                c=(8,31,35) if layer else (17,55,57)
                d.rectangle((xx-5,base-ht//3,xx+5,base),fill=c)
                d.ellipse((xx-48,base-ht,xx+48,base-ht//4),fill=c)
                d.ellipse((xx-34,base-ht-30,xx+34,base-ht//3),fill=c)
    elif env=="castle":
        for x,hh in ((30,260),(145,190),(300,230),(405,170)):
            bx=x-int(t*7)%35
            d.rectangle((bx,H*.52,bx+75,H*.82),fill=(25,31,48))
            d.polygon(((bx-8,H*.52),(bx+37,H*.40),(bx+83,H*.52)),fill=(31,35,54))
            for wx in (bx+18,bx+48):
                d.rounded_rectangle((wx,H*.59,wx+10,H*.67),radius=5,fill=glow)
    elif env=="city":
        for x in range(-10,W+30,65):
            bh=120+((x*17)%145); bx=x-int(t*10)%65
            d.rectangle((bx,H*.76-bh,bx+43,H*.76),fill=(17,29,48))
            for wy in range(int(H*.78-bh+12),int(H*.74),25):
                for wx in (bx+9,bx+25):
                    d.rectangle((wx,wy,wx+6,wy+9),fill=(190,174,123,190))
    elif env=="space":
        for x in (55,360):
            d.ellipse((x-55,H*.58-55,x+55,H*.58+55),outline=(124,188,216),width=3)
            d.ellipse((x-45,H*.58-45,x+45,H*.58+45),fill=(34,67,92))
            d.ellipse((x-20,H*.58-65,x+60,H*.58+20),fill=(44,77,104))
    elif env=="coast":
        d.rectangle((0,int(H*.68),W,H),fill=(17,66,91))
        for j in range(5):
            yy=int(H*.70+j*34+math.sin(t*2+j)*5)
            d.arc((-60,yy-18,W+60,yy+18),0,180,fill=(107,178,194),width=2)
    else:
        d.polygon(((0,H*.75),(W*.23,H*.58),(W*.45,H*.76),(W*.68,H*.55),(W,H*.75),(W,H)),fill=(22,48,57))
    # foreground silhouettes move fastest to create depth
    shift=int(t*24)%180
    for x in range(-180,W+180,180):
        xx=x-shift
        d.ellipse((xx-48,H*.79,xx+48,H*.98),fill=(7,22,28))
        d.rectangle((xx-4,H*.82,xx+4,H),fill=(7,22,28))
def draw_character(im, t, pose, seed, palette):
    d=ImageDraw.Draw(im)
    cx=W*.50 + math.sin(t*.55+seed)*13
    ground=H*.83
    moving=pose in ("walk","run")
    speed=8 if pose=="run" else 4
    phase=t*speed
    stride=math.sin(phase)* (31 if pose=="run" else 19) if moving else 0
    bob=abs(math.sin(phase*2))*9 if moving else math.sin(t*1.8)*2
    # ground shadow
    d.ellipse((cx-58,ground-5,cx+58,ground+13),fill=(5,12,18))
    # legs and shoes, animated around hip
    hip_y=ground-105-bob
    legw=16
    for side in (-1,1):
        ang=math.sin(phase+(0 if side<0 else math.pi))* (0.55 if pose=="run" else .32) if moving else 0
        knee_x=cx+side*13+math.sin(ang)*24
        knee_y=hip_y+52+abs(math.sin(ang))*8
        foot_x=knee_x+math.sin(ang)*27
        foot_y=ground-8
        d.line((cx+side*12,hip_y,knee_x,knee_y,foot_x,foot_y),fill=(29,38,55),width=17,joint="curve")
        d.ellipse((foot_x-14,foot_y-7,foot_x+17,foot_y+5),fill=(13,18,27))
    # torso, neck and arms
    shirt=(42+(seed%45),82+(seed%40),119+(seed%35))
    d.rounded_rectangle((cx-31,hip_y-80-bob,cx+31,hip_y+5),radius=19,fill=shirt,outline=(170,197,208),width=2)
    d.rectangle((cx-9,hip_y-96-bob,cx+9,hip_y-75-bob),fill=(174,117,83))
    for side in (-1,1):
        swing=math.sin(phase+(math.pi if side<0 else 0))*(27 if moving else 7)
        shoulder=(cx+side*27,hip_y-67-bob)
        elbow=(cx+side*39+swing*.45,hip_y-31-bob)
        hand=(cx+side*39+swing,hip_y+3-bob)
        d.line((shoulder,elbow,hand),fill=shirt,width=14,joint="curve")
        d.ellipse((hand[0]-7,hand[1]-7,hand[0]+7,hand[1]+7),fill=(177,119,86))
    # head and simple expressive face
    head_y=hip_y-139-bob
    d.ellipse((cx-30,head_y-32,cx+30,head_y+35),fill=(190,137,103),outline=(69,48,43),width=2)
    d.pieslice((cx-31,head_y-36,cx+31,head_y+8),180,360,fill=(35,25,24))
    eye_y=head_y+2
    d.ellipse((cx-13,eye_y-3,cx-8,eye_y+4),fill=(20,22,28))
    d.ellipse((cx+8,eye_y-3,cx+13,eye_y+4),fill=(20,22,28))
    d.arc((cx-8,head_y+8,cx+9,head_y+20),5,165,fill=(80,37,37),width=2)
    # small rim light
    d.arc((cx-33,head_y-32,cx+33,head_y+36),205,290,fill=palette[2],width=3)
def render_frame(scene, idx, frame, duration, seed, genre, rng):
    t=frame/FPS
    words=keywords(scene); env=environment(words,genre)
    palette=PALETTES.get(genre.lower(),PALETTES["cinematográfico"])
    im=Image.new("RGB",(W,H))
    # Independent seeded star field, stored on RNG for consistent frame-to-frame layout.
    if not hasattr(rng,"stars"):
        rng.stars=[(rng.randrange(W),rng.randrange(int(H*.52)),rng.choice((1,2,3))) for _ in range(70)]
    draw_background(im,env,palette,t,rng)
    if any(k in words for k in ("corre","foge","persegue","corrida","run","escape")): pose="run"
    elif any(k in words for k in ("caminha","anda","segue","viaja","walk")): pose="walk"
    else: pose="idle"
    draw_character(im,t,pose,seed,palette)
    # cinematic darkening at top and bottom, preserving clean central action
    overlay=Image.new("RGBA",(W,H),(0,0,0,0)); od=ImageDraw.Draw(overlay)
    for y in range(100):
        a=int(85*(1-y/100))
        od.line((0,y,W,y),fill=(0,0,0,a))
        od.line((0,H-y,W,H-y),fill=(0,0,0,a))
    return Image.alpha_composite(im.convert("RGBA"),overlay).convert("RGB")
def main():
    ap=argparse.ArgumentParser()
    ap.add_argument("--input",default="scenes.json"); ap.add_argument("--output",default="output/video.mp4")
    args=ap.parse_args()
    if not shutil.which("ffmpeg"): raise SystemExit("FFmpeg não encontrado.")
    data=json.loads(Path(args.input).read_text(encoding="utf-8"))
    scenes=data.get("scenes",[])
    if not scenes: raise SystemExit("O roteiro não gerou nenhuma cena.")
    genre=str(data.get("genre","cinematográfico"))
    out=Path(args.output); out.parent.mkdir(parents=True,exist_ok=True)
    title=str(data.get("title",""))
    with tempfile.TemporaryDirectory() as tmp:
        root=Path(tmp); clips=[]
        for i,scene in enumerate(scenes,1):
            duration=max(2.0,min(30.0,float(scene.get("duration",6))))
            count=max(1,int(duration*FPS))
            seed=int(hashlib.sha256((title+str(i)).encode()).hexdigest()[:8],16)
            rng=random.Random(seed)
            frames_dir=root/f"scene_{i:03d}"; frames_dir.mkdir()
            for n in range(count):
                frame=render_frame(scene,i,n,duration,seed,genre,rng)
                frame.save(frames_dir/f"frame_{n:06d}.jpg",quality=88,optimize=False)
            clip=root/f"clip_{i:03d}.mp4"
            run(["ffmpeg","-hide_banner","-loglevel","error","-y","-framerate",str(FPS),
                 "-i",str(frames_dir/"frame_%06d.jpg"),"-c:v","libx264","-preset","ultrafast",
                 "-crf","24","-pix_fmt","yuv420p","-an",str(clip)])
            clips.append(clip)
            print(f"Cena {i}/{len(scenes)} renderizada ({duration:.1f}s)")
        concat=root/"concat.txt"
        concat.write_text("".join(f"file '{c.as_posix()}'\n" for c in clips),encoding="utf-8")
        run(["ffmpeg","-hide_banner","-loglevel","error","-y","-f","concat","-safe","0",
             "-i",str(concat),"-c:v","libx264","-preset","ultrafast","-crf","23",
             "-pix_fmt","yuv420p","-movflags","+faststart",str(out)])
    print(f"Vídeo offline concluído: {out}")
if __name__=="__main__": main()
