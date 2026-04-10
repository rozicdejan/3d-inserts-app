import streamlit as st
import pandas as pd
import plotly.graph_objects as go
import plotly.express as px
import numpy as np

# ── Page config ───────────────────────────────────────────────────────────────
st.set_page_config(
    page_title="3D Print Insert Guide",
    page_icon="🔩",
    layout="wide",
    initial_sidebar_state="collapsed",
)

# ── Custom CSS ─────────────────────────────────────────────────────────────────
st.markdown("""
<style>
  @import url('https://fonts.googleapis.com/css2?family=Space+Mono:wght@400;700&family=DM+Sans:wght@400;500;600;700&family=DM+Serif+Display&display=swap');

  html, body, [class*="css"] {
    font-family: 'DM Sans', sans-serif;
  }

  /* Background */
  .stApp {
    background: #f4f6f9;
    background-image:
      radial-gradient(ellipse at 0% 0%, #deeeff 0%, transparent 55%),
      radial-gradient(ellipse at 100% 100%, #d6f5ec 0%, transparent 55%);
  }

  /* Remove default padding */
  .block-container { padding-top: 2rem; padding-bottom: 2rem; }

  /* Hero section */
  .hero-title {
    font-family: 'DM Serif Display', serif;
    font-weight: 400;
    font-size: 3rem;
    letter-spacing: -1px;
    background: linear-gradient(135deg, #1a5276 0%, #1a7a5e 100%);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    background-clip: text;
    line-height: 1.15;
    margin: 0;
  }
  .hero-sub {
    font-family: 'Space Mono', monospace;
    font-size: 0.75rem;
    color: #2e86ab;
    letter-spacing: 3px;
    text-transform: uppercase;
    margin-bottom: 0.5rem;
  }
  .hero-desc {
    color: #4a6274;
    font-size: 1rem;
    max-width: 600px;
    line-height: 1.65;
  }

  /* Stat cards */
  .stat-card {
    background: #ffffff;
    border: 1px solid #d0e4f0;
    border-radius: 14px;
    padding: 1.2rem 1.4rem;
    text-align: center;
    box-shadow: 0 2px 12px rgba(30,90,140,0.07);
  }
  .stat-value {
    font-family: 'Space Mono', monospace;
    font-size: 2rem;
    font-weight: 700;
    color: #0e8a6a;
  }
  .stat-label {
    font-size: 0.72rem;
    color: #7a98aa;
    letter-spacing: 2px;
    text-transform: uppercase;
    margin-top: 0.2rem;
  }

  /* Section headers */
  .section-header {
    font-family: 'DM Sans', sans-serif;
    font-weight: 700;
    font-size: 1.15rem;
    color: #1a3a4a;
    border-left: 3px solid #0e8a6a;
    padding-left: 0.8rem;
    margin: 1.5rem 0 1rem 0;
  }

  /* Size badge */
  .size-badge {
    display: inline-block;
    background: #eaf4ff;
    border: 1px solid #b0d4ee;
    border-radius: 8px;
    padding: 0.5rem 1rem;
    font-family: 'Space Mono', monospace;
    font-size: 0.9rem;
    color: #2e6ea6;
    cursor: pointer;
    transition: all 0.2s;
    margin: 0.3rem;
  }
  .size-badge:hover { border-color: #0e8a6a; color: #0e8a6a; }

  /* Info card */
  .info-card {
    background: #ffffff;
    border: 1px solid #d0e4f0;
    border-radius: 12px;
    padding: 1.5rem;
    margin: 0.8rem 0;
    box-shadow: 0 1px 6px rgba(0,0,0,0.05);
  }
  .info-card-highlight {
    background: linear-gradient(135deg, #edfaf4 0%, #eaf4ff 100%);
    border: 1px solid #b0e0cc;
    border-radius: 12px;
    padding: 1.5rem;
    margin: 0.8rem 0;
  }

  /* Metric display */
  .metric-big {
    font-family: 'Space Mono', monospace;
    font-size: 2.5rem;
    font-weight: 700;
    color: #0e8a6a;
  }
  .metric-unit {
    font-family: 'Space Mono', monospace;
    font-size: 1rem;
    color: #2eab8a;
  }
  .metric-label {
    font-size: 0.75rem;
    color: #7a98aa;
    letter-spacing: 2px;
    text-transform: uppercase;
  }

  /* Tip box */
  .tip-box {
    background: #edfaf4;
    border-left: 3px solid #0e8a6a;
    border-radius: 0 8px 8px 0;
    padding: 0.8rem 1rem;
    margin: 0.5rem 0;
    font-size: 0.88rem;
    color: #1a5240;
  }
  .tip-box strong { color: #0a6e54; }

  .warn-box {
    background: #fff8e6;
    border-left: 3px solid #d4960a;
    border-radius: 0 8px 8px 0;
    padding: 0.8rem 1rem;
    margin: 0.5rem 0;
    font-size: 0.88rem;
    color: #7a5010;
  }
  .warn-box strong { color: #b87e0a; }

  /* Tab styling */
  .stTabs [data-baseweb="tab-list"] {
    background: #ffffff;
    border-radius: 10px;
    padding: 4px;
    gap: 4px;
    border: 1px solid #d0e4f0;
    box-shadow: 0 1px 6px rgba(0,0,0,0.05);
  }
  .stTabs [data-baseweb="tab"] {
    background: transparent;
    color: #7a98aa;
    border-radius: 8px;
    font-family: 'Space Mono', monospace;
    font-size: 0.75rem;
    letter-spacing: 1px;
    padding: 0.5rem 1.2rem;
  }
  .stTabs [aria-selected="true"] {
    background: #e8f5f0 !important;
    color: #0e8a6a !important;
  }

  /* Dataframe */
  .dataframe-container {
    border-radius: 12px;
    overflow: hidden;
    border: 1px solid #d0e4f0;
  }

  /* Divider */
  .fancy-divider {
    height: 1px;
    background: linear-gradient(90deg, transparent, #b0d4ee, #0e8a6a, #b0d4ee, transparent);
    margin: 2rem 0;
    opacity: 0.5;
  }

  /* Selectbox */
  .stSelectbox > div > div {
    background: #ffffff !important;
    border-color: #c0d8ea !important;
    color: #1a3a4a !important;
    font-family: 'Space Mono', monospace !important;
  }

  /* Streamlit metric override */
  [data-testid="metric-container"] {
    background: #ffffff;
    border: 1px solid #d0e4f0;
    border-radius: 10px;
    padding: 1rem 1.2rem;
    box-shadow: 0 2px 8px rgba(30,90,140,0.06);
  }
  [data-testid="metric-container"] label {
    color: #7a98aa !important;
    font-family: 'Space Mono', monospace !important;
    font-size: 0.7rem !important;
    letter-spacing: 2px !important;
  }
  [data-testid="metric-container"] [data-testid="stMetricValue"] {
    color: #0e8a6a !important;
    font-family: 'Space Mono', monospace !important;
    font-size: 1.8rem !important;
  }

  /* Hide streamlit branding */
  #MainMenu, footer, header { visibility: hidden; }

  /* Slider */
  .stSlider [data-baseweb="slider"] { padding: 0.5rem 0; }

  /* Custom table */
  table.custom-table {
    width: 100%;
    border-collapse: collapse;
    font-family: 'Space Mono', monospace;
    font-size: 0.82rem;
  }
  table.custom-table th {
    background: #f0f7ff;
    color: #5a7a8a;
    text-transform: uppercase;
    letter-spacing: 2px;
    font-size: 0.7rem;
    padding: 0.8rem 1rem;
    text-align: left;
    border-bottom: 1px solid #d0e4f0;
  }
  table.custom-table td {
    padding: 0.7rem 1rem;
    border-bottom: 1px solid #eaf0f6;
    color: #1a3a4a;
  }
  table.custom-table tr:hover td { background: #f4faff; }
  table.custom-table td.highlight { color: #0e8a6a; font-weight: 700; }
  table.custom-table td.size-col { color: #2e6ea6; font-weight: 700; }
  table.custom-table tr.active-row td { background: #edfaf4 !important; }
  table.custom-table tr.active-row td.size-col { color: #0e8a6a; }
</style>
""", unsafe_allow_html=True)

# ── DATA ───────────────────────────────────────────────────────────────────────
# Source: CNC Kitchen, Accu-Components, utils.com thread-insert reference
insert_data = {
    "M2":   {"screw_d": 2.0, "insert_od": 3.2,  "insert_len_short": 3.0,  "insert_len_long": 3.0,  "hole_d_tight": 3.0, "hole_d_std": 3.2,  "hole_depth_add": 1.0, "min_wall": 6.4,  "solder_temp_pla": "200–210°C", "solder_temp_petg": "230–240°C"},
    "M2.5": {"screw_d": 2.5, "insert_od": 4.0,  "insert_len_short": 4.0,  "insert_len_long": 4.0,  "hole_d_tight": 3.8, "hole_d_std": 4.0,  "hole_depth_add": 1.0, "min_wall": 8.0,  "solder_temp_pla": "200–210°C", "solder_temp_petg": "230–240°C"},
    "M3":   {"screw_d": 3.0, "insert_od": 4.6,  "insert_len_short": 3.0,  "insert_len_long": 5.7,  "hole_d_tight": 4.0, "hole_d_std": 4.4,  "hole_depth_add": 1.0, "min_wall": 9.2,  "solder_temp_pla": "200–210°C", "solder_temp_petg": "230–240°C"},
    "M4":   {"screw_d": 4.0, "insert_od": 5.6,  "insert_len_short": 4.0,  "insert_len_long": 8.1,  "hole_d_tight": 5.4, "hole_d_std": 5.6,  "hole_depth_add": 1.0, "min_wall": 11.2, "solder_temp_pla": "200–210°C", "solder_temp_petg": "240–255°C"},
    "M5":   {"screw_d": 5.0, "insert_od": 6.4,  "insert_len_short": 5.8,  "insert_len_long": 9.5,  "hole_d_tight": 6.2, "hole_d_std": 6.4,  "hole_depth_add": 1.0, "min_wall": 12.8, "solder_temp_pla": "210–220°C", "solder_temp_petg": "245–260°C"},
    "M6":   {"screw_d": 6.0, "insert_od": 8.0,  "insert_len_short": 8.0,  "insert_len_long": 12.7, "hole_d_tight": 7.8, "hole_d_std": 8.0,  "hole_depth_add": 1.0, "min_wall": 16.0, "solder_temp_pla": "210–220°C", "solder_temp_petg": "245–260°C"},
    "M8":   {"screw_d": 8.0, "insert_od": 9.7,  "insert_len_short": 9.7,  "insert_len_long": 12.7, "hole_d_tight": 9.5, "hole_d_std": 9.7,  "hole_depth_add": 1.0, "min_wall": 19.4, "solder_temp_pla": "215–225°C", "solder_temp_petg": "250–265°C"},
    "M10":  {"screw_d": 10.0,"insert_od": 12.0, "insert_len_short": 10.0, "insert_len_long": 12.7, "hole_d_tight": 11.8,"hole_d_std": 12.0, "hole_depth_add": 1.0, "min_wall": 24.0, "solder_temp_pla": "215–225°C", "solder_temp_petg": "250–265°C"},
}

self_tap_data = {
    "M2":   {"pilot_pla": 1.6, "pilot_abs": 1.7, "pilot_petg": 1.6, "depth_mult": 2.0},
    "M2.5": {"pilot_pla": 2.0, "pilot_abs": 2.1, "pilot_petg": 2.0, "depth_mult": 2.0},
    "M3":   {"pilot_pla": 2.4, "pilot_abs": 2.6, "pilot_petg": 2.5, "depth_mult": 2.5},
    "M4":   {"pilot_pla": 3.3, "pilot_abs": 3.4, "pilot_petg": 3.3, "depth_mult": 2.5},
    "M5":   {"pilot_pla": 4.1, "pilot_abs": 4.3, "pilot_petg": 4.2, "depth_mult": 2.5},
    "M6":   {"pilot_pla": 5.0, "pilot_abs": 5.2, "pilot_petg": 5.1, "depth_mult": 3.0},
    "M8":   {"pilot_pla": 6.7, "pilot_abs": 6.9, "pilot_petg": 6.8, "depth_mult": 3.0},
    "M10":  {"pilot_pla": 8.3, "pilot_abs": 8.6, "pilot_petg": 8.4, "depth_mult": 3.0},
}

clearance_data = {
    "M2":   {"close": 2.2,  "normal": 2.4,  "free": 2.6},
    "M2.5": {"close": 2.7,  "normal": 2.9,  "free": 3.1},
    "M3":   {"close": 3.4,  "normal": 3.6,  "free": 3.8},
    "M4":   {"close": 4.5,  "normal": 4.8,  "free": 5.0},
    "M5":   {"close": 5.5,  "normal": 5.8,  "free": 6.1},
    "M6":   {"close": 6.6,  "normal": 7.0,  "free": 7.4},
    "M8":   {"close": 8.8,  "normal": 9.2,  "free": 9.6},
    "M10":  {"close": 11.0, "normal": 11.5, "free": 12.0},
}

SIZES = list(insert_data.keys())

# ── HERO ───────────────────────────────────────────────────────────────────────
col_hero, col_stats = st.columns([3, 2], gap="large")

with col_hero:
    st.markdown('<p class="hero-sub">🔩 Engineering Reference</p>', unsafe_allow_html=True)
    st.markdown('<h1 class="hero-title">3D Print Insert<br>Hole Calculator</h1>', unsafe_allow_html=True)
    st.markdown("""
    <p class="hero-desc">
      Precise hole diameter & depth recommendations for heat-set brass inserts,
      self-tapping screws, and clearance holes — M2 through M10.
      Based on CNC Kitchen, Accu-Components, and community testing data.
    </p>
    """, unsafe_allow_html=True)

with col_stats:
    s1, s2, s3 = st.columns(3)
    with s1:
        st.markdown('<div class="stat-card"><div class="stat-value">8</div><div class="stat-label">Metric Sizes</div></div>', unsafe_allow_html=True)
    with s2:
        st.markdown('<div class="stat-card"><div class="stat-value">3</div><div class="stat-label">Insert Types</div></div>', unsafe_allow_html=True)
    with s3:
        st.markdown('<div class="stat-card"><div class="stat-value">M2–M10</div><div class="stat-label">Range</div></div>', unsafe_allow_html=True)

st.markdown('<div class="fancy-divider"></div>', unsafe_allow_html=True)

# ── TABS ───────────────────────────────────────────────────────────────────────
tab1, tab2, tab3, tab4, tab5 = st.tabs([
    "🔥 HEAT-SET INSERTS",
    "⚙️ SELF-TAPPING SCREWS",
    "⭕ CLEARANCE HOLES",
    "📊 VISUAL COMPARISON",
    "🏗️ BOSS & PULL-OUT",
])

# ─────────────────────────────────────────────────────────────────────────────
# TAB 1 — HEAT-SET INSERTS
# ─────────────────────────────────────────────────────────────────────────────
with tab1:
    st.markdown("")
    left, right = st.columns([1, 2], gap="large")

    with left:
        st.markdown('<div class="section-header">Select Thread Size</div>', unsafe_allow_html=True)
        selected = st.selectbox("Thread size", SIZES, index=2, label_visibility="collapsed")
        d = insert_data[selected]

        st.markdown('<div class="section-header">Material</div>', unsafe_allow_html=True)
        material = st.radio("Material", ["PLA", "PETG / ABS", "ASA / PC"], label_visibility="collapsed")

        st.markdown('<div class="section-header">Insert Length</div>', unsafe_allow_html=True)
        if d["insert_len_short"] == d["insert_len_long"]:
            ins_len = d["insert_len_short"]
            st.markdown(f'<div class="info-card"><span style="font-family:Space Mono;color:#7ab8f5">{ins_len} mm</span> <span style="color:#4a7c9e;font-size:0.8rem">(standard)</span></div>', unsafe_allow_html=True)
        else:
            ins_len = st.slider("Insert length (mm)", min_value=d["insert_len_short"],
                                max_value=d["insert_len_long"],
                                value=d["insert_len_short"], step=0.1,
                                label_visibility="collapsed")

    with right:
        st.markdown('<div class="section-header">Recommended Dimensions</div>', unsafe_allow_html=True)

        hole_depth = round(ins_len + d["hole_depth_add"] + 0.5, 1)
        if material == "PLA":
            hole_d = d["hole_d_tight"]
            temp = d["solder_temp_pla"]
        elif material == "PETG / ABS":
            hole_d = round((d["hole_d_tight"] + d["hole_d_std"]) / 2, 1)
            temp = d["solder_temp_petg"]
        else:
            hole_d = d["hole_d_std"]
            temp = d["solder_temp_petg"]

        m1, m2, m3, m4 = st.columns(4)
        m1.metric("Hole Ø", f"{hole_d} mm")
        m2.metric("Hole Depth", f"{hole_depth} mm")
        m3.metric("Insert OD", f"{d['insert_od']} mm")
        m4.metric("Min Wall", f"{d['min_wall']} mm")

        st.markdown("")

        # Cross-section diagram
        fig = go.Figure()
        wall_w = d["min_wall"] / 2
        total_w = d["insert_od"] / 2 + wall_w
        total_h = hole_depth + 3

        # Outer body
        fig.add_shape(type="rect", x0=-total_w, y0=0, x1=total_w, y1=total_h,
                      fillcolor="#f0f7ff", line=dict(color="#c0d8ea", width=1.5))
        # Hole cavity
        fig.add_shape(type="rect", x0=-hole_d/2, y0=0, x1=hole_d/2, y1=hole_depth,
                      fillcolor="#e8f0fa", line=dict(color="#2e86c1", width=1.5))
        # Insert body
        fig.add_shape(type="rect", x0=-d["insert_od"]/2, y0=0.2,
                      x1=d["insert_od"]/2, y1=ins_len+0.2,
                      fillcolor="#b8e8d0", line=dict(color="#0e8a6a", width=2))
        # Screw hole inside insert
        fig.add_shape(type="rect", x0=-d["screw_d"]/2, y0=0.2,
                      x1=d["screw_d"]/2, y1=ins_len+0.2,
                      fillcolor="#e8f0fa", line=dict(color="#2a8060", width=1))
        # Knurling lines
        for y in np.linspace(0.8, ins_len - 0.5, 5):
            fig.add_shape(type="line", x0=-d["insert_od"]/2, y0=y,
                          x1=-d["insert_od"]/2 + 0.4, y1=y,
                          line=dict(color="#0e8a6a", width=1))
            fig.add_shape(type="line", x0=d["insert_od"]/2, y0=y,
                          x1=d["insert_od"]/2 - 0.4, y1=y,
                          line=dict(color="#0e8a6a", width=1))

        # Dimension arrows / annotations
        fig.add_annotation(x=0, y=-0.8, text=f"⌀ {hole_d} mm",
                           font=dict(color="#2e86c1", size=11, family="Space Mono"),
                           showarrow=False)
        fig.add_annotation(x=total_w + 1.2, y=hole_depth/2,
                           text=f"{hole_depth} mm depth",
                           font=dict(color="#5a8aaa", size=10, family="Space Mono"),
                           showarrow=False, textangle=-90)

        fig.update_layout(
            title=dict(text=f"{selected} Insert — Cross Section",
                       font=dict(color="#1a3a4a", size=14, family="Syne"), x=0.5),
            paper_bgcolor="#f8fbff", plot_bgcolor="#f8fbff",
            xaxis=dict(range=[-total_w-2, total_w+4], showgrid=False,
                       zeroline=False, showticklabels=False),
            yaxis=dict(range=[-2, total_h+1], showgrid=False,
                       zeroline=False, showticklabels=False),
            height=320,
            margin=dict(l=10, r=40, t=40, b=20),
        )
        st.plotly_chart(fig, use_container_width=True)

        # Tips
        st.markdown(f"""
        <div class="tip-box">
          <strong>💡 Soldering Iron Temperature:</strong> {temp} for {material}
        </div>
        <div class="tip-box">
          <strong>💡 Chamfer:</strong> Add a 0.5 mm 45° chamfer at the hole opening to guide the insert.
        </div>
        <div class="warn-box">
          <strong>⚠️ Always test-print</strong> a sample with multiple hole sizes (±0.1 mm steps) before production — printer tolerances vary.
        </div>
        """, unsafe_allow_html=True)

    # Full reference table
    st.markdown('<div class="fancy-divider"></div>', unsafe_allow_html=True)
    st.markdown('<div class="section-header">Complete Reference Table — Heat-Set Inserts</div>', unsafe_allow_html=True)

    rows = []
    for sz in SIZES:
        dd = insert_data[sz]
        rows.append({
            "Size": sz,
            "Screw Ø (mm)": dd["screw_d"],
            "Insert OD (mm)": dd["insert_od"],
            "Insert Length (mm)": f'{dd["insert_len_short"]}–{dd["insert_len_long"]}' if dd["insert_len_short"] != dd["insert_len_long"] else str(dd["insert_len_short"]),
            "Hole Ø PLA (mm)": dd["hole_d_tight"],
            "Hole Ø PETG/ABS (mm)": round((dd["hole_d_tight"] + dd["hole_d_std"]) / 2, 1),
            "Hole Ø ASA/PC (mm)": dd["hole_d_std"],
            "Min Wall (mm)": dd["min_wall"],
        })
    df = pd.DataFrame(rows)

    # Highlight selected row
    def highlight_row(row):
        if row["Size"] == selected:
            return ["background-color: #edfaf4; color: #0a6e54"] * len(row)
        return [""] * len(row)

    styled = df.style.apply(highlight_row, axis=1).format({
        "Screw Ø (mm)": "{:.1f}",
        "Insert OD (mm)": "{:.1f}",
        "Hole Ø PLA (mm)": "{:.1f}",
        "Hole Ø PETG/ABS (mm)": "{:.1f}",
        "Hole Ø ASA/PC (mm)": "{:.1f}",
        "Min Wall (mm)": "{:.1f}",
    }).set_properties(**{
        "background-color": "#0a1420",
        "color": "#c8dff0",
        "border-color": "#1e3048",
        "font-family": "Space Mono, monospace",
        "font-size": "0.82rem",
    }).set_table_styles([
        {"selector": "th", "props": [
            ("background-color", "#0d1b2a"), ("color", "#4a7c9e"),
            ("font-family", "Space Mono, monospace"), ("font-size", "0.72rem"),
            ("text-transform", "uppercase"), ("letter-spacing", "1px"),
            ("border-color", "#1e3a55"),
        ]},
    ])

    st.dataframe(df.style.apply(highlight_row, axis=1), use_container_width=True, hide_index=True)


# ─────────────────────────────────────────────────────────────────────────────
# TAB 2 — SELF-TAPPING SCREWS
# ─────────────────────────────────────────────────────────────────────────────
with tab2:
    st.markdown("")
    left2, right2 = st.columns([1, 2], gap="large")

    with left2:
        st.markdown('<div class="section-header">Select Thread Size</div>', unsafe_allow_html=True)
        sel2 = st.selectbox("Thread size ST", SIZES, index=2, label_visibility="collapsed", key="st_sel")
        st_d = self_tap_data[sel2]

        st.markdown('<div class="section-header">Material</div>', unsafe_allow_html=True)
        mat2 = st.radio("Material ST", ["PLA", "PETG", "ABS"], label_visibility="collapsed", key="st_mat")

    with right2:
        st.markdown('<div class="section-header">Recommended Pilot Hole</div>', unsafe_allow_html=True)

        if mat2 == "PLA":
            pilot = st_d["pilot_pla"]
        elif mat2 == "PETG":
            pilot = st_d["pilot_petg"]
        else:
            pilot = st_d["pilot_abs"]

        screw_d2 = insert_data[sel2]["screw_d"]
        min_depth = round(screw_d2 * st_d["depth_mult"], 1)

        m1, m2, m3 = st.columns(3)
        m1.metric("Pilot Hole Ø", f"{pilot} mm")
        m2.metric("Min Depth", f"{min_depth} mm")
        m3.metric("% of Screw Ø", f"{round(pilot/screw_d2*100)}%")

        st.markdown(f"""
        <div class="tip-box">
          <strong>💡 Rule of thumb:</strong> Pilot hole = 75–85% of screw outer diameter. Tighter for soft materials (PLA), looser for harder ones (ABS).
        </div>
        <div class="tip-box">
          <strong>💡 Thread engagement:</strong> Aim for at least {int(st_d["depth_mult"])}× screw diameter of depth for reliable pull-out strength.
        </div>
        <div class="warn-box">
          <strong>⚠️ Self-tapping degrades</strong> after 3–5 insertion cycles. Use heat-set inserts for frequently disassembled parts.
        </div>
        """, unsafe_allow_html=True)

    st.markdown('<div class="fancy-divider"></div>', unsafe_allow_html=True)
    st.markdown('<div class="section-header">Complete Reference Table — Self-Tapping Screws</div>', unsafe_allow_html=True)

    st_rows = []
    for sz in SIZES:
        sd = self_tap_data[sz]
        id_ = insert_data[sz]
        st_rows.append({
            "Size": sz,
            "Screw Ø (mm)": id_["screw_d"],
            "Pilot — PLA (mm)": sd["pilot_pla"],
            "Pilot — PETG (mm)": sd["pilot_petg"],
            "Pilot — ABS (mm)": sd["pilot_abs"],
            "Min Depth (mm)": round(id_["screw_d"] * sd["depth_mult"], 1),
        })
    df2 = pd.DataFrame(st_rows)

    def hl2(row):
        if row["Size"] == sel2:
            return ["background-color: #edfaf4; color: #0a6e54"] * len(row)
        return [""] * len(row)

    st.dataframe(df2.style.apply(hl2, axis=1), use_container_width=True, hide_index=True)


# ─────────────────────────────────────────────────────────────────────────────
# TAB 3 — CLEARANCE HOLES
# ─────────────────────────────────────────────────────────────────────────────
with tab3:
    st.markdown("")
    left3, right3 = st.columns([1, 2], gap="large")

    with left3:
        st.markdown('<div class="section-header">Select Thread Size</div>', unsafe_allow_html=True)
        sel3 = st.selectbox("Thread CL", SIZES, index=2, label_visibility="collapsed", key="cl_sel")
        cl_d = clearance_data[sel3]

        st.markdown('<div class="section-header">Fit Type</div>', unsafe_allow_html=True)
        fit = st.radio("Fit", ["Close Fit", "Normal Fit", "Free Fit"], label_visibility="collapsed", key="cl_fit")

    with right3:
        st.markdown('<div class="section-header">Recommended Clearance Hole</div>', unsafe_allow_html=True)

        if fit == "Close Fit":
            cl_val = cl_d["close"]
            fit_desc = "Tight — minimal play, good for alignment"
        elif fit == "Normal Fit":
            cl_val = cl_d["normal"]
            fit_desc = "Standard — easy assembly, slight play"
        else:
            cl_val = cl_d["free"]
            fit_desc = "Loose — easy assembly, more tolerance"

        screw_d3 = insert_data[sel3]["screw_d"]
        oversize = round((cl_val - screw_d3) * 1000) / 1000

        m1, m2, m3 = st.columns(3)
        m1.metric("Clearance Hole Ø", f"{cl_val} mm")
        m2.metric("Oversize vs Screw", f"+{oversize:.2f} mm")
        m3.metric("Fit Type", fit.split()[0])

        st.markdown(f"""
        <div class="tip-box">
          <strong>📐 {fit}:</strong> {fit_desc}
        </div>
        <div class="tip-box">
          <strong>💡 FDM compensation:</strong> Values include +0.2–0.4 mm to account for typical FDM hole shrinkage from thermal effects and nozzle path rounding.
        </div>
        """, unsafe_allow_html=True)

    st.markdown('<div class="fancy-divider"></div>', unsafe_allow_html=True)
    st.markdown('<div class="section-header">Complete Reference Table — Clearance Holes</div>', unsafe_allow_html=True)

    cl_rows = []
    for sz in SIZES:
        cd = clearance_data[sz]
        id_ = insert_data[sz]
        cl_rows.append({
            "Size": sz,
            "Screw Ø (mm)": id_["screw_d"],
            "Close Fit (mm)": cd["close"],
            "Normal Fit (mm)": cd["normal"],
            "Free Fit (mm)": cd["free"],
        })
    df3 = pd.DataFrame(cl_rows)

    def hl3(row):
        if row["Size"] == sel3:
            return ["background-color: #edfaf4; color: #0a6e54"] * len(row)
        return [""] * len(row)

    st.dataframe(df3.style.apply(hl3, axis=1), use_container_width=True, hide_index=True)


# ─────────────────────────────────────────────────────────────────────────────
# TAB 4 — VISUAL COMPARISON
# ─────────────────────────────────────────────────────────────────────────────
with tab4:
    st.markdown("")

    col4a, col4b = st.columns(2, gap="large")

    with col4a:
        st.markdown('<div class="section-header">Hole Diameter by Size</div>', unsafe_allow_html=True)

        sizes_list = SIZES
        screw_d_list = [insert_data[s]["screw_d"] for s in sizes_list]
        hole_pla = [insert_data[s]["hole_d_tight"] for s in sizes_list]
        hole_petg = [round((insert_data[s]["hole_d_tight"] + insert_data[s]["hole_d_std"]) / 2, 1) for s in sizes_list]
        hole_asa = [insert_data[s]["hole_d_std"] for s in sizes_list]
        insert_od_list = [insert_data[s]["insert_od"] for s in sizes_list]
        cl_normal = [clearance_data[s]["normal"] for s in sizes_list]

        fig2 = go.Figure()
        fig2.add_trace(go.Bar(name="Insert OD", x=sizes_list, y=insert_od_list,
                              marker_color="#a8c8e8", marker_line_color="#6a9ac0",
                              marker_line_width=1))
        fig2.add_trace(go.Scatter(name="Hole Ø PLA", x=sizes_list, y=hole_pla,
                                  mode="lines+markers", line=dict(color="#0e8a6a", width=2.5),
                                  marker=dict(size=8, symbol="circle")))
        fig2.add_trace(go.Scatter(name="Hole Ø PETG", x=sizes_list, y=hole_petg,
                                  mode="lines+markers", line=dict(color="#2e86c1", width=2, dash="dot"),
                                  marker=dict(size=7)))
        fig2.add_trace(go.Scatter(name="Hole Ø ASA/PC", x=sizes_list, y=hole_asa,
                                  mode="lines+markers", line=dict(color="#d4960a", width=2, dash="dash"),
                                  marker=dict(size=7)))
        fig2.update_layout(
            paper_bgcolor="#f8fbff", plot_bgcolor="#ffffff",
            font=dict(family="Space Mono, monospace", color="#4a6274", size=11),
            legend=dict(bgcolor="#ffffff", bordercolor="#d0e4f0", borderwidth=1),
            xaxis=dict(gridcolor="#e0ecf4", title="Thread Size"),
            yaxis=dict(gridcolor="#e0ecf4", title="Diameter (mm)"),
            height=350, margin=dict(l=10, r=10, t=20, b=10),
            barmode="overlay",
        )
        st.plotly_chart(fig2, use_container_width=True)

    with col4b:
        st.markdown('<div class="section-header">Hole Sizes Side-by-Side</div>', unsafe_allow_html=True)

        fig3 = go.Figure()
        fig3.add_trace(go.Scatter(name="Screw Ø", x=screw_d_list, y=screw_d_list,
                                  mode="lines+markers", line=dict(color="#5a8aaa", width=1.5, dash="dot"),
                                  marker=dict(size=6)))
        fig3.add_trace(go.Scatter(name="Insert OD", x=screw_d_list, y=insert_od_list,
                                  mode="lines+markers", line=dict(color="#1e5a9e", width=2),
                                  marker=dict(size=8, symbol="diamond")))
        fig3.add_trace(go.Scatter(name="Hole Ø (PLA)", x=screw_d_list, y=hole_pla,
                                  mode="lines+markers", line=dict(color="#0e8a6a", width=2.5),
                                  marker=dict(size=9, symbol="circle")))
        fig3.add_trace(go.Scatter(name="Clearance (Normal)", x=screw_d_list, y=cl_normal,
                                  mode="lines+markers", line=dict(color="#d4960a", width=2, dash="dash"),
                                  marker=dict(size=7, symbol="square")))
        fig3.update_layout(
            paper_bgcolor="#f8fbff", plot_bgcolor="#ffffff",
            font=dict(family="Space Mono, monospace", color="#4a6274", size=11),
            legend=dict(bgcolor="#ffffff", bordercolor="#d0e4f0", borderwidth=1),
            xaxis=dict(gridcolor="#e0ecf4", title="Screw Diameter (mm)"),
            yaxis=dict(gridcolor="#e0ecf4", title="Diameter (mm)"),
            height=350, margin=dict(l=10, r=10, t=20, b=10),
        )
        st.plotly_chart(fig3, use_container_width=True)

    # Grouped bar — all hole types
    st.markdown('<div class="section-header">All Hole Types Comparison</div>', unsafe_allow_html=True)

    fig4 = go.Figure()
    fig4.add_trace(go.Bar(name="Screw Ø", x=sizes_list, y=screw_d_list,
                          marker_color="#4a7aaa"))
    fig4.add_trace(go.Bar(name="Heat-Set Hole (PLA)", x=sizes_list, y=hole_pla,
                          marker_color="#a0dcc0"))
    fig4.add_trace(go.Bar(name="Insert Outer Ø", x=sizes_list, y=insert_od_list,
                          marker_color="#a8c8e8"))
    fig4.add_trace(go.Bar(name="Self-Tap Pilot (PLA)", x=sizes_list,
                          y=[self_tap_data[s]["pilot_pla"] for s in sizes_list],
                          marker_color="#f5d8a0"))
    fig4.add_trace(go.Bar(name="Clearance (Normal)", x=sizes_list, y=cl_normal,
                          marker_color="#f0c898"))
    fig4.update_layout(
        paper_bgcolor="#f8fbff", plot_bgcolor="#ffffff",
        font=dict(family="Space Mono, monospace", color="#4a6274", size=11),
        legend=dict(bgcolor="#ffffff", bordercolor="#d0e4f0", borderwidth=1,
                    orientation="h", y=-0.18),
        xaxis=dict(gridcolor="#e0ecf4"),
        yaxis=dict(gridcolor="#e0ecf4", title="Diameter (mm)"),
        barmode="group",
        height=380, margin=dict(l=10, r=10, t=20, b=60),
    )
    st.plotly_chart(fig4, use_container_width=True)

# ─────────────────────────────────────────────────────────────────────────────
# TAB 5 — BOSS DIAMETER & PULL-OUT FORCE & FLASH/WALL
# ─────────────────────────────────────────────────────────────────────────────
with tab5:
    st.markdown("")

    # ── Pull-out force base data (N) per insert size per material at standard length
    # Sources: CNC Kitchen pull-out tests, Markforged data, community benchmarks
    # Values represent average pull-out force for standard-length insert, well-installed
    pullout_base = {
        #          PLA    PETG   ABS    ASA    PC
        "M2":   [  90,   120,   110,   115,   160],
        "M2.5": [ 130,   175,   155,   165,   220],
        "M3":   [ 200,   280,   250,   265,   360],
        "M4":   [ 380,   530,   470,   500,   680],
        "M5":   [ 580,   800,   710,   755,  1020],
        "M6":   [ 850,  1180,  1050,  1110,  1500],
        "M8":   [1300,  1800,  1600,  1700,  2300],
        "M10":  [1900,  2650,  2350,  2480,  3350],
    }
    materials_po = ["PLA", "PETG", "ABS", "ASA", "PC"]
    mat_colors   = ["#38d9a9", "#7ab8f5", "#e8a820", "#e07060", "#b07af5"]

    # ── Flash / wall recommendations
    # Rule: min wall = insert_od * 1.5 (functional), insert_od * 2.0 (recommended), insert_od * 2.5 (optimal)
    # Top flash (material above hole bottom): min 0.8 mm, recommended 1.5 mm
    # Bottom flash (below insert tip): min 0.5 mm, recommended 1.0 mm

    # ── SECTION 1: Boss Diameter Calculator ──────────────────────────────────
    st.markdown('<div class="section-header">🏛️ Boss Diameter Calculator</div>', unsafe_allow_html=True)
    bc1, bc2 = st.columns([1, 2], gap="large")

    with bc1:
        st.markdown('<div class="section-header">Inputs</div>', unsafe_allow_html=True)
        b_size = st.selectbox("Thread size", SIZES, index=2, key="boss_size")
        b_mode = st.radio("Design goal", ["Functional (minimum)", "Recommended", "Optimal (max strength)"],
                          label_visibility="collapsed", key="boss_mode")
        b_wall_custom = st.checkbox("Override wall thickness", key="boss_custom")
        if b_wall_custom:
            b_wall_manual = st.slider("Wall thickness (mm)", 0.5, 8.0, 2.0, 0.1, key="boss_wall_slider")

    with bc2:
        bd = insert_data[b_size]
        ins_od = bd["insert_od"]

        # Wall thickness per mode
        if b_mode == "Functional (minimum)":
            wall_t = ins_od * 0.75
            wall_label = "1.5× insert OD — bare minimum, risk of cracking"
            wall_color = "#e87050"
            wall_icon = "⚠️"
        elif b_mode == "Recommended":
            wall_t = ins_od * 1.0
            wall_label = "2.0× insert OD — solid, reliable for most use cases"
            wall_color = "#38d9a9"
            wall_icon = "✅"
        else:
            wall_t = ins_od * 1.25
            wall_label = "2.5× insert OD — high-cycle or structural applications"
            wall_color = "#7ab8f5"
            wall_icon = "🏆"

        if b_wall_custom:
            wall_t = b_wall_manual

        boss_od = ins_od + 2 * wall_t
        boss_od = round(boss_od, 2)
        wall_t  = round(wall_t, 2)

        m1, m2, m3, m4 = st.columns(4)
        m1.metric("Boss Outer Ø", f"{boss_od} mm")
        m2.metric("Wall Thickness", f"{wall_t} mm")
        m3.metric("Insert OD", f"{ins_od} mm")
        m4.metric("Hole Ø", f"{bd['hole_d_tight']} mm")

        # Boss cross-section diagram
        fig_boss = go.Figure()
        cx, cy = 0, 0
        # Outer boss circle
        theta = np.linspace(0, 2*np.pi, 200)
        fig_boss.add_trace(go.Scatter(
            x=np.cos(theta) * boss_od/2, y=np.sin(theta) * boss_od/2,
            fill="toself", fillcolor="#f0f7ff",
            line=dict(color="#c0d8ea", width=2), showlegend=False, hoverinfo="skip"
        ))
        # Insert OD
        fig_boss.add_trace(go.Scatter(
            x=np.cos(theta) * ins_od/2, y=np.sin(theta) * ins_od/2,
            fill="toself", fillcolor="#d6f5e8",
            line=dict(color="#0e8a6a", width=2), showlegend=False, hoverinfo="skip",
            name="Insert OD"
        ))
        # Hole
        hole_r = bd['hole_d_tight'] / 2
        fig_boss.add_trace(go.Scatter(
            x=np.cos(theta) * hole_r, y=np.sin(theta) * hole_r,
            fill="toself", fillcolor="#e8f0fa",
            line=dict(color="#2e86c1", width=1.5), showlegend=False, hoverinfo="skip"
        ))
        # Screw hole
        screw_r = bd['screw_d'] / 2
        fig_boss.add_trace(go.Scatter(
            x=np.cos(theta) * screw_r, y=np.sin(theta) * screw_r,
            fill="toself", fillcolor="#f0f4ff",
            line=dict(color="#1a8a60", width=1), showlegend=False, hoverinfo="skip"
        ))
        # Dimension lines
        fig_boss.add_annotation(x=boss_od/2 + 0.8, y=0,
            text=f"⌀{boss_od}", font=dict(color="#1a3a4a", size=11, family="Space Mono"),
            showarrow=False)
        fig_boss.add_annotation(x=ins_od/2 * 0.7, y=-ins_od/2 * 0.7,
            text=f"⌀{ins_od}", font=dict(color="#0e8a6a", size=10, family="Space Mono"),
            showarrow=False)
        fig_boss.add_annotation(x=0, y=0,
            text=f"⌀{bd['hole_d_tight']}", font=dict(color="#2e86c1", size=9, family="Space Mono"),
            showarrow=False)
        # Wall arrows
        r_mid = (ins_od/2 + boss_od/2) / 2
        fig_boss.add_annotation(x=r_mid, y=0.3,
            text=f"{wall_t}mm wall", font=dict(color=wall_color, size=10, family="Space Mono"),
            showarrow=False)

        lim = boss_od/2 + 2.5
        fig_boss.update_layout(
            paper_bgcolor="#f8fbff", plot_bgcolor="#f8fbff",
            xaxis=dict(range=[-lim, lim+2.5], showgrid=False, zeroline=False, showticklabels=False,
                       scaleanchor="y", scaleratio=1),
            yaxis=dict(range=[-lim, lim], showgrid=False, zeroline=False, showticklabels=False),
            title=dict(text=f"{b_size} Boss — Top View", font=dict(color="#1a3a4a", size=13, family="Syne"), x=0.5),
            height=300, margin=dict(l=10, r=10, t=40, b=10),
        )
        st.plotly_chart(fig_boss, use_container_width=True)

        st.markdown(f"""
        <div class="tip-box" style="border-color:{wall_color}">
          <strong>{wall_icon} {b_mode}:</strong> {wall_label}
        </div>
        """, unsafe_allow_html=True)

    # Boss reference table
    st.markdown('<div class="fancy-divider"></div>', unsafe_allow_html=True)
    st.markdown('<div class="section-header">Boss Dimensions Reference Table</div>', unsafe_allow_html=True)

    boss_rows = []
    for sz in SIZES:
        dd = insert_data[sz]
        oid = dd["insert_od"]
        boss_rows.append({
            "Size": sz,
            "Insert OD (mm)": oid,
            "Boss Ø — Functional (mm)": round(oid + 2 * oid * 0.75, 1),
            "Boss Ø — Recommended (mm)": round(oid + 2 * oid * 1.0, 1),
            "Boss Ø — Optimal (mm)": round(oid + 2 * oid * 1.25, 1),
            "Wall — Min (mm)": round(oid * 0.75, 1),
            "Wall — Rec (mm)": round(oid * 1.0, 1),
            "Wall — Opt (mm)": round(oid * 1.25, 1),
        })
    df_boss = pd.DataFrame(boss_rows)

    def hl_boss(row):
        if row["Size"] == b_size:
            return ["background-color: #edfaf4; color: #0a6e54"] * len(row)
        return [""] * len(row)

    st.dataframe(df_boss.style.apply(hl_boss, axis=1), use_container_width=True, hide_index=True)

    # ── SECTION 2: Flash / Material Around Insert ─────────────────────────────
    st.markdown('<div class="fancy-divider"></div>', unsafe_allow_html=True)
    st.markdown('<div class="section-header">💧 Flash & Material Zones Around Insert</div>', unsafe_allow_html=True)

    fl1, fl2 = st.columns([1, 2], gap="large")

    with fl1:
        f_size = st.selectbox("Thread size", SIZES, index=2, key="flash_size")
        f_ins_len = st.slider("Insert length (mm)",
                              min_value=insert_data[f_size]["insert_len_short"],
                              max_value=insert_data[f_size]["insert_len_long"] + 2.0,
                              value=insert_data[f_size]["insert_len_short"],
                              step=0.5, key="flash_len")
        f_mat = st.radio("Material", ["PLA", "PETG", "ABS", "PC"], key="flash_mat",
                         label_visibility="collapsed")

    with fl2:
        fd = insert_data[f_size]

        # Flash zones
        top_flash_min = 0.8    # mm material above insert top
        top_flash_rec = 1.5
        bot_flash_min = 0.5    # mm below hole bottom
        bot_flash_rec = 1.0
        side_flash_min = round(fd["insert_od"] * 0.75, 1)
        side_flash_rec = round(fd["insert_od"] * 1.0,  1)

        total_hole_depth_min = f_ins_len + bot_flash_min
        total_hole_depth_rec = f_ins_len + bot_flash_rec
        part_height_min      = total_hole_depth_min + top_flash_min
        part_height_rec      = total_hole_depth_rec + top_flash_rec

        m1, m2, m3 = st.columns(3)
        m1.metric("Top Flash (rec)", f"{top_flash_rec} mm")
        m2.metric("Bottom Flash (rec)", f"{bot_flash_rec} mm")
        m3.metric("Side Wall (rec)", f"{side_flash_rec} mm")

        r1, r2, r3 = st.columns(3)
        r1.metric("Min Part Height", f"{round(part_height_min,1)} mm")
        r2.metric("Rec Part Height", f"{round(part_height_rec,1)} mm")
        r3.metric("Hole Depth (rec)", f"{round(total_hole_depth_rec,1)} mm")

        # Side cross-section diagram with zones
        fig_flash = go.Figure()
        iod = fd["insert_od"]
        hd  = fd["hole_d_tight"]
        wt  = side_flash_rec
        total_w = iod/2 + wt
        ph = part_height_rec

        # Part body
        fig_flash.add_shape(type="rect", x0=-total_w, y0=0, x1=total_w, y1=ph,
                            fillcolor="#f0f7ff", line=dict(color="#c0d8ea", width=1.5))
        # Side flash zone (left)
        fig_flash.add_shape(type="rect", x0=-total_w, y0=0, x1=-iod/2, y1=ph,
                            fillcolor="rgba(14,138,106,0.06)", line=dict(color="#b8e8d0", width=0))
        # Side flash zone (right)
        fig_flash.add_shape(type="rect", x0=iod/2, y0=0, x1=total_w, y1=ph,
                            fillcolor="rgba(14,138,106,0.06)", line=dict(color="#b8e8d0", width=0))
        # Hole cavity
        fig_flash.add_shape(type="rect", x0=-hd/2, y0=top_flash_rec, x1=hd/2, y1=ph,
                            fillcolor="#e8f0fa", line=dict(color="#2e86c1", width=1.5))
        # Insert
        fig_flash.add_shape(type="rect", x0=-iod/2, y0=top_flash_rec,
                            x1=iod/2, y1=top_flash_rec + f_ins_len,
                            fillcolor="#b8e8d0", line=dict(color="#0e8a6a", width=2))
        # Screw thread inside
        fig_flash.add_shape(type="rect", x0=-fd["screw_d"]/2, y0=top_flash_rec,
                            x1=fd["screw_d"]/2, y1=top_flash_rec + f_ins_len,
                            fillcolor="#e8eeff", line=dict(color="#1a9070", width=1))
        # Top flash zone
        fig_flash.add_shape(type="rect", x0=-total_w, y0=0, x1=total_w, y1=top_flash_rec,
                            fillcolor="rgba(46,134,193,0.08)", line=dict(color="#1a3a5c", width=0))
        # Bottom flash zone
        fig_flash.add_shape(type="rect", x0=-hd/2, y0=top_flash_rec,
                            x1=hd/2, y1=top_flash_rec + bot_flash_rec,
                            fillcolor="rgba(212,150,10,0.1)", line=dict(color="#3a2a00", width=0))

        # Annotations
        fig_flash.add_annotation(x=total_w+0.8, y=top_flash_rec/2,
            text=f"top\n{top_flash_rec}mm", font=dict(color="#2e86c1", size=9, family="Space Mono"),
            showarrow=False)
        fig_flash.add_annotation(x=-total_w-0.8, y=(ph - top_flash_rec)/2 + top_flash_rec,
            text=f"side\n{side_flash_rec}mm", font=dict(color="#0e8a6a", size=9, family="Space Mono"),
            showarrow=False, textangle=90)
        fig_flash.add_annotation(x=iod/2 + 0.5, y=top_flash_rec + bot_flash_rec/2,
            text=f"bot {bot_flash_rec}mm", font=dict(color="#d4960a", size=9, family="Space Mono"),
            showarrow=False)
        fig_flash.add_annotation(x=0, y=top_flash_rec + f_ins_len/2,
            text=f"{f_size}\n{f_ins_len}mm", font=dict(color="#0e8a6a", size=10, family="Space Mono"),
            showarrow=False)

        lim_x = total_w + 3
        fig_flash.update_layout(
            paper_bgcolor="#f8fbff", plot_bgcolor="#f8fbff",
            xaxis=dict(range=[-lim_x, lim_x], showgrid=False, zeroline=False, showticklabels=False),
            yaxis=dict(range=[-1, ph + 1.5], showgrid=False, zeroline=False, showticklabels=False),
            title=dict(text=f"{f_size} Flash Zones — Side View",
                       font=dict(color="#1a3a4a", size=13, family="Syne"), x=0.5),
            height=340, margin=dict(l=10, r=10, t=40, b=10),
        )
        st.plotly_chart(fig_flash, use_container_width=True)

        st.markdown("""
        <div class="tip-box"><strong>🟦 Top Flash (blue):</strong> Material above the insert top — prevents insert blowout under axial load. Min 0.8 mm, recommended 1.5 mm.</div>
        <div class="tip-box"><strong>🟩 Side Flash (green):</strong> Wall around the boss — resists torque-out. Min 1.5× insert OD, recommended 2×.</div>
        <div class="tip-box"><strong>🟨 Bottom Flash (amber):</strong> Space below the insert tip for displaced melt. Min 0.5 mm, recommended 1.0 mm.</div>
        """, unsafe_allow_html=True)

    # Flash reference table
    st.markdown('<div class="fancy-divider"></div>', unsafe_allow_html=True)
    st.markdown('<div class="section-header">Flash Zones Reference Table</div>', unsafe_allow_html=True)
    flash_rows = []
    for sz in SIZES:
        dd = insert_data[sz]
        il = dd["insert_len_short"]
        flash_rows.append({
            "Size": sz,
            "Insert OD (mm)": dd["insert_od"],
            "Top Flash Min (mm)": 0.8,
            "Top Flash Rec (mm)": 1.5,
            "Side Wall Min (mm)": round(dd["insert_od"] * 0.75, 1),
            "Side Wall Rec (mm)": round(dd["insert_od"] * 1.0, 1),
            "Bottom Flash Min (mm)": 0.5,
            "Bottom Flash Rec (mm)": 1.0,
            "Min Part Height (mm)": round(il + 0.8 + 0.5, 1),
            "Rec Part Height (mm)": round(il + 1.5 + 1.0, 1),
        })
    df_flash = pd.DataFrame(flash_rows)

    def hl_flash(row):
        if row["Size"] == f_size:
            return ["background-color: #edfaf4; color: #0a6e54"] * len(row)
        return [""] * len(row)

    st.dataframe(df_flash.style.apply(hl_flash, axis=1), use_container_width=True, hide_index=True)

    # ── SECTION 3: Pull-Out Force Estimator ──────────────────────────────────
    st.markdown('<div class="fancy-divider"></div>', unsafe_allow_html=True)
    st.markdown('<div class="section-header">💪 Pull-Out Force Estimator</div>', unsafe_allow_html=True)

    po1, po2 = st.columns([1, 2], gap="large")

    with po1:
        po_size = st.selectbox("Thread size", SIZES, index=2, key="po_size")
        po_mat  = st.selectbox("Material", materials_po, key="po_mat")
        po_dd   = insert_data[po_size]
        po_len_short = po_dd["insert_len_short"]
        po_len_long  = po_dd["insert_len_long"]
        if po_len_short == po_len_long:
            po_len = po_len_short
            st.markdown(f'<div class="info-card"><span style="font-family:Space Mono;color:#7ab8f5">Length: {po_len} mm</span></div>', unsafe_allow_html=True)
        else:
            po_len = st.slider("Insert length (mm)", po_len_short, po_len_long,
                               po_len_short, 0.1, key="po_len")

        install_quality = st.radio("Install quality",
            ["Poor (cold, crooked)", "Standard", "Optimal (hot, centered)"],
            index=1, key="po_qual", label_visibility="visible")

    with po2:
        mat_idx = materials_po.index(po_mat)
        base_force = pullout_base[po_size][mat_idx]

        # Length scaling: longer insert = more surface = more force (roughly linear with length)
        len_ref = po_dd["insert_len_short"]
        len_factor = po_len / len_ref if len_ref > 0 else 1.0

        # Quality factor
        if install_quality == "Poor (cold, crooked)":
            q_factor = 0.55
            q_color = "#e87050"
            q_note = "Cold installation leaves air gaps. Force can drop 40–50%."
        elif install_quality == "Standard":
            q_factor = 1.0
            q_color = "#38d9a9"
            q_note = "Clean installation with proper soldering iron temperature."
        else:
            q_factor = 1.20
            q_color = "#7ab8f5"
            q_note = "Optimal temp, perpendicular insertion, slow cool. +20% vs standard."

        est_force = round(base_force * len_factor * q_factor)
        safety_2x = round(est_force / 2)   # recommended max working load (50% safety factor)

        m1, m2, m3, m4 = st.columns(4)
        m1.metric("Est. Pull-Out Force", f"{est_force} N")
        m2.metric("Rec. Working Load", f"{safety_2x} N")
        m3.metric("≈ kg equiv.", f"{round(est_force/9.81)} kg")
        m4.metric("Safety Factor", "2.0×")

        # Bar chart: all materials for selected size
        forces_all = [round(pullout_base[po_size][i] * len_factor) for i in range(len(materials_po))]
        fig_po = go.Figure()
        fig_po.add_trace(go.Bar(
            x=materials_po, y=forces_all,
            marker_color=[q_color if m == po_mat else "#1e3a55" for m in materials_po],
            marker_line_color=["#38d9a9" if m == po_mat else "#2a4a6a" for m in materials_po],
            marker_line_width=2,
            text=[f"{f} N" for f in forces_all],
            textposition="outside",
            textfont=dict(family="Space Mono", size=10, color="#8aa5bf"),
        ))
        fig_po.update_layout(
            paper_bgcolor="#f8fbff", plot_bgcolor="#ffffff",
            font=dict(family="Space Mono, monospace", color="#4a6274", size=11),
            xaxis=dict(gridcolor="#e0ecf4"),
            yaxis=dict(gridcolor="#e0ecf4", title="Pull-Out Force (N)"),
            title=dict(text=f"{po_size} Pull-Out Force by Material  |  length={po_len}mm",
                       font=dict(color="#1a3a4a", size=13, family="Syne"), x=0.5),
            height=310, margin=dict(l=10, r=10, t=50, b=10),
        )
        st.plotly_chart(fig_po, use_container_width=True)

        st.markdown(f"""
        <div class="tip-box" style="border-color:{q_color}">
          <strong>Install quality note:</strong> {q_note}
        </div>
        <div class="warn-box">
          <strong>⚠️ Disclaimer:</strong> These are estimates based on published test data (CNC Kitchen, Markforged). Actual values depend on printer calibration, infill %, wall count, and filament brand. Always validate with physical testing for structural applications.
        </div>
        """, unsafe_allow_html=True)

    # Pull-out full table
    st.markdown('<div class="fancy-divider"></div>', unsafe_allow_html=True)
    st.markdown('<div class="section-header">Pull-Out Force Reference Table — Standard Install (N)</div>', unsafe_allow_html=True)

    po_rows = []
    for sz in SIZES:
        forces = pullout_base[sz]
        po_rows.append({
            "Size": sz,
            "PLA (N)": forces[0],
            "PETG (N)": forces[1],
            "ABS (N)": forces[2],
            "ASA (N)": forces[3],
            "PC (N)": forces[4],
            "PLA kg": round(forces[0]/9.81),
            "PETG kg": round(forces[1]/9.81),
        })
    df_po = pd.DataFrame(po_rows)

    def hl_po(row):
        if row["Size"] == po_size:
            return ["background-color: #edfaf4; color: #0a6e54"] * len(row)
        return [""] * len(row)

    st.dataframe(df_po.style.apply(hl_po, axis=1), use_container_width=True, hide_index=True)

    # Pull-out heatmap
    st.markdown('<div class="section-header">Pull-Out Force Heatmap</div>', unsafe_allow_html=True)
    po_matrix = [[pullout_base[sz][i] for i in range(len(materials_po))] for sz in SIZES]
    fig_heat = go.Figure(data=go.Heatmap(
        z=po_matrix,
        x=materials_po,
        y=SIZES,
        colorscale=[
            [0.0,  "#0a1420"],
            [0.2,  "#0d2a1a"],
            [0.5,  "#b8e8d0"],
            [0.8,  "#2a8060"],
            [1.0,  "#38d9a9"],
        ],
        text=[[f"{pullout_base[sz][i]} N" for i in range(len(materials_po))] for sz in SIZES],
        texttemplate="%{text}",
        textfont=dict(family="Space Mono", size=11, color="#e2f0ff"),
        hovertemplate="Size: %{y}<br>Material: %{x}<br>Force: %{z} N<extra></extra>",
    ))
    fig_heat.update_layout(
        paper_bgcolor="#f8fbff", plot_bgcolor="#f8fbff",
        font=dict(family="Space Mono, monospace", color="#4a6274", size=11),
        title=dict(text="Pull-Out Force (N) — All Sizes × Materials",
                   font=dict(color="#1a3a4a", size=13, family="Syne"), x=0.5),
        height=350, margin=dict(l=10, r=10, t=50, b=10),
        xaxis=dict(title="Material"),
        yaxis=dict(title="Insert Size"),
    )
    st.plotly_chart(fig_heat, use_container_width=True)


# ── Footer ────────────────────────────────────────────────────────────────────
st.markdown('<div class="fancy-divider"></div>', unsafe_allow_html=True)
st.markdown("""
<div style="text-align:center; font-family: Space Mono, monospace; font-size: 0.72rem; color: #2a4a5e; letter-spacing: 2px;">
  DATA SOURCES: CNC KITCHEN · ACCU-COMPONENTS · UTILS.COM · PRUSA COMMUNITY · MARKFORGED<br>
  VALUES ARE STARTING POINTS — ALWAYS TEST-PRINT FOR YOUR SPECIFIC PRINTER & MATERIAL
</div>
""", unsafe_allow_html=True)