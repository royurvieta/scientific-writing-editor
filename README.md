# Scientific Writing Editor

[![CI](https://github.com/royurvieta/scientific-writing-editor/actions/workflows/ci.yml/badge.svg)](https://github.com/royurvieta/scientific-writing-editor/actions/workflows/ci.yml)
[![Release](https://img.shields.io/github/v/release/royurvieta/scientific-writing-editor)](https://github.com/royurvieta/scientific-writing-editor/releases/latest)
[![License: MIT](https://img.shields.io/badge/License-MIT-blue.svg)](LICENSE)

Edit scientific and technical writing without changing the science—or replacing the author with a generic professional voice.

`scientific-writing-editor` is a reusable agent skill for English and Spanish manuscripts, reviewer responses, reports, and technical explanations. It protects data, statistical meaning, uncertainty, comparisons, limitations, and editorial action status while making the prose clearer, shorter, and more natural.

It is built for researchers and technical authors who want careful editing, not a “humanizer” that simply swaps formal words for casual ones.

## A quick example

**Before**

> It is important to highlight that response time was 18% lower at Site B than at Site A (p = 0.04), thereby providing valuable insight into meaningful differences between the two sites.

**After**

> Response time was 18% lower at Site B than at Site A (p = 0.04).

The rewrite removes empty emphasis and an unsupported interpretation. It keeps the value, direction, sites, comparison, and `p` value exactly where they belong.

All examples and values in this repository are synthetic.

## Why this skill exists

Ordinary rewriting tools often improve fluency by quietly changing scientific meaning. Common failures include:

- moving a value to the wrong variable, group, or comparison;
- turning an association into causality;
- turning a trend into a confirmed effect;
- rewriting non-significance as “no difference” or equivalence;
- removing a limitation because the paragraph reads better without it;
- changing `we will revise` into `we revised`;
- inventing relevance, novelty, mechanisms, citations, or manuscript changes;
- replacing the author's voice with polished but generic academic prose.

This skill treats those changes as errors, not stylistic improvements.

## The core promise

The source is the authority. The skill preserves:

- numbers, decimals, signs, percentages, counts, ranges, thresholds, times, doses, and units;
- statistics, intervals, `p` values, significance, non-significance, adjustments, and uncertainty;
- the variable, subject, group, denominator, condition, and comparison attached to each value;
- direction and magnitude of effects, associations, trends, and differences;
- population, scope, limitations, exceptions, causal boundaries, and degree of certainty;
- names, citations, labels, terminology, and table or figure references;
- whether an editorial action is proposed, planned, completed, or declined.

When style and scientific meaning compete, meaning wins.

## Three modes

| Mode | Use it for | Default output |
| --- | --- | --- |
| `REWRITE` | Editing, shortening, translating, or improving a draft | A minimally edited, source-faithful version |
| `REVIEWER RESPONSE` | Point-by-point peer-review replies | A cordial, direct response with evidence and accurate revision status |
| `DETECT` | Auditing AI-style or artificial writing patterns | Observable findings with short quotations, without rewriting or guessing authorship |

## What the editing looks like

### 1. Academic wording becomes direct wording

**Before**

> The analytical procedure was employed for the purpose of determining whether an association existed between exposure duration and signal loss.

**After**

> We used the analytical procedure to test whether exposure duration was associated with signal loss.

The edit uses simpler verbs but preserves `association`. It does not introduce an effect or mechanism.

### 2. Non-significance stays non-significance

**Before**

> The adjusted mean was 9% lower, although the difference was not statistically significant (p = 0.21; 95% CI: -2.8 to 0.7 units), and the result should therefore be interpreted cautiously.

**After**

> The adjusted mean was 9% lower, but the difference was not statistically significant (p = 0.21; 95% CI: -2.8 to 0.7 units).

The result becomes shorter without becoming “no effect.” Direction, non-significance, interval, and uncertainty remain intact.

### 3. A reviewer can be partly right

**Context**

> A reviewer argues that a 24-hour observation window makes the entire study unreliable. The window was selected in advance to evaluate the immediate response, but later events were not measured. The Methods were revised to state this limit.

**Response**

> We recognize that the 24-hour window does not capture later events. This window was selected in advance to evaluate the immediate response. We have clarified that the results should not be interpreted beyond 24 hours.

The response recognizes the real limitation without accepting the broader unsupported conclusion. It also distinguishes a deliberate methodological choice from an accidental omission.

### 4. Spanish becomes natural, not casual

**Before**

> Cabe destacar que el procedimiento fue implementado con el objetivo de evaluar la posible asociación entre el tiempo de exposición y la pérdida de señal.

**After**

> Usamos el procedimiento para evaluar la posible asociación entre el tiempo de exposición y la pérdida de señal.

La versión elimina una apertura vacía y una construcción inflada. Mantiene `posible asociación` y no agrega causalidad.

More synthetic examples are available in [references/examples.md](skills/scientific-writing-editor/references/examples.md).

## Personal voice without imitation

The skill does not reproduce a person's voice by inserting favorite expressions, recurring sentence openings, or informal phrases. Personal voice is treated primarily as a pattern of editorial decisions:

- what should remain unchanged;
- what can be removed without losing meaning;
- which word is simpler but equally precise;
- when a long sentence works and should be kept;
- when evidence should appear before interpretation;
- how much courtesy a reviewer response actually needs;
- when an imperfect human sentence is better than a polished generic one.

The target is not “better than the author.” It is the same author on a very good writing day.

See the complete [personal voice profile](skills/scientific-writing-editor/references/personal-voice.md).

## Priority order

When objectives conflict, the skill uses this order:

1. scientific fidelity;
2. logical accuracy;
3. preservation of interpretation and uncertainty;
4. clarity;
5. brevity;
6. personal voice;
7. elegance.

Elegance is deliberately last. A smoother sentence is not an improvement if it changes the science.

## How it works

For each rewrite, the skill:

1. builds a private ledger of claims, values, comparisons, uncertainty, limitations, and action status;
2. protects exact quotations and manuscript wording when required;
3. diagnoses the actual writing problem before changing anything;
4. makes the minimum effective edit;
5. removes empty AI-style patterns only when they serve no scientific or logical function;
6. calibrates the result to the author's register and the source language;
7. validates scientific fidelity and personal voice separately.

The private ledger is not shown unless requested.

## Install

### Skills CLI

```bash
npx skills add royurvieta/scientific-writing-editor --skill scientific-writing-editor --global --yes
```

### Codex: manual installation

```bash
git clone https://github.com/royurvieta/scientific-writing-editor.git
cp -R scientific-writing-editor/skills/scientific-writing-editor ~/.codex/skills/
```

The installed entrypoint should be:

```text
~/.codex/skills/scientific-writing-editor/SKILL.md
```

### Release archives

The [latest release](https://github.com/royurvieta/scientific-writing-editor/releases/latest) includes:

- `scientific-writing-editor-codex.zip`: contains the named skill folder expected by Codex-style installations;
- `scientific-writing-editor-claude.zip`: places `SKILL.md` at the ZIP root for Claude-compatible packaging.

## Use

### Rewrite scientific text

```text
Use $scientific-writing-editor in REWRITE mode. Make the minimum effective edit. Preserve every number, comparison, limitation, and degree of certainty.

[paste text]
```

### Prepare a reviewer response

```text
Use $scientific-writing-editor in REVIEWER RESPONSE mode. Keep the tone cordial and direct. Distinguish a clarity problem from a scientific concession, and do not claim manuscript changes that are not confirmed.

[paste reviewer comment and draft response]
```

### Translate into natural scientific English

```text
Use $scientific-writing-editor to translate this passage into natural scientific English. Preserve all terminology, values, comparisons, uncertainty, and interpretation.

[paste text]
```

### Audit without rewriting

```text
Use $scientific-writing-editor in DETECT mode. Identify observable artificial-writing patterns with short quotations. Do not rewrite, score the text, or infer authorship.

[paste text]
```

## Fidelity checker

The bundled checker compares two same-language text files:

```bash
python3 skills/scientific-writing-editor/scripts/check_fidelity.py source.txt rewrite.txt --bindings
```

Use quote protection when exact wording must remain literal:

```bash
python3 skills/scientific-writing-editor/scripts/check_fidelity.py source.txt rewrite.txt --bindings --protect-quotes
```

The checker can flag:

- missing, added, or changed numeric literals;
- changed units, percentages, statistical markers, and labels;
- values that may have moved to a different nearby subject;
- altered protected quotations.

It is an alarm, not a proof of semantic equivalence. It cannot determine whether a scientifically valid interpretation became invalid, and literal matching is not sufficient for translation across languages. Those cases still require semantic review.

## What this skill will not do

It will not:

- recalculate or silently correct suspicious data;
- invent citations, mechanisms, explanations, results, limitations, or implications;
- claim that a revision was completed when it is only planned;
- turn observational evidence into causality;
- remove uncertainty to make a conclusion stronger;
- guarantee that a text was written by a human;
- assign an “AI probability” from writing style;
- rewrite a passage merely because another wording is possible.

If the source is contradictory or ambiguous, the skill preserves the conflict and asks for clarification.

## Project structure

```text
skills/scientific-writing-editor/
├── SKILL.md
├── agents/openai.yaml
├── references/
│   ├── anti-slop-bilingual.md
│   ├── evaluation.md
│   ├── examples.md
│   ├── personal-voice.md
│   ├── reviewer-responses.md
│   └── test-cases.md
└── scripts/
    └── check_fidelity.py
```

- [`SKILL.md`](skills/scientific-writing-editor/SKILL.md) contains the core workflow and fidelity contract.
- [`personal-voice.md`](skills/scientific-writing-editor/references/personal-voice.md) defines the editorial profile.
- [`reviewer-responses.md`](skills/scientific-writing-editor/references/reviewer-responses.md) distinguishes five reviewer-response situations.
- [`anti-slop-bilingual.md`](skills/scientific-writing-editor/references/anti-slop-bilingual.md) documents contextual English and Spanish patterns.
- [`evaluation.md`](skills/scientific-writing-editor/references/evaluation.md) provides the final fidelity and voice review.
- [`test-cases.md`](skills/scientific-writing-editor/references/test-cases.md) contains behavioral evaluation cases.

## Test and build

```bash
python3 -m unittest discover -s tests -v
python3 scripts/build_packages.py dist
unzip -t dist/scientific-writing-editor-codex.zip
unzip -t dist/scientific-writing-editor-claude.zip
```

The automated tests cover public packaging, numerical inventory, value bindings, quote protection, and repository privacy markers. Behavioral cases separately evaluate scientific meaning and editorial judgment.

## Privacy

All scientific scenarios, labels, and values distributed in the README, examples, tests, and release archives are synthetic. Do not add unpublished results, reviewer text, author details, local paths, credentials, or identifiable research fixtures to public examples.

## License and attribution

This project is released under the [MIT License](LICENSE).

Its contextual anti-slop principles adapt ideas from Peter Yang's [`no-ai-slop`](https://github.com/petergyang/no-ai-slop), also MIT-licensed. See [THIRD_PARTY_NOTICES.md](THIRD_PARTY_NOTICES.md) for attribution details.
