

#### 👷‍♀️⚠️ Work in Progress ⚠️ 👷‍♀️


## Dokumentation quenfo_py
***
Die Software **quenfo_py** bietet verschiedene Funktionen zur Verarbeitung von Stellenanzeigen an.
Diese unterteilen sich in die Klassifikation von Stellenanzeigen, in die Informationsextraktion von Kompetenzen und Tools und in Matching-Workflows zum Auffinden bereits bekannter Entitäten innerhalb klassifizierter Paragrafen.
In dieser Dokumentation werden die jeweiligen Workflows beschrieben. Dabei werden die einzelnen Schritte und die genutzten Klassen und Methoden aufgeführt. 
Jede ausführbare Applikation arbeitet mit Object Relational Mapping (ORM). Objekte werden hierbei als Datenbankeinträge persistiert, d.h. in den Datenklassen (z.B. in den Klassen ClassifyUnits, ExtractedEntity, InformationEntity oder ExtractionUnit) werden entsprechende Annotationen an Klassenattributen vorgenommen, um diese als vorzunehmenden Eintrag zu kennzeichnen. Für die Realisierung wurde [SQLAlchemy](https://docs.sqlalchemy.org/en/14/orm/) genutzt. 

Die Software entstand im Projekt [Quenfo](https://dh.phil-fak.uni-koeln.de/forschung/qualifikationsentwicklungsforschung) 
und in Kooperation mit dem Bundesinstitut für Berufsbildung.


**Zielsetzung:**

	a. Stellenanzeigen werden in Paragraphen aufgesplittet und klassifiziert.
Mögliche Klassen: 
1. Selbstvorstellung des ausschreibenden Unternehmens
2. Beschreibung der Tätigkeit, Angebote an die Bewerberinnen und Bewerber
3. Anforderungen an die Bewerberin bzw. den Bewerber 
4. Formalia und Sonstiges
5. 1&3
6. 2&3

   
	b. Informationsextraktion von Kompetenzen und Tools aus klassifizierten Paragraphen
	c. Matching-Workflows zum Auffinden bereits bekannter Entitäten innerhalb klassifizierter Paragrafen.

**Input:**

	1. Trainingsdaten (SQL-Datenbank mit bereits klassifizierten Stellenanzeigen)
	2. Input-Daten (SQL-Datenbank mit Stellenanzeigen)

**Hauptstruktur:**

	1. Classification
	2. Information Extraction
	3. Matching

**Output:** SQL-Datenbank bestehend aus:

	1.  SQL-Tabelle mit klassifizierten Paragraphen
	2.
	3.

***
### Quickstart🏃
***
Die Anwendung wurde in Python 3.7 geschrieben.

Klone das Repository

`git clone https://github.com/agerlac1/quenfo_py.git`

cd in den Ordner **quenfo_py/code**: hier liegt die requirements Datei und das Programm wird von hier ausgeführt (working dir)

`python -m pip install -r requirements.txt`

Mit der nachfolgenden Ausführung wird das gesamte Programm samt Default-Settings aufgerufen (Pfade zu Testdaten und Trainingsdaten müssen zuvor in der config.yaml angegeben werden).

`python main.py --input_path "path_to_input_data" --db_mode {overwrite,append}`

Informationen über die erfolgten Abläufe und Ergebnisse werden in dem Modul `/logger` in den entsprechenden logging-Dateien gespeichert.

***
### Workflow🔁
***
Hier kommt der Workflow hin

#### Allgemein

Hier kommt der allgemeine Workflow hin

#### Aufteilung Classification, IE und Matching

Das sind die drei Steps

und hier bitte das Workflow bild einbinden

<img src=""/>


#### Code Struktur
Der Code ist so struktuiert, dass sich die einzelnen Module (im Workflow s.o. erkennbar) ebenfalls in der Ordnerstruktur wiederfinden.
```
📦quenfo_py
 ┣ 📂additional_scripts
 ┣ 📂code
 ┃ ┣ 📂classification
 ┃ ┃ ┣ 📂predict_classes
 ┃ ┃ ┃ ┣ 📜knn_predictor.py
 ┃ ┃ ┃ ┣ 📜regex_predictor.py
 ┃ ┃ ┃ ┣ 📜result_merger.py
 ┃ ┃ ┃ ┗ 📜__init__.py
 ┃ ┃ ┣ 📂prepare_classifyunits
 ┃ ┃ ┃ ┣ 📂classify_units
 ┃ ┃ ┃ ┃ ┣ 📜convert_classifyunits.py
 ┃ ┃ ┃ ┃ ┗ 📜__init__.py
 ┃ ┃ ┃ ┣ 📂feature_units
 ┃ ┃ ┃ ┃ ┣ 📜convert_featureunits.py
 ┃ ┃ ┃ ┃ ┗ 📜__init__.py
 ┃ ┃ ┃ ┣ 📂feature_vectors
 ┃ ┃ ┃ ┃ ┣ 📜convert_featurevectors.py
 ┃ ┃ ┃ ┃ ┗ 📜__init__.py
 ┃ ┃ ┃ ┗ 📜__init__.py
 ┃ ┃ ┗ 📜__init__.py
 ┃ ┣ 📂configuration
 ┃ ┃ ┣ 📜config.yaml
 ┃ ┃ ┣ 📜config_model.py
 ┃ ┃ ┗ 📜__init__.py
 ┃ ┣ 📂database
 ┃ ┃ ┣ 📜connection.py
 ┃ ┃ ┗ 📜__init__.py
 ┃ ┣ 📂information_extraction
 ┃ ┃ ┣ 📂prepare_extractionunits
 ┃ ┃ ┃ ┣ 📂extraction_units
 ┃ ┃ ┃ ┃ ┣ 📜convert_extractionunits.py
 ┃ ┃ ┃ ┃ ┗ 📜__init__.py
 ┃ ┃ ┃ ┗ 📜__init__.py
 ┃ ┃ ┣ 📂prepare_resources
 ┃ ┃ ┃ ┣ 📜connection_resources.py
 ┃ ┃ ┃ ┣ 📜convert_entities.py
 ┃ ┃ ┃ ┗ 📜__init__.py
 ┃ ┃ ┣ 📜helper.py
 ┃ ┃ ┣ 📜models.py
 ┃ ┃ ┗ 📜__init__.py
 ┃ ┣ 📂logger
 ┃ ┣ 📂orm_handling
 ┃ ┃ ┣ 📜models.py
 ┃ ┃ ┣ 📜orm.py
 ┃ ┃ ┗ 📜__init__.py
 ┃ ┣ 📂tests
 ┃ ┣ 📂training
 ┃ ┃ ┣ 📂knnclassifier
 ┃ ┃ ┃ ┣ 📜gen_knn.py
 ┃ ┃ ┃ ┗ 📜__init__.py
 ┃ ┃ ┣ 📂regexclassifier
 ┃ ┃ ┃ ┣ 📜gen_regex.py
 ┃ ┃ ┃ ┗ 📜__init__.py
 ┃ ┃ ┣ 📂tfidfvectorizer
 ┃ ┃ ┃ ┣ 📜gen_vectorizer.py
 ┃ ┃ ┃ ┗ 📜__init__.py
 ┃ ┃ ┣ 📜helper.py
 ┃ ┃ ┣ 📜train_models.py
 ┃ ┃ ┗ 📜__init__.py
 ┃ ┣ 📜main.py
 ┃ ┗ 📜requirements.txt
 ┣ 📂docs
 ┣ 📜.gitignore
 ┗ 📜README.md
```

***
### Implementierung und Module 🛠️
***
#### orm_handling

#### database
1. `connection.py`: Script mit dem die connections zu den SQL-Datenbanken hergestellt werden (Input, Output und Backup-Dateien).

#### tests

#### classification




**main.py**

Main-Skript des Tools. Hier befindet sich die grobe Architektur und Verwaltung des Programms. Des Weiteren sind hier die ArgumentParser Befehle deklariert, mit denen bestimmte Teile des Skriptes aufgerufen werden können (mehr dazu weiter unten).

**requirements**

Enthält eine Auflistung an Python-Dependencies, die benötigt werden, um das Tool auszuführen.

**logger**

Logging-File, in dem zusätzliche Informationen während der Ausführung des Tools gespeichert werden. Außerdem befinden sich hier die Evaluation-Reports und Sanity_checks.

**input/, output/, temp/**

Ordner, in denen die Input, Output und Temp-Dateien liegen. Wenn andere Pfade für die Dateien verwendet werden sollen, müssen diese in der config.yaml Datei angepasst werden.

***
### Configuration📋✔️
***
In der Datei config.yaml sind alle Pfade, einstellbare Parameter und der Metadaten-Filter vermerkt. Dadurch wird gewährleistet, dass im Code selbst für eine Anwendung nichts verändert werden muss. Alle Änderungen werden in der `config.yaml` Datei vorgenommen.

**Im aktuellen Zustand befindet sich das Programm in der "Werkseinstellung" und es können nach Belieben Modelle trainiert und Daten analysiert werden (mit entsprechenden Pfadangaben zu Test- und Trainingsdaten).**

Ansonsten können folgende Werte angepasst werden:

1. Andere **Input-Dateien** auswählen:

	- `train_data` und `test_data`

2. Andere **Output-Datei** auswählen:

	- `output_path`

3. Andere **Temp-Dateien** und Pfade festlegen für Dateien, die schon unique_ids bekommen haben:

	- `id_train_data` und `id_test_data`

4. Auswählen, ob für den Prozess ein **trained** oder **retrained Doc2Vec Modell** verwendet wird (nur relevant, wenn Doc2Vec verwendet wird):

	- `d2v_model_type` -> `type` 

	entweder 'd2v_model' für trained Modell oder 'd2v_remodel' für retrained Modell.


***
### CommandLine - Befehle📢
***
Alle Befehle werden relativ zum Ordner `code/` ausgeführt.

**Grundsätzlich:** 

    usage: main.py [-h] [--classification] [--extraction] [--matching]
               [--input_path INPUT_PATH] [--db_mode {overwrite,append}]

    classify jobads and extract/match information

    optional arguments:
    -h, --help            show this help message and exit
    --classification
    --extraction
    --matching
    --input_path INPUT_PATH
    --db_mode {overwrite,append}



***
### Input Daten📚
***
Als Input-Dateien müssen SQL-Datenbanken vorliegen. Die Benennung der darin verzeichneten Tabellen ist irrelevant. Die Daten müssen mindestens über folgende Metadaten verfügen, damit sie als Input-Daten verwendet werden können (egal ob als Test- oder Trainingsdaten):

- full_text

- location_name

- date

- profession_isco_code

- advertiser_name
