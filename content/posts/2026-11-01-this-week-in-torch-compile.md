---
title: "This week in torch.compile #13 - Nov 01"
date: 2026-11-01
---

_Covering 2026-10-25 to 2026-11-01._

## News and Announcements

<!-- editorial: releases, RFCs, blog posts, talks, announcements. Delete section if empty. -->

- [PyTorch 2.15.0 General Availability](https://dev-discuss.pytorch.org/t/pytorch-2-15-0-general-availability/3470)

## On the forums

Quiet week on [the compiler forum](https://dev-discuss.pytorch.org/c/compiler/5).

## Config changes
- new: `torch._inductor.config.max_autotune_gemm_min_sms`

## Dynamo commits
- Out-of-tree backends such as Ascend NPU (torch_npu) now have their current_stream registered with Dynamo, fixing a crash in wait_stream calls inside compiled functions. ([#192970](https://github.com/pytorch/pytorch/pull/192970), @AAYESLY)
- Dynamo now keeps true division, floor division and modulo by constant divisors lazy on lazy integer constants, avoiding value guards and the recompiles they cause. ([#198992](https://github.com/pytorch/pytorch/pull/198992), @guan404ming)
- Dynamo now keeps str() and bitwise invert lazy on lazy integer constants, avoiding value guards and recompiles, and handles symbolic values without sending the whole frame to eager. ([#198988](https://github.com/pytorch/pytorch/pull/198988), @guan404ming)
- Dynamo's saved_tensors_hooks guard now invalidates when a guarded hook is freed, preventing a new hook reusing the old address from running a graph compiled for the old hook. ([#202143](https://github.com/pytorch/pytorch/pull/202143), @chinmaydk99)
- Dynamo can now trace repr() and str() of mappingproxy objects (such as class dictionaries) instead of graph breaking. ([#196902](https://github.com/pytorch/pytorch/pull/196902), @weicheng-hsu)
- Dynamo no longer builds a length guard for iterables passed to list(), so objects with __iter__ but no __len__ now work as in eager. ([#201070](https://github.com/pytorch/pytorch/pull/201070), @riccardofelluga)
- Dynamo now supports bytearray.insert() and pop() without graph breaks. ([#199810](https://github.com/pytorch/pytorch/pull/199810), @jayzuccarelli)
- Dynamo now supports bytearray.split and rsplit with constant arguments without graph breaks. ([#200612](https://github.com/pytorch/pytorch/pull/200612), @Sanskaaar1)
- Enables more tests on s390x by adding a cache-size query for that platform and making the test shim link libdl explicitly. ([#198886](https://github.com/pytorch/pytorch/pull/198886), @AlekseiNikiforovIBM)
- Fixes a flaky Dynamo random-draw test by compiling with a warm-up call before reseeding the RNG. ([#202224](https://github.com/pytorch/pytorch/pull/202224), @ezyang)
- ...plus 1 more commits ([full log]({{< relref "/full-log/2026-11-01#dynamo-commits" >}}))

## Inductor commits
- A new Inductor config makes the minimum SM (streaming multiprocessor) count for is_big_gpu adjustable, so Jetson-class GPUs can use max-autotune GEMM templates instead of silently falling back to ATen. ([#201583](https://github.com/pytorch/pytorch/pull/201583), @andriidrok1)
- Inductor now rounds the conv bias add to the fp16/bf16 conv dtype before fusion, so compiled numerics match eager regardless of whether the conv output is saved for backward. ([#201713](https://github.com/pytorch/pytorch/pull/201713), @KarhouTam)
- Reverts the change that prefetched Inductor cache keys in a background thread at torch.compile() time, because it caused vLLM CI hangs on builds including it (nightlies since 20261001, release/2.15). ([#202167](https://github.com/pytorch/pytorch/pull/202167), @atalman)
- Inductor's CUDA Triton conv templates now use TF32 when eager cuDNN convolutions do, so max-autotune compares like-for-like precision against cuDNN. ([#201774](https://github.com/pytorch/pytorch/pull/201774), @shoumikhin)
- Fixes a NameError in generated code when a user Triton kernel receives a NamedTuple constexpr argument whose type was missing from the generated namespace. ([#192531](https://github.com/pytorch/pytorch/pull/192531), @sankalpsthakur)
- The compiled binary_cross_entropy now raises on out-of-range inputs like eager does, instead of silently computing. ([#200512](https://github.com/pytorch/pytorch/pull/200512), @KarhouTam)
- Inductor now includes a Triton config's extra_options in its identity, so configs that differ only in those options are no longer conflated; configs with non-empty options get new autotune hashes and old tuning records are invalidated. ([#201695](https://github.com/pytorch/pytorch/pull/201695), @luochao-dev)
- Max-autotune for reductions now always keeps the default persistent-reduction config in its search, so the search space is a superset of the default one. ([#194887](https://github.com/pytorch/pytorch/pull/194887), @shino16)
- On MPS, each Inductor Metal kernel now has its own headers set, so kernels without asserts no longer get an unused error_buf parameter after another kernel added the error header. ([#202232](https://github.com/pytorch/pytorch/pull/202232), @Isalia20)
- Fixes Flex Flash score_mod vector widths under max_autotune on Hopper-class GPUs, where unsupported vec_size 4 raised an error during lowering. ([#202123](https://github.com/pytorch/pytorch/pull/202123), @Aidyn-A)
- ...plus 12 more commits ([full log]({{< relref "/full-log/2026-11-01#inductor-commits" >}}))

_In total, 11 Dynamo and 22 Inductor commits landed upstream this week._

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
Nov 01  ██▏                    6    ████▊                  13
```
