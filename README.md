# DLBDSOOFPP01_D - Kurs Objektorientierte und funktionale Programmierung mit Python

## Übersicht

Dieses Projekt stellt ein **Dashboard** zur Verfügung, mit dem Studenten des Studiengangs "Angewandte Künstliche Intelligenz" ihre Modulbuchungen verwalten und ihren Fortschritt überwachen können. Das Dashboard zeigt:
1. Einen **Fortschrittsbalken**, der den Anteil der erreichten ECTS-Punkte im Studium anzeigt.
2. Ein **Tortendiagramm**, das die Anzahl der Prüfungsversuche für jedes Modul visualisiert.

## Voraussetzungen

Damit das Dashboard funktioniert, müssen folgende Voraussetzungen erfüllt sein:
- **Python 3.x** muss auf deinem System installiert sein. Falls Python nicht vorhanden ist, wird es automatisch installiert.
- Die Python-Pakete `dash`, `plotly` und `pandas` müssen installiert sein. Dies wird von der `.bat` Datei automatisch erledigt.

## Installation und Ausführung

Folge diesen Schritten, um das Dashboard auszuführen:

1. **Lade das Projekt herunter** oder **klone es aus deinem Repository**.
2. Stelle sicher, dass alle Dateien sich im gleichen Verzeichnis befinden.
3. Doppelklicke auf die Datei `start_dashboard.bat`.

### Was passiert beim Ausführen der `.bat` Datei?

- Die `.bat` Datei überprüft, ob Python auf deinem System installiert ist. Falls Python nicht installiert ist, wird es automatisch heruntergeladen und installiert.
- Nach der Installation von Python werden die benötigten Pakete (`dash`, `plotly`, `pandas`) installiert.
- Anschließend wird das Dashboard (`Dashboard_Code.py`) gestartet, und du kannst das Dashboard in deinem Browser aufrufen.

## CSV-Dateien

Die folgenden CSV-Dateien sind erforderlich, um die Daten des Dashboards zu laden und zu speichern:
- `Student.csv`: Enthält die Matrikelnummern und Namen der Studenten.
- `Module.csv`: Enthält die verfügbaren Module und ihre zugehörigen ECTS-Punkte.
- `Buchungen.csv`: Speichert die Modulbuchungen der Studenten, inklusive der Versuche und des Prüfungsstatus.

Stelle sicher, dass sich diese Dateien im gleichen Verzeichnis wie `Dashboard_Code.py` befinden.

## Probleme

Falls es zu Problemen kommt:
- Vergewissere dich, dass Python korrekt installiert wurde.
- Stelle sicher, dass die CSV-Dateien korrekt formatiert und vorhanden sind.
- Überprüfe die Konsolenausgabe (das Fenster bleibt nach dem Start offen), um eventuelle Fehler oder Hinweise zu sehen.

Viel Spass beim Testen!
Maria Auer
