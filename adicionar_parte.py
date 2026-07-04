#!/usr/bin/env python3
"""
Adiciona uma nova parte ao app Jack Hannaford.

USO:
  python3 adicionar_parte.py --parte 04 \
      --audios /caminho/para/audios_mp3/ \
      --full /caminho/para/audio_completo.mp3

O script:
  1. Comprime os MP3s (remove capa de álbum, converte para voz otimizada)
  2. Copia para audio/partXX/
  3. Cria um esqueleto data/partXX.json para você preencher texto/traduções/vocabulário
  4. Registra a parte no data/manifest.json

Depois de rodar, edite o data/partXX.json gerado com as frases,
traduções e vocabulário, e pronto.

Requisitos: ffmpeg instalado (sudo apt install ffmpeg)
"""
import argparse, json, os, subprocess, sys, shutil, re

BASE = os.path.dirname(os.path.abspath(__file__))

def compress(src, dst, bitrate="16k", rate="16000"):
    """Comprime MP3 removendo artwork/metadata, mono, otimizado para voz."""
    subprocess.run([
        "ffmpeg", "-y", "-loglevel", "error",
        "-i", src, "-vn", "-map_metadata", "-1",
        "-ac", "1", "-ar", rate, "-b:a", bitrate, dst
    ], check=True)

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--parte", required=True, help="Número da parte, ex: 04")
    ap.add_argument("--audios", required=True, help="Pasta com os MP3s das frases")
    ap.add_argument("--full", required=False, help="MP3 do áudio completo (opcional)")
    args = ap.parse_args()

    part_num = args.parte.zfill(2)
    part_id = "part" + part_num
    label = "Part " + part_num

    audio_dir = os.path.join(BASE, "audio", part_id)
    os.makedirs(audio_dir, exist_ok=True)

    # 1. Comprime e copia áudios das frases
    mp3s = sorted([f for f in os.listdir(args.audios) if f.lower().endswith(".mp3")])
    if not mp3s:
        print("ERRO: nenhum MP3 encontrado em", args.audios)
        sys.exit(1)

    sentence_ids = []
    for f in mp3s:
        # extrai o número do começo do nome do arquivo (ex: "33_jack_said.mp3" -> "33")
        m = re.match(r"(\d+)", f)
        if not m:
            print("Ignorando (sem número no início):", f)
            continue
        sid = str(int(m.group(1)))  # remove zeros à esquerda
        dst = os.path.join(audio_dir, sid + ".mp3")
        compress(os.path.join(args.audios, f), dst)
        sentence_ids.append(sid)
        print("  Áudio frase:", f, "->", sid + ".mp3")

    # 2. Áudio completo
    if args.full and os.path.exists(args.full):
        compress(args.full, os.path.join(audio_dir, "full.mp3"), bitrate="24k")
        print("  Áudio completo -> full.mp3")

    # 3. Cria esqueleto do JSON
    data_path = os.path.join(BASE, "data", part_id + ".json")
    if os.path.exists(data_path):
        print("AVISO:", data_path, "já existe — não sobrescrito.")
    else:
        skeleton = {
            "id": part_id,
            "label": label,
            "text": "COLE_AQUI_O_TEXTO_COMPLETO_EM_INGLES",
            "sentences": [
                {"id": sid, "en": "FRASE_EM_INGLES", "pt": "TRADUCAO_EM_PORTUGUES"}
                for sid in sentence_ids
            ],
            "vocab": [
                {"word": "palavra", "pt": "traducao", "example": "frase de exemplo", "type": "expressão"}
            ]
        }
        with open(data_path, "w", encoding="utf-8") as fp:
            json.dump(skeleton, fp, ensure_ascii=False, indent=2)
        print("Esqueleto criado:", data_path)
        print(">>> EDITE esse arquivo com as frases, traduções e vocabulário.")

    # 4. Registra no manifest
    manifest_path = os.path.join(BASE, "data", "manifest.json")
    with open(manifest_path, encoding="utf-8") as fp:
        manifest = json.load(fp)
    if not any(p["id"] == part_id for p in manifest["parts"]):
        manifest["parts"].append({"id": part_id, "label": label})
        manifest["parts"].sort(key=lambda p: p["id"])
        with open(manifest_path, "w", encoding="utf-8") as fp:
            json.dump(manifest, fp, ensure_ascii=False, indent=2)
        print("Registrado no manifest.json")
    else:
        print("Já estava no manifest.json")

    print("\n✅ Pronto! Não esqueça de editar data/" + part_id + ".json")

if __name__ == "__main__":
    main()
