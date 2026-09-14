---
title: "This week in torch.compile #6 - Sep 13"
date: 2026-09-13
---

_Covering 2026-09-06 to 2026-09-13._

## News and Announcements

<!-- editorial: releases, RFCs, blog posts, talks, announcements. Delete section if empty. -->

- [PyTorch Release 2.15 | Key Dates](https://dev-discuss.pytorch.org/t/pytorch-release-2-15-key-dates/3434)

## On the forums

Quiet week on [the compiler forum](https://dev-discuss.pytorch.org/c/compiler/5).

## Config changes
- new: `torch._inductor.config.compile_worker_mode`

## Dynamo commits
- Fixed a Dynamo bug where compiling code after loading a previously saved compiled package could crash due to a global variable name collision, by minting names guaranteed unique to the target module. ([#196822](https://github.com/pytorch/pytorch/pull/196822), @bobrenjc93)
- Dynamo no longer crashes when a graph-traced object calls a method decorated with torch.no_grad, torch.enable_grad, dual_level, or inference_mode. ([#195413](https://github.com/pytorch/pytorch/pull/195413), @aperson30)
- Switched an internal tracing check in nn.Module's forward call path to a lighter-weight API, giving roughly 15% faster module call overhead when JIT tracing. ([#196236](https://github.com/pytorch/pytorch/pull/196236), @benediktjohannes)
- Manual collective bucketing's wait-node repair pass in Inductor is now linear instead of quadratic, fixing apparent hangs on large sharded graphs. ([#195616](https://github.com/pytorch/pytorch/pull/195616), @aditvenk)
- Dynamo's precompile cache now discards only the specific guard variant that failed to serialize instead of throwing away all working recompiles for that code object. ([#196505](https://github.com/pytorch/pytorch/pull/196505), @bobrenjc93)
- Adds a declarative 'implies' mechanism to PyTorch's config system so selecting one config mode can automatically force related settings. ([#196663](https://github.com/pytorch/pytorch/pull/196663), @karthickai)
- Dynamo now surfaces more genuine user errors directly instead of masking them as graph breaks. ([#196432](https://github.com/pytorch/pytorch/pull/196432), @hameerabbasi)
- Dynamo now supports calling bytes() with zero arguments instead of falling back to an unsupported-builtin graph break. ([#196103](https://github.com/pytorch/pytorch/pull/196103), @jacobhorne-jth)
- Dynamo now models Python's built-in property objects with their own dedicated variable tracker, matching CPython's descriptor semantics. ([#194642](https://github.com/pytorch/pytorch/pull/194642), @guilhermeleobas)
- Fixed a Dynamo bug where the FP64 upcast used for softmax/log-softmax debugging repros left a stale half_to_float flag, breaking output overload argument matching. ([#194595](https://github.com/pytorch/pytorch/pull/194595), @mengph)
- ...plus 46 more commits ([full log]({{< relref "/full-log/2026-09-13#dynamo-commits" >}}))

## Inductor commits
- Adds per-row scalar accumulators for online softmax in Inductor's large reduction loops, reducing memory traffic and improving performance. ([#190692](https://github.com/pytorch/pytorch/pull/190692), @eellison)
- Inductor adds a dedicated thread pool for compiling Triton kernels under free-threaded (no-GIL) Python, part of the broader effort to speed up compilation by avoiding process-based worker overhead. ([#179548](https://github.com/pytorch/pytorch/pull/179548), @alrobichaud)
- Adds float8_e4m3fn dtype support on the Apple MPS backend. ([#194074](https://github.com/pytorch/pytorch/pull/194074), @Isalia20)
- Reworked the flex_gemm matrix-multiply integration so Inductor again owns autotuning of QUACK-based kernel configs, cutting tuning time and restoring config legality verification that had been lost after a prior rebase. ([#196174](https://github.com/pytorch/pytorch/pull/196174), @drisspg)
- Adds a new pre-swizzled MX FP4/FP8 scale memory layout for scaled matrix multiplication on gfx950 ROCm GPUs. ([#190290](https://github.com/pytorch/pytorch/pull/190290), @jagadish-amd)
- Removes a restrictive row/column ratio gate in Inductor's mix-order reduction optimization so it applies to more profitable flat-shaped reductions. ([#188660](https://github.com/pytorch/pytorch/pull/188660), @oonyshch)
- Enables out-of-tree Inductor backends like TLX to register custom FlexAttention backward kernel choices on ROCm. ([#195786](https://github.com/pytorch/pytorch/pull/195786), @bangtianliu)
- Adds Tensor Data Mover hardware descriptor support in Inductor for dense matrix multiply and addmm on gfx950 ROCm GPUs. ([#191166](https://github.com/pytorch/pytorch/pull/191166), @glen-amd)
- Fixes Inductor's graph normalization pass to also canonicalize torch.concatenate calls, not just torch.cat and torch.concat, enabling further fusion optimizations. ([#195174](https://github.com/pytorch/pytorch/pull/195174), @Ultron09)
- Extends per-row scalar accumulators, previously only used for online softmax, to all reduction types in large Inductor inner loops for better performance. ([#196371](https://github.com/pytorch/pytorch/pull/196371), @eellison)
- ...plus 48 more commits ([full log]({{< relref "/full-log/2026-09-13#inductor-commits" >}}))

_In total, 56 Dynamo and 58 Inductor commits landed upstream this week._
