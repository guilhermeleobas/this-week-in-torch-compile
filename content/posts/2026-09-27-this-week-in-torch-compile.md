---
title: "This week in torch.compile #8 - Sep 27"
date: 2026-09-27
---

_Covering 2026-09-20 to 2026-09-27._

## News and Announcements

<!-- editorial: releases, RFCs, blog posts, talks, announcements. Delete section if empty. -->

- [PyTorch Release 2.14.1](https://dev-discuss.pytorch.org/t/pytorch-release-2-14-1/3444)

## On the forums

- [[RFC-0036] Zero-GC 64-Byte Cache-Aligned Flat Arena for Speculative Decoding Verification](https://dev-discuss.pytorch.org/t/rfc-0036-zero-gc-64-byte-cache-aligned-flat-arena-for-speculative-decoding-verification/3441) (1 posts) (new)

## Config changes
- new: `torch._inductor.config.alignment_asserts_inputs`
- new: `torch._inductor.config.autotune_cudagraph_benchmarking_iters`
- new: `torch._inductor.config.benchmark_template_fusion`
- new: `torch._inductor.config.fusion_memory_timeline_peak_memory_increase_gb`
- new: `torch._inductor.config.fusion_memory_timeline_peak_memory_pct_threshold`
- new: `torch._inductor.config.max_template_fusion_benchmarked_choices`
- new: `torch._inductor.config.use_rand4x`

## Dynamo commits
- Fixes Dynamo silently evaluating isinstance() to False for unions or tuples of runtime-checkable Protocols, which differed from eager behavior. ([#196124](https://github.com/pytorch/pytorch/pull/196124), @jonasvq)
- Dynamo now correctly constant-folds unbound int/float/complex methods like float.__rsub__ on constants, fixing crashes and unsupported errors. ([#198482](https://github.com/pytorch/pytorch/pull/198482), @hknsahin97-coder)
- Fixes Dynamo giving wrong results for super() calls inside classmethods by leaving plain functions unbound, matching CPython. ([#198435](https://github.com/pytorch/pytorch/pull/198435), @christianaurichzm)
- Fixes silently wrong results in Dynamo when accessing user-defined descriptors in a class's own __dict__, where __get__ ran repeatedly during guards. ([#198410](https://github.com/pytorch/pytorch/pull/198410), @hknsahin97-coder)
- Fixes torch.autograd.grad graph breaks under aot_eager, where gradients could silently become None, by skipping unsafe frames. ([#185829](https://github.com/pytorch/pytorch/pull/185829), @jansel)
- Torch.export now preserves tensor-valued torch._assert as a runtime assertion instead of creating a data-dependent guard. ([#186306](https://github.com/pytorch/pytorch/pull/186306), @jansel)
- Fixes Dynamo failing to trace torch.random.fork_rng when passed a set of devices. ([#186168](https://github.com/pytorch/pytorch/pull/186168), @jansel)
- Higher-order operator subgraph tracing now rejects input mutation and aliasing by default, with transparent wrappers opting in explicitly. ([#185738](https://github.com/pytorch/pytorch/pull/185738), @jansel)
- Dynamo now graph-breaks on shape-changing .data assignment to differentiable tensors, fixing invalid-gradient failures in DeepSpeed ZeRO-3 style hooks. ([#186512](https://github.com/pytorch/pytorch/pull/186512), @jansel)
- Adds Dynamo support for Python 3.15. ([#178393](https://github.com/pytorch/pytorch/pull/178393), @rtimpe)
- ...plus 74 more commits ([full log]({{< relref "/full-log/2026-09-27#dynamo-commits" >}}))

## Inductor commits
- Fixes Inductor's SDPA fusion silently rewriting hand-written attention into wrong-output code (or crashing) by validating pattern matches against the real graph. ([#195383](https://github.com/pytorch/pytorch/pull/195383), @jansel)
- Lets Inductor fuse copies into a concatenation as a single foreach kernel even when input shapes are dynamic, instead of launching one kernel per copy. ([#198294](https://github.com/pytorch/pytorch/pull/198294), @laithsakka)
- Fixes wrong results in FlexAttention's decoding kernel (query length under 128) caused by freezing the query layout too late during lowering. ([#198543](https://github.com/pytorch/pytorch/pull/198543), @drisspg)
- Fixes a memory leak where torch.export permanently retained the traced graph, and through it the whole module and its parameters, via a debug-only map. ([#198295](https://github.com/pytorch/pytorch/pull/198295), @oniononion36)
- Inductor now recognizes X @ X.T (and batched equivalents) and lowers them to a symmetric CuTeDSL kernel. ([#194178](https://github.com/pytorch/pytorch/pull/194178), @mlazos)
- Inductor now generates runtime asserts for backed SymInt shape checks recorded as deferred asserts instead of guards, rather than dropping them. ([#185588](https://github.com/pytorch/pytorch/pull/185588), @jansel)
- Fixes silently wrong results where Inductor reinplaced a scatter whose source was a view of the mutated storage, as in x[1:] = x[:-1].clone(). ([#198010](https://github.com/pytorch/pytorch/pull/198010), @alepot55)
- Fixes transposed indices returned by compiled max_pool, adaptive_max_pool2d and fractional_max_pool on non-contiguous inputs. ([#197596](https://github.com/pytorch/pytorch/pull/197596), @varadrane1707)
- Added `_scaled_mm_v2` support for float8_e4m3fn on Apple MPS, with tensorwise and rowwise scaling, optional bias, and several output dtypes. ([#196916](https://github.com/pytorch/pytorch/pull/196916), @Isalia20)
- Inductor backend-specific config values can now be passed through `torch.compile(options={"<device>.<key>": ...})` for registered custom backends. ([#194998](https://github.com/pytorch/pytorch/pull/194998), @yeyehaha)
- ...plus 56 more commits ([full log]({{< relref "/full-log/2026-09-27#inductor-commits" >}}))

_In total, 84 Dynamo and 66 Inductor commits landed upstream this week._

_Notable commits per week (score 3+ of 5), last 8 weeks:_

```
        Dynamo                      Inductor
Aug 09  ███████▍               14   █████████▍             18
Aug 16  ██████████▌            20   ██████████████████████ 42
Aug 23  █████████▍             18   ████████████████████▍  39
Aug 30  ███████████            21   ██████████████▋        28
Sep 06  █████▊                 11   ████████████▋          24
Sep 13  ██████▎                12   ████████▍              16
Sep 20  ████████████████████▍  39   ██████████████████████ 42
Sep 27  ██████████████████▉    36   █████████████████████  40
```
