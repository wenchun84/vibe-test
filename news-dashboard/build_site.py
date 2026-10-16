#!/usr/bin/env python3
"""Build the static site: site shell + dashboard page -> OUT_DIR/index.html."""
import pathlib, sys

here = pathlib.Path(__file__).parent
out = pathlib.Path(sys.argv[1] if len(sys.argv) > 1 else "_site")
out.mkdir(parents=True, exist_ok=True)
shell = (here / "site" / "shell.html").read_text(encoding="utf-8")
page = (here / "index.html").read_text(encoding="utf-8")
(out / "index.html").write_text(shell.replace("<!--PAGE-->", page), encoding="utf-8")
print(f"wrote {out / 'index.html'}")
