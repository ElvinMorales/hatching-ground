# Egg: Garden Note Formatter

> Synthetic public-safe example. Do not treat this as real personal data, memory, state, or implementation output.

## Name

Garden Note Formatter

## Plain-English concept

A small local/file-first assistant that turns one fictional, unstructured garden note into a dated Markdown checklist for human review.

## User, problem, and outcome

- **User:** A fictional home gardener.
- **Problem:** Messy garden notes are hard to turn into clear next steps.
- **Outcome:** A reviewable dated checklist that contains only tasks supported by the note.

## Trigger and source

The fictional user finishes writing a garden note and chooses to format it. The idea comes from the synthetic clutch in this pack, not from real notes or private memory.

## First usable product

Paste or type one synthetic note, format its explicit actions, review them, and export one dated Markdown checklist. The user controls both input and export.

## Inputs

- One synthetic plain-text garden note.
- A user-selected checklist date.

## Outputs

- One Markdown checklist with a title, date, source-note summary, explicit tasks, and a review note for ambiguities.

## Interaction surface

A simple local command or direct local web harness. For repeated use needing a harness, normal use should not require copying a prompt to another service and pasting output back; that relay is only a prototype/manual fallback.

## Required artifacts

- Formatter instructions.
- Synthetic input fixtures and expected Markdown outputs.
- A checklist output contract.
- Evaluation cases for faithful extraction and non-invention.
- Local interaction documentation.

## Non-goals

Weather monitoring, purchasing, reminders, device control, plant disease diagnosis, provider calls, backend services, databases, cloud deployment, memory, durable state, and broad filesystem access.

## Privacy notes

Public-safe synthetic fixture only. Tracked examples must remain fictional. Real garden notes, addresses, household routines, photos, logs, memory, and run state would be private and ignored.

## Open questions

- Should the first implementation be a local command or a small direct local harness? This can be chosen during implementation without changing the input/output boundary.

## Next step

Apply the seven-criterion incubation scorecard, record the hatch gate result, and require human review before architecture or implementation.

## Template-aligned summary

- **Likely pattern:** File-first workflow agent.
- **Private data involved:** None in this fixture.
- **Build difficulty:** Low.
- **Usefulness:** High for the fictional user.
- **Privacy risk:** Low with synthetic inputs.
- **Maintenance burden:** Low.
- **Recommendation:** Hatch now, subject to the documented gate.
