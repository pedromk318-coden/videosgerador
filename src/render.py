#!/usr/bin/env python3
"""Procedural cinematic scene generator and vertical MP4 renderer (no external image API)."""
from __future__ import annotations
import argparse, hashlib, json, math, shutil, subprocess, tempfile, random
from pathlib import Path
from PIL import Image, ImageDraw, ImageFont, ImageFilter

def font(size, bold=True):
    candidates = (["/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"] if bold else ["/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf"])
    for p in candidates:
        if Path(p).exists(): return ImageFont.truetype(p, size)
    return ImageFont.load_default()

def rgb(value):
    value=value.lstrip("#"); return tuple(int(value[i:i+2],16) for i in (0,2,4))

def gradient(size, top, bottom):
    w,h=size; im=Image.new("RGB",size); pix=im.load(); a,b=rgb(top),rgb(bottom)
    for y in range(h):
        t=y/max(1,h-1); c=tuple(int(a[k]*(1-t)+b[k]*t) for k in range(3))
        for x in range(w): pix[x,y]=c
    return im

def wrap(draw, text, f, maxw):
    lines=[]; current=""
    for word in str(text).split():
        test=(current+" "+word).strip()
        if draw.textbbox((0,0),test,font=f)[2] <= maxw: current=test
        else:
            if current: lines.append(current)
            current=word
    if current: lines.append(current)
    return lines

def make_art(scene, size, index, idea):
    w,h=size
    seed=int(hashlib.sha256((idea+str(index)+scene.get("title","")).encode()).hexdigest()[:8],16)
    rng=random.Random(seed)
    palettes=[("#08162b","#387c9a"),("#1d1239","#8c477b"),("#201b16","#ba7442"),("#061c24","#4a9a80"),("#101a39","#596da9")]
    top,bottom=palettes[seed%len(palettes)]
    im=gradient(size,top,bottom).convert("RGBA")
    d=ImageDraw.Draw(im,"RGBA")
    # Soft glow / celestial body
    cx=int(w*rng.uniform(.25,.8)); cy=int(h*rng.uniform(.15,.36)); rad=int(w*rng.uniform(.08,.15))
    glow=Image.new("RGBA",size,(0,0,0,0)); gd=ImageDraw.Draw(glow)
    gd.ellipse((cx-rad*2,cy-rad*2,cx+rad*2,cy+rad*2),fill=(255,218,170,45))
    glow=glow.filter(ImageFilter.GaussianBlur(rad)); im=Image.alpha_composite(im,glow); d=ImageDraw.Draw(im,"RGBA")
    d.ellipse((cx-rad,cy-rad,cx+rad,cy+rad),fill=(255,229,186,230))
    # stars
    for _ in range(90):
        x=rng.randrange(w); y=rng.randrange(int(h*.62))
        d.ellipse((x,y,x+2,y+2),fill=(255,255,255,rng.randrange(80,190)))
    # layered mountains
    for layer in range(4):
        base=int(h*(.48+layer*.10)); points=[(0,base)]
        x=0
        while x<w:
            peakx=min(w,x+rng.randint(int(w*.08),int(w*.22)))
            peaky=base-rng.randint(int(h*.04),int(h*.19))
            points.extend([(x,base),(peakx,peaky),(min(w,peakx+rng.randint(int(w*.04),int(w*.14))),base)])
            x=peakx+rng.randint(int(w*.04),int(w*.12))
        points.extend([(w,h),(0,h)])
        shades=[(34,58,83,140),(24,43,67,180),(12,27,43,210),(5,13,24,245)]
        d.polygon(points,fill=shades[layer])
    # mist bands
    for _ in range(8):
        yy=int(h*rng.uniform(.45,.83)); d.rectangle((0,yy,w,yy+rng.randint(8,28)),fill=(180,210,230,12))
    # atmospheric vignette
    vign=Image.new("RGBA",size,(0,0,0,0)); vd=ImageDraw.Draw(vign)
    vd.rectangle((0,0,w,h),fill=(0,0,0,25)); im=Image.alpha_composite(im,vign)
    # Text panel and typography
    d=ImageDraw.Draw(im,"RGBA"); title=str(scene.get("title",f"Cena {index}")); body=str(scene.get("text",""))
    tf=font(max(24,int(w*.062))); bf=font(max(18,int(w*.038)),False)
    margin=int(w*.085); y=int(h*.20)
    d.rounded_rectangle((margin,int(h*.13),w-margin,int(h*.52)),radius=26,fill=(2,7,16,75),outline=(255,255,255,24),width=1)
    for line in wrap(d,title,tf,w-2*margin-36):
        d.text((margin+18,y),line,font=tf,fill=(255,255,255,255),stroke_width=1,stroke_fill=(0,0,0,80)); y+=int(tf.size*1.25)
    y+=20
    for line in wrap(d,body,bf,w-2*margin-36)[:5]:
        d.text((margin+18,y),line,font=bf,fill=(232,241,248,245)); y+=int(bf.size*1.45)
    # Bottom label
    d.text((margin,h-int(h*.06)),f"CAPÍTULO {index:02d}",font=font(int(w*.025)),fill=(220,230,240,170))
    return im.convert("RGB")

def run(cmd): subprocess.run(cmd,check=True)

def main():
    p=argparse.ArgumentParser(description="Generate procedural cinematic scenes and render a vertical video")
    p.add_argument("--input",default="scenes.json"); p.add_argument("--output",default="output/video.mp4")
    args=p.parse_args()
    if not shutil.which("ffmpeg"): raise SystemExit("FFmpeg não encontrado.")
    data=json.loads(Path(args.input).read_text(encoding="utf-8")); w=int(data.get("resolution",{}).get("width",720)); h=int(data.get("resolution",{}).get("height",1280)); fps=int(data.get("fps",24)); scenes=data.get("scenes",[])
    if not scenes: raise SystemExit("O JSON precisa ter pelo menos uma cena.")
    idea=data.get("idea","")
    out=Path(args.output); out.parent.mkdir(parents=True,exist_ok=True)
    with tempfile.TemporaryDirectory() as td:
        td=Path(td); clips=[]
        for i,s in enumerate(scenes,1):
            duration=max(1,float(s.get("duration",10))); image=td/f"scene_{i:03d}.png"; clip=td/f"clip_{i:03d}.mp4"
            make_art(s,(w,h),i,idea).save(image); frames=max(1,int(duration*fps))
            # Slow camera drift/zoom on the engine-created artwork.
            vf=f"zoompan=z='min(zoom+0.0006,1.06)':x='iw/2-(iw/zoom/2)+sin(on/45)*12':y='ih/2-(ih/zoom/2)':d={frames}:s={w}x{h}:fps={fps},format=yuv420p"
            run(["ffmpeg","-hide_banner","-loglevel","error","-y","-loop","1","-i",str(image),"-vf",vf,"-t",str(duration),"-r",str(fps),"-pix_fmt","yuv420p","-an",str(clip)])
            clips.append(clip)
        concat=td/"concat.txt"; concat.write_text("".join("file '"+c.as_posix()+"'\n" for c in clips),encoding="utf-8")
        run(["ffmpeg","-hide_banner","-loglevel","error","-y","-f","concat","-safe","0","-i",str(concat),"-c","copy",str(out)])
    print("Vídeo gerado pelo motor procedural:",out)
if __name__=="__main__": main()
