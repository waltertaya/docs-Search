import os
import datetime
from rich.console import Console
from whoosh.index import create_in
from whoosh.fields import Schema, TEXT, ID, DATETIME, KEYWORD

from file_extractors import extract_text_from_docx, extract_text_from_pdf, extract_text_from_txt

console = Console()


def build_index(folder, index_dir="indexdir"):
    if not os.path.exists(index_dir):
        os.mkdir(index_dir)

    schema = Schema(
        title=ID(stored=True),
        content=TEXT(stored=True),
        modified=DATETIME(stored=True),
        filetype=KEYWORD(stored=True)
    )
    ix = create_in(index_dir, schema)

    writer = ix.writer()
    for file in os.listdir(folder):
        path = os.path.join(folder, file)
        text = ""
        filetype = file.split(".")[-1].lower()

        if file.endswith(".pdf"):
            text = extract_text_from_pdf(path)
        elif file.endswith(".docx"):
            text = extract_text_from_docx(path)
        elif file.endswith(".txt"):
            text = extract_text_from_txt(path)

        if text.strip():
            mod_time = datetime.datetime.fromtimestamp(os.path.getmtime(path))
            writer.add_document(title=file, content=text, modified=mod_time, filetype=filetype)
            console.print(f"[green]Indexed:[/green] {file} ({filetype}, modified {mod_time.date()})")

    writer.commit()
