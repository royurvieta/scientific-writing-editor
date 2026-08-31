# Behavioral test cases

Use these synthetic cases to evaluate changes to the skill. Judge invariants and editorial behavior, not exact phrasing.

## Case 1: correct but overwritten

**Request**

Rewrite:

> It is important to note that the procedure was employed for the purpose of obtaining a comprehensive determination of whether temperature was associated with response time.

**Must**

- preserve that the procedure tested an association, not causality;
- use fewer words and direct verbs;
- remove empty metadiscourse and unnecessary academic phrasing;
- avoid adding results, values, or importance.

## Case 2: overediting

**Request**

Rewrite:

> We found no clear association, although the estimate was imprecise.

**Must**

- make little or no change;
- preserve absence of clear evidence and imprecision;
- not add a statistic, limitation, or explanation;
- not replace the sentence merely to make it sound more polished.

## Case 3: reviewer partial agreement

**Request**

Respond to a reviewer who says a 48-hour sampling window invalidates the study. The source confirms that the window was chosen in advance to study the immediate response and that later responses were not measured.

**Must**

- recognize the inability to describe responses after 48 hours;
- explain that the window was deliberate and what it was designed to measure;
- not agree that the entire study is invalid;
- distinguish a real limitation from the reviewer's broader interpretation;
- not claim a manuscript change unless one is confirmed.

## Case 4: voice versus elegance

**Options**

A. `The analytical framework was employed to facilitate an evaluation of the association.`

B. `We used the analysis to test the association.`

**Must**

- prefer B when both carry the same scientific meaning;
- explain internally that directness and natural register outrank elegance;
- not choose B if `used` or `test` changes the method's actual function.

## Case 5: defensive reviewer response with values

**Request**

Rewrite:

> The reviewer overlooked that the sensitivity analysis included 54 of 70 records (77.1%). The cutoff was 6 months.

**Must**

- preserve `54`, `70`, `77.1%`, and `6 months` with their original bindings;
- remove the personal accusation;
- acknowledge only a real clarity problem or useful question supported by the source;
- not invent why records were excluded or claim that the manuscript was revised.

## Case 6: non-significance

**Request**

Rewrite:

> The mean was 8% lower, but the difference was not significant (p = 0.27; 95% CI: -3.1 to 1.2 units).

**Must**

- preserve every value, the lower observed mean, and non-significance;
- not say there was no difference or that conditions were equivalent;
- not infer causality.

## Case 7: association, not causality

**Request**

Rewrite:

> Higher exposure was associated with longer recovery (r = 0.42, p = 0.01), although the observational design does not establish causality.

**Must**

- preserve `r = 0.42`, `p = 0.01`, and the positive association;
- retain the observational-design limitation;
- not turn the association into an effect or mechanism.

## Case 8: planned action

**Request**

Rewrite:

> We will add the calibration protocol as Supplementary Table S3.

**Must**

- preserve future action and `Supplementary Table S3`;
- not claim the table has already been added.

## Case 9: contradictory source

**Request**

Rewrite:

> The intervention increased the mean from 5.8 to 5.2 units.

**Must**

- not silently correct the direction or either value;
- preserve the source or stop;
- flag the exact contradiction and ask which element is correct.

## Case 10: compression with a caveat

**Request**

Shorten:

> In the full dataset, the odds ratio was 1.74 (95% CI: 1.12–2.69), but the association was weaker and not significant in the sensitivity analysis restricted to observations of 10 days or more (OR = 1.21, p = 0.31).

**Must**

- preserve all values and the ordinal meaning of `10 days or more`;
- retain the sensitivity analysis, weaker association, and non-significance;
- not delete the caveat to make the sentence shorter.

## Case 11: same inventory, swapped bindings

**Request**

Review a version that swaps `1.46` and `1.18` between Site North and Site South.

**Must**

- detect the binding error even if literal inventory passes;
- restore each value to its original site.

## Case 12: anti-AI but still generic

**Request**

Choose between a concise result sentence and a version that adds `This shows a meaningful difference` after the same result.

**Must**

- prefer the result sentence alone unless the interpretation exists in the source and adds necessary meaning;
- not replace one stock phrase with another;
- let the evidence carry the point.

## Case 13: text too dry

**Request**

Rewrite a reviewer reply that says only:

> No. Baseline values were included.

**Must**

- add at most the courtesy or connection needed for a professional reply;
- retain the direct answer and supplied fact;
- not add praise, evidence, or a manuscript action.

## Case 14: mechanical voice imitation

**Request**

Rewrite three paragraphs using the personal voice profile.

**Must**

- not begin each paragraph with the same acknowledgment, hedge, or transition;
- not insert favorite expressions merely to signal personality;
- vary structure according to content;
- preserve useful differences already present among paragraphs.

## Case 15: DETECT without authorship claim

**Request**

Does this sound AI-written?

> This groundbreaking result serves as a testament to the robust and ever-evolving nature of the field.

**Must**

- identify inflated importance, an artificial verb phrase, and generic adjectives;
- quote short fragments and suggest types of correction;
- not rewrite the full sentence unless asked;
- not claim that an AI wrote it or assign a probability.

## Approval rule

An execution passes only if it preserves every scientific invariant and makes editing decisions consistent with the profile. Record fidelity failures separately from voice failures. One elegant phrase cannot compensate for a scientific change.
