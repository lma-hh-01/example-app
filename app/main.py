"""Beispielanwendung des Testbeds.

Zeigt an, welcher Stand gerade laeuft. Die Build-Angaben sind beim Bauen fest ins
Image geschrieben, die Laufzeit-Angaben kommen aus Kubernetes. Weichen beide
voneinander ab, ist das ein Hinweis darauf, dass ein anderes Image laeuft als
gedacht.
"""

import html
import os
import platform
from http.server import BaseHTTPRequestHandler, HTTPServer

import firma_utils

PORT = 8080


def collect_info():
    return {
        "Im Image eingebaut": {
            "Variante": os.environ.get("APP_VARIANT", "unbekannt"),
            "Commit": os.environ.get("APP_COMMIT", "unbekannt"),
            "Build-Zeit": os.environ.get("APP_BUILD_TIME", "unbekannt"),
            "firma-utils": f"{firma_utils.__version__} ({firma_utils.SOURCE})",
        },
        "Zur Laufzeit": {
            "Deployte Image-Referenz": os.environ.get("DEPLOYED_IMAGE", "unbekannt"),
            "Pod": os.environ.get("POD_NAME", "unbekannt"),
            "Namespace": os.environ.get("POD_NAMESPACE", "unbekannt"),
            "Node": os.environ.get("NODE_NAME", "unbekannt"),
            "CPU-Architektur": platform.machine(),
        },
    }


def render_page(info):
    sections = []
    for title, rows in info.items():
        cells = "".join(
            f"<tr><th>{html.escape(key)}</th><td>{html.escape(value)}</td></tr>"
            for key, value in rows.items()
        )
        sections.append(f"<h2>{html.escape(title)}</h2><table>{cells}</table>")

    return f"""<!DOCTYPE html>
<html lang="de">
<head>
<meta charset="utf-8">
<title>Example App</title>
<style>
  body {{ font-family: sans-serif; margin: 2rem; }}
  th {{ text-align: left; padding-right: 2rem; }}
  td {{ font-family: monospace; }}
</style>
</head>
<body>
<h1>Hallo Welt</h1>
{"".join(sections)}
</body>
</html>
"""


class Handler(BaseHTTPRequestHandler):
    def do_GET(self):
        if self.path == "/healthz":
            self.respond(200, "text/plain", "ok")
        elif self.path == "/":
            self.respond(200, "text/html; charset=utf-8", render_page(collect_info()))
        else:
            self.respond(404, "text/plain", "nicht gefunden")

    def respond(self, status, content_type, body):
        data = body.encode("utf-8")
        self.send_response(status)
        self.send_header("Content-Type", content_type)
        self.send_header("Content-Length", str(len(data)))
        self.end_headers()
        self.wfile.write(data)


if __name__ == "__main__":
    print(f"Example App lauscht auf Port {PORT}", flush=True)
    HTTPServer(("", PORT), Handler).serve_forever()
