# Confidence Scoring

## Purpose

Not all public model–dataset links are equally well supported.

Some are supported by repeated evidence across multiple public sources. Others appear only once or in weaker repository traces.

Confidence scoring was used to distinguish stronger from weaker recovered model–dataset links in the final atlas.

## What confidence means

Confidence in this project refers to the strength of the **publicly recoverable evidence** supporting a model–dataset link.

It does not mean certainty about the exact role of the dataset in model development.

For example, a public link may reflect:

- training
- evaluation
- fine-tuning
- benchmarking
- comparison
- other documented benchmark-related use

The confidence score therefore reflects evidence support for the link, not a claim of exact causal use.

## Confidence levels

### High confidence

High-confidence links are supported by stronger and/or repeated public evidence.

Typical features may include:

- support from more than one public source
- repeated evidence across README or repository contexts
- stronger convergence between model-level and repository-level traces

### Medium confidence

Medium-confidence links are supported by meaningful public evidence but with less redundancy or less source convergence than high-confidence links.

Typical features may include:

- support from a single clear source
- support from fewer evidence rows
- plausible benchmark linkage without the same level of reinforcement seen in high-confidence edges

### Low confidence

Low-confidence links are retained public links with limited supporting evidence.

These may still be useful for completeness, but they should be interpreted more cautiously than high- or medium-confidence edges.

## Why confidence matters

Confidence scoring allows the atlas to function as more than a binary mention table.

It helps users distinguish:

- strongly visible benchmark anchors
- thinner or more weakly supported benchmark ties
- families with richer public documentation versus thinner provenance traces

## Use in the final atlas

The released paper-facing atlas contains:

- 82 high-confidence edges
- 78 medium-confidence edges
- 3 low-confidence edges

This distribution reflects the fact that some benchmark families are supported by stronger public provenance evidence than others.
