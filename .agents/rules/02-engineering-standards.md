---
name: engineering-standards
description: Senior-engineer coding standards, asynchronous convergence budgets, settle windows, and spec documentation vocabulary.
trigger: always_on
---

# Engineering Standards & Asynchronous Convergence

## 1. Asynchronous Convergence & Settle Budgets
- **Non-Instantaneous State**: Infrastructure provisioning, background worker jobs, database indexing, and SPA route rendering take physical time. Never assert state immediately after triggering a mutation.
- **Explicit Polling Budgets**: Implement explicit polling loops with configured timeout budgets (e.g., 60s–180s budget at 5s–10s intervals) checking for affirmative steady-state convergence (`ACTIVE`, `READY`, `200 OK`).
- **Gracious Settle Windows**:
  - Web UI: Allow a 3000ms–6000ms settle delay after heavy client route switches or drawer transitions before testing interactivity.
  - Backend Services: Allow 10s–30s settle periods post-healthcheck before running concurrent load assertions.
  - Teardown: Confirm complete resource release before declaring a test complete.

## 2. Senior-Engineer Specification Vocabulary
- Maintain clear architectural commentary explaining *intent*, *constraints*, and *edge cases*.
- Avoid fluffy conversational filler in code, docs, and pull requests.
- Use precise technical terminology:
  - *ingest, reconcile, serialize, affirmative teardown, steady-state convergence, idempotent resumption, telemetry sanitization*.
