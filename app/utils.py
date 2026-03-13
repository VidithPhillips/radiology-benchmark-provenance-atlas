"""
Helpers for the Provenance Atlas Streamlit MVP: paths, loading, display.
"""
from pathlib import Path

import pandas as pd
import streamlit as st

# Repository root (parent of app/)
REPO_ROOT = Path(__file__).resolve().parent.parent

PATH_S1 = REPO_ROOT / "data" / "release" / "supplementary_table_s1_full_atlas_edge_list.csv"
PATH_S2 = REPO_ROOT / "data" / "release" / "supplementary_table_s2_model_registry_in_atlas.csv"
PATH_TABLE2 = REPO_ROOT / "data" / "release" / "table2_dataset_summary.csv"

EM_DASH = "—"

# Display-only mapping for benchmark family labels (raw CSV values unchanged in source dfs)
FAMILY_DISPLAY_MAP = {
    "Mimic": "MIMIC",
    "Chexpert": "CheXpert",
    "Mri": "MRI",
    "Radgraph": "RadGraph",
    "Vindr": "VinDr",
    "Radialog": "RaDialog",
}


def family_display_label(raw: object) -> str:
    if pd.isna(raw) or str(raw).strip() == "":
        return EM_DASH
    s = str(raw).strip()
    return FAMILY_DISPLAY_MAP.get(s, s)


@st.cache_data(show_spinner=False)
def load_s1() -> pd.DataFrame:
    if not PATH_S1.is_file():
        return pd.DataFrame()
    return pd.read_csv(PATH_S1, dtype=str, na_filter=False)


@st.cache_data(show_spinner=False)
def load_s2() -> pd.DataFrame:
    if not PATH_S2.is_file():
        return pd.DataFrame()
    return pd.read_csv(PATH_S2, dtype=str, na_filter=False)


@st.cache_data(show_spinner=False)
def load_table2() -> pd.DataFrame:
    if not PATH_TABLE2.is_file():
        return pd.DataFrame()
    return pd.read_csv(PATH_TABLE2, dtype=str, na_filter=False)


def is_blank(v: object) -> bool:
    if v is None or (isinstance(v, float) and pd.isna(v)):
        return True
    s = str(v).strip()
    return s == "" or s.lower() == "nan"


def blank_to_em_dash_df(df: pd.DataFrame) -> pd.DataFrame:
    """Copy for display: empty/NaN -> em dash. Does not mutate input."""
    out = df.copy()
    for c in out.columns:
        out[c] = out[c].map(
            lambda x: EM_DASH if is_blank(x) else str(x).strip()
        )
    return out


def apply_family_display_column(df: pd.DataFrame, col: str = "Benchmark family") -> pd.DataFrame:
    """Add display column; use for UI only."""
    out = df.copy()
    if col in out.columns:
        out[col] = out[col].map(family_display_label)
    return out


def text_search_mask(series_a: pd.Series, series_b: pd.Series, query: str) -> pd.Series:
    q = (query or "").strip().lower()
    if not q:
        return pd.Series(True, index=series_a.index)
    a = series_a.astype(str).str.lower()
    b = series_b.astype(str).str.lower()
    return a.str.contains(q, na=False, regex=False) | b.str.contains(q, na=False, regex=False)


def multiselect_filter_mask(series: pd.Series, selected: list) -> pd.Series:
    if not selected:
        return pd.Series(True, index=series.index)
    return series.astype(str).isin(selected)


def high_confidence_mask_s1(df: pd.DataFrame) -> pd.Series:
    if "Confidence" not in df.columns:
        return pd.Series(False, index=df.index)
    return df["Confidence"].astype(str).str.lower().str.strip() == "high"


def quick_view_mask_s1(df: pd.DataFrame, qv: str) -> pd.Series:
    """Preset slices for S1 (same semantics as Atlas Explorer Quick view)."""
    base = pd.Series(True, index=df.index)
    if qv == "High confidence only":
        base &= df["Confidence"].astype(str).str.lower().str.strip() == "high"
    elif qv == "Open access datasets":
        base &= df["Access type"].astype(str).str.lower().str.strip() == "open"
    elif qv == "MIMIC family":
        base &= df["Benchmark family"].astype(str).str.strip() == "Mimic"
    elif qv == "CheXpert family":
        base &= df["Benchmark family"].astype(str).str.strip() == "Chexpert"
    return base


def bipartite_atlas_figure(filtered: pd.DataFrame):
    """
    Bipartite layout: models (left) ↔ datasets (right).
    Edge color = confidence. Hover nodes for full id/name.
    """
    import plotly.graph_objects as go

    if filtered.empty or "Model ID" not in filtered.columns or "Dataset" not in filtered.columns:
        fig = go.Figure()
        fig.add_annotation(
            text="No edges in this view—widen Quick view or clear filters.",
            xref="paper",
            yref="paper",
            x=0.5,
            y=0.5,
            showarrow=False,
            font=dict(size=14, color="#666"),
        )
        fig.update_layout(
            height=420,
            margin=dict(l=20, r=20, t=20, b=20),
            plot_bgcolor="#fafbfc",
        )
        return fig

    deg_m = filtered.groupby("Model ID", sort=False).size().sort_values(ascending=False)
    deg_d = filtered.groupby("Dataset", sort=False).size().sort_values(ascending=False)
    model_order = deg_m.index.tolist()
    dataset_order = deg_d.index.tolist()
    n_m, n_d = len(model_order), len(dataset_order)

    def y_slot(i: int, n: int) -> float:
        if n <= 1:
            return 0.5
        return 1.0 - (i / (n - 1)) * 0.92 - 0.04

    pos_m = {m: (0.0, y_slot(i, n_m)) for i, m in enumerate(model_order)}
    pos_d = {d: (1.0, y_slot(i, n_d)) for i, d in enumerate(dataset_order)}

    # Distinct per confidence (hue-separated for quick scan)
    conf_style = {
        "high": dict(color="rgba(5,150,105,0.55)", width=1.4),   # emerald
        "medium": dict(color="rgba(234,88,12,0.5)", width=1.2),  # orange
        "low": dict(color="rgba(124,58,237,0.45)", width=1.0),   # violet
    }

    fig = go.Figure()
    for conf_label, style in conf_style.items():
        sub = filtered[
            filtered["Confidence"].astype(str).str.lower().str.strip() == conf_label
        ]
        if sub.empty:
            continue
        ex, ey = [], []
        for _, r in sub.iterrows():
            m, d = r["Model ID"], r["Dataset"]
            if m not in pos_m or d not in pos_d:
                continue
            x0, y0 = pos_m[m]
            x1, y1 = pos_d[d]
            ex += [x0, x1, None]
            ey += [y0, y1, None]
        fig.add_trace(
            go.Scatter(
                x=ex,
                y=ey,
                mode="lines",
                line=style,
                name=f"{conf_label} confidence",
                hoverinfo="skip",
                showlegend=True,
            )
        )

    fig.add_trace(
        go.Scatter(
            x=[pos_m[m][0] for m in model_order],
            y=[pos_m[m][1] for m in model_order],
            mode="markers",
            marker=dict(size=9, color="#0f3d5c", line=dict(width=1, color="white")),
            name="Models",
            hovertext=[str(m) for m in model_order],
            hoverinfo="text",
        )
    )
    fig.add_trace(
        go.Scatter(
            x=[pos_d[d][0] for d in dataset_order],
            y=[pos_d[d][1] for d in dataset_order],
            mode="markers",
            marker=dict(
                size=11,
                symbol="square",
                color="#2d6a4f",
                line=dict(width=1, color="white"),
            ),
            name="Datasets",
            hovertext=[
                (
                    f"{d} · {family_display_label(filtered.loc[filtered['Dataset'] == d, 'Benchmark family'].iloc[0])}"
                    if "Benchmark family" in filtered.columns
                    and len(filtered.loc[filtered["Dataset"] == d])
                    else str(d)
                )
                for d in dataset_order
            ],
            hoverinfo="text",
        )
    )

    fig.update_layout(
        title=dict(
            text="Model ↔ dataset links (bipartite)",
            font=dict(size=15, color="#1c1c1c"),
            x=0.5,
            xanchor="center",
        ),
        xaxis=dict(visible=False, range=[-0.08, 1.08], fixedrange=True),
        yaxis=dict(visible=False, range=[-0.02, 1.02], scaleanchor="x", scaleratio=1.2, fixedrange=True),
        plot_bgcolor="#fafbfc",
        paper_bgcolor="#fafbfc",
        height=min(720, 320 + max(n_m, n_d) * 5),
        margin=dict(l=8, r=8, t=48, b=8),
        legend=dict(
            orientation="h",
            yanchor="bottom",
            y=1.02,
            xanchor="center",
            x=0.5,
            font=dict(size=11),
        ),
        hovermode="closest",
    )
    fig.add_annotation(x=0, y=1.06, xref="paper", yref="paper", text="Models", showarrow=False, font=dict(size=12, color="#0f3d5c"))
    fig.add_annotation(x=1, y=1.06, xref="paper", yref="paper", text="Datasets", showarrow=False, font=dict(size=12, color="#2d6a4f"), xanchor="right")
    return fig


def _model_page_url(row: pd.Series) -> str:
    """
    Clickable model link only when the release table has an explicit URL.
    No guessed HF paths (those often 404). Dataset URL never used here.
    """
    for k in ("Model URL", "Repository URL"):
        if k in row.index:
            v = str(row[k]).strip()
            if v.startswith("http"):
                return v
    return ""


def radial_mindmap_figure(filtered: pd.DataFrame, dataset_name: str):
    """
    One dataset at center; models on a ring. Rim nodes carry customdata [url, id] for Streamlit selection.
    Hub has no label (readability)—title lives outside in Streamlit.
    """
    import numpy as np
    import plotly.graph_objects as go

    sub = filtered[filtered["Dataset"].astype(str) == str(dataset_name)].copy()
    if sub.empty:
        fig = go.Figure()
        fig.add_annotation(
            text="No links for this dataset in the current filter.",
            xref="paper",
            yref="paper",
            x=0.5,
            y=0.5,
            showarrow=False,
            font=dict(size=15, color="#1D1D1F"),
        )
        fig.update_layout(height=400, plot_bgcolor="#ECECF0", paper_bgcolor="#ECECF0")
        return fig, {"dataset_url": "", "dataset_name": dataset_name}

    def rank_conf(s):
        s = str(s).lower().strip()
        return {"high": 0, "medium": 1, "low": 2}.get(s, 3)

    sub = sub.sort_values(
        "Confidence", key=lambda c: c.map(rank_conf)
    ).drop_duplicates(subset=["Model ID"], keep="first")

    models = sub["Model ID"].astype(str).tolist()
    n = len(models)
    theta = np.linspace(0, 2 * np.pi, n, endpoint=False)
    R = 1.12
    xm, ym = R * np.cos(theta), R * np.sin(theta)

    # High = green, medium = orange, low = violet (rim + spoke match)
    conf_line = {"high": "#059669", "medium": "#EA580C", "low": "#7C3AED"}
    conf_dot = dict(conf_line)
    conf_default = "#64748B"

    fig = go.Figure()
    # Soft vignette
    fig.add_shape(
        type="circle",
        xref="x",
        yref="y",
        x0=-0.35,
        y0=-0.35,
        x1=0.35,
        y1=0.35,
        fillcolor="rgba(255,255,255,0.85)",
        line=dict(width=0),
        layer="below",
    )

    for i, m in enumerate(models):
        row = sub[sub["Model ID"] == m].iloc[0]
        c = str(row["Confidence"]).lower().strip()
        lc = conf_line.get(c, conf_default)
        fig.add_trace(
            go.Scatter(
                x=[0, xm[i]],
                y=[0, ym[i]],
                mode="lines",
                line=dict(width=2.2, color=lc),
                hoverinfo="skip",
                showlegend=False,
            )
        )

    ds_url = ""
    if "Dataset URL" in sub.columns:
        u = str(sub["Dataset URL"].iloc[0]).strip()
        if u.startswith("http"):
            ds_url = u

    fig.add_trace(
        go.Scatter(
            x=[0],
            y=[0],
            mode="markers",
            marker=dict(
                size=32,
                color="#1D1D1F",
                line=dict(width=4, color="#FFFFFF"),
                opacity=1,
            ),
            hoverinfo="text",
            hovertext=f"<b>{dataset_name}</b><br>Click to open dataset page" if ds_url else f"<b>{dataset_name}</b>",
            customdata=[[ds_url or "", dataset_name]],
            showlegend=False,
        )
    )

    hover_models = []
    customdata = []
    rim_colors = []
    for m in models:
        row = sub[sub["Model ID"] == m].iloc[0]
        ev = row.get("Evidence count", "—")
        c = str(row["Confidence"]).lower().strip()
        url = _model_page_url(row)
        if url:
            hover_models.append(
                f"<b>{m}</b><br>{c} confidence · evidence {ev}<br><i>Click to open</i>"
            )
        else:
            hover_models.append(
                f"<b>{m}</b><br>{c} confidence · evidence {ev}<br><span style='color:#86868B'>No model/repo URL in atlas</span>"
            )
        customdata.append([url if url else "", m])
        rim_colors.append(conf_dot.get(c, conf_default))

    fig.add_trace(
        go.Scatter(
            x=xm,
            y=ym,
            mode="markers",
            marker=dict(
                size=16,
                color=rim_colors,
                line=dict(width=3, color="#FFFFFF"),
            ),
            hovertext=hover_models,
            hoverinfo="text",
            customdata=customdata,
            name="models",
            showlegend=False,
        )
    )

    for leg_name, leg_color in (
        ("High confidence", conf_line["high"]),
        ("Medium confidence", conf_line["medium"]),
        ("Low confidence", conf_line["low"]),
    ):
        fig.add_trace(
            go.Scatter(
                x=[None],
                y=[None],
                mode="markers",
                marker=dict(size=12, color=leg_color, line=dict(width=2, color="#FFF")),
                name=leg_name,
                showlegend=True,
            )
        )

    if n <= 20:
        short = [f"{m[:18]}…" if len(m) > 20 else m for m in models]
        fig.add_trace(
            go.Scatter(
                x=xm * 1.14,
                y=ym * 1.14,
                mode="text",
                text=short,
                textfont=dict(size=10, color="#1D1D1F", family="system-ui, sans-serif"),
                hoverinfo="skip",
                showlegend=False,
            )
        )

    pad = 1.5
    fig.update_layout(
        title=dict(
            text=f"<span style='color:#1D1D1F;font-weight:600'>{n} models</span> "
            f"<span style='color:#86868B'>· green / orange / violet = confidence</span>",
            font=dict(size=16, family="system-ui, sans-serif"),
            x=0.5,
            xanchor="center",
        ),
        xaxis=dict(visible=False, range=[-pad, pad], fixedrange=True, zeroline=False),
        yaxis=dict(visible=False, range=[-pad, pad], scaleanchor="x", scaleratio=1, fixedrange=True, zeroline=False),
        plot_bgcolor="#ECECF0",
        paper_bgcolor="#ECECF0",
        height=620,
        margin=dict(l=20, r=20, t=72, b=72),
        showlegend=True,
        legend=dict(
            orientation="h",
            yanchor="top",
            y=-0.02,
            xanchor="center",
            x=0.5,
            bgcolor="rgba(255,255,255,0.92)",
            bordercolor="#D2D2D7",
            borderwidth=1,
            font=dict(size=12, color="#1D1D1F"),
        ),
        font=dict(color="#1D1D1F", family="system-ui, sans-serif"),
        uirevision="mindmap",
        dragmode=False,
    )
    meta = {"dataset_url": ds_url, "dataset_name": dataset_name}
    return fig, meta


def mindmap_figure_to_clickable_html(fig, div_id: str = "atlas-mindmap", height: int = 640) -> str:
    """Plotly figure as HTML; rim + hub clicks open customdata[0] in a new tab."""
    import plotly.io as pio

    html = pio.to_html(
        fig,
        include_plotlyjs="cdn",
        full_html=True,
        div_id=div_id,
        config={"displayModeBar": True, "responsive": True},
    )
    script = f"""
<script>
(function() {{
  function run() {{
    var el = document.getElementById("{div_id}");
    if (!el) return;
    el.on("plotly_click", function(ev) {{
      var p = ev.points && ev.points[0];
      if (!p || p.customdata === undefined || p.customdata === null) return;
      var cd = p.customdata;
      var url = (Array.isArray(cd) || (typeof cd === "object" && cd.length !== undefined)) ? cd[0] : cd;
      url = url && String(url).trim();
      if (!url || url.indexOf("http") !== 0) return;
      window.open(url, "_blank", "noopener,noreferrer");
    }});
  }}
  if (document.readyState === "complete") run();
  else window.addEventListener("load", run);
  setTimeout(run, 300);
}})();
</script>
"""
    return html.replace("</body>", script + "</body>")


def benchmark_constellation_figure(filtered: pd.DataFrame):
    """Only dataset nodes on a ring—sizes by #links. No crossing edges."""
    import numpy as np
    import plotly.graph_objects as go

    if filtered.empty:
        fig, _ = radial_mindmap_figure(filtered, "")
        return fig

    g = (
        filtered.groupby("Dataset", sort=False)
        .agg(
            n=("Model ID", "count"),
            family=("Benchmark family", "first"),
            access=("Access type", "first"),
        )
        .reset_index()
    )
    g = g.sort_values("n", ascending=False)
    names = g["Dataset"].tolist()
    k = len(names)
    theta = np.linspace(np.pi / 2, -3 * np.pi / 2, k, endpoint=False)
    R = 1.2
    x, y = R * np.cos(theta), R * np.sin(theta)
    sizes = (12 + np.sqrt(g["n"].values) * 4).clip(14, 52)

    fig = go.Figure()
    fig.add_trace(
        go.Scatter(
            x=x,
            y=y,
            mode="markers",
            marker=dict(
                size=sizes,
                color="#0071E3",
                opacity=0.92,
                line=dict(width=2, color="#FFFFFF"),
            ),
            hovertext=[
                f"<b>{row.Dataset}</b><br>{family_display_label(row.family)} · {row.access}<br>{int(row.n)} linked models"
                for row in g.itertuples(index=False)
            ],
            hoverinfo="text",
            showlegend=False,
        )
    )
    for i, row in enumerate(g.itertuples(index=False)):
        short = row.Dataset if len(row.Dataset) <= 20 else row.Dataset[:18] + "…"
        fig.add_annotation(
            x=x[i] * 1.22,
            y=y[i] * 1.22,
            text=f"<b style='color:#1D1D1F'>{short}</b><br><span style='font-size:10px;color:#86868B'>{int(row.n)} models</span>",
            showarrow=False,
            xref="x",
            yref="y",
        )

    fig.add_trace(
        go.Scatter(
            x=[0],
            y=[0],
            mode="markers",
            marker=dict(size=30, color="#1D1D1F", line=dict(width=2, color="#FFFFFF")),
            showlegend=False,
            hoverinfo="text",
            hovertext="Benchmarks in view — hover ring",
        )
    )
    fig.add_annotation(
        x=0,
        y=0,
        text="<b style='color:#FFF'>Atlas</b><br><span style='font-size:10px;color:#AEAEB2'>datasets</span>",
        showarrow=False,
        xref="x",
        yref="y",
    )

    pad = 1.65
    fig.update_layout(
        title=dict(
            text="<span style='color:#1D1D1F'>Benchmark map</span> · <span style='color:#86868B'>size ∝ linked models</span>",
            font=dict(size=16, family="system-ui, -apple-system, sans-serif"),
            x=0.5,
            xanchor="center",
        ),
        xaxis=dict(visible=False, range=[-pad, pad], fixedrange=True),
        yaxis=dict(visible=False, range=[-pad, pad], scaleanchor="x", scaleratio=1, fixedrange=True),
        plot_bgcolor="#E8E8ED",
        paper_bgcolor="#E8E8ED",
        height=600,
        margin=dict(l=24, r=24, t=56, b=24),
        font=dict(color="#1D1D1F"),
    )
    return fig
