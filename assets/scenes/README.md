# Imagens das cenas

Coloque aqui uma imagem vertical ou cinematográfica para cada cena do roteiro.

Use exatamente esta convenção:
- scene_001.png
- scene_002.png
- scene_003.png

A cena 1 usa scene_001.png, a cena 2 usa scene_002.png e assim por diante.

Dicas para manter o visual:
- Gere todas as imagens com o mesmo estilo de animação 3D.
- Reutilize a mesma descrição dos personagens em todos os prompts para ajudar na consistência.
- Não inclua títulos ou legendas dentro da imagem; o vídeo e o arquivo SRT são montados separadamente.
- Prefira imagens com composição vertical 9:16.

Depois de adicionar as imagens e fazer commit no repositório, execute o workflow em Actions. Quando uma imagem estiver presente, o renderizador aplica zoom e deslocamento de câmera. Quando faltar, ele usa o cenário procedural como reserva.

Observação: o GitHub Actions não gera imagens por IA nem importa automaticamente imagens do Google Flow. Esta pasta recebe arquivos de imagem que já foram criados e adicionados ao repositório.
