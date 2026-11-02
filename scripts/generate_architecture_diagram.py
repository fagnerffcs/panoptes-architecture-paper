#!/usr/bin/env python3
"""
Renders a publication-quality diagram of the 4-layer PANOPTES reference architecture
to high-resolution PNG (figures/fig_panoptes_architecture.png).
"""

import os
import matplotlib.pyplot as plt
import matplotlib.patches as patches

def draw_diagram():
    fig, ax = plt.subplots(figsize=(14, 10), dpi=300)
    ax.set_xlim(-8.5, 8.5)
    ax.set_ylim(-1.5, 7.2)
    ax.axis('off')

    # Styles
    badge_style = dict(boxstyle="round,pad=0.4", fc="#E5E7EB", ec="#374151", lw=1.5)
    layer_style = dict(boxstyle="round,pad=0.4", fc="#F9FAFB", ec="#9CA3AF", lw=1.2, ls="--")
    sut_style = dict(boxstyle="round,pad=0.3", fc="#DBEAFE", ec="#1D4ED8", lw=1.2)
    probe_style = dict(boxstyle="round,pad=0.3", fc="#CFFAFE", ec="#0E7490", lw=1.2)
    store_style = dict(boxstyle="round,pad=0.3", fc="#CCFBF1", ec="#0F766E", lw=1.2)
    correl_style = dict(boxstyle="round,pad=0.3", fc="#F3E8FF", ec="#7E22CE", lw=1.2)
    act_style = dict(boxstyle="round,pad=0.3", fc="#FFEDD5", ec="#C2410C", lw=1.2)

    # --- LAYER 1 ---
    # Background Box
    rect1 = patches.FancyBboxPatch((-5.8, 4.3), 12.8, 2.5, **layer_style)
    ax.add_patch(rect1)
    # Left Badge
    ax.text(-7.2, 5.55, "Layer 1\nTelemetry\nIngestion &\nProbing", 
            ha='center', va='center', fontsize=9, fontweight='bold', color='#1E3A8A',
            bbox=dict(boxstyle="round,pad=0.5", fc="#DBEAFE", ec="#1D4ED8", lw=1.5))
    
    # SUT Row
    ax.text(-3.8, 6.2, "frontend / cart\n(HTTP/gRPC Gateway & State)", ha='center', va='center', fontsize=8, fontweight='bold', bbox=sut_style)
    ax.text(0.6, 6.2, "shipping / checkout\n(Synchronous RPC Workloads)", ha='center', va='center', fontsize=8, fontweight='bold', bbox=sut_style)
    ax.text(5.0, 6.2, "payment / currency\n(Kafka Async & Background)", ha='center', va='center', fontsize=8, fontweight='bold', bbox=sut_style)

    # Probes Row
    ax.text(-3.8, 4.9, "OTel SDK & Auto-Instr.\nModality: Distributed Traces\nW3C TraceContext Propagation", ha='center', va='center', fontsize=7.5, bbox=probe_style)
    ax.text(0.6, 4.9, "eBPF & cgroup v2 Scrapers\nModality: Socket & CPU Metrics\ntcp_v4_connect | Throttling", ha='center', va='center', fontsize=7.5, bbox=probe_style)
    ax.text(5.0, 4.9, "Promtail DaemonSet\nModality: Container Logs\n/var/log/pods/*.log Streaming", ha='center', va='center', fontsize=7.5, bbox=probe_style)

    # Arrows L1 Intra
    for x in [-3.8, 0.6, 5.0]:
        ax.annotate("", xy=(x, 5.35), xytext=(x, 5.85), arrowprops=dict(arrowstyle="->", lw=1.2, color="#374151"))

    # --- LAYER 2 ---
    rect2 = patches.FancyBboxPatch((-5.8, 2.45), 12.8, 1.35, **layer_style)
    ax.add_patch(rect2)
    ax.text(-7.2, 3.12, "Layer 2\nMultimodal\nFederated\nStorage", 
            ha='center', va='center', fontsize=9, fontweight='bold', color='#0F766E',
            bbox=dict(boxstyle="round,pad=0.5", fc="#CCFBF1", ec="#0F766E", lw=1.5))

    ax.text(-3.8, 3.12, "Grafana Tempo\nModality: Distributed Traces\nOTLP Inverted Trace Indexing", ha='center', va='center', fontsize=8, fontweight='bold', bbox=store_style)
    ax.text(0.6, 3.12, "Prometheus TSDB\nModality: Time-Series Metrics\nHigh-Frequency Scraping & PromQL", ha='center', va='center', fontsize=8, fontweight='bold', bbox=store_style)
    ax.text(5.0, 3.12, "Grafana Loki\nModality: Structured Event Logs\nLabel-Indexed Log Streams", ha='center', va='center', fontsize=8, fontweight='bold', bbox=store_style)

    # Arrows L1 -> L2
    ax.annotate("OTLP Spans", xy=(-3.8, 3.55), xytext=(-3.8, 4.45), ha='left', va='center', fontsize=7, color="#1F2937",
                arrowprops=dict(arrowstyle="->", lw=1.5, color="#1F2937"))
    ax.annotate("Prom Scrapes", xy=(0.6, 3.55), xytext=(0.6, 4.45), ha='left', va='center', fontsize=7, color="#1F2937",
                arrowprops=dict(arrowstyle="->", lw=1.5, color="#1F2937"))
    ax.annotate("Log Streams", xy=(5.0, 3.55), xytext=(5.0, 4.45), ha='left', va='center', fontsize=7, color="#1F2937",
                arrowprops=dict(arrowstyle="->", lw=1.5, color="#1F2937"))

    # Exemplars Arrow in L2
    ax.annotate("", xy=(-1.2, 3.12), xytext=(-2.0, 3.12),
                arrowprops=dict(arrowstyle="<->", lw=1.5, color="#0F766E"))
    ax.text(-1.6, 3.28, "OpenMetrics\nExemplars", ha='center', va='bottom', fontsize=6.5, fontweight='bold', color="#0F766E")

    # --- LAYER 3 ---
    rect3 = patches.FancyBboxPatch((-5.8, 0.65), 12.8, 1.35, **layer_style)
    ax.add_patch(rect3)
    ax.text(-7.2, 1.32, "Layer 3\nCausal\nCorrelation &\nRCA Engine", 
            ha='center', va='center', fontsize=9, fontweight='bold', color='#7E22CE',
            bbox=dict(boxstyle="round,pad=0.5", fc="#F3E8FF", ec="#7E22CE", lw=1.5))

    ax.text(-3.8, 1.32, "Algorithm 1: Span Self-Time\nT_self = T_span - sum(T_child)\nEliminates Cascading Span Bias", ha='center', va='center', fontsize=7.5, fontweight='bold', bbox=correl_style)
    ax.text(2.8, 1.32, "Algorithm 2: Cross-Modal Evidence Fusion\nV* = argmax(w_m*S_metric + w_l*S_log + w_t*S_trace)\nCorrelates Exemplar Trace Context with Metric/Log Signatures", ha='center', va='center', fontsize=7.5, fontweight='bold', bbox=correl_style)

    # Arrows L2 -> L3
    ax.annotate("Trace Trees", xy=(-3.8, 1.8), xytext=(-3.8, 2.7), ha='right', va='center', fontsize=7, color="#7E22CE",
                arrowprops=dict(arrowstyle="->", lw=1.5, color="#7E22CE"))
    ax.annotate("PromQL deltaM > 3sigma", xy=(0.6, 1.8), xytext=(0.6, 2.7), ha='left', va='center', fontsize=7, color="#7E22CE",
                arrowprops=dict(arrowstyle="->", lw=1.5, color="#7E22CE"))
    ax.annotate("LogQL Crash Sigs", xy=(5.0, 1.8), xytext=(5.0, 2.7), ha='left', va='center', fontsize=7, color="#7E22CE",
                arrowprops=dict(arrowstyle="->", lw=1.5, color="#7E22CE"))

    # L3 Intra Arrow
    ax.annotate("", xy=(-1.2, 1.32), xytext=(-2.0, 1.32),
                arrowprops=dict(arrowstyle="->", lw=1.5, color="#7E22CE"))
    ax.text(-1.6, 1.48, "Disambiguated\nT_self", ha='center', va='bottom', fontsize=6.5, fontweight='bold', color="#7E22CE")

    # --- LAYER 4 ---
    rect4 = patches.FancyBboxPatch((-5.8, -1.05), 12.8, 0.95, **layer_style)
    ax.add_patch(rect4)
    ax.text(-7.2, -0.58, "Layer 4\nClosed-Loop\nRemediation", 
            ha='center', va='center', fontsize=9, fontweight='bold', color='#C2410C',
            bbox=dict(boxstyle="round,pad=0.5", fc="#FFEDD5", ec="#C2410C", lw=1.5))

    ax.text(0.6, -0.58, "Autonomous Diagnostic Verification & Kubernetes Custom Operator\nStandardized JSONL Evidence Audit Trail  |  Automated Pod Rescheduling  |  SLO Enforcement", ha='center', va='center', fontsize=8, fontweight='bold', bbox=act_style)

    # Arrow L3 -> L4
    ax.annotate("Authoritative Diagnostic Verdict V*", xy=(0.6, -0.2), xytext=(0.6, 0.75), ha='left', va='center', fontsize=7.5, fontweight='bold', color="#C2410C",
                arrowprops=dict(arrowstyle="->", lw=1.8, color="#C2410C"))

    # Feedback Loop around right side
    ax.plot([6.8, 7.5, 7.5, 7.0], [-0.58, -0.58, 5.55, 5.55], color="#1D4ED8", lw=1.4, ls="--")
    ax.annotate("", xy=(6.9, 5.55), xytext=(7.1, 5.55),
                arrowprops=dict(arrowstyle="->", lw=1.4, color="#1D4ED8"))
    ax.text(7.6, 2.5, "Dynamic Telemetry Throttling\n& Automated Healing Loop", ha='left', va='center', fontsize=7, color="#1D4ED8", rotation=270)

    # Save
    out_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "figures")
    out_path = os.path.join(out_dir, "fig_panoptes_architecture.png")
    plt.tight_layout()
    plt.savefig(out_path, dpi=300, bbox_inches='tight')
    plt.close()
    print(f"Successfully generated diagram at: {out_path}")

if __name__ == "__main__":
    draw_diagram()
