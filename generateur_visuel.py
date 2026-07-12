import re
import os
import sys
import shutil
from pyvis.network import Network

# ==============================================================================
# CONFIGURATION DES DOSSIERS
# ==============================================================================
DOSSIER_DUMP = "dump_compteurs"
DOSSIER_SORTIE = "cartographies_generees"

path_master = os.path.join(DOSSIER_DUMP, "_gtgtpcpt.d")
path_compt = os.path.join(DOSSIER_DUMP, "_gtcompt.d")
path_formule = os.path.join(DOSSIER_DUMP, "_formule.d")

# Capture du focus depuis le terminal
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

# 2. Lecture du dictionnaire des noms
compteur_noms = {}
try:
    with open(path_compt, 'r', encoding='cp1252', errors='ignore') as f:
        content = f.read()
    lines = content.split('\n')
    for line in lines:
        line_str = line.strip()
        if not line_str or not line_str.startswith('"'):
            continue
        matches = re.findall(r'"([^"\\]*(?:\\.[^"\\]*)*)"', line_str)
        if matches:
            potential_code = matches[0].strip()
            if potential_code in valid_codes:
                if len(matches) >= 2:
                    compteur_noms[potential_code] = matches[1].strip()
                else:
                    compteur_noms[potential_code] = potential_code
except FileNotFoundError:
    print(f"❌ Erreur : Fichier des caractéristiques introuvable : {path_compt}")
    exit(1)

for code in valid_codes:
    if code not in compteur_noms:
        compteur_noms[code] = code

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
    filtered_compteurs = {code: compteur_noms[code] for code in nodes_to_keep}
    filtered_edges = edges_to_keep
    nom_fichier = f"carte_du_compteur_{COMPTEUR_FOCUS}.html"
else:
    print("🌐 [GLOBAL] Extraction complète de tous les compteurs.")
    filtered_compteurs = compteur_noms
    filtered_edges = all_edges
    nom_fichier = "carte_globale_des_compteurs.html"

# 5. Construction du Graphe (PyVis)
net = Network(height="850px", width="100%", directed=True, bgcolor="#ffffff", font_color="#000000")

# Utilisation de la physique par défaut pour les calculs initiaux
net.barnes_hut()

# Ajout des Nœuds - Stratégie "Interface Chronos" (Fonds clairs, texte noir)
for code, nom in filtered_compteurs.items():
    label_visuel = f" {code} " 
    
    # Palette calquée sur l'application Chronos
    if code == COMPTEUR_FOCUS:
        couleur_fond = "#E6EEFA"     # Bleu très clair pour le fond
        couleur_bordure = "#1A3263"  # Bleu nuit pour la bordure
        epaisseur_bordure = 3        # Plus épais pour le focus
    else:
        couleur_fond = "#E0F2F1"     # Turquoise pastel/lumineux
        couleur_bordure = "#00A896"  # Turquoise vif pour la bordure
        epaisseur_bordure = 1
        
    net.add_node(
        code, 
        label=label_visuel, 
        title=f"{code} - {nom}", 
        shape="box", 
        borderWidth=epaisseur_bordure,
        color={
            "background": couleur_fond,
            "border": couleur_bordure,
            "highlight": { # Couleur quand on clique dessus
                "background": "#FFEB3B",
                "border": "#F57F17"
            }
        },
        font={
            'size': 16, 
            'face': 'Courier', 
            'color': '#000000', # TEXTE NOIR PUR
            'bold': True        
        }
    )

# Ajout des Liens
for source, target in filtered_edges:
    net.add_edge(source, target, color="#848484", arrows="to")

# --- CONFIGURATION STRICTE SANS CAPRICE DE PYVIS ---
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
    "dragView": true
  }
}
""")

# Sauvegarde propre du fichier HTML
net.save_graph(nom_fichier)

# Injection HTML/CSS/JS post-sauvegarde pour l'écran de chargement personnalisé
try:
    with open(nom_fichier, 'r', encoding='utf-8') as file:
        html_content = file.read()
    
    # 1. Écran d'attente HTML & CSS (Style Espace Collaborateur Chronos)
    ecran_chargement = """
    <!-- Écran d'attente personnalisé -->
    <div id="loading-screen" style="
        position: fixed;
        top: 0; left: 0;
        width: 100%; height: 100%;
        background-color: #ffffff;
        z-index: 99999;
        display: flex;
        flex-direction: column;
        justify-content: center;
        align-items: center;
        font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
        transition: opacity 0.5s ease-on-out;
    ">
        <!-- Spinner d'attente Turquoise Chronos -->
        <div style="
            border: 6px solid #E0F2F1;
            border-top: 6px solid #00A896;
            border-radius: 50%;
            width: 60px; height: 60px;
            animation: spin 1s linear infinite;
            margin-bottom: 20px;
        "></div>
        <h2 style="color: #1A3263; margin: 0; font-weight: 600;">Génération de la cartographie...</h2>
        <p style="color: #848484; margin: 5px 0 0 0; font-size: 14px;">Calcul des liaisons entre les compteurs</p>
    </div>

    <style>
        @keyframes spin {
            0% { transform: rotate(0deg); }
            100% { transform: rotate(360deg); }
        }
    </style>
    """

    # 2. Script JS pour masquer l'écran d'attente à la fin de la stabilisation
    js_fix_avec_loader = """
    network.on("stabilizationIterationsDone", function () {
        // 1. Coupe la physique
        network.setOptions({ physics: false });
        
        // 2. Fait disparaître l'écran de chargement en douceur
        var loader = document.getElementById('loading-screen');
        if (loader) {
            loader.style.opacity = '0';
            setTimeout(function() {
                loader.style.display = 'none';
            }, 500); // Temps de la transition CSS
        }
    });
    """

    # Insertion de l'écran d'attente juste après l'ouverture de la balise body
    html_content = html_content.replace('<body>', f'<body>\n{ecran_chargement}')
    
    # Remplacement de l'ancien arrêt de physique par notre version améliorée
    html_content = html_content.replace('drawGraph();', f'drawGraph();\n    {js_fix_avec_loader}')
    
    with open(nom_fichier, 'w', encoding='utf-8') as file:
        file.write(html_content)

except Exception as e:
    print(f"⚠️ Note : Impossible d'injecter l'écran d'attente ({e})")


# Déplacement du fichier généré vers le dossier cible défini par la variable
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