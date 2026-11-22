"""Automatic script-to-scenes planner; uses heuristics, not an AI model."""
from __future__ import annotations
import argparse, json, re
from pathlib import Path

def split_script(script):
    paragraphs=[p.strip() for p in re.split(r"\n\s*\n+",script.strip()) if p.strip()]
    beats=[]
    for paragraph in paragraphs:
        sentences=[s.strip() for s in re.split(r"(?<=[.!?])\s+",paragraph) if s.strip()]
        chunk=[]; words=0
        for sentence in sentences:
            n=len(sentence.split())
            if chunk and words+n>38:
                beats.append(" ".join(chunk)); chunk=[]; words=0
            chunk.append(sentence); words+=n
        if chunk: beats.append(" ".join(chunk))
    return beats

def estimate_duration(text):
    return round(max(3.0,min(18.0,len(text.split())/2.4+1.5)),1)

def build_story(script,genre="cinematográfico"):
    script=script.strip()
    if not script: raise ValueError("Cole o roteiro completo antes de gerar.")
    beats=split_script(script) or [script]
    scenes=[]
    for i,beat in enumerate(beats,1):
        title=" ".join(beat.split()[:7]).strip(" ,.;:!?") or f"Cena {i}"
        scenes.append({"duration":estimate_duration(beat),"title":title,"text":beat,"narration":beat,
          "visual_prompt":"High-quality stylized 3D animated film, expressive consistent characters, detailed cinematic environment, realistic materials, cinematic lighting, depth of field, vertical 9:16. Depict this exact story moment: "+beat,
          "background":["#17243b","#536b83"]})
    return {"title":script[:100],"genre":genre,"format":"9:16","fps":24,"resolution":{"width":720,"height":1280},"scene_planning":"automatic_from_script","scenes":scenes}

def main():
    p=argparse.ArgumentParser(description="Divide a complete script into scenes automatically")
    p.add_argument("--script"); p.add_argument("--script-file"); p.add_argument("--idea",help="Legacy alias")
    p.add_argument("--genre",default="cinematográfico"); p.add_argument("--output",default="scenes.json"); a=p.parse_args()
    script=Path(a.script_file).read_text(encoding="utf-8") if a.script_file else (a.script or a.idea or "")
    data=build_story(script,a.genre)
    Path(a.output).write_text(json.dumps(data,ensure_ascii=False,indent=2),encoding="utf-8")
    print(f"Planejamento: {len(data['scenes'])} cenas, aproximadamente {sum(s['duration'] for s in data['scenes']):.1f}s")
if __name__=="__main__": main()
