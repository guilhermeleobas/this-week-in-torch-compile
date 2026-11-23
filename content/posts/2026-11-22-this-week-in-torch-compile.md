---
title: "This week in torch.compile #16 - Nov 22"
date: 2026-11-22
---

_Covering 2026-11-15 to 2026-11-22._

## News and Announcements

<!-- editorial: releases, RFCs, blog posts, talks, announcements. Delete section if empty. -->

- [No PyTorch 2.15.1 release](https://dev-discuss.pytorch.org/t/no-pytorch-2-15-1-release/3536)

## On the forums

Quiet week on [the compiler forum](https://dev-discuss.pytorch.org/c/compiler/5).

## Config changes
- new: `torch._inductor.config.avoid_modular_indexing`
- new: `torch._inductor.config.max_autotune_reduction`
- new: `torch._inductor.config.reinplace_scatter_chain_threshold`
- new: `torch._inductor.config.reinplace_whenever_possible`
- new: `torch._inductor.config.reorder_for_peak_memory_preserve_collective_order`

## Dynamo commits
- Fixes torch.compile silently returning the traced device's stream when code calls current_stream() with the index of a different device. ([#201619](https://github.com/pytorch/pytorch/pull/201619), @AAYESLY)
- Speeds up the guard that checks whether mutated inputs still share storage the same way, which compared every pair of views on each cache hit and slowed compiled optimizer steps. ([#205789](https://github.com/pytorch/pytorch/pull/205789), @williamwen42)
- Fixes activation-checkpointing compile failures by never marking graph inputs as must-recompute, since inputs cannot be recomputed. ([#199629](https://github.com/pytorch/pytorch/pull/199629), @0z5a)
- Fixes a guard-creation crash (NameError: SYNTHETIC_LOCAL) when code calls type(), hasattr() or methods on an nn.Parameter created inside the compiled function. ([#205173](https://github.com/pytorch/pytorch/pull/205173), @peterdsharpe)
- Fixes a recent regression where a function that mutates an input and uses an assume_constant_result tensor failed to compile with NameError. ([#205231](https://github.com/pytorch/pytorch/pull/205231), @zlin888)
- Fixes incorrect results when comparing a Tensor or SymInt with an IntEnum, IntFlag or float enum member under torch.compile; == was always False and < caused graph breaks. ([#204573](https://github.com/pytorch/pytorch/pull/204573), @daud4653)
- Adds per-code-object locking around Dynamo's cache metadata to fix races from multithreaded use and torch._dynamo.reset(), especially on free-threaded Python. ([#201685](https://github.com/pytorch/pytorch/pull/201685), @alexmalyshev)
- Dynamo can now trace `del some_global` (the DELETE_GLOBAL bytecode), which used to fail under fullgraph=True or cause a graph break. ([#197056](https://github.com/pytorch/pytorch/pull/197056), @KarhouTam)
- Fixes RecursionError at graph breaks in very long functions by making Dynamo's live-variable analysis and instruction copying non-recursive. ([#204639](https://github.com/pytorch/pytorch/pull/204639), @KasraGhodsi)
- Leaving a config.patch() block now leaves previously unset keys unset instead of overriding them with their defaults, which fixes spurious Dynamo recompiles. ([#205211](https://github.com/pytorch/pytorch/pull/205211), @aorenste)
- ...plus 55 more commits ([full log]({{< relref "/full-log/2026-11-22#dynamo-commits" >}}))

## Inductor commits
- Inductor now computes floor divisions that depend only on sizes once on the host instead of in every kernel element, which made vLLM's FP8 block-cast kernel about 1.2x faster under dynamic shapes. ([#205053](https://github.com/pytorch/pytorch/pull/205053), @oonyshch)
- Inductor can now generate pointwise and reduction kernels tiled over more than three dimensions when triton.max_tiles is set above 3; the default is unchanged. ([#204324](https://github.com/pytorch/pytorch/pull/204324), @blaine-rister)
- Fixes a race where Inductor's reinplacing pass dropped user CUDA stream annotations from rebuilt scatter ops, so they ran on the default stream and could read stale data. ([#205925](https://github.com/pytorch/pytorch/pull/205925), @ankitgala007)
- Fixes Inductor fusing long scatter chains into a padding kernel that reached about 1% of the memory bandwidth limit on H100 and GB300. ([#204118](https://github.com/pytorch/pytorch/pull/204118), @Roger-ZRZ)
- Flex attention's Triton kernels on AMD MI300/MI350 (gfx942/gfx950) now place blocks of the same batch and head on the same XCC (accelerator complex die) so they share its L2 cache. ([#204453](https://github.com/pytorch/pytorch/pull/204453), @jayfurmanek)
- Fixes symbolic modular-indexing simplifications that could give incorrect index results, and makes them handle more general expressions. ([#200418](https://github.com/pytorch/pytorch/pull/200418), @morrison-turnansky)
- Limits how many dynamic-shape sub-kernels go into one combo kernel, fixing RecursionErrors and compiles of over 30 minutes on large dynamic torch.cat calls. ([#205934](https://github.com/pytorch/pytorch/pull/205934), @anijain2305)
- Adds a max_autotune_reduction config so reduction kernels can get the wider autotuning search separately from pointwise kernels; existing settings are unchanged. ([#205532](https://github.com/pytorch/pytorch/pull/205532), @jhou-jpg)
- Torch.compile on Apple MPS now packs kernel arguments into Metal argument buffers, so heavily fused kernels no longer exceed Metal's buffer-argument limit. ([#202180](https://github.com/pytorch/pytorch/pull/202180), @Arnav66692)
- Adds the reorder_for_peak_memory_preserve_collective_order config so Inductor's peak-memory reordering keeps distributed collectives in their original order, avoiding possible hangs. ([#205256](https://github.com/pytorch/pytorch/pull/205256), @Microve)
- ...plus 90 more commits ([full log]({{< relref "/full-log/2026-11-22#inductor-commits" >}}))

_In total, 65 Dynamo and 100 Inductor commits landed upstream this week._

_Notable commits per week (score 3+ of 5), last 8 weeks:_

```
        Dynamo                      Inductor
Oct 04  ██████████▌            29   ██████████████████████ 61
Oct 11  █████▊                 16   ████████████████████▉  58
Oct 18  █████████▊             27   ██████████████████▍    51
Oct 25  ██▉                    8    ███████████▏           31
Nov 01  █████████▊             27   █████████████▊         38
Nov 08  ████████▎              23   █████████████          36
Nov 15  █████████▊             27   ████████████████▋      46
Nov 22  ███████████████▏       42   ████████████████████▌  57
```
