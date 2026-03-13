"""Dataset summary (Table 2)."""
import sys
from pathlib import Path

import pandas as pd
import streamlit as st

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from ui import global_footer, sidebar_shell
from utils import (
    apply_family_display_column,
    blank_to_em_dash_df,
    load_table2,
    multiselect_filter_mask,
)

st.set_page_config(page_title="Datasets · Atlas", layout="wide")

sidebar_shell("datasets")
st.page_link("app.py", label="← Home", icon="🗺️")
st.title("Dataset browser")
st.markdown(
    "**Use this page** to see how many models tie to each canonical dataset, edge counts by confidence, "
    "and example models—good for **benchmark-centric** questions (e.g. “who clusters on CheXpert?”)."
)
st.caption("Source: `data/release/table2_dataset_summary.csv`")

df = load_table2()
if df.empty:
    st.error("Could not load table2 CSV (missing `data/release/table2_dataset_summary.csv`?).")
    st.stop()


def _opts(s):
    u = sorted(s.dropna().astype(str).unique())
    u = [x for x in u if str(x).strip()]
    return u if u else ["—"]


with st.sidebar:
    st.markdown("### Find rows")
    q = st.text_input("Search dataset name", value="", key="t2_search", placeholder="e.g. MIMIC, BraTS…")
    with st.expander("Refine columns", expanded=False):
        fam_sel = st.multiselect(
            "Benchmark family", options=_opts(df["Benchmark family"]), default=[], key="t2_fam"
        )
        mod_sel = st.multiselect("Modality", options=_opts(df["Modality"]), default=[], key="t2_mod")
        tier_sel = st.multiselect(
            "Benchmark tier", options=_opts(df["Benchmark tier"]), default=[], key="t2_tier"
        )
        access_sel = st.multiselect(
            "Access type", options=_opts(df["Access type"]), default=[], key="t2_acc"
        )
fam_sel = st.session_state.get("t2_fam", [])
mod_sel = st.session_state.get("t2_mod", [])
tier_sel = st.session_state.get("t2_tier", [])
access_sel = st.session_state.get("t2_acc", [])

m = pd.Series(True, index=df.index)
if q.strip():
    m &= df["Dataset"].astype(str).str.lower().str.contains(
        q.strip().lower(), na=False, regex=False
    )
m &= multiselect_filter_mask(df["Benchmark family"], fam_sel)
m &= multiselect_filter_mask(df["Modality"], mod_sel)
m &= multiselect_filter_mask(df["Benchmark tier"], tier_sel)
m &= multiselect_filter_mask(df["Access type"], access_sel)

filtered = df.loc[m].copy()

sort_opt = st.selectbox(
    "Sort",
    [
        "Linked models, n (desc)",
        "Atlas edges, n (desc)",
        "High-confidence edges, n (desc)",
        "Dataset (asc)",
    ],
    key="t2_sort",
)

def num_series(name: str) -> pd.Series:
    return pd.to_numeric(filtered[name], errors="coerce").fillna(0)

if sort_opt == "Linked models, n (desc)":
    filtered = filtered.assign(_n=num_series("Linked models, n")).sort_values("_n", ascending=False).drop(columns="_n")
elif sort_opt == "Atlas edges, n (desc)":
    filtered = filtered.assign(_n=num_series("Atlas edges, n")).sort_values("_n", ascending=False).drop(columns="_n")
elif sort_opt == "High-confidence edges, n (desc)":
    filtered = filtered.assign(_n=num_series("High-confidence edges, n")).sort_values("_n", ascending=False).drop(columns="_n")
else:
    filtered = filtered.sort_values("Dataset", key=lambda s: s.astype(str).str.lower())

cols = [
    "Dataset",
    "Benchmark family",
    "Modality",
    "Benchmark tier",
    "Access type",
    "Linked models, n",
    "Atlas edges, n",
    "High-confidence edges, n",
    "Medium-confidence edges, n",
    "Low-confidence edges, n",
    "Confidence profile",
    "Example linked models",
]
cols = [c for c in cols if c in filtered.columns]
out = filtered[cols].copy()
out = apply_family_display_column(out, "Benchmark family")
out = blank_to_em_dash_df(out)

st.dataframe(out, use_container_width=True, hide_index=True, height=420)
global_footer()
