# VideosGerador 🎬

Renderizador de projetos de vídeo em JSON. O planejamento criativo pode ser feito no Claude ou manualmente; a renderização é procedural e **não usa IA nem APIs pagas**.

## Fluxo novo: enviar arquivo e renderizar
1. Peça ao Claude para criar um arquivo JSON seguindo `projects/modelo-projeto.json`.
2. Salve o arquivo com extensão `.json`.
3. No GitHub, abra a pasta `projects/` e envie o JSON usando **Add file → Upload files**.
4. Faça commit. O envio de um único JSON nessa pasta inicia a renderização automaticamente.
5. Abra **Actions**, entre na execução e baixe o artefato `video-completo`.

Também é possível abrir **Actions → Render uploaded video project → Run workflow** e informar o caminho do JSON que já está no repositório, por exemplo `projects/meu-video.json`.

## Formato do projeto
Veja o exemplo completo em [projects/modelo-projeto.json](projects/modelo-projeto.json). Campos principais:
- `title`: título do vídeo.
- `style`: estilo visual, como `fantasia`, `aventura`, `mistério`, `drama` ou `cinematográfico`.
- `format`: formato, normalmente `9:16`.
- `scenes`: lista de cenas na ordem de exibição.
- Cada cena deve informar `duration` em segundos e `narration` (ou `script` / `text`).
- Campos opcionais: `visual_description`, `environment`, `action` e `camera`.

O validador aceita até 150 cenas, com duração entre 1 e 60 segundos cada. Ele verifica o JSON antes de renderizar e mostra erros de forma clara.

## Prompt para pedir o arquivo ao Claude
"Crie um arquivo JSON de projeto de vídeo seguindo exatamente o formato de projects/modelo-projeto.json. Defina título, estilo visual, formato 9:16 e todas as cenas na ordem correta. Para cada cena informe duração em segundos, descrição visual, ambiente, ação, movimento de câmera e narração. Não escreva explicações fora do JSON. Não use Markdown nem blocos de código. Garanta que o JSON seja válido."

## Motor offline sem IA
`src/animation_engine.py` desenha os quadros usando Python/Pillow e monta o MP4 com FFmpeg. Ele usa cenários e personagens procedurais, animações básicas e movimento em camadas para simular profundidade 2.5D. O projeto JSON fornece a direção criativa; o renderizador transforma os dados em animação usando regras fixas, sem chamar Claude, ChatGPT, Flow, Gemini ou qualquer serviço externo.

O resultado é uma animação procedural estilizada, não um filme 3D realista. A descrição de cena orienta o contexto e as palavras-chave disponíveis no motor; nem todos os movimentos ou objetos descritos já têm representação visual própria.

## Tecnologias
Python, Pillow, FFmpeg e GitHub Actions. O Actions tem limites próprios de uso gratuito.

## Arquivos principais
- `projects/modelo-projeto.json`: exemplo de entrada.
- `src/project_validator.py`: valida e normaliza projetos.
- `src/animation_engine.py`: renderizador quadro a quadro.
- `src/subtitles.py`: legendas SRT.
- `src/audio_engine.py`: trilha ambiente sintética.
- `.github/workflows/render.yml`: automação do GitHub.
