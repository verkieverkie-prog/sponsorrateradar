# Sponsor Rate Radar

Free, sourced sponsorship rates for YouTubers, newsletter writers and podcasters.

- Data: `data/rates.json` (every row has a source_url)
- Settings: `config.json` (sponsor slot, newsletter link, submit form, contact)
- Build: `python3 build.py` writes the static site to `site/`
- Deploy: pushing to `main` runs GitHub Actions, which deploys to GitHub Pages
