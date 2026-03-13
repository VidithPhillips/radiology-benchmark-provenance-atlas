# Benchmark Tiering

## Why tiering is needed

Public dataset references in open repositories are noisy.

The same benchmark may appear as:

- a canonical dataset
- a derived annotation resource
- a rehosted copy
- a mirror
- a community-uploaded variant

If all of these are treated as equally important atlas nodes, the resulting map becomes inflated and harder to interpret. Benchmark tiering was therefore used to preserve canonical structure while still capturing useful public linkage evidence.

## Tier definitions

### Tier 1 — Canonical benchmarks

Tier 1 represents primary benchmark datasets that function as core reference datasets in the public radiology AI ecosystem.

These are the main benchmark nodes that should anchor the atlas.

Examples include:

- MIMIC-CXR Database
- CheXpert
- fastMRI
- BraTS
- LIDC-IDRI
- PadChest
- ChestX-ray14
- OASIS
- INbreast
- MIAS
- VinDr-CXR
- VinDr-Mammo

### Tier 2 — Derived or annotation resources

Tier 2 represents benchmark-related resources that are derived from, layered on top of, or tightly coupled to canonical datasets.

These resources may still function as meaningful atlas nodes because they support important public model development, evaluation, or task-specific benchmark use.

Examples include:

- RadGraph
- RadGraph-XL
- MS-CXR
- RaDialog Instruct

### Tier 3 — Community mirrors or reuploads

Tier 3 includes community mirrors, reuploads, platform-specific copies, and other public variants that can be useful for evidence recovery but should not typically be treated as equal to canonical benchmark nodes in the main atlas.

These entries were useful during the public matching process but were not intended to dominate the benchmark-centered final representation.

## How tiering was used in the project

The broader public crawl used the full registry to improve recovery of public evidence.

The stricter paper-facing atlas then prioritized:

- Tier 1 canonical benchmarks
- Tier 2 derived or annotation resources

This allowed the final atlas to remain benchmark-centered while reducing distortion from mirror inflation.

## Practical effect

Tiering helps the atlas answer the intended question:

**Which benchmark datasets actually anchor the public radiology AI ecosystem?**

rather than the looser question:

**Which dataset-like strings happen to appear in public repositories?**
