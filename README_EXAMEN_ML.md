# Examen Apprentissage Automatique - Calculatrice par IA

## Description

Ce projet implémente une calculatrice par apprentissage artificiel capable de reproduire:
- **f(a,b) = a + b** (addition) avec régression linéaire
- **g(a,b) = a × b** (multiplication) avec plongement non-linéaire

## Prérequis

```bash
pip install numpy scikit-learn
```

## Utilisation

### Exécuter le programme complet

```bash
python examen_ml_calculatrice.py
```

Le programme affiche:
- Création des jeux de données
- Résultats pour l'addition (Partie 2)
- Résultats pour la multiplication (Partie 3)
- Comparaison des différentes approches

### Structure du code

```
examen_ml_calculatrice.py          # Programme principal
REPONSES_EXAMEN_ML.md              # Réponses théoriques détaillées
README_EXAMEN_ML.md                # Ce fichier
```

## Résultats attendus

### Partie 1 - Création des données
- 1000 exemples générés
- 70% pour l'entraînement, 30% pour le test

### Partie 2 - Addition
- **Régression linéaire simple** → R² = 1.0 (parfait)
- Coefficients: w₁=1, w₂=1, b=0

### Partie 3 - Multiplication
- **Régression linéaire** → R² ≈ 0 (échec)
- **Ridge** → R² ≈ 0 (échec)
- **KernelRidge (poly-2)** → R² = 1.0 (succès)
- **Plongement [a,b,a×b]** → R² = 1.0 (succès)

## Points clés

1. **Addition = problème linéaire** → régression linéaire suffisante
2. **Multiplication = problème non-linéaire** → nécessite transformation des features
3. **Plongement explicite** Φ(a,b) = [a, b, a×b] rend le problème trivial
4. **Ridge ne suffit pas** car elle reste linéaire (régularisation ≠ non-linéarité)

## Notes

- Le code utilise `np.random.seed(42)` pour la reproductibilité
- Toutes les questions de l'examen sont traitées dans l'ordre
- Les réponses théoriques sont dans `REPONSES_EXAMEN_ML.md`
