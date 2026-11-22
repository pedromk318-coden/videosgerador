# VideosGerador 🎬

Gerador experimental de vídeos verticais (9:16) a partir de um roteiro completo.

## Fluxo atual
1. Abra Actions.
2. Escolha **Render video from complete script** e clique em **Run workflow**.
3. Cole o roteiro completo e escolha o clima visual.
4. O planejador divide o texto em cenas e estima uma duração individual por trecho.
5. Baixe **video-completo**, com MP4 e legendas SRT.

Não há quantidade fixa de cenas nem duração fixa por cena.

## Imagens de cena
O renderizador agora aceita uma imagem pronta por cena. Salve as imagens geradas em estilo 3D cinematográfico em `assets/scenes/`, com estes nomes:
- `scene_001.png`
- `scene_002.png`
- `scene_003.png`
- e assim por diante.

O campo `image_path` de cada cena já aponta para esse padrão. Quando a imagem existe, o motor usa a imagem como base e aplica movimento de câmera cinematográfico (zoom e deslocamento suave). Se não existir, usa a arte procedural antiga como alternativa.

As imagens precisam ser adicionadas ao repositório antes de iniciar o workflow. O arquivo `assets/scenes/README.md` explica a organização. O GitHub Actions não gera essas imagens sozinho nem se conecta diretamente ao Google Flow.

## Estado real do motor
- Planejamento automático de cenas e estimativa de duração a partir do roteiro.
- Prompt visual 3D cinematográfico por cena.
- Importação de imagens externas por cena e animação 2.5D por movimento de câmera.
- Fallback procedural quando a imagem ainda não foi fornecida.
- Áudio ambiente sintético e legendas SRT.
- Ainda não há geração automática de imagens por IA, rig de personagens 3D, animação corporal ou voz narrada. O movimento aplicado a imagens é uma animação de câmera, não animação 3D real.

## Stack
Python, Pillow, FFmpeg e GitHub Actions.
