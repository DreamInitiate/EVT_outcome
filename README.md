# EVT 90-Day Outcome Calculator — Streamlit

[![Model tests](https://github.com/TO-BE-UPDATED/evt-outcome-calculator/actions/workflows/test.yml/badge.svg)](https://github.com/TO-BE-UPDATED/evt-outcome-calculator/actions)
[![Open in Streamlit](https://static.streamlit.io/badges/streamlit_badge_black_white.svg)](https://TO-BE-UPDATED.streamlit.app/)

Open-source Streamlit implementation of a locked, fixed-coefficient logistic
regression model for estimating 90-day unfavorable functional outcome
(modified Rankin Scale score 3–6) after endovascular thrombectomy (EVT) for
anterior circulation acute ischemic stroke.

中文部署说明见 [DEPLOYMENT_GUIDE_CN.md](DEPLOYMENT_GUIDE_CN.md)。

## What is included

- `streamlit_app.py`: public web interface with seven predictor inputs.
- `model/model.json`: authoritative intercept, coefficients, units, coding,
  definitions, and reported performance.
- `model.py`: dependency-free prediction and validation functions.
- `tests/test_model.py`: fixed worked examples protecting against accidental
  coefficient, coding, or formula changes.
- `MODEL_CARD.md`: intended use, limitations, validation, and governance.
- `CITATION.cff`: GitHub-readable software citation metadata.
- `.github/workflows/test.yml`: automatic model verification on every change.

## Model equation

```text
LP =
-3.261854950250
+ 0.027956881229 × Age
- 0.022379601582 × Lymphocyte count
+ 0.068403101354 × Neutrophil count
+ 0.003783356189 × CRP
+ 0.046180231591 × preprocedural NIHSS
+ 0.994514705102 × END
+ 1.296954431745 × cerebral edema

p = 1 / (1 + exp(-LP))
```

END and cerebral edema are coded No=0 and Yes=1. Coefficients retain the
unrounded precision exported from the final model; Supplementary Table S6
presents rounded display values.

## Run locally

Python 3.12 is recommended.

```bash
python -m venv .venv
# Windows: .venv\Scripts\activate
# macOS/Linux: source .venv/bin/activate
python -m pip install -r requirements.txt
streamlit run streamlit_app.py
```

Verify the locked prediction formula without starting the web app:

```bash
python -m unittest discover -s tests -v
```

## Deploy on Streamlit Community Cloud

1. Create a public GitHub repository, for example
   `evt-outcome-calculator`, and upload this folder's contents to its root.
2. Sign in to [Streamlit Community Cloud](https://share.streamlit.io/) with
   GitHub and choose **Create app**.
3. Select the repository, branch `main`, and entrypoint
   `streamlit_app.py`.
4. In advanced settings, select Python 3.12. No secrets are required.
5. Deploy, then add the resulting `https://...streamlit.app/` URL to this
   README and to the repository's **About** section.

Community Cloud runs the app from the GitHub repository and redeploys after
new commits. See the Chinese guide for the complete release workflow.

## Privacy

This application deliberately contains no database, analytics, cookies, or
application-level logging. Streamlit Community Cloud nevertheless processes
widget values on its server during the active session. Users should enter
only the seven required deidentified values and must not enter patient names,
record numbers, dates of birth, or other protected health information. For
local-only processing, run the application on a trusted local computer or
institutional server.

## Before the first public release

- Confirm the final manuscript, Supplementary Table S6, nomogram, JSON file,
  and tests all use the same locked model version.
- Replace every `TO-BE-UPDATED` placeholder with the final repository/app URL.
- Add the final author list, affiliations, article DOI, and contact details
  after they are approved for release.
- Do not upload patient-level data, identifiable information, journal-formatted
  PDFs, copyrighted figures, or unpublished confidential material.
- Create a frozen `v1.0.0` GitHub Release and archive that release with Zenodo
  after the repository metadata is complete.

## License and disclaimer

Code and the machine-readable model specification are provided under the MIT
License. This calculator is research-use clinical prediction support, not a
medical device, and does not replace professional judgment. It must not be
used alone to select EVT, estimate causal treatment effects, or reduce or
withdraw care.
