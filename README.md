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

## Commit-Signaturen (ab Variante V1)

Ab V1 baut und signiert die Pipeline nur, wenn jeder neue Commit auf `main` entweder

- von einer erlaubten Person mit [gitsign](https://github.com/sigstore/gitsign) signiert ist (Anmeldung über GitHub im Browser) oder
- ein Merge-Commit ist, den GitHub beim Zusammenführen eines Pull Requests erzeugt und selbst signiert.

Änderungen kommen deshalb über Pull Requests auf `main`, zusammengeführt als Merge-Commit. Squash und Rebase sind abgeschaltet, weil dabei die Signaturen verloren gehen. Die Prüfung und die Liste der erlaubten Personen liegen im zentralen Workflow in [secure-workflows](https://github.com/lma-hh-01/secure-workflows), nicht in diesem Repository.

gitsign für dieses Repository einrichten:

```sh
git config --local gpg.format x509
git config --local gpg.x509.program gitsign
git config --local commit.gpgsign true
git config --local gitsign.connectorID https://github.com/login/oauth
```
