#!/usr/bin/env python3
"""CLI wrapper around the narrative scaffolding engine."""
import argparse, json
from pathlib import Path
from story_engine import build_story

def main():
    p=argparse.ArgumentParser(description="Prepare scenes from a video idea")
    p.add_argument("--idea",required=True)
    p.add_argument("--count",type=int,default=6)
    p.add_argument("--duration",type=int,default=10)
    p.add_argument("--genre",default="mistério")
    p.add_argument("--output",default="scenes.json")
    a=p.parse_args()
    data=build_story(a.idea,a.count,a.duration,a.genre)
    Path(a.output).write_text(json.dumps(data,ensure_ascii=False,indent=2),encoding="utf-8")
    print(f"Roteiro-base salvo em {a.output} ({a.count} cenas, {a.duration}s cada).")
if __name__ == "__main__": main()
