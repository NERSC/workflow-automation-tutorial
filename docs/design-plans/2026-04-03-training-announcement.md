# Training Announcement Web Page Design

## Summary

This design creates a plain-text announcement document for the "Automating HPC Research Workflows on Perlmutter, May 2026" half-day training seminar. The document follows established NERSC training event page conventions for structure, tone, and content ordering, and is ready to paste into the NERSC web CMS. The announcement describes a remote seminar introducing five workflow management tools (GNU Parallel, signac, Maestro, Merlin, AiiDA) through hands-on examples on Perlmutter. All known event details are filled in directly; unavailable content (registration link and repository URL) is marked with labeled placeholders that will be replaced when those resources become available. The document is delivered as a version-controlled file in the repository, making updates straightforward and traceable.

## Definition of Done

A plain-text document ready to paste into the NERSC web CMS that announces the "Automating HPC Research Workflows on Perlmutter, May 2026" half-day seminar. The document follows NERSC training event page conventions (tone, structure, section ordering) and contains all known details filled in. Labeled placeholders mark content not yet available (registration link, GitHub repository URL). The document is committed to the repository for version tracking.

**In scope:** Page copy, structure, tone, all known event details, placeholder conventions.
**Out of scope:** HTML markup, CMS submission, registration form creation.

## Acceptance Criteria

### training-announcement.AC1: Document structure is complete and correctly ordered
- **training-announcement.AC1.1 Success:** Document contains all eight sections (title, header block, overview, topics, prerequisites, training resources, registration, materials) in the specified order
- **training-announcement.AC1.2 Success:** Topics section contains exactly five bullets, one per tool (GNU Parallel, signac, Maestro, Merlin, AiiDA)
- **training-announcement.AC1.3 Failure:** A section present in a different order fails the check

### training-announcement.AC2: Known details are filled in
- **training-announcement.AC2.1 Success:** Title reads "Automating HPC Research Workflows on Perlmutter, May 2026"
- **training-announcement.AC2.2 Success:** Date/time reads "May 28, 2026, 8 a.m. – 12 p.m. PDT"
- **training-announcement.AC2.3 Success:** Location reads "Remote"
- **training-announcement.AC2.4 Success:** Prerequisites list contains Slurm job submission, shell scripting, and Python basics — no NERSC account requirement

### training-announcement.AC3: Placeholders are present and correctly labeled
- **training-announcement.AC3.1 Success:** Registration section contains exactly the string `[REGISTRATION_URL]`
- **training-announcement.AC3.2 Success:** Materials section contains exactly the string `[REPOSITORY_URL]`
- **training-announcement.AC3.3 Failure:** Either placeholder is absent or uses a different format

### training-announcement.AC4: Tone and phrasing match NERSC conventions
- **training-announcement.AC4.1 Success:** Overview paragraph is written in third person
- **training-announcement.AC4.2 Success:** Training resources line reads "Training accounts for Perlmutter will be provided to registered participants"
- **training-announcement.AC4.3 Failure:** Overview paragraph contains first-person language or promotional phrasing

## Glossary

- **NERSC**: National Energy Research Scientific Computing Center, a DOE facility providing high-performance computing resources to researchers
- **Perlmutter**: A supercomputer at NERSC used as the training platform for this seminar
- **CMS**: Content Management System, the web publishing platform used by NERSC for event announcements
- **GNU Parallel**: A shell tool for executing jobs in parallel on single or multiple machines
- **signac**: A Python framework for managing data and workflows in computational research projects
- **Maestro**: A lightweight workflow orchestration tool for defining and executing task dependencies as directed acyclic graphs
- **Merlin**: A distributed workflow system designed for large-scale ensemble simulations, built on top of Maestro
- **AiiDA**: An automated interactive infrastructure and database for computational science, emphasizing provenance tracking and reproducibility
- **Slurm**: A workload manager and job scheduler used on HPC systems including Perlmutter
- **PDT**: Pacific Daylight Time, the timezone for the event schedule

## Architecture

Single plain-text file delivered at `docs/training-announcement.txt` (or `.md`). No HTML, no templating system — raw copy ready for paste into the NERSC web CMS.

The document has seven sections in a fixed order:

1. **Title line** — event name including year and month
2. **Header block** — date, time with timezone, location (two lines)
3. **Overview paragraph** — three sentences, third person, describes what participants will do and learn
4. **Topics** — five bullet points, one per tool, format: `Tool name: one-line description`
5. **Prerequisites** — three bullet points describing assumed background knowledge
6. **Training resources** — one sentence using standard NERSC phrasing for training account access
7. **Registration** — one line: `Register at [REGISTRATION_URL]`
8. **Materials** — one line: `Slides and example code: [REPOSITORY_URL]`

Sections 7 and 8 use labeled placeholders (`[REGISTRATION_URL]`, `[REPOSITORY_URL]`) that are replaced when those details become available.

## Existing Patterns

This design follows NERSC training event page conventions established across five sampled pages:

- **Standard structure**: Title + date/time/location header → overview paragraph → topics list → prerequisites → registration/materials. Followed by containers-mar2026, hpcsdk-mar2026, and new-user-training-february-2026.
- **Training account phrasing**: Standard NERSC language is "Training accounts for Perlmutter will be provided to [qualifier]" — seen verbatim in dl-at-scale and agentic-ai-bootcamp pages.
- **Prerequisites as bullets**: Newer 2026 events (agentic-ai-bootcamp, ai-for-science-bootcamp) list prerequisites as a bullet list rather than a paragraph. This design follows that pattern.
- **Topics as one-liners**: Containers and HPC SDK pages list topics with one-line descriptions and no time estimates. This design follows that pattern (lighter than the time-blocked ATPESC/DL-at-Scale style, appropriate for a half-day event).
- **Tone**: Terse, professional, third person. No marketing language. Matches all sampled pages.

This design diverges from one pattern: "Who should attend" is omitted. Only one of six sampled pages (DL4SCI) uses this section explicitly; the norm is implicit targeting through the overview paragraph and prerequisites.

## Implementation Phases

<!-- START_PHASE_1 -->
### Phase 1: Announcement Page Content

**Goal:** Create the plain-text announcement document with all known details filled in and placeholders for unavailable content.

**Components:**
- `docs/training-announcement.txt` — the complete announcement page copy, ready to paste into the NERSC CMS

**Dependencies:** None (first phase)

**Done when:** File exists at `docs/training-announcement.txt`, all seven sections are present in order, all known details are filled in (title, date, time, timezone, location, overview, five tool one-liners, three prerequisites, training resources sentence), and both placeholder labels (`[REGISTRATION_URL]`, `[REPOSITORY_URL]`) appear exactly once each.
<!-- END_PHASE_1 -->

<!-- START_PHASE_2 -->
### Phase 2: Placeholder Resolution

**Goal:** Replace the two labeled placeholders with live URLs when registration and repository are ready.

**Components:**
- `docs/training-announcement.txt` — updated in-place: `[REGISTRATION_URL]` replaced with the actual registration link, `[REPOSITORY_URL]` replaced with the actual GitHub repo URL

**Dependencies:** Phase 1 (file must exist); registration link must be provided; GitHub repo URL must be confirmed

**Done when:** Neither `[REGISTRATION_URL]` nor `[REPOSITORY_URL]` appears in the file; both replaced with real URLs.
<!-- END_PHASE_2 -->

## Additional Considerations

**Placeholder convention:** Both placeholders use `[ALL_CAPS_WITH_UNDERSCORES]` format to make them visually distinct in plain text and easy to locate with a simple search.

**File format:** `.txt` extension keeps the file unambiguous as plain text for CMS paste. If the repo prefers Markdown for rendering, `.md` is an acceptable alternative — the content is identical either way.

**Post-event update:** After the seminar, the Materials line (`[REPOSITORY_URL]`) will be live. No structural changes needed — the placeholder resolves in Phase 2.
