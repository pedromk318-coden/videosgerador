# VideosGerador 🎬

Gerador **offline e sem IA** de vídeos verticais a partir de um roteiro completo.

## Como funciona
1. Abra **Actions**.
2. Escolha **Render video from complete script** e clique em **Run workflow**.
3. Cole o roteiro completo e escolha o estilo visual.
4. O planejador divide o texto em cenas e calcula a duração de cada trecho.
5. O motor desenha e anima cada cena localmente com Python/Pillow e monta o MP4 com FFmpeg.
6. Baixe o artefato **video-completo**, que contém o vídeo e as legendas SRT.

Não existe quantidade fixa de cenas nem duração fixa por cena. A divisão e a duração são calculadas a partir do roteiro.

## Motor de animação sem IA
O arquivo `src/animation_engine.py` cria os quadros do vídeo do zero, sem chamar Claude, ChatGPT, Flow, Gemini ou qualquer API externa. Ele inclui:
- Cenários procedurais com variações de floresta, castelo, cidade, espaço, litoral e paisagem.
- Personagem desenhado pelo próprio código, com rosto, roupa, braços e pernas.
- Animações básicas de caminhada, corrida e movimento em repouso.
- Movimento de elementos do cenário em velocidades diferentes para simular profundidade 2.5D.
- Luz, atmosfera, paleta de cores por gênero e movimento contínuo entre quadros.

O resultado é uma animação procedural estilizada. Não é um filme 3D realista nem gera modelos complexos a partir do significado de qualquer frase: o motor usa regras e palavras-chave para escolher cenários e ações. Personagens e recursos visuais podem ser ampliados gradualmente.

## Tecnologias
- Python e Pillow: desenho dos quadros.
- FFmpeg: codificação e montagem do vídeo.
- GitHub Actions: execução automática do processo.

Não precisa de chave de API, conta em serviço de IA ou assinatura. O GitHub Actions tem limites próprios de uso gratuito conforme o tipo de conta e repositório.

## Estrutura
- `src/story_engine.py`: divisão do roteiro e duração das cenas.
- `src/idea_to_scenes.py`: interface de geração do plano de cenas.
- `src/animation_engine.py`: motor visual e animação quadro a quadro.
- `src/subtitles.py`: legendas SRT.
- `src/audio_engine.py`: trilha ambiente sintética.
- `.github/workflows/render.yml`: automação do GitHub.
