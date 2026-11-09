---
title: "This week in torch.compile #14 - Nov 08"
date: 2026-11-08
---

_Covering 2026-11-01 to 2026-11-08._

## News and Announcements

<!-- editorial: releases, RFCs, blog posts, talks, announcements. Delete section if empty. -->

- [Release 2.16.0 | Key Dates](https://dev-discuss.pytorch.org/t/release-2-16-0-key-dates/3472)

## On the forums

Quiet week on [the compiler forum](https://dev-discuss.pytorch.org/c/compiler/5).

## Config changes
- new: `torch._inductor.config.realize_broadcast_reuse_threshold`

## Dynamo commits
- Fixes Dynamo's itertools.cycle polyfill so a stateful iterable is iterated only once, matching CPython and eager results. ([#201608](https://github.com/pytorch/pytorch/pull/201608), @mottopanikeiku)
- Fixes Dynamo overwriting a separately configured Inductor deterministic setting (such as TORCHINDUCTOR_DETERMINISTIC=1) when it restores deterministic-algorithms state after tracing. ([#198572](https://github.com/pytorch/pytorch/pull/198572), @AnkitNakhawa)
- Fixes silently wrong results when calling different tensor methods or properties on a Tensor subclass under torch.compile by guarding method descriptors. ([#202891](https://github.com/pytorch/pytorch/pull/202891), @Light-yzc)
- Makes torch.compiler tracing flags per-thread so concurrent torch.compile and torch.export sessions in different threads no longer interfere or leave flags stuck. ([#202198](https://github.com/pytorch/pytorch/pull/202198), @KarhouTam)
- Optimizes the backward of mean by dividing before expanding the gradient, avoiding an input-sized buffer and returning a stride-0 expanded gradient like sum does. ([#202976](https://github.com/pytorch/pytorch/pull/202976), @matthewdcong)
- Dynamo now guards the code object of inlined bound methods, so replacing a method's __code__ or rebinding it after compilation no longer runs a stale graph. ([#198124](https://github.com/pytorch/pytorch/pull/198124), @RyanL2)
- Fixes a Python 3.14 crash and missed cache hits where a garbage-collected guard manager was freed while Dynamo was still evaluating a cache entry. ([#199820](https://github.com/pytorch/pytorch/pull/199820), @itamaro)
- Fixes compiled torch.cuda.synchronize() on an index-less device to sync the caller's current device instead of always device 0. ([#197384](https://github.com/pytorch/pytorch/pull/197384), @aorenste)
- Dynamo can now trace bytearray.splitlines, partition and rpartition with constant arguments instead of graph breaking. ([#201350](https://github.com/pytorch/pytorch/pull/201350), @Sanskaaar1)
- Dynamo now models needs_input_grad on autograd.Function contexts and graph breaks on custom vmap staticmethods under functorch transforms. ([#202283](https://github.com/pytorch/pytorch/pull/202283), @guilhermeleobas)
- ...plus 41 more commits ([full log]({{< relref "/full-log/2026-11-08#dynamo-commits" >}}))

## Inductor commits
- Fixes torch.cat returning partially uninitialized memory (causing NaNs) with graph_partition=True when its inputs are computed in different graph partitions. ([#200865](https://github.com/pytorch/pytorch/pull/200865), @Microve)
- Inductor no longer launches Triton kernels that contain device asserts during compile-time autotuning, avoiding sticky GPU failures on made-up inputs in AOTInductor. ([#202931](https://github.com/pytorch/pytorch/pull/202931), @shoumikhin)
- Fixes a 'Input tensor must have contiguous last dimension' crash in compiled flash-attention SDPA when Inductor passed a key or value with a non-contiguous head dimension. ([#202297](https://github.com/pytorch/pytorch/pull/202297), @echen4096)
- Fixes AOTInductor runtime constant folding returning non-dense folded views as contiguous copies, which caused kernels to read wrong memory or hit illegal memory access. ([#199817](https://github.com/pytorch/pytorch/pull/199817), @mrmiywj)
- Inductor can now fuse a native matmul followed by a row reduction into a single kernel as a persistent reduction for small N. ([#193292](https://github.com/pytorch/pytorch/pull/193292), @mlazos)
- Adds an Inductor option, triton.enable_fp_fusion, to turn off fused multiply-add contraction so kernels give identical bits regardless of which autotuned config is picked. ([#202218](https://github.com/pytorch/pytorch/pull/202218), @dmdok)
- Relands a fix so Inductor's persistent-TMA matmul feasibility check no longer specializes dynamic dimensions, avoiding ConstraintViolationError and recompiles on every new size. ([#201920](https://github.com/pytorch/pytorch/pull/201920), @jananisriram)
- Adds an opt-in Inductor CPU config, cpp.sqrt_without_errno, that emits sqrt and rsqrt without setting errno so the compiler can vectorize normalization ops like LayerNorm better. ([#203519](https://github.com/pytorch/pytorch/pull/203519), @ShuyangLiu)
- Adds an opt-in Inductor CPU config, cpp.simd_horizontal_reduction, that makes clang builds use the faster AVX2 shuffle-tree reduction of vector accumulators. ([#203835](https://github.com/pytorch/pytorch/pull/203835), @helloguo)
- Fixes wrong results and out-of-bounds reads in ROCm Composable Kernel (CK) rowwise FP8 GEMM caused by misclassified singleton-column scale layouts. ([#202816](https://github.com/pytorch/pytorch/pull/202816), @desertfire)
- ...plus 66 more commits ([full log]({{< relref "/full-log/2026-11-08#inductor-commits" >}}))

_In total, 51 Dynamo and 76 Inductor commits landed upstream this week._

_Notable commits per week (score 3+ of 5), last 8 weeks:_

```
        Dynamo                      Inductor
Sep 20  ██████████████▏        39   ███████████████▏       42
Sep 27  █████████████          36   ██████████████▍        40
Oct 04  ██████████▌            29   ██████████████████████ 61
Oct 11  █████▊                 16   ████████████████████▉  58
Oct 18  █████████▊             27   ██████████████████▍    51
Oct 25  ██▉                    8    ███████████▏           31
Nov 01  █████████▊             27   █████████████▊         38
Nov 08  ████████▎              23   █████████████          36
```
