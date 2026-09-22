---
name: React Engineering
description: React/Next.js methodology — composition, server vs client boundaries, state, data fetching, performance and verification. Use for React/Next work. Do not use for non-React UI. For multi-step features, use MAIN skill pixz.core.orchestrator.
version: 1.2.0
id: pixz.frontend.react
category: frontend
triggers: [react, next.js, component, hooks, react patterns]
compatible_runtimes: [claude, openclaw, opencode, hermes, codex, generic]
---

# React Engineering — `pixz.frontend.react`

> **Specialist HOW skill.** For practical multi-step operating methodology, activate the **MAIN skill** `pixz.core.orchestrator`. Load `core/orchestrator/references/operating-methodology.md` when the feature crosses data, auth, and UI.

## Purpose

Correct React/Next.js structure: server/client boundaries, minimal state, predictable data flow, measurable performance — not hook soup.

## When to Use / When NOT

| Use | Do not |
|-----|--------|
| Components, hooks, Next.js app/pages router, RSC, server actions | Vue/Svelte/plain HTML, backend-only work |
| State, effects, data fetching, hydration issues | "Change copy in a markdown file" |

Inspect the actual stack first (`pixz.core.environment-awareness`): App Router vs Pages, Next version, RSC availability. Do not assume Next.js 15 App Router.

## Methodology

### 1. Composition & boundaries

| Live here | Why |
|-----------|-----|
| Server Component (default in App Router) | Data fetch, secrets, no bundle cost |
| Client Component (`"use client"`) | State, effects, event handlers, browser APIs |
| Server Action / Route Handler | Mutations, revalidation |

Push `"use client"` to the **leaves**. Do not mark a whole page client because one button needs `onClick`.

Props vs context vs store: colocate state. Context for truly cross-tree values (theme, auth session). Stores for high-frequency client state. No prop-drilling heroics — lift only when evidence needs it.

### 2. Data

- Fetch on the server when possible. Cache/revalidate explicitly (`fetch` cache options, `revalidatePath`/`revalidateTag`).
- Parallelize independent fetches; do not waterfall.
- Handle `loading.tsx` / `error.tsx` / `not-found.tsx` for routes you touch.
- Keys: stable ids, never array index if the list can reorder.

### 3. Effects (the usual bug)

`useEffect` is for synchronizing with an *external* system, not for "run this when x changes" derived state. Derived data = compute during render. If an effect only sets state from props, it is probably a bug.

Always clean up subscriptions, timers, and GSAP tweens on unmount.

### 4. Performance

- Memo / `useMemo` / `useCallback` **only with measured gain** (profiler or a real wasted-render). Do not sprinkle.
- RSC streaming and Suspense boundaries around slow data, not around everything.
- Motion only on `transform`/`opacity` (`pixz.motion.gsap` if GSAP).
- Images: explicit size, modern format, no layout shift.

### 5. Correctness pitfalls

- Don't serialize non-plain data (classes, Dates without transform) across the RSC boundary.
- Don't read `searchParams` in a client child and also SSG the page without a plan.
- Don't put secrets in client components or `NEXT_PUBLIC_` without intent.
- Forms: prefer progressive enhancement (Server Actions) where the stack allows.

### 6. Verify

- Type-check (`tsc --noEmit` or the repo script).
- Unit + integration for hooks and critical flows.
- a11y per `pixz.frontend.accessibility`.
- Anti-slop: no abstraction astronautics (`pixz.quality.anti-ai-slop`).
- Manual: happy path, error path, loading, back-button, slow network.

## Failure Conditions

- Entire tree marked `"use client"` without a reason → redo boundaries.
- `useEffect` used to derive state → rewrite.
- Memo everywhere, no measurement → noise; remove.

## Example

> Add a filters bar to an App Router list page. Keep the page as a Server Component fetching data. Extract `<Filters>` as the client leaf. Update URL search params; server re-renders from `searchParams`. No global store. `loading.tsx` for the list slot only.

## Structured Output

```yaml
react_design:
  router: app|pages
  boundaries: [{file, server|client, reason}]
  state: {colocated, context, store}
  data: {where, cache, revalidate}
  verification: [tsc, tests, a11y]
  residual_risks: [...]
```

## Main Skill

A product feature (API + UI + a11y + tests) is orchestrator work. Activate `pixz.core.orchestrator`.
