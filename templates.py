# ==============================================================================
# TEMPLATES VISUELS ET INJECTIONS JAVASCRIPT POUR L'INTERFACE DE CARTOGRAPHIE
# ==============================================================================

# 1. ÉCRAN D'ATTENTE (Style Espace Collaborateur Chronos avec Barre de Progression)
ECRAN_CHARGEMENT = """
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
    transition: opacity 0.5s ease-out;
">
    <!-- Logo officiel de l'application Chronos (sur fond blanc) -->
    <img src="../assets/chronos.jpg" alt="Logo Chronos" style="
        max-height: 135px;
        max-width: 380px;
        margin-bottom: 30px;
        object-fit: contain;
    ">

    <h2 style="color: #1A3263; margin: 0; font-weight: 600;">Génération de la cartographie...</h2>
    <p style="color: #848484; margin: 5px 0 0 0; font-size: 14px;">Calcul des liaisons entre les compteurs</p>
    
    <!-- Conteneur externe de la barre de progression -->
    <div style="
        width: 320px;
        height: 12px;
        background-color: #E0F2F1;
        border-radius: 6px;
        margin-top: 25px;
        overflow: hidden;
        border: 1px solid #B2DFDB;
    ">
        <!-- Barre de progression interne dynamique -->
        <div id="progress-bar-fill" style="
            width: 0%;
            height: 100%;
            background-color: #00A896;
            transition: width 0.1s ease-out;
        "></div>
    </div>
    
    <!-- Pourcentage de progression positionné juste en dessous -->
    <div id="progress-percentage" style="
        margin-top: 10px;
        font-size: 16px;
        font-weight: 700;
        color: #1A3263;
    ">0%</div>
</div>
"""

# 2. PANEL DE SÉLECTION MULTIPLE ET COPIE RAPIDE
PANEL_SELECTION = """
<!-- Panneau flottant de sélection Chronos -->
<div id="selection-panel" style="
    position: fixed;
    top: 20px;
    left: 20px;
    z-index: 9999;
    background: rgba(255, 255, 255, 0.96);
    border: 2px solid #00A896;
    border-radius: 8px;
    padding: 15px;
    box-shadow: 0 4px 20px rgba(0,0,0,0.15);
    font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
    width: 280px;
    display: none; /* Masqué par défaut */
    transition: opacity 0.2s ease;
">
    <!-- Bouton Fermer & Désélectionner Tout -->
    <button id="close-panel-btn" onclick="clearSelectionAndClose()" title="Fermer et tout désélectionner" style="
        position: absolute;
        top: 10px;
        right: 12px;
        background: none;
        border: none;
        font-size: 20px;
        font-weight: bold;
        color: #848484;
        cursor: pointer;
        padding: 0;
        line-height: 1;
        transition: color 0.15s ease;
    " onmouseover="this.style.color='#00A896'" onmouseout="this.style.color='#848484'">&times;</button>

    <h4 style="margin: 0 0 8px 0; color: #1A3263; font-weight: 600; font-size: 14px; padding-right: 20px;">Compteurs sélectionnés</h4>
    
    <!-- Zone textuelle pour la copie -->
    <textarea id="selection-text" readonly style="
        width: 100%;
        height: 55px;
        resize: none;
        border: 1px solid #cccccc;
        border-radius: 4px;
        padding: 8px;
        font-family: 'Courier New', Courier, monospace;
        font-size: 12px;
        color: #333333;
        background-color: #f9f9f9;
        box-sizing: border-box;
        margin-bottom: 10px;
    "></textarea>
    
    <!-- Bouton Copier -->
    <button id="copy-btn" onclick="copySelectionToClipboard()" style="
        width: 100%;
        background-color: #00A896;
        color: white;
        border: none;
        border-radius: 4px;
        padding: 8px 12px;
        font-weight: bold;
        font-size: 13px;
        cursor: pointer;
        transition: background-color 0.2s;
    ">Copier les codes</button>
    
    <p style="margin: 8px 0 0 0; font-size: 11px; color: #848484; text-align: center; line-height: 1.3;">
        Maintenez <strong>Ctrl</strong> (ou <strong>Cmd</strong> sur Mac)<br>pour sélectionner plusieurs compteurs
    </p>
</div>
"""

# 3. PANNEAU DE RECHERCHE INTELLIGENT CHRONOS AVEC SA LÉGENDE INTERACTIVE
PANEL_RECHERCHE = """
<!-- Panneau de recherche flottant Chronos (en haut à droite) -->
<div id="search-container" style="
    position: fixed;
    top: 20px;
    right: 20px;
    z-index: 9999;
    font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
    width: 340px;
    box-sizing: border-box;
    pointer-events: auto;
    background: transparent;
">
    <!-- Barre de recherche -->
    <div id="search-bar" style="
        background: rgba(255, 255, 255, 0.98);
        border: 2px solid #1A3263;
        border-radius: 8px;
        padding: 10px 12px;
        box-shadow: 0 4px 15px rgba(0,0,0,0.1);
        display: flex;
        gap: 8px;
        align-items: center;
        transition: border-radius 0.1s ease;
    ">
        <input type="text" id="search-input" placeholder="Chercher un code ou un nom..." autocomplete="off" style="
            flex: 1;
            padding: 8px 12px;
            border: 1px solid #cccccc;
            border-radius: 4px;
            font-size: 13px;
            outline: none;
            transition: border-color 0.15s ease;
        " onfocus="this.style.borderColor='#1A3263'" onblur="this.style.borderColor='#cccccc'">
        
        <button id="search-btn" onclick="executeSearch()" style="
            background-color: #1A3263;
            color: white;
            border: none;
            border-radius: 4px;
            padding: 8px 16px;
            font-weight: bold;
            font-size: 13px;
            cursor: pointer;
            transition: background-color 0.15s;
        " onmouseover="this.style.backgroundColor='#00A896'" onmouseout="this.style.backgroundColor='#1A3263'">
            Chercher
        </button>
    </div>
    
    <!-- Liste d'autocomplétion premium personnalisée -->
    <div id="custom-search-results" style="
        display: none;
        background: white;
        border: 1px solid #00A896;
        border-top: none;
        border-radius: 0 0 8px 8px;
        margin-top: 1px;
        box-shadow: 0 8px 24px rgba(0,0,0,0.15);
        max-height: 250px;
        overflow-y: auto;
        box-sizing: border-box;
    "></div>
</div>

<!-- Légende Flottante et Rétractable Chronos (Placée en bas à droite) -->
<div id="legend-panel" style="
    position: fixed;
    bottom: 20px;
    right: 20px;
    z-index: 9998;
    background: rgba(255, 255, 255, 0.96);
    border: 2px solid #1A3263;
    border-radius: 8px;
    padding: 12px;
    box-shadow: 0 4px 15px rgba(0,0,0,0.12);
    font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
    width: 220px;
    transition: all 0.25s cubic-bezier(0.4, 0, 0.2, 1);
    user-select: none;
">
    <!-- En-tête de la légende (cliquable pour plier/déplier) -->
    <div style="display: flex; justify-content: space-between; align-items: center; cursor: pointer;" onclick="toggleLegend()">
        <h4 style="margin: 0; color: #1A3263; font-weight: 600; font-size: 13px;">Légende de la carte</h4>
        <span id="legend-toggle-icon" style="font-size: 11px; color: #1A3263; font-weight: bold; transition: transform 0.2s; transform: rotate(0deg);">▲</span>
    </div>
    
    <!-- Corps de la légende -->
    <div id="legend-content" style="margin-top: 12px; display: flex; flex-direction: column; gap: 8px; transition: opacity 0.2s;">
        <!-- Calcul Classique -->
        <div style="display: flex; align-items: center; gap: 10px;">
            <div style="width: 24px; height: 16px; background-color: #E0F2F1; border: 1px solid #00A896; border-radius: 3px; box-sizing: border-box;"></div>
            <span style="font-size: 11px; color: #424242; font-weight: 500;">Calcul Intermédiaire</span>
        </div>
        <!-- Droit -->
        <div style="display: flex; align-items: center; gap: 10px;">
            <div style="width: 24px; height: 16px; background-color: #E8EAF6; border: 2px solid #3F51B5; border-radius: 3px; box-sizing: border-box;"></div>
            <span style="font-size: 11px; color: #424242; font-weight: 500;">Alimente un Droit (RTT, CA...)</span>
        </div>
        <!-- Paie -->
        <div style="display: flex; align-items: center; gap: 10px;">
            <div style="width: 24px; height: 16px; background-color: #FFF3E0; border: 2px solid #FB8C00; border-radius: 3px; box-sizing: border-box;"></div>
            <span style="font-size: 11px; color: #424242; font-weight: 500;">Alimente la Paie (Rubrique)</span>
        </div>
        <!-- Focus -->
        <div style="display: flex; align-items: center; gap: 10px;">
            <div style="width: 24px; height: 16px; background-color: #E6EEFA; border: 3px solid #1A3263; border-radius: 3px; box-sizing: border-box;"></div>
            <span style="font-size: 11px; color: #424242; font-weight: 500;">Compteur Ciblé (Focus)</span>
        </div>
        <!-- Inactif -->
        <div style="display: flex; align-items: center; gap: 10px;">
            <div style="width: 24px; height: 16px; background-color: #F5F5F5; border: 1px solid #9E9E9E; border-radius: 3px; box-sizing: border-box;"></div>
            <span style="font-size: 11px; color: #9E9E9E; font-weight: 500;">Compteur Inactif</span>
        </div>
    </div>
</div>

<script>
    // Fonction interactive pour plier/déplier la légende
    window.toggleLegend = function() {
        var content = document.getElementById('legend-content');
        var icon = document.getElementById('legend-toggle-icon');
        var panel = document.getElementById('legend-panel');
        
        if (content.style.display === 'none') {
            content.style.display = 'flex';
            icon.style.transform = 'rotate(0deg)';
            panel.style.width = '220px';
        } else {
            content.style.display = 'none';
            icon.style.transform = 'rotate(180deg)';
            panel.style.width = '150px';
        }
    };
</script>

<style>
    /* Style de la barre de scroll interne des suggestions */
    #custom-search-results::-webkit-scrollbar {
        width: 6px;
    }
    #custom-search-results::-webkit-scrollbar-track {
        background: #f1f1f1;
    }
    #custom-search-results::-webkit-scrollbar-thumb {
        background: #00A896;
        border-radius: 3px;
    }
</style>
"""

# 4. CODE JAVASCRIPT D'INJECTION POUR LE COMPORTEMENT ACTIF (AVEC RECHERCHE ET BARRE DE PROGRESSION)
JS_INJECTION = """
// Écoute de la progression physique en temps réel pour mettre à jour la barre et le pourcentage
network.on("stabilizationProgress", function (params) {
    var percentage = Math.round((params.iterations / params.total) * 100);
    
    // Mise à jour de la largeur de la barre de chargement
    var progressBar = document.getElementById('progress-bar-fill');
    if (progressBar) {
        progressBar.style.width = percentage + '%';
    }
    
    // Mise à jour du texte de pourcentage juste en dessous
    var progressText = document.getElementById('progress-percentage');
    if (progressText) {
        progressText.innerText = percentage + '%';
    }
});

// Écoute de la fin de la stabilisation
network.on("stabilizationIterationsDone", function () {
    // 1. Force l'affichage à 100% sur la barre et le texte
    var progressBar = document.getElementById('progress-bar-fill');
    if (progressBar) progressBar.style.width = '100%';
    
    var progressText = document.getElementById('progress-percentage');
    if (progressText) progressText.innerText = '100%';

    // 2. Coupe la physique globale pour figer les nœuds et éviter toute latence
    network.setOptions({ physics: false });
    
    // 3. Fait disparaître l'écran de chargement en douceur
    var loader = document.getElementById('loading-screen');
    if (loader) {
        loader.style.opacity = '0';
        setTimeout(function() {
            loader.style.display = 'none';
        }, 500);
    }
    
    // 4. Initialise le moteur de recherche d'autocomplétion premium
    initCustomAutocomplete();
});

// Écoute de l'événement de saisie clavier pour l'autocomplétion
window.initCustomAutocomplete = function() {
    var searchInput = document.getElementById('search-input');
    var resultsBox = document.getElementById('custom-search-results');
    
    if (!searchInput || !resultsBox || typeof searchDatabase === 'undefined') return;
    
    searchInput.addEventListener('input', function() {
        var query = searchInput.value.trim().toLowerCase();
        resultsBox.innerHTML = ''; // Nettoyage
        
        if (!query) {
            resultsBox.style.display = 'none';
            document.getElementById('search-bar').style.borderRadius = '8px';
            return;
        }
        
        // Recherche insensible à la casse sur le code ou le nom
        var matches = searchDatabase.filter(function(item) {
            return item.code.toLowerCase().includes(query) || 
                   item.nom.toLowerCase().includes(query);
        });
        
        if (matches.length === 0) {
            resultsBox.style.display = 'none';
            document.getElementById('search-bar').style.borderRadius = '8px';
            return;
        }
        
        // Affiche au maximum les 10 meilleurs résultats pour garder une belle interface
        matches.slice(0, 10).forEach(function(item) {
            var row = document.createElement('div');
            row.style.padding = '10px 14px';
            row.style.cursor = 'pointer';
            row.style.fontSize = '12px';
            row.style.borderBottom = '1px solid #f0f0f0';
            row.style.transition = 'all 0.15s ease';
            row.style.fontFamily = 'Segoe UI, sans-serif';
            row.style.color = '#333333';
            row.style.display = 'flex';
            row.style.justifyContent = 'space-between';
            row.style.alignItems = 'center';
            row.style.boxSizing = 'border-box';
            
            // Définition de la pastille Actif / Inactif selon l'état réel du compteur
            var statusText = item.actif ? 'Actif' : 'Inactif';
            var statusBg = item.actif ? '#E0F2F1' : '#EEEEEE';
            var statusColor = item.actif ? '#00A896' : '#9E9E9E';
            
            // Format visuel de la ligne
            row.innerHTML = '<span><strong style="color: #1A3263;">' + item.code + '</strong> - <span style="color: #555;">' + item.nom + '</span></span>' +
                            '<span style="font-size: 10px; padding: 2px 6px; border-radius: 4px; background-color: ' + statusBg + '; color: ' + statusColor + '; font-weight: bold; transition: background 0.15s;">' + statusText + '</span>';
            
            // Détermination dynamique des couleurs de surbrillance au survol (cohérent avec les nœuds)
            var hoverBg = '#E0F2F1';     // Classique Actif (Turquoise)
            var hoverBorder = '#00A896';
            
            if (!item.actif) {
                hoverBg = '#F5F5F5';      // Inactif (Gris)
                hoverBorder = '#9E9E9E';
            } else if (item.rubrique_paie) {
                hoverBg = '#FFF3E0';      // Paie Actif (Orange Abricot)
                hoverBorder = '#FB8C00';
            } else if (item.droit) {
                hoverBg = '#E8EAF6';      // Droit Actif (Bleu Periwinkle)
                hoverBorder = '#3F51B5';
            }
            
            // Événement au survol (style Chronos personnalisé par type de compteur)
            row.addEventListener('mouseover', function() {
                row.style.backgroundColor = hoverBg;
                row.style.color = '#1A3263';
                row.style.borderLeft = '3px solid ' + hoverBorder;
                row.style.paddingLeft = '11px'; // Ajustement pour compenser la bordure gauche de 3px
            });
            
            row.addEventListener('mouseout', function() {
                row.style.backgroundColor = 'transparent';
                row.style.color = '#333333';
                row.style.borderLeft = 'none';
                row.style.paddingLeft = '14px';
            });
            
            // Événement au clic sur un élément de la suggestion
            row.addEventListener('click', function() {
                searchInput.value = item.code + " - " + item.nom;
                resultsBox.style.display = 'none';
                executeSearch(); // Déclenche instantanément la recherche
            });
            
            resultsBox.appendChild(row);
        });
        
        // Rend le volet de suggestions visible avec des bords inférieurs arrondis pour fusionner avec la barre
        resultsBox.style.display = 'block';
        document.getElementById('search-bar').style.borderRadius = '8px 8px 0 0';
        document.getElementById('search-bar').style.borderBottom = '1px solid #1A3263';
    });
    
    // Ferme le volet de suggestions en cliquant en dehors de la boîte de recherche
    document.addEventListener('click', function(e) {
        if (!searchInput.contains(e.target) && !resultsBox.contains(e.target)) {
            resultsBox.style.display = 'none';
            document.getElementById('search-bar').style.borderRadius = '8px';
            document.getElementById('search-bar').style.borderBottom = '2px solid #1A3263';
        }
    });
};

// Écoute de l'événement de sélection Vis.js pour le panneau de copie
network.on("select", function (params) {
    updateSelectionPanel();
});
network.on("deselect", function (params) {
    updateSelectionPanel();
});

// Met à jour la liste des compteurs sélectionnés dans l'interface
window.updateSelectionPanel = function() {
    var selectedNodes = network.getSelectedNodes();
    var panel = document.getElementById('selection-panel');
    var textarea = document.getElementById('selection-text');
    var btn = document.getElementById('copy-btn');
    
    if (selectedNodes && selectedNodes.length > 0) {
        panel.style.display = 'block';
        textarea.value = selectedNodes.join(','); // Séparation par virgule sans espace
        btn.innerHTML = 'Copier les codes (' + selectedNodes.length + ')';
    } else {
        panel.style.display = 'none';
        textarea.value = '';
    }
};

// Désélectionne tous les compteurs et cache le panneau
window.clearSelectionAndClose = function() {
    if (network) {
        network.unselectAll();
        updateSelectionPanel();
    }
};

// Exécute la recherche par touche Entrée
document.addEventListener('keypress', function(e) {
    if (e.key === 'Enter') {
        var activeEl = document.activeElement;
        var searchInput = document.getElementById('search-input');
        if (activeEl === searchInput) {
            var resultsBox = document.getElementById('custom-search-results');
            if (resultsBox) resultsBox.style.display = 'none';
            executeSearch();
        }
    }
});

// Recherche visuelle et ciblage de caméra sur la carte
window.executeSearch = function() {
    var input = document.getElementById('search-input');
    var searchBar = document.getElementById('search-bar');
    if (!input || !searchBar) return;
    
    var query = input.value.trim();
    if (!query) return;
    
    var targetCode = null;
    
    // 1. Découpage pour récupérer le code depuis le format "CODE - Nom"
    var parts = query.split(" - ");
    var potentialCode = parts[0].trim().toUpperCase();
    
    if (network.body.data.nodes.get(potentialCode)) {
        targetCode = potentialCode;
    } else {
        // 2. Recherche textuelle globale insensible à la casse
        var queryLower = query.toLowerCase();
        var matched = searchDatabase.find(function(item) {
            return item.code.toUpperCase() === query.toUpperCase() || 
                   item.nom.toLowerCase().includes(queryLower);
        });
        if (matched) {
            targetCode = matched.code;
        }
    }
    
    // Restaure le style normal de la barre de recherche
    document.getElementById('custom-search-results').style.display = 'none';
    searchBar.style.borderRadius = '8px';
    searchBar.style.borderBottom = '2px solid #1A3263';
    
    if (targetCode) {
        network.unselectAll();
        
        // Focus fluide
        network.focus(targetCode, {
            scale: 1.25,
            animation: {
                duration: 800,
                easingFunction: "easeInOutQuad"
            }
        });
        
        // Sélectionne le nœud pour ouvrir le panneau de copie et appliquer le style jaune
        network.selectNodes([targetCode]);
        updateSelectionPanel();
        
        // Animation visuelle de succès (Vert) sur la barre
        searchBar.style.borderColor = "#2e7d32";
        setTimeout(function() {
            searchBar.style.borderColor = "#1A3263";
        }, 1500);
    } else {
        // Animation visuelle d'échec (Rouge) sur la barre
        searchBar.style.borderColor = "#c62828";
        setTimeout(function() {
            searchBar.style.borderColor = "#1A3263";
        }, 1500);
    }
};

// Copie robuste vers le presse-papier compatible Iframe
window.copySelectionToClipboard = function() {
    var textarea = document.getElementById('selection-text');
    textarea.select();
    textarea.setSelectionRange(0, 99999);
    
    try {
        var successful = document.execCommand('copy');
        var btn = document.getElementById('copy-btn');
        if (successful) {
            var originalText = btn.innerHTML;
            btn.innerHTML = 'Copié ! ✅';
            btn.style.backgroundColor = '#2e7d32';
            setTimeout(function() {
                btn.innerHTML = originalText;
                btn.style.backgroundColor = '#00A896';
            }, 1200);
        } else {
            console.warn('La copie automatique a échoué.');
        }
    } catch (err) {
        console.error('Erreur lors de la copie', err);
    }
};
"""