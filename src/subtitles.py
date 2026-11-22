#!/usr/bin/env python3
"""Create simple SRT captions from scene text and duration."""
import argparse, json
from pathlib import Path
def ts(seconds):
 ms=int(round(seconds*1000)); h=ms//3600000; ms%=3600000; m=ms//60000; ms%=60000; s=ms//1000; ms%=1000
 return f"{h:02}:{m:02}:{s:02},{ms:03}"
def main():
 p=argparse.ArgumentParser(); p.add_argument("--input",default="scenes.json"); p.add_argument("--output",default="output/subtitles.srt"); a=p.parse_args()
 data=json.loads(Path(a.input).read_text(encoding="utf-8")); t=0; blocks=[]
 for n,scene in enumerate(data.get("scenes",[]),1):
  dur=float(scene.get("duration",10)); caption=scene.get("narration") or scene.get("text") or scene.get("title","")
  blocks.append(f"{n}\n{ts(t)} --> {ts(t+dur)}\n{caption}\n"); t+=dur
 out=Path(a.output); out.parent.mkdir(parents=True,exist_ok=True); out.write_text("\n".join(blocks),encoding="utf-8"); print("SRT:",out)
if __name__=="__main__": main()
