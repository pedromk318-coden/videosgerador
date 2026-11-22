"""Narrative engine: turns a short idea into a structured multi-scene story.
This is deterministic scaffolding, not an AI model. Replace/adapt with an LLM API later.
"""
from __future__ import annotations
import argparse, json
from pathlib import Path

def build_story(idea: str, count: int = 6, duration: int = 10, genre: str = "mistério"):
    if not idea.strip(): raise ValueError("Informe uma ideia.")
    if not 1 <= count <= 12: raise ValueError("count deve ficar entre 1 e 12.")
    if not 1 <= duration <= 60: raise ValueError("duration deve ficar entre 1 e 60.")
    structure = [
        ("Abertura", "Apresente o protagonista e o ambiente, estabelecendo o clima."),
        ("Sinal estranho", "Um detalhe inesperado quebra a normalidade e desperta curiosidade."),
        ("Investigação", "O protagonista segue uma pista e descobre algo incomum."),
        ("Complicação", "Um obstáculo muda os planos e aumenta a tensão."),
        ("Revelação", "Uma descoberta conecta os acontecimentos anteriores."),
        ("Clímax", "O protagonista precisa tomar uma decisão importante."),
        ("Consequência", "Mostre o impacto da decisão e uma nova informação."),
        ("Encerramento", "Finalize com uma imagem memorável e um gancho opcional."),
        ("Gancho", "Sugira que ainda existe algo desconhecido."),
        ("Epílogo", "Feche o episódio sem perder o clima da narrativa."),
        ("Nova pista", "Apresente uma pista para uma possível continuação."),
        ("Final", "Conclua a história de forma clara."),
    ]
    scenes=[]
    for i in range(count):
        label, beat=structure[i]
        scenes.append({
            "duration": duration,
            "title": f"{label} — Cena {i+1}",
            "text": f"{idea.strip()} {beat}",
            "visual_prompt": f"Vertical cinematic 2.5D parallax scene, {genre}, visualizing: {idea.strip()}. Beat: {beat}. Layered foreground, midground and background, atmospheric lighting, no text in image.",
            "narration": f"{idea.strip()} — {beat}",
            "background": ["#0b1e35","#34526e"] if i%2==0 else ["#17132d","#533a6e"]
        })
    return {"title":idea.strip(),"genre":genre,"format":"9:16","fps":24,"resolution":{"width":720,"height":1280},"scenes":scenes}

def main():
    p=argparse.ArgumentParser()
    p.add_argument("--idea",required=True)
    p.add_argument("--count",type=int,default=6)
    p.add_argument("--duration",type=int,default=10)
    p.add_argument("--genre",default="mistério")
    p.add_argument("--output",default="scenes.json")
    a=p.parse_args()
    data=build_story(a.idea,a.count,a.duration,a.genre)
    Path(a.output).write_text(json.dumps(data,ensure_ascii=False,indent=2),encoding="utf-8")
    print(f"Roteiro-base: {a.count} cenas x {a.duration}s -> {a.output}")
if __name__=="__main__": main()
