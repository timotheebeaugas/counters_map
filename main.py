import re
import os
import sys
import shutil
from pyvis.network import Network

# Importation des éléments HTML, CSS et JS déportés dans templates.py
from templates import ECRAN_CHARGEMENT, PANEL_SELECTION, JS_INJECTION

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

# 1. Lecture de la liste Master
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
    print(f"❌ Erreur : Le compteur '{COMPTEUR_FOCUS}' n'existe pas.")
    exit(1)

# 2. Lecture du dictionnaire des noms et des statuts (actif/inactif)
compteur_infos = {}
try:
    with open(path_compt, 'r', encoding='cp1252', errors='ignore') as f:
        content = f.read()
    lines = content.split('\n')
    for line in lines:
        line_str = line.strip()
        if not line_str or not line_str.startswith('"'):
            continue
        
        # Capture robuste du préfixe : "CODE" "NOM" statut (yes/no)
        match_prefix = re.match(r'^"([^"]*)"\s+"([^"]*)"\s+(yes|no)', line_str)
        if match_prefix:
            potential_code = match_prefix.group(1).strip()
            if potential_code in valid_codes:
                nom = match_prefix.group(2).strip()
                statut_brut = match_prefix.group(3).strip().lower()
                est_actif = (statut_brut == "yes")
                
                compteur_infos[potential_code] = {
                    "nom": nom,
                    "actif": est_actif
                }
        else:
            # Fallback de sécurité si la ligne a une structure exotique
            matches = re.findall(r'"([^"\\]*(?:\\.[^"\\]*)*)"', line_str)
            if matches:
                potential_code = matches[0].strip()
                if potential_code in valid_codes:
                    nom = matches[1].strip() if len(matches) >= 2 else potential_code
                    compteur_infos[potential_code] = {
                        "nom": nom,
                        "actif": True  # Actif par défaut si indéterminable
                    }
except FileNotFoundError:
    print(f"❌ Erreur : Fichier des caractéristiques introuvable : {path_compt}")
    exit(1)

# Remplissage par défaut pour les codes manquants dans le dictionnaire
for code in valid_codes:
    if code not in compteur_infos:
        compteur_infos[code] = {"nom": code, "actif": True}

# 3. Analyse des formules et liaisons
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
                tokens = re.split(r'[\s\+\-\*\/\(\)\,\=\<\>\!]+', element)
                for token in tokens:
                    child_code = token.strip()
                    if child_code in valid_codes and child_code != parent_code:
                        all_edges.add((parent_code, child_code))
except FileNotFoundError:
    print(f"❌ Erreur : Fichier des formules introuvable : {path_formule}")
    exit(1)

# 4. Filtrage (Focus ou Global)
nodes_to_keep = set()
edges_to_keep = set()

if COMPTEUR_FOCUS:
    print(f"🔍 [FOCUS] Filtrage autour de : {COMPTEUR_FOCUS}")
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
    filtered_compteurs = {code: compteur_infos[code] for code in nodes_to_keep}
    filtered_edges = edges_to_keep
    nom_fichier = f"carte_du_compteur_{COMPTEUR_FOCUS}.html"
else:
    print("🌐 [GLOBAL] Extraction complète de tous les compteurs.")
    filtered_compteurs = compteur_infos
    filtered_edges = all_edges
    nom_fichier = "carte_globale_des_compteurs.html"

# 5. Construction du Graphe (PyVis)
net = Network(height="850px", width="100%", directed=True, bgcolor="#ffffff", font_color="#000000")

# Utilisation de la physique par défaut pour les calculs initiaux
net.barnes_hut()

# Ajout des Nœuds - Stratégie "Interface Chronos" (Fonds clairs, texte noir, grisage inactifs)
for code, info in filtered_compteurs.items():
    label_visuel = f" {code} " 
    nom = info["nom"]
    actif = info["actif"]
    
    statut_texte = "Actif" if actif else "Inactif"
    infobulle = f"Code : {code}\nNom  : {nom}\nStatut : {statut_texte}"
    
    # Palette calquée sur l'application Chronos (avec grisage des inactifs)
    if not actif:
        couleur_fond = "#F5F5F5"     # Gris très clair pour le fond
        couleur_bordure = "#9E9E9E"  # Gris moyen pour la bordure
        epaisseur_bordure = 1
        couleur_police = "#9E9E9E"   # Texte grisé
    elif code == COMPTEUR_FOCUS:
        couleur_fond = "#E6EEFA"     # Bleu très clair pour le fond
        couleur_bordure = "#1A3263"  # Bleu nuit pour la bordure
        epaisseur_bordure = 3        # Plus épais pour le focus
        couleur_police = "#000000"
    else:
        couleur_fond = "#E0F2F1"     # Turquoise pastel/lumineux
        couleur_bordure = "#00A896"  # Turquoise vif pour la bordure
        epaisseur_bordure = 1
        couleur_police = "#000000"
        
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
                "background": "#FFEB3B",
                "border": "#F57F17"
            }
        },
        font={
            'size': 16, 
            'face': 'Courier', 
            'color': couleur_police, 
            'bold': True        
        }
    )

# Ajout des Liens
for source, target in filtered_edges:
    net.add_edge(source, target, color="#848484", arrows="to")

# --- CONFIGURATION STRICTE SANS CAPRICE DE PYVIS (Avec multi-sélection activée) ---
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
    "multiselect": true,
    "dragNodes": true,
    "dragView": true
  }
}
""")

# Sauvegarde propre du fichier HTML
net.save_graph(nom_fichier)

# Injection HTML/CSS/JS post-sauvegarde (Simplifiée grâce aux variables importées)
try:
    with open(nom_fichier, 'r', encoding='utf-8') as file:
        html_content = file.read()
    
    # 1. Insertion de l'écran d'attente et du panneau de sélection après l'ouverture du body
    html_content = html_content.replace('<body>', f'<body>\n{ECRAN_CHARGEMENT}\n{PANEL_SELECTION}')
    
    # 2. Remplacement de l'ancien arrêt de physique par le script JS complet (physique, loader et copie)
    html_content = html_content.replace('drawGraph();', f'drawGraph();\n    {JS_INJECTION}')
    
    with open(nom_fichier, 'w', encoding='utf-8') as file:
        file.write(html_content)

except Exception as e:
    print(f"⚠️ Note : Impossible d'injecter l'écran d'attente et les outils ({e})")

# Déplacement du fichier généré vers le dossier de sortie ciblé
path_destination = os.path.join(DOSSIER_SORTIE, nom_fichier)
try:
    if not os.path.exists(DOSSIER_SORTIE):
        os.makedirs(DOSSIER_SORTIE)
    if os.path.exists(path_destination):
        os.remove(path_destination)
    shutil.move(nom_fichier, path_destination)
    print(f"🎉 Terminé ! Le schéma a été rangé ici : '{path_destination}'")
except Exception as e:
    print(f"⚠️ Impossible de ranger le fichier dans {DOSSIER_SORTIE}, il reste à la racine. (Erreur: {e})")