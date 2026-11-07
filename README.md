# example-app

Beispielanwendung des Testbeds zur Masterarbeit *Sicherheit in Software Supply Chains*: eine kleine „Hallo Welt“-Webseite, die anzeigt, welcher Stand gerade läuft (Variante, Commit, Build-Zeit, Version des internen Pakets, Pod und Node).

| Pfad | Inhalt |
|---|---|
| `app/` | Webserver (nur Python-Standardbibliothek) |
| `packages/` | interne und „öffentliche“ Paketquelle, siehe [packages/README.md](packages/README.md) |
| `k8s/` | Kubernetes-Manifeste |
| `.github/workflows/` | ein Workflow je Toolchain-Variante (`v0.yml` bis `v3.yml`) |

Jeder Push auf `main` baut die Anwendung in allen Varianten. Die Images liegen unter `ghcr.io/lma-hh-01/example-app-<variante>`.

Aufbau, Bedienung und Szenarien beschreibt das Repository [testbed](https://github.com/lma-hh-01/testbed).
