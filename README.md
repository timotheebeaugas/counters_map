# **Outil de Cartographie et Graphe de Dépendance des Compteurs**

Cet outil permet de générer une cartographie interactive et visuelle sous forme de **graphe de dépendances orienté** à partir des fichiers de dump Progress du logiciel de gestion de temps **Chronos**.

Il facilite l'analyse des liaisons de formules entre les différents compteurs, permettant aux consultants de diagnostiquer et de vérifier rapidement les configurations.

## **📂 Structure du projet**

```
counters\_modeling/  
│  
├── main.py                     \<-- Script principal (lecture des dumps, filtrage & construction du graphe)  
├── templates.py                \<-- Constantes d'interface (écran de chargement, panneau de sélection, légende & scripts JS)  
├── run.bat                     \<-- Lanceur automatique
├── README.md                   \<-- Documentation du projet (ce fichier)  
│  
├── dump\_compteurs/             \<-- Dossier contenant vos fichiers sources de dump .d  
│   ├── \_gtgtpcpt.d             \<-- Fichier master des types de compteurs  
│   ├── \_gtcompt.d              \<-- Dictionnaire des libellés et caractéristiques  
│   └── \_formule.d              \<-- Liaisons et formules de calcul  
│  
└── cartographies\_generees/     \<-- Répertoire de sortie des schémas HTML interactifs
```

## **🎨 Code Couleur Ergonomique (Légende intégrée)**

Le graphe intègre une charte visuelle pensée pour l'analyse d'un consultant en gestion des temps :

* **Turquoise Pastel (Style classique)** : Compteur standard de calcul ou d'accumulation intermédiaire.  
* **Bleu Lavande / Indigo** : Compteur alimentant directement un droit (RTT, Congés Annuels, etc.). Affiche la ligne Droit : \[CODE\] dans l'infobulle.  
* **Orange Abricot / Ambre** : Compteur terminal de paie exportant directement vers une rubrique. Affiche la ligne Rubrique Paie : \[CODE\] dans l'infobulle.  
* **Rouge Corail / Cerise** : Compteur sélectionné par clic, ou au centre du filtrage lors d'une recherche avec ciblage (Focus).  
* **Gris Neutre** : Compteur désactivé/inactif dans la configuration de l'entreprise.

## **🚀 Utilisation**

L'utilisation a été entièrement simplifiée grâce au lanceur run.bat. Lancez simplement la commande dans votre console à la racine du projet :

.\\run

*Le fichier de sortie sera généré sous : cartographies_generees/carte_globale_des_compteurs.html*

## **💡 Fonctionnalités de l'interface**

1. **Écran de chargement pro** : Affichage d'une barre de progression fluide avec pourcentage et intégration du logo officiel Chronos pendant la stabilisation du graphe.  
2. **Moteur de recherche intelligent** : Recherche dynamique par code ou libellé avec surbrillance et recentrage automatique de la caméra sur le compteur recherché.  
3. **Panneau de sélection multiple** : Maintenez Ctrl / Cmd enfoncé sur la carte pour sélectionner plusieurs compteurs et copiez la liste de leurs codes en un seul clic. 
4. **Légende interactive** : Une légende dépliable en bas à droite permet de vous repérer à tout moment sans encombrer l'espace de travail.