# CyberShield AI — 3D Cinematic Experience Implementation Plan
**Document Version**: 1.0.0  
**Target Environment**: Windows 11, React 18, Vite 5, TailwindCSS 3.4, Three.js, Web Audio API, FastAPI Master Backend

---

## 1. Architectural Architecture & Philosophy

The objective is to elevate CyberShield AI from a functional cybersecurity dashboard into an **awe-inspiring, cinematic interactive 3D universe** inspired by the aesthetics of [ysuriadesign.co](https://ysuriadesign.co/).

### 1.1 Coexistence with Operational Application
The cinematic landing experience will live at route `/`, presenting the story of CyberShield AI across 6 chapters with deep links into operational tools:
- `Chapter 01 (The Signal)` $\rightarrow$ Links to `/message-analyzer`
- `Chapter 02 (The Attack Surface)` $\rightarrow$ Links to `/scanner`
- `Chapter 03 (Intelligence in Motion)` $\rightarrow$ Links to `/message-analyzer` (AI Failover inspection)
- `Chapter 04 (The Evidence)` $\rightarrow$ Links to `/history` (Forensic Investigation Registry)
- `Chapter 05 (Verifiable Trust)` $\rightarrow$ Links to `/history` & `/report/:id` (Blockchain verification)
- `Chapter 06 (What's Next)` $\rightarrow$ Links to `/dashboard` (Full operational platform)

Existing operational routes (`/dashboard`, `/scanner`, `/message-analyzer`, `/history`, `/report/:id`, `/settings`) remain completely intact and functional, communicating with the master FastAPI backend and Member 2 AI microservice.

---

## 2. Component Hierarchy

```
frontend/src/
│
├── components/
│   ├── 3d/
│   │   ├── ThreeHeroCanvas.tsx         # WebGL canvas wrapper with resize/context listeners
│   │   ├── CyberShieldScene.ts         # Three.js scene graph, lights, shield, lasers, particles
│   │   ├── CameraChoreographer.ts     # Chapter-based camera positions, lookAt lerping, FOV
│   │   └── WebGLFallback.tsx          # High-fidelity 2D canvas/CSS particle fallback for low-end
│   │
│   ├── audio/
│   │   ├── CyberShieldAudio.ts        # Procedural Web Audio API sound synthesizer
│   │   └── AudioGateModal.tsx         # "Enter with Sound" vs "Enter Muted" intro modal
│   │
│   ├── hud/
│   │   ├── CinematicHUD.tsx           # Overlay container (Top bar, rail, bottom info, CTA)
│   │   ├── ChapterRail.tsx            # Right-side vertical chapter navigator (01..06)
│   │   ├── ChapterIndexModal.tsx      # Fullscreen chapter index drawer
│   │   ├── CustomCursor.tsx           # Trailing dot + ring custom mouse cursor
│   │   └── ScrollCue.tsx              # Bottom animated scroll indicator
│   │
│   ├── Navbar.tsx                     # Top navigation with toggle between "3D World" and "Platform"
│   ├── RiskBadge.tsx
│   ├── ScoreGauge.tsx
│   └── VerificationCard.tsx
│
├── pages/
│   ├── CinematicExperience.tsx        # Master 6-chapter scroll controller & HUD orchestrator
│   ├── Dashboard.tsx                  # Operational Triage Overview
│   ├── Scanner.tsx                    # URL & Domain Threat Scanner
│   ├── MessageAnalyzer.tsx            # Member 2 Scam Analysis Engine
│   ├── History.tsx                    # Relational Investigation Registry
│   ├── ReportDetail.tsx               # Cryptographic Report & Blockchain Status
│   └── Settings.tsx                   # System Diagnostics & Provider Health
│
└── App.tsx                            # React Router with seamless navigation
```

---

## 3. The Six Chapters: Narrative & Visual Choreography

| Chapter | Title & Kicker | Visual 3D Composition | Camera Behavior | Primary Action / CTA |
| :--- | :--- | :--- | :--- | :--- |
| **00** | **CyberShield Core**<br>`Intelligence Before Impact` | Central floating crystalline shield, 8 orbiting dark polyhedrons, dual crimson laser axes intersecting at core, gentle stardust. | Orbiting macro view (`z: 14, y: 1.5, x: 0`), subtle mouse parallax. | `Scroll to Explore ↓` |
| **01** | **The Signal**<br>`Every signal has a story` | Suspicious message fragments float into the field; crimson laser pulses scan text snippets and telemetry tokens. | Dolly forward towards upper left (`z: 9, y: 1.0, x: -2.5`), focusing on fragmented signal nodes. | `Analyse a Message ↗`<br>(`/message-analyzer`) |
| **02** | **The Attack Surface**<br>`Every link leads somewhere` | Complex URL paths, DNS nodes, and TLS reputation lines materialize in 3D around a compromised node. | Wide sweeping diagonal tilt (`z: 11, y: 3.5, x: 3.2`), revealing attack surface topography. | `Investigate a URL ↗`<br>(`/scanner`) |
| **03** | **Intelligence in Motion**<br>`Understand what hides in the message` | Tri-tier neural failover paths glow: Groq $\rightarrow$ Gemini $\rightarrow$ OpenAI $\rightarrow$ Heuristics. Processing waves illuminate the core. | Close-up internal penetration into the shield's neural chamber (`z: 6, y: 0.2, x: 0`). | `Explore AI Engine ↗`<br>(`/message-analyzer`) |
| **04** | **The Evidence**<br>`Suspicion becomes structured intelligence` | Dispersed threat indicators (+91 phone, spoofed domain, phishing URL, urgency quote) align into a structured 3D forensic block. | Low-angle elevation view (`z: 8, y: -2.0, x: 1.8`), looking up as evidence crystallizes. | `View Threat Reports ↗`<br>(`/history`) |
| **05** | **Verifiable Trust**<br>`Evidence should leave a verifiable trace` | Laser lighting shifts from crimson threat red to cryptographic teal/emerald (`#00f5a0`). Hex hashes and blockchain blocks link in space. | Lateral tracking shot alongside the cryptographic ledger chain (`z: 7, y: 0.8, x: -3.0`). | `Explore Verification ↗`<br>(`/history`) |
| **06** | **What's Next**<br>`Make your next decision with confidence` | All systems converge: Shield core expands with protective aura, laser arrays project outward, full cyber defense matrix active. | Epic pullback to wide cinematic frame (`z: 16, y: 2.0, x: 0`), revealing complete defense umbrella. | `Launch Platform ↗`<br>(`/dashboard`) |

---

## 4. Procedural Audio Synthesizer Design

Following the reference site's zero-dependency Web Audio API model:
1. **Atmospheric Sub-Drone**:
   - `OscillatorNode` (Sine @ 55Hz) + `OscillatorNode` (Triangle @ 110Hz).
   - `BiquadFilterNode` (Lowpass, 24dB roll-off, base cutoff 160Hz).
   - Frequency modulation connected to scroll velocity (cutoff increases to 450Hz during fast scroll, creating a dynamic whoosh effect).
2. **Cyber Spatial Scan Pulse**:
   - Short decaying envelope (attack: 5ms, release: 250ms) on sine wave @ 880Hz through a resonant bandpass filter, triggered on chapter transitions.
3. **User Controls & Accessibility**:
   - Audio strictly OFF by default.
   - Opening modal choices: `Enter with sound` (unlocks AudioContext) vs `Enter muted`.
   - Top-right sound toggle button with animated 3-bar equalizer waveform.
   - Page visibility detection: Automatically suspends audio when tab is hidden, resumes when visible.

---

## 5. Scroll & Interaction Mechanics

- **Virtual Scroll Container**:
  - The scroll track spans 600vh (`6 * 100vh`), with each chapter occupying 100vh of normalized scroll domain.
  - Current chapter calculation: `chapterIndex = Math.min(5, Math.floor(scrollProgress * 6))`.
  - Camera position, lookAt target, laser beam intensity, and particle velocities are smoothly interpolated using exponential damping (`lerp` with factor `0.05 - 0.08`).
- **Direct Navigation**:
  - Clicking any item on the right-side rail (`01` through `06`) or top counter smoothly scrolls the window to the target chapter position without requiring linear manual scrolling.
- **Mouse Parallax**:
  - Normalized mouse coordinates `(x, y) ∈ [-1, 1]` apply a subtle rotational tilt to the 3D scene (`±0.15 radians`) for visceral tactile depth.
- **Custom Cursor**:
  - Dual-layer: Fixed center dot (`.c-dot`) + spring-smoothed trailing ring (`.c-ring`). Expands when hovering clickable links/buttons.

---

## 6. Performance & Fallback Strategy

1. **Geometry Optimization**:
   - Procedural polyhedrons with low polygon counts (< 800 vertices each).
   - Particle cloud implemented using a single `THREE.Points` object with typed arrays (`Float32Array`).
2. **GPU Throttling Defense**:
   - `renderer.setPixelRatio(Math.min(window.devicePixelRatio, 2))`.
   - `powerPreference: "high-performance"`.
3. **Graceful Fallback**:
   - Detect WebGL support via `canvas.getContext('webgl2') || canvas.getContext('webgl')`.
   - If WebGL is unavailable or fails, automatically mount `WebGLFallback.tsx`, rendering an animated HTML5 2D canvas cyber particle matrix with CSS3D lighting, maintaining full visual continuity and zero errors.
4. **Accessibility (`prefers-reduced-motion`)**:
   - Media query detection disables rapid camera translation and limits motion to gentle ambient breathing.

---

## 7. Execution Timeline

1. Install Three.js & types (`three`, `@types/three`) using user cache directory.
2. Build 3D engine: `CyberShieldScene.ts`, `CameraChoreographer.ts`, `ThreeHeroCanvas.tsx`.
3. Build procedural audio synthesizer: `CyberShieldAudio.ts`, `AudioGateModal.tsx`.
4. Build HUD & Navigation: `CinematicHUD.tsx`, `ChapterRail.tsx`, `CustomCursor.tsx`, `ChapterIndexModal.tsx`.
5. Build main controller page: `CinematicExperience.tsx` and integrate into `App.tsx` and `Navbar.tsx`.
6. Verify production build (`npm run build`).
7. Run complete automated integration tests (`tests/test_cybershield.py`, `tests/test_member4_comprehensive.py`).
8. Compile `docs/CYBERSHIELD_3D_FINAL_REPORT.md`.
