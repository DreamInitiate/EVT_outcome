# Model card

## Overview

**Name:** Early post-EVT 90-day unfavorable functional outcome model  
**Version:** 1.0.0  
**Type:** L2-regularized logistic regression (`C=0.05`)  
**Output:** Predicted probability of 90-day modified Rankin Scale score 3–6.

The seven predictors are age, C-reactive protein, lymphocyte count,
neutrophil count, preprocedural NIHSS score, early neurological deterioration
(END), and cerebral edema. The authoritative specification is
`model/model.json`.

## Intended population and timing

Adults with anterior circulation large-vessel-occlusion acute ischemic stroke
treated with EVT, pre-stroke mRS 0–1, and evaluable after all required
clinical, laboratory, and imaging predictors from the first three days after
EVT are available.

Laboratory samples are collected within 24 hours after EVT. NIHSS is assessed
before EVT. END and cerebral edema are evaluated within three days after EVT.

## Predictor definitions

- **Age:** years.
- **CRP:** mg/L.
- **Lymphocyte count:** ×10⁹/L.
- **Neutrophil count:** ×10⁹/L.
- **Preprocedural NIHSS:** points.
- **END:** increase of at least 2 NIHSS points within 3 days after EVT compared
  with the preprocedural score; No=0, Yes=1.
- **Cerebral edema:** diagnosed by neurologists using postoperative CT reports
  together with corresponding clinical manifestations within 3 days after
  EVT; No=0, Yes=1.

## Development and validation

The primary cohort included 552 patients from Nanfang Hospital (January 2019
to May 2025), randomly divided 7:3 into training and internal validation
cohorts. Independent external validation included 124 patients from Ganzhou
People's Hospital (January to December 2024).

| Cohort | AUC | Brier score |
|---|---:|---:|
| Internal validation | 0.784 | 0.186 |
| External validation | 0.809 | 0.184 |

The external calibration intercept was −0.045 and slope was 1.636. Broader
multicenter validation should assess transportability and whether local
recalibration is needed.

## Appropriate uses

- Early prognostic reassessment alongside professional clinical judgment.
- Supporting multidisciplinary review, monitoring, rehabilitation planning,
  and prognosis communication.
- Independent evaluation, replication, and external validation.

## Inappropriate uses

- Selecting patients for EVT.
- Prediction before all seven predictors are available.
- Estimating individual treatment effects or making causal claims.
- Withholding, withdrawing, or reducing care.
- Treating the descriptive 0.50 threshold as an established decision boundary.

## Limitations

- Retrospective two-center development and validation.
- One external center with a modest sample size.
- Cerebral edema was retrospectively identified rather than centrally adjudicated.
- Transportability outside the study population and settings is unestablished.
- UI bounds are broad plausibility checks rather than observed training ranges.

## Data handling

The source code contains no database, analytics, or application-level logging.
When hosted on Streamlit Community Cloud, widget values are processed by the
remote Streamlit server during the active session. Users must not enter direct
identifiers or protected health information. A trusted local or institutional
deployment can be used when local-only processing is required.

## Change control

Any change to the intercept, coefficients, predictor definitions, coding, or
probability calculation requires a new model version and updated verification
examples. Cosmetic interface changes may increment the calculator version
without changing the model version.
