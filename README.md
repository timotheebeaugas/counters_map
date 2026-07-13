## Outil de Cartographie et Graphe de Dépendance des Compteurs

Cet outil permet de générer une cartographie interactive et visuelle sous forme de **graphe de dépendances orienté** à partir des fichiers de dump des compteurs du logiciel de gestion de temps **Chronos**.

Il facilite l'analyse des liaisons de formules entre les différents compteurs, permettant aux consultants de diagnostiquer et de vérifier rapidement les configurations.

### 📂 Structure du projet

```
counters_modeling/
│
├── main.py <-- Script principal (lecture des dumps, filtrage & construction du graphe)
├── templates.py <-- Constantes d'interface (écran de chargement, panneau de sélection & scripts JS)
├── run.bat <-- Lanceur générique ultra-rapide (ex: .\\run ou .\\run CODE)
├── README.md <-- Documentation du projet (ce fichier)
│
├── dump_compteurs/ <-- Dossier contenant vos fichiers sources de dump .d
│ ├── _gtgtpcpt.d <-- Fichier master des types de compteurs
│ ├── _gtcompt.d <-- Dictionnaire des libellés et caractéristiques
│ └── _formule.d <-- Liaisons et formules de calcul
│
└── cartographies_generees/ <-- Répertoire de sortie des schémas HTML interactifs
```

### 🚀 Utilisation

L'utilisation a été simplifiée grâce au lanceur générique `run.bat`. Ouvrez votre console à la racine du projet et utilisez l'une des commandes suivantes :

#### 1. Générer la cartographie globale complète

Génère un graphe complet de tous les compteurs liés entre eux :

```
.\\run
```

*Le fichier de sortie sera disponible sous : `cartographies_generees/carte_globale_des_compteurs.html`*

#### 2. Générer une cartographie filtrée autour d'un compteur (Focus)

Génère uniquement le sous-graphe des dépendances (directes et indirectes, ascendantes et descendantes) d'un compteur ciblé :

```
.\\run DCAH
```

*(Remplacez `DCAH` par le code du compteur souhaité) Le fichier de sortie sera disponible sous : `cartographies_generees/carte_du_compteur_DCAH.html`*