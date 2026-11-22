#!/usr/bin/env python3
import argparse,json
from pathlib import Path
from story_engine import build_story
def main():
 p=argparse.ArgumentParser(description="Divide a complete script into scenes")
 p.add_argument("--script");p.add_argument("--script-file");p.add_argument("--idea",help="Legacy alias")
 p.add_argument("--genre",default="cinematográfico");p.add_argument("--output",default="scenes.json");a=p.parse_args()
 script=Path(a.script_file).read_text(encoding="utf-8") if a.script_file else (a.script or a.idea or "")
 data=build_story(script,a.genre)
 Path(a.output).write_text(json.dumps(data,ensure_ascii=False,indent=2),encoding="utf-8")
 print(f"{len(data['scenes'])} cenas planejadas automaticamente.")
if __name__=="__main__":main()
