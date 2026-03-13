# Limitations

This repository captures **publicly recoverable provenance evidence** for open radiology AI models. It should not be interpreted as a complete ground-truth map of all dataset usage in radiology AI.

## 1. Public evidence is incomplete

Some models may use benchmark datasets without clearly documenting them in public model cards, READMEs, or repository files. Others may document them only partially.

As a result, absence of a link in the atlas should not be interpreted as proof of absence of dataset use.

## 2. Public links do not always specify role

A model–dataset link may reflect different kinds of use, including:

- training
- evaluation
- fine-tuning
- benchmarking
- comparison
- documentation or reporting context

The current atlas is therefore best interpreted as a benchmark provenance resource rather than a strict training-data registry.

## 3. Alias matching depends on public naming

Although the project uses canonical naming and alias normalization, public references remain noisy. Ambiguity, abbreviation, and inconsistent naming can affect recovery.

## 4. Platform coverage is selective

The current atlas was built from selected public sources, especially Hugging Face and GitHub, with supporting benchmark/resource inputs. It does not capture every public radiology AI artifact on the internet.

## 5. Community mirrors can inflate raw public traces

Public mirrors and reuploads can distort the apparent shape of the ecosystem if not collapsed carefully. This is why benchmark tiering was used to preserve a cleaner benchmark-centered atlas.

## 6. The atlas is a living resource

As public repositories evolve, benchmark links, models, and documentation may change. The atlas should therefore be understood as a versioned public snapshot rather than a permanent final state.
