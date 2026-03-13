"""Model registry (S2)."""
import sys
from pathlib import Path

import pandas as pd
import streamlit as st

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from ui import global_footer, sidebar_shell
from utils import blank_to_em_dash_df, load_s2, multiselect_filter_mask

st.set_page_config(page_title="Models · Atlas", layout="wide")

sidebar_shell("models")
st.page_link("app.py", label="← Home", icon="🗺️")
st.title("Model browser")
st.markdown(
    "**Use this page** for **model-centric** questions: how many datasets/families each model links to, "
    "confidence mix, and quick links to HF/GitHub."
)
st.caption("Source: `data/release/supplementary_table_s2_model_registry_in_atlas.csv`")

df = load_s2()
if df.empty:
    st.error("Could not load S2 CSV.")
    st.stop()


def _opts(s):
    u = sorted(s.dropna().astype(str).unique())
    u = [x for x in u if str(x).strip()]
    return u if u else ["—"]


with st.sidebar:
    st.markdown("### Find rows")
    q = st.text_input("Search model id", value="", key="s2_search", placeholder="e.g. IAMJB/…")
    with st.expander("Refine", expanded=False):
        plat_sel = st.multiselect("Platform", options=_opts(df["Platform"]), default=[], key="s2_plat")
        mm_sel = st.multiselect(
            "Model modality", options=_opts(df["Model modality"]), default=[], key="s2_mm"
        )
plat_sel = st.session_state.get("s2_plat", [])
mm_sel = st.session_state.get("s2_mm", [])

m = pd.Series(True, index=df.index)
if q.strip():
    m &= df["Model ID"].astype(str).str.lower().str.contains(
        q.strip().lower(), na=False, regex=False
    )
m &= multiselect_filter_mask(df["Platform"], plat_sel)
m &= multiselect_filter_mask(df["Model modality"], mm_sel)

filtered = df.loc[m].copy()

sort_opt = st.selectbox(
    "Sort",
    [
        "Linked datasets, n (desc)",
        "Linked families, n (desc)",
        "High-confidence links, n (desc)",
        "Downloads / stars (desc)",
        "Model ID (asc)",
    ],
    key="s2_sort",
)


def num_series(name: str) -> pd.Series:
    return pd.to_numeric(filtered[name], errors="coerce")

if sort_opt == "Linked datasets, n (desc)":
    filtered = filtered.assign(_n=num_series("Linked datasets, n")).sort_values("_n", ascending=False, na_position="last").drop(columns="_n")
elif sort_opt == "Linked families, n (desc)":
    filtered = filtered.assign(_n=num_series("Linked families, n")).sort_values("_n", ascending=False, na_position="last").drop(columns="_n")
elif sort_opt == "High-confidence links, n (desc)":
    filtered = filtered.assign(_n=num_series("High-confidence links, n")).sort_values("_n", ascending=False, na_position="last").drop(columns="_n")
elif sort_opt == "Downloads / stars (desc)":
    filtered = filtered.assign(_n=num_series("Downloads / stars")).sort_values("_n", ascending=False, na_position="last").drop(columns="_n")
else:
    filtered = filtered.sort_values("Model ID", key=lambda s: s.astype(str).str.lower())

cols = [
    "Model ID",
    "Platform",
    "Model modality",
    "Linked datasets, n",
    "Linked families, n",
    "High-confidence links, n",
    "Medium-confidence links, n",
    "Downloads / stars",
    "Model URL",
    "Repository URL",
]
cols = [c for c in cols if c in filtered.columns]
out = filtered[cols].copy()
out = blank_to_em_dash_df(out)

col_cfg = {}
if "Model URL" in out.columns:
    col_cfg["Model URL"] = st.column_config.LinkColumn("Model URL", display_text="Model URL")
if "Repository URL" in out.columns:
    col_cfg["Repository URL"] = st.column_config.LinkColumn("Repository URL", display_text="Repository URL")

st.dataframe(
    out, use_container_width=True, hide_index=True, column_config=col_cfg, height=480
)
global_footer()
