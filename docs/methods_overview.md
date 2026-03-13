# Methods Overview

## Purpose

The goal of this project is to recover and organize public model–dataset provenance links for open radiology AI models across public repositories.

Rather than relying on a single source such as a model card alone, the atlas integrates multiple public evidence sources and contracts them into a benchmark-centered, confidence-scored resource.

## High-level workflow

### 1. Build a radiology benchmark registry

A radiology-relevant benchmark registry was assembled to represent public datasets and related benchmark resources relevant to open radiology AI.

This registry included:

- canonical benchmark datasets
- derived or annotation-related benchmark resources
- community mirrors or reuploads where relevant to public matching

### 2. Normalize dataset aliases

Dataset names in public repositories are often inconsistent. The project therefore defined canonical dataset identities together with alias mappings used for text matching across public sources.

Examples include abbreviation variants, punctuation variants, platform-specific naming, and mirror-specific naming.

### 3. Harvest public radiology AI artifacts

The project collected radiology-relevant public models and repositories from sources including:

- Hugging Face models
- Hugging Face datasets
- GitHub repositories
- PhysioNet-linked benchmark resources

In addition to repositories linked directly from Hugging Face model cards, the project also incorporated GitHub-first repository expansion.

### 4. Mine public text evidence

Public text evidence was extracted from multiple locations, including:

- Hugging Face model metadata
- Hugging Face model card README text
- GitHub repository README text
- candidate GitHub repository files and top-level text files

This multi-source approach improved recovery beyond any one platform alone.

### 5. Recover candidate model–dataset links

The normalized alias library was used to detect benchmark mentions in recovered public text.

These matches were then aggregated into candidate model–dataset links.

### 6. Score evidence

Each candidate link was scored based on the amount and type of supporting evidence recovered from public sources.

Evidence scoring incorporated factors such as:

- number of supporting evidence rows
- whether support came from one versus multiple public sources
- whether support came from metadata, README text, or repository file text

### 7. Collapse to unique atlas edges

Candidate evidence rows were aggregated into unique model–dataset edges. These were assigned confidence labels and then summarized across benchmark families and canonical datasets.

### 8. Build the final paper atlas

The broader public crawl was contracted into a stricter benchmark-centered paper atlas by prioritizing canonical and derived benchmark nodes and reducing inflation from mirrors or community reuploads.

## Final released atlas

The current paper-facing atlas contains:

- 117 models
- 18 canonical or derived datasets
- 163 atlas edges

These edges are distributed across benchmark families including MIMIC, CheXpert, MRI, RadGraph, CT, mammography, VinDr, RaDialog, and other datasets.

## Interpretation

This atlas should be interpreted as a map of **publicly recoverable provenance evidence** for benchmark-linked open radiology AI models.

It is intended to support both:

- empirical study of benchmark concentration and structure
- practical lookup of public model–dataset relationships
