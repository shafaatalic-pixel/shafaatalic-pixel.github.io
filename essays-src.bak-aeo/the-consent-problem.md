---
slug: the-consent-problem
title: The consent problem - health AI's real bottleneck
lens: ai
date: 2026-08-06
dek: Every debate about health AI fixates on accuracy. What actually stalls it is trust by design: consent, privacy, and provenance: the layer nobody demos.
og: /assets/og/the-consent-problem.png
figure: /assets/og/the-consent-problem.png
figureAlt: The consent problem, health AI's bottleneck isn't accuracy, it's consent, privacy and provenance; trust by design.
figureCaption: The real gate, at a glance, click to enlarge.
keywords: health AI, consent, privacy, data governance, trust by design, provenance, HIPAA, AI in production, dual-market
readmin: 6
search: consent problem health ai accuracy privacy provenance trust by design surecash financial data hipaa data governance
---

Every debate about health AI fixates on accuracy, is the model right often enough to be safe? It's the wrong obsession. The thing that actually stalls health AI in the real world isn't usually a wrong answer. It's an unanswered question: does the person know, and agree to, what's happening with their data? Accuracy is necessary. It has never been sufficient.

## Accuracy gets you a demo; consent gets you deployed

A model can be brilliant and still be dead on arrival if patients, clinicians, or regulators don't trust what it does with information. The gate isn't "is it correct", it's "who saw this, why, and with whose permission." That's a governance and design problem, not a modeling one, and it's exactly the part teams skip because it doesn't produce an impressive benchmark.

## Consent and provenance are the product, not the paperwork

Real consent isn't a checkbox buried in an onboarding flow; it's a design commitment, the system is legible about what it collects, transparent about how it's used, and able to show where a given answer came from. I build AI in production with verification engineered in for exactly this reason: my systems ran **155 sessions with zero fabricated facts** by design, because in anything touching health, an untraceable answer is a liability whether or not it's correct.

> Health AI's bottleneck isn't accuracy. It's consent, privacy, and provenance, trust, by design.

## I've handled trust at scale with sensitive data

This is my lane. At SureCash we moved a government stipend to roughly **10 million people**, deeply sensitive financial data at national scale, where a single breach of trust would have collapsed adoption. You learn quickly that people don't hand over their money, or their health, to a system that feels opaque, no matter how clever it is. Trust is engineered up front or it's absent.

## The dual-market shape

In the US, the risk is *consent theater*, heavy formal frameworks (HIPAA and the rest) that produce compliance without actually earning trust. In Bangladesh, formal frameworks are thinner but trust is intensely relational, so a system that mishandles data loses adoption instantly and by word of mouth. Different failure modes, same rule: design for real consent and provenance, or the smartest health AI in the room never gets used.

## The short version

- Health AI stalls on consent and governance, not on accuracy, accuracy is necessary, not sufficient.
- Real consent is a design commitment: legible collection, transparent use, traceable answers.
- I engineer trust in: verification by design (0 fabricated), and sensitive data at scale (SureCash, ~10M).
- US risk is consent theater; BD risk is relational trust lost instantly, both demand trust by design.

**Would your users still use your AI if they fully understood what it does with their data, and if not, is that an accuracy problem or a consent one?**
