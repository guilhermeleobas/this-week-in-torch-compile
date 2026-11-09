---
title: "This week in torch.compile #13 - Nov 01"
date: 2026-11-01
---

_Covering 2026-10-25 to 2026-11-01._

## News and Announcements

- [PyTorch 2.15.0 General Availability](https://dev-discuss.pytorch.org/t/pytorch-2-15-0-general-availability/3470)

## On the forums

Quiet week on [the compiler forum](https://dev-discuss.pytorch.org/c/compiler/5).

## Config changes
- new: `torch._inductor.config.max_autotune_gemm_min_sms`

## Dynamo commits
- Fixes a Python 3.14 crash and missed cache hits where a garbage-collected guard manager was freed while Dynamo was still evaluating a cache entry. ([#199820](https://github.com/pytorch/pytorch/pull/199820), @itamaro)
- Fixes unnecessary recompilation in Dynamo when slices have dynamic bounds, so such functions now compile once. ([#202378](https://github.com/pytorch/pytorch/pull/202378), @khushi-411)
- Fixes compiled torch.cuda.synchronize() on an index-less device to sync the caller's current device instead of always device 0. ([#197384](https://github.com/pytorch/pytorch/pull/197384), @aorenste)
- Fixes Dynamo silently taking the wrong branch for `if x:` when truthiness isn't a constant, which gave wrong results for values like range or dict.keys() inputs. ([#202375](https://github.com/pytorch/pytorch/pull/202375), @hameerabbasi)
- Torch.compiler.precompile.capture() now accepts torch.compile's mode= and options= so models can be precompiled with settings like max-autotune. ([#201940](https://github.com/pytorch/pytorch/pull/201940), @bobrenjc93)
- Deletes the legacy, never-launched TorchScript graph-mode quantization workflows (about 11k lines), a BC-breaking removal from the public API. ([#201696](https://github.com/pytorch/pytorch/pull/201696), @vkuzo)
- Fixes Dynamo's itertools.product with repeat=0 so it no longer consumes the input iterators, matching CPython. ([#201609](https://github.com/pytorch/pytorch/pull/201609), @mottopanikeiku)
- Precompiled Dynamo artifacts now import the modules that register custom ops, so replay of functions calling only torch.ops.<ns>.<op> no longer fails. ([#202258](https://github.com/pytorch/pytorch/pull/202258), @bobrenjc93)
- Adds extra Dynamo guards on dictionary length so compiled code is correct when dict sizes change. ([#202374](https://github.com/pytorch/pytorch/pull/202374), @hameerabbasi)
- Fixes a Dynamo crash on `not obj` when a user-defined object's truthiness is symbolic after a recompile. ([#202376](https://github.com/pytorch/pytorch/pull/202376), @hameerabbasi)
- ...plus 43 more commits ([full log]({{< relref "/full-log/2026-11-01#dynamo-commits" >}}))

## Inductor commits
- Adds an Inductor option, triton.enable_fp_fusion, to turn off fused multiply-add contraction so kernels give identical bits regardless of which autotuned config is picked. ([#202218](https://github.com/pytorch/pytorch/pull/202218), @dmdok)
- Fixes dropout on CUDA under-reserving random number generator offsets in vectorized kernels, which made the next random call reuse values. ([#202606](https://github.com/pytorch/pytorch/pull/202606), @jbschlosser)
- Fixes Inductor wrongly removing a clone whose storage offset differs from its source, which gave wrong results for as_strided and user Triton kernels. ([#202409](https://github.com/pytorch/pytorch/pull/202409), @zztbit)
- A new Inductor config makes the minimum SM (streaming multiprocessor) count for is_big_gpu adjustable, so Jetson-class GPUs can use max-autotune GEMM templates instead of silently falling back to ATen. ([#201583](https://github.com/pytorch/pytorch/pull/201583), @andriidrok1)
- Inductor now rounds the conv bias add to the fp16/bf16 conv dtype before fusion, so compiled numerics match eager regardless of whether the conv output is saved for backward. ([#201713](https://github.com/pytorch/pytorch/pull/201713), @KarhouTam)
- Reverts the change that prefetched Inductor cache keys in a background thread at torch.compile() time, because it caused vLLM CI hangs on builds including it (nightlies since 20261001, release/2.15). ([#202167](https://github.com/pytorch/pytorch/pull/202167), @atalman)
- Inductor's CUDA Triton conv templates now use TF32 when eager cuDNN convolutions do, so max-autotune compares like-for-like precision against cuDNN. ([#201774](https://github.com/pytorch/pytorch/pull/201774), @shoumikhin)
- Fixes a NameError in generated code when a user Triton kernel receives a NamedTuple constexpr argument whose type was missing from the generated namespace. ([#192531](https://github.com/pytorch/pytorch/pull/192531), @sankalpsthakur)
- The compiled binary_cross_entropy now raises on out-of-range inputs like eager does, instead of silently computing. ([#200512](https://github.com/pytorch/pytorch/pull/200512), @KarhouTam)
- Adds a wave32 WMMA int4 matrix-multiply path on ROCm so int4mm works on RDNA (gfx11/gfx12) and gfx1250 GPUs. ([#201248](https://github.com/pytorch/pytorch/pull/201248), @jeffdaily)
- ...plus 61 more commits ([full log]({{< relref "/full-log/2026-11-01#inductor-commits" >}}))

_In total, 53 Dynamo and 71 Inductor commits landed upstream this week._

_Notable commits per week (score 3+ of 5), last 8 weeks:_

```
        Dynamo                      Inductor
Sep 13  ████▍                  12   █████▊                 16
Sep 20  ██████████████▏        39   ███████████████▏       42
Sep 27  █████████████          36   ██████████████▍        40
Oct 04  ██████████▌            29   ██████████████████████ 61
Oct 11  █████▊                 16   ████████████████████▉  58
Oct 18  █████████▊             27   ██████████████████▍    51
Oct 25  ██▉                    8    ███████████▏           31
Nov 01  █████████▊             27   █████████████▊         38
```
