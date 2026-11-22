#!/usr/bin/env python3
"""Validate and normalize a Claude-authored video project. No AI/API calls."""
import argparse, json
from pathlib import Path

def main():
    p=argparse.ArgumentParser()
    p.add_argument("--input",required=True)
    p.add_argument("--output",default="scenes.json")
    a=p.parse_args()
    source=Path(a.input)
    if not source.is_file():
        raise SystemExit(f"Arquivo de projeto não encontrado: {source}")
    try:
        data=json.loads(source.read_text(encoding="utf-8"))
    except json.JSONDecodeError as e:
        raise SystemExit(f"JSON inválido na linha {e.lineno}, coluna {e.colno}: {e.msg}")
    if not isinstance(data,dict):
        raise SystemExit("O projeto precisa ser um objeto JSON.")
    scenes=data.get("scenes")
    if not isinstance(scenes,list) or not scenes:
        raise SystemExit("O projeto precisa conter uma lista 'scenes' com pelo menos uma cena.")
    if len(scenes)>150:
        raise SystemExit("Limite do projeto: 150 cenas por renderização.")
    style=str(data.get("style") or data.get("genre") or "cinematográfico")
    title=str(data.get("title") or data.get("project_name") or "Vídeo")
    normalized=[]
    for i,scene in enumerate(scenes,1):
        if not isinstance(scene,dict):
            raise SystemExit(f"Cena {i}: cada cena precisa ser um objeto.")
        duration=scene.get("duration",scene.get("duration_seconds"))
        try: duration=float(duration)
        except (TypeError,ValueError):
            raise SystemExit(f"Cena {i}: informe 'duration' em segundos.")
        if not 1 <= duration <= 60:
            raise SystemExit(f"Cena {i}: duração deve ficar entre 1 e 60 segundos.")
        text=str(scene.get("narration") or scene.get("script") or scene.get("text") or "")
        if not text.strip():
            raise SystemExit(f"Cena {i}: informe 'narration', 'script' ou 'text'.")
        normalized.append({
            **scene,
            "duration":duration,
            "title":str(scene.get("title") or f"Cena {i}"),
            "text":str(scene.get("text") or text),
            "narration":text,
            "visual_prompt":str(scene.get("visual_prompt") or scene.get("visual_description") or ""),
        })
    result={
        "title":title,"genre":style,
        "format":data.get("format","9:16"),
        "fps":int(data.get("fps",20)),
        "resolution":data.get("resolution",{"width":480,"height":854}),
        "scenes":normalized
    }
    Path(a.output).write_text(json.dumps(result,ensure_ascii=False,indent=2),encoding="utf-8")
    print(f"Projeto validado: {len(normalized)} cenas | {sum(s['duration'] for s in normalized):.1f} segundos | estilo: {style}")
if __name__=="__main__": main()
