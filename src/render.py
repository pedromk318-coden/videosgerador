#!/usr/bin/env python3
"""Render a simple vertical video from JSON scene cards using Pillow and FFmpeg."""
from __future__ import annotations
import argparse, json, shutil, subprocess, tempfile
from pathlib import Path
from PIL import Image, ImageDraw, ImageFont

def find_font():
    candidates=["/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf","/usr/share/fonts/truetype/liberation2/LiberationSans-Bold.ttf"]
    for path in candidates:
        if Path(path).exists(): return path
    return None

def gradient(size, top, bottom):
    w,h=size; image=Image.new("RGB",size); pixels=image.load()
    def rgb(v):
        v=v.lstrip("#"); return tuple(int(v[i:i+2],16) for i in (0,2,4))
    a,b=rgb(top),rgb(bottom)
    for y in range(h):
        t=y/max(1,h-1); c=tuple(round(a[i]*(1-t)+b[i]*t) for i in range(3))
        for x in range(w): pixels[x,y]=c
    return image

def wrap_text(draw,text,font,max_width):
    lines=[]; current=""
    for word in text.split():
        test=(current+" "+word).strip()
        if draw.textbbox((0,0),test,font=font)[2]<=max_width: current=test
        else:
            if current: lines.append(current)
            current=word
    if current: lines.append(current)
    return lines

def create_card(scene,width,height,path,index):
    colors=scene.get("background",["#0b1e35","#34526e"])
    image=gradient((width,height),colors[0],colors[1]); draw=ImageDraw.Draw(image,"RGBA")
    draw.ellipse((width*.62,-height*.05,width*1.15,height*.48),fill=(255,220,160,28))
    draw.polygon([(0,height*.72),(width*.22,height*.49),(width*.43,height*.73),(width*.66,height*.54),(width,height*.76),(width,height),(0,height)],fill=(7,15,28,110))
    draw.polygon([(0,height*.83),(width*.18,height*.68),(width*.48,height*.84),(width*.72,height*.66),(width,height*.86),(width,height),(0,height)],fill=(3,9,20,170))
    fp=find_font(); tf=ImageFont.truetype(fp,42) if fp else ImageFont.load_default(); bf=ImageFont.truetype(fp,30) if fp else ImageFont.load_default()
    margin=int(width*.09); y=int(height*.29)
    for line in wrap_text(draw,scene.get("title",f"Cena {index}"),tf,width-2*margin):
        draw.text((margin,y),line,font=tf,fill=(255,255,255,255),stroke_width=2,stroke_fill=(0,0,0,90)); y+=56
    y+=28
    for line in wrap_text(draw,scene.get("text",""),bf,width-2*margin):
        draw.text((margin,y),line,font=bf,fill=(240,245,250,255),stroke_width=1,stroke_fill=(0,0,0,90)); y+=44
    image.save(path)

def run(cmd): subprocess.run(cmd,check=True)

def main():
    p=argparse.ArgumentParser(description="Render vertical scene cards into MP4")
    p.add_argument("--input",default="scenes.json"); p.add_argument("--output",default="output/video.mp4"); args=p.parse_args()
    if not shutil.which("ffmpeg"): raise SystemExit("FFmpeg não encontrado. Instale-o e adicione ao PATH.")
    data=json.loads(Path(args.input).read_text(encoding="utf-8")); w=int(data.get("resolution",{}).get("width",720)); h=int(data.get("resolution",{}).get("height",1280)); fps=int(data.get("fps",24)); scenes=data.get("scenes",[])
    if not scenes: raise SystemExit("O JSON precisa ter pelo menos uma cena.")
    out=Path(args.output); out.parent.mkdir(parents=True,exist_ok=True)
    with tempfile.TemporaryDirectory() as td:
        td=Path(td); clips=[]
        for i,s in enumerate(scenes,1):
            duration=float(s.get("duration",10)); card=td/f"scene_{i:03d}.png"; clip=td/f"clip_{i:03d}.mp4"; create_card(s,w,h,card,i); frames=max(1,int(duration*fps))
            vf=f"zoompan=z='min(zoom+0.0008,1.08)':d={frames}:s={w}x{h}:fps={fps}"
            run(["ffmpeg","-y","-loop","1","-i",str(card),"-vf",vf,"-t",str(duration),"-r",str(fps),"-pix_fmt","yuv420p","-an",str(clip)]); clips.append(clip)
        concat=td/"concat.txt"; concat.write_text("".join("file '"+c.as_posix()+"'\n" for c in clips),encoding="utf-8")
        run(["ffmpeg","-y","-f","concat","-safe","0","-i",str(concat),"-c","copy",str(out)])
    print("Vídeo gerado:",out)

if __name__=="__main__": main()
