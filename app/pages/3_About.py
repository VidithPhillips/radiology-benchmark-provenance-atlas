"""About the atlas."""
import sys
from pathlib import Path

import streamlit as st

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from ui import REPO_URL, global_footer, sidebar_shell

st.set_page_config(page_title="About · Atlas", layout="wide")

sidebar_shell("about")
st.page_link("app.py", label="← Home", icon="🗺️")
st.title("About this app")

st.markdown(
    """
<div style="max-width:40rem;line-height:1.55;color:#1D1D1F">

### How to use (workflow)

| Step | Where | What |
|------|--------|------|
| 1 | **Home** | Choose **Quick view** (e.g. MIMIC family) and a **benchmark** in the dropdown. |
| 2 | Same | Read the **mind map**: green / orange / violet = confidence. **Click** rim dots only when the atlas lists a model or repo URL. |
| 3 | **Datasets** | Benchmark-centric table: how many models per dataset, confidence mix. |
| 4 | **Models** | Model-centric table + HF/repo links. |
| 5 | **Atlas map** | Extra views (benchmark ring, bipartite). Main map lives on **Home**. |
| 6 | Expanders on Home | Full **edge table** and **URLs** for the current filter. |

---

### What the atlas is

Benchmark-centered links between **open radiology AI models** and **canonical datasets**, from **public text**
(Hugging Face, GitHub)—not private training logs.

---

### Confidence & tier

- **Confidence** (high / medium / low): strength of repeated public evidence—not proof of training.  
- **Benchmark tier**: registry slot (e.g. canonical vs derived); see paper/repo for definitions.

---

### Current release (snapshot)

| Metric | Count |
|--------|------:|
| Models | 117 |
| Datasets | 18 |
| Edges | 163 |
| High / medium / low edges | 82 / 78 / 3 |

---

### Cite & source

If you use the atlas or this app in research, cite the **paper** (when available) and point to the repository:

**Repository:** [github.com/…/radiology-benchmark-provenance-atlas]({repo})

Released tables: `data/release/supplementary_table_s1_full_atlas_edge_list.csv` (edges),  
`table2_dataset_summary.csv` (datasets), `supplementary_table_s2_model_registry_in_atlas.csv` (models).

---

### Limitations

Public provenance only; absence of a link does not imply non-use. URLs in the CSV can go stale—rim clicks use only explicit model/repo URLs.

</div>
""".format(repo=REPO_URL),
    unsafe_allow_html=True,
)

with st.expander("Copy-paste citation (placeholder)"):
    st.code(
        "Author(s). Public Radiology AI Benchmark Provenance Atlas. "
        "GitHub: " + REPO_URL + " (accessed YYYY-MM-DD).",
        language=None,
    )

global_footer()
