---
title: "This week in torch.compile #15 - Nov 15"
date: 2026-11-15
---

_Covering 2026-11-08 to 2026-11-15._

## News and Announcements

<!-- editorial: releases, RFCs, blog posts, talks, announcements. Delete section if empty. -->

## On the forums

Quiet week on [the compiler forum](https://dev-discuss.pytorch.org/c/compiler/5).

## Dynamo commits
- Removes the deprecated public TorchScript APIs (torch.jit.script, trace, load, save, freeze, and others) and makes torch.load reject TorchScript archives. ([#203621](https://github.com/pytorch/pytorch/pull/203621), @janeyx99)
- Dynamo now guards on a dictionary's insertion order, runtime type, and length wherever user code can observe them, so a cached graph that depends on those facts is no longer reused when they change. ([#200601](https://github.com/pytorch/pytorch/pull/200601), @XuehaiPan)
- Fixes wrong results when a compiled function that mutates an input is later called with overlapping views; new AOTAutograd guards trigger a recompile instead. ([#185891](https://github.com/pytorch/pytorch/pull/185891), @yinli-systems)
- Fixes Dynamo silently ignoring an autograd.Function's custom jvp under forward-mode AD and returning wrong tangents; it now graph-breaks or recompiles instead. ([#193277](https://github.com/pytorch/pytorch/pull/193277), @RyanL2)
- Loading a precompiled or AOT compile package now checks GPU architecture instead of GPU name, so packages built on one variant (for example GB300) load on a same-silicon variant (GB300 Max-Q). ([#204527](https://github.com/pytorch/pytorch/pull/204527), @bobrenjc93)
- Fixes stale graph reuse with caching_precompile=True, which dropped the closure guard (CLOSURE_MATCH) so rebinding a global function did not trigger a recompile. ([#204502](https://github.com/pytorch/pytorch/pull/204502), @williamwen42)
- Fixes stale results when d[key] raises KeyError inside a compiled function; Dynamo now guards on key membership, so a later call with the key present recompiles. ([#201414](https://github.com/pytorch/pytorch/pull/201414), @Sukhshum2628)
- Fixes Dynamo's itertools.cycle polyfill so a stateful iterable is iterated only once, matching CPython and eager results. ([#201608](https://github.com/pytorch/pytorch/pull/201608), @mottopanikeiku)
- Fixes a circular import between the AOTAutograd runtime wrappers and Dynamo that could leave Dynamo half-initialized and make later torch.compile calls fail. ([#204231](https://github.com/pytorch/pytorch/pull/204231), @LittlePyx)
- Len() on a 0-dimensional tensor under torch.compile now raises TypeError like eager mode does, instead of leaking an internal IndexError that failed compilation. ([#203515](https://github.com/pytorch/pytorch/pull/203515), @vuvinh08)
- ...plus 49 more commits ([full log]({{< relref "/full-log/2026-11-15#dynamo-commits" >}}))

## Inductor commits
- AOTInductor models compiled with aot_inductor.cudagraphs=True can now run as CUDA graphs through a new C API and a Python run_with_lazy_cuda_graphs method on loaded packages. ([#202231](https://github.com/pytorch/pytorch/pull/202231), @desertfire)
- On CUDA, Inductor now replaces small topk calls (k up to 16 over rows of at most 1024 elements) with fused rounds of argmax, which greatly speeds up mixture-of-experts routers such as DeepSeek-V3's. ([#200740](https://github.com/pytorch/pytorch/pull/200740), @anijain2305)
- Fixes an unsound dynamic-shapes guard where float-valued symbolic expressions were truncated to integers, producing guards that failed on the very inputs they were built from. ([#202324](https://github.com/pytorch/pytorch/pull/202324), @laithsakka)
- Fixes wrong results from compiled resize_/resize_as_ on padded, permuted, or sliced inputs, which Inductor read as dense memory and ignored their strides. ([#204633](https://github.com/pytorch/pytorch/pull/204633), @nandesuka)
- Fixes a memory leak where AOTInductor model .so files could never be unloaded on long-lived server threads, because of a thread-local error string with a non-trivial destructor. ([#204491](https://github.com/pytorch/pytorch/pull/204491), @aaronenyeshi)
- Fixes Inductor's FX wrapper launching user-defined Triton kernels with the wrong grid or shifted arguments, caused by compile-time constant (constexpr) arguments being restored before the grid was read. ([#204567](https://github.com/pytorch/pytorch/pull/204567), @zlin888)
- Inductor now builds host-side TMA (Tensor Memory Accelerator) descriptors from dynamic sizes read at launch, avoiding per-block on-device descriptor creation and speeding up GEMM templates with dynamic shapes on H100. ([#202612](https://github.com/pytorch/pytorch/pull/202612), @htyu)
- Fixes Inductor's no-op removal pass collapsing two distinct graph outputs into the same tensor. ([#203433](https://github.com/pytorch/pytorch/pull/203433), @nirali25parekh)
- Adds public F.quantize_tensor and F.quantize_tensor_dual APIs, starting with MXFP8 quantization backed by CuTe DSL kernels. ([#199022](https://github.com/pytorch/pytorch/pull/199022), @vkuzo)
- Adds a disallow_implicit_grad_accumulation flag to .backward() that raises an error whenever backward would silently sum gradients from a tensor used more than once. ([#203413](https://github.com/pytorch/pytorch/pull/203413), @soulitzer)
- ...plus 68 more commits ([full log]({{< relref "/full-log/2026-11-15#inductor-commits" >}}))

_In total, 59 Dynamo and 78 Inductor commits landed upstream this week._

_Notable commits per week (score 3+ of 5), last 8 weeks:_

```
        Dynamo                      Inductor
Sep 27  █████████████          36   ██████████████▍        40
Oct 04  ██████████▌            29   ██████████████████████ 61
Oct 11  █████▊                 16   ████████████████████▉  58
Oct 18  █████████▊             27   ██████████████████▍    51
Oct 25  ██▉                    8    ███████████▏           31
Nov 01  █████████▊             27   █████████████▊         38
Nov 08  ████████▎              23   █████████████          36
Nov 15  █████████▊             27   ████████████████▋      46
```
