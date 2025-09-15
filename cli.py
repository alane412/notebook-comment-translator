import argparse
from core import translate_notebook, default_out_path

def main():
    ap = argparse.ArgumentParser(description="Translate markdown cells and Python # comments in a Jupyter notebook.")
    ap.add_argument("notebook", help="Path to .ipynb")
    ap.add_argument("--direction", choices=["en->es", "es->en"], default="en->es")
    ap.add_argument("--no-md", action="store_true", help="Do not translate markdown cells")
    ap.add_argument("--no-comments", action="store_true", help="Do not translate code comments")
    ap.add_argument("-o", "--out", help="Output .ipynb path (defaults to adding .es/.en before extension)")
    args = ap.parse_args()

    out = args.out or default_out_path(args.notebook, args.direction)
    translate_notebook(
        in_path=args.notebook,
        out_path=out,
        direction=args.direction,
        translate_markdown=not args.no_md,
        translate_comments=not args.no_comments
    )
    print(f"Wrote: {out}")

if __name__ == "__main__":
    main()
