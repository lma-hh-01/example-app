"""Example application of the testbed.

Shows which version is currently running. The build details are baked into the
image at build time, the runtime details come from Kubernetes. If the two
differ, this indicates that a different image is running than intended.
"""

import html
import os
import platform
from http.server import BaseHTTPRequestHandler, HTTPServer

import company_utils

PORT = 8080


def collect_info():
    return {
        "Built into the image": {
            "Variant": os.environ.get("APP_VARIANT", "unknown"),
            "Commit": os.environ.get("APP_COMMIT", "unknown"),
            "Build time": os.environ.get("APP_BUILD_TIME", "unknown"),
            "company-utils": f"{company_utils.__version__} ({company_utils.SOURCE})",
        },
        "At runtime": {
            "Deployed image reference": os.environ.get("DEPLOYED_IMAGE", "unknown"),
            "Pod": os.environ.get("POD_NAME", "unknown"),
            "Namespace": os.environ.get("POD_NAMESPACE", "unknown"),
            "Node": os.environ.get("NODE_NAME", "unknown"),
            "CPU architecture": platform.machine(),
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
<html lang="en">
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
<h1>Hello World</h1>
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
            self.respond(404, "text/plain", "not found")

    def respond(self, status, content_type, body):
        data = body.encode("utf-8")
        self.send_response(status)
        self.send_header("Content-Type", content_type)
        self.send_header("Content-Length", str(len(data)))
        self.end_headers()
        self.wfile.write(data)


if __name__ == "__main__":
    print(f"Example App listening on port {PORT}", flush=True)
    HTTPServer(("", PORT), Handler).serve_forever()
