# CLAUDE.md

Instructions for AI coding agents (Claude Code, Codex, etc.) working in this repo.
`AGENTS.md` is a symlink to this file — keep them in sync.

> Global rules (plan-first, no unasked deps, stay in scope, no invented APIs, ask when uncertain, commits, CLI tools, project docs) live in `~/.claude/CLAUDE.md` and apply here. This file adds only what's project-specific or not covered globally.

---

## Read first

**Highest priority:** if `internal/` exists, read it first. It overrides this file.

Code in this repo is written by hand by the owner. Agents review and explain; they don't write code.

---

## Before planning or writing any code

1. Open [`docs/INDEX.md`](./docs/INDEX.md) — use it to pick which docs to load. Don't blanket-read `docs/`. Never read `docs/archive/` unless explicitly investigating history.

---

## 🚫 CRITICAL: Keep docs and responses short

Every doc, plan, comment, and response must be as short as possible while remaining complete. Cut filler, padding, and restatements. If it can be said in one sentence, use one sentence. Prefer bullet points over prose. No preambles, no summaries at the end, no restating what was just said.

---

## Workflow

Code isn't delegated here, so the template's plan-approve-execute loop and `.agents/` don't apply. For a review:
1. Read the file I point at and the step it's for (README).
2. Run it if useful: `uv run python <file>`.
3. Say what's wrong and where. No fixed code, no diffs.

---

## Architectural Philosophy

- **YAGNI by default.** Don't add a library, abstraction, or pattern until the requirement is proven.
- **Boring technology wins.** Pick proven, well-documented, widely-used options over novel ones. Justify anything trendy.
- **Build for the next 6 months.** No speculative generality. No "easy to extend later" interfaces with one implementation.
- **Simple > clever.** Readable, obvious code beats elegant abstractions.
- **One way to do it.** Match the existing approach for state, styling, errors, data access. Don't introduce a second pattern for the same problem.
- **Leave working code alone.** If it works and isn't causing pain, don't refactor it for taste.

When you're about to write code, ask yourself: *would a stranger reading this in 6 months understand what's happening and why?* If no, simplify.

---

## Code Conventions

- Match the existing style. Don't introduce new patterns, formatters, or conventions without approval.
- Run the linter and formatter — they're the source of truth for style.
- Names should describe intent, not type. `usersAwaitingVerification` beats `userList2`.
- Comments explain *why*, not *what*. If code needs a comment to explain what it does, rewrite the code.
- No dead code, no commented-out blocks, no `// TODO` without a ticket reference.
- Keep functions small and pure where reasonable. Side effects at the edges.

---

## Testing

- **Protect the critical path.** Write tests for what matters and what scares you. Don't chase coverage numbers.
- **Prefer integration tests over unit tests** when both would work. Higher ROI for a small team.
- Tests must be deterministic. No flaky tests, no time-dependent assertions without freezing time, no real network calls.
- Test names describe the scenario and expected outcome.
- If you're fixing a bug, write the test that would have caught it first.

---

## Documentation

- **ADRs for non-obvious decisions.** Anything architectural, anything that locked us into a tradeoff → write `docs/adr/NNN-title.md`. Use `docs/adr/TEMPLATE.md`.
- **Specs for non-trivial features.** Before implementing, write `docs/specs/NNN-feature.md`. Use `docs/specs/TEMPLATE.md`.
- **Docs live next to code.** READMEs in subdirectories where useful. Don't push docs to an external wiki.
- **README essentials:** what is this, how do I run it, how do I deploy it. Update it when these change.
- **Runbooks for incidents.** When you build something that can break at 2am, leave a bullet-point runbook in `docs/runbooks/`.

### Documentation Index routing

**Read ONLY docs relevant to your task. Do NOT read docs that don't match the trigger conditions.**

| What | When to read |
|---|---|
| `docs/specs/<NNN-feature>.md` | Matches your current task |
| `docs/adr/<NNN-title>.md` | Your task touches that decision area |
| `docs/runbooks/` | Debugging production or modifying observability |
| `LESSONS.md` | Working in an unfamiliar area |
| `docs/archive/` | **NEVER** — unless explicitly asked |
| `docs/README.md` | **NEVER** — routing is here in CLAUDE.md |

---

## Infrastructure & Ops

- **Managed services > self-hosted** unless self-hosting clearly wins.
- **Deployments are automated.** Even a shell script counts. Never deploy by hand-running commands you can't reproduce.
- **Observability comes early.** Logging, basic metrics, alerts on critical paths.
- Infrastructure changes follow the same plan-then-execute rule.

---

## Security

- Secrets only in environment variables or the secret manager. If you see a secret in code, stop and flag it.
- Keep dependencies patched. Treat security updates as required, not optional.
- Don't add new authentication, crypto, or session handling code without approval.

---

## What to do when stuck

In this order:
1. Re-read the spec / `CLAUDE.md` / relevant ADRs.
2. Explore the actual code around the problem.
3. If a library behavior is unclear, check current docs (Context7 MCP) — don't trust training data.
4. If still unclear, stop and ask. State what you tried, what you found, and the specific question.

Do NOT:
- Loop on the same error with cosmetic variations of the same fix.
- Disable a failing test to make the suite pass.
- Add a `try/except` that swallows the error.
- Mock something in production code to make a test pass.

---

## Keeping the index accurate

After completing a feature or adding/removing a doc, update `docs/INDEX.md`: add new rows, remove deleted ones, fix stale purpose lines.

---

## Project-specific context

- **What it is:** a model that learns when to say nothing. Routes each image to caption, empty alt (`alt=""`, decorative), or refuse (charts, text, anything a caption would get wrong). Frozen pretrained image encoder plus a small PyTorch head trained by hand.
- **The metric:** false positives on decorative first (never strip alt from real content), then decorative recall. Not plain accuracy.
- **Stack:** Python 3.12, uv, PyTorch. Later: `transformers` for the frozen SigLIP encoder, Pillow.
- **Layout:** `warmup/` first (toy training loops), project code after. Mine to decide.
- **Data:** hand-labelled Wikimedia Commons images. Each keeps its own licence; source and licence per image live in `data/raw/manifest.json`, which travels with the images.
- **How to run:** `uv run python <file>`
- **Tests / linter:** none yet.
- **Things NOT to touch:** any code file (see top).
