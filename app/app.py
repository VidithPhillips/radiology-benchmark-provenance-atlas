"""
Public Radiology AI Benchmark Provenance Atlas — home = visual map + table.

Run: ./run_app.sh
"""
import sys
from pathlib import Path

try:
    import pandas as pd
except ImportError as e:
    if "numpy" in str(e).lower() or "_core" in str(e):
        sys.stderr.write("\nUse ./run_app.sh (repo .venv).\n\n")
    raise

import streamlit as st
import streamlit.components.v1 as components

sys.path.insert(0, str(Path(__file__).resolve().parent))

from ui import global_footer, sidebar_shell
from utils import (
    PATH_S1,
    apply_family_display_column,
    benchmark_constellation_figure,
    blank_to_em_dash_df,
    family_display_label,
    high_confidence_mask_s1,
    load_s1,
    multiselect_filter_mask,
    quick_view_mask_s1,
    mindmap_figure_to_clickable_html,
    radial_mindmap_figure,
    text_search_mask,
)

st.set_page_config(
    page_title="Provenance Atlas",
    layout="wide",
    initial_sidebar_state="expanded",
)

st.markdown(
    """
    <style>
      .block-container { padding-top: 1.5rem; max-width: 1280px; }
      h1 { font-weight: 600 !important; letter-spacing: -0.02em; color: #1D1D1F !important; }
      .atlas-sub { color: #86868B; font-size: 1.05rem; line-height:1.45; max-width: 38rem; margin-bottom: 1.25rem; }
      .hub-card {
        background: #FFFFFF; border-radius: 18px; padding: 1.25rem 1.5rem;
        border: 1px solid #D2D2D7; box-shadow: 0 4px 24px rgba(0,0,0,0.07);
        margin-bottom: 1rem;
      }
      .hub-card h2 { margin: 0 0 0.35rem 0; font-size: 1.35rem; font-weight: 600; color: #1D1D1F; line-height: 1.25; }
      .hub-card .meta { color: #86868B; font-size: 0.9rem; margin-bottom: 0.75rem; }
      div[data-testid="stMetricValue"] { font-variant-numeric: tabular-nums; color: #1D1D1F !important; }
      [data-testid="stExpander"] summary { color: #1D1D1F; font-weight: 500; }
    </style>
    """,
    unsafe_allow_html=True,
)

st.title("Public Radiology AI Benchmark Provenance Atlas")
st.markdown(
    "<p class='atlas-sub'>Explore <strong style='color:#1D1D1F'>which open models</strong> publicly link to "
    "<strong style='color:#1D1D1F'>which benchmarks</strong>—mind map first, full table when you need it. "
    "Not proof of training; mined from READMEs & model cards.</p>",
    unsafe_allow_html=True,
)

df = load_s1()
if df.empty or not PATH_S1.is_file():
    st.error(
        f"Could not load atlas CSV.\n\n`{PATH_S1}`\n\nRun from repo root (folder with `data/release/`)."
    )
    st.stop()


def _opts(series):
    u = sorted(series.dropna().astype(str).unique())
    u = [x for x in u if str(x).strip()]
    return u if u else ["(no values)"]


qv = st.radio(
    "Quick view",
    [
        "All edges",
        "High confidence only",
        "Open access datasets",
        "MIMIC family",
        "CheXpert family",
    ],
    horizontal=True,
    key="quick_view",
)

sidebar_shell("home")
with st.sidebar:
    st.markdown("### Scope")
    search = st.text_input(
        "Search",
        value="",
        key="s1_search",
        placeholder="Model or dataset…",
    )
    with st.expander("More filters", expanded=False):
        st.multiselect("Benchmark family", options=_opts(df["Benchmark family"]), key="fam")
        st.multiselect("Confidence", options=_opts(df["Confidence"]), key="conf")
        st.multiselect("Platform", options=_opts(df["Platform"]), key="plat")
        st.multiselect("Model modality", options=_opts(df["Model modality"]), key="mm")
        st.multiselect("Dataset modality", options=_opts(df["Dataset modality"]), key="dm")
        st.multiselect("Benchmark tier", options=_opts(df["Benchmark tier"]), key="tier")
        st.multiselect("Access type", options=_opts(df["Access type"]), key="access")

base_m = quick_view_mask_s1(df, qv)
m = base_m.copy()
m &= text_search_mask(df["Model ID"], df["Dataset"], search)
m &= multiselect_filter_mask(df["Benchmark family"], st.session_state.get("fam", []))
m &= multiselect_filter_mask(df["Confidence"], st.session_state.get("conf", []))
m &= multiselect_filter_mask(df["Platform"], st.session_state.get("plat", []))
m &= multiselect_filter_mask(df["Model modality"], st.session_state.get("mm", []))
m &= multiselect_filter_mask(df["Dataset modality"], st.session_state.get("dm", []))
m &= multiselect_filter_mask(df["Benchmark tier"], st.session_state.get("tier", []))
m &= multiselect_filter_mask(df["Access type"], st.session_state.get("access", []))
filtered = df.loc[m].copy()

# ——— Hero: mind map ———
st.markdown("##### Mind map")
st.caption(
    "**Green** = high · **orange** = medium · **violet** = low confidence. "
    "Rim opens only with Model/Repo URL. Center = dataset when listed."
)

counts = filtered.groupby("Dataset").size().sort_values(ascending=False)
dataset_names = counts.index.tolist()
if not dataset_names:
    st.warning("No edges match—widen Quick view or clear search.")
else:
    col_a, col_b = st.columns([1, 2.35])
    with col_a:
        choice = st.selectbox(
            "Benchmark at center",
            options=dataset_names,
            format_func=lambda d: f"{d}  ({counts[d]} models)",
            key="home_center_ds",
        )
        sub_ds = filtered[filtered["Dataset"] == choice]
        fam = sub_ds["Benchmark family"].iloc[0] if len(sub_ds) else ""
        access = sub_ds["Access type"].iloc[0] if len(sub_ds) else ""
        ds_url = ""
        if len(sub_ds) and "Dataset URL" in sub_ds.columns:
            u = str(sub_ds["Dataset URL"].iloc[0]).strip()
            if u.startswith("http"):
                ds_url = u
        st.markdown(
            f"<div class='hub-card'><h2>{choice}</h2>"
            f"<div class='meta'>{family_display_label(fam)} · {access}</div></div>",
            unsafe_allow_html=True,
        )
        if ds_url:
            st.link_button("Open benchmark / dataset page →", ds_url, use_container_width=True)
    with col_b:
        try:
            import plotly.graph_objects  # noqa: F401

            fig, _meta = radial_mindmap_figure(filtered, choice)
            html = mindmap_figure_to_clickable_html(fig, div_id="atlas-mindmap-home", height=620)
            components.html(html, height=640, scrolling=False)
        except ImportError:
            st.info("Install plotly: `./run_app.sh`")

with st.expander("Benchmark map (all datasets in this view)", expanded=False):
    try:
        import plotly.graph_objects  # noqa: F401
        st.plotly_chart(benchmark_constellation_figure(filtered), use_container_width=True)
    except ImportError:
        pass

st.markdown("---")
st.markdown("##### Numbers for this view")
c1, c2, c3, c4 = st.columns(4)
with c1:
    st.metric("Edges", f"{len(filtered):,}")
with c2:
    st.metric("Models", f"{filtered['Model ID'].nunique():,}")
with c3:
    st.metric("Datasets", f"{filtered['Dataset'].nunique():,}")
with c4:
    st.metric("High-confidence edges", f"{int(high_confidence_mask_s1(filtered).sum()):,}")

# Table secondary
with st.expander("Full edge table", expanded=False):
    sort_choice = st.selectbox(
        "Sort",
        ["Evidence (desc)", "Model A→Z", "Dataset A→Z"],
        key="home_sort",
    )
    t = filtered.copy()
    if sort_choice == "Evidence (desc)" and "Evidence count" in t.columns:
        t = t.assign(_e=pd.to_numeric(t["Evidence count"], errors="coerce")).sort_values(
            "_e", ascending=False
        ).drop(columns="_e")
    elif sort_choice == "Model A→Z":
        t = t.sort_values("Model ID", key=lambda s: s.astype(str).str.lower())
    else:
        t = t.sort_values("Dataset", key=lambda s: s.astype(str).str.lower())

    main_cols = [
        "Model ID",
        "Platform",
        "Model modality",
        "Dataset",
        "Benchmark family",
        "Dataset modality",
        "Benchmark tier",
        "Access type",
        "Confidence",
        "Evidence count",
        "Evidence types",
        "Matched aliases",
    ]
    main_cols = [c for c in main_cols if c in t.columns]
    display_main = blank_to_em_dash_df(apply_family_display_column(t[main_cols].copy()))
    st.dataframe(
        display_main,
        use_container_width=True,
        hide_index=True,
        height=380,
        column_config={
            "Model ID": st.column_config.TextColumn("Model ID", width="large"),
            "Dataset": st.column_config.TextColumn("Dataset", width="medium"),
        },
    )

with st.expander("Source URLs (this view)"):
    url_cols = ["Model ID", "Dataset", "Model URL", "Dataset URL", "Repository URL"]
    url_cols = [c for c in url_cols if c in filtered.columns]
    if url_cols:
        show = blank_to_em_dash_df(filtered[url_cols].copy())
        lc = {c: st.column_config.LinkColumn(c) for c in ["Model URL", "Dataset URL", "Repository URL"] if c in show.columns}
        st.dataframe(show, use_container_width=True, hide_index=True, height=240, column_config=lc)

global_footer()
