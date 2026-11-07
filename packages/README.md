# Paketquellen

Die Anwendung bezieht ihre Python-Pakete aus zwei Paketindizes, die beide in diesem Verzeichnis liegen:

| Verzeichnis | steht für | Inhalt |
|---|---|---|
| `public/` | eine öffentliche Registry wie PyPI | im Normalfall leer |
| `internal/` | die interne Registry der Firma | `firma-utils` 1.0.0 |

Beide liegen im Repository, weil die gehosteten GitHub-Runner keine lokale Registry erreichen und Angriffe gegen echte öffentliche Registries nicht erlaubt sind. Im Dependency-Confusion-Szenario legt der „Angreifer“ ein gleichnamiges Paket mit höherer Version in `public/`.

`src/firma-utils/` enthält den Quellcode des internen Pakets. Nach einer Änderung baut `./build-internal-index.sh` den internen Index neu.
