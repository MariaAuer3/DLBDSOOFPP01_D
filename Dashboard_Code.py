##########################
# DASHBOARD FÜR STUDENTEN
##########################

# Das Dashboard soll für Studenten des Studiengangs "Angewandte Künstliche Intelligenz" der IU sein.
# Ziel ist es, dass neue Modulbuchungen abgespeichert werden können und zwei Ziele eines Studenten verfolgt
# werden kann.
# Zum einen sieht man links einen Fortschrittsbalken - wie weit der Student im Studium ist.
# Zum anderen wird rechts ein Tortendiagramm dargestellt, welches anzeigt wie viele Versuche ein Student
# für das erfolgreiche Ablegen von Modulen benötigt hat.


from dash import dcc, html
import pandas as pd
import dash
from dash.dependencies import Input, Output, State
import plotly.graph_objs as go
import os


#_____________________________________________________________________
# DomainLayer
#_____________________________________________________________________


# Domain-Klassen
class Student:
    def __init__(self, matrikelnummer, name):
        self.matrikelnummer = matrikelnummer
        self.name = name

class Modul:
    def __init__(self, modul_id, name, ects):
        self.modul_id = modul_id
        self.name = name
        self.ects = ects

class ModulBuchung:
    def __init__(self, buchungs_id, student, modul, status, versuche, erreichte_etcs_pro_modul):
        self.buchungs_id = buchungs_id
        self.student = student
        self.modul = modul
        self.status = status
        self.versuche = versuche
        self.erreichte_etcs_pro_modul = erreichte_etcs_pro_modul



        



#_____________________________________________________________________
# RespositoryLayer
#_____________________________________________________________________

# Pfade zu den CSV-Dateien
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
STUDENT_CSV_PATH = os.path.join(BASE_DIR, 'Student.csv')
MODUL_CSV_PATH = os.path.join(BASE_DIR, 'Module.csv')
BUCHUNGEN_CSV_PATH = os.path.join(BASE_DIR, 'Buchungen.csv')

#STUDENT_CSV_PATH = r'C:\Users\maria\Documents\allgemein 05.06.2024\Dokuments\Studium\Künstliche Intelligenz\OOP Python\Phase 2\OOProgramming\Student.csv'
#MODUL_CSV_PATH = r'C:\Users\maria\Documents\allgemein 05.06.2024\Dokuments\Studium\Künstliche Intelligenz\OOP Python\Phase 2\OOProgramming\Module.csv'
#BUCHUNGEN_CSV_PATH = r'C:\Users\maria\Documents\allgemein 05.06.2024\Dokuments\Studium\Künstliche Intelligenz\OOP Python\Phase 2\OOProgramming\Buchungen.csv'


# Repository-Klassen
class StudentRepository:
    def __init__(self, csv_file):
        self.csv_file = csv_file

    def find_by_matrikelnummer(self, matrikelnummer):
        df = pd.read_csv(self.csv_file, encoding='latin1', sep=';')
        student_data = df[df['matrikelnummer'] == matrikelnummer].iloc[0]
        return Student(student_data['matrikelnummer'], student_data['name'])

class ModulRepository:
    def __init__(self, csv_file):
        self.csv_file = csv_file

    def find_all(self):
        df = pd.read_csv(self.csv_file, encoding='latin1', sep=';')
        return [Modul(row['modul_id'], row['name'], row['etcs']) for _, row in df.iterrows()]

    def find_by_name(self, name):
        df = pd.read_csv(self.csv_file, encoding='latin1', sep=';')
        modul_data = df[df['name'] == name].iloc[0]
        return Modul(modul_data['modul_id'], modul_data['name'], modul_data['etcs'])

class ModulBuchungRepository:
    def __init__(self, csv_file, modul_repo):
        self.csv_file = csv_file
        self.modul_repo = modul_repo

    def save_buchung(self, matrikelnummer, modulname, status, versuche):
        print(f"save_buchung aufgerufen: Matrikelnummer={matrikelnummer}, Modulname={modulname}, Status={status}, Versuche={versuche}")
        try:
            # Lese die bestehende CSV-Datei
            df = pd.read_csv(self.csv_file, encoding='latin1', sep=';')
         
            # Finde das entsprechende Modul
            modul = self.modul_repo.find_by_name(modulname)
            buchungs_id = f"{matrikelnummer}-{modul.modul_id}"

            # Prüfen, ob die Kombination bereits existiert
            if not df[(df['buchung_matrikelnr'] == matrikelnummer) & (df['modulkennung'] == modul.modul_id)].empty:
                print(f"Kombination Matrikelnummer={matrikelnummer} und Modulkennung={modul.modul_id} existiert bereits.")
                return False

            # Neue Buchung als DataFrame erstellen
            neue_buchung = pd.DataFrame([{
                'buchungs_id': buchungs_id,
                'buchung_matrikelnr': matrikelnummer,
                'modulkennung': modul.modul_id,
                'pruefungsstatus': status,
                'versuche': versuche,
                'erreichte_etcs_pro_modul': modul.ects if status else 0
            }])

            # Füge die neue Buchung hinzu
            df = pd.concat([df, neue_buchung], ignore_index=True)

            # Speichern in der CSV-Datei
            df.to_csv(self.csv_file, index=False, encoding='latin1', sep=';')
            print("Neue Buchung erfolgreich in die CSV gespeichert.")
            return True

        except Exception as e:
            print(f"Fehler beim Speichern der Buchung: {e}")
            return False




    def find_by_student(self, student):
        df = pd.read_csv(self.csv_file, encoding='latin1', sep=';')
        modul_dict = {modul.modul_id: modul for modul in self.modul_repo.find_all()}
        buchungen = []
        
        for _, row in df[df['buchung_matrikelnr'] == student.matrikelnummer].iterrows():
            modul = modul_dict.get(row['modulkennung'])
            if modul is not None:
                buchung = ModulBuchung(
                    row['buchungs_id'],
                    student,
                    modul,
                    row['pruefungsstatus'],
                    row['versuche'],
                    row['erreichte_etcs_pro_modul']
                )
                buchungen.append(buchung)
            else:
                print(f"Modul mit ID {row['modulkennung']} nicht gefunden für Matrikelnummer {student.matrikelnummer}.")
        
        return buchungen





# Initialisiere die Repositories mit den entsprechenden CSV-Dateien
student_repo = StudentRepository(STUDENT_CSV_PATH)
modul_repo = ModulRepository(MODUL_CSV_PATH)
buchung_repo = ModulBuchungRepository(BUCHUNGEN_CSV_PATH, modul_repo)





#_____________________________________________________________________
# ApplicationLayer
#_____________________________________________________________________


# Variablen:
# ETCs Anzahl welche man insgesamt im Studium erreichen kann
gesamt_etcs = 180

# wurde ursprünglich erstellt, nun aber durch andereweise ausgeführt
        # Funktion zur Erstellung und Speicherung der buchungs_id
        #def buchungs_id_erstellen_und_speichern():
            # Lese die CSV-Datei
        #   df = pd.read_csv(BUCHUNGEN_CSV_PATH, encoding='latin1', sep=';')
        #  # Iteriere durch die Zeilen, um buchungs_id für diejenigen zu erstellen, die noch keine haben
        # for index, row in df.iterrows():
            #    if pd.isna(row['buchungs_id']) and not pd.isna(row['buchung_matrikelnr']) and not pd.isna(row['modulkennung']):
            #       buchungs_id = f"{row['buchung_matrikelnr']}-{row['modulkennung']}"
            #      # Speichere die buchungs_id in der entsprechenden Zeile
            #     df.at[index, 'buchungs_id'] = buchungs_id
            # Speichere die geänderte CSV-Datei
            #df.to_csv(BUCHUNGEN_CSV_PATH, index=False, encoding='latin1', sep=';')

# wurde ursprünglich erstellt, nun aber durch andereweise ausgeführt
        # Anzahl ETCs erreicht in einem Modul
        # Funktion zur Überprüfung und Aktualisierung der ETCS basierend auf dem pruefungsstatus
        #def etcs_pro_modul_aktualisieren():
            # Lese die CSV-Datei
        #   df = pd.read_csv(BUCHUNGEN_CSV_PATH, encoding='latin1', sep=';')
            # Iteriere durch die Zeilen der CSV-Datei
        #  for index, row in df.iterrows():
                # Überprüfe, ob die Spalte erreichte_etcs_pro_modul leer ist oder den Wert 0 hat
        #     if pd.isna(row['erreichte_etcs_pro_modul']) or row['erreichte_etcs_pro_modul'] == 0:
                    # Lade das entsprechende Modul für diese Zeile
            #        modul = next((m for m in modul_repo.find_all() if m.modul_id == row['modulkennung']), None)
            #       if modul:
                        # Überprüfe den pruefungsstatus (flexibler Check)
            #          if str(row['pruefungsstatus']).lower() in ["true", "1", "yes"]:
                            # Setze die ETCS-Punkte für das Modul
            #             df.at[index, 'erreichte_etcs_pro_modul'] = modul.ects
                #        else:
                            # Setze die ETCS-Punkte auf 0
                #           df.at[index, 'erreichte_etcs_pro_modul'] = 0
            # Speichere die geänderte CSV-Datei
            #df.to_csv(BUCHUNGEN_CSV_PATH, index=False, encoding='latin1', sep=';')



# Berechne insgesamt erreichte ETCs als Studienfortschritt
def studienfortschritt_etcs(ausgewählte_matrikelnummer):
    # Lade den Studenten basierend auf der ausgewählten Matrikelnummer
    student = student_repo.find_by_matrikelnummer(ausgewählte_matrikelnummer)
    # Lade die Modulbuchungen des Studenten
    buchungen = buchung_repo.find_by_student(student)
    # Initialisiere eine Variable für die erreichten ECTS-Punkte
    erreichte_etcs = 0
    # Durchlaufe die Buchungen und summiere die ECTS-Punkte
    for buchung in buchungen:
        erreichte_etcs += buchung.modul.ects
    # Rückgabe der insgesamt erreichten ECTS-Punkte
    return erreichte_etcs



# Berechne die prozentuale erreichte ECTS als Studienfortschritt
def prozent_etcs_berechnen(ausgewählte_matrikelnummer, gesamt_etcs):
    # Erhalte die erreichten ECTS-Punkte
    erreichte_etcs = studienfortschritt_etcs(ausgewählte_matrikelnummer)
    # Berechne den Prozentsatz der erreichten ECTS im Verhältnis zu den Gesamt-ECTS
    prozent_etcs = round((erreichte_etcs * 100) / gesamt_etcs)
    # Rückgabe des Prozentsatzes
    return prozent_etcs



# Berechne die Verteilung von Erst-, Zweit- und Drittversuche
def student_versuche(ausgewählte_matrikelnummer):
    # Lade den Studenten basierend auf der ausgewählten Matrikelnummer
    student = student_repo.find_by_matrikelnummer(ausgewählte_matrikelnummer)
    # Lade die Modulbuchungen des Studenten
    buchungen = buchung_repo.find_by_student(student)
    # Initialisiere Zählvariablen für die Anzahl der Modulbuchungen mit 1, 2 und 3 Versuchen
    erstversuch = 0
    zweitversuch = 0
    drittversuch = 0
    # Durchlaufe die Buchungen und zähle die Versuche
    for buchung in buchungen:
        if buchung.versuche == 1:
            erstversuch += 1
        elif buchung.versuche == 2:
            zweitversuch += 1
        elif buchung.versuche == 3:
            drittversuch += 1
    
    # Rückgabe der Ergebnisse als Dictionary
    return {
        "erstversuch": erstversuch,
        "zweitversuch": zweitversuch,
        "drittversuch": drittversuch
    }






#_____________________________________________________________________
# PresentationLayer
#_____________________________________________________________________

# Initialisiere die Dash-App
app = dash.Dash(__name__)

# Layout der App
app.layout = html.Div([
    html.H1("Student Dashboard"),

    # Modul buchen Bereich
    html.Div([
        html.H2("Modul buchen", style={'marginBottom': '20px'}),
        # Eingabefelder für Matrikelnummer, Modulname, Prüfungsstatus und Versuche
        html.Div([
            html.Div([
                html.Label("Student", style={'fontWeight': 'bold', 'display': 'block', 'marginBottom': '5px'}),
                dcc.Dropdown(
                     id='dropdown-studentenname-buchen',
                     options=[
                        {'label': student_repo.find_by_matrikelnummer(matrikelnummer).name, 'value': matrikelnummer}
                        for matrikelnummer in pd.read_csv(STUDENT_CSV_PATH, encoding='latin1', sep=';')['matrikelnummer']
                ],
                placeholder='Student auswählen',
                style={
                    'width': '100%', 
                    'padding': '10px', 
                    'marginBottom': '10px',
                    'borderRadius': '5px',
                    'border': '1px solid #ccc',
                    'boxShadow': 'inset 0 1px 3px rgba(0, 0, 0, 0.1)'
                }
            ),
            ], style={'marginBottom': '10px'}),
            html.Div([
                html.Label("Modulname", style={'fontWeight': 'bold', 'display': 'block', 'marginBottom': '5px'}),
                dcc.Dropdown(
                    id='input-modulname',
                    options=[{'label': modul.name, 'value': modul.name} for modul in modul_repo.find_all()],
                    placeholder='Modulname auswählen',
                    style={
                        'width': '100%', 
                        'padding': '10px', 
                        'marginBottom': '10px',
                        'borderRadius': '5px',
                        'border': '1px solid #ccc',
                        'boxShadow': 'inset 0 1px 3px rgba(0, 0, 0, 0.1)'
                    }
                ),
            ], style={'marginBottom': '10px'}),
            html.Div([
                html.Label("Prüfungsstatus", style={'fontWeight': 'bold', 'display': 'block', 'marginBottom': '5px'}),
                dcc.Checklist(
                    id='input-pruefungsstatus',
                    options=[
                        {'label': 'Prüfung bestanden', 'value': 'status'}
                    ],
                    value=[],
                    style={'padding': '10px', 'marginBottom': '10px'}
                ),
            ], style={'marginBottom': '10px'}),
            html.Div([
                html.Label("Versuche", style={'fontWeight': 'bold', 'display': 'block', 'marginBottom': '5px'}),
                dcc.Dropdown(
                    id='input-versuche',
                    options=[
                        {'label': str(i), 'value': i} for i in range(4)
                    ],
                    placeholder='Versuche',
                    style={
                        'width': '100%', 
                        'padding': '10px', 
                        'marginBottom': '20px',
                        'borderRadius': '5px',
                        'border': '1px solid #ccc',
                        'boxShadow': 'inset 0 1px 3px rgba(0, 0, 0, 0.1)'
                    }
                ),
            ], style={'marginBottom': '20px'}),
            html.Button('Speichern', id='button-speichern', style={
                'width': '100%', 
                'padding': '10px', 
                'backgroundColor': '#007bff', 
                'color': 'white', 
                'border': 'none', 
                'borderRadius': '5px', 
                'cursor': 'pointer',
                'fontWeight': 'bold'
            }),
            html.Div(id='output-message', style={'marginTop': '20px', 'color': 'green', 'fontWeight': 'bold'})
        ], style={
            'padding': '20px', 
            'border': '1px solid #ddd', 
            'borderRadius': '5px', 
            'backgroundColor': '#f9f9f9',
            'boxShadow': '0 2px 4px rgba(0, 0, 0, 0.1)'
        })
    ], style={'width': '48%', 'display': 'inline-block', 'verticalAlign': 'top', 'marginBottom': '40px'}),


    # Auswahlbereich für Studenten
    html.Div([
        html.H2("Wählen Sie einen Studenten aus!", style={'textAlign': 'left', 'marginBottom': '20px'}),
        dcc.Dropdown(
            id='dropdown-studentenname',
            options=[
                {'label': student_repo.find_by_matrikelnummer(matrikelnummer).name, 'value': matrikelnummer}
                for matrikelnummer in pd.read_csv(STUDENT_CSV_PATH, encoding='latin1', sep=';')['matrikelnummer']
            ],
            placeholder='Student',
            style={
                'width': '100%', 
                'padding': '10px', 
                'borderRadius': '5px',
                'border': '1px solid #ccc',
                'boxShadow': 'inset 0 1px 3px rgba(0, 0, 0, 0.1)'
            }
        )
    ], style={
        'width': '40%',  # Breite der Box
        'display': 'inline-block',
        'verticalAlign': 'top',
        'marginLeft': '5%',  # Abstand zur linken Seite
        'marginBottom': '40px'
    }),


    
    # Fortschrittsbalken (links unten)
    html.Div([
        #html.H3("Studienfortschritt"),
        dcc.Graph(id='fortschrittsbalken'),
        html.Div(id='prozent-anzeige', style={'textAlign': 'center', 'marginTop': '10px', 'fontSize': '20px'})
    ], style={'width': '48%', 'display': 'inline-block', 'verticalAlign': 'top', 'paddingTop': '20px'}),  # Padding hinzugefügt

    # Tortendiagramm für Versuche (rechts)
    html.Div([
        #html.H3("Verteilung der Versuche"),  # Überschrift hinzugefügt
        dcc.Graph(id='versuche-torte')
    ], style={'width': '48%', 'display': 'inline-block', 'verticalAlign': 'top', 'paddingTop': '20px'})  # Padding hinzugefügt


])




@app.callback(
    Output('output-message', 'children'),
    [Input('button-speichern', 'n_clicks')],
    [State('dropdown-studentenname-buchen', 'value'),
     State('input-modulname', 'value'),
     State('input-pruefungsstatus', 'value'),
     State('input-versuche', 'value')]
)
def save_buchung(n_clicks, matrikelnummer, modulname, pruefungsstatus, versuche):
    if n_clicks is None:
        print("Speichern-Button wurde noch nicht geklickt.")
        return ""
   
    if not matrikelnummer or not modulname or versuche is None:
        return "Bitte füllen Sie alle Felder aus."
    
    status = bool(pruefungsstatus) and 'status' in pruefungsstatus
    versuche = int(versuche)  # Konvertiere den Wert zu einer Ganzzahl
    success = buchung_repo.save_buchung(matrikelnummer, modulname, status, int(versuche))

    if success:
        print("Buchung erfolgreich gespeichert.")
        return "Buchung erfolgreich gespeichert."
    else:
        print("Fehler: Buchung konnte nicht gespeichert werden.")
        return "Fehler: Buchung konnte nicht gespeichert werden."


# Callback für den Fortschrittsbalken und Prozentanzeige
@app.callback(
    [Output('fortschrittsbalken', 'figure'), Output('prozent-anzeige', 'children')],
    [Input('dropdown-studentenname', 'value')]
)
def update_fortschritt_und_prozent(ausgewählte_matrikelnummer):
    if not ausgewählte_matrikelnummer:
        return go.Figure(), ""

    # Berechnung der Fortschrittsbalken-Daten
    erreichte_etcs = studienfortschritt_etcs(ausgewählte_matrikelnummer)
    gesamt_etcs = 180  # Gesamtanzahl der ETCS
    prozent_etcs = prozent_etcs_berechnen(ausgewählte_matrikelnummer, gesamt_etcs)
    anzahl_kaestchen = gesamt_etcs // 5
    ausgefuellte_kaestchen = erreichte_etcs // 5

    # Erstellung des Fortschrittsbalkens
    fig = go.Figure(go.Bar(
        x=[ausgefuellte_kaestchen, anzahl_kaestchen - ausgefuellte_kaestchen],
        y=[''],
        orientation='h',
        marker=dict(color=['green', 'lightgray']),
        text=[f"{ausgefuellte_kaestchen*5} / {gesamt_etcs} ECTS"],
        textposition='auto',
        width=0.3  # Höhe des Balkens angepasst
    ))

    fig.update_layout(
    xaxis=dict(
        range=[0, anzahl_kaestchen], 
        showgrid=False,
        tickvals=list(range(0, anzahl_kaestchen + 1, 6)),  # Schritte von 30 ECTS
        ticktext=[str(i*30) for i in range(7)]  # Labels entsprechend anpassen
    ),
    yaxis=dict(showticklabels=False),
    title='Studienfortschritt in ECTS (je 5 ECTS pro Kästchen)',
    showlegend=False,
    bargap=0
)

    # Rückgabe des Fortschrittsbalkens und der Prozentanzeige
    return fig, f"{prozent_etcs} % des Studiums abgeschlossen"


# Callback für das Tortendiagramm
@app.callback(
    Output('versuche-torte', 'figure'),
    [Input('dropdown-studentenname', 'value')]
)
def update_versuche_torte(ausgewählte_matrikelnummer):
    if not ausgewählte_matrikelnummer:
        return go.Figure()

    # Daten für die Versuche
    versuche = student_versuche(ausgewählte_matrikelnummer)
    
    # Erstellung des Tortendiagramms
    fig = go.Figure(go.Pie(
        labels=['Erstversuch', 'Zweitversuch', 'Drittversuch'],
        values=[versuche['erstversuch'], versuche['zweitversuch'], versuche['drittversuch']],
        hole=0.3,
        textinfo='value'  # Ändere das textinfo-Attribut
    ))
    fig.update_layout(
        title='Verteilung der Versuche'
    )
    return fig


# Starte die Dash-App
if __name__ == '__main__':
    app.run_server(debug=True)