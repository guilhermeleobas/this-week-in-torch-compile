---
title: "This week in torch.compile #5 - Sep 06"
date: 2026-09-06
---

_Covering 2026-08-30 to 2026-09-06._

## News and Announcements

<!-- editorial: releases, RFCs, blog posts, talks, announcements. Delete section if empty. -->

- [PyTorch 2.14.0 General Availability](https://dev-discuss.pytorch.org/t/pytorch-2-14-0-general-availability/3431)

## On the forums

Quiet week on [the compiler forum](https://dev-discuss.pytorch.org/c/compiler/5).

## Config changes
- new: `torch._dynamo.config.gc_gen2_threshold_during_compile`

## Dynamo commits
- Fixed Dynamo to guard autocast context objects by their actual settings (device, dtype, enabled, cache) instead of object identity, avoiding unnecessary recompilations and preventing stale graph reuse when an autocast object is mutated in place. ([#194754](https://github.com/pytorch/pytorch/pull/194754), @bobrenjc93)
- Fixed two Dynamo guard bugs where a compiled graph specialized on the float value 0.0 could incorrectly be reused for -0.0 (giving wrong results for functions like copysign or 1/x), and where a NaN guard for complex numbers didn't check both real and imaginary parts. ([#192604](https://github.com/pytorch/pytorch/pull/192604), @ezyang)
- Sped up torch.compile's cold-compile time by temporarily raising Python's garbage-collection threshold during compilation, avoiding repeated full garbage-collection scans of a rapidly growing heap of compiler objects. ([#193289](https://github.com/pytorch/pytorch/pull/193289), @anijain2305)
- Fixed a silent correctness bug where compiling code that uses torch.inference_mode() with node-order canonicalization enabled could produce output tensors as if inference_mode were never entered, with no error. ([#195518](https://github.com/pytorch/pytorch/pull/195518), @jansel)
- Torch.compile no longer recompiles on every new shape for the out= variants of max, min, and topk, by giving those overloads meta functions so symbolic shapes propagate correctly. ([#187952](https://github.com/pytorch/pytorch/pull/187952), @jonasvq)
- Fixed a Dynamo bug where the FP64 upcast used for softmax/log-softmax debugging repros left a stale half_to_float flag, breaking output overload argument matching. ([#194595](https://github.com/pytorch/pytorch/pull/194595), @mengph)
- Fixed a memory leak in Dynamo where compiling higher-order-operator subgraphs (e.g. for control flow) kept input tensors alive via a reference cycle until a full garbage collection ran. ([#195954](https://github.com/pytorch/pytorch/pull/195954), @drisspg)
- Added support for Dynamo to trace deallocation of tensors on Meta's MTIA accelerator so compiled code can safely reuse cross-stream memory the way CUDA already does. ([#195524](https://github.com/pytorch/pytorch/pull/195524), @excalibur68)
- Fixed nonstrict_trace (a mechanism for tracing through custom operators) to correctly handle function arguments and return values that are None instead of rejecting them. ([#185742](https://github.com/pytorch/pytorch/pull/185742), @jansel)
- Fixed Dynamo to preserve activation-memory-budget annotations on operations after a graph break, which were previously silently dropped for resumed frames. ([#194808](https://github.com/pytorch/pytorch/pull/194808), @soulitzer)
- ...plus 26 more commits

## Inductor commits
- Fixed a bug where compiling an integer modulo operation with a tensor size that doesn't fill a full vectorized lane raised a spurious divide-by-zero error on the CPU backend. ([#192025](https://github.com/pytorch/pytorch/pull/192025), @he-yufeng)
- Fixed a silent memory-safety bug where compiling a raw Triton kernel that mutated a strided/offset tensor view could read and leak freed memory outside the tensor's allocated storage. ([#192227](https://github.com/pytorch/pytorch/pull/192227), @KyleMylonakisProtopia)
- Fixed a silent correctness bug where compiling a while_loop whose condition function mutates a captured tensor (not a loop-carried variable) could return correct results on the first call but leave stale data in that tensor for later calls. ([#195393](https://github.com/pytorch/pytorch/pull/195393), @jansel)
- Fixed a silent correctness bug where torch.compile could return wrong tensor contents after calling resize_() on a view of an intermediate tensor produced by a compiled graph. ([#191844](https://github.com/pytorch/pytorch/pull/191844), @HussainNizamani)
- Added a new BF16x9 precision mode for CUDA FP32 matrix multiplication that's more numerically accurate than TF32, with cache and fallback handling so it doesn't break other operations that don't support it. ([#195301](https://github.com/pytorch/pytorch/pull/195301), @drisspg)
- Enabled nested reductions by default in the open-source build of Inductor, letting compiled reduction kernels split into a staged form more often for better fusion. ([#191974](https://github.com/pytorch/pytorch/pull/191974), @eellison)
- Fixed a bug where compiling with dynamic shapes could crash on the second call because a saved activation tensor's memory stride got permanently baked in as a constant from the first call's shape instead of staying symbolic. ([#194420](https://github.com/pytorch/pytorch/pull/194420), @laithsakka)
- Fixed a bug where compiling torch.frexp on CUDA returned a zero mantissa for subnormal float32 inputs because the underlying math library flushed them to zero, and also fixed the sign of negative zero being dropped. ([#195041](https://github.com/pytorch/pytorch/pull/195041), @jansel)
- Fixed a C++ compile error in AOTInductor's generated wrapper code where a symbolic element-count variable declared inside a kernel-profiling scope block was invisible to a later use, but only redeclared it correctly for kernels that actually open such a scope. ([#179698](https://github.com/pytorch/pytorch/pull/179698), @A-Kokolis)
- Added tuned default kernel configurations for FlexAttention's backward pass on AMD's gfx950 GPU architecture, giving up to a 2.3x speedup over the generic AMD defaults. ([#194151](https://github.com/pytorch/pytorch/pull/194151), @nithinsubbiah)
- ...plus 58 more commits

_In total, 36 Dynamo and 68 Inductor commits landed upstream this week._
