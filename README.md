# Kieron Harding CV

The website and download are generated from one source: [`_data/cv.json`](_data/cv.json). The terminal-style website uses plain HTML and CSS with a small optional script for animation controls. It has no external fonts or frontend dependencies and deploys directly to GitHub Pages without Jekyll. All CV content and ordinary navigation work without JavaScript.

The terminal commands are decorative; there is no interactive command prompt. The effects control pauses animation, the intro can be replayed, and reduced-motion preferences disable animation automatically.

## Local preview

Generate the HTML and serve the repository:

```sh
python3 scripts/build_site.py
python3 -m http.server 8000 --bind 127.0.0.1
```

Open `http://127.0.0.1:8000/` and refresh after edits. Edit `assets/css/style.css` for styling and `scripts/build_site.py` for markup; `index.html` is generated output. Keep `.nojekyll` and `CNAME` when publishing the repository root to GitHub Pages.

## Updating the CV

Edit the JSON data, then generate the website and PDF locally:

The website builder uses only the Python standard library. The PDF builder also needs `reportlab` and `pypdf` installed.

```sh
python3 scripts/build_pdf.py
python3 scripts/build_site.py
```

The generated PDF is intentionally constrained to one A4 page; the build fails if a content update would overflow it. The GitHub Actions workflow regenerates and commits the matching page and PDF whenever the CV data is pushed to `gh-pages`.
