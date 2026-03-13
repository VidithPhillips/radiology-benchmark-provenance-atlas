# Host the atlas app for free (Streamlit Community Cloud)

**Cost:** $0 · **Auth:** GitHub

---

## Stuck on “in the oven” / logs stop after “Resolved 38 packages”?

That almost always means the builder is on **Python 3.14** while **numpy/pandas** install hangs or never finishes.

**Python version cannot be changed after you deploy.** You have to start over:

1. **Delete** the app: [Manage app](https://share.streamlit.io) → **⋮** → **Delete app**  
   (Same subdomain, e.g. `radiology-atlas`, is free again right away.)

2. **Deploy again** → before clicking final Deploy, open **Advanced settings**.

3. Set **Python version** to **3.12** (or **3.11**). **Not 3.14.**

4. Save → Deploy again with:
   - **Repository:** `VidithPhillips/radiology-benchmark-provenance-atlas`
   - **Branch:** `main`
   - **Main file path:** `app/app.py`
   - **App URL:** e.g. `radiology-atlas`

Logs should then show install progress and **Running Streamlit** within a few minutes.

---

## First-time deploy (checklist)

1. [share.streamlit.io](https://share.streamlit.io) → GitHub login  
2. **New app** → repo + branch `main` + main file **`app/app.py`**  
3. **Advanced settings → Python 3.12** (required)  
4. Deploy  

---

## After deploy

- README / GitHub **Website** → your `https://….streamlit.app` URL  
- **Sleep:** first load after idle ~30s is normal on free tier  

## Notes

- Data: `data/release/` in repo — no secrets needed.  
- Docs: [Upgrade Python (delete + redeploy)](https://docs.streamlit.io/deploy/streamlit-community-cloud/manage-your-app/upgrade-python)
