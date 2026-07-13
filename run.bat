@echo off
chcp 65001 > nul
title Générateur de Cartographie SIRH Chronos

echo =====================================================================
echo    GÉNÉRATEUR DE CARTOGRAPHIE INTERACTIVE DES COMPTEURS CHRONOS
echo =====================================================================
echo.

:: 1. Vérification automatique de la bibliothèque pyvis
echo [1/3] Vérification des dépendances Python...
python -c "import pyvis" 2>nul
if %errorlevel% neq 0 (
    echo     -^> Bibliothèque 'pyvis' manquante. Installation en cours...
    pip install pyvis --quiet
    if %errorlevel% neq 0 (
        echo ❌ Erreur : Impossible d'installer 'pyvis'. Vérifiez votre connexion.
        pause
        exit /b
    )
    echo     -^> Installation de 'pyvis' réussie.
) else (
    echo     -^> Dépendances OK.
)
echo.

:: 2. Demande du choix de mode
echo [2/3] Choix du mode d'affichage :
echo ---------------------------------------------------------------------
echo À blanc (appuyez juste sur Entrée) : Générer la carte GLOBALE
echo Saisir un code (ex: Z009, TEFFJ)   : Générer le FOCUS du compteur
echo ---------------------------------------------------------------------
set "compteur="
set /p "compteur=Entrez votre choix : "
echo.

:: 3. Exécution du script Python
echo [3/3] Génération du schéma interactif...
if "%compteur%"=="" (
    python main.py
) else (
    python main.py %compteur%
)

:: 4. Ouverture du dossier de résultats
if %errorlevel% equ 0 (
    echo.
    echo 🎉 Succès ! La cartographie a été générée.
    echo Ouverture du dossier des résultats...
    if exist "cartographies_generees" (
        start "" "cartographies_generees"
    )
) else (
    echo.
    echo ❌ Une erreur est survenue pendant la génération du schéma.
)

echo.
pause