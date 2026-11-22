# VideosGerador 🎬

Gerador experimental de vídeos verticais (9:16) a partir de um roteiro completo.

## Novo fluxo
1. Abra Actions.
2. Escolha **Render video from complete script** e clique em **Run workflow**.
3. Cole o roteiro completo e escolha o clima visual.
4. O planejador divide o texto em cenas automaticamente e estima uma duração individual para cada trecho.
5. Baixe o artefato **video-completo**, com MP4 e legendas SRT.

Não há quantidade fixa de cenas nem duração fixa por cena. Parágrafos e frases orientam a divisão; a duração é estimada pelo tamanho de cada trecho.

## Interface
O arquivo index.html permite colar um roteiro e baixar um scenes.json com a divisão automática. Para renderizar no GitHub Actions, cole o roteiro na entrada do workflow.

## Estado real do motor
- O planejador cria cenas a partir do texto fornecido e calcula tempos individuais por estimativa de narração.
- Cada cena recebe um prompt visual descritivo no estilo de animação 3D cinematográfica.
- O renderizador atual ainda desenha cenários e personagens proceduralmente com Pillow e simula profundidade com camadas e movimentos de câmera.
- Os prompts ainda não são enviados a um gerador de imagens; o resultado ainda não corresponde visualmente a uma animação 3D de estúdio.
- O áudio atual é uma cama ambiente sintética; ainda não há voz narrada nem efeitos sonoros específicos.
- É necessário executar o workflow para validar a renderização após esta atualização.

## Stack
Python, Pillow, FFmpeg e GitHub Actions.
