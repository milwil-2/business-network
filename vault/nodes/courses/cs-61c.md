---
id: cs-61c
label: "CS 61C: Great Ideas in Computer Architecture"
node_type: Course
tags: [eecs, architecture, systems, Course]
properties:
  number: "CS 61C"
  department: "EECS"
  units: 4
summary: "A course on how programs map to hardware, covering machine representation, assembly, the memory hierarchy, and parallelism."
relationships:
  - type: PREREQUISITE_OF
    target: cs-162
  - type: PREREQUISITE_OF
    target: cs-164
  - type: PREREQUISITE_OF
    target: cs-161
  - type: PREREQUISITE_OF
    target: cs-168
  - type: COVERS
    target: caching
---

CS 61C explores the relationship between software and the hardware that runs it. Students learn how data is represented in binary, write RISC-V assembly, and understand how a compiler, assembler, and linker turn C into executable machine code.

A central theme is performance through the **memory hierarchy**: the course dives deep into [[caching]], virtual memory, and the latency tradeoffs that make or break real programs. Later units cover pipelining, parallelism with SIMD and threads, and the datacenter as a computer.

Building on [[cs-61b]], CS 61C is the systems foundation for [[cs-162]], [[cs-164]], [[cs-161]], and [[cs-168]], giving students the hardware intuition those courses assume.
