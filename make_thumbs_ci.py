#!/usr/bin/env python3
"""
make_thumbs_ci.py — version pour GitHub Action.

Difference avec make_thumbs.py (celui de ton PC) :
  - ton PC : parcourt tout contenu/ et fait les vignettes manquantes.
  - ici    : recoit en argument la liste des images qui viennent de changer,
             et ne traite QUE celles-la. Beaucoup plus rapide, et ca evite
             de regenerer 2411 vignettes a chaque ajout.

Usage (appele automatiquement par l'Action) :
    python make_thumbs_ci.py contenu/nouvelle-oeuvre.jpg contenu/autre.png

Genere contenu/thumb/<nom>.webp pour chaque image donnee.
Ignore proprement tout ce qui n'est pas une image de contenu.
"""

import sys
from pathlib import Path
from PIL import Image

OUT_DIR = Path("contenu/thumb")
WIDTH   = 440
QUALITY = 80
EXTS    = {".jpg", ".jpeg", ".png", ".webp"}

def main(paths):
    OUT_DIR.mkdir(parents=True, exist_ok=True)
    done = 0

    for raw in paths:
        p = Path(raw)

        # Garde-fous : on ne traite que des images directement dans contenu/,
        # jamais un fichier deja dans thumb/ (sinon boucle), ni autre chose.
        if p.suffix.lower() not in EXTS:
            continue
        if p.parent != Path("contenu"):
            continue
        if not p.exists():
            # Image supprimee dans le commit : rien a generer.
            continue

        out = OUT_DIR / (p.stem + ".webp")
        try:
            with Image.open(p) as im:
                im = im.convert("RGB")
                if im.width > WIDTH:
                    h = round(im.height * WIDTH / im.width)
                    im = im.resize((WIDTH, h), Image.LANCZOS)
                im.save(out, "WEBP", quality=QUALITY, method=6)
            print(f"  vignette : {p.name} -> {out.name}")
            done += 1
        except Exception as ex:
            print(f"  !! {p.name} : {ex}")

    print(f"::notice::{done} vignette(s) generee(s)")

if __name__ == "__main__":
    main(sys.argv[1:])
