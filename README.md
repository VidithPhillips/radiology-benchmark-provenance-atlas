# Public Radiology AI Benchmark Provenance Atlas

A public resource linking open radiology AI models to canonical benchmark datasets using evidence recovered from Hugging Face and GitHub.

## Overview

Public radiology AI models often mention datasets inconsistently across model cards, repository READMEs, and other public files. This makes it hard to understand which benchmark datasets actually anchor the visible open-model ecosystem.

This repository releases a benchmark-centered atlas of model–dataset provenance links for open radiology AI. The atlas was built by collecting public radiology AI models and repositories, normalizing benchmark dataset aliases, mining public text evidence across platforms, and assigning confidence scores to recovered model–dataset links.

The project is intended as both:

- a research resource for studying benchmark concentration and reuse in open radiology AI
- a practical lookup tool for navigating public model–dataset links

## Current atlas snapshot

The current paper-facing atlas contains:

- **117** public models
- **18** canonical or derived radiology benchmark datasets
- **163** final atlas edges
- **82** high-confidence edges
- **78** medium-confidence edges
- **3** low-confidence edges

### Dominant benchmark families in the final atlas

- **MIMIC family**
- **CheXpert family**
- **MRI family**
- **RadGraph family**

Secondary families include CT, mammography, VinDr, RaDialog, and other benchmark groupings.

## Released files

The main released files are located in `data/release/`.

### Main paper tables

- `table1_family_summary.csv`  
  Benchmark family composition of the final atlas

- `table2_dataset_summary.csv`  
  Canonical datasets represented in the final atlas

### Supplementary tables

- `supplementary_table_s1_full_atlas_edge_list.csv`  
  Full atlas edge list for the final paper atlas

- `supplementary_table_s2_model_registry_in_atlas.csv`  
  Model registry for all models represented in the final atlas

### Workbook

- `atlas_tables_for_manuscript.xlsx`  
  Consolidated workbook containing the main manuscript tables and supplementary atlas tables

## What this resource contains

This repository currently provides four main outputs:

1. **Canonical benchmark registry logic**  
   A benchmark-centered representation of radiology datasets organized into canonical datasets, derived resources, and broader benchmark families.

2. **Model registry**  
   A list of public models included in the final atlas.

3. **Evidence-scored atlas edge list**  
   Model–dataset links recovered from public sources and labeled by confidence and evidence type.

4. **Family-level and dataset-level summaries**  
   Aggregated views of the final atlas for manuscript reporting and downstream reuse.

## High-level method

The atlas was built using a multi-step public-source pipeline:

1. Build a radiology benchmark registry
2. Normalize canonical dataset names and aliases
3. Harvest radiology-relevant public models and repositories
4. Extract public text evidence from Hugging Face and GitHub
5. Match benchmark aliases in model cards, READMEs, and repository files
6. Aggregate evidence into candidate model–dataset links
7. Assign confidence scores based on evidence strength and source combinations
8. Collapse links into a benchmark-centered final atlas
9. Summarize the atlas at family and dataset level

A concise methods description is provided in [`docs/methods_overview.md`](docs/methods_overview.md).

## Repository structure

```text
radiology-benchmark-provenance-atlas/
├── data/
│   └── release/
├── docs/
├── figures/
├── notebooks/
├── src/
└── app/
