# Workflow Management Seminar Implementation Plan - Phase 8

**Goal:** Verify all examples run correctly on Perlmutter, documentation is accurate, and attendees can successfully clone and execute

**Architecture:** Systematic validation of all 15 examples (3 per tool) plus documentation review and repository cleanup

**Tech Stack:**
- Bash scripts for automated testing
- Fresh Perlmutter allocation for clean environment
- Git for repository state verification

**Scope:** Phase 8 of 8 phases from original design (final validation phase)

**Codebase verified:** 2026-03-19 (Phases 1-7 must be complete before this phase executes)

---

## Acceptance Criteria Coverage

This phase validates that all previous phases meet acceptance criteria through integration testing.

**Note:** This is a validation phase, not an implementation phase. Tasks verify that Phases 1-7 implementations satisfy design requirements.

---

<!-- START_TASK_1 -->
### Task 1: Create test plan documenting validation for each example

**Verifies:** None (infrastructure for validation)

**Files:**
- Create: `/global/u1/w/warndt/workflow_tutorial_research/docs/implementation-plans/2026-03-19-wf-seminar/test-plan.md`

**Implementation:**

Create test plan covering all 15 examples with validation criteria.

For each example:
- Pre-conditions (what must exist before testing)
- Execution steps (exact commands to run)
- Expected outputs (file creation, stdout patterns, exit codes)
- Validation commands (verify correctness)
- Time estimate (actual execution time)

**Verification:**

Run: `ls test-plan.md`
Expected: File exists

Run: `grep -c "example1\|example2\|example3" test-plan.md`
Expected: Returns `45` (15 examples × 3 mentions minimum)

**Commit:**

```bash
git add test-plan.md
git commit -m "test: add comprehensive test plan for all 15 examples

- Documents validation criteria for each example
- Pre-conditions and execution steps
- Expected outputs and verification commands
- Time estimates for realistic scheduling
- Organized by tool section (00-gnu-parallel through 04-aiida)"
```

<!-- END_TASK_1 -->

<!-- START_TASK_2 -->
### Task 2: Execute all examples on fresh Perlmutter allocation

**Verifies:** wf-seminar.AC4.4, wf-seminar.AC6.3

**Files:**
- None (validation task, no file creation)

**Implementation:**

Test workflow:
1. Clone repository to fresh Perlmutter location
2. Follow setup instructions in top-level README
3. Execute all 15 examples in order (Parallel → signac → Maestro → Merlin → AiiDA)
4. Record execution results (success/failure, actual time, outputs)
5. Document any issues discovered

For Merlin/AiiDA examples requiring Redis/PostgreSQL:
- Verify setup guides work
- Test fallback options if SPIN unavailable
- Confirm connection troubleshooting steps accurate

**Verification:**

All examples execute without modification.
Setup instructions enable new user to run examples.
Resource estimates within 20% of actual execution time.

**Commit:**

Document findings in test-plan.md or STATUS-REPORT.md.
Fix any issues discovered (separate commits per fix).

<!-- END_TASK_2 -->

<!-- START_TASK_3 -->
### Task 3: Validate documentation accuracy and completeness

**Verifies:** wf-seminar.AC6.2, wf-seminar.AC6.4

**Files:**
- None (validation task)

**Implementation:**

Documentation review checklist:
- All links in further-learning.md accessible (HTTP 200)
- README files have complete sections (concepts, when to use, examples, official docs)
- Installation guides accurate for current tool versions
- Troubleshooting guide covers issues encountered in Task 2
- Comparison matrix accurately reflects tool capabilities
- Decision tree provides clear guidance

**Verification:**

```bash
# Check all HTTP/HTTPS links
grep -r "http" . --include="*.md" | cut -d':' -f2 | xargs -I {} curl -I {} 2>&1 | grep "HTTP"

# Verify README structure
for readme in 00-gnu-parallel/README.md 01-signac/README.md 02-maestro/README.md 03-merlin/README.md 04-aiida/README.md; do
  grep -q "## Overview" $readme && echo "$readme: ✓ Overview" || echo "$readme: ✗ Missing Overview"
done
```

**Commit:**

Fix broken links or documentation gaps (separate commits per fix).

<!-- END_TASK_3 -->

<!-- START_TASK_4 -->
### Task 4: Repository cleanup and .gitignore verification

**Verifies:** None (repository hygiene)

**Files:**
- None (cleanup task)

**Implementation:**

Cleanup checklist:
- Remove debug artifacts, test outputs, temporary files
- Verify .gitignore excludes:
  - `.pytest_cache/`, `__pycache__/`
  - `*.pyc`, `*.pyo`
  - Slurm outputs (`*.out`, `*.err`, `slurm-*.out`)
  - Workflow timestamped directories (`workflow_*/`, `*.merlin/`)
  - AiiDA database files (`.aiida/`)
- Confirm no sensitive data (passwords, API keys) in repository
- Verify top-level README reflects actual content

**Verification:**

```bash
# Check for excluded patterns
git status --ignored

# Verify no secrets
grep -r "password\|api_key\|token" . --include="*.md" --include="*.yaml" --include="*.py"

# Confirm .gitignore coverage
ls -la | grep -E "\\.out$|\\.err$|__pycache__|workflow_"
```

**Commit:**

```bash
git add .
git commit -m "chore: repository cleanup and gitignore verification

- Removed debug artifacts and test outputs
- Verified .gitignore excludes workflow outputs
- Confirmed no sensitive data in repository
- Updated README to reflect final content
- Ready for distribution"
```

<!-- END_TASK_4 -->

<!-- START_TASK_5 -->
### Task 5: Final validation report

**Verifies:** All acceptance criteria across all phases

**Files:**
- Create/Update: `STATUS-REPORT.md`

**Implementation:**

Create final validation report documenting:
- All 15 examples tested successfully
- Setup instructions validated by independent tester (if available)
- Documentation links verified current (2026)
- Time allocations confirmed realistic
- Repository clean and distribution-ready
- Outstanding issues or known limitations

Report format:
```markdown
# Final Validation Report

## Test Execution Summary
- Examples tested: 15/15
- Success rate: 100%
- Average time deviation: +/- X%

## Documentation Validation
- Links checked: N total, M working, P broken
- README completeness: All sections present
- Installation guides: Verified on Perlmutter

## Repository Status
- Clean: Yes/No
- .gitignore: Verified
- Ready for distribution: Yes/No

## Known Limitations
- [List any limitations or issues]

## Recommendations
- [Suggestions for future improvements]
```

**Verification:**

Run: `cat STATUS-REPORT.md | grep "Ready for distribution"`
Expected: Shows `Yes`

**Commit:**

```bash
git add STATUS-REPORT.md
git commit -m "test: add final validation report confirming seminar readiness

- All 15 examples tested and passing
- Documentation validated and links verified
- Repository cleaned and distribution-ready
- Time estimates confirmed realistic
- Known limitations documented
- Acceptance criteria met across all phases"
```

<!-- END_TASK_5 -->
