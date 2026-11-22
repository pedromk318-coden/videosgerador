# VideosGerador 🎬

Gerador experimental de vídeos verticais (9:16) a partir de uma ideia. O motor cria arte procedural, anima camadas com movimentos de câmera diferentes e renderiza MP4 via FFmpeg no GitHub Actions.

## Como executar
1. Abra a aba **Actions**.
2. Escolha **Render video with procedural engine** e clique em **Run workflow**.
3. Informe a ideia, número de cenas, duração e gênero.
4. Quando concluir, baixe o artefato **video-mp4**.

## Motor visual próprio
- Imagens geradas por código: gradientes, luzes, estrelas, montanhas e silhuetas de cidade/árvores.
- Camadas independentes (fundo, plano intermediário, primeiro plano e texto).
- Zoom com taxas diferentes entre camadas para simular profundidade/parallax.
- Paletas que variam por gênero (fantasia, aventura, mistério, terror, sci-fi, drama).
- Formato vertical e 24 FPS padrão.
- Arte determinística: a mesma ideia/cena produz a mesma composição base.

## Recursos de produção incorporados ao planejamento
Inspirado em práticas e ferramentas de produção cinematográfica do pacote enviado pelo usuário e na biblioteca Lemo-Opuscar (MIT), o projeto organiza a renderização por cenas, composição em camadas, formato vertical, timeline, áudio e legendas como módulos separados. Este repositório implementa seu próprio código; não redistribui arquivos do Estúdio 66 sob licença pessoal restritiva.

## Limitações atuais
- Os cenários são procedurais e abstratos; não são imagens de IA que interpretem a narrativa.
- O roteiro é determinístico/templateado, não gerado por modelo de linguagem.
- Parallax atual é uma simulação por camadas com movimentos de câmera, não rig 3D/depth map.
- Narração, trilha, efeitos sonoros e legendas sincronizadas ainda não estão integrados.
- O workflow precisa ser executado para validar o resultado final do render atualizado.

## Stack
Python, Pillow, FFmpeg e GitHub Actions.
