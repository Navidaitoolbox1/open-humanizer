"""Small local web interface. No dependencies and no network calls."""
from __future__ import annotations

import html
import json
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path
from urllib.parse import parse_qs

from .engine import analyze_text, load_rules

ROOT = Path(__file__).parents[1]
RULES = load_rules(ROOT / "rules" / "writing_rules.json")

PAGE = """<!doctype html><html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>Open Humanizer</title><style>body{font:16px system-ui;max-width:980px;margin:40px auto;padding:0 20px;color:#202124}textarea{width:100%;min-height:280px;padding:14px;font:16px system-ui}button{padding:10px 16px;margin:12px 0;background:#185abc;color:#fff;border:0;border-radius:4px}pre{white-space:pre-wrap;background:#f5f6f7;padding:14px}.finding{border-left:4px solid #d93025;padding:8px 12px;margin:8px 0;background:#fff4f2}.muted{color:#5f6368}</style></head><body><h1>Open Humanizer</h1><p class="muted">Local editorial quality checker. Your text stays on this machine. This is not an AI detector.</p><form method="post"><textarea name="text" placeholder="Paste English text here...">{text}</textarea><br><button type="submit">Check writing</button></form>{result}</body></html>"""


def render_result(report: dict) -> str:
    s = report["summary"]
    out = [f"<h2>{html.escape(s['status'].title())} · score {s['editorial_score']}/100</h2>", f"<p>Findings: {s['finding_count']} · high {s['severity_counts']['high']} · medium {s['severity_counts']['medium']} · low {s['severity_counts']['low']}</p>"]
    for f in report["findings"]:
        out.append(f"<div class='finding'><b>Line {f['line']} · {html.escape(f['label'])}</b><br>Matched: <code>{html.escape(f['match'])}</code><br>{html.escape(f['suggestion'])}</div>")
    return "".join(out)


class Handler(BaseHTTPRequestHandler):
    def _send(self, body: str) -> None:
        data = body.encode("utf-8")
        self.send_response(200)
        self.send_header("Content-Type", "text/html; charset=utf-8")
        self.send_header("Content-Length", str(len(data)))
        self.end_headers()
        self.wfile.write(data)

    def do_GET(self) -> None:
        self._send(PAGE.format(text="", result=""))

    def do_POST(self) -> None:
        length = int(self.headers.get("Content-Length", "0"))
        text = parse_qs(self.rfile.read(length).decode("utf-8")).get("text", [""])[0]
        report = analyze_text(text, RULES)
        self._send(PAGE.format(text=html.escape(text), result=render_result(report)))

    def log_message(self, *_args) -> None:
        return


def main() -> None:
    server = ThreadingHTTPServer(("127.0.0.1", 8788), Handler)
    print("Open Humanizer running at http://127.0.0.1:8788")
    server.serve_forever()


if __name__ == "__main__":
    main()
