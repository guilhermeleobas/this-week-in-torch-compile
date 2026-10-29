---
title: "This week in torch.compile #10 - Oct 11"
date: 2026-10-11
---

_Covering 2026-10-04 to 2026-10-11._

## News and Announcements

- [PyTorch 2.15 RC1 produced for pytorch, torchvision & torchaudio](https://dev-discuss.pytorch.org/t/pytorch-2-15-rc1-produced-for-pytorch-torchvision-torchaudio/3464)
- [PyTorch Release 2.15 Branch Cut is Complete](https://dev-discuss.pytorch.org/t/pytorch-release-2-15-branch-cut-is-complete/3461)

## On the forums

Quiet week on [the compiler forum](https://dev-discuss.pytorch.org/c/compiler/5).

## Config changes
- new: `torch._dynamo.config.use_cpp_fake_tensor`
- new: `torch._inductor.config.incremental_autotune_max_dispatches`
- new: `torch._inductor.config.strict_pointwise`
- new: `torch._inductor.config.strict_reduction`

## Dynamo commits
- Precompile can now save captures where a graph break happens inside a called function (such as a child module's forward) by writing them as installed-mode artifacts. ([#198523](https://github.com/pytorch/pytorch/pull/198523), @bobrenjc93)
- Dynamo no longer silently drops maxlen when replaying mutations on deque inputs, so bounded deques behave like eager. ([#200528](https://github.com/pytorch/pytorch/pull/200528), @XuehaiPan)
- Fx.traceback.annotate tags are now preserved across graph breaks instead of being lost or failing the frame. ([#198959](https://github.com/pytorch/pytorch/pull/198959), @enlighten5)
- The scan higher-order op now accepts inputs that are views of the same storage (such as K and V from a fused QKV projection) as long as none are mutated. ([#199688](https://github.com/pytorch/pytorch/pull/199688), @bohnstingl)
- Dynamo's has_torch_function now returns True while a TorchFunctionMode is active, so modes see calls following the standard override pattern. ([#196053](https://github.com/pytorch/pytorch/pull/196053), @ezyang)
- Dynamo can now trace torch.overrides.handle_torch_function, dispatching modes and subclass overrides like eager. ([#196055](https://github.com/pytorch/pytorch/pull/196055), @ezyang)
- Fixes compiled graphs that inlined a TorchFunctionMode running the mode a second time, which gave wrong results. ([#196056](https://github.com/pytorch/pytorch/pull/196056), @ezyang)
- Dynamo now raises the same TypeError as eager when a traced __init__ returns a non-None value, instead of silently succeeding. ([#198604](https://github.com/pytorch/pytorch/pull/198604), @hknsahin97-coder)
- Installed precompile artifacts now refuse recompiles with their own callback instead of toggling the process-global fail_on_recompile stance, which broke concurrent torch.compile calls in other threads. ([#198557](https://github.com/pytorch/pytorch/pull/198557), @bobrenjc93)
- Dynamo can now trace calls to a polyfilled function's __wrapped__ or __torch_dynamo_polyfill__ attributes when they are ordinary Python functions. ([#200361](https://github.com/pytorch/pytorch/pull/200361), @XuehaiPan)
- ...plus 19 more commits ([full log]({{< relref "/full-log/2026-10-11#dynamo-commits" >}}))

## Inductor commits
- Fixed a bug where, under CUDA graphs (reduce-overhead), a compiled function returning a CPU-constructed tensor returned a CUDA tensor instead. ([#199007](https://github.com/pytorch/pytorch/pull/199007), @oonyshch)
- Fixes AOTInductor compile errors with CUDA 13 headers for models whose Triton kernels take host TMA descriptors. ([#200323](https://github.com/pytorch/pytorch/pull/200323), @leimao)
- Fixed a graph partition (CUDA graphs) error when a graph output is the result of a mutating op such as the stateless RNG ops. ([#199171](https://github.com/pytorch/pytorch/pull/199171), @jbschlosser)
- Fixes a regression where pattern matching refused auto_functionalized nodes carrying default kwargs, which broke vLLM's fusion passes. ([#200442](https://github.com/pytorch/pytorch/pull/200442), @bobrenjc93)
- Fixes silent wrong results where decompose_addmm rewrote addmm calls with non-default alpha or beta as a plain matmul plus add. ([#196588](https://github.com/pytorch/pytorch/pull/196588), @christianaurichzm)
- User-defined Triton kernels autotuned through Inductor now keep each config's maxnreg register cap instead of silently compiling uncapped. ([#199849](https://github.com/pytorch/pytorch/pull/199849), @leimao)
- Fixes wrong results from Triton floor division when the minimum integer is divided by a negative divisor. ([#198598](https://github.com/pytorch/pytorch/pull/198598), @alepot55)
- Graphs containing with_effects now use the FX graph cache when the wrapped op is cacheable, avoiding minutes of recompilation per restart. ([#200187](https://github.com/pytorch/pytorch/pull/200187), @tanvigupta17)
- Fixes addmm and baddbmm so a NaN or inf bias is ignored when beta is zero, matching eager. ([#196600](https://github.com/pytorch/pytorch/pull/196600), @christianaurichzm)
- Torch.addmm with out_dtype now compiles in Inductor instead of crashing with a TypeError. ([#200194](https://github.com/pytorch/pytorch/pull/200194), @anijain2305)
- ...plus 89 more commits ([full log]({{< relref "/full-log/2026-10-11#inductor-commits" >}}))

_In total, 29 Dynamo and 99 Inductor commits landed upstream this week._

_Notable commits per week (score 3+ of 5), last 8 weeks:_

```
        Dynamo                      Inductor
Aug 16  ███████▎               20   ███████████████▏       42
Aug 23  ██████▌                18   ██████████████▏        39
Aug 30  ███████▋               21   ██████████▏            28
Sep 06  ████                   11   ████████▋              24
Sep 13  ████▍                  12   █████▊                 16
Sep 20  █▏                     3    ██▏                    6
Oct 04  ██████████▌            29   ██████████████████████ 61
Oct 11  █████▊                 16   ████████████████████▉  58
```
