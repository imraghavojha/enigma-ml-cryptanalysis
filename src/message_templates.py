"""
German military message templates and vocabulary for Enigma dataset generation.
"""

# Naval and military ranks
NAVAL_RANKS = [
    "Großadmiral", "Admiral", "Vizeadmiral", "Konteradmiral", 
    "Flottillenadmiral", "Kapitän zur See", "Fregattenkapitän", "Korvettenkapitän"
]

NON_COMMISSIONED_RANKS = [
    "Bootsmannmaat", "Oberbootsmann", "Hauptbootsmann", "Signalmaat", 
    "Signalobermaat", "Zimmermannsmaat", "Artilleriemechanikermaat", "Torpedomechanikermaat"
]

# Military units and organizations
MILITARY_UNITS = [
    "Kriegsmarine", "Wehrmacht", "Oberkommando der Marine", "OKM", 
    "Luftwaffe", "Abwehr", "Abteilung", "U-Bootwaffe", "Flottenkommando"
]

# Message structure components
ADDRESSING = ["AN", "VON", "BETR"]

PRIORITY_INDICATORS = ["SEHR DRINGEND", "DRINGEND", "SOFORT"]

TIME_FORMATS = ["UHR", "STUNDEN", "MINUTEN"]

# Common message openings
MESSAGE_OPENINGS = [
    "AN BEFEHLSHABER", "AN GRUPPE", "VON KOMMANDO", "FUNKSPRUCH", "GEHEIME KOMMANDOSACHE"
]

# Naval communication terms
SIGNAL_SYSTEMS = ["Signalbuch", "Wetterkurzschlüssel", "WKS", "Kurzsignale"]

COMMUNICATION_TERMS = [
    "Funkspruch", "Verzifferung", "Funkpeilung", "Einleitungszeichen", 
    "Antennenkreis", "Antennenleistung"
]

# Submarine operations vocabulary
SUBMARINE_TERMS = [
    "U-Boot", "Periskop", "Aufgetaucht", "Getaucht", "Sehrohr", 
    "Batterien in Reihen geschaltet", "Abgeschossen", "Tiefe", "Oberwasserzieloptik"
]

# Navigation terms
NAVIGATION_TERMS = [
    "Kurs", "Quadrat", "Standort", "Abschnitt", "Abdrift", 
    "Abdriftwinkel", "Aufmarsch"
]

# Weather reporting terminology
WEATHER_TERMS = [
    "Wetterbericht", "Temperatur", "Sicht", "Wolkenhoehe", 
    "Windstaerke", "Nebelgebiet", "Frontensystem"
]

# Combat and tactical terms
COMBAT_TERMS = [
    "Geleitzug", "Konvoi", "Feindsichtung", "Handelschiff", "Kreuzer", 
    "Angriff", "Versenkung", "Adlerangriff", "Abteilungsnachrichtenstaffel"
]

# Commands and orders
COMMAND_TERMS = [
    "Befehl", "Anweisung", "Abtreten", "Abweisen", "Absetzung", 
    "Aufgabe", "Aufklarung"
]

# Alert and status terms
ALERT_TERMS = [
    "Gefechtsbereit", "Alarmstart", "Abtransport", "Abwehrzone", "Anflugrichtung"
]

# Naval vessels and equipment
VESSELS = [
    "Schnellboot", "Hilfskreuzer", "Zerstörer", "Schlachtschiff", 
    "Panzerschiff", "Unterseeboot", "Minensucher", "Torpedoboot", 
    "Flugzeugträger", "Kreuzer", "Flakschiff", "Vorpostenboot"
]

# Action verbs
ACTION_VERBS = [
    "abschießen", "versenken", "angreifen", "beschädigen", "aufklären", 
    "treffen", "abwerfen", "auslaufen", "einlaufen", "melden", 
    "beobachten", "funken"
]

# Positions and coordinates
POSITIONS = [
    "Quadrat", "Breitengrad", "Längengrad", "Position", "Standort", 
    "Sektor", "Abschnitt", "Operationsgebiet", "Marinequadrat"
]

# Grid square examples (historical Kriegsmarine grid system)
GRID_SQUARES = [
    "AJ47", "BF13", "CK89", "AL88", "AM63", "BC10",
    "BD20", "CX33", "DJ56", "FG77", "HI22", "JK45"
]

# Time expressions
TIME_EXPRESSIONS = [
    "Uhr", "Stunden", "Minuten", "sofort", "unverzüglich", 
    "baldmöglichst", "bei Tagesanbruch", "bei Einbruch der Dunkelheit"
]

# Message templates patterns
WEATHER_REPORT_TEMPLATE = "WETTERKURZSIGNAL QUADRAT {grid} {time}UHR {temp}GRAD {visibility}KM {wind_dir} {wind_strength} {pressure} {phenomenon}"

POSITION_REPORT_TEMPLATE = "STANDORT QUADRAT {grid} {time}UHR KURS {course} GESCHWINDIGKEIT {speed}"

ENEMY_SIGHTING_TEMPLATE = "FEINDSICHTUNG {vessel_type} {number} {location} {time}UHR KURS {course} GESCHWINDIGKEIT {speed}"