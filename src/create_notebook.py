"""Generate and execute a notebook reviewing current audited analysis outputs."""
from pathlib import Path
import nbformat
from nbclient import NotebookClient
from research_io import load_results


def create_notebook(base_dir):
    root=Path(base_dir)
    load_results(root)
    nb=nbformat.v4.new_notebook()
    md=nbformat.v4.new_markdown_cell;code=nbformat.v4.new_code_cell
    nb.cells=[
        md('# Global Maternal Mortality, 2000–2023\n\nTrends, inequalities and exploratory associations. Author: Dr. Aung Chit Moe, MBBS.\n\n'
           'WHO/UN MMEIG already uses GDP, general fertility and skilled birth attendance. Regression results are conditional associations with modeled national outcomes. They do not independently establish causal effects or individual clinical risk.'),
        code("from pathlib import Path\nimport sys, json\nimport pandas as pd\nfrom IPython.display import display, Image\nroot = Path.cwd().parent if Path.cwd().name == 'notebooks' else Path.cwd()\nsys.path.insert(0, str(root / 'src'))\nfrom research_io import load_results\nr, audit = load_results(root)\ndf = pd.read_csv(root / 'data/processed/maternal_mortality_analytical_master.csv')\ndisplay(pd.DataFrame([r['sample']]))\nprint('Analytical SHA-256:', r['data_sha256'])"),
        md('## Data quality and sample selection\n\nThe audit calculates its outcome. Missing raw files in a lightweight clone are reported as NOT_CACHED. Integrity checks do not establish absence of bias.'),
        code("display(pd.DataFrame(audit['checks']))\ndisplay(pd.read_csv(root / 'reports/tables/sample_selection.csv'))\ndisplay(pd.DataFrame(r['excluded']))"),
        md('## Descriptive trends\n\nCountry averages weight countries equally. The derived aggregate ratio uses summed country median death estimates and live births and can differ from the official global posterior estimate. Income classifications are fixed at acquisition.'),
        code("display(pd.DataFrame(r['global_trends']).query('year in [2000, 2010, 2015, 2023]'))\ndisplay(Image(filename=str(root / 'docs/images/fig1_mmr_trends_by_income.png')))"),
        md('## Exploratory models\n\nThe panel models include explicit country and year dummy variables, with country-clustered t inference. This handles the unbalanced sample without incorrectly applying rectangular two-way demeaning. Income subsets and first differences are exploratory sensitivity analyses.'),
        code("for key, model in r['models'].items():\n    print(model['label'], 'countries:', model['n_countries'], 'rows:', model['n_obs'])\n    display(pd.DataFrame(model['coefficients']))"),
        md('## Diagnostics and sensitivity\n\nLower/upper outcome limits are marginal quantiles rather than joint posterior draws. Replacing outcomes with these limits does not propagate full estimation uncertainty. VIF and influence checks diagnose instability without resolving confounding.'),
        code("display(pd.DataFrame(r['vif']))\ndisplay(pd.DataFrame([r['diagnostics']]))\ndisplay(Image(filename=str(root / 'docs/images/fig5_uncertainty_forest_plot.png')))\ndisplay(Image(filename=str(root / 'docs/images/fig8_model_diagnostics.png')))"),
        md('## Reproduction and interpretation\n\nRun `python src/run_pipeline.py` from the repository root to refit the models and regenerate all outputs, then `python -m pytest -q`. Add `--integrate` to rebuild the master from cached raw files. WDI revisions can change the snapshot.\n\nCurrent health expenditure does not isolate government priority. National fertility does not measure individual parity or birth spacing. Selection excludes several conflict-affected countries. A defensible CRVS-quality subset and full posterior uncertainty propagation remain open tasks.\n\nSources: [WHO 2025](https://www.who.int/publications/i/item/9789240108462), [WDI](https://databank.worldbank.org/source/world-development-indicators), and the repository methods/source register. AI tools assisted implementation and review.')]
    nb.metadata=dict(kernelspec=dict(display_name='Python 3',language='python',name='python3'),language_info=dict(name='python',version='3.12'))
    NotebookClient(nb,timeout=180,kernel_name='python3',resources={'metadata':{'path':str(root/'notebooks')}}).execute()
    nbformat.write(nb,root/'notebooks/maternal_mortality_analysis.ipynb')
    print('Generated and executed notebook')


if __name__=='__main__':
    create_notebook(Path(__file__).resolve().parents[1])
