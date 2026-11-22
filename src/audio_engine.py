#!/usr/bin/env python3
"""Generate a synthetic ambient bed and mux it into a video (no audio assets)."""
import argparse, json, subprocess, shutil
from pathlib import Path
def run(cmd): subprocess.run(cmd,check=True)
def main():
 p=argparse.ArgumentParser(); p.add_argument("--input",default="scenes.json"); p.add_argument("--video",default="output/video.mp4"); p.add_argument("--output",default="output/video_with_audio.mp4"); a=p.parse_args()
 if not shutil.which("ffmpeg"): raise SystemExit("FFmpeg não encontrado.")
 data=json.loads(Path(a.input).read_text(encoding="utf-8")); total=sum(float(s.get("duration",10)) for s in data.get("scenes",[]))
 out=Path(a.output); out.parent.mkdir(parents=True,exist_ok=True); temp=out.with_name("ambient.wav")
 # A low-volume synthesized ambience: gentle sine layers with fade-in/out.
 expr="0.10*sin(2*PI*110*t)+0.06*sin(2*PI*164.81*t)+0.035*sin(2*PI*220*t)"
 run(["ffmpeg","-hide_banner","-loglevel","error","-y","-f","lavfi","-i",f"aevalsrc={expr}:s=44100:d={total}","-af",f"afade=t=in:d=2,afade=t=out:st={max(0,total-3)}:d=3,volume=0.22","-c:a","pcm_s16le",str(temp)])
 run(["ffmpeg","-hide_banner","-loglevel","error","-y","-i",a.video,"-i",str(temp),"-map","0:v:0","-map","1:a:0","-c:v","copy","-c:a","aac","-shortest",str(out)])
 temp.unlink(missing_ok=True); Path(a.video).unlink(missing_ok=True); out.replace(a.video); print("Áudio ambiente muxado:",a.video)
if __name__=="__main__": main()
