# Product

<!-- impeccable:product-schema 1 -->

## Platform

web

## Users

Everyone who lands on github.com/R204570, weighted equally (confirmed):

- **Hiring managers and recruiters** for AI Engineering, Agentic AI and Data Science roles. They skim for under a minute and decide whether to open the résumé.
- **Open-source developers** who might star, use or contribute to DocsForge.
- **Freelance clients** who want an idea built and deployed: agents, computer-vision models, Django/FastAPI backends.
- **Peers** browsing from a pinned repo, a PR or a follower list.

## Product Purpose

The GitHub profile README for Raj Patel (handle `R204570`). It replaces a version that failed because it stacked seven medical-imaging gimmicks and buried who Raj is and what they have shipped (confirmed). Success: within the first screen a visitor knows who Raj is, what they build, has seen proof that it ships, and has an obvious next step (résumé, email, DocsForge, live demos).

## Positioning

Raj builds the model *and* the deployed software around it: agentic systems (DocsForge, an MCP server in production), medical imaging (NeuroAssist), industrial computer vision (PCB defect detection, Intel programme), and full-stack apps people log into (Hospital Management System, 100★). "Idea → deployed" is the claim; live links are the proof.

## Operating Context

- Rendered by GitHub inside the profile page's main column: about 830px wide on desktop, about 360px on phones. GitHub's own sidebar already shows avatar, name, bio, location and links; pinned repos and the contribution calendar render below the README.
- GitHub sanitises README HTML: no CSS, no JS, no iframes. Custom visuals must be images (SVG via `<img>`/`<picture>`). SVG animation and data-URI fonts work; links inside an SVG do not. `<picture>` with `prefers-color-scheme` follows the viewer's GitHub theme (light and dark both matter).
- A GitHub Action (`.github/workflows/activity.yml`, `GITHUB_TOKEN`, `contents: write`) redraws the live panels (the hero's 26-week strip and the activity panel) from the contribution calendar twice a day.

## Capabilities and Constraints

- Keep (confirmed): a live, self-updating activity graph driven by a GitHub Action, redesigned; the hidden-flag easter egg for security people.
- Drop (confirmed): the medical / MRI / radiology framing everywhere. Start the visual world from scratch.
- Every visual must stay legible at phone width and in both GitHub themes.

## Brand Commitments

- Name: Raj Patel. Handle: R204570. Based in Ahmedabad, Gujarat, India.
- Voice: first person, plain, specific; numbers over adjectives.
- Register (confirmed 2026-10-21): "visually appealing as well as great" and "somewhat formal". Two themed worlds were rejected in a row (stacked medical imaging; a demoscene cracktro screen); playful costume reads as unprofessional here.
- Links: portfolio https://portfolio-raj-25.netlify.app/ · LinkedIn https://www.linkedin.com/in/raj-patel5 · Kaggle https://www.kaggle.com/raj072004 · Medium https://medium.com/@rajpatel9408019 · Résumé https://portfolio-raj-25.netlify.app/Raj-Patel-Resume.pdf · rajpatel9408019@gmail.com

## Evidence on Hand

Verified from the repositories on 2026-10-21:

- **DocsForge** (github.com/R204570/DocsForge, docsforge.vercel.app): open-source MCP server; name a library and it finds, verifies and harvests the official, version-specific docs for Claude Code, Cursor, Codex and other MCP clients. Held-out test: 91% of never-seen names resolved to their official docs on first pass (round 3, 56 names). `pipx install docsforge`. Actively seeking contributors.
- **NeuroAssist** (github.com/R204570/BrainTumor): Flask clinical decision-support prototype; MRI (NIfTI/DICOM) → 3D Attention U-Net segmentation on BraTS 2020 → tumour volumes and lobe involvement → RAG-grounded LLM report. Built under Microsoft Elevate × GTU; Raj's own previous README tagged it `capstone`.
- **PCB Defect Detection** (github.com/R204570/PCB_DEFECT_DETECTION, pcb-anomaly-detection.streamlit.app): YOLOv8, mAP@0.5 > 85% per its README, webcam and batch modes. Intel AI for Manufacturing.
- **Hospital Management System** (github.com/R204570/hospital-management-system, live on Render): Django, role-based access, appointments, billing, pharmacy, PDF reports. 100 stars, 4 forks: the most-starred repo.
- **SAC AI Search** (repo description: GST SAC code database with AI search from a plain description), **Reconciliation** (atomic compute-then-commit wallet reconciliation, Flask + MS SQL), **ExpenseFlow** (live on Vercel; previous README: AI extraction from receipt to saved expense), **Cafe-POS** (Django + DRF, 5★), **GearGuard** (repo description: maintenance and equipment management platform, Django 5.2 + PostgreSQL), Kaggle **BraTS2020 MGMT** preprocessed dataset.
- Card and row details verified from the repositories' READMEs and descriptions on 2026-10-21:
  DocsForge's chat panel is a FastAPI extra and it can store harvests in Postgres (`[web]`, `[postgres]` extras);
  NeuroAssist stores imaging results in PostgreSQL; PCB Defect Detection runs PyTorch, processes single or batch
  images, charts defect distributions and exports annotated images as a ZIP; Reconciliation has a Flask dashboard,
  CLI and batch runner on MS SQL Server; SAC AI Search is Python and open source; ExpenseFlow is JavaScript on
  Vercel; Cafe-POS is Django + Django REST Framework + PostgreSQL; GearGuard is a full-featured Django 5.2 +
  PostgreSQL web platform; the BraTS2020 MGMT work used a 3D ResNet (Raj's previous README).
- Credentials: Intel® AI for Manufacturing (2025, first batch, 16 weeks, demoed to GTU's Vice Chancellor and Intel leadership); Microsoft Elevate × GTU (2026); B.E. Information Technology + Data Science honours, GTU (2026); CPTE certified.
- Skills as Raj listed them in the previous README: agentic AI, RAG, tool use, MCP servers, Claude Code; FastAPI, Django, Flask, Postgres + pgvector, Redis; PyTorch, TensorFlow, YOLOv8, OpenCV, 3D U-Net; LLMs/SLMs, NLP, Hugging Face, pandas, NumPy, scikit-learn; Streamlit, Node.js, GCP, Render, Vercel, Netlify; CPTE, STRIDE threat models, OWASP LLM Top 10, DPDP.
- Not verified, do not use: Dice scores for NeuroAssist; mAP ≈ 0.90 for PCB.

## Product Principles

1. Sell in one screen: who, what, proof, next step.
2. Proof beats adjectives: shipped links, real numbers, stars.
3. One idea, executed once. No stacked metaphors.
4. Legible everywhere: phone width, light and dark.
5. Personality lives in details (the live graph, the hidden flag), never in the way of the pitch.
