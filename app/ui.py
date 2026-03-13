"""
Shared navigation, footer, and chrome for a consistent app shell.
"""
import streamlit as st

# Public repo (update if you fork)
REPO_URL = "https://github.com/VidithPhillips/radiology-benchmark-provenance-atlas"


def sidebar_shell(active: str = "home") -> None:
    """Branded sidebar; native page list stays above (search = filter pages)."""
    with st.sidebar:
        st.markdown("#### Provenance Atlas")
        st.caption("Open models linked to public radiology benchmarks")
        st.page_link("app.py", label="Home", icon="🗺️")
        st.page_link("pages/1_Dataset_Browser.py", label="Datasets", icon="📁")
        st.page_link("pages/2_Model_Browser.py", label="Models", icon="🤖")
        st.page_link("pages/4_Atlas_Graph.py", label="Atlas map", icon="🕸️")
        st.page_link("pages/3_About.py", label="About", icon="ℹ️")
        with st.expander("Quick start", expanded=False):
            st.markdown(
                "1. Home: benchmark + mind map  \n"
                "2. Quick view: MIMIC / CheXpert / high only  \n"
                "3. Green / orange / violet = confidence  \n"
                "4. Expand **Full edge table** for CSV detail"
            )
        st.divider()
        st.markdown(f"[Repository]({REPO_URL})")


def page_hero(title: str, lede: str) -> None:
    """Top of subpages: title + one line + home link."""
    st.markdown(f"[← Back to Home](app.py)")
    st.title(title)
    st.markdown(f"<p class='atlas-sub' style='margin-top:-0.5rem'>{lede}</p>", unsafe_allow_html=True)


def global_footer() -> None:
    st.divider()
    st.caption(
        f"Released CSVs in `data/release/` · [GitHub]({REPO_URL}) · "
        "Confidence colors: green high · orange medium · violet low"
    )
