# CyberShield AI — GPU Particle Fluid Experience Setup
**Environment**: Windows 11, Node.js 18+, Python 3.13, Vite 5, React 18, Three.js  
**Target Path**: `D:\My Created Projects\Merge 2 and 4`

---

## 1. Quick Start & Execution

### 1.1 Run Full Platform (FastAPI Backend + Built Experience)
```powershell
cd "D:\My Created Projects\Merge 2 and 4"
.\run-server.ps1
```
Open **[http://127.0.0.1:8000/](http://127.0.0.1:8000/)** in Chrome or Edge.

### 1.2 Run Frontend in Vite Dev Server
```powershell
cd "D:\My Created Projects\Merge 2 and 4\frontend"
npm run dev
```
Open **[http://localhost:5173/](http://localhost:5173/)**.

---

## 2. Interactive Navigation Guide

- **Canvas Interaction**:
  - Drag mouse or swipe across screen to create dynamic fluid wakes.
  - Hovering or clicking capability cards triggers localized fluid impulses.
  - Camera subtly gazes toward cursor coordinates.
- **Top Brand**:
  - Clicking the top-left logo or brand title provides quick access to the platform overview (`/dashboard`).
- **Capability Cards (Left)**:
  - `Signal / Message`: Launches Member 2 AI Scam Analyzer (`/message-analyzer`).
  - `Surface / URL`: Launches URL & Domain Scanner (`/scanner`).
  - `Evidence / Report`: Opens Forensic Threat Registry (`/history`).
  - `Trust / Ledger`: Opens Blockchain Verification (`/history`).
- **Category Filter Chips**:
  - Click `All`, `Messages`, `URLs`, `Domains`, `AI`, `Evidence`, `Reports`, `Blockchain`, etc., to instantly filter capabilities.
- **Sound Toggle (Top-Right)**:
  - Procedural Web Audio drone; starts muted by default. Click `SOUND: OFF` to activate synthesized sub-drone.

---

## 3. GPU Performance Profiles

- **Desktop (High Profile)**:
  - 262,144 particles ($512 \times 512$ GPGPU texture).
  - $256 \times 256$ Navier-Stokes fluid velocity solver, 5 Jacobi pressure iterations.
- **Mobile (Adaptive Profile)**:
  - 16,384 particles ($128 \times 128$ texture).
  - $128 \times 128$ fluid solver, touch event interaction.
- **Low/Non-WebGL Fallback**:
  - Automatically mounts `ExperienceFallback.tsx` (2D Canvas particle vortex) if float textures or WebGL extensions are unsupported.
