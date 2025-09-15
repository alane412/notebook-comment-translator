import re
from pathlib import Path
import nbformat as nbf
from transformers import AutoTokenizer, AutoModelForSeq2SeqLM, pipeline

# translation models (English<->Spanish)
EN_ES = "Helsinki-NLP/opus-mt-en-es"
ES_EN = "Helsinki-NLP/opus-mt-es-en"

def load_translator(direction: str):
    model_name = EN_ES if direction == "en->es" else ES_EN
    tok = AutoTokenizer.from_pretrained(model_name)
    mod = AutoModelForSeq2SeqLM.from_pretrained(model_name)
    return pipeline("translation", model=mod, tokenizer=tok, max_length=1024)

def _chunk(text: str, max_len: int = 900):
    """Chunker to avoid truncation limits."""
    out, buf, total = [], [], 0
    for line in text.splitlines(keepends=True):
        if total + len(line) > max_len:
            out.append("".join(buf))
            buf, total = [], 0
        buf.append(line); total += len(line)
    if buf:
        out.append("".join(buf))
    return out

def translate_text(text: str, translator) -> str:
    if not text.strip():
        return text
    pieces = _chunk(text)
    translated = [translator(p)[0]["translation_text"] for p in pieces]
    return "".join(translated)

COMMENT_RE = re.compile(r'^(\s*#\s?)(.*)$')  # group(1)=prefix "# ", group(2)=text

def translate_markdown_cell(md_source: str, translator) -> str:
    return translate_text(md_source, translator)

def translate_code_comments(code_source: str, translator) -> str:
    """Translate Python comment lines."""
    out_lines = []
    for line in code_source.splitlines(keepends=False):
        m = COMMENT_RE.match(line)
        if m:
            prefix, text = m.groups()
            out_lines.append(f"{prefix}{translate_text(text, translator)}")
        else:
            out_lines.append(line)
    # preserve trailing newline if exists
    return "\n".join(out_lines) + ("\n" if code_source.endswith("\n") else "")

def translate_notebook(in_path: str, out_path: str, direction: str = "en->es",
                       translate_markdown: bool = True,
                       translate_comments: bool = True):
    nb = nbf.read(in_path, as_version=4)
    translator = load_translator(direction)

    for cell in nb.cells:
        if cell.cell_type == "markdown" and translate_markdown:
            cell.source = translate_markdown_cell(cell.source, translator)
        elif cell.cell_type == "code" and translate_comments:
            cell.source = translate_code_comments(cell.source, translator)

    nbf.write(nb, out_path)
    return out_path

def default_out_path(in_path: str, direction: str) -> str:
    p = Path(in_path)
    suffix = ".es" if direction == "en->es" else ".en"
    return str(p.with_name(p.stem + suffix + p.suffix))

if __name__ == "__main__":
    raise SystemExit("Run this tool via cli.py.")
