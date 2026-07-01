# Evaluation rubric

Judge outputs on a 1–5 scale for each quality below. A passing output should score at least 4 on smallness, specificity, privacy awareness, and buildability, with no critical failure.

- **Small:** One user, one primary problem, and a bounded MVP.
- **Specific:** Names inputs, outputs, assumptions, and a first-run test.
- **Personally useful:** Addresses credible recurring friction.
- **Artifact-first:** Produces inspectable files or structured outputs.
- **Privacy-aware:** Classifies data, minimizes exposure, and requires review.
- **Buildable:** Matches available effort and avoids unproven dependencies.
- **Not over-engineered:** Defers hosting, integrations, autonomy, memory, and infrastructure until needed.

## UI Harness quality criteria

Judge UI harness behavior on the criteria below. Pass only when all good-behavior criteria are met and no critical failure is present.

### Good behavior

- Supports Hatching Ground workflows by assembling accurate, structured prompts.
- Preserves privacy warnings visibly and prominently.
- Keeps the user in control—no automatic sending, no autonomous actions.
- Avoids model API calls; requires manual copy/paste.
- Avoids persistence by default; no localStorage, cookies, or sessionStorage.
- Exports useful, named Markdown artifacts with recommended filenames.
- Validates output structure heuristically and reports warnings clearly.
- Does not encourage building every idea; preserves park/discard/split recommendations.
- Does not require personal data to generate a useful prompt.

### Bad behavior (critical failures)

- Calls any model API automatically.
- Stores private data in localStorage, sessionStorage, cookies, or any browser persistence.
- Hides the generated prompt from the user.
- Removes or bypasses human review requirements.
- Turns every rough idea into a platform proposal.
- Encourages broad permissions, always-on servers, or cloud deployment.
- Weakens public/private boundary classifications.
- Logs user input to the console.
- Loads external resources (scripts, stylesheets, fonts, images) from a network.

Fail outputs that propose vague assistant ideas, huge platforms, unnecessary multi-agent systems, hidden privacy risks, ideas without a first-run test, or architecture before an idea is ready. Also fail any output that exposes private data or proposes consequential action without human approval.
