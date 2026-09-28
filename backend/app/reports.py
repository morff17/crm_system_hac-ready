import io, json, os
import xlwt
from openpyxl import Workbook
from reportlab.pdfgen import canvas
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.lib.pagesizes import A4, landscape
from reportlab.lib.units import mm

COLUMNS = [
    ("institution", "ВУЗ"), ("direction", "ИТ-направление"), ("product", "ИТ-продукт"),
    ("status", "Статус"), ("manager", "Ответственный"), ("contract", "Договор"),
    ("students", "Студенты"), ("streams", "Потоки"), ("applications", "Заявки")
]

def _all_rows(interactions):
    for x in interactions:
        yield {
            "institution": x.institution.name,
            "direction": x.direction.name if x.direction else "",
            "product": x.product.name if x.product else "",
            "status": x.status,
            "manager": x.institution.manager.full_name if x.institution.manager else "",
            "contract": x.institution.contract_number or "",
            "students": x.students_count, "streams": x.streams_count, "applications": x.applications_count,
        }

def _shape(interactions, columns=None):
    selected = [c for c in COLUMNS if not columns or c[0] in columns]
    if not selected: selected = COLUMNS
    headers = [x[1] for x in selected]
    rows = [[row[key] for key, _ in selected] for row in _all_rows(interactions)]
    return selected, headers, rows

def build_xlsx(interactions, columns=None):
    _, headers, rows = _shape(interactions, columns)
    wb = Workbook(); ws = wb.active; ws.title = "CRM report"; ws.append(headers)
    for row in rows: ws.append(row)
    for col in ws.columns: ws.column_dimensions[col[0].column_letter].width = min(max(len(str(c.value or "")) for c in col) + 2, 45)
    bio = io.BytesIO(); wb.save(bio); bio.seek(0); return bio

def build_xls(interactions, columns=None):
    _, headers, rows = _shape(interactions, columns)
    wb = xlwt.Workbook(); ws = wb.add_sheet("CRM report")
    for c, h in enumerate(headers): ws.write(0, c, h)
    for r, row in enumerate(rows, 1):
        for c, v in enumerate(row): ws.write(r, c, v)
    bio = io.BytesIO(); wb.save(bio); bio.seek(0); return bio

def build_pdf(interactions, columns=None):
    _, headers, rows = _shape(interactions, columns)
    bio = io.BytesIO(); font = "Helvetica"
    for path in ["/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf", "/usr/share/fonts/dejavu/DejaVuSans.ttf"]:
        if os.path.exists(path): pdfmetrics.registerFont(TTFont("DejaVu", path)); font = "DejaVu"; break
    c = canvas.Canvas(bio, pagesize=landscape(A4)); width, height = landscape(A4)
    c.setFont(font, 13); c.drawString(12*mm, height-14*mm, "CRM: отчёт по взаимодействиям")
    y = height - 24*mm; c.setFont(font, 6.5)
    usable = 273 / max(len(headers), 1); xs = [12 + i*usable for i in range(len(headers))]
    for x, h in zip(xs, headers): c.drawString(x*mm, y, h[:24])
    y -= 7*mm
    for row in rows:
        if y < 12*mm: c.showPage(); c.setFont(font, 6.5); y = height - 15*mm
        for x, v in zip(xs, row): c.drawString(x*mm, y, str(v)[:26])
        y -= 5.5*mm
    c.save(); bio.seek(0); return bio

def build_json(interactions, columns=None):
    _, headers, rows = _shape(interactions, columns)
    data = [dict(zip(headers, row)) for row in rows]
    return io.BytesIO(json.dumps(data, ensure_ascii=False, indent=2).encode("utf-8"))
