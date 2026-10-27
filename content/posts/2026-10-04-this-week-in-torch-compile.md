---
title: "This week in torch.compile #9 - Oct 04"
date: 2026-10-04
---

_Covering 2026-09-27 to 2026-10-04._

## News and Announcements

<!-- editorial: releases, RFCs, blog posts, talks, announcements. Delete section if empty. -->

- [PyTorch 2.14.1 General Availability](https://dev-discuss.pytorch.org/t/pytorch-2-14-1-general-availability/3455)

## On the forums

Quiet week on [the compiler forum](https://dev-discuss.pytorch.org/c/compiler/5).

## Config changes
- new: `torch._inductor.config.var_std_reduction_dedup`

## Dynamo commits
- Dynamo now raises the same TypeError as eager when a traced __init__ returns a non-None value, instead of silently succeeding. ([#198604](https://github.com/pytorch/pytorch/pull/198604), @hknsahin97-coder)
- Dynamo now preserves the original exceptions and messages from constant-folded Python operations, fixing empty messages and internal crashes versus eager. ([#198590](https://github.com/pytorch/pytorch/pull/198590), @hknsahin97-coder)
- Dynamo now draws from the live random.Random object at runtime instead of baking in trace-time values, fixing stale random numbers on cache hits. ([#196921](https://github.com/pytorch/pytorch/pull/196921), @JaynouOliver)
- Fixes Dynamo passing random float draws as float32 instead of float64, which made Inductor CPU kernels return garbage like -9e34. ([#199075](https://github.com/pytorch/pytorch/pull/199075), @Sahil170595)
- AOTAutograd cache now accepts graphs with inference_mode regions and torch._refs.tensor nodes, which previously bypassed caching entirely. ([#191409](https://github.com/pytorch/pytorch/pull/191409), @aorenste)
- Dynamo can now constant-fold bytes() calls and correctly propagates expected exceptions from constant-like objects such as regex patterns. ([#197499](https://github.com/pytorch/pytorch/pull/197499), @VenkataSriSaiSuryaMandava)
- Dynamo can now trace calls to classmethod() and staticmethod() inside compiled regions instead of graph breaking. ([#197781](https://github.com/pytorch/pytorch/pull/197781), @KarhouTam)
- Fixes torch.compile used as a class decorator crashing under caching_precompile, as hit by flash-linear-attention. ([#191977](https://github.com/pytorch/pytorch/pull/191977), @cjolivier01)
- Dynamo now constant-folds __name__, __module__ and similar metadata on torch builtin functions, so checks like func.__name__.endswith('_') no longer graph break. ([#196049](https://github.com/pytorch/pytorch/pull/196049), @ezyang)
- Dynamo now raises a proper AttributeError for missing attributes on opaque objects, making hasattr and getattr-with-default traceable. ([#196050](https://github.com/pytorch/pytorch/pull/196050), @ezyang)
- ...plus 41 more commits ([full log]({{< relref "/full-log/2026-10-04#dynamo-commits" >}}))

## Inductor commits
- Fixes torch.normal under torch.compile returning the wrong dtype when mean and std have different floating dtypes, so it now matches eager. ([#194557](https://github.com/pytorch/pytorch/pull/194557), @akki-g)
- On Apple MPS, Inductor now reduces short reductions (8-31 elements) with one thread per output, speeding up a MoE combine kernel from 5.5 ms to 0.1 ms. ([#199278](https://github.com/pytorch/pytorch/pull/199278), @Isalia20)
- Inductor's multi-dimensional reduction tiling now supports a third reduction axis (R2) in addition to R0 and R1. ([#197437](https://github.com/pytorch/pytorch/pull/197437), @nandesuka)
- Fixes compiled adaptive max-pool 3D gradients differing from eager for channels-last inputs by enforcing eager-compatible strides. ([#199068](https://github.com/pytorch/pytorch/pull/199068), @mlazos)
- Fixes a NameError with torch.compile reduce-overhead and graph partitioning when a mutating fallback op returns an alias of its input. ([#199414](https://github.com/pytorch/pytorch/pull/199414), @karthickai)
- Fixes Inductor on CPU changing the output dtype of same-dtype integer bmm/matmul (e.g. int8 became int64), so it now matches eager. ([#191324](https://github.com/pytorch/pytorch/pull/191324), @he-yufeng)
- Fixes Inductor producing wrong values or scheduler errors for in-place ops like index_put_ on a realized buffer that earlier lowered code still referenced. ([#198549](https://github.com/pytorch/pytorch/pull/198549), @alepot55)
- Fixes compiled argmax/argmin on Apple MPS returning wrong indices for transposed inputs and sliced inputs over 1024 elements. ([#199134](https://github.com/pytorch/pytorch/pull/199134), @Isalia20)
- Adds a cudagraph_dynamic_shape_rerecord_limit config so graphs with a few dynamic shapes keep CUDA graphs while highly dynamic ones are skipped. ([#197433](https://github.com/pytorch/pytorch/pull/197433), @Microve)
- Fixes Inductor dropping a needed device copy of a view of a constant, which could pass a CPU buffer to a CUDA kernel. ([#199402](https://github.com/pytorch/pytorch/pull/199402), @karthickai)
- ...plus 76 more commits ([full log]({{< relref "/full-log/2026-10-04#inductor-commits" >}}))

_In total, 51 Dynamo and 86 Inductor commits landed upstream this week._

_Notable commits per week (score 3+ of 5), last 8 weeks:_

```
        Dynamo                      Inductor
Aug 09  █████                  14   ██████▌                18
Aug 16  ███████▎               20   ███████████████▏       42
Aug 23  ██████▌                18   ██████████████▏        39
Aug 30  ███████▋               21   ██████████▏            28
Sep 06  ████                   11   ████████▋              24
Sep 13  ████▍                  12   █████▊                 16
Sep 20  █▏                     3    ██▏                    6
Oct 04  ██████████▌            29   ██████████████████████ 61
```
