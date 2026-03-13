# Data Dictionary

This document describes the released atlas files in `data/release/`.

---

## 1. `table1_family_summary.csv`

Family-level summary of the final paper atlas.

### Columns

- **dataset_family**  
  Benchmark family name

- **canonical_datasets_n**  
  Number of canonical or derived datasets represented in that family in the final atlas

- **n_models**  
  Number of unique models linked to datasets in that family

- **n_edges**  
  Number of atlas edges in that family

- **high_confidence_edges**  
  Number of family edges labeled high confidence

- **medium_confidence_edges**  
  Number of family edges labeled medium confidence

- **low_confidence_edges**  
  Number of family edges labeled low confidence

- **representative_datasets**  
  Example datasets representing the family

---

## 2. `table2_dataset_summary.csv`

Dataset-level summary of the final paper atlas.

### Columns

- **dataset_title**  
  Canonical dataset name

- **dataset_family**  
  Benchmark family containing the dataset

- **dataset_modality**  
  Broad modality category for the dataset

- **benchmark_tier**  
  Tier classification used in the atlas

- **access_type**  
  Access type or public-access grouping used for the dataset

- **n_models**  
  Number of unique linked models

- **n_edges**  
  Number of atlas edges involving this dataset

- **high_confidence_edges**  
  Number of dataset edges labeled high confidence

- **medium_confidence_edges**  
  Number of dataset edges labeled medium confidence

- **low_confidence_edges**  
  Number of dataset edges labeled low confidence

- **confidence_profile**  
  Compact text summary of the confidence distribution for the dataset

- **example_linked_models**  
  Example public models linked to the dataset in the atlas

---

## 3. `supplementary_table_s1_full_atlas_edge_list.csv`

Full model–dataset edge list for the final paper atlas.

### Columns

- **model_id**  
  Unique model identifier used in the atlas

- **platform**  
  Source platform associated with the model or public artifact

- **model_modality**  
  Broad modality category associated with the model

- **dataset_title**  
  Canonical dataset linked to the model

- **dataset_family**  
  Benchmark family for the linked dataset

- **dataset_modality**  
  Broad modality category for the dataset

- **benchmark_tier**  
  Tier assignment for the linked dataset

- **access_type**  
  Access category for the dataset

- **confidence**  
  Confidence label for the recovered model–dataset link

- **evidence_count**  
  Number of supporting evidence rows aggregated into this edge

- **evidence_types**  
  Types of public evidence supporting the link

- **matched_aliases**  
  Dataset aliases or variants matched during evidence recovery

- **model_url**  
  Public URL for the model or main model artifact

- **dataset_url**  
  Public URL for the linked dataset

- **repository_url**  
  Repository URL associated with the model where applicable

---

## 4. `supplementary_table_s2_model_registry_in_atlas.csv`

Registry of models included in the final paper atlas.

### Columns

- **model_id**  
  Unique atlas model identifier

- **platform**  
  Source platform associated with the model

- **model_name**  
  Public model name

- **model_url**  
  Public URL for the model

- **repository_url**  
  Linked repository URL where available

- **model_modality**  
  Broad modality category for the model

- **n_linked_datasets**  
  Number of canonical datasets linked to the model in the final atlas

- **n_edges**  
  Number of final atlas edges involving the model

- **confidence_profile**  
  Summary of confidence levels across the model’s atlas edges

- **linked_datasets**  
  Compact summary of linked canonical datasets

---

## 5. `atlas_tables_for_manuscript.xlsx`

Workbook containing the main manuscript tables and supplementary atlas tables in spreadsheet form.

This file is intended for manuscript preparation, review, and convenient inspection of the released resource.
