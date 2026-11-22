#!/usr/bin/env python3
"""Create a basic scene-card storyboard from a submitted idea."""
import argparse, json
from pathlib import Path

BEATS = [
    "A história começa: apresente o cenário e o personagem.",
    "Um detalhe estranho chama a atenção e cria curiosidade.",
    "O personagem se aproxima e descobre uma pista inesperada.",
    "A situação muda e surge um novo mistério.",
    "A descoberta revela uma parte surpreendente da história.",
    "O momento decisivo conecta as pistas anteriores.",
    "Uma última surpresa muda a interpretação dos acontecimentos.",
    "A história termina com uma imagem marcante e espaço para reflexão.",
    "Um novo elemento aparece, sugerindo que há mais por descobrir.",
    "Finalize com um gancho intrigante.",
]
PALETTES = [["#0b1e35", "#34526e"], ["#17132d", "#533a6e"], ["#102b26", "#38705b"]]

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--idea", required=True)
    parser.add_argument("--count", type=int, default=6)
    parser.add_argument("--duration", type=int, default=10)
    parser.add_argument("--output", default="scenes.json")
    args = parser.parse_args()
    idea = args.idea.strip()
    if not idea: raise SystemExit("A ideia não pode estar vazia.")
    if not 1 <= args.count <= 10: raise SystemExit("Quantidade de cenas deve ser entre 1 e 10.")
    if not 1 <= args.duration <= 60: raise SystemExit("Duração por cena deve ser de 1 a 60 segundos.")
    data = {"title": idea, "format": "9:16", "fps": 24, "resolution": {"width": 720, "height": 1280},
             "scenes": [{"duration": args.duration, "title": f"Cena {i+1}",
                         "text": f"{idea} {BEATS[i % len(BEATS)]}", "background": PALETTES[i % len(PALETTES)]}
                        for i in range(args.count)]}
    Path(args.output).write_text(json.dumps(data, ensure_ascii=False, indent=2), encoding="utf-8")
    print(f"Roteiro-base salvo em {args.output}: {args.count} cenas de {args.duration}s.")

if __name__ == "__main__": main()
