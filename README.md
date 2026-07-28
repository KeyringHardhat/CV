# Kieron Harding CV

The website and download are driven from one source: [`_data/cv.json`](_data/cv.json).

## Updating the CV

Edit the JSON data, then generate the PDF locally:

```sh
python3 scripts/build_pdf.py
```

The generated PDF is intentionally constrained to one A4 page; the build fails if a content update would overflow it. The GitHub Actions workflow regenerates and commits `assets/Kieron-Harding-CV.pdf` whenever the CV data is pushed to `gh-pages`. GitHub Pages then serves the matching new page and PDF.
