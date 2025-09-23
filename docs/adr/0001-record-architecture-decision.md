# 1. Record Architecture Decision

## Context
We needed to choose a programming language and architecture for the Mars Rover Kata.

## Why Ports & Adapters?

- **Testability**: Core rules are pure and framework-free; easy to unit test.
- **Swap policies**: Grid navigation (bounds), collisions, or wraps can be swapped without touching business logic.
- **Keep the UI**: We kept our teammate’s  `main.py` / `main_enhanced.py` / `visualizer.py` look & feel by adding a tiny **compat** adapter instead of rewriting the UI.
- **Future-proof**: We can add a web UI, different CLIs, or file formats by creating new adapters.

## Architecture Overview

- **Ports** (`hexrover/ports.py`) — `Navigator` protocol, `Position`, `Heading`.
- **Domain** (`hexrover/domain.py`) — immutable `Rover` applying `L/R/M` via a `Navigator`; no UI/IO deps.
- **Adapters** (`hexrover/adapters/*`) — implement `Navigator` and orchestration (e.g., `GridNavigator`, `CollisionNavigator`, `MissionController`).
- **Compat** (`hexrover/compat/*`) — exposes the legacy `Rover`/`Plateau` API so the **existing UI** continues to work unchanged.

## Why Use Compat?
- **Preserve the old UI & output format exactly**
- **Minimize churn**: you only changed 2 import lines instead of rewriting the UIs.
- **Clean architecture**: the domain stays pure; UI calls the compat shim (an adapter), which delegates to: 
  - domain (hexrover/domain.py)
  - policy adapters (hexrover/adapters/grid_nav.py, etc.)