# Scientific Writing Editor

[![CI](https://github.com/royurvieta/scientific-writing-editor/actions/workflows/ci.yml/badge.svg)](https://github.com/royurvieta/scientific-writing-editor/actions/workflows/ci.yml)

A bilingual agent skill for editing scientific and technical writing without changing the science.

It rewrites English or Spanish text, prepares reviewer responses, and audits AI-style writing patterns while protecting numbers, statistics, units, comparisons, limitations, certainty, and scientific interpretation. It aims to preserve the author's own voice instead of replacing it with polished generic prose.

## What makes it different

- **Evidence ledger:** binds every value to its variable, group, unit, denominator, and comparison before editing.
- **Scientific guardrails:** prevents association from becoming causality, trends from becoming effects, and non-significance from becoming equivalence.
- **Action-status protection:** keeps `we will revise`, `we revised`, and `we propose to revise` distinct.
- **Exact-wording protection:** can verify that reviewer quotes and manuscript replacements stayed literal.
- **Binding alarm:** flags values that may have moved to a different subject or comparison even when the numeric inventory still matches.
- **Contextual anti-slop pass:** removes filler without banning scientifically necessary passive voice, contrast, repetition, or technical terms.
- **Personal-voice layer:** models editorial decisions—what to keep, remove, simplify, or reorder—without inserting favorite phrases mechanically.
- **Minimal intervention:** leaves strong sentences alone and treats elegance as lower priority than meaning, clarity, and the author's natural register.
- **Bilingual workflow:** edits natural scientific English and Spanish rather than translating syntax mechanically.

## Modes

- `REWRITE`: minimal, source-faithful editing.
- `REVIEWER RESPONSE`: point-by-point peer-review replies with confirmed manuscript changes and protected exact wording.
- `DETECT`: observable style findings without a rewrite, score, or authorship claim.

## Install

With the Skills CLI:

```bash
npx skills add royurvieta/scientific-writing-editor --skill scientific-writing-editor --global --yes
```

Manual Codex installation:

```bash
git clone https://github.com/royurvieta/scientific-writing-editor.git
cp -R scientific-writing-editor/skills/scientific-writing-editor ~/.codex/skills/
```

Release archives include:

- `scientific-writing-editor-codex.zip`: contains the named skill folder.
- `scientific-writing-editor-claude.zip`: places `SKILL.md` at the archive root.

## Use

```text
Use $scientific-writing-editor to rewrite this response to Reviewer 2. Preserve every statistic and keep the quoted manuscript changes exact.
```

```text
Use $scientific-writing-editor to translate this Results paragraph into natural scientific English without changing certainty, comparisons, or terminology.
```

```text
Use $scientific-writing-editor in DETECT mode. Name the artificial writing patterns, but do not rewrite or guess authorship.
```

## Fidelity checker

For same-language text files:

```bash
python3 skills/scientific-writing-editor/scripts/check_fidelity.py source.txt rewrite.txt --bindings
```

Add `--protect-quotes` when quoted wording must remain literal. The checker is an alarm, not a semantic proof; its output still requires review.

All scientific scenarios and values included in the distributed examples and behavioral tests are synthetic.

## Test and build

```bash
python3 -m unittest discover -s tests -v
python3 scripts/build_packages.py dist
unzip -t dist/scientific-writing-editor-codex.zip
unzip -t dist/scientific-writing-editor-claude.zip
```

## License and attribution

This project is released under the MIT License. Its anti-slop editing principles adapt ideas from Peter Yang's [`no-ai-slop`](https://github.com/petergyang/no-ai-slop), also MIT-licensed. See [THIRD_PARTY_NOTICES.md](THIRD_PARTY_NOTICES.md).
