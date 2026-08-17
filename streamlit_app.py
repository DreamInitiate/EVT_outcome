"""Streamlit interface for the locked early post-EVT outcome model."""

from __future__ import annotations

import streamlit as st

from model import MODEL, predict, validate_plausibility


st.set_page_config(
    page_title="EVT 90-Day Outcome Calculator",
    page_icon="🧠",
    layout="wide",
    initial_sidebar_state="expanded",
)

st.markdown(
    """
    <style>
    :root {
      --evt-accent: #0f6b57;
      --evt-hover: #094c3e;
      --evt-line: rgba(128, 128, 128, .34);
      --evt-surface: rgba(128, 128, 128, .10);
    }
    .block-container { max-width: 1180px; padding-top: 2.6rem; padding-bottom: 4rem; }
    h1, h2, h3 { color: inherit !important; letter-spacing: -.025em; }
    h1 { font-size: clamp(2.35rem, 5vw, 4.4rem) !important; line-height: 1.02 !important; }
    .eyebrow {
      display: inline-block;
      background: var(--evt-accent);
      border-radius: 999px;
      color: #fff;
      font-size: .72rem;
      font-weight: 800;
      letter-spacing: .14em;
      padding: .38rem .68rem;
      text-transform: uppercase;
    }
    .lead { color: inherit; font-size: 1.08rem; line-height: 1.65; max-width: 760px; opacity: .72; }
    div[data-testid="stForm"] {
      background: transparent !important;
      border: 1px solid var(--evt-line) !important;
      border-radius: 18px;
      padding: 1.25rem 1.35rem 1.45rem;
    }
    div[data-testid="stMetric"] {
      background: var(--evt-surface) !important;
      border: 1px solid var(--evt-line);
      border-radius: 14px;
      padding: .8rem 1rem;
    }
    [data-testid="stWidgetLabel"],
    [data-testid="stWidgetLabel"] p,
    [data-testid="stMarkdownContainer"],
    [data-testid="stMarkdownContainer"] p,
    [data-testid="stCaptionContainer"],
    [data-testid="stMetricLabel"],
    [data-testid="stMetricValue"] {
      color: inherit !important;
    }
    [data-testid="stCaptionContainer"] { opacity: .72; }
    [data-testid="stNumberInput"] input {
      background: var(--evt-surface) !important;
      color: inherit !important;
      -webkit-text-fill-color: currentColor !important;
    }
    [data-testid="stNumberInput"] input::placeholder {
      color: inherit !important;
      -webkit-text-fill-color: currentColor !important;
      opacity: .56 !important;
    }
    [data-testid="stNumberInput"] button,
    [data-testid="stTooltipIcon"] {
      color: inherit !important;
      opacity: .72;
    }
    [data-testid="stTooltipIcon"] svg {
      fill: currentColor !important;
      stroke: currentColor !important;
    }
    [data-testid="stRadio"] label,
    [data-testid="stRadio"] label p {
      color: inherit !important;
    }
    [data-testid="stVerticalBlockBorderWrapper"] {
      border-color: var(--evt-line) !important;
    }
    .katex { color: inherit !important; }
    [data-testid="stSidebar"] .model-summary { line-height: 1.55; opacity: .82; }
    .equation-note { font-size: .82rem; line-height: 1.45; opacity: .72; }
    .st-key-equation_panel .katex { font-size: .90em !important; }
    .st-key-equation_panel .katex-display {
      margin: .7rem 0;
      overflow-x: auto;
      overflow-y: hidden;
      padding-bottom: .12rem;
    }
    .result-card { background: #102a24; border-radius: 18px; color: white; padding: 1.45rem 1.55rem; margin-bottom: 1rem; }
    .result-card .label { color: #b7d0c8; font-size: .72rem; font-weight: 800; letter-spacing: .12em; text-transform: uppercase; }
    .result-card .number { font-size: 3.35rem; font-weight: 650; letter-spacing: -.05em; margin: .25rem 0; }
    .result-card .caption { color: #d7e4e0; line-height: 1.5; }
    .muted-card { background: var(--evt-surface); border: 1px solid var(--evt-line); border-radius: 14px; color: inherit; padding: 1rem 1.1rem; line-height: 1.55; }
    .muted-card { opacity: .82; }
    .footer { border-top: 1px solid var(--evt-line); color: inherit; font-size: .76rem; line-height: 1.6; margin-top: 2.8rem; opacity: .72; padding-top: 1.1rem; }
    .stButton > button, .stFormSubmitButton > button { border-radius: 10px; font-weight: 700; }
    .stFormSubmitButton > button { background: var(--evt-accent); color: white; border-color: var(--evt-accent); }
    .stFormSubmitButton > button:hover { background: var(--evt-hover); border-color: var(--evt-hover); color: white; }
    @media (prefers-contrast: more) {
      :root {
        --evt-line: rgba(128, 128, 128, .72);
        --evt-surface: rgba(128, 128, 128, .18);
      }
      .lead, .muted-card, .footer, [data-testid="stCaptionContainer"] { opacity: 1; }
      [data-testid="stNumberInput"] input::placeholder { opacity: .82 !important; }
    }
    </style>
    """,
    unsafe_allow_html=True,
)


predictors = {item["id"]: item for item in MODEL["predictors"]}

with st.sidebar:
    st.markdown("### EVT Outcome Calculator")
    st.caption(f"Locked model version {MODEL['model_version']}")
    st.markdown(
        '<p class="model-summary">An externally validated, fixed-coefficient '
        "logistic regression model for adults with anterior circulation "
        "large-vessel-occlusion ischemic stroke treated with endovascular "
        "thrombectomy.</p>",
        unsafe_allow_html=True,
    )
    st.divider()
    st.markdown("**Prediction time**  ")
    st.write("After all required variables from the first 3 days following EVT are available.")
    st.markdown("**Outcome**  ")
    st.write("90-day unfavorable functional outcome: modified Rankin Scale score 3–6.")
    st.divider()
    st.warning(
        "Research-use clinical prediction support only. Do not use this calculator "
        "alone to select treatment or to reduce or withdraw care."
    )
    st.caption(
        "Community Cloud processes entered values on its server for the active "
        "session. This app contains no database, analytics, or application-level "
        "logging. Do not enter names, identifiers, or other protected health information."
    )

st.markdown('<div class="eyebrow">3-day post-EVT reassessment</div>', unsafe_allow_html=True)
st.title("Estimate 90-day unfavorable functional outcome probability")
input_column, result_column = st.columns(
    [1.35, 1], gap="large", vertical_alignment="top"
)

with input_column:
    st.subheader("Patient inputs")
    st.caption(
        "Enter all seven predictors using the stated units and timing. The displayed "
        "limits are broad plausibility guardrails, not the observed training ranges."
    )
    with st.form("calculator_form", border=True):
        left, right = st.columns(2, gap="medium")
        with left:
            age = st.number_input(
                "1. Age (years)", min_value=18, max_value=110, value=None, step=1,
                placeholder="e.g., 70",
            )
            lymphocyte = st.number_input(
                "2. Lymphocyte count (×10⁹/L)", min_value=0.0, max_value=10.0,
                value=None, step=0.01, format="%.2f", placeholder="e.g., 1.50",
                help=predictors["lymphocyte"]["timing"],
            )
            nihss = st.number_input(
                "3. Preprocedural NIHSS score (points)", min_value=0, max_value=42,
                value=None, step=1, placeholder="e.g., 15",
                help=predictors["nihss"]["timing"],
            )
        with right:
            crp = st.number_input(
                "4. C-reactive protein (mg/L)", min_value=0.0, max_value=500.0,
                value=None, step=0.01, format="%.2f", placeholder="e.g., 10.00",
                help=predictors["crp"]["timing"],
            )
            neutrophil = st.number_input(
                "5. Neutrophil count (×10⁹/L)", min_value=0.0, max_value=50.0,
                value=None, step=0.01, format="%.2f", placeholder="e.g., 7.50",
                help=predictors["neutrophil"]["timing"],
            )
            end_label = st.radio(
                "6. Early neurological deterioration (END)", ["No", "Yes"],
                horizontal=True, help=predictors["end"]["definition"],
            )
            edema_label = st.radio(
                "7. Cerebral edema", ["No", "Yes"], horizontal=True,
                help=predictors["cerebral_edema"]["definition"],
            )
        submitted = st.form_submit_button(
            "Calculate predicted probability", use_container_width=True, type="primary"
        )

    values = {
        "age": age,
        "crp": crp,
        "lymphocyte": lymphocyte,
        "neutrophil": neutrophil,
        "nihss": nihss,
        "end": 1 if end_label == "Yes" else 0,
        "cerebral_edema": 1 if edema_label == "Yes" else 0,
    }

with result_column:
    st.subheader("Model output")
    if submitted:
        errors = validate_plausibility(values)
        if errors:
            for error in errors:
                st.error(error)
        else:
            _, probability = predict(values)
            st.markdown(
                f"""
                <div class="result-card">
                  <div class="label">Predicted probability</div>
                  <div class="number">{probability * 100:.1f}%</div>
                  <div class="caption">Estimated probability of a 90-day modified
                  Rankin Scale score of 3–6.</div>
                </div>
                """,
                unsafe_allow_html=True,
            )
            st.progress(probability)
    else:
        st.markdown(
            '<div class="muted-card"><strong>No result yet.</strong><br>Complete all '
            "five numeric inputs, select the two binary predictors, and choose "
            "Calculate predicted probability.</div>",
            unsafe_allow_html=True,
        )

    with st.container(border=True, key="equation_panel"):
        st.markdown("**Linear predictor**")
        st.markdown(
            '<div class="equation-note">Locked raw-scale model equation</div>',
            unsafe_allow_html=True,
        )
        st.latex(
            r"""
            \begin{aligned}
            \mathrm{LP} ={}& -3.261854950250 \\
            &+ 0.027956881229\,(\mathrm{Age}) \\
            &- 0.022379601582\,(\mathrm{Lymphocyte}) \\
            &+ 0.068403101354\,(\mathrm{Neutrophil}) \\
            &+ 0.003783356189\,(\mathrm{CRP}) \\
            &+ 0.046180231591\,(\mathrm{NIHSS}) \\
            &+ 0.994514705102\,(\mathrm{END}) \\
            &+ 1.296954431745\,(\mathrm{Cerebral\ edema})
            \end{aligned}
            """
        )
        st.markdown("**Predicted probability**")
        st.latex(r"\displaystyle p=\frac{1}{1+e^{-\mathrm{LP}}}")

st.divider()
st.subheader("Model transparency")
st.markdown(
    "The calculator uses the locked raw-scale coefficients from the final "
    "L2-regularized logistic regression model. It performs no model fitting or "
    "recalibration. Internal validation AUC was **0.784** with Brier score "
    "**0.186**; independent external validation AUC was **0.809** with Brier "
    "score **0.184**."
)
st.info(
    "The external calibration slope was 1.636. Broader multicenter validation "
    "and, where appropriate, local recalibration are required before routine use "
    "in other settings."
)

with st.expander("Intended population and predictor definitions"):
    st.markdown(
        """
        **Intended population:** Adults with anterior circulation large-vessel-occlusion
        acute ischemic stroke treated with EVT, pre-stroke mRS 0–1, and evaluable after
        the first 3 postprocedural days.

        **END:** Increase of at least 2 NIHSS points within 3 days after EVT compared
        with the preprocedural score. Code No=0 and Yes=1.

        **Cerebral edema:** Evaluated within 3 days after EVT and diagnosed by
        neurologists according to postoperative CT reports together with corresponding
        clinical manifestations. Code No=0 and Yes=1.

        Laboratory predictors are collected within 24 hours after EVT. The NIHSS score
        is assessed before EVT.
        """
    )

st.markdown(
    f"""
    <div class="footer">
      <strong>Research-use clinical prediction support.</strong> Model v{MODEL['model_version']} ·
      MIT-licensed code · No database, analytics, cookies, or application-level logging.
      Community Cloud values are processed server-side during the active session; do not
      enter direct patient identifiers.
    </div>
    """,
    unsafe_allow_html=True,
)
