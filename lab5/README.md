# Lab 5 — Optimize LLM on Edge Devices

Official materials:

- [Lab handout](./MIT_Efficient_AI_Lab_5_Optimize_LLM_on_Edge.docx)
- [Report template](./Report%20template_%20MIT_Efficient_AI_Lab_5_Optimize_LLM_on_Edge.docx)

## Source snapshot

The upstream [mit-han-lab/tinychat-tutorial](https://github.com/mit-han-lab/tinychat-tutorial)
repository is vendored under [`tinychat-tutorial/`](./tinychat-tutorial/) at commit
`f241215` ("Add `+dotprod` flag to clang++ command"). The nested Git metadata and
submodule pointers were removed so the source is tracked directly in this
repository. The [`transformer/json/`](./tinychat-tutorial/transformer/json/)
dependency is the nlohmann/json source at commit `a0c1318`; the build only needs
its `single_include/` headers. `transformer/whisper.cpp` is an uninitialized
upstream submodule and is not used by this lab.

The upstream `.gitignore` was narrowed so that source, tests, scripts, and the
small tokenizer assets are tracked. Only generated build outputs and downloaded
model weights are ignored.

## Model download

The LLaMA2-7B-chat int4 model (about 5.3 GB) is **not** committed. Download it
into the ignored `transformer/INT4/models/LLaMA_7B_2_chat/` directory:

```bash
cd lab5/tinychat-tutorial/transformer
python download_model.py --model LLaMA_7B_2_chat --QM QM_x86   # Intel/AMD
# or
python download_model.py --model LLaMA_7B_2_chat --QM QM_ARM   # Apple M1/M2
```

The script needs `requests` and `tqdm`. The small tokenizer files in
`transformer/models/` are already tracked, so `download_assets.sh` is normally
not required.

## Build and evaluate

```bash
cd lab5/tinychat-tutorial/transformer
./evaluate.sh reference          # sanity check / baseline
./evaluate.sh loop_unrolling     # one optimization at a time
./evaluate.sh                    # all implementations
```

The implementations to complete are in
[`kernels/starter_code/`](./tinychat-tutorial/kernels/starter_code/). On x86
complete the `QM_x86` paths; on ARM complete the `QM_ARM` paths.

The official submission requires a PDF report (use the template above) and a
patch generated with `git diff`. Generate it from inside the vendored source
tree so the paths are relative to the tutorial repository:

```bash
cd lab5/tinychat-tutorial
git diff --relative > <studentID>-<x86|ARM>.patch
```

(From the repository root, the equivalent is
`git diff --relative=lab5/tinychat-tutorial > <studentID>-<x86|ARM>.patch`.)

## Note

This is a learning record for MIT 6.5940. TinyChatEngine (the upstream
project) is MIT-licensed; the tutorial repository itself does not ship a
separate license file. Course handouts and templates remain the property of
their original authors.
