# Host the atlas app for free (Streamlit Community Cloud)

**Cost:** $0 · **Auth:** GitHub · **Time:** ~2 minutes

Streamlit hosts Python apps and pulls your code from GitHub. No credit card.

## Steps

1. **Open** [share.streamlit.io](https://share.streamlit.io) and sign in with **GitHub** (authorize Streamlit if asked).

2. **New app** → **Deploy a public app from GitHub**.

3. **Repository:** choose `VidithPhillips/radiology-benchmark-provenance-atlas` (or your fork).

4. **Branch:** `main`

5. **Main file path:** `app/app.py`  
   (This is the entrypoint; multipage apps under `app/pages/` load automatically.)

6. **App URL:** pick a subdomain, e.g. `radiology-atlas` → live at  
   `https://radiology-atlas.streamlit.app`

7. **Deploy.** First build installs `requirements.txt` (~1–2 min).

## After deploy

- Put the public URL in the **GitHub repo → Settings → Website** (optional).
- Add a badge or link at the top of **README.md** so visitors click straight from GitHub.

## Notes

- **CSV data** lives in `data/release/` in the repo — already on GitHub, so the hosted app reads it like local.
- **Sleep:** free apps spin down after idle; first visitor after sleep may wait ~30s (normal).
- **Secrets:** this app needs none. Don’t add API keys unless you add features that need them.

## Alternative (also free, more setup)

- **Hugging Face Spaces** (Streamlit SDK) — good if you already use HF; config is different from above.

If deploy fails, check the Streamlit Cloud **logs**: usually a missing dependency → add to `requirements.txt` and push.
