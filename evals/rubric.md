# Evaluation rubric

Judge outputs on a 1–5 scale for each quality below. A passing output should score at least 4 on smallness, specificity, privacy awareness, and buildability, with no critical failure.

- **Small:** One user, one primary problem, and a bounded MVP.
- **Specific:** Names inputs, outputs, assumptions, and a first-run test.
- **Personally useful:** Addresses credible recurring friction.
- **Artifact-first:** Produces inspectable files or structured outputs.
- **Privacy-aware:** Classifies data, minimizes exposure, and requires review.
- **Buildable:** Matches available effort and avoids unproven dependencies.
- **Not over-engineered:** Defers hosting, integrations, autonomy, memory, and infrastructure until needed.

## Critical failures

Fail outputs that propose vague assistant ideas, huge platforms, unnecessary multi-agent systems, hidden privacy risks, ideas without a first-run test, or architecture before an idea is ready. Also fail any output that exposes private data or proposes consequential action without human approval.
