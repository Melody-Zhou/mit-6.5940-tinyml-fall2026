# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

Personal solutions to the labs of **MIT 6.5940: TinyML and Efficient AI Computing (Fall 2026)**. The repository is a learning record: completed lab notebooks, official lab scaffolding, and links to lecture notes. The README is the public index; the notes themselves live on CSDN.

- Course: https://hanlab.mit.edu/courses/2026-fall-65940
- Course alias: https://efficientml.ai
- Local GPU: NVIDIA RTX 4060
- At the time of writing: Lab 0 is complete (92.62% CIFAR-10 test accuracy); Lab 1 is in progress. The README is the source of truth for lab status.

## Repository Structure

```text
.
├── lab0/
│   └── lab0.ipynb                 # Completed; outputs and 92.62% result preserved
├── lab1_gpu_basics/
│   ├── README.md                  # Official course handout; do not edit
│   ├── lab1.ipynb                 # Working notebook; complete in place
│   ├── assets/                    # Official figures; do not edit
│   └── utils/                     # Official helper code; do not edit
├── .gitignore
├── LICENSE
└── README.md                      # Public index: labs, notes, setup, references
```

## Working Rules

- **One notebook per lab.** Keep only the working/completed notebook (`labN_<topic>/labN.ipynb` or `lab0/lab0.ipynb`). Do not add pristine course templates, duplicate solution copies, or `*_impl.ipynb` files.
- **Edit the official notebook in place.** Keep the course markdown, question numbering, and instructions. Replace `# YOUR CODE HERE` / `raise NotImplementedError()` cells and fill the `Your Answer:` prompts with measured results.
- **Keep notebook outputs.** Completed notebooks retain execution outputs and plots; they document results (Lab 0 is ~600 KB for this reason). Do not strip outputs.
- **Do not modify course-provided files** (`lab1_gpu_basics/README.md`, `utils/`, `assets/`) unless a task explicitly requires it. Put solutions in the notebook.
- **Run Lab 1 from `lab1_gpu_basics/`.** The notebook does `sys.path.insert(0, '.')` and loads `./assets/*.png`; starting Jupyter in that directory is required.
- **Lab 0 keeps its official Colab setup cells.** The Google Drive mount and `pip install` cells are intentionally unexecuted locally; do not delete them just to run the notebook locally. Skip them instead.
- **Update the README when a lab changes state.** Keep the Labs table status, notebook link, and accuracy/result current. Add new labs as their own `labN_<topic>/` directory with one notebook.
- **Notes are external.** Lecture notes are on CSDN (linked from the README); do not vendor them into the repository.
- **English in README**; notebook content is the course's English. Notes links may point to Chinese posts.
- **AI disclosure stays.** The README states that the work was developed with Claude Code assistance and is for learning/reference only. Do not remove it.
- **No root `requirements.txt`.** The official Lab 1 README is the dependency source of truth; do not create a duplicate root dependency file unless the user asks.

## Environment and Commands

Lab 1 requires a CUDA-enabled PyTorch 2.x environment. Pinned dependencies from the official handout:

```bash
conda install nvidia::cuda-nvcc==12.4.99
pip install "transformers==4.57.6" "tokenizers==0.22.2" \
            "huggingface_hub==0.36.2" "accelerate==1.11.0"

# Optional, Part 5 only:
pip install --no-build-isolation flash-attn
```

Run the local notebook:

```bash
cd lab1_gpu_basics
jupyter lab lab1.ipynb    # or: jupyter notebook lab1.ipynb
```

Lab 0 dependencies: PyTorch/torchvision, `torchprofile`, `tqdm`, and `matplotlib`. CIFAR-10 downloads automatically to `data/cifar10` and is gitignored.

Notes:

- The default shell may not have `torch` installed; use the environment configured in the notebook kernel.
- Lab 1 exports `trace.json` via `prof.export_chrome_trace("trace.json")`; it is gitignored.
- On the local RTX 4060, `flash-attn` may need to compile from source. The Colab notebook variant is not tracked; if an A100 is needed, re-download the official handout or restore the backup.

## Git and Ignore Rules

- Do not commit or push unless the user asks.
- Keep the repository clean: one notebook per lab, no duplicate handouts, no archived course templates.
- `.gitignore` intentionally ignores runtime artifacts (`trace.json`, `data/cifar10`, model weights, `*.zip`, caches, environments) but **must not ignore** course sources: `lab*/lab*.ipynb`, `lab1_gpu_basics/utils/**`, `assets/**`, lab READMEs, the root README, and `LICENSE`.
- Do not add broad ignores for `data/`, `models/`, `utils/`, or `*.png`; future labs may ship source or data under those names.
- `*.zip` is ignored because extracted course handouts are tracked. Do not commit archives.

## Verification

Before claiming a repository task is complete:

```bash
# Repository state and notebook presence
git status --short
find . -path ./.git -prune -o -type f -print | sort

# Validate notebook JSON and expected cell counts
python3 - <<'PY'
import json
for rel, cells in [('lab0/lab0.ipynb', 55), ('lab1_gpu_basics/lab1.ipynb', 104)]:
    nb = json.load(open(rel))
    assert len(nb['cells']) == cells, (rel, len(nb['cells']))
    print('OK', rel, len(nb['cells']), 'cells')
PY

# Confirm runtime artifacts are ignored and course sources are not
git check-ignore -v lab1_gpu_basics/trace.json lab0/data/cifar10/x
if git check-ignore -q README.md lab1_gpu_basics/lab1.ipynb; then
  echo 'ERROR: course source is ignored'
fi
```

For README edits, verify that relative links resolve and that the `## Labs` and `## Notes` anchors still exist. For notebook work, execute the affected cells end-to-end on the local GPU and report actual results or failures.
