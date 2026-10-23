<div align="center">

<h1>MIT 6.5940 · TinyML and Efficient AI Computing</h1>

<p><strong>Fall 2026 · Massachusetts Institute of Technology</strong></p>

<p>
  <a href="https://hanlab.mit.edu/courses/2026-fall-65940">Course Website</a> ·
  <a href="https://efficientml.ai">EfficientML.ai</a> ·
  <a href="https://live.efficientml.ai/">Videos</a> ·
  <a href="#labs">Labs</a> ·
  <a href="#notes">Notes</a>
</p>

<p>
  <img alt="MIT 6.5940" src="https://img.shields.io/badge/MIT-6.5940-8A2BE2?style=flat-square">
  <img alt="Fall 2026" src="https://img.shields.io/badge/Fall-2026-1f6feb?style=flat-square">
  <img alt="Claude Code assisted" src="https://img.shields.io/badge/AI-Claude%20Code-d97757?style=flat-square">
</p>

</div>

## Introduction

Implementation of MIT 6.5940 (**TinyML and Efficient AI Computing**, Fall 2026), taught by Song Han and Shang Yang. This repository contains my lab implementations and links to my lecture notes, developed with assistance from **Claude Code**.

> **Note:** This repository is for **learning and reference purposes** only. It is not affiliated with or endorsed by MIT or the course staff. Implementations may differ from the official solutions; please use them at your own discretion and follow the course's collaboration and AI-use policies.

## Labs

| Lab | Topic | Status | Notebook | Official material |
|:---:|-------|:------:|----------|-------------------|
| 0 | PyTorch tutorial: VGG-11 variant on CIFAR-10 | ✅ Completed · 92.62% test accuracy | [lab0.ipynb](./lab0/lab0.ipynb) | [Colab](https://colab.research.google.com/drive/1PfVYxikSaVpCSD-cnmNLN4l7yx_4odmg) |
| 1 | GPU basics: metrics, roofline, profiling, FlashAttention (80 + 20 bonus) | ✅ Completed · local RTX 4060 | [lab1.ipynb](./lab1_gpu_basics/lab1.ipynb) | [Lab README](./lab1_gpu_basics/README.md) · [Handout](https://www.dropbox.com/scl/fi/y2zmly5aoekmsg7jq4954/lab1_gpu_basics.zip?rlkey=29v29mlm2muvm0c5teleiusvc&st=2xh5vnk3&dl=1) |
| 2 | Pruning | ✅ Completed · NVIDIA A30 | [lab2_pruning.ipynb](./lab2/lab2_pruning.ipynb) | [Colab](https://colab.research.google.com/drive/1-HEcO8qxlbOgccAg6TyuDTOqWt1Jx45W) |
| 3 | Neural architecture search | ✅ Completed | [lab3_nas.ipynb](./lab3/lab3_nas.ipynb) | [Colab](https://colab.research.google.com/drive/1g_o6v2EErRJKZx5pmX3r8dCsInVkVC7h) |
| 4 | Quantization | ⏳ Planned | — | Handout TBA |
| 5 | LLM deployment on a laptop | ⏳ Planned | — | Handout TBA |

Only the working or completed notebook is kept for each lab; pristine course templates are intentionally not tracked. Lab 0 was completed locally, and the official Colab notebook is linked for reference. The Dropbox handout link may expire; the [course website](https://hanlab.mit.edu/courses/2026-fall-65940) is canonical.

## Notes

Unofficial lecture notes (in Chinese) are published in my [CSDN column](https://blog.csdn.net/qq_40672115/category_13216139.html).

| # | Lecture | Notes |
|:---:|---------|:-----:|
| 1 | Introduction | [Read](https://blog.csdn.net/qq_40672115/article/details/165444500) |
| 2 | Basics of Neural Networks | [Read](https://blog.csdn.net/qq_40672115/article/details/165885581) |
| 3 | Pruning and Sparsity (Part I) | [Read](https://blog.csdn.net/qq_40672115/article/details/166129527) |
| 4 | Pruning and Sparsity (Part II) | [Read](https://blog.csdn.net/qq_40672115/article/details/166900887) |
| 5 | Quantization (Part I) | [Read](https://blog.csdn.net/qq_40672115/article/details/167276357) |
| 6 | Quantization (Part II) | [Read](https://blog.csdn.net/qq_40672115/article/details/167691738) |
| 7 | Neural Architecture Search (Part I) | [Read](https://blog.csdn.net/qq_40672115/article/details/167700081) |
| 8 | Neural Architecture Search (Part II) | [Read](https://blog.csdn.net/qq_40672115/article/details/167807879) |
| 9 | Knowledge Distillation | [Read](https://blog.csdn.net/qq_40672115/article/details/168122345) |
| 10 | MCUNet: TinyML on Microcontrollers | [Read](https://blog.csdn.net/qq_40672115/article/details/168434588) |
| 11 | TinyEngine and Parallel Processing | [Read](https://blog.csdn.net/qq_40672115/article/details/168753582) |

## Setup

Each lab has its own environment; only the essentials are listed here.

### Lab 0 — PyTorch tutorial

- Completed locally with a CUDA-enabled PyTorch environment.
- The official notebook includes Colab-only setup cells (Google Drive mount and package install); skip those when running locally.
- Dependencies: PyTorch/torchvision, `torchprofile`, `tqdm`, and `matplotlib`.
- CIFAR-10 is downloaded automatically to `data/cifar10` and is gitignored.

### Lab 1 — GPU basics

- Full instructions and point breakdown: [lab1_gpu_basics/README.md](./lab1_gpu_basics/README.md).
- Target environment: local NVIDIA RTX 4060 with a CUDA-enabled PyTorch 2.x build ([install guide](https://pytorch.org/get-started/locally/)).
- Start Jupyter from `lab1_gpu_basics/` so `utils/` imports and `assets/` images resolve.
- Pinned dependencies from the official handout:

```bash
conda install nvidia::cuda-nvcc==12.4.99
pip install "transformers==4.57.6" "tokenizers==0.22.2" \
            "huggingface_hub==0.36.2" "accelerate==1.11.0"
pip install --no-build-isolation flash-attn   # optional, Part 5 bonus
```

- `trace.json` (Chrome trace) and local caches are gitignored.

### Lab 2 — Pruning

- Completed notebook: [lab2/lab2_pruning.ipynb](./lab2/lab2_pruning.ipynb).
- The reference run was performed on an **NVIDIA A30**; the RTX 4060 did not have enough VRAM for the later training/fine-tuning steps.
- The notebook uses a repo-local Hugging Face cache at `lab2/.cache/huggingface` and runs in offline mode. The cache is gitignored. Start Jupyter from `lab2/` so `Path.cwd()` resolves to the lab directory.
- On a fresh machine, the setup cell automatically falls back to the default Hugging Face cache in online mode when `lab2/.cache/huggingface` is absent. Accept the Gemma license and set `HF_TOKEN` for the one-time download; alternatively, pre-populate the cache to run fully offline.

### Lab 3 — Neural architecture search

- Completed notebook: [lab3/lab3_nas.ipynb](./lab3/lab3_nas.ipynb).
- The reference run uses a local offline asset layout: `lab3/mcunet_repo/` (MCUNet code, accuracy dataset, `vww_supernet.pth`) and `lab3/vww_data/` (VWW validation images). Both are gitignored; the notebook's setup cell selects them.
- Run Jupyter from `lab3/`; a CUDA GPU, `graphviz`, `thop`, and `onnx` are required.
- To rebuild the assets on a fresh machine, use the original Dropbox setup cell (kept commented in the notebook) or pre-populate those two directories.

## Repository Structure

```text
.
├── lab0/
│   └── lab0.ipynb                 # Completed: VGG-11 variant on CIFAR-10 (92.62%)
├── lab1_gpu_basics/
│   ├── README.md                  # Official Lab 1 handout and point breakdown
│   ├── lab1.ipynb                 # Completed notebook (local RTX 4060)
│   ├── decode_layer_tracing.png   # Decode profiling timeline
│   ├── mlp_cuda_graph_tracing.png # CUDA Graph profiling timeline
│   ├── assets/                    # Figures used by the notebook
│   └── utils/                     # Benchmarking, config (incl. the 4060 spec), model, visualization helpers
├── lab2/
│   └── lab2_pruning.ipynb         # Completed notebook (NVIDIA A30; local HF cache)
├── lab3/
│   └── lab3_nas.ipynb             # Completed notebook (local offline assets)
├── .gitignore
├── LICENSE
└── README.md
```

Future labs will live in their own `labN_<topic>/` directories when local materials are provided.

## Acknowledgements

- Course instructors Song Han and Shang Yang, and the MIT HAN Lab.
- Lab 1 materials were provided by Zhijian Liu's Z Lab, as credited in the official handout.
- Thanks to the maintainers of PyTorch, Hugging Face Transformers, torchprofile, and FlashAttention.

## Reference

- [MIT 6.5940: TinyML and Efficient AI Computing (Fall 2026)](https://hanlab.mit.edu/courses/2026-fall-65940)
- [EfficientML.ai](https://efficientml.ai)
- [Course videos](https://live.efficientml.ai/)
- [MIT HAN Lab](https://hanlab.mit.edu/)
- [erectbranch/MIT-Efficient-AI](https://github.com/erectbranch/MIT-Efficient-AI) — lecture notes and README layout inspiration
- [yifanlu0227/MIT-6.5940](https://github.com/yifanlu0227/MIT-6.5940) — previous lab implementations for reference

## License

My own solutions and notes are released under the [MIT License](./LICENSE). Course-provided materials, including lab handouts, starter code, and figures, remain the property of their original authors and are included for personal, educational reference only.
