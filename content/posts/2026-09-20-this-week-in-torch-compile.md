---
title: "This week in torch.compile #7 - Sep 20"
date: 2026-09-20
---

_Covering 2026-09-13 to 2026-09-20._

## On the forums

Quiet week on [the compiler forum](https://dev-discuss.pytorch.org/c/compiler/5).

## Config changes
- new: `torch._inductor.config.compile_worker_mode`

## Dynamo commits
- Fixed guard-state serialization so shared singletons like `torch.float32` and `Ellipsis` are never pruned, which previously produced artifacts that failed to load with a dtype error. ([#197749](https://github.com/pytorch/pytorch/pull/197749), @bobrenjc93)
- Loading an AOT-compiled module whose forward is wrapped by `torch.compile` or `disable` now resolves the right guard scope instead of failing with a KeyError on user globals. ([#196908](https://github.com/pytorch/pytorch/pull/196908), @bobrenjc93)
- Fixed AOT-compiled artifacts serving the load-time value of a guarded global; the global is now re-read before every call, avoiding silently wrong numerics when it is rebound. ([#196897](https://github.com/pytorch/pytorch/pull/196897), @bobrenjc93)
- Function artifacts loaded with `f_globals` now also re-read guarded globals per call, closing the same silent wrong-numerics case on the function load path. ([#197218](https://github.com/pytorch/pytorch/pull/197218), @bobrenjc93)
- Fixed `torch.Tensor(torch.Size(...))` under Dynamo, which was treated as data and produced a tensor of the wrong shape instead of the requested size. ([#196717](https://github.com/pytorch/pytorch/pull/196717), @karatarassul4-max)
- Dynamo now models `OrderedSet` separately from `set`, preserving insertion order across the compile boundary in reconstruction and `repr`. ([#196167](https://github.com/pytorch/pytorch/pull/196167), @yashb98)
- Fixed `random.seed()` not affecting scalar draws like `random.random()` on the first compile, which gave results differing from eager. ([#197221](https://github.com/pytorch/pytorch/pull/197221), @aperson30)
- FlexGEMM now raises on backward under torch.compile instead of silently producing no gradients, and guards kernel_options keys. ([#196320](https://github.com/pytorch/pytorch/pull/196320), @drisspg)
- Loading an AOT-compiled module now resolves its guard scope from `model.forward`'s live globals, fixing both stale and missing global guards. ([#196818](https://github.com/pytorch/pytorch/pull/196818), @bobrenjc93)
- Fixed a Dynamo bug where compiling code after loading a previously saved compiled package could crash due to a global variable name collision, by minting names guaranteed unique to the target module. ([#196822](https://github.com/pytorch/pytorch/pull/196822), @bobrenjc93)
- ...plus 100 more commits ([full log]({{< relref "/full-log/2026-09-20#dynamo-commits" >}}))

## Inductor commits
- Added `_scaled_mm_v2` support for float8_e4m3fn on Apple MPS, with tensorwise and rowwise scaling, optional bias, and several output dtypes. ([#196916](https://github.com/pytorch/pytorch/pull/196916), @Isalia20)
- Inductor backend-specific config values can now be passed through `torch.compile(options={"<device>.<key>": ...})` for registered custom backends. ([#194998](https://github.com/pytorch/pytorch/pull/194998), @yeyehaha)
- NVGEMM migrated to the CUTLASS Operators package, with more epilogue fusion support, Hopper coverage, and re-enabled B200 CI. ([#194364](https://github.com/pytorch/pytorch/pull/194364), @crcrpar)
- Inductor, ROCm and flex attention no longer crash with a mixed-API error when fp32 matmul precision is set through the new per-backend `fp32_precision` API. ([#189955](https://github.com/pytorch/pytorch/pull/189955), @jeffdaily)
- New config `triton.cudagraph_initial_mempool_allocation_gb` primes the CUDA graph memory pool with one large allocation to reduce device memory fragmentation. ([#196378](https://github.com/pytorch/pytorch/pull/196378), @eellison)
- CPU Flash Attention now overlaps AMX matrix multiplies with AVX softmax, giving roughly 6-29% speedups on some BF16 shapes. ([#191780](https://github.com/pytorch/pytorch/pull/191780), @cfgfung)
- FlexGEMM now supports `F.grouped_mm` with variable-length M through QuACK, covering ragged experts and empty groups. ([#196318](https://github.com/pytorch/pytorch/pull/196318), @drisspg)
- FlexGEMM supports block-scaled GEMMs through QuACK, enabling a full low-precision dense MLP. ([#192839](https://github.com/pytorch/pytorch/pull/192839), @drisspg)
- Fixed a compile crash for floor division of fp16/bf16 aranges by keeping fp32 compute promotion in `value_expr`. ([#197132](https://github.com/pytorch/pytorch/pull/197132), @eellison)
- Fixed a bug in Inductor's CPU linear-layer weight packing where the bias device check compared against the wrong variable, so the check never actually validated the bias was on CPU. ([#195833](https://github.com/pytorch/pytorch/pull/195833), @gavinwang269)
- ...plus 69 more commits ([full log]({{< relref "/full-log/2026-09-20#inductor-commits" >}}))

_In total, 110 Dynamo and 79 Inductor commits landed upstream this week._

_Notable commits per week (score 3+ of 5), last 7 weeks:_

```
        Dynamo                      Inductor
Aug 09  ███████▍               14   █████████▍             18
Aug 16  ██████████▌            20   ██████████████████████ 42
Aug 23  █████████▍             18   ████████████████████▍  39
Aug 30  ███████████            21   ██████████████▋        28
Sep 06  █████▊                 11   ████████████▋          24
Sep 13  ██████▎                12   ████████▍              16
Sep 20  ████████████████████▍  39   ██████████████████████ 42
```
