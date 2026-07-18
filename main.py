import re
import os
import sys
import shutil
import json
from pyvis.network import Network

# Importation des constantes de l'interface utilisateur (sans l'import inutilisé HTML_TEMPLATE)
from templates import ECRAN_CHARGEMENT, PANEL_SELECTION, PANEL_RECHERCHE, JS_INJECTION

# ==============================================================================
# CONFIGURATION DES DOSSIERS
# ==============================================================================
DOSSIER_DUMP = "dump_compteurs"
DOSSIER_SORTIE = "cartographies_generees"

path_master = os.path.join(DOSSIER_DUMP, "_gtgtpcpt.d")
path_compt = os.path.join(DOSSIER_DUMP, "_gtcompt.d")
path_formule = os.path.join(DOSSIER_DUMP, "_formule.d")

# Capture du focus depuis le terminal (ex: .\run DCAH)
COMPTEUR_FOCUS = None
if len(sys.argv) > 1:
    COMPTEUR_FOCUS = sys.argv[1].strip().upper()

# 1. Lecture de la liste Master des compteurs
valid_codes = set()
try:
    with open(path_master, 'r', encoding='cp1252', errors='ignore') as f:
        for line in f:
            matches = re.findall(r'"([^"\\]*(?:\\.[^"\\]*)*)"', line)
            if len(matches) >= 2:
                code = matches[1].strip()
                if len(code) > 1:
                    valid_codes.add(code)
except FileNotFoundError:
    print(f"❌ Erreur : Fichier master introuvable : {path_master}")
    exit(1)

if COMPTEUR_FOCUS and COMPTEUR_FOCUS not in valid_codes:
    print(f"❌ Erreur : Le compteur '{COMPTEUR_FOCUS}' n'existe pas dans le paramétrage.")
    exit(1)

def parse_progress_line(line):
    """
    Analyse une ligne de dump Progress (.d) pour extraire proprement tous les champs,
    qu'ils soient entourés de guillemets (avec caractères échappés) ou bruts.
    """
    pattern = r'"([^"\\]*(?:\\.[^"\\]*)*)"|([^\s]+)'
    fields = []
    for match in re.finditer(pattern, line):
        quoted, unquoted = match.groups()
        if quoted is not None:
            fields.append(quoted)
        else:
            fields.append(unquoted)
    return fields

# 2. Lecture du dictionnaire et des attributs de configuration depuis _gtcompt.d
compteurs_info = {}
try:
    with open(path_compt, 'r', encoding='cp1252', errors='ignore') as f:
        for line in f:
            line_str = line.strip()
            if not line_str:
                continue
            
            # Découpage rigoureux de la ligne Progress
            fields = parse_progress_line(line_str)
            if len(fields) > 0:
                code = fields[0].strip()
                if code in valid_codes:
                    nom = fields[1].strip() if len(fields) > 1 else code
                    actif_bool = (fields[2].strip().lower() == "yes") if len(fields) > 2 else True
                    
                    # Extraction du droit (Index 83)
                    droit_id = ""
                    if len(fields) > 83:
                        val_83 = fields[83].strip()
                        if val_83 and val_83 != "?" and val_83 != '""':
                            droit_id = val_83
                    
                    # Extraction de la rubrique de paie (Index 15)
                    rubrique_paie = ""
                    if len(fields) > 15:
                        val_15 = fields[15].strip()
                        if val_15 and val_15 != "?" and val_15 != '""':
                            rubrique_paie = val_15

                    compteurs_info[code] = {
                        "nom": nom,
                        "actif": actif_bool,
                        "droit": droit_id,
                        "rubrique_paie": rubrique_paie
                    }
except FileNotFoundError:
    print(f"❌ Erreur : Fichier des caractéristiques introuvable : {path_compt}")
    exit(1)

# Remplissage par défaut pour les codes master manquants
for code in valid_codes:
    if code not in compteurs_info:
        compteurs_info[code] = {
            "nom": code,
            "actif": True,
            "droit": "",
            "rubrique_paie": ""
        }

# 3. Analyse des formules et liaisons de dépendances (_formule.d)
all_edges = set()
try:
    with open(path_formule, 'r', encoding='cp1252', errors='ignore') as f:
        for line in f:
            matches = re.findall(r'"([^"\\]*(?:\\.[^"\\]*)*)"', line)
            if not matches:
                continue
            parent_code = matches[0].strip()
            if parent_code not in valid_codes:
                continue
            for element in matches[1:]:
                # Extraction des jetons de formule
                tokens = re.split(r'[\s\+\-\*\/\(\)\,\=\<\>\!]+', element)
                for token in tokens:
                    child_code = token.strip()
                    if child_code in valid_codes and child_code != parent_code:
                        all_edges.add((parent_code, child_code))
except FileNotFoundError:
    print(f"❌ Erreur : Fichier des formules introuvable : {path_formule}")
    exit(1)

# 4. Traitement du Filtrage (Focus ou Global)
nodes_to_keep = set()
edges_to_keep = set()

if COMPTEUR_FOCUS:
    print(f"🔍 [FOCUS] Filtrage récursif autour de : {COMPTEUR_FOCUS}")
    nodes_to_keep.add(COMPTEUR_FOCUS)
    changement = True
    while changement:
        taille_initiale = len(nodes_to_keep)
        for source, target in all_edges:
            if source in nodes_to_keep:
                nodes_to_keep.add(target)
                edges_to_keep.add((source, target))
            if target in nodes_to_keep:
                nodes_to_keep.add(source)
                edges_to_keep.add((source, target))
        changement = len(nodes_to_keep) > taille_initiale
    filtered_compteurs = {code: compteurs_info[code] for code in nodes_to_keep}
    filtered_edges = edges_to_keep
    nom_fichier = f"carte_du_compteur_{COMPTEUR_FOCUS}.html"
else:
    print("🌐 [GLOBAL] Extraction complète de tous les compteurs liés.")
    filtered_compteurs = compteurs_info
    filtered_edges = all_edges
    nom_fichier = "carte_globale_des_compteurs.html"

# 5. Construction du Graphe (PyVis)
net = Network(height="100vh", width="100%", directed=True, bgcolor="#ffffff", font_color="#000000")

# Algorithme physique d'organisation
net.barnes_hut()

# Ajout des Nœuds avec le typage visuel et fonctionnel de la charte Chronos
for code, info in filtered_compteurs.items():
    label_visuel = f" {code} " 
    infobulle = f"Code : {code}\nNom  : {info['nom']}"
    
    # Ajout dynamique des informations d'infobulle
    if info['droit']:
        infobulle += f"\nDroit : {info['droit']}"
    if info['rubrique_paie']:
        infobulle += f"\nRubrique Paie : {info['rubrique_paie']}"
        
    # Choix stratégique de la couleur du nœud
    if not info["actif"]:
        # Gris (Désactivé)
        couleur_fond = "#F5F5F5"
        couleur_bordure = "#9E9E9E"
        epaisseur_bordure = 1
    elif code == COMPTEUR_FOCUS:
        # Rouge Corail/Cerise (Focus au démarrage) - Inspiré de la bulle de notification Chronos
        couleur_fond = "#FFCDD2"
        couleur_bordure = "#C62828"
        epaisseur_bordure = 3
    elif info["rubrique_paie"]:
        # Orange Abricot / Ambre (Terminaux d'export paie) - Couleur chaude de l'interface
        couleur_fond = "#FFF3E0"
        couleur_bordure = "#FB8C00"
        epaisseur_bordure = 2
    elif info["droit"]:
        # Bleu Periwinkle / Indigo (Alimentation directe d'un droit) - Tons froids doux
        couleur_fond = "#E8EAF6"
        couleur_bordure = "#3F51B5"
        epaisseur_bordure = 2
    else:
        # Turquoise Pastel (Classique / Intermédiaire)
        couleur_fond = "#E0F2F1"
        couleur_bordure = "#00A896"
        epaisseur_bordure = 1
        
    net.add_node(
        code, 
        label=label_visuel, 
        title=infobulle, 
        shape="box", 
        borderWidth=epaisseur_bordure,
        color={
            "background": couleur_fond,
            "border": couleur_bordure,
            "highlight": {
                # Rouge Corail/Cerise de l'interface Chronos pour le clic/focus dynamique
                "background": "#FFCDD2",
                "border": "#C62828"
            }
        },
        font={
            'size': 14, 
            'face': 'Courier', 
            'color': '#1A3263', 
            'bold': True        
        }
    )

# Ajout des Liens de dépendance
for source, target in filtered_edges:
    net.add_edge(source, target, color="#848484", arrows="to")

# Configuration de la physique visuelle et des interactions
net.set_options("""
var options = {
  "physics": {
    "barnesHut": {
      "gravitationalConstant": -15000,
      "centralGravity": 0.1,
      "springLength": 180,
      "springConstant": 0.05,
      "damping": 0.9,
      "avoidOverlap": 1
    },
    "stabilization": {
      "enabled": true,
      "iterations": 1000,
      "fit": true
    }
  },
  "interaction": {
    "hover": true,
    "selectable": true,
    "selectConnectedEdges": true,
    "dragNodes": true,
    "dragView": true,
    "multiselect": true
  }
}
""")

# Sauvegarde propre du fichier HTML de base
net.save_graph(nom_fichier)

# 6. Préparation de la base de recherche locale pour l'autocomplétion
search_data = []
for code, info in filtered_compteurs.items():
    search_data.append({
        "code": code,
        "nom": info["nom"],
        "actif": info["actif"],
        "rubrique_paie": info.get("rubrique_paie", ""),
        "droit": info.get("droit", "")
    })

js_search_database = f"const searchDatabase = {json.dumps(search_data, ensure_ascii=False)};"

# 7. Injection HTML/CSS/JS pour finaliser l'interface premium
try:
    with open(nom_fichier, 'r', encoding='utf-8') as file:
        html_content = file.read()
    
    # Injection de la base de recherche locale et de l'écran d'attente
    html_content = html_content.replace('<body>', f'<body>\n{ECRAN_CHARGEMENT}')
    
    # Injection des panneaux de commande (Recherche & Sélection & Légende)
    panneaux_et_styles = PANEL_SELECTION + "\n" + PANEL_RECHERCHE
    html_content = html_content.replace('</body>', f'{panneaux_et_styles}\n</body>')
    
    # Remplacement des scripts pour injecter nos comportements interactifs
    ancien_draw = "drawGraph();"
    nouveau_draw = f"""
    {js_search_database}
    drawGraph();
    {JS_INJECTION}
    """
    html_content = html_content.replace(ancien_draw, nouveau_draw)
    
    with open(nom_fichier, 'w', encoding='utf-8') as file:
        file.write(html_content)

except Exception as e:
    print(f"⚠️ Note : Impossible d'injecter l'interface utilisateur enrichie ({e})")

# 8. Déplacement du fichier finalisé vers le dossier de destination
path_destination = os.path.join(DOSSIER_SORTIE, nom_fichier)
try:
    if not os.path.exists(DOSSIER_SORTIE):
        os.makedirs(DOSSIER_SORTIE)
    if os.path.exists(path_destination):
        os.remove(path_destination)
    shutil.move(nom_fichier, path_destination)
    print(f"🎉 Terminé ! La cartographie interactive est disponible ici : '{path_destination}'")
except Exception as e:
    print(f"⚠️ Impossible de ranger le fichier dans {DOSSIER_SORTIE} (Erreur: {e})")