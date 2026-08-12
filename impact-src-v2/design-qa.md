# Design QA — Impact Map Extension

## Comparison targets

### T-shaped Impact Atlas

- Source visual truth: `/workspace/scratch/f3c5720d88bf/upload/T shaped.png`
- Browser-rendered implementation: `/workspace/scratch/f3c5720d88bf/impact-system-map/qa-atlas-implementation-pass2.jpg`
- Full-view comparison: `/workspace/scratch/f3c5720d88bf/impact-system-map/qa-atlas-comparison-pass2.png`
- Focused canvas comparison: `/workspace/scratch/f3c5720d88bf/impact-system-map/qa-atlas-focus-pass2.png`
- State: T-shaped atlas · All evidence · Praava selected · no comparison open

### Career Journey

- Source visual truth: `/workspace/scratch/f3c5720d88bf/upload/Career journey.png`
- Browser-rendered implementation: `/workspace/scratch/f3c5720d88bf/impact-system-map/qa-career-implementation-pass2.jpg`
- Full-view comparison: `/workspace/scratch/f3c5720d88bf/impact-system-map/qa-career-comparison-pass2.png`
- Focused timeline comparison: `/workspace/scratch/f3c5720d88bf/impact-system-map/qa-career-focus-pass2.png`
- State: Career Journey · All lenses · Laser Treat chapter selected · detail inspector open

## Viewport and normalization

- Source dimensions: 1487 × 1058 px for each reference.
- Browser CSS viewport: 1363 × 936 px at device-pixel ratio 1.
- Browser screenshot dimensions: 1348 × 926 px for each implementation capture; the remaining width is occupied by browser scrollbar/chrome behavior.
- Normalized source dimensions: 1348 × 926 px, produced by proportional width resize followed by a north-aligned crop.
- Comparisons therefore use equal 1348 × 926 px source and implementation panels at density 1.

## Findings

- No actionable P0, P1, or P2 issue remains.
- Fonts and typography: Manrope provides the display hierarchy and Inter provides compact UI and evidence text. Weight, wrapping, line height, and hierarchy closely follow both references.
- Spacing and layout rhythm: hero, proof row, navigation, canvas, inspector, and legend proportions align with the normalized references. Neither final view introduces page-level horizontal overflow at the QA viewport.
- Colors and visual tokens: obsidian, navy, teal, amber, blue, ivory, and muted slate remain consistent with the original prototype and both references. Selected, compared, filtered, and dimmed states retain sufficient contrast.
- Image and icon fidelity: neither reference contains photographic or raster UI assets. Tabler icons and React Flow connections reproduce the reference icon language without placeholder graphics or handcrafted SVG assets.
- Copy and content: visual copy follows the references while exact evidence, company names, roles, and tenures come from the verified Impact and Experience data. HSREP is described only as an independent public-health platform. Its 57,274 figure is qualified as gross platform-reported views and impressions.

## Comparison history

### Pass 1

Observed:

- [P2] Career Journey hero: placing navigation beside the hero shortened the copy column and wrapped the supporting sentence, unlike the reference.
- [P2] Career Journey breadth row: repeated Digital and Health Communication labels created denser capability content than the reference.
- [P2] Career Journey year axis: the fixed minimum width plus margins produced an internal horizontal scrollbar at the desktop QA viewport.
- [P2] T-shaped Atlas inspector: three additional metric cards made the inspector taller and denser than the reference and introduced internal scrolling.
- [P2] T-shaped Atlas connections: invalid edge and directional-handle configuration generated React Flow warnings and prevented several left-side growth paths from rendering.

Fixed:

- Moved the Career Journey navigation into the panel toolbar and restored a full-width hero.
- Suppressed duplicate capability labels while preserving their milestone connections.
- Recalculated the year rail width against the available canvas width; final overflow is zero pixels at the QA viewport.
- Removed the atlas metric stack and retained evidence access through the inspector CTA and comparison control.
- Replaced unsupported edge types and added valid left/right source and target handles.

Post-fix evidence:

- `qa-career-comparison-pass2.png` and `qa-career-focus-pass2.png`
- `qa-atlas-comparison-pass2.png` and `qa-atlas-focus-pass2.png`

### Pass 2

- No P0, P1, or P2 mismatch remains.
- P3: the Atlas uses a node-based orange growth spine instead of the reference's enclosing orange capsule. The hierarchy remains equally legible and supports interactive tracing.
- P3: navigation contains four views rather than the three shown in each new reference because the already-built System Map remains available alongside the two new pages and Two Markets.
- Intentional: several illustrative reference labels were replaced with exact verified metrics.
- Intentional: the Career Journey inspector includes the exact role, organization, and tenure stack so all 14 experience entries remain available through the 10 readable chapters.

## Primary interactions tested

- Switched among System Map, T-shaped Atlas, Career Journey, and Two Markets.
- Filtered the Atlas by Growth, Health, Operations, Technology, and Population.
- Selected applied-sector nodes and verified the inspector changed to the corresponding case.
- Opened and closed the accessible case-comparison control; compared nodes and inspector evidence updated.
- Verified capability hover/click tracing, zoom controls, fit view, and reset view.
- Filtered the Career Journey by Growth, Health, Operations, Tech, and Population.
- Selected all 10 journey milestones; their chapter role counts total 14: `1, 3, 2, 1, 1, 1, 1, 2, 1, 1`.
- Verified exact company, role, and tenure information in each chapter inspector.
- Closed and reopened the Career Journey inspector and advanced with Next result.
- Opened the evidence ledger from Career Journey and confirmed all 21 evidence cards were present.
- Rechecked the original System Map and both Two Markets cards after integration.
- Checked a fresh cloud-browser tab after final fixes: no application console errors or warnings were present. An unrelated Chrome-extension metadata error was excluded.

## Result

final result: passed
