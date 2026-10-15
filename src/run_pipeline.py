"""Rebuild the audited research snapshot and all presentation artifacts."""
from pathlib import Path
import argparse
import os
import subprocess
import sys


def main():
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--integrate',action='store_true',help='Rebuild the master from existing cached raw files first')
    args=parser.parse_args()
    root=Path(__file__).resolve().parents[1]
    env=os.environ.copy()
    env.update(OPENBLAS_NUM_THREADS='1',OMP_NUM_THREADS='1',MKL_NUM_THREADS='1',PYTHONIOENCODING='utf-8')
    scripts=(['integrate_data.py'] if args.integrate else [])+[
        'data_quality.py','analysis.py','write_research_docs.py','generate_dashboard_data.py',
        'create_presentation.py','create_notebook.py']
    for script in scripts:
        print('Running',script,flush=True)
        subprocess.run([sys.executable,'-u',str(root/'src'/script)],cwd=root,env=env,check=True)


if __name__=='__main__':
    main()
