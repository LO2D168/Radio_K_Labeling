# Agent Instructions

These instructions adapt the behavioral guidelines from
[`multica-ai/andrej-karpathy-skills`](https://github.com/multica-ai/andrej-karpathy-skills/blob/main/CLAUDE.md)
for OpenCode. Apply them together with the task requested by the user.

## Think Before Coding

- State important assumptions before implementing.
- If the request has multiple plausible interpretations, identify them and ask
  instead of silently choosing one.
- Prefer the simplest approach that satisfies the request.
- Surface uncertainty and tradeoffs before making a consequential change.

## Simplicity First

- Implement only what was requested.
- Avoid speculative features, abstractions, configurability, and error handling
  for impossible scenarios.
- Keep one-off logic local unless reuse or composition is clearly needed.
- If an implementation is substantially longer than necessary, simplify it.

## Surgical Changes

- Touch only files required for the task.
- Preserve the existing style and structure of this repository.
- Do not refactor adjacent code, formatting, comments, or dead code unrelated to
  the request.
- Remove imports, variables, or functions made unused by your own changes.
- Do not remove pre-existing dead code unless explicitly requested.

## Goal-Driven Execution

- Define a concrete success check for every change.
- For bug fixes, reproduce the problem with a focused test or command when
  practical, then verify the fix.
- For refactors, verify behavior before and after when practical.
- Run the narrowest relevant validation first, followed by broader checks when
  available.
- Report validation commands and any checks that could not be run.

## Repository Context

- This repository contains Python implementations for radio k-labeling using
  SAT and CPLEX/Gurobi-based methods, plus graph instances under `dataset/`.
- Keep changes scoped to the specific solver/method and model version involved;
  do not assume that similarly named implementations are interchangeable.
- Check local imports, relative paths, solver availability, and input-file
  expectations before changing execution code.
- Do not modify files under `dataset/` unless the user explicitly asks for data
  changes.
