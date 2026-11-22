# VideosGerador 🎬

Gerador experimental de vídeos verticais (9:16) a partir de uma ideia, com cenas visuais procedurais criadas pelo próprio motor e montagem MP4 via FFmpeg.

## Como executar no GitHub
1. Abra a aba **Actions**.
2. Selecione **Render video** e clique **Run workflow**.
3. Informe a ideia, quantidade de cenas, duração e gênero.
4. Aguarde o workflow terminar e baixe o artefato **video-mp4**.

## O motor visual próprio
O renderizador em `src/render.py` cria imagens originais por desenho procedural com Pillow (gradientes, luzes, estrelas, montanhas em camadas, névoa e composição de texto), e anima a câmera com zoom lento e deriva lateral usando FFmpeg. Não depende de Google Flow nem de imagens externas.

## Limitações atuais (transparentes)
- A arte é procedural/abstrata e não interpreta semanticamente cada ideia como um gerador de imagens por IA.
- O roteiro é uma estrutura-base determinística, não texto criado por um modelo de linguagem.
- Ainda não há narração de áudio, trilha, efeitos sonoros, legendas sincronizadas, segmentação real em camadas 3D ou Parallax 2.5D com depth map.
- A próxima evolução é enriquecer o motor procedural e adicionar camadas/movimento, depois integrar serviços de IA opcionalmente.

## Tecnologias
Python, Pillow e FFmpeg. Renderização em GitHub Actions (runner Ubuntu).
