# **Outil de Cartographie et Graphe de Dépendance des Compteurs**

Cet outil permet de générer une cartographie interactive et visuelle sous forme de **graphe de dépendances orienté** à partir des fichiers de dump Progress du logiciel de gestion de temps **Chronos**.

Il facilite l'analyse des liaisons de formules entre les différents compteurs, permettant aux consultants de diagnostiquer et de vérifier rapidement les configurations.

## **📂 Structure du projet**

counters\_modeling/  
│  
├── main.py                     \<-- Script principal (lecture des dumps, filtrage & construction du graphe)  
├── templates.py                \<-- Constantes d'interface (écran de chargement, panneau de sélection, légende & scripts JS)  
├── run.bat                     \<-- Lanceur générique ultra-rapide (ex: .\\run ou .\\run CODE)  
├── README.md                   \<-- Documentation du projet (ce fichier)  
│  
├── assets/                     \<-- Ressources visuelles pour l'interface  
│   └── chronos.jpg             \<-- Logo officiel pour l'écran d'accueil  
│  
├── dump\_compteurs/             \<-- Dossier contenant vos fichiers sources de dump .d  
│   ├── \_gtgtpcpt.d             \<-- Fichier master des types de compteurs  
│   ├── \_gtcompt.d              \<-- Dictionnaire des libellés et caractéristiques  
│   └── \_formule.d              \<-- Liaisons et formules de calcul  
│  
└── cartographies\_generees/     \<-- Répertoire de sortie des schémas HTML interactifs

## **🎨 Code Couleur Ergonomique (Légende intégrée)**

Le graphe intègre une charte visuelle pensée pour l'analyse d'un consultant en gestion des temps :

* **Turquoise Pastel (Style classique)** : Compteur standard de calcul ou d'accumulation intermédiaire.  
* **Bleu Lavande / Indigo** : Compteur alimentant directement un droit (RTT, Congés Annuels, etc.). Affiche la ligne Droit : \[CODE\] dans l'infobulle.  
* **Orange Abricot / Ambre** : Compteur terminal de paie exportant directement vers une rubrique. Affiche la ligne Rubrique Paie : \[CODE\] dans l'infobulle.  
* **Rouge Corail / Cerise** : Compteur sélectionné par clic, ou au centre du filtrage lors d'une recherche avec ciblage (Focus).  
* **Gris Neutre** : Compteur désactivé/inactif dans la configuration de l'entreprise.

## **🚀 Utilisation**

L'utilisation a été simplifiée grâce au lanceur générique run.bat. Ouvrez votre console à la racine du projet et utilisez l'une des commandes suivantes :

### **1\. Générer la cartographie globale complète**

Génère un graphe complet de tous les compteurs liés entre eux :

.\\run

*Le fichier de sortie sera disponible sous : cartographies\_generees/carte\_globale\_des\_compteurs.html*

### **2\. Générer une cartographie filtrée autour d'un compteur (Focus)**

Génère uniquement le sous-graphe des dépendances (directes et indirectes, ascendantes et descendantes) d'un compteur ciblé :

.\\run CPT1

*(Remplacez CPT1 par le code du compteur souhaité)*. *Le fichier de sortie sera disponible sous : cartographies\_generees/carte\_du\_compteur\CPT1.html*

## **💡 Fonctionnalités de l'interface**

1. **Écran de chargement pro** : Affichage d'une barre de progression fluide avec pourcentage et intégration du logo officiel Chronos pendant la stabilisation physique du graphe.  
2. **Moteur de recherche intelligent** : Recherche dynamique par code ou libellé avec une surbrillance personnalisée (aux couleurs du type de compteur) lors du survol des suggestions.  
3. **Panneau de sélection multiple** : Maintenez Ctrl / Cmd enfoncé pour sélectionner plusieurs compteurs et copiez la liste de leurs codes en un seul clic pour vos requêtes.  
4. **Légende interactive** : Une légende dépliable en bas à droite vous permet de vous repérer à tout moment sans empiéter sur l'espace de travail.