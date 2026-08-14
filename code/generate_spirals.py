#!/usr/bin/env python3
"""
Plane Spiral Curvature Tools
============================
Constant-Δφ generator, Archimedean proxy, curvature computation,
and β fitting for power-law plane spirals.

Author: Nicholas Perry
Repo: https://github.com/luckyseoul/plane-spiral-curvature
"""

import numpy as np
from scipy.integrate import cumulative_trapezoid

def archimedean_proxy_spiral(R_outer=2.0, Theta_total=40*np.pi, n_points=5000):
    """
    Archimedean proxy (β = −0.5) with constant-Δφ parametrization.
    Matches outer radius and total turning angle of a logarithmic spiral
    while using linear radial growth (much cheaper numerically).
    """
    phi = np.linspace(0.0, Theta_total, n_points)
    r = (R_outer / Theta_total) * phi          # linear radial growth
    x = r * np.cos(phi)
    y = r * np.sin(phi)

    # Arc-length
    ds = np.sqrt(np.diff(x)**2 + np.diff(y)**2)
    s = np.concatenate(([0.0], cumulative_trapezoid(ds, phi[:-1])))
    return x, y, s, r, phi


def logarithmic_spiral(R_outer=2.0, R_inner=0.05, Theta_total=40*np.pi, n_points=20000):
    """True logarithmic spiral (β → −1) for comparison."""
    phi = np.linspace(0.0, Theta_total, n_points)
    # r = a * exp(b * phi) so that r(0)=R_inner, r(Theta)=R_outer
    b = np.log(R_outer / R_inner) / Theta_total
    a = R_inner
    r = a * np.exp(b * phi)
    x = r * np.cos(phi)
    y = r * np.sin(phi)
    ds = np.sqrt(np.diff(x)**2 + np.diff(y)**2)
    s = np.concatenate(([0.0], cumulative_trapezoid(ds, phi[:-1])))
    return x, y, s, r, phi


def compute_curvature(x, y, s):
    """Return κ(s) for any parametric plane curve."""
    # Avoid division by zero at s=0
    s_safe = np.maximum(s, 1e-12)
    dx = np.gradient(x, s_safe)
    dy = np.gradient(y, s_safe)
    d2x = np.gradient(dx, s_safe)
    d2y = np.gradient(dy, s_safe)
    speed2 = dx**2 + dy**2
    kappa = np.abs(dx * d2y - dy * d2x) / (speed2 ** 1.5 + 1e-30)
    return kappa


def fit_beta(s, kappa, tail_fraction=0.3):
    """
    Fit κ ~ s^β on the outer tail of the spiral.
    Returns (beta, intercept).
    """
    n = len(s)
    start = int((1.0 - tail_fraction) * n)
    s_tail = s[start:]
    k_tail = kappa[start:]

    valid = (s_tail > 0) & (k_tail > 0) & np.isfinite(s_tail) & np.isfinite(k_tail)
    log_s = np.log10(s_tail[valid])
    log_k = np.log10(k_tail[valid])

    if len(log_s) < 10:
        return np.nan, np.nan

    beta, intercept = np.polyfit(log_s, log_k, 1)
    return beta, intercept


def constant_delta_phi_spiral(beta, R_outer=2.0, Theta_total=20*np.pi, n_points=4000):
    """
    Generic constant-Δφ generator for any β.
    Uses the asymptotic relation κ ∼ s^β to adapt step size.
    (Simple demonstration version; refine for production work.)
    """
    # Approximate construction via polar angle
    phi = np.linspace(0.0, Theta_total, n_points)
    # Rough radial mapping consistent with β = -n/(n+1)
    # n = -β/(β+1)
    if abs(beta + 1) < 1e-9:
        n = 1e6   # near-logarithmic
    else:
        n = -beta / (beta + 1.0)
    r = R_outer * (phi / Theta_total)**max(n, 0.1)
    x = r * np.cos(phi)
    y = r * np.sin(phi)
    ds = np.sqrt(np.diff(x)**2 + np.diff(y)**2)
    s = np.concatenate(([0.0], cumulative_trapezoid(ds, phi[:-1])))
    return x, y, s, r, phi


if __name__ == "__main__":
    import matplotlib.pyplot as plt

    print("Generating Archimedean proxy (β = −0.5) ...")
    x_a, y_a, s_a, r_a, phi_a = archimedean_proxy_spiral(
        R_outer=2.0, Theta_total=40*np.pi, n_points=5000
    )
    kappa_a = compute_curvature(x_a, y_a, s_a)
    beta_a, _ = fit_beta(s_a, kappa_a)
    print(f"  Fitted β (proxy): {beta_a:.4f}  (expected ≈ −0.50)")

    print("Generating true logarithmic spiral for comparison ...")
    x_l, y_l, s_l, r_l, phi_l = logarithmic_spiral(
        R_outer=2.0, R_inner=0.05, Theta_total=40*np.pi, n_points=20000
    )
    kappa_l = compute_curvature(x_l, y_l, s_l)
    beta_l, _ = fit_beta(s_l, kappa_l)
    print(f"  Fitted β (log):   {beta_l:.4f}  (expected ≈ −1.00)")

    # Simple gallery plot
    fig, axes = plt.subplots(1, 2, figsize=(12, 5))
    axes[0].plot(x_a, y_a, lw=0.8)
    axes[0].set_title("Archimedean Proxy (β ≈ −0.5)")
    axes[0].set_aspect("equal")
    axes[0].grid(True, alpha=0.3)

    axes[1].plot(x_l, y_l, lw=0.6)
    axes[1].set_title("True Logarithmic (β ≈ −1)")
    axes[1].set_aspect("equal")
    axes[1].grid(True, alpha=0.3)

    plt.tight_layout()
    plt.savefig("spiral_comparison.png", dpi=150)
    print("Saved spiral_comparison.png")

    # Log-log curvature plot (outer tail)
    fig2, ax = plt.subplots(figsize=(7, 5))
    mask = s_a > 0.2
    ax.loglog(s_a[mask], kappa_a[mask], label="Archimedean proxy")
    mask_l = s_l > 0.2
    ax.loglog(s_l[mask_l], kappa_l[mask_l], label="Logarithmic", alpha=0.7)
    ax.set_xlabel("arc length s")
    ax.set_ylabel("curvature κ")
    ax.set_title("Log-log κ(s) — asymptotic slope = β")
    ax.legend()
    ax.grid(True, which="both", alpha=0.3)
    plt.tight_layout()
    plt.savefig("kappa_loglog.png", dpi=150)
    print("Saved kappa_loglog.png")

    print("Done. Open the PNGs or re-run with your own parameters.")
