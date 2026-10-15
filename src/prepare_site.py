"""Assemble the public static site after checking input and audit freshness."""
from pathlib import Path
import shutil
from research_io import load_results


def prepare_site(base_dir):
    root=Path(base_dir)
    load_results(root)
    target=root/'_site'
    target.mkdir(exist_ok=True)
    for name in ['dashboard','reports','docs']:
        shutil.copytree(root/name,target/name,dirs_exist_ok=True)
    (target/'index.html').write_text('<!doctype html><html lang="en"><meta charset="utf-8"><meta http-equiv="refresh" content="0;url=dashboard/"><title>Maternal mortality dashboard</title><a href="dashboard/">Open the research dashboard</a></html>',encoding='utf-8')
    (target/'.nojekyll').touch()
    print('Prepared audited static site in _site/')


if __name__=='__main__':
    prepare_site(Path(__file__).resolve().parents[1])
