#!/usr/bin/env python3
"""
Renders a publication-quality, color-blind accessible (Okabe-Ito compliant)
diagram of the 4-layer PANOPTES reference architecture.
Saves to figures/fig_panoptes_architecture.png (300 DPI).
"""

import os
import matplotlib.pyplot as plt
import matplotlib.patches as patches

def draw_diagram():
    fig, ax = plt.subplots(figsize=(14.2, 9.8), dpi=300)
    ax.set_xlim(-8.6, 8.6)
    ax.set_ylim(-1.45, 7.15)
    ax.axis('off')

    # Okabe-Ito & WCAG AA Accessible Palette:
    # Layer 1 (Blue):       Fill #EBF3FB, Border #0072B2
    # Layer 2 (Teal/Green): Fill #E6F5F0, Border #009E73
    # Layer 3 (Purple):     Fill #F5EDF6, Border #882255
    # Layer 4 (Orange):     Fill #FDF3E7, Border #D55E00
    # Containers (Neutral): Fill #FAFAFA, Border #B0B0B0, Dashed

    layer_container_style = dict(boxstyle="round,pad=0.35", fc="#FAFAFA", ec="#A0AEC0", lw=1.2, ls="--")
    sut_style = dict(boxstyle="round,pad=0.3", fc="#EBF3FB", ec="#0072B2", lw=1.3)
    probe_style = dict(boxstyle="round,pad=0.3", fc="#E1EEF9", ec="#0072B2", lw=1.3)
    store_tempo_style = dict(boxstyle="round,pad=0.3", fc="#E1EEF9", ec="#0072B2", lw=1.3)
    store_prom_style = dict(boxstyle="round,pad=0.3", fc="#E6F5F0", ec="#009E73", lw=1.3)
    store_loki_style = dict(boxstyle="round,pad=0.3", fc="#FEF3C7", ec="#D97706", lw=1.3)
    correl_algo1_style = dict(boxstyle="round,pad=0.3", fc="#F5EDF6", ec="#882255", lw=1.3)
    correl_algo2_style = dict(boxstyle="round,pad=0.3", fc="#F5EDF6", ec="#882255", lw=1.3)
    act_style = dict(boxstyle="round,pad=0.3", fc="#FDF3E7", ec="#D55E00", lw=1.3)

    # =========================================================================
    # LAYER 1: INGESTION & PROBING
    # =========================================================================
    rect1 = patches.FancyBboxPatch((-5.8, 4.3), 12.8, 2.5, **layer_container_style)
    ax.add_patch(rect1)
    
    # Left Badge
    ax.text(-7.2, 5.55, "Layer 1\nTelemetry\nIngestion &\nProbing", 
            ha='center', va='center', fontsize=9, fontweight='bold', color='#004C7A',
            bbox=dict(boxstyle="round,pad=0.5", fc="#EBF3FB", ec="#0072B2", lw=1.6))
    
    # SUT Row
    ax.text(-3.8, 6.2, "frontend / cart\n(HTTP/gRPC Gateway & State)", ha='center', va='center', fontsize=8, fontweight='bold', color="#111827", bbox=sut_style)
    ax.text(0.6, 6.2, "shipping / checkout\n(Synchronous RPC Workloads)", ha='center', va='center', fontsize=8, fontweight='bold', color="#111827", bbox=sut_style)
    ax.text(5.0, 6.2, "payment / currency\n(Kafka Async & Background)", ha='center', va='center', fontsize=8, fontweight='bold', color="#111827", bbox=sut_style)

    # Probes Row (Modality-specific cues)
    ax.text(-3.8, 4.9, "OTel SDK & Auto-Instr.\n[Modality: Distributed Traces]\nW3C TraceContext Propagation", ha='center', va='center', fontsize=7.5, color="#111827", bbox=probe_style)
    ax.text(0.6, 4.9, "eBPF & cgroup v2 Scrapers\n[Modality: Socket & CPU Metrics]\ntcp_v4_connect | Throttling", ha='center', va='center', fontsize=7.5, color="#111827", bbox=probe_style)
    ax.text(5.0, 4.9, "Promtail DaemonSet\n[Modality: Container Logs]\n/var/log/pods/*.log Streaming", ha='center', va='center', fontsize=7.5, color="#111827", bbox=probe_style)

    # Intra Layer 1 Arrows
    for x in [-3.8, 0.6, 5.0]:
        ax.annotate("", xy=(x, 5.35), xytext=(x, 5.85), arrowprops=dict(arrowstyle="->", lw=1.3, color="#1F2937"))

    # =========================================================================
    # LAYER 2: FEDERATED STORAGE
    # =========================================================================
    rect2 = patches.FancyBboxPatch((-5.8, 2.45), 12.8, 1.35, **layer_container_style)
    ax.add_patch(rect2)
    
    # Left Badge
    ax.text(-7.2, 3.12, "Layer 2\nMultimodal\nFederated\nStorage", 
            ha='center', va='center', fontsize=9, fontweight='bold', color='#00664B',
            bbox=dict(boxstyle="round,pad=0.5", fc="#E6F5F0", ec="#009E73", lw=1.6))

    ax.text(-3.8, 3.12, "Grafana Tempo\n[Distributed Trace Store]\nOTLP Inverted Trace Indexing", ha='center', va='center', fontsize=8, fontweight='bold', color="#111827", bbox=store_tempo_style)
    ax.text(0.6, 3.12, "Prometheus TSDB\n[Time-Series Metric Store]\n15s Scraping & PromQL", ha='center', va='center', fontsize=8, fontweight='bold', color="#111827", bbox=store_prom_style)
    ax.text(5.0, 3.12, "Grafana Loki\n[Structured Event Log Store]\nLabel-Indexed Log Streams", ha='center', va='center', fontsize=8, fontweight='bold', color="#111827", bbox=store_loki_style)

    # Layer 1 -> Layer 2 Unobstructed Vertical Arrows
    ax.annotate("OTLP Spans", xy=(-3.8, 3.55), xytext=(-3.8, 4.45), ha='left', va='center', fontsize=7.2, fontweight='bold', color="#004C7A",
                arrowprops=dict(arrowstyle="->", lw=1.6, color="#0072B2"))
    ax.annotate("Prom Scrapes", xy=(0.6, 3.55), xytext=(0.6, 4.45), ha='left', va='center', fontsize=7.2, fontweight='bold', color="#00664B",
                arrowprops=dict(arrowstyle="->", lw=1.6, color="#009E73"))
    ax.annotate("Log Streams", xy=(5.0, 3.55), xytext=(5.0, 4.45), ha='left', va='center', fontsize=7.2, fontweight='bold', color="#92400E",
                arrowprops=dict(arrowstyle="->", lw=1.6, color="#D97706"))

    # Exemplars Bidirectional Link in Layer 2
    ax.annotate("", xy=(-1.2, 3.12), xytext=(-2.0, 3.12),
                arrowprops=dict(arrowstyle="<->", lw=1.8, color="#009E73"))
    ax.text(-1.6, 3.28, "OpenMetrics\nExemplars", ha='center', va='bottom', fontsize=6.8, fontweight='bold', color="#00664B")

    # =========================================================================
    # LAYER 3: CAUSAL CORRELATION & RCA
    # =========================================================================
    rect3 = patches.FancyBboxPatch((-5.8, 0.65), 12.8, 1.35, **layer_container_style)
    ax.add_patch(rect3)
    
    # Left Badge
    ax.text(-7.2, 1.32, "Layer 3\nCausal\nCorrelation &\nRCA Engine", 
            ha='center', va='center', fontsize=9, fontweight='bold', color='#5C183B',
            bbox=dict(boxstyle="round,pad=0.5", fc="#F5EDF6", ec="#882255", lw=1.6))

    ax.text(-3.8, 1.32, "Algorithm 1: Span Self-Time\nT_self = T_span - sum(T_child)\nEliminates Cascading Span Bias", ha='center', va='center', fontsize=7.5, fontweight='bold', color="#111827", bbox=correl_algo1_style)
    ax.text(2.8, 1.32, "Algorithm 2: Cross-Modal Evidence Fusion\nV* = argmax(w_m*S_metric + w_l*S_log + w_t*S_trace)\nCorrelates Exemplar Trace Context with Metric/Log Signatures", ha='center', va='center', fontsize=7.5, fontweight='bold', color="#111827", bbox=correl_algo2_style)

    # Layer 2 -> Layer 3 Unobstructed Vertical Arrows
    ax.annotate("Trace Trees", xy=(-3.8, 1.8), xytext=(-3.8, 2.7), ha='right', va='center', fontsize=7.2, fontweight='bold', color="#882255",
                arrowprops=dict(arrowstyle="->", lw=1.6, color="#882255"))
    ax.annotate("PromQL deltaM > 3sigma", xy=(0.6, 1.8), xytext=(0.6, 2.7), ha='left', va='center', fontsize=7.2, fontweight='bold', color="#882255",
                arrowprops=dict(arrowstyle="->", lw=1.6, color="#882255"))
    ax.annotate("LogQL Crash Sigs", xy=(5.0, 1.8), xytext=(5.0, 2.7), ha='left', va='center', fontsize=7.2, fontweight='bold', color="#882255",
                arrowprops=dict(arrowstyle="->", lw=1.6, color="#882255"))

    # Layer 3 Horizontal Connection
    ax.annotate("", xy=(-1.2, 1.32), xytext=(-2.0, 1.32),
                arrowprops=dict(arrowstyle="->", lw=1.8, color="#882255"))
    ax.text(-1.6, 1.48, "Disambiguated\nT_self", ha='center', va='bottom', fontsize=6.8, fontweight='bold', color="#5C183B")

    # =========================================================================
    # LAYER 4: CLOSED-LOOP REMEDIATION
    # =========================================================================
    rect4 = patches.FancyBboxPatch((-5.8, -1.05), 12.8, 0.95, **layer_container_style)
    ax.add_patch(rect4)
    
    # Left Badge
    ax.text(-7.2, -0.58, "Layer 4\nClosed-Loop\nRemediation", 
            ha='center', va='center', fontsize=9, fontweight='bold', color='#9A4300',
            bbox=dict(boxstyle="round,pad=0.5", fc="#FDF3E7", ec="#D55E00", lw=1.6))

    ax.text(0.6, -0.58, "Autonomous Diagnostic Verification & Kubernetes Custom Operator\nStandardized JSONL Evidence Audit Trail  |  Automated Pod Rescheduling  |  SLO Enforcement", ha='center', va='center', fontsize=8, fontweight='bold', color="#111827", bbox=act_style)

    # Layer 3 -> Layer 4 Verdict Arrow
    ax.annotate("Authoritative Diagnostic Verdict V*", xy=(0.6, -0.2), xytext=(0.6, 0.75), ha='left', va='center', fontsize=7.8, fontweight='bold', color="#D55E00",
                arrowprops=dict(arrowstyle="->", lw=2.0, color="#D55E00"))

    # Feedback Loop (Dashed for non-color differentiation)
    ax.plot([6.8, 7.5, 7.5, 7.0], [-0.58, -0.58, 5.55, 5.55], color="#0072B2", lw=1.6, ls="--")
    ax.annotate("", xy=(6.9, 5.55), xytext=(7.1, 5.55),
                arrowprops=dict(arrowstyle="->", lw=1.6, color="#0072B2"))
    ax.text(7.65, 2.5, "Dynamic Telemetry Throttling\n& Automated Healing Loop", ha='left', va='center', fontsize=7.2, fontweight='bold', color="#004C7A", rotation=270)

    # Save
    out_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "figures")
    out_path = os.path.join(out_dir, "fig_panoptes_architecture.png")
    plt.tight_layout()
    plt.savefig(out_path, dpi=300, bbox_inches='tight')
    plt.close()
    print(f"Successfully generated Okabe-Ito color-blind compliant diagram at: {out_path}")

if __name__ == "__main__":
    draw_diagram()
