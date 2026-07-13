# ==============================================================================
# TEMPLATES VISUELS ET INJECTIONS JAVASCRIPT POUR L'INTERFACE DE CARTOGRAPHIE
# ==============================================================================

# 1. ÉCRAN D'ATTENTE (Style Espace Collaborateur Chronos)
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

# 2. PANNEAU FLOTTANT DE SÉLECTION ET COPIE
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

# 3. CODE JAVASCRIPT D'INJECTION POUR LE COMPORTEMENT ACTIF
JS_INJECTION = """
network.on("stabilizationIterationsDone", function () {
    // 1. Coupe la physique
    network.setOptions({ physics: false });
    
    // 2. Fait disparaître l'écran de chargement en douceur
    var loader = document.getElementById('loading-screen');
    if (loader) {
        loader.style.opacity = '0';
        setTimeout(function() {
            loader.style.display = 'none';
        }, 500);
    }
});

// Écoute de l'événement de sélection Vis.js
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
            alert('La copie automatique a échoué. Veuillez utiliser Ctrl+C.');
        }
    } catch (err) {
        console.error('Erreur lors de la copie', err);
    }
};
"""