---
title: "This week in torch.compile #3 - Aug 23"
date: 2026-08-23
---

_Covering 2026-08-16 to 2026-08-23._

## News and Announcements

<!-- editorial: releases, RFCs, blog posts, talks, announcements. Delete section if empty. -->

## On the forums

Quiet week on [the compiler forum](https://dev-discuss.pytorch.org/c/compiler/5).

## Config changes
- new: `torch._inductor.config._cache_config_serializer`
- new: `torch._inductor.config.bmm_shared_a`
- removed: `torch._inductor.config._cache_config_factory_keys`

## Dynamo commits
- Makes the foreach operations public as `torch.foreach.*`, with cleaned-up parameter names, keyword-only arguments, and no out variants. ([#193607](https://github.com/pytorch/pytorch/pull/193607), @janeyx99)
- Fixes a crash when compiling code that uses activation checkpointing with dynamic shapes, caused by Dynamo caching a symbolic float value against the wrong tracer when the value was first seen inside a higher-order operator body. ([#193254](https://github.com/pytorch/pytorch/pull/193254), @aperson30)
- Stops the loud, unactionable "Backend compiler exception" warning that was printed every time Dynamo took an allowed fall back to eager, such as `Tensor.tolist()` with captured scalar outputs. ([#185155](https://github.com/pytorch/pytorch/pull/185155), @jansel)
- Fixes a "dictionary changed size during iteration" crash when Dynamo traces a dictionary, such as a module's globals, that Dynamo itself mutates during garbage collection. ([#191281](https://github.com/pytorch/pytorch/pull/191281), @aperson30)
- Lets a compiler backend declare a `_dynamo_backend_init` hook that runs once at `torch.compile()` time, so out-of-tree backends can do eager setup like loading native libraries without monkey-patching Dynamo. ([#192345](https://github.com/pytorch/pytorch/pull/192345), @yeyehaha)
- Adds `TORCH_COMPILE_STATIC_SOURCES` to force specific sources to be treated as static shapes, an escape hatch when automatic dynamic shapes or profile-guided optimization makes something dynamic and hurts the generated kernel. ([#193626](https://github.com/pytorch/pytorch/pull/193626), @Microve)
- Stops the deprecation warning spam from the renamed public collective aliases like `all_gather_into_tensor`, keeping the aliases and moving the guidance into the docstring. ([#193874](https://github.com/pytorch/pytorch/pull/193874), @kapilsh)
- Lets `tensor.requires_grad = True` be traced instead of always breaking the graph, when the tensor was created inside the compiled region and has a differentiable dtype, matching what `.requires_grad_(True)` already supported. ([#191129](https://github.com/pytorch/pytorch/pull/191129), @guan404ming)
- Fixes a CUDA memory leak where the symbolic shape environment kept holding fake tensors after compilation finished. ([#193015](https://github.com/pytorch/pytorch/pull/193015), @gtnv)
- Dynamo can now rebuild stable Triton Tensor Memory Accelerator (TMA) descriptors after a captured graph returns, instead of silently falling back to eager execution. ([#185469](https://github.com/pytorch/pytorch/pull/185469), @jansel)
- ...plus 20 more commits

## Inductor commits
- Fixes silently wrong gradients under `torch.compile` for chained modulated LayerNorms that slice one shared parameter (the DiT/AdaLN pattern used by models like Wan 2.1), a regression from mix-order reduction being enabled by default in 2.10. ([#193103](https://github.com/pytorch/pytorch/pull/193103), @haojiang01)
- Fixes corrupted gradients when a `nested_compile_region` is reused, caused by the subgraph inheriting the outer graph's donated-buffer indices and overwriting a saved input during the first backward pass. ([#193960](https://github.com/pytorch/pytorch/pull/193960), @anijain2305)
- One-line fix for silent data corruption in Inductor, where a non-contiguous reshape before the layout was frozen could produce large numerical errors in backward passes, most often with non-power-of-two strided slices. ([#192575](https://github.com/pytorch/pytorch/pull/192575), @cartazio)
- Adds a batched `wait_tensors` API so a coalesced multi-output functional collective can be awaited in one call instead of one wait per output tensor. ([#193892](https://github.com/pytorch/pytorch/pull/193892), @xmfan)
- Fixes compiled `torch.randn` and `torch.randn_like` on CUDA returning uniform instead of normally distributed values when the `align_random_eager` option was enabled. ([#194118](https://github.com/pytorch/pytorch/pull/194118), @Mukesh-SCS)
- Disables the `batch_linear_lhs` fusion by default on Intel XPU, fixing a crash when serving Qwen models whose layout-sensitive consumers broke on the fusion's non-contiguous views. ([#194225](https://github.com/pytorch/pytorch/pull/194225), @etaf)
- Fixes a crash in Inductor's communication/compute overlap scheduling when it was run with both memory caps set to None, the documented way to run the pass without a memory limit. ([#192628](https://github.com/pytorch/pytorch/pull/192628), @HussainNizamani)
- Fixes a CPU performance bug where a vectorized outer loop smaller than the vector width made Inductor move OpenMP parallelism inside a serial loop, re-forking the thread pool on every iteration. ([#190928](https://github.com/pytorch/pytorch/pull/190928), @frost-intel)
- Makes the eight low-level Bessel special functions differentiable in both reverse and forward mode, including careful handling of the removable singularity in J1's derivative at zero. ([#189872](https://github.com/pytorch/pytorch/pull/189872), @colalb1)
- Fixes 32-bit integer overflow in the Triton grouped matrix multiply kernel that caused crashes or wrong results on very large tensors, and skips a hardware mode that cannot handle oversized inputs. ([#192649](https://github.com/pytorch/pytorch/pull/192649), @alexsamardzic)
- ...plus 48 more commits

_In total, 30 Dynamo and 58 Inductor commits landed upstream this week._
