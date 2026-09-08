---
title: "This week in torch.compile #4 - Aug 30"
date: 2026-08-30
---

_Covering 2026-08-23 to 2026-08-30._

## News and Announcements

<!-- editorial: releases, RFCs, blog posts, talks, announcements. Delete section if empty. -->

- [PyTorch 2.14 Final RC Available](https://dev-discuss.pytorch.org/t/pytorch-2-14-final-rc-available/3429)

## On the forums

Quiet week on [the compiler forum](https://dev-discuss.pytorch.org/c/compiler/5).

## Config changes
- new: `torch._inductor.config.flydsl_enable_autotuning`
- new: `torch._inductor.config.unsafe_skip_scalar_range_asserts`

## Dynamo commits
- Torch.compile no longer recompiles on every new shape for the out= variants of max, min, and topk, by giving those overloads meta functions so symbolic shapes propagate correctly. ([#187952](https://github.com/pytorch/pytorch/pull/187952), @jonasvq)
- Fixes generated repro scripts for dynamic-shape graphs that previously crashed with NameError because symbolic shape expressions were emitted as raw internal math-library syntax instead of runnable Python. ([#194827](https://github.com/pytorch/pytorch/pull/194827), @prithvip0524)
- Fixes a torch.compile crash on tensor subclasses without a custom dispatch method, caused by in-place operations incorrectly resetting the tracked subclass type back to plain torch.Tensor. ([#193969](https://github.com/pytorch/pytorch/pull/193969), @robertomeroni)
- Fixes torch.compile crashing on MultivariateNormal KL-divergence computation by teaching Dynamo how to trace calls to the internal shape-broadcasting helper torch._C._infer_size. ([#185471](https://github.com/pytorch/pytorch/pull/185471), @jansel)
- Fixes a dispatch crash under torch.compile for tensor subclasses that don't define a custom __torch_dispatch__ method, so common ops like matmul now work on them. ([#193968](https://github.com/pytorch/pytorch/pull/193968), @robertomeroni)
- Fixes torch.compile under torch.func transforms incorrectly dropping a custom backward function because a requires_grad flag change wasn't synced to Dynamo's tracked tensor state; note this can newly surface an existing graph break for custom vjp/jvp under func.grad. ([#193724](https://github.com/pytorch/pytorch/pull/193724), @robertomeroni)
- Fixes a silent correctness bug where torch.compile's caching could reuse results for a different Python float input, because a float-to-tensor optimization sometimes baked one float's value into the cache key incorrectly. ([#195040](https://github.com/pytorch/pytorch/pull/195040), @jansel)
- Relands support for min/max range hints in torch._dynamo.maybe_mark_dynamic, letting a dimension be marked dynamic with an initial size range without forcing it to always stay dynamic. ([#194625](https://github.com/pytorch/pytorch/pull/194625), @laithsakka)
- Dynamo now resolves static method attributes on `torch.autograd.Function` subclasses to the real underlying functions, removing a graph break that happened when `setup_context` was inspected. ([#185316](https://github.com/pytorch/pytorch/pull/185316), @jansel)
- Guard checking no longer applies its dictionary-version fast path to relational guards such as object-aliasing checks, which could otherwise skip half of a relation and silently accept a recompile-worthy change. ([#185911](https://github.com/pytorch/pytorch/pull/185911), @jansel)
- ...plus 27 more commits

## Inductor commits
- Fixes Inductor's lightweight compile mode so it reorders passes to avoid an unnecessary full tensor copy for every user-defined Triton kernel, cutting wasted GPU memory copies significantly. ([#194325](https://github.com/pytorch/pytorch/pull/194325), @zoranzhao)
- Fixes a torch.compile crash when writing scaled-dot-product-attention manually with a 0-dimensional tensor as the scale factor, which worked fine in eager mode. ([#191496](https://github.com/pytorch/pytorch/pull/191496), @HussainNizamani)
- Fixes a CUDA-graphs bug that could cause silent gradient corruption in multi-graph training by making tensor-liveness tracking correctly account for a still-pending backward pass holding a saved activation. ([#194124](https://github.com/pytorch/pytorch/pull/194124), @eellison)
- Adds new stateless random-number-generation APIs (randint, bits, and their in-place variants) for generating reproducible random integers keyed explicitly rather than by global RNG state. ([#190253](https://github.com/pytorch/pytorch/pull/190253), @jbschlosser)
- AOTInductor's constant folder no longer replaces a mutated buffer with its compile-time value, fixing exported packages that reset stateful buffers such as counters on every call. ([#185077](https://github.com/pytorch/pytorch/pull/185077), @jansel)
- Adds a flag to AOTInductor letting users skip overly strict inferred bounds checks on unbacked symbolic integers while still keeping shape-equality checks. ([#192857](https://github.com/pytorch/pytorch/pull/192857), @ColinPeppler)
- Fixes Inductor code generation for user-written Triton kernels that pass custom (non-builtin) Python objects as compile-time constant arguments. ([#189692](https://github.com/pytorch/pytorch/pull/189692), @AnthonyBarbier)
- Speeds up Inductor compilation on large graphs by caching formatted kernel-comment strings instead of rebuilding them for every kernel that shares the same source node. ([#194010](https://github.com/pytorch/pytorch/pull/194010), @anijain2305)
- Fixes the static Triton kernel launcher so 16-bit float (fp16/bf16) scalar arguments are packed with the correct byte width instead of being mishandled as 32-bit floats or raw pointers. ([#184065](https://github.com/pytorch/pytorch/pull/184065), @jansel)
- Fixes an Inductor crash where an optimization that simplifies full-tensor-then-cumsum patterns incorrectly assumed the fill value was always a constant instead of a symbolic scalar. ([#193959](https://github.com/pytorch/pytorch/pull/193959), @robertomeroni)
- ...plus 61 more commits

_In total, 37 Dynamo and 71 Inductor commits landed upstream this week._
