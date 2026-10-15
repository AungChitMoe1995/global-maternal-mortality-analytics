"""Keep PowerPoint numeric caches identical to the embedded worksheet cells.

python-pptx and its workbook writer can serialize a binary float with different
decimal precision. Refresh caches from the actual workbook XML after saving so
opening or editing the workbook cannot subtly change the plotted values.
"""
from io import BytesIO
from pathlib import Path
import posixpath
import zipfile
from lxml import etree
from openpyxl.utils.cell import range_boundaries, get_column_letter

C='http://schemas.openxmlformats.org/drawingml/2006/chart'
S='http://schemas.openxmlformats.org/spreadsheetml/2006/main'
R='http://schemas.openxmlformats.org/officeDocument/2006/relationships'
P='http://schemas.openxmlformats.org/package/2006/relationships'


def sync_numeric_caches(path):
    path=Path(path)
    content=BytesIO()
    with zipfile.ZipFile(path) as package, zipfile.ZipFile(content,'w',zipfile.ZIP_DEFLATED) as target:
        for info in package.infolist():
            raw=package.read(info.filename)
            if info.filename.startswith('ppt/charts/chart') and info.filename.endswith('.xml'):
                chart=etree.fromstring(raw)
                external=chart.find(f'{{{C}}}externalData')
                if external is not None:
                    relpath=posixpath.join(posixpath.dirname(info.filename),'_rels',posixpath.basename(info.filename)+'.rels')
                    relationships=etree.fromstring(package.read(relpath))
                    rid=external.get(f'{{{R}}}id')
                    rel=next(x for x in relationships if x.get('Id')==rid)
                    workbook_path=posixpath.normpath(posixpath.join(posixpath.dirname(info.filename),rel.get('Target')))
                    with zipfile.ZipFile(BytesIO(package.read(workbook_path))) as workbook:
                        book=etree.fromstring(workbook.read('xl/workbook.xml'))
                        book_rels=etree.fromstring(workbook.read('xl/_rels/workbook.xml.rels'))
                        sheets={}
                        for sheet in book.findall(f'{{{S}}}sheets/{{{S}}}sheet'):
                            relation=next(x for x in book_rels if x.get('Id')==sheet.get(f'{{{R}}}id'))
                            file=relation.get('Target')
                            file=file.lstrip('/') if file.startswith('/') else posixpath.normpath(posixpath.join('xl',file))
                            xml=etree.fromstring(workbook.read(file))
                            sheets[sheet.get('name')]={cell.get('r'):cell.findtext(f'{{{S}}}v') for cell in xml.findall(f'.//{{{S}}}c')}
                        for ref in chart.findall(f'.//{{{C}}}numRef'):
                            formula=ref.findtext(f'{{{C}}}f')
                            sheet_name, cell_range=formula.rsplit('!',1)
                            cells=sheets[sheet_name.strip("'")]
                            c1,r1,c2,r2=range_boundaries(cell_range)
                            values=[cells[f'{get_column_letter(c)}{r}'] for r in range(r1,r2+1) for c in range(c1,c2+1)]
                            cache=ref.find(f'{{{C}}}numCache')
                            if cache is None:
                                raise ValueError('Expected an embedded numeric cache')
                            points=cache.findall(f'{{{C}}}pt')
                            if len(points)!=len(values):
                                raise ValueError('Worksheet range and chart cache lengths differ')
                            for point in points:
                                point.find(f'{{{C}}}v').text=values[int(point.get('idx'))]
                    raw=etree.tostring(chart,xml_declaration=True,encoding='UTF-8',standalone=True)
            target.writestr(info,raw)
    path.write_bytes(content.getvalue())
