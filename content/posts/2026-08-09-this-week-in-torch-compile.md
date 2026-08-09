---
title: "This week in torch.compile #1 - Aug 09"
date: 2026-08-09
---

_Covering 2026-08-02 to 2026-08-09._

## News and Announcements

<!-- editorial: releases, RFCs, blog posts, talks, announcements. Delete section if empty. -->

## On the forums

Quiet week on [the compiler forum](https://dev-discuss.pytorch.org/c/compiler/5).

## Config changes
- new: `torch._inductor.config._partitioned_scatter_default`
- new: `torch._inductor.config.partitioned_scatter_force`
- new: `torch._inductor.config.partitioned_scatter_min_contention_ratio`
- new: `torch._inductor.config.partitioned_scatter_min_index_size`
- new: `torch._inductor.config.partitioned_scatter_non_model_floor_bytes`
- removed: `torch._inductor.config.partitioned_scatter_memory_budget`

## Dynamo commits
- Fixes ahead-of-time compile guard serialization for functions using torch.func transforms (vmap, grad, jvp), which previously failed because an unserializable dictionary-version guard was used and stale guard state leaked between guard builds. ([#191428](https://github.com/pytorch/pytorch/pull/191428), @deckpulse)
- Torch.compile can now be applied directly on top of a @staticmethod, which previously silently fell back to eager or errored with fullgraph=True. ([#190673](https://github.com/pytorch/pytorch/pull/190673), @HussainNizamani)
- Has_triton() now discovers Triton support by querying registered device interfaces instead of a hardcoded device list, so out-of-tree accelerator backends (PrivateUse1) work without monkeypatching. ([#190324](https://github.com/pytorch/pytorch/pull/190324), @05mengmeizi)
- Fixes Dynamo replaying a fake placeholder script object into Python code when a value-opaque object was both a graph output and tensor-subclass metadata; the real value is now unwrapped consistently. ([#187057](https://github.com/pytorch/pytorch/pull/187057), @jansel)
- Attribute writes on collections.deque inside compiled code now raise AttributeError matching CPython behavior instead of triggering a graph break. ([#191405](https://github.com/pytorch/pytorch/pull/191405), @guilhermeleobas)
- Dynamo now handles unbound rich-comparison calls like complex.__eq__(a, b) on int/float/complex constants, which previously errored or graph-broke. ([#191406](https://github.com/pytorch/pytorch/pull/191406), @guilhermeleobas)
- Fixes a large per-call overhead in nested compile region reuse checks: fingerprinting arguments that need pytree flattening (dataclasses, namedtuples) no longer bytecode-traces the flattening code on every invocation. ([#191817](https://github.com/pytorch/pytorch/pull/191817), @aperson30)
- Nested compile regions (invoke_subgraph) now accept user-defined objects as inputs when the object is reachable from a guarded source, and sourceless nn.Modules that were previously accepted without safety checks are now rejected. ([#192003](https://github.com/pytorch/pytorch/pull/192003), @anijain2305)
- Fixes unsafe reuse of nested compile regions that read a global variable rebound between calls; global loads and stores are now tracked so mutation is detected. ([#192006](https://github.com/pytorch/pytorch/pull/192006), @anijain2305)
- Fixes nested compile regions failing to compile when they read a transposed view of a captured buffer (like x @ self.w.T), caused by the transpose node being emitted in the wrong graph. ([#191785](https://github.com/pytorch/pytorch/pull/191785), @anijain2305)
- ...plus 18 more commits

## Inductor commits
- Adds ctx.set_output_grad_dtype to autograd.Function, letting an output declare what dtype its incoming gradient should be converted to, independently of the output's own storage dtype. ([#189634](https://github.com/pytorch/pytorch/pull/189634), @SongyuanZhao)
- FlexGEMM gains fused epilogue lowerings for the MX FP8 (E8M0 scale) and NVFP4 (E4M3 scale) quantization ops, so float8/float4 quantization can fuse into the matmul instead of running as separate kernels. ([#188739](https://github.com/pytorch/pytorch/pull/188739), @drisspg)
- FlexGEMM now supports contracted main outputs along the N dimension, enabling fused epilogues like SwiGLU and similar gated activations directly in the GEMM. ([#190158](https://github.com/pytorch/pytorch/pull/190158), @drisspg)
- Fixes silent wrong results in mix-order reduction loops when Triton tensor-memory-accelerator descriptors are enabled: the scalar offset was never advanced inside the loop, so every iteration read and wrote the same first tile. ([#192344](https://github.com/pytorch/pytorch/pull/192344), @jananisriram)
- Fixes an Inductor lowering bug where float8 inputs were wrongly rejected on GPUs older than sm89 even though the uint8-storage conversion path for float8 is valid there. ([#189561](https://github.com/pytorch/pytorch/pull/189561), @gderossi)
- FlexGEMM can now write packed NVFP4 (two 4-bit E2M1 values per byte) directly as the matmul output using Blackwell's native packed conversion, eliminating a separate quantization kernel. ([#191270](https://github.com/pytorch/pytorch/pull/191270), @drisspg)
- Fixes Inductor codegen for user-defined Triton kernels whose metadata contains Python Enum values, which previously serialized to invalid Python source like '<RoundingMode.even: 2>'. ([#189494](https://github.com/pytorch/pytorch/pull/189494), @mmarthmm)
- Re-lands the removal of eager Triton bundle loading during cache-artifact population, which raced with compilation and caused segfaults; kernels now fall back to safe just-in-time loading. ([#192526](https://github.com/pytorch/pytorch/pull/192526), @warrendeng)
- Inductor now runs its peak-memory reordering pass before foreach-kernel combo formation, recovering scheduling freedom that combos previously hid and cutting peak memory by up to ~40 MiB on benchmark graphs. ([#192449](https://github.com/pytorch/pytorch/pull/192449), @karthickai)
- Adds common-subexpression elimination for repeated captured-tensor loads in CuTeDSL FlexAttention modification code, trimming generated code and measurably speeding up first compile. ([#192247](https://github.com/pytorch/pytorch/pull/192247), @drisspg)
- ...plus 27 more commits

_In total, 28 Dynamo and 37 Inductor commits landed upstream this week._
