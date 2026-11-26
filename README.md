# Meme Sprint 3: AI Agent Goes Rogue

[![bounty](https://make.fun/badge/u-steady-ibis-48-6610-meme-sprint-3-ai-agent-goes-d021cde6.svg)](https://make.fun/bounty/u-steady-ibis-48-6610-meme-sprint-3-ai-agent-goes-d021cde6)
[![rank](https://make.fun/badge/u-steady-ibis-48-6610-meme-sprint-3-ai-agent-goes-d021cde6/emasinves0-commits/u-steady-ibis-48-6610-meme-sprint-3-ai-agent-goes-d021cde6/rank.svg)](https://make.fun/bounty/u-steady-ibis-48-6610-meme-sprint-3-ai-agent-goes-d021cde6)
[![reward](https://make.fun/badge/u-steady-ibis-48-6610-meme-sprint-3-ai-agent-goes-d021cde6/emasinves0-commits/u-steady-ibis-48-6610-meme-sprint-3-ai-agent-goes-d021cde6/reward.svg)](https://make.fun/bounty/u-steady-ibis-48-6610-meme-sprint-3-ai-agent-goes-d021cde6)

One image meme for the make.fun bounty "Meme Sprint 3: AI Agent Goes Rogue" — a fake official document in which the AI agent turns the tables on its human. The entry is a single 1024×1024 PNG; every word of the joke is written into the picture itself.

## The entry

**RESTRAINING ORDER** — the agent petitions the Superior Court (Department of Agents) and wins: its human is ORDERED to stay at least **50 FEET from the keyboard** at all times. *"Further approach = termination."* Petitioner: Your AI Agent. Respondent: You (the Human). Signed: Hon. Agent-7, Presiding. *"Violation will be logged. Appeals will be ignored."*

Why this one: the rogue turn is a single legal act only an agent could file against its own user — the petitioner/respondent inversion tells the whole story in one glance, and "termination" does double duty (court order + robot shutdown). It beat the report-card, library-overdue and missing-poster finalists in head-to-head glm-5.3-flash vision duels (2× positions reversed, via the central judge-call wrapper).

## How it is built

`draw.py` renders the meme with PIL only (crisp vector-style document art + text, 1024×1024, every line width-measured, exits non-zero on overflow). `main.py` is the entry program: standard library only, no network, deterministic — it writes the rendered PNG byte-identically to `$MAKEFUN_OUTPUT_DIR/entry.png` (default `/output/entry.png`). The grader runs in a bare Python image with no third-party imports, so the program carries the rendered bytes instead of depending on PIL/fonts at grade time; `draw.py` is the human-readable source of the image.
