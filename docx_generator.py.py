from docx import Document

def generate_docx(metadata: dict, output_path: str):
    doc = Document()
    doc.add_heading(metadata.get("title", "Ч"), level=1)
    doc.add_paragraph(f'јвторы: {metadata.get("authors", "Ч")}')
    doc.add_paragraph(f'∆урнал: {metadata.get("journal", "Ч")} ({metadata.get("issued", "Ч")})')
    doc.add_paragraph(f'“ом: {metadata.get("volume", "Ч")}  є{metadata.get("issue", "Ч")} стр. {metadata.get("pages", "Ч")}')

    doc.add_heading("јннотаци€", level=2)
    doc.add_paragraph(metadata.get("abstract", "Ч"))

    doc.add_heading("¬ыводы", level=2)
    doc.add_paragraph(metadata.get("conclusion", "Ч"))

    doc.add_heading("ѕредложени€", level=2)
    doc.add_paragraph(metadata.get("suggestions", "Ч"))

    doc.save(output_path)
