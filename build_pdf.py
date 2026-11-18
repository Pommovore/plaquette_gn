"""Script de génération de plaquette PDF à partir d'un template HTML."""

import argparse
from pathlib import Path
import subprocess
import sys


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Génère un PDF A4 à partir d'un template HTML via Google Chrome headless."
    )
    parser.add_argument(
        "-i",
        "--input",
        type=Path,
        default=Path("plaquette.html"),
        help="Chemin du fichier HTML d'entrée (défaut : plaquette.html)",
    )
    parser.add_argument(
        "-o",
        "--output",
        type=Path,
        default=None,
        help="Chemin du fichier PDF de sortie (défaut : même nom que l'entrée avec .pdf)",
    )
    parser.add_argument(
        "--preview",
        action="store_true",
        help="Génère également des aperçus PNG des pages via pdftoppm",
    )
    return parser.parse_args()


def build_pdf(html_path: Path, pdf_path: Path, preview: bool = False) -> None:
    html_path = html_path.resolve()
    pdf_path = pdf_path.resolve()

    if not html_path.exists():
        print(f"Erreur : fichier introuvable : {html_path}", file=sys.stderr)
        sys.exit(1)

    pdf_path.parent.mkdir(parents=True, exist_ok=True)

    cmd = [
        "google-chrome",
        "--headless",
        "--disable-gpu",
        "--no-sandbox",
        "--no-pdf-header-footer",
        f"--print-to-pdf={pdf_path}",
        html_path.as_uri(),
    ]

    result = subprocess.run(cmd, capture_output=True, text=True)
    if result.returncode != 0:
        print("Erreur lors de la génération du PDF :", result.stderr, file=sys.stderr)
        sys.exit(result.returncode)

    print(f"PDF généré avec succès : {pdf_path}")

    if preview:
        preview_prefix = pdf_path.parent / f"{pdf_path.stem}_page"
        subprocess.run(
            ["pdftoppm", "-png", "-r", "150", str(pdf_path), str(preview_prefix)],
            check=True,
        )
        previews = sorted(pdf_path.parent.glob(f"{pdf_path.stem}_page-*.png"))
        print(f"Nombre de pages générées : {len(previews)}")
        for p in previews:
            print(f"  - {p.name}")


def main() -> None:
    args = parse_args()
    output_path = args.output if args.output is not None else args.input.with_suffix(".pdf")
    build_pdf(args.input, output_path, preview=args.preview)


if __name__ == "__main__":
    main()
