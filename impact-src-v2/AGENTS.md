# Prototype Instructions

Run the local server yourself and open the preview in the browser available to this environment. Do not give the user server-start instructions when you can run it.

Before making substantial visual changes, use the Product Design plugin's `get-context` skill when the visual source is unclear or no longer matches the current goal. When the user gives durable prototype-specific design feedback, preferences, or decisions, record them in `AGENTS.md`.

When implementing from a selected generated mock, treat that image as the source of truth for layout, component anatomy, density, spacing, color, typography, visible content, and hierarchy.

Build app UI in `src/`. Keep `.openai/hosting.json`, `worker/index.js`, `scripts/prepare-sites-build.mjs`, and `tests/sites-worker.test.mjs` intact so the same local prototype can be handed to Sites. Before a Sites handoff, run `npm run build` and `npm run test:sites`; the build must leave `dist/client/index.html`, `dist/server/index.js`, and `dist/.openai/hosting.json`.

## Prototype-specific decisions

- Visual target: the selected Option 3 “Insight-to-Outcome System Map” mockup generated in this conversation.
- Content source: `https://shafaatalichoyon.com/impact.html` and the full experience arc at `https://shafaatalichoyon.com/?view=full#experience`.
- Include all 21 impact evidence points and the complete company/organization and tenure information from the 2009–present experience journey.
- Position growth as the deep, transferable capability and health as its deliberate application.
- HSREP must be described only as an independent public-health platform. Do not label it a company, startup, employer, founder role, or founding activity.
- Preserve four connected views: the original System Map, the T-shaped Impact Atlas, the Career Journey, and Two Markets.
- T-shaped Impact Atlas source: `/workspace/scratch/f3c5720d88bf/upload/T shaped.png`. It must support lens filtering, capability tracing, evidence inspection, comparison, zoom, and reset.
- Career Journey source: `/workspace/scratch/f3c5720d88bf/upload/Career journey.png`. It must organize the career into ten readable chapters while retaining all fourteen exact roles, companies, and tenures in the chapter inspector.
- HSREP's 57,274 figure must be described as gross platform-reported views and impressions, not unique people reached.
