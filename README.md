# Notebook Comment Translator

Translate **markdown cells** and **Python `#` comments** in Jupyter notebooks, while leaving all code intact.  
This is useful for bilingual education, collaboration, or sharing analysis across English/Spanish audiences without breaking code execution.

---

## Quickstart

1. Install requirements:
   ```bash
   pip install -r requirements.txt
2. Translate a notebook from **English to Spanish**
    ```bash
      python cli.py my_notebook.ipynb --direction en->es
3. Translate a notebook from **Spanish to English**
    ```bash
        python cli.py my_notebook.ipynb --direction es->es
## Features

- Translate Markdown cells  
- Translate Python `#` comments  
- Works both directions (English ↔ Spanish)  
- Leaves code untouched  
- Simple CLI  