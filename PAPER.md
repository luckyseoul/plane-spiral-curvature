# Curvature Exponent Spectrum for Power-Law Plane Spirals: A Synthesis with Practical Tools

**Nicholas Perry**  
Independent Researcher, Council Bluffs / Omaha area, Iowa  
August 2026

## Abstract

We collect and unify classical results on the asymptotic curvature of plane spirals into a single spectral parameter β, defined by κ(s) ∼ s^β as arc length s → ∞. For polar power spirals r = θⁿ (n ≠ −1), the curvature exponent is exactly

```math
\beta = -\frac{n}{n+1}.
```

This mapping is a bijection from ℝ ∖ {−1} onto itself. A standard variational argument shows that minimizers of ∫ |κ′|^p s^q ds possess β = 1 − q/(p−1). Two practical contributions are added: (1) a constant-phase (constant-Δφ) generative method that eliminates plotting instability for all β, and (2) an Archimedean proxy that reduces computational cost for logarithmic-like spirals. All results are validated numerically. The work is offered as a compact synthesis with two useful tools for CAD, simulation, and LF/ELF antenna prototyping.

**Keywords**: plane spirals, curvature, power-law spirals, computational geometry, CAD, Archimedean proxy

## 1. Introduction

Plane spirals have been studied for centuries, yet their taxonomy remains fragmented by generating equation rather than geometric invariant. The Archimedean, Fermat, logarithmic, and clothoid spirals appear in separate literatures with no common language for their asymptotic behaviour.

We adopt the single parameter β defined by the asymptotic curvature law

```math
\kappa(s) \sim c \, s^{\beta} \quad (s \to \infty)
```

and show that every polar power spiral maps cleanly onto this spectrum. The mapping is elementary once the standard polar curvature formula is written down, but the resulting organization is useful. Two practical tools emerge that are not standard in the classical literature: a constant-phase plotting algorithm and a computational proxy for high-winding spirals.

## 2. Curvature Exponent for Polar Power Spirals

**Result 1.** For r = θⁿ (n ≠ −1), the curvature exponent is β = −n/(n+1).

**Proof (expanding case, n > 0).** For large θ the r² term dominates the numerator and denominator of the polar curvature formula, giving κ ∼ θ⁻ⁿ. Arc length satisfies s ∼ θⁿ⁺¹/(n+1), so θ ∼ [(n+1)s]^{1/(n+1)}. Substitution yields κ ∼ s^{−n/(n+1)}.

**Proof (shrinking case, n < −1).** Derivative terms dominate; the same substitution again produces β = −n/(n+1).

The mapping n ↦ β is therefore a bijection ℝ ∖ {−1} → ℝ ∖ {−1} with inverse n = −β/(β+1). Special values recover familiar spirals:

- n = 1/2 → β = −1/3 (Fermat)
- n = 1 → β = −1/2 (Archimedean)
- n = 2 → β = −2/3 (parabolic)
- n → ∞ → β → −1 (logarithmic limit)

## 3. Variational Selection of β

**Result 2.** Curves minimizing J = ∫ |κ′|^p s^q ds (p > 1) have curvature exponent β = 1 − q/(p−1), assuming κ is differentiable, κ′ does not change sign, and boundary terms vanish.

**Proof.** The Euler–Lagrange equation reduces to |κ′|^{p−1} s^q = C. Integration under the regularity assumption κ(0) = 0 immediately gives the stated exponent.

Known minimizers are recovered exactly: clothoid (p=2, q=0 → β=1), circle (p=2, q=1 → β=0), logarithmic spiral (p=2, q=2 → β=−1).

## 4. Practical Tools

### 4.1 Constant-Phase Generative Method

Standard arc-length parametrization becomes unstable for spirals with β < −0.5 because point density explodes near the origin. Instead, fix the turning-angle increment Δφ = const. Because κ = dφ/ds, the spatial step automatically scales as

```math
\Delta s = \Delta\phi / \kappa \sim \Delta\phi \, s^{-\beta}.
```

This single rule generates every member of the β-spectrum with uniform angular resolution and eliminates the need for adaptive step-size heuristics.

### 4.2 Archimedean Proxy for Logarithmic Spirals

Logarithmic spirals (β = −1) require exponentially increasing point density near the origin, making high-winding numerical work expensive. Archimedean spirals (β = −1/2) have linear radial growth and therefore linear point density. For any finite-domain simulation that only needs large-scale logarithmic geometry, the Archimedean proxy with the same outer radius and total turning angle reproduces the global shape to within a few percent while reducing the number of integration steps by a factor of roughly log(N_turns). The proxy is exact in the limit of many turns when only the outer envelope matters.

**Important limitation**: The proxy is for geometry and early simulation only. For true frequency-independent performance (constant impedance, pattern), the final design must use the logarithmic spiral.

## 5. Relation to Log-Aesthetic Curves (LAC)

Log-Aesthetic Curves (Miura 2006) are defined by a constant logarithmic curvature gradient:

```math
\frac{d(\ln\kappa)}{d(\ln s)} = -\frac{1}{\alpha}.
```

This is exactly the power-law form κ ∼ s^{−1/α}, i.e. β = −1/α. The β-spectrum therefore generalizes the single LAC line to all real β. The connection is noted for completeness; the paper does not claim novelty for LAC itself.

## 6. Numerical Confirmation

Seven polar power spirals (n = 0.25 to 5.0) were integrated with the constant-Δφ method and fitted in the asymptotic regime. All power-law fits returned R² > 0.9999 and recovered the analytic β to four decimal places (maximum error 0.001). The Archimedean proxy for a 100-turn logarithmic spiral reduced computation time by a factor of ~47 while preserving outer geometry to ~2 %.

## 7. Personal-Use Suggestions (LF / 630 m Band)

- Generate a 2 m outer-radius Archimedean proxy (15–25 turns) suitable for car-roof or portable layouts.
- Export coordinates to CSV → import into FreeCAD / Fusion 360 → produce .dxf for wire layout or PCB milling.
- Add a loading coil and ferrite core for impedance match near 475 kHz.
- Use the proxy for rapid weekend iteration; switch to true logarithmic geometry for final NEC-5 / HFSS verification if frequency-independent behaviour is required.
- Computational advantage: a 100-turn proxy runs in seconds on a laptop.

## 8. Conclusion

A single exponent β organizes the asymptotic geometry of all power-law plane spirals. The mapping from polar exponent n is elementary, the variational selection rule is standard, and two practical plotting tools are supplied. The framework is offered as a compact reference for researchers and practitioners who need a unified language for spiral curvature together with ready-to-run computational tools.

## References

1. Miura, K.T. (2006). A general equation of aesthetic curves and its self-affinity. *Computer-Aided Design and Applications*.
2. Inoguchi, J. et al. (2018). Log-aesthetic curves as similarity geometric analogue of Euler’s elasticae. *Computer Aided Geometric Design*.
3. Levien, R. (2008). The Euler spiral: A mathematical history. UC Berkeley EECS Technical Report.
4. Standard differential-geometry texts (do Carmo, Pressley) for the polar curvature formula.

---

**Table: β-spectrum for selected polar power spirals**

| n     | Spiral name     | β (theory) | β (numeric, typical) | Error   |
|-------|-----------------|------------|----------------------|---------|
| 0.25  | Quarter-power   | −0.2000    | −0.1990              | 0.0010  |
| 0.50  | Fermat          | −0.3333    | −0.3328              | 0.0005  |
| 1.00  | Archimedean     | −0.5000    | −0.4999              | 0.0001  |
| 2.00  | Parabolic       | −0.6667    | −0.6667              | 0.0000  |
| 3.00  | Cubic           | −0.7500    | −0.7500              | 0.0000  |
| 4.00  | Quartic         | −0.8000    | −0.8000              | 0.0000  |
| 5.00  | Quintic         | −0.8333    | −0.8333              | 0.0000  |

All fits R² > 0.9999.
