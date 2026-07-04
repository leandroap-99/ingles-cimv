# Jack Hannaford — App de Inglês (GitHub Pages)

App de flashcards com frases, vocabulário, áudio e texto do curso CIMV,
pronto para publicar **grátis** no GitHub Pages, com HTTPS automático
(essencial para o áudio funcionar no iPhone pela internet).
-----
## Estrutura

```
jack-hannaford/
├── index.html          ← o app
├── .nojekyll           ← arquivo técnico (não apague)
├── data/
│   ├── manifest.json   ← lista de todas as partes
│   ├── part02.json     ← frases, traduções e vocabulário
│   └── part03.json
├── audio/
│   ├── part02/         ← 009.mp3 … 022.mp3 + full.mp3
│   └── part03/         ← 23.mp3 … 32.mp3 + full.mp3
└── adicionar_parte.py  ← script para adicionar novas partes
```

---

## Como publicar no GitHub Pages (passo a passo)

### 1. Crie uma conta no GitHub (se ainda não tiver)
Vá em https://github.com e crie uma conta gratuita.

### 2. Crie um repositório novo
- Clique no **+** no topo direito → **New repository**
- Nome do repositório: por exemplo `ingles-cimv`
- Marque como **Public** (o GitHub Pages grátis exige repositório público)
- **Não** marque "Add a README"
- Clique em **Create repository**

### 3. Envie os arquivos

**Opção A — pelo site (mais fácil, sem instalar nada):**
1. Na página do repositório recém-criado, clique em **uploading an existing file**
2. Arraste **todo o conteúdo** desta pasta (o `index.html`, as pastas
   `data/` e `audio/`, o `.nojekyll`, etc.) para a área de upload
   - Dica: selecione tudo de uma vez. Se o site não aceitar pastas,
     use a Opção B abaixo.
3. Escreva uma mensagem qualquer em "Commit changes" e clique no botão verde

**Opção B — pela linha de comando (git):**
```bash
cd jack-hannaford
git init
git add .
git commit -m "App Jack Hannaford"
git branch -M main
git remote add origin https://github.com/SEU_USUARIO/ingles-cimv.git
git push -u origin main
```

### 4. Ative o GitHub Pages
- No repositório, vá em **Settings** (Configurações)
- No menu lateral, clique em **Pages**
- Em **Source**, selecione a branch **main** e a pasta **/ (root)**
- Clique em **Save**
- Aguarde 1-2 minutos

### 5. Acesse seu app
O endereço será:
```
https://SEU_USUARIO.github.io/ingles-cimv/
```
(troque `SEU_USUARIO` pelo seu nome de usuário do GitHub e `ingles-cimv`
pelo nome que você deu ao repositório).

Abra esse link no PC ou no iPhone — o áudio vai funcionar em ambos. ✅

> Dica: adicione o link à tela inicial do iPhone (botão compartilhar →
> "Adicionar à Tela de Início") para abrir como se fosse um aplicativo.

---

## Como adicionar uma nova parte (ex: Part 04)

1. Junte os MP3s das frases (numerados, ex: `33_...mp3`) e o MP3 do
   áudio completo.

2. Rode o script (precisa de Python 3 e ffmpeg no seu computador):
   ```bash
   python3 adicionar_parte.py --parte 04 \
       --audios /caminho/dos/mp3/ \
       --full /caminho/audio_completo.mp3
   ```
   Ele comprime os áudios, coloca em `audio/part04/`, registra no
   `manifest.json` e cria um `data/part04.json` em branco.

3. Edite o `data/part04.json` com as frases, traduções e vocabulário.

4. Envie os arquivos novos/modificados para o GitHub (repita o passo 3
   da publicação, ou `git add . && git commit -m "Part 04" && git push`).

5. Em 1-2 minutos a Part 04 aparece sozinha no app. Nenhuma mudança no
   `index.html` é necessária.

---

## Observações

- **Repositório privado:** o GitHub Pages grátis funciona melhor com
  repositório público. Se quiser privado, precisa de conta paga (GitHub Pro).
- **Limites do GitHub Pages:** até 1 GB de repositório e 100 GB de banda
  por mês — muito acima do que este app usa. Áudios comprimidos são leves.
- **Domínio próprio:** se um dia quiser um endereço como `ingles.seusite.com`,
  o GitHub Pages permite configurar domínio personalizado grátis
  (em Settings → Pages → Custom domain).
