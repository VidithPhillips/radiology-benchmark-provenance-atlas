"""
Mind-map style graph: one benchmark hub + spokes; benchmark overview; optional bipartite.
"""
import sys
from pathlib import Path

import pandas as pd
import streamlit as st
import streamlit.components.v1 as components

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from ui import global_footer, sidebar_shell
from utils import (
    PATH_S1,
    benchmark_constellation_figure,
    bipartite_atlas_figure,
    load_s1,
    multiselect_filter_mask,
    quick_view_mask_s1,
    mindmap_figure_to_clickable_html,
    radial_mindmap_figure,
    text_search_mask,
)

st.set_page_config(page_title="Atlas map · Atlas", layout="wide")

sidebar_shell("map")
st.page_link("app.py", label="← Home (same mind map)", icon="🗺️")

try:
    import plotly.graph_objects  # noqa: F401
except ImportError:
    st.title("Atlas map")
    st.error("Install Plotly: `./run_app.sh` or `.venv/bin/pip install plotly`")
    st.stop()

st.title("Atlas map")
st.markdown(
    """
The **home page** already opens with the mind map. Here you can **switch datasets** with the same filters,
open the **benchmark ring** full-screen, or use **Advanced bipartite** after narrowing.

**Mind map:** one benchmark at center, spokes = models. **Benchmark map:** all datasets, dot size ∝ links.
**Bipartite:** dense; use High confidence or one family first.
"""
)

df = load_s1()
if df.empty or not PATH_S1.is_file():
    st.error("Could not load S1 CSV.")
    st.stop()


def _opts(series):
    u = sorted(series.dropna().astype(str).unique())
    u = [x for x in u if str(x).strip()]
    return u if u else ["(no values)"]


with st.sidebar:
    st.markdown("### Scope")
    qv = st.radio(
        "Quick view",
        [
            "All edges",
            "High confidence only",
            "Open access datasets",
            "MIMIC family",
            "CheXpert family",
        ],
        key="map_qv",
    )
    search = st.text_input("Search (optional)", key="map_search", placeholder="Narrows mind map…")
    with st.expander("More filters", expanded=False):
        st.multiselect("Benchmark family", options=_opts(df["Benchmark family"]), key="m_fam")
        st.multiselect("Confidence", options=_opts(df["Confidence"]), key="m_conf")
        st.multiselect("Access type", options=_opts(df["Access type"]), key="m_acc")

base_m = quick_view_mask_s1(df, qv)
m = base_m.copy()
m &= text_search_mask(df["Model ID"], df["Dataset"], st.session_state.get("map_search", ""))
m &= multiselect_filter_mask(df["Benchmark family"], st.session_state.get("m_fam", []))
m &= multiselect_filter_mask(df["Confidence"], st.session_state.get("m_conf", []))
m &= multiselect_filter_mask(df["Access type"], st.session_state.get("m_acc", []))
filtered = df.loc[m].copy()

mode = st.radio(
    "View",
    ["Mind map (one benchmark)", "Benchmark map (overview)", "Advanced: full bipartite"],
    horizontal=True,
    key="map_mode",
)

if mode == "Mind map (one benchmark)":
    counts = filtered.groupby("Dataset").size().sort_values(ascending=False)
    dataset_names = counts.index.tolist()
    if not dataset_names:
        st.warning("No edges in this filter—widen Quick view or clear search.")
        st.stop()
    default_ds = dataset_names[0]
    idx = dataset_names.index(default_ds) if default_ds in dataset_names else 0
    choice = st.selectbox(
        "Center this benchmark",
        options=dataset_names,
        index=idx,
        format_func=lambda d: f"{d}  ({counts[d]} models)",
        help="Each option is one canonical dataset; spokes = models with an atlas link to it.",
    )
    st.caption(
        "Spokes are **non-crossing**. Darker lines = higher confidence. Hover rim dots for full model id."
    )
    fig, meta = radial_mindmap_figure(filtered, choice)
    if meta.get("dataset_url"):
        st.link_button("Dataset page →", meta["dataset_url"])
    html = mindmap_figure_to_clickable_html(fig, div_id="atlas-mindmap-page", height=620)
    components.html(html, height=640, scrolling=False)

elif mode == "Benchmark map (overview)":
    st.caption("Larger nodes = more linked models. Hover for family, access, and count.")
    fig = benchmark_constellation_figure(filtered)
    st.plotly_chart(fig, use_container_width=True, config={"displayModeBar": True})

else:
    st.caption("Full left-right bipartite layout—best with **High confidence** or one family only.")
    if len(filtered) > 120:
        st.warning("Still dense; bipartite works better under ~80 edges here.")
    fig = bipartite_atlas_figure(filtered)
    st.plotly_chart(fig, use_container_width=True, config={"displayModeBar": True})

st.caption("Counts and URLs: **Home** table + released CSV remain authoritative.")
global_footer()
