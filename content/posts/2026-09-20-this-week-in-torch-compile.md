---
title: "This week in torch.compile #6 - Sep 20"
date: 2026-09-20
---

_Covering 2026-09-13 to 2026-09-20._

## News and Announcements

<!-- editorial: releases, RFCs, blog posts, talks, announcements. Delete section if empty. -->

## On the forums

Quiet week on [the compiler forum](https://dev-discuss.pytorch.org/c/compiler/5).

## Config changes
- new: `torch._inductor.config.compile_worker_mode`

## Dynamo commits
- Fixed a Dynamo bug where compiling code after loading a previously saved compiled package could crash due to a global variable name collision, by minting names guaranteed unique to the target module. ([#196822](https://github.com/pytorch/pytorch/pull/196822), @bobrenjc93)
- Switched an internal tracing check in nn.Module's forward call path to a lighter-weight API, giving roughly 15% faster module call overhead when JIT tracing. ([#196236](https://github.com/pytorch/pytorch/pull/196236), @benediktjohannes)
- Two flaky multi-stream tests now insert proper stream synchronization so reads no longer race with the writes that produce their data. ([#195798](https://github.com/pytorch/pytorch/pull/195798), @Tharun-tharun)
- Dynamo's guard system now decides whether to keep a tuple's exact contents in a compiled-code snapshot based solely on whether it was recorded as guarded, fixing an edge case where such tuples were previously pruned incorrectly. ([#196767](https://github.com/pytorch/pytorch/pull/196767), @bobrenjc93)
- Test-only change tagging list-related Dynamo tests with a hardware classification label for CI routing. ([#193496](https://github.com/pytorch/pytorch/pull/193496), @waterxyj)
- Test-only change tagging nested graph break (NGB) tests with a hardware classification label for CI routing. ([#193066](https://github.com/pytorch/pytorch/pull/193066), @littlexiaozhang)
- Test-only change tagging lazy constant Dynamo tests with a hardware classification label for CI routing. ([#193494](https://github.com/pytorch/pytorch/pull/193494), @waterxyj)
- Test-only change tagging hooks-related Dynamo tests with hardware classification labels for CI routing. ([#193762](https://github.com/pytorch/pytorch/pull/193762), @littlexiaozhang)
- Test-only change tagging pre-grad FX graph pass tests with hardware classification labels for CI routing. ([#192929](https://github.com/pytorch/pytorch/pull/192929), @taochong123456)
- Test-only change tagging two Dynamo numeric-operator tests with hardware classification labels for CI routing. ([#192744](https://github.com/pytorch/pytorch/pull/192744), @littlexiaozhang)
- ...plus 3 more commits

## Inductor commits
- Fixed a bug in Inductor's CPU linear-layer weight packing where the bias device check compared against the wrong variable, so the check never actually validated the bias was on CPU. ([#195833](https://github.com/pytorch/pytorch/pull/195833), @gavinwang269)
- Fixed a silent correctness bug where Inductor's post-grad fusion pass for batched subtraction dropped the 'alpha' scaling argument, computing x - y instead of x - alpha*y. ([#195463](https://github.com/pytorch/pytorch/pull/195463), @PranshulSoni)
- Inductor can now compile Triton kernels using threads instead of separate worker processes when running on free-threaded Python (no GIL), avoiding expensive process spawn overhead. ([#179547](https://github.com/pytorch/pytorch/pull/179547), @alrobichaud)
- Inductor's all-gather bucketing pass now copies differently-shaped tensors with a single fused copy operation instead of one kernel launch per shape, reducing kernel launch overhead in distributed collectives. ([#196621](https://github.com/pytorch/pytorch/pull/196621), @IvanKobzarev)
- Inductor adds a dedicated thread pool for compiling Triton kernels under free-threaded (no-GIL) Python, part of the broader effort to speed up compilation by avoiding process-based worker overhead. ([#179548](https://github.com/pytorch/pytorch/pull/179548), @alrobichaud)
- Reworked the flex_gemm matrix-multiply integration so Inductor again owns autotuning of QUACK-based kernel configs, cutting tuning time and restoring config legality verification that had been lost after a prior rebase. ([#196174](https://github.com/pytorch/pytorch/pull/196174), @drisspg)
- The Metal (Apple GPU) Inductor backend now lets out-of-tree device backends override the hardcoded kernel launch device instead of forcing 'mps'. ([#195809](https://github.com/pytorch/pytorch/pull/195809), @gavinwang269)
- Internal Sandcastle test infrastructure fix for AOTInductor arrayref tests, no user-facing change. ([#196917](https://github.com/pytorch/pytorch/pull/196917), @aorenste)
- An XPU flash attention test is now skipped on older Intel PVC hardware that lacks support for the newer AOT-compiled kernel. ([#190322](https://github.com/pytorch/pytorch/pull/190322), @yucai-pro)
- Test-only change tagging cache directory utility tests with a hardware classification label for CI routing. ([#193920](https://github.com/pytorch/pytorch/pull/193920), @pengyeqing)
- ...plus 5 more commits

_In total, 13 Dynamo and 15 Inductor commits landed upstream this week._
