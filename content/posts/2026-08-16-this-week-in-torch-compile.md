---
title: "This week in torch.compile #2 - Aug 16"
date: 2026-08-16
---

_Covering 2026-08-09 to 2026-08-16._

## News and Announcements

<!-- editorial: releases, RFCs, blog posts, talks, announcements. Delete section if empty. -->

- [Reminder — Call for Features: PyTorch 2.14](https://dev-discuss.pytorch.org/t/reminder-call-for-features-pytorch-2-14/3423)
- [PyTorch 2.14 RC1 produced for pytorch & torchvision](https://dev-discuss.pytorch.org/t/pytorch-2-14-rc1-produced-for-pytorch-torchvision/3422)
- [PyTorch Release 2.14 Branch Cut is Complete](https://dev-discuss.pytorch.org/t/pytorch-release-2-14-branch-cut-is-complete/3420)

## On the forums

Quiet week on [the compiler forum](https://dev-discuss.pytorch.org/c/compiler/5).

## Dynamo commits
- Graphs containing autocast enter/exit are now cacheable by AOTAutograd instead of permanently bypassing the cache, which had forced a full recompile every process start for models entering autocast inside forward. ([#192555](https://github.com/pytorch/pytorch/pull/192555), @anijain2305)
- Lets `tensor.requires_grad = True` be traced instead of always breaking the graph, when the tensor was created inside the compiled region and has a differentiable dtype, matching what `.requires_grad_(True)` already supported. ([#191129](https://github.com/pytorch/pytorch/pull/191129), @guan404ming)
- Fixes a CUDA memory leak where the symbolic shape environment kept holding fake tensors after compilation finished. ([#193015](https://github.com/pytorch/pytorch/pull/193015), @gtnv)
- Dynamo can now rebuild stable Triton Tensor Memory Accelerator (TMA) descriptors after a captured graph returns, instead of silently falling back to eager execution. ([#185469](https://github.com/pytorch/pytorch/pull/185469), @jansel)
- Dynamo skips calling the backend compiler entirely for graphs that compute nothing after dead-code elimination, saving a full AOTAutograd pass per such frame. ([#193157](https://github.com/pytorch/pytorch/pull/193157), @anijain2305)
- Dynamo can now trace list subclasses that override `__new__` with extra arguments instead of breaking the graph. ([#191512](https://github.com/pytorch/pytorch/pull/191512), @guilhermeleobas)
- Dynamo emits the pre-graph profiler marker behind a runtime check, removing roughly 10% of the fixed per-call overhead of a compiled function when no profiler is attached. ([#190623](https://github.com/pytorch/pytorch/pull/190623), @williamwen42)
- Reverts boxing of resume-frame values because it renamed the physical source paths Dynamo reports, breaking dynamic-shape whitelists recorded by profile-guided optimization for any model that deletes a variable after a graph break. ([#192868](https://github.com/pytorch/pytorch/pull/192868), @ezyang)
- Dynamo lowers symbolic boolean negation to `torch.sym_not` so `torch._check(not expr)` installs a real assertion instead of being constant-folded away. ([#186043](https://github.com/pytorch/pytorch/pull/186043), @jansel)
- Dynamo refreshes cached tensor size, stride, and contiguity after any in-place mutation, fixing stale metadata reads after calls like `as_strided_`. ([#187890](https://github.com/pytorch/pytorch/pull/187890), @jansel)
- ...plus 30 more commits

## Inductor commits
- Apple Metal (MPS) gains native int8 matrix multiplication, so quantized and ahead-of-time-compiled workloads no longer fail on Mac GPUs. ([#193153](https://github.com/pytorch/pytorch/pull/193153), @froggy-hyun)
- Fixes out-of-bounds atomic writes in Inductor's CPU two-dimensional tiling, which applied an index offset twice and caused heap corruption on x86 and silently wrong results on aarch64 with multiple threads. ([#191861](https://github.com/pytorch/pytorch/pull/191861), @agarg0627)
- Adds an opt-in Inductor mode that makes compiled `torch.sum` bit-for-bit identical to eager by reproducing eager's reduction ordering. ([#187971](https://github.com/pytorch/pytorch/pull/187971), @karthickai)
- Inductor can generate device-agnostic code and launchers, so a graph compiled on one rank produces a byte-identical artifact that loads and runs on any rank. ([#187870](https://github.com/pytorch/pytorch/pull/187870), @aorenste)
- Symmetric-memory feature detection now works without calling a deprecated registration function, so users like TorchTitan no longer have to keep invoking it to get async tensor-parallel and one-shot all-reduce fusions. ([#193115](https://github.com/pytorch/pytorch/pull/193115), @RohitRathore1)
- Inline PTX assembly can now be used inside flex attention score and mask modifications on both the Triton and CuTeDSL FLASH backends. ([#193459](https://github.com/pytorch/pytorch/pull/193459), @drisspg)
- Inductor's static Triton launcher now supports kernels needing global scratch space, so device-side TMA kernels can be restored straight from the FX graph cache instead of going back through a compile worker. ([#191133](https://github.com/pytorch/pytorch/pull/191133), @GodlyDonuts)
- Inductor stops emitting a full two-dimensional tile load for values that only vary per output row, cutting redundant address and load work inside reductions. ([#192410](https://github.com/pytorch/pytorch/pull/192410), @rahul342)
- Compiling `torch.special.log_ndtr` no longer loses the negative-zero sign bit for large positive inputs, where fast-math optimizations were swallowing it. ([#191339](https://github.com/pytorch/pytorch/pull/191339), @l1ve709)
- The mm_plus_mm and bmm Triton templates now count the reduction loop upward, working around an Intel GPU compiler bug that silently produced wrong results. ([#189516](https://github.com/pytorch/pytorch/pull/189516), @xuhancn)
- ...plus 48 more commits

_In total, 40 Dynamo and 58 Inductor commits landed upstream this week._
