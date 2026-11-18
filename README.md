# plaquette_gn

## installation :

- `python3.12` requis
- usage de `uv` conseillé

## utilisation
build_pdf.py accepte les options en ligne de commande :

- -i / --input : chemin du template HTML d'entrée (défaut : plaquette.html)
- -o / --output : chemin du PDF de sortie (défaut : même nom que l'entrée avec l'extension .pdf)
- --preview (optionnel) : génère en plus les aperçus PNG de chaque page

### Exemples d'utilisation avec uv

```bash
uv run python build_pdf.py -i plaquette_gn_fedegn.html -o plaquette_gn_fedegn.pdf
```
