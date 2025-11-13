# OpenCV TPs - Travaux Pratiques

Ce dépôt contient les travaux pratiques OpenCV en C++.

## Prérequis

- OpenCV (version 3.x ou 4.x)
- g++ ou un compilateur C++ compatible
- CMake (optionnel, pour la méthode de compilation CMake)

### Installation d'OpenCV (Ubuntu/Debian)

```bash
sudo apt-get update
sudo apt-get install libopencv-dev
```

## Structure du projet

```
opencv_tps/
├── TP1.cpp              # TP1: Profil d'intensité
├── TP2.cpp              # TP2: Expansion de plage et histogrammes
├── CMakeLists.txt       # Configuration CMake
├── Makefile             # Makefile pour compilation simple
└── README.md            # Ce fichier
```

## Compilation

### Méthode 1: Avec Makefile (recommandé)

```bash
# Compiler tous les TPs
make all

# Ou compiler individuellement
make tp1
make tp2

# Nettoyer les fichiers compilés
make clean
```

### Méthode 2: Avec CMake

```bash
mkdir build
cd build
cmake ..
make
```

### Méthode 3: Compilation manuelle

```bash
# TP1
g++ -std=c++11 TP1.cpp -o tp1 `pkg-config --cflags --libs opencv4`

# TP2
g++ -std=c++11 TP2.cpp -o tp2 `pkg-config --cflags --libs opencv4`
```

*Note: Remplacez `opencv4` par `opencv` si vous utilisez OpenCV 3.x*

## Utilisation

### TP1 - Profil d'intensité

Ce programme affiche le profil d'intensité d'une ligne sélectionnée dans une image.

```bash
./tp1
```

**Fonctionnalités:**
- Cliquez sur l'image pour sélectionner une ligne horizontale
- Le profil d'intensité s'affiche dans une fenêtre séparée
- Appuyez sur 'r' pour réinitialiser
- Appuyez sur 'q' ou ESC pour quitter

**Configuration:**
- Par défaut, charge l'image `test.jpg`
- Modifiez la variable `imagePath` dans le code pour utiliser une autre image

### TP2 - Expansion de plage et histogrammes (Homework 2)

Ce programme effectue une expansion de plage (contrast stretching) et affiche les histogrammes.

```bash
# Télécharger l'image de test
make download_test_image

# Exécuter le programme
./tp2

# Ou avec une image personnalisée
./tp2 mon_image.png
```

**Fonctionnalités:**
- Affiche 4 fenêtres:
  1. Image originale
  2. Image avec expansion de plage
  3. Histogramme original
  4. Histogramme de l'image étendue
- Appuyez sur 's' pour sauvegarder l'image étendue et les histogrammes
- Appuyez sur 'q' ou ESC pour quitter

**L'image de test:**
L'image AI_totoro.png semble noire mais ne l'est pas! Elle a une très faible plage de valeurs de gris, ce qui la rend idéale pour démontrer l'expansion de plage.

## Concepts théoriques

### TP2 - Expansion de plage (Range Expansion / Contrast Stretching)

L'expansion de plage est une technique d'amélioration d'image qui étend les valeurs de pixels pour utiliser toute la plage disponible [0, 255].

**Formule:**
```
new_value = (old_value - min) * 255 / (max - min)
```

Où:
- `old_value` = valeur du pixel original
- `min` = valeur minimale dans l'image originale
- `max` = valeur maximale dans l'image originale

**Avantages:**
- Améliore le contraste pour les images sous-exposées ou surexposées
- Simple et efficace
- Préserve les relations relatives entre les pixels

**Histogramme:**
Un histogramme montre la distribution des intensités de pixels dans une image. Après l'expansion de plage, l'histogramme devrait être plus étalé sur toute la plage [0, 255].

## Ressources

- [Documentation OpenCV](https://docs.opencv.org/)
- [OpenCV Histogram Tutorial](https://docs.opencv.org/4.x/d8/dbc/tutorial_histogram_calculation.html)
- Image de test: https://mavromatis.org/dl/AI_totoro.png

## Auteur

Développé dans le cadre des travaux pratiques OpenCV.
