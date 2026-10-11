"""
create_notebook.py
==================
Generates and executes the complete, reproducible Jupyter Notebook:
notebooks/maternal_mortality_analysis.ipynb

Populates real execution counts, stdout streams, HTML DataFrame tables,
and embedded base64 PNG figures so the notebook renders with full outputs on GitHub.

Author: Dr. Aung Chit Moe (MBBS)
Date: October 2026
"""

import os
import io
import ast
import json
import base64
import contextlib
import pandas as pd
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt


def execute_cells(cells, notebooks_dir):
    """Executes all code cells in order inside notebooks_dir and populates outputs."""
    exec_ns = {}
    exec_count = 1
    orig_cwd = os.getcwd()
    os.chdir(notebooks_dir)

    try:
        for idx, cell in enumerate(cells):
            if cell.get("cell_type") != "code":
                continue

            cell["id"] = f"cell-{idx:02d}"
            cell["execution_count"] = exec_count
            outputs = []

            code_str = "".join(cell["source"])
            tree = ast.parse(code_str)

            stdout_buf = io.StringIO()
            last_val = None

            # Intercept plt.show() to capture figure as base64 PNG
            captured_pngs = []

            def custom_show(*args, **kwargs):
                buf = io.BytesIO()
                plt.savefig(buf, format="png", dpi=150, bbox_inches="tight")
                buf.seek(0)
                b64 = base64.b64encode(buf.read()).decode("ascii")
                captured_pngs.append(b64)
                plt.close("all")

            with contextlib.redirect_stdout(stdout_buf):
                # Inject custom plt.show if plt is already imported
                if "plt" in exec_ns:
                    exec_ns["plt"].show = custom_show

                if tree.body and isinstance(tree.body[-1], ast.Expr):
                    last_expr = ast.Expression(tree.body[-1].value)
                    body_mod = ast.Module(body=tree.body[:-1], type_ignores=[])
                    ast.fix_missing_locations(body_mod)
                    ast.fix_missing_locations(last_expr)
                    exec(compile(body_mod, f"<cell-{exec_count}>", "exec"), exec_ns)
                    if "plt" in exec_ns:
                        exec_ns["plt"].show = custom_show
                    last_val = eval(compile(last_expr, f"<cell-{exec_count}>", "eval"), exec_ns)
                else:
                    exec(compile(tree, f"<cell-{exec_count}>", "exec"), exec_ns)

            std_text = stdout_buf.getvalue()
            if std_text:
                outputs.append({
                    "name": "stdout",
                    "output_type": "stream",
                    "text": [line + "\n" for line in std_text.splitlines()]
                })

            for b64 in captured_pngs:
                outputs.append({
                    "data": {
                        "image/png": b64,
                        "text/plain": ["<Figure size 1500x825 with Axes>"]
                    },
                    "metadata": {},
                    "output_type": "display_data"
                })

            if last_val is not None:
                data_dict = {"text/plain": [repr(last_val)]}
                if hasattr(last_val, "to_html"):
                    data_dict["text/html"] = [last_val.to_html()]
                outputs.append({
                    "data": data_dict,
                    "execution_count": exec_count,
                    "metadata": {},
                    "output_type": "execute_result"
                })

            cell["outputs"] = outputs
            exec_count += 1
    finally:
        os.chdir(orig_cwd)


def build_notebook(base_dir: str):
    notebooks_dir = os.path.join(base_dir, "notebooks")
    os.makedirs(notebooks_dir, exist_ok=True)
    
    cells = []
    
    # Cell 1: Markdown Title & Introduction
    cells.append({
        "id": "cell-00",
        "cell_type": "markdown",
        "metadata": {},
        "source": [
            "# Macroeconomic Financing, Demographic Transition, and Global Maternal Mortality\n",
            "## A 24-Year Longitudinal Study across 195 Countries (177-Country Balanced Panel, 2000–2023)\n",
            "\n",
            "**Author:** Dr. Aung Chit Moe (MBBS)  \n",
            "**Investigator:** MBBS Physician Transitioning into Healthcare Data Analytics  \n",
            "**Primary Sources:** WHO/UN MMEIG 2025 Estimation Round • World Bank World Development Indicators (WDI)  \n",
            "\n",
            "### Notebook Workflow\n",
            "1. **Environment & Data Ingestion:** Loading the integrated analytical master dataset (`data/processed/maternal_mortality_analytical_master.csv`).\n",
            "2. **Exploratory Data Analysis:** Summary benchmarks, income-group trajectories, and the Preston curve.\n",
            "3. **Demographic & Health Financing Gradients:** Fertility, adolescent pregnancy, and health spending priority (% of GDP).\n",
            "4. **Cross-Sectional Models (OLS):** Evaluating structural shifts across 2000, 2010, and 2023.\n",
            "5. **Primary Econometric Model:** Two-Way Fixed Effects (TWFE) panel regression with country-clustered standard errors.\n",
            "6. **Sensitivity Analyses:** Extreme-bound testing across MMEIG 80% Uncertainty Intervals."
        ]
    })
    
    # Cell 2: Code Imports
    cells.append({
        "cell_type": "code",
        "execution_count": None,
        "metadata": {},
        "outputs": [],
        "source": [
            "import os\n",
            "import numpy as np\n",
            "import pandas as pd\n",
            "import matplotlib.pyplot as plt\n",
            "import seaborn as sns\n",
            "import statsmodels.api as sm\n",
            "import statsmodels.formula.api as smf\n",
            "\n",
            "# Styling setup\n",
            "plt.rcParams['font.sans-serif'] = 'Arial'\n",
            "plt.rcParams['figure.dpi'] = 150\n",
            "sns.set_theme(style='whitegrid', palette='deep')\n",
            "print('Environment initialized successfully.')"
        ]
    })
    
    # Cell 3: Code Data Loading & Inspection
    cells.append({
        "cell_type": "code",
        "execution_count": None,
        "metadata": {},
        "outputs": [],
        "source": [
            "data_path = '../data/processed/maternal_mortality_analytical_master.csv'\n",
            "df = pd.read_csv(data_path)\n",
            "df_bal = df[df['is_balanced_sample'] == 1].copy()\n",
            "\n",
            "print(f'Total Grid Observations: {len(df):,} rows ({df[\"country_iso3\"].nunique()} countries, 2000-2023)')\n",
            "print(f'Balanced Analytical Sample: {len(df_bal):,} rows ({df_bal[\"country_iso3\"].nunique()} countries)')\n",
            "df_bal[['country_iso3', 'year', 'mmr_pt', 'gdp_pcap_ppp', 'chex_gdp_pct', 'tfr', 'ado_fert_rate']].head(5)"
        ]
    })
    
    # Cell 4: Markdown Section 1
    cells.append({
        "id": "cell-md-1",
        "cell_type": "markdown",
        "metadata": {},
        "source": [
            "## 1. Descriptive Benchmarks Across Decades (2000 vs 2010 vs 2015 vs 2023)"
        ]
    })
    
    # Cell 5: Code Benchmarks
    cells.append({
        "cell_type": "code",
        "execution_count": None,
        "metadata": {},
        "outputs": [],
        "source": [
            "bench_summary = df_bal.groupby('year').agg({\n",
            "    'mmr_pt': ['mean', 'median', 'std'],\n",
            "    'gdp_pcap_ppp': ['mean', 'median'],\n",
            "    'chex_gdp_pct': ['mean', 'median'],\n",
            "    'tfr': ['mean', 'median'],\n",
            "    'maternal_deaths': 'sum'\n",
            "}).loc[[2000, 2010, 2015, 2023]]\n",
            "\n",
            "bench_summary.round(2)"
        ]
    })

    # Cell 5b: Code 2023 Income Group Disparity Table
    cells.append({
        "cell_type": "code",
        "execution_count": None,
        "metadata": {},
        "outputs": [],
        "source": [
            "df_2023 = df_bal[df_bal['year'] == 2023].copy()\n",
            "inc_summary_2023 = df_2023.groupby('income_level_name').agg(\n",
            "    n_countries=('country_iso3', 'count'),\n",
            "    mean_mmr=('mmr_pt', 'mean'),\n",
            "    median_mmr=('mmr_pt', 'median'),\n",
            "    mean_gdp_ppp=('gdp_pcap_ppp', 'mean'),\n",
            "    mean_chex_pct=('chex_gdp_pct', 'mean'),\n",
            "    mean_tfr=('tfr', 'mean'),\n",
            "    mean_ado_fert=('ado_fert_rate', 'mean')\n",
            ").loc[['Low income', 'Lower middle income', 'Upper middle income', 'High income']]\n",
            "inc_summary_2023.round(2)"
        ]
    })
    
    # Cell 6: Code Fig 1 Trajectories
    cells.append({
        "cell_type": "code",
        "execution_count": None,
        "metadata": {},
        "outputs": [],
        "source": [
            "# Plotting MMR Trajectories by Income Tier\n",
            "income_order = ['Low income', 'Lower middle income', 'Upper middle income', 'High income']\n",
            "palette = {'Low income': '#d95f02', 'Lower middle income': '#7570b3', 'Upper middle income': '#1b9e77', 'High income': '#386cb0'}\n",
            "\n",
            "fig, ax = plt.subplots(figsize=(10, 5))\n",
            "traj = df_bal.groupby(['year', 'income_level_name'])['mmr_pt'].mean().reset_index()\n",
            "for inc in income_order:\n",
            "    sub_traj = traj[traj['income_level_name'] == inc]\n",
            "    ax.plot(sub_traj['year'], sub_traj['mmr_pt'], label=inc, color=palette[inc], linewidth=2.5, marker='o', markersize=3)\n",
            "\n",
            "ax.set_yscale('log')\n",
            "ax.set_ylim(2, 1400)\n",
            "ax.set_title('Global MMR Trajectories by World Bank Income Group (2000–2023)', fontsize=12, fontweight='bold')\n",
            "ax.set_xlabel('Calendar Year')\n",
            "ax.set_ylabel('MMR (Deaths / 100k Live Births, Log Scale)')\n",
            "ax.legend(title='Income Group', loc='lower left', ncol=2)\n",
            "plt.tight_layout()\n",
            "plt.show()"
        ]
    })
    
    # Cell 6a: Markdown Section on Preston Curve
    cells.append({
        "id": "cell-md-1b",
        "cell_type": "markdown",
        "metadata": {},
        "source": [
            "## 1B. The Preston Curve of Maternal Survival (Figure 2)\n",
            "Evaluating the non-linear diminishing returns relationship between constant-price PPP GDP per capita and Maternal Mortality Ratio (2023), strictly decoupled from Health Expenditure (% of GDP)."
        ]
    })

    # Cell 6a_code: Code Fig 2 Preston Curve
    cells.append({
        "cell_type": "code",
        "execution_count": None,
        "metadata": {},
        "outputs": [],
        "source": [
            "fig, ax = plt.subplots(figsize=(10, 5.5))\n",
            "for inc in income_order:\n",
            "    sub = df_2023[df_2023['income_level_name'] == inc]\n",
            "    ax.scatter(sub['gdp_pcap_ppp'], sub['mmr_pt'], color=palette[inc], label=inc, s=65, alpha=0.88, edgecolors='white', linewidth=0.6)\n",
            "\n",
            "z = np.polyfit(df_2023['log_gdp_pcap_ppp'], df_2023['log_mmr_pt'], 2)\n",
            "p = np.poly1d(z)\n",
            "x_vals = np.linspace(df_2023['log_gdp_pcap_ppp'].min(), df_2023['log_gdp_pcap_ppp'].max(), 100)\n",
            "ax.plot(np.exp(x_vals), np.exp(p(x_vals)), color='#b2182b', linewidth=2.5, linestyle='--', label='Quadratic Log-Log Fit (rho = -0.85, p < 0.001)')\n",
            "ax.set_xscale('log')\n",
            "ax.set_yscale('log')\n",
            "ax.set_title('The Preston Curve of Maternal Survival: Real GDP per Capita vs MMR (2023)', fontweight='bold')\n",
            "ax.set_xlabel('Real GDP per Capita, PPP (Constant 2021 International $, Log Scale)')\n",
            "ax.set_ylabel('MMR (Deaths / 100k Live Births, Log Scale)')\n",
            "ax.legend(loc='lower left')\n",
            "plt.tight_layout()\n",
            "plt.show()"
        ]
    })

    # Cell 6b: Markdown Section on Fertility & Adolescent Health
    cells.append({
        "id": "cell-md-2",
        "cell_type": "markdown",
        "metadata": {},
        "source": [
            "## 2. Demographic Transition & Adolescent Pregnancy (Figure 6)\n",
            "Evaluating Total Fertility Rate (TFR) and Adolescent Fertility Rate vs Maternal Mortality Ratio (2023)."
        ]
    })

    # Cell 6c: Code Fig 6 Fertility
    cells.append({
        "cell_type": "code",
        "execution_count": None,
        "metadata": {},
        "outputs": [],
        "source": [
            "fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(14, 6))\n",
            "\n",
            "for inc in income_order:\n",
            "    sub = df_2023[df_2023['income_level_name'] == inc]\n",
            "    ax1.scatter(sub['tfr'], sub['mmr_pt'], color=palette[inc], label=inc, s=55, alpha=0.85, edgecolors='white', linewidth=0.5)\n",
            "    ax2.scatter(sub['ado_fert_rate'], sub['mmr_pt'], color=palette[inc], label=inc, s=55, alpha=0.85, edgecolors='white', linewidth=0.5)\n",
            "\n",
            "# Fit curves\n",
            "p1 = np.polyfit(df_2023['tfr'], df_2023['log_mmr_pt'], 1)\n",
            "x1 = np.linspace(df_2023['tfr'].min(), df_2023['tfr'].max(), 100)\n",
            "ax1.plot(x1, np.exp(p1[0]*x1 + p1[1]), color='#b2182b', linewidth=2.5, linestyle='--', label='Trend (rho = +0.79, p < 0.001)')\n",
            "\n",
            "p2 = np.polyfit(df_2023['ado_fert_rate'], df_2023['log_mmr_pt'], 1)\n",
            "x2 = np.linspace(df_2023['ado_fert_rate'].min(), df_2023['ado_fert_rate'].max(), 100)\n",
            "ax2.plot(x2, np.exp(p2[0]*x2 + p2[1]), color='#b2182b', linewidth=2.5, linestyle='--', label='Trend (rho = +0.86, p < 0.001)')\n",
            "\n",
            "ax1.set_yscale('log')\n",
            "ax1.set_title('A: Total Fertility Rate (TFR) vs MMR (2023)', fontweight='bold')\n",
            "ax1.set_xlabel('Total Fertility Rate (Births per Woman)')\n",
            "ax1.set_ylabel('MMR (Deaths / 100k Live Births, Log Scale)')\n",
            "ax1.legend(loc='lower right')\n",
            "\n",
            "ax2.set_yscale('log')\n",
            "ax2.set_title('B: Adolescent Fertility Rate vs MMR (2023)', fontweight='bold')\n",
            "ax2.set_xlabel('Adolescent Births per 1,000 Girls Aged 15–19')\n",
            "ax2.set_ylabel('MMR (Deaths / 100k Live Births, Log Scale)')\n",
            "ax2.legend(loc='lower right')\n",
            "\n",
            "plt.tight_layout()\n",
            "plt.show()"
        ]
    })

    # Cell 6d: Markdown Section on Health Expenditure Decoupled
    cells.append({
        "id": "cell-md-3",
        "cell_type": "markdown",
        "metadata": {},
        "source": [
            "## 3. Domestic Health Financing Priority (% of GDP) Decoupled from GDP (Figure 7)\n",
            "Showing Health Expenditure (% of GDP) vs MMR and median MMR across spending priority quartiles."
        ]
    })

    # Cell 6e: Code Fig 7 Health Expenditure
    cells.append({
        "cell_type": "code",
        "execution_count": None,
        "metadata": {},
        "outputs": [],
        "source": [
            "fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(14, 6))\n",
            "for inc in income_order:\n",
            "    sub = df_2023[df_2023['income_level_name'] == inc]\n",
            "    ax1.scatter(sub['chex_gdp_pct'], sub['mmr_pt'], color=palette[inc], label=inc, s=55, alpha=0.85, edgecolors='white', linewidth=0.5)\n",
            "\n",
            "p_chex = np.polyfit(df_2023['chex_gdp_pct'], df_2023['log_mmr_pt'], 1)\n",
            "xc = np.linspace(df_2023['chex_gdp_pct'].min(), 18, 100)\n",
            "ax1.plot(xc, np.exp(p_chex[0]*xc + p_chex[1]), color='#b2182b', linewidth=2.5, linestyle='--', label='Trend (rho = -0.39, p < 0.001)')\n",
            "ax1.set_yscale('log')\n",
            "ax1.set_title('A: Health Exp (% GDP) vs MMR (2023)', fontweight='bold')\n",
            "ax1.set_xlabel('Current Health Expenditure (% of GDP)')\n",
            "ax1.set_ylabel('MMR (Deaths / 100k Live Births, Log Scale)')\n",
            "ax1.legend(loc='upper right')\n",
            "\n",
            "# Quartiles Bar\n",
            "df_2023['chex_q'] = pd.qcut(df_2023['chex_gdp_pct'], 4, labels=['Q1 (<4.4%)', 'Q2 (4.4%–6.5%)', 'Q3 (6.5%–8.5%)', 'Q4 (>8.5%)'])\n",
            "q_med = df_2023.groupby('chex_q', observed=False)['mmr_pt'].median().reset_index()\n",
            "bars = ax2.bar(q_med['chex_q'], q_med['mmr_pt'], color=['#d73027', '#fc8d59', '#91bfdb', '#4575b4'], width=0.55, edgecolor='black')\n",
            "for b in bars:\n",
            "    ax2.text(b.get_x() + b.get_width()/2., b.get_height() + 4, f'{b.get_height():.1f}', ha='center', va='bottom', fontweight='bold')\n",
            "ax2.set_title('B: Median MMR by Spending Priority Quartile (2023)', fontweight='bold')\n",
            "ax2.set_ylabel('Median MMR (Deaths / 100k Live Births)')\n",
            "ax2.set_ylim(0, 200)\n",
            "\n",
            "plt.tight_layout()\n",
            "plt.show()"
        ]
    })
    
    # Cell 7: Markdown Section 4
    cells.append({
        "id": "cell-md-4",
        "cell_type": "markdown",
        "metadata": {},
        "source": [
            "## 4. Cross-Sectional OLS Regressions (2000, 2010, 2023)\n",
            "Model specification:\n",
            "$$\\ln(\\text{MMR}_i) = \\beta_0 + \\beta_1 \\ln(\\text{GDP}_i) + \\beta_2 \\text{HealthExp}_i + \\beta_3 \\text{TFR}_i + \\beta_4 \\text{AdoFert}_i + \\beta_5 \\text{Urban}_i + \\epsilon_i$$"
        ]
    })
    
    # Cell 8: Code Cross-Sectional OLS
    cells.append({
        "cell_type": "code",
        "execution_count": None,
        "metadata": {},
        "outputs": [],
        "source": [
            "for y in [2000, 2010, 2023]:\n",
            "    sub_y = df_bal[df_bal['year'] == y]\n",
            "    m = smf.ols('log_mmr_pt ~ log_gdp_pcap_ppp + chex_gdp_pct + tfr + ado_fert_rate + urban_pct', data=sub_y).fit(cov_type='HC1')\n",
            "    print(f'=== OLS REGRESSION YEAR {y} (R-squared: {m.rsquared:.3f}) ===')\n",
            "    print(m.summary().tables[1])\n",
            "    print()"
        ]
    })
    
    # Cell 9: Markdown Section 5
    cells.append({
        "id": "cell-md-5",
        "cell_type": "markdown",
        "metadata": {},
        "source": [
            "## 5. Primary Longitudinal Model: Two-Way Fixed Effects (TWFE)\n",
            "Controlling for unobserved time-invariant country fixed effects and secular global time shocks:\n",
            "$$\\ln(\\text{MMR}_{it}) = \\alpha_i + \\gamma_t + \\beta_1 \\ln(\\text{GDP}_{it}) + \\beta_2 \\text{HealthExp}_{it} + \\beta_3 \\text{TFR}_{it} + \\beta_4 \\text{AdoFert}_{it} + \\beta_5 \\text{Urban}_{it} + \\epsilon_{it}$$"
        ]
    })
    
    # Cell 10: Code TWFE (exact dummy-encoded FE with country-clustered CRV1 SEs matching src/analysis.py)
    cells.append({
        "cell_type": "code",
        "execution_count": None,
        "metadata": {},
        "outputs": [],
        "source": [
            "# Two-Way Fixed Effects on balanced panel (177 countries, 24 years, n = 4,248)\n",
            "core_vars = ['log_gdp_pcap_ppp', 'chex_gdp_pct', 'tfr', 'ado_fert_rate', 'urban_pct']\n",
            "twfe_formula = 'log_mmr_pt ~ log_gdp_pcap_ppp + chex_gdp_pct + tfr + ado_fert_rate + urban_pct + C(country_iso3) + C(year)'\n",
            "m_twfe_pt = smf.ols(twfe_formula, data=df_bal).fit(cov_type='cluster', cov_kwds={'groups': df_bal['country_iso3']})\n",
            "\n",
            "print('=== PRIMARY TWO-WAY FIXED EFFECTS RESULTS (CRV1 Clustered SE, n = 4,248) ===')\n",
            "twfe_summary = pd.DataFrame({\n",
            "    'Coef': m_twfe_pt.params[core_vars],\n",
            "    'Cluster_SE': m_twfe_pt.bse[core_vars],\n",
            "    'z_stat': m_twfe_pt.tvalues[core_vars],\n",
            "    'p_value': m_twfe_pt.pvalues[core_vars]\n",
            "})\n",
            "twfe_summary.round(4)"
        ]
    })
    
    # Cell 11: Markdown Section 6
    cells.append({
        "id": "cell-md-6",
        "cell_type": "markdown",
        "metadata": {},
        "source": [
            "## 6. Sensitivity Analyses: 80% Uncertainty Bounds Re-Estimation\n",
            "Testing whether our findings are invariant to MMEIG's lower 10th percentile (`0.1`) and upper 90th percentile (`0.9`) bounds."
        ]
    })
    
    # Cell 12: Code Sensitivity
    cells.append({
        "cell_type": "code",
        "execution_count": None,
        "metadata": {},
        "outputs": [],
        "source": [
            "m_low = smf.ols('log_mmr_low ~ log_gdp_pcap_ppp + chex_gdp_pct + tfr + ado_fert_rate + urban_pct + C(country_iso3) + C(year)',\n",
            "                data=df_bal).fit(cov_type='cluster', cov_kwds={'groups': df_bal['country_iso3']})\n",
            "m_high = smf.ols('log_mmr_high ~ log_gdp_pcap_ppp + chex_gdp_pct + tfr + ado_fert_rate + urban_pct + C(country_iso3) + C(year)',\n",
            "                 data=df_bal).fit(cov_type='cluster', cov_kwds={'groups': df_bal['country_iso3']})\n",
            "\n",
            "sens_df = pd.DataFrame({\n",
            "    'Variable': ['ln(GDP PPP)', 'Health Exp % GDP', 'Total Fertility', 'Adolescent Fert', 'Urban %'],\n",
            "    'Point Estimate (0.5)': [m_twfe_pt.params[v] for v in core_vars],\n",
            "    'Lower Bound (0.1)': [m_low.params[v] for v in core_vars],\n",
            "    'Upper Bound (0.9)': [m_high.params[v] for v in core_vars]\n",
            "})\n",
            "sens_df.round(4)"
        ]
    })

    # Execute all code cells to populate real outputs & embedded figures
    execute_cells(cells, notebooks_dir)

    notebook_dict = {
        "cells": cells,
        "metadata": {
            "kernelspec": {
                "display_name": "Python 3",
                "language": "python",
                "name": "python3"
            },
            "language_info": {
                "name": "python",
                "version": "3.12.8"
            }
        },
        "nbformat": 4,
        "nbformat_minor": 5
    }
    
    nb_path = os.path.join(notebooks_dir, "maternal_mortality_analysis.ipynb")
    with open(nb_path, "w", encoding="utf-8") as f:
        json.dump(notebook_dict, f, indent=2)
    print(f"[SAVED & EXECUTED] Jupyter notebook saved to {nb_path} ({os.path.getsize(nb_path):,} bytes)")

if __name__ == "__main__":
    base_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
    build_notebook(base_dir)
