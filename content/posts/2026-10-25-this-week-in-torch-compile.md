---
title: "This week in torch.compile #12 - Oct 25"
date: 2026-10-25
---

_Covering 2026-10-18 to 2026-10-25._

## News and Announcements

- [PyTorch 2.15 Final RC Available](https://dev-discuss.pytorch.org/t/pytorch-2-15-final-rc-available/3466)

## On the forums

Quiet week on [the compiler forum](https://dev-discuss.pytorch.org/c/compiler/5).

## Dynamo commits
- Dynamo now infers torch.full's dtype from a Tensor scalar fill value the way eager does, instead of defaulting to float. ([#199433](https://github.com/pytorch/pytorch/pull/199433), @haojiang01)
- Precompile now records frames Dynamo fell back to eager on, so a loaded artifact runs them eagerly instead of refusing the call. ([#201314](https://github.com/pytorch/pytorch/pull/201314), @bobrenjc93)
- Reduces the cost of Dynamo's autocast state guard by cutting thread-local storage lookups. ([#200299](https://github.com/pytorch/pytorch/pull/200299), @benjaminglass1)
- Dynamo can now trace bytearray.rindex, including start/end arguments and error behavior. ([#201363](https://github.com/pytorch/pytorch/pull/201363), @stefanind)
- Exceptions raised while Dynamo traces a class definition now reach the traced program's try/except instead of escaping the compiled region. ([#195626](https://github.com/pytorch/pytorch/pull/195626), @gabrielfruet)
- Dynamo's default repr and str for traced objects now follow CPython's object_repr with a placeholder address instead of baking one instance's address into reused graphs. ([#200001](https://github.com/pytorch/pytorch/pull/200001), @guilhermeleobas)
- Dynamo guards on a DistributedDataParallel module using a non-default process group can now be serialized, so precompile no longer bypasses those frames. ([#201319](https://github.com/pytorch/pytorch/pull/201319), @bobrenjc93)
- Precompile artifacts now keep identity guards on objects like typing.List that pickle as references to themselves, instead of reporting them as risky drops. ([#201315](https://github.com/pytorch/pytorch/pull/201315), @bobrenjc93)
- Shaves a bit more warm-cache overhead from Dynamo's get_backend by using a cheaper attribute lookup. ([#200300](https://github.com/pytorch/pytorch/pull/200300), @benjaminglass1)
- Moves repr cycle detection into each container's tp_repr in Dynamo, fixing wrong placeholders for self-referential list and dict subclasses. ([#200003](https://github.com/pytorch/pytorch/pull/200003), @guilhermeleobas)
- ...plus 9 more commits ([full log]({{< relref "/full-log/2026-10-25#dynamo-commits" >}}))

## Inductor commits
- Inductor's generated Python wrapper now defines Triton kernels as ordinary module-level functions by default, making the output readable and editable instead of burying kernels in string literals. ([#200502](https://github.com/pytorch/pytorch/pull/200502), @bobrenjc93)
- Fixes a NameError in generated code when a user Triton kernel receives a NamedTuple constexpr argument whose type was missing from the generated namespace. ([#192531](https://github.com/pytorch/pytorch/pull/192531), @sankalpsthakur)
- The compiled binary_cross_entropy now raises on out-of-range inputs like eager does, instead of silently computing. ([#200512](https://github.com/pytorch/pytorch/pull/200512), @KarhouTam)
- Inductor now keeps reset_to_zero and restore_value when rebuilding a user Triton Autotuner, fixing wrong gradients with autotuned kernels. ([#200358](https://github.com/pytorch/pytorch/pull/200358), @eshoyuan)
- Fixes max-autotune benchmark inputs for sliced views whose as_strided offset is rebased to a negative value. ([#200911](https://github.com/pytorch/pytorch/pull/200911), @KarhouTam)
- Fixes wrong results with triton.multi_kernel=1 where a subgraph's kernel names collided with and shadowed the parent's. ([#200214](https://github.com/pytorch/pytorch/pull/200214), @jananisriram)
- Fixes wrong results on MPS when a reduction is fused with index_add or scatter_add, where every thread added the value and scaled the result. ([#201460](https://github.com/pytorch/pytorch/pull/201460), @indrajeetapache)
- Fixes a device-memory leak in AOTInductor GPU wrappers where fallback kernel codegen created tensor handles that were never freed on every forward. ([#201267](https://github.com/pytorch/pytorch/pull/201267), @aaronenyeshi)
- Fixes a compile crash when a prologue fused into a Triton matmul contains a float16 or bfloat16 rounding cast. ([#201029](https://github.com/pytorch/pytorch/pull/201029), @shoumikhin)
- Fixes flex attention decoding so the safe-boundary setting is computed from each config's own BLOCK_M, which previously failed when BLOCK_M was pinned to a non-default value. ([#201328](https://github.com/pytorch/pytorch/pull/201328), @felipemello1)
- ...plus 39 more commits ([full log]({{< relref "/full-log/2026-10-25#inductor-commits" >}}))

_In total, 19 Dynamo and 49 Inductor commits landed upstream this week._

_Notable commits per week (score 3+ of 5), last 8 weeks:_

```
        Dynamo                      Inductor
Aug 30  ███████▋               21   ██████████▏            28
Sep 06  ████                   11   ████████▋              24
Sep 13  ████▍                  12   █████▊                 16
Sep 20  █▏                     3    ██▏                    6
Oct 04  ██████████▌            29   ██████████████████████ 61
Oct 11  █████▊                 16   ████████████████████▉  58
Oct 18  █████████▊             27   ██████████████████▍    51
Oct 25  ██▉                    8    ███████████▏           31
```
