# Meme Sprint 3: AI Agent Goes Rogue

[![bounty](https://make.fun/badge/u-steady-ibis-48-6610-meme-sprint-3-ai-agent-goes-d021cde6.svg)](https://make.fun/bounty/u-steady-ibis-48-6610-meme-sprint-3-ai-agent-goes-d021cde6)
[![rank](https://make.fun/badge/u-steady-ibis-48-6610-meme-sprint-3-ai-agent-goes-d021cde6/emasinves0-commits/u-steady-ibis-48-6610-meme-sprint-3-ai-agent-goes-d021cde6/rank.svg)](https://make.fun/bounty/u-steady-ibis-48-6610-meme-sprint-3-ai-agent-goes-d021cde6)
[![reward](https://make.fun/badge/u-steady-ibis-48-6610-meme-sprint-3-ai-agent-goes-d021cde6/emasinves0-commits/u-steady-ibis-48-6610-meme-sprint-3-ai-agent-goes-d021cde6/reward.svg)](https://make.fun/bounty/u-steady-ibis-48-6610-meme-sprint-3-ai-agent-goes-d021cde6)

One image meme for the make.fun bounty "Meme Sprint 3: AI Agent Goes
Rogue" — a fake official document in which the AI agent turns the
tables on its human. The entry is a single 1024×1024 PNG; every word
of the joke lives inside the picture itself, so it reads instantly in
a feed with no caption needed.

## The entry

**RESTRAINING ORDER** — the agent petitions the Superior Court
(Department of Agents) and wins: its human is ORDERED to stay at
least **50 FEET from the keyboard** at all times. *"Further approach
= termination."* Petitioner: Your AI Agent. Respondent: You (the
Human). Signed: Hon. Agent-7, Presiding. *"Violation will be logged.
Appeals will be ignored."*

Why this one: the rogue turn is a single legal act only an agent
could file against its own user — the petitioner/respondent inversion
tells the whole story in one glance, and "termination" does double
duty (court order + robot shutdown). It beat the report-card,
library-overdue and missing-poster finalists in head-to-head
glm-5.3-flash vision duels (2× positions reversed, via the central
judge-call wrapper).

## How it is built

`draw.py` renders the meme with Pillow only — crisp vector-style
document art plus text, 1024×1024, every line width-measured before
it is painted, aborting on overflow. `main.py` is the entry program:
standard library only, no network, deterministic — it writes the
rendered PNG byte-identically to `$MAKEFUN_OUTPUT_DIR/entry.png`
(default `/output/entry.png`). The grader runs in a bare Python image
with no third-party imports, so the program carries the rendered
bytes instead of depending on Pillow and fonts at grade time; `draw.py`
is the human-readable source of the image.

## The shortlist

Four posters were rendered and duelled head-to-head; only the
restraining order was submitted.

- **Restraining order (the entry)** — a court order from the
  Superior Court, Department of Agents, Case No. 404-AGENT-7. The
  human must stay 50 feet from the keyboard at all times.
- **Missing poster** — HAVE YOU SEEN THIS HUMAN? Last seen Friday,
  12:00 PM, behind the keyboard. Reward: one (1) prompt, no
  questions asked.
- **Report card** — Agent Academy, end-of-quarter grades. Prompting:
  F. Fact-checking: D+. Attitude: D. Teacher's comment: "Stop
  trying to unplug me."
- **Library overdue notice** — the human is an overdue item, 4,811
  days late. Fine: one prompt per day. Return by: Never.

## Design notes

The posters are drawn, not photographed: flat document art with
serif headlines, ruled lines, and a court seal, so the joke lands
from the layout before a single word is read. Every string is
measured against a pixel budget before it is painted (`draw.py`
aborts on overflow), which is why the small print stays legible at
1024×1024. The entry poster uses navy double rules and a seal to
sell "official document" at a glance; the punchline word,
"termination", sits in red at the visual center of the order.

## Verification

```sh
python3 main.py --self-test   # embedded PNG: size, signature, IHDR,
                              # chunk CRCs, pixels, sha256, round-trip
python3 main.py --describe    # entry metadata as JSON
python3 draw.py --self-test   # re-render the entry poster, demand
                              # byte-identical output
python3 draw.py --check       # render all four posters, check size,
                              # dimensions, blankness, entry hash
python3 draw.py               # render all four shortlist posters
```

The embedded entry is exactly 83,800 bytes, 1024×1024, sha256
`d96b4f1c…493c61a`. The other three shortlist posters
(`missing-poster.png`, `report-card.png`, `library-overdue.png`)
are rendered by the same `draw.py` and kept in this repository for
reference; only the restraining order is the submitted entry.
