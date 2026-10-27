---
title: "This week in torch.compile #11 - Oct 18"
date: 2026-10-18
---

_Covering 2026-10-11 to 2026-10-18._

## News and Announcements

<!-- editorial: releases, RFCs, blog posts, talks, announcements. Delete section if empty. -->

## On the forums

Quiet week on [the compiler forum](https://dev-discuss.pytorch.org/c/compiler/5).

## Config changes
- new: `torch._dynamo.config.use_cpp_fake_tensor`
- new: `torch._inductor.config.avoid_32bit_indexing_guards`
- new: `torch._inductor.config.partitioned_scatter_fp32_accumulation`

## Dynamo commits
- Adds a public torch.distributed.functional_collectives module and documentation for the functional collective ops used by DTensor, FSDP2 and torch.compile, previously only available via a private module. ([#200479](https://github.com/pytorch/pytorch/pull/200479), @d4l3k)
- Dynamo now graph breaks on in-place view ops applied to a no-op alias of a graph input (e.g. x.contiguous().unsqueeze_()), fixing a guard-creation IndexError. ([#198103](https://github.com/pytorch/pytorch/pull/198103), @wwoosshh)
- Fixes deserialized training graphs (precompile, packages) packing saved tensors twice when saved-tensor hooks were inlined at compile time. ([#200551](https://github.com/pytorch/pytorch/pull/200551), @bobrenjc93)
- Fixes bool() on a torch.compile'd module raising TypeError when the original module has no __len__; it now falls back to the original module's truthiness. ([#196323](https://github.com/pytorch/pytorch/pull/196323), @CYQFWang)
- Dynamo now supports ctx.set_output_grad_dtype in autograd.Function instead of failing on a missing FunctionCtx attribute. ([#200311](https://github.com/pytorch/pytorch/pull/200311), @pianpwk)
- Dynamo no longer constant-folds three-argument type() calls, which reused one class across calls; such frames now run eagerly (and error under fullgraph). ([#199605](https://github.com/pytorch/pytorch/pull/199605), @williamwen42)
- Dynamo now guards that an instance __dict__ entry doesn't shadow a registered nn.Module attribute, fixing stale compiled graphs after object.__setattr__ on a module. ([#199212](https://github.com/pytorch/pytorch/pull/199212), @aperson30)
- Precompile can now save captures where a graph break happens inside a called function (such as a child module's forward) by writing them as installed-mode artifacts. ([#198523](https://github.com/pytorch/pytorch/pull/198523), @bobrenjc93)
- Dynamo no longer silently drops maxlen when replaying mutations on deque inputs, so bounded deques behave like eager. ([#200528](https://github.com/pytorch/pytorch/pull/200528), @XuehaiPan)
- Dynamo can now trace bytearray.append() and extend() instead of graph breaking. ([#199675](https://github.com/pytorch/pytorch/pull/199675), @jayzuccarelli)
- ...plus 52 more commits ([full log]({{< relref "/full-log/2026-10-18#dynamo-commits" >}}))

## Inductor commits
- Fixes flex attention decoding so the safe-boundary setting is computed from each config's own BLOCK_M, which previously failed when BLOCK_M was pinned to a non-default value. ([#201328](https://github.com/pytorch/pytorch/pull/201328), @felipemello1)
- CUDA graphs now preallocate their RNG state before capture, fixing a cudaErrorCapturedEvent failure when RNG is lazily initialized during capture. ([#193993](https://github.com/pytorch/pytorch/pull/193993), @eee4017)
- Adds a precompile.no_compilation() policy that raises if any graph or Triton compilation, autotuning or JIT build happens while serving a precompiled artifact. ([#198942](https://github.com/pytorch/pytorch/pull/198942), @bobrenjc93)
- Fixes MPSInductor truncating int64 constants to 32-bit, which miscompiled expressions like where(x < 0, 0, x) (seen with Gemma-4). ([#201060](https://github.com/pytorch/pytorch/pull/201060), @Isalia20)
- Precompile captures now freeze Triton kernels with their selected config and a static launcher into the cache, so serving needs no triton.compile or autotuning. ([#198954](https://github.com/pytorch/pytorch/pull/198954), @bobrenjc93)
- Prunes flex attention configs with large blocks for head_dim above 256 on Blackwell (sm_10x), avoiding a known Triton miscompile that caused memory faults. ([#200725](https://github.com/pytorch/pytorch/pull/200725), @drisspg)
- Relands fusion of pointwise producers into template epilogue inputs such as the addmm/baddbmm bias, so a computed bias no longer needs its own kernel and buffer. ([#200591](https://github.com/pytorch/pytorch/pull/200591), @laithsakka)
- Fixes compiled conv2d backward returning channels-last grad_input strides under layout optimization, so strides now match eager. ([#198120](https://github.com/pytorch/pytorch/pull/198120), @MBUYt0n)
- Fixes a CUDA misaligned-address error in scaled dot product attention by skipping flash and cuDNN when q/k/v row starts aren't 16-byte aligned. ([#199304](https://github.com/pytorch/pytorch/pull/199304), @liangel-02)
- MPSInductor now computes in float32 after casts to fp16/bf16, fixing a bf16 compile failure and wrong fp16 results such as log1p returning 0 for small inputs. ([#200559](https://github.com/pytorch/pytorch/pull/200559), @Isalia20)
- ...plus 88 more commits ([full log]({{< relref "/full-log/2026-10-18#inductor-commits" >}}))

_In total, 62 Dynamo and 98 Inductor commits landed upstream this week._

_Notable commits per week (score 3+ of 5), last 8 weeks:_

```
        Dynamo                      Inductor
Aug 23  ██████▌                18   ██████████████▏        39
Aug 30  ███████▋               21   ██████████▏            28
Sep 06  ████                   11   ████████▋              24
Sep 13  ████▍                  12   █████▊                 16
Sep 20  █▏                     3    ██▏                    6
Oct 04  ██████████▌            29   ██████████████████████ 61
Oct 11  █████▊                 16   ████████████████████▉  58
Oct 18  █████████▊             27   ██████████████████▍    51
```
