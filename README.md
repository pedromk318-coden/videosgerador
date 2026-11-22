# videosgerador

Gerador inicial de vídeos verticais (9:16) a partir de cenas em JSON. A primeira versão cria cartões animados com movimento de zoom/pan usando FFmpeg; é uma base para evoluir para imagens, Parallax 2.5D, narração e legendas.

## Requisitos
- Python 3.10+
- FFmpeg instalado e disponível no PATH
- Pillow

## Uso local

```bash
pip install -r requirements.txt
python src/render.py --input scenes.json --output output/video.mp4
```

Cada cena tem duração padrão de 10 segundos. A resolução padrão é 720x1280 (vertical).

## GitHub Actions
Abra **Actions → Render video → Run workflow**. O vídeo final será anexado à execução como artifact `video-mp4`.


## Próximas etapas
1. Gerar imagens de cada cena
2. Criar camadas de profundidade para Parallax 2.5D
3. Adicionar narração, trilha/efeitos e legendas sincronizadas
4. Interface web para escolher tema e iniciar renderização
