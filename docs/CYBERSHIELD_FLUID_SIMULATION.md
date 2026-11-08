# CyberShield AI — GPU Fluid Simulation Engine
**Specification**: Real-time 2D Navier-Stokes Fluid Solver for Cursor Interaction  
**Resolution**: 256×256 Simulation Grid | 512×512 Density Grid  
**Coupling**: Bidirectional momentum transfer to 3D GPU particles

---

## 1. Navier-Stokes Pipeline Overview

The fluid simulation solves the incompressible Navier-Stokes equations on a discrete 2D grid:
$$\frac{\partial \vec{u}}{\partial t} + (\vec{u} \cdot \nabla)\vec{u} = -\frac{1}{\rho}\nabla p + \nu \nabla^2 \vec{u} + \vec{f}$$
$$\nabla \cdot \vec{u} = 0$$

```
   [Cursor / Touch Movement]
              │
              ▼
    1. Advection Pass (MacCormack / BFECC / Semi-Lagrangian)
              │
              ▼
    2. Force Splatting (Gaussian Impulse from Pointer Velocity)
              │
              ▼
    3. Vorticity Confinement (Curl = 30.0)
              │
              ▼
    4. Divergence Calculation (2-point central difference)
              │
              ▼
    5. Jacobi Pressure Solver (5 iterations, Dissipation = 0.95)
              │
              ▼
    6. Gradient Subtraction (Projection step: Divergence-free field)
              │
              ▼
   [Fluid Velocity Texture] ────► [Sampled by 3D Particle Simulation]
```

---

## 2. Parameter Tuning Matrix

| Parameter | Value | Functional Role |
| :--- | :--- | :--- |
| **Sim Resolution** | $256 \times 256$ | Velocity solver grid dimensions |
| **Density Resolution** | $512 \times 512$ | Visual dye/disturbance grid dimensions |
| **Velocity Dissipation** | `0.98` | Natural decay of kinetic energy per frame |
| **Density Dissipation** | `0.97` | Dissipation rate of visible fluid wakes |
| **Pressure Dissipation** | `0.95` | Damping of acoustic pressure waves |
| **Pressure Iterations** | `5` | Jacobi solver passes for incompressibility |
| **Curl Confinement** | `30.0` | Boosts fine-scale rotational micro-vortices |
| **Time Step ($\Delta t$)** | `1/60` | Fixed simulation integration increment |

---

## 3. Pointer Interaction & Splatting

When the user moves the mouse or drags across a touchscreen:
1. Calculates normalized pointer delta: $\Delta \vec{x} = (\vec{x}_t - \vec{x}_{t-1})$.
2. Projects pointer coordinates to UV space: $(u, v) \in [0, 1]^2$.
3. Evaluates Gaussian impulse:
   $$\vec{u}_{\text{splat}} = \Delta \vec{x} \cdot S_{\text{force}} \cdot \exp\left(-\frac{\|\vec{x} - \vec{x}_{\text{pointer}}\|^2}{2 \sigma^2}\right)$$
4. Splats both velocity vectors and lavender/white density into the active fluid grid.
5. In the particle simulation pass, particles sample this velocity texture at their projected screen coordinates, creating realistic swirls that dissipate and restore in ~1.5 seconds.
