# CyberShield AI — GPU Particle Engine Architecture
**Specification**: Ping-Pong GPGPU Particle Simulation & Sculpted Geometry  
**Target Particle Counts**: Desktop 262,144 (512×512) | Mobile 16,384 (128×128)  
**Palette**: Pure White, Muted Slate, Sparse Lavender (`#AA88FF`)

---

## 1. Geometric Shape Formulation: The Digital Shield Vortex

Rather than a random amorphous cloud, the particles are anchored to an **original 3D parametric Digital Shield Vortex**:

```
                       . . . - - - . . .
                   . '                   ' .
                .                             .
              /        /\             /\        \
             |        /  \   CORE    /  \        |
            |        /    \ (VOID)  /    \        |
            |        \     \       /     /        |
             |        \     \     /     /        |
              \        \     \   /     /        /
                .       \     \ /     /       .
                   ' .   \     v     /   . '
                       ' - - - - - - '
```

### Parametric Equations
For coordinates $(u, v) \in [0, 2\pi) \times [-\pi, \pi]$:
$$x(u, v) = \left(R_0 + r \cos v \cdot (1 - 0.15 \cos^2 u)\right) \cdot \sin u + \text{offset}_X$$
$$y(u, v) = \left(H_0 \cos u - 0.25 |x|\right) + r \sin v$$
$$z(u, v) = D_0 \cdot \sin(2u) + \tau \cdot \cos v$$

Where:
- $R_0 = 2.4$: Shield base radius.
- $H_0 = 3.2$: Vertical shield elongation.
- $D_0 = 0.85$: Spatial curvature and depth.
- $\tau = 0.45$: Subtle Möbius twist along the outer perimeter.
- $\text{offset}_X = +1.4$: Offsets the sculpture to the right of screen center, allowing optimal negative space for UI cards and text.

---

## 2. GPGPU Ping-Pong FBO Architecture

The simulation runs entirely on the GPU using double-buffered floating-point render targets (`WebGLRenderTarget` with `FloatType` or `HalfFloatType`):

```
       ┌────────────────┐                  ┌────────────────┐
       │ Pos Target A   │ ── Read Pass ──► │ Simulation     │
       └────────────────┘                  │ Shader (Quad)  │
               ▲                           └───────┬────────┘
               │                                   │ Write
               └─────────── Ping-Pong ─────────────▼
                                           ┌────────────────┐
                                           │ Pos Target B   │
                                           └────────────────┘
```

### Simulation Passes (Fragment Shader)
1. **Current State**: Samples previous position $P$ and velocity $V$.
2. **Anchor Spring Force**:
   $$\vec{F}_{\text{spring}} = -k_{\text{spring}} \cdot (P - P_{\text{anchor}})$$
3. **Curl Noise Vector Field**:
   Evaluates 3D Simplex Curl Noise $\nabla \times \vec{\psi}(P \cdot s)$ to introduce organic micro-turbulence.
4. **Fluid Force Coupling**:
   Projects 3D particle coordinates to screen space $(u_s, v_s)$ and samples the 2D fluid velocity field $\vec{V}_{\text{fluid}}$.
   $$\vec{F}_{\text{fluid}} = \beta \cdot \vec{V}_{\text{fluid}}(u_s, v_s)$$
5. **Damping & Integration**:
   $$V_{t+\Delta t} = V_t \cdot \gamma_{\text{damping}} + (\vec{F}_{\text{spring}} + \vec{F}_{\text{curl}} + \vec{F}_{\text{fluid}}) \cdot \Delta t$$
   $$P_{t+\Delta t} = P_t + V_{t+\Delta t} \cdot \Delta t$$

---

## 3. Particle Shading & Optical Pipeline

- **Point Sizing**:
  Perspective-correct point scaling:
  $$\text{size} = \text{baseSize} \cdot \left(\frac{280.0}{-z_{\text{view}}}\right) \cdot \text{scaleFactor}$$
- **Spherical Shading**:
  Points are rendered with circular alpha cutouts ($r = \|uv - 0.5\| \le 0.5$) and pseudo-matcap spherical normals:
  $$\vec{N} = (2 \cdot uv_x - 1, -(2 \cdot uv_y - 1), \sqrt{1 - 4 r^2})$$
- **Color Distribution**:
  - $80\%$ Soft White (`#F0F0F5`)
  - $12\%$ Slate Muted Grey (`#8A8A9E`)
  - $8\%$ Lavender Threat Accents (`#AA88FF`)
- **Blending**: `THREE.AdditiveBlending` for luminous depth.
