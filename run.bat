@echo off
chcp 65001 > nul
title Générateur de Cartographie SIRH Chronos

echo =====================================================================
echo    GÉNÉRATEUR DE CARTOGRAPHIE INTERACTIVE DES COMPTEURS CHRONOS
echo =====================================================================
echo.

:: 1. Vérification automatique de la bibliothèque pyvis
echo [1/2] Vérification des dépendances Python...
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

:: 2. Exécution directe de la génération globale
echo [2/2] Génération du schéma interactif global...
python main.py

:: 3. Ouverture du dossier de résultats
if %errorlevel% equ 0 (
echo.
echo 🎉 Succès ! La cartographie globale a été générée.
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