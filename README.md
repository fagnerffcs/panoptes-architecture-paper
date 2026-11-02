# Replication Package: PANOPTES — A Reference Architecture and Multimodal Correlation Engine for Cloud-Native Observability

Este repositório contém o Pacote de Replicação (*Replication Package*) completo, aberto e auditável do artigo de pesquisa científica estruturado no padrão **ACM (`acmart` / `sigconf`)** e alinhado às diretrizes de **Open Science & Empirical Standards da ACM/IEEE**:

> **Título do Artigo:** PANOPTES: A Reference Architecture and Multimodal Correlation Engine for Cloud-Native Observability  
> **Autores:** Fagner Silva, Jackson Raniel, Vinícius Cardoso Garcia  
> **Instituição:** Centro de Informática, Universidade Federal de Pernambuco (CIn - UFPE) / UPE  
> **Licença:** MIT License  

---

## 📌 Visão Geral do Artefato e Fundamentação Metodológica

O **PANOPTES** é uma **Arquitetura de Referência** e um **Motor de Correlação Multimodal** projetado para resolver a fragmentação diagnóstica (silos de telemetria) e o viés de propagação em cascata (*Cascading Span Bias*) em microsserviços distribuídos sobre Kubernetes.

O projeto é fundamentado na metodologia **Design Science Research (DSR)** (Simon, 1969; Hevner et al., 2004; Peffers et al., 2007; Vaishnavi & Kuechler, 2015), estabelecendo três contribuições complementares:
1. **Artefato de Arquitetura (Modelo):** Um framework de 4 camadas (Ingestão/Probes, Armazenamento Federado, Correlação Causal e Remediação em Malha Fechada).
2. **Artefato de Método (Algoritmo):** Decomposição formal do Tempo Próprio de Spans ($T_{\text{self}} = T_{\text{span}} - \sum T_{\text{child}}$) e fusão contextual via OpenMetrics Exemplars.
3. **Artefato de Instanciação (Software):** Implementação concreta como *Infrastructure-as-Code* (IaC) integrando eBPF (Grafana Beyla), OpenTelemetry Collector, Prometheus, Grafana Loki e Grafana Tempo.

---

## 🗂️ Estrutura do Repositório

```text
panoptes-architecture-paper/
├── .gitignore                                     # Regras de exclusão Git (LaTeX, Python, OS)
├── LICENSE                                        # Licença MIT
├── README.md                                      # Documentação do pacote de replicação
├── sigconf.tex                                    # Documento principal LaTeX (template ACM sigconf)
├── references.bib                                 # Base bibliográfica BibTeX completa e validada
├── data/                                          # Dados empíricos coletados durante os experimentos
│   ├── scenario1_workload_baseline.csv            # Telemetria de linha de base da aplicação (N = 30)
│   ├── scenario2_overhead_panoptes.csv            # Amostragem de consumo de CPU/RAM da stack (N = 30)
│   ├── scenario3_diagnostic_trials_stratified.csv # Ensaios diagnósticos com regimes baselines (L2, L3)
│   ├── scenario4b_optimized_trials.csv            # Ensaios pareados e estratificados no PANOPTES (N = 30)
│   └── scenario4b_evidence_audit.jsonl            # Trilha de auditoria JSONL com evidências e queries
├── figures/                                       # Diagramas TikZ e gráficos empíricos em alta resolução
│   ├── fig-panoptes-architecture.tex              # Diagrama arquitetural em TikZ das 4 camadas
│   ├── final_accuracy_comparison.png              # Gráfico comparativo de acurácia (L2 vs. L3 vs. L4)
│   ├── final_mttdiag_comparison.png               # Comparação de tempo até o diagnóstico (MTTDiag)
│   ├── kaplan_meier_survival_curve.png            # Curva de sobrevivência diagnóstica de Kaplan-Meier
│   ├── scenario2_cpu_overhead.png                 # Distribuição de CPU: Carga vs. Observabilidade
│   └── scenario2_memory_overhead.png              # Distribuição de RAM da stack de observabilidade
├── tables/                                        # Tabelas LaTeX modulares
│   ├── tab-dsr-elements.tex                       # Mapeamento epistemológico DSR do PANOPTES
│   ├── tab-panoptes-layers.tex                    # Taxonomia e invariantes das 4 camadas
│   ├── tab-evaluation-accuracy-latency.tex        # Tabela comparativa de acurácia, latência e testes
│   └── tab-overhead-budget.tex                    # Orçamento de overhead e consumo de recursos
├── scripts/                                       # Automação de provisionamento, execução e análise
│   ├── deploy-panoptes.yml                        # Playbook Ansible para provisionamento da stack
│   ├── check-panoptes-health.sh                   # Script de pre-flight check e prontidão de telemetria
│   ├── run-scenario2-overhead.py                  # Coletor de consumo de recursos em estado estável
│   ├── run-scenario4-optimized-trials.py          # Orquestrador experimental de injeção e diagnóstico
│   └── analyze_panoptes_evaluation.py             # Script de inferência estatística não-paramétrica
└── sections/                                      # Código-fonte LaTeX modularizado
    ├── 01.introduction.tex                        # Introdução, motivação e questões de pesquisa
    ├── 02.background_and_problem.tex              # Fundamentação de telemetria e o dilema diagnóstico
    ├── 03.dsr_methodology.tex                     # Metodologia Design Science Research (DSRM)
    ├── 04.panoptes_reference_architecture.tex     # A Arquitetura de Referência PANOPTES em 4 camadas
    ├── 05.instantiation_and_algorithms.tex       # Instanciação IaC e algoritmos formais (T_self)
    ├── 06.empirical_evaluation.tex                # Avaliação experimental controlada (N = 30)
    ├── 07.threats_to_validity.tex                 # Ameaças à validade (Construct, Internal, External)
    └── 08.conclusion.tex                          # Conclusão, trabalhos futuros e declarações de integridade
```

---

## ⚙️ Reprodução Experimental e Replicação

### 1. Requisitos do Ambiente
* **Sistema Operacional:** Linux (Ubuntu 22.04 LTS ou superior / WSL2)
* **Cluster:** Kubernetes v1.28+ (K3s ou K3d recomendado) com quotas de nós ($2\,\text{vCPUs}$, $4096\,\text{MiB}$ RAM)
* **Ferramental:** Python 3.10+, Ansible 2.14+, `kubectl`, `helm`

### 2. Executando a Análise Estatística Direta
Para revalidar imediatamente todos os testes de hipótese, acurácia, latência e tamanhos de efeito a partir dos dados brutos:

```bash
# Executa inferência não-paramétrica (Fisher, McNemar, Wilcoxon, Â_12)
python3 scripts/analyze_panoptes_evaluation.py
```

### 3. Provisionamento do Cluster e Execução dos Ensaios
```bash
# 1. Aplica o playbook Ansible para configurar a stack PANOPTES
ansible-playbook -i localhost, scripts/deploy-panoptes.yml

# 2. Executa a checagem de prontidão e pipelines de telemetria
bash scripts/check-panoptes-health.sh

# 3. Executa as rodadas pareadas de injeção de caos e diagnóstico cego
python3 scripts/run-scenario4-optimized-trials.py
```

---

## 📊 Principais Resultados Empíricos

| Dimensão Avaliada | Regime Baseline (CLI / Tracing) | PANOPTES Reference Architecture | Evidência / Teste Estatístico |
|---|---|---|---|
| **Acurácia Diagnóstica ($Acc$)** | $20.00\%$ (CLI) / $0.00\%$ (Tracing) | **$83.33\%$ ($25/30$)** | Exato de Fisher $p = 5.49 \times 10^{-12}$; McNemar $p = 2.98 \times 10^{-8}$ |
| **Latência Diagnóstica ($MTTDiag$)** | Mediana $300.00\,\text{s}$ (Penalidade) | **Mediana $17.27\,\text{s}$** (Média $54.52 \pm 98.41\,\text{s}$) | Wilcoxon Pareado $W = 465.0$, $p = 1.35 \times 10^{-4}$, $\hat{A}_{12} = 0.817$ |
| **Overhead de CPU ($\Delta_{\text{CPU}}$)** | Não delimitado | **$5.26\% \pm 2.65\%$** da carga ($131.17 \pm 66.26\,\text{mCPU}$) | Conforme Princípio de Controle **CP1** ($\le 10\%$) |
| **Overhead de Memória RAM** | Isolado em silos | **$2{,}237.00 \pm 455.45\,\text{MiB}$** (Cluster completo) | Telemetria federada sem esgotamento de nós |

---

## 📜 Licença
Os artefatos deste pacote de replicação são distribuídos sob a licença **MIT License**, garantindo transparência, auditabilidade e reprodutibilidade acadêmica irrestrita.
