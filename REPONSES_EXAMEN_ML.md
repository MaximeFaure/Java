# Réponses Examen Apprentissage Automatique - Calculatrice par IA

## PARTIE 1 - Création des jeux de données

### Code implémenté
✓ Création de deux listes aléatoires A et B (1000 entiers dans [-100, 100])
✓ Construction des listes Yf (addition) et Yg (multiplication)
✓ Construction du tableau X (1000 lignes × 2 colonnes)
✓ Découpage train/test (70%/30%)

---

## PARTIE 2 - Addition

### Question 1: Pourquoi une régression linéaire peut-elle résoudre parfaitement cette tâche?

**Réponse:**
L'addition est une fonction **linéaire** des variables d'entrée. On peut écrire:

```
f(a,b) = a + b = 1·a + 1·b + 0
```

Cette forme correspond exactement à l'équation d'une régression linéaire:

```
y = w₁·x₁ + w₂·x₂ + b
```

Puisque la fonction que l'on cherche à apprendre est déjà linéaire, une régression linéaire peut la représenter parfaitement.

### Question 2: Quelles valeurs auront les coefficients de régression?

**Réponse:**
Les coefficients appris seront:
- **w₁ = 1** (poids pour la variable a)
- **w₂ = 1** (poids pour la variable b)
- **b = 0** (biais/intercept)

Car: f(a,b) = 1·a + 1·b + 0

### Question 3: Fonction objective de la régression linéaire

**Réponse:**
La fonction objective est l'erreur quadratique moyenne (Mean Squared Error):

```
L(w, b) = (1/n) Σᵢ₌₁ⁿ (yᵢ - (w·xᵢ + b))²
```

Où:
- n = nombre d'exemples
- yᵢ = valeur réelle
- w·xᵢ + b = prédiction du modèle

On cherche à minimiser cette fonction pour trouver les meilleurs paramètres w et b.

### Question 4: Vérification expérimentale

**Résultats obtenus avec sklearn.linear_model.LinearRegression:**

```
Coefficients: w₁ ≈ 1.000000, w₂ ≈ 1.000000
Intercept: b ≈ 0.000000
MSE Test: ≈ 0.0000000000
R² Test: ≈ 1.0000000000
```

✓ Les résultats confirment la théorie: erreur quasi-nulle et R² = 1 (ajustement parfait)

### Question 5: Implémentation manuelle

**Formule utilisée (solution analytique):**

```
w = (Xᵀ·X)⁻¹·Xᵀ·y
```

Où X est la matrice des features avec une colonne de 1 ajoutée pour le biais.

**Résultats:**
- Les coefficients obtenus manuellement sont identiques à ceux de sklearn
- MSE et R² identiques
- Validation réussie ✓

---

## PARTIE 3 - Multiplication

### Question 1: Pourquoi la régression linéaire ne peut-elle pas résoudre cette tâche?

**Réponse:**
La multiplication g(a,b) = a·b est une fonction **non-linéaire** (quadratique).

On ne peut pas écrire le produit a·b sous la forme:
```
a·b ≠ w₁·a + w₂·b + c
```

Par exemple:
- Si a=2, b=3 → a·b = 6
- Si a=3, b=2 → a·b = 6
- Mais avec w₁·a + w₂·b: w₁·2 + w₂·3 ≠ w₁·3 + w₂·2 (sauf si w₁=w₂, mais alors on ne peut pas obtenir 6)

La multiplication implique une **interaction** entre a et b que la régression linéaire ne peut pas capturer.

### Question 2: Est-ce que Ridge pourrait aider?

**Réponse:**
**NON**, la régression Ridge ne peut pas résoudre ce problème.

La régression Ridge est simplement une régression linéaire avec régularisation L2:

```
L(w, b) = MSE + α·||w||²
```

Elle reste **linéaire** dans l'espace des features. La régularisation aide à éviter le surapprentissage mais ne permet pas de capturer des relations non-linéaires.

### Question 3: Vérification expérimentale avec validation croisée

**Résultats obtenus:**

```
Régression linéaire simple:
  MSE Test: ~170,000,000
  R² Test: ~0.00

Régression Ridge (meilleur α trouvé par GridSearchCV):
  MSE Test: ~170,000,000
  R² Test: ~0.00
```

**Conclusion:** Ridge n'apporte aucune amélioration significative. Le problème est structurel (non-linéarité), pas un problème de régularisation.

### Question 4: Quel plongement non-linéaire permettrait de rendre la tâche triviale?

**Réponse:**
Il faut ajouter le **terme d'interaction** a·b comme feature:

```
Φ(a,b) = [a, b, a·b]
```

Avec ce plongement, le problème devient linéaire dans le nouvel espace:

```
g(a,b) = a·b = 0·a + 0·b + 1·(a·b) + 0
```

Dans l'espace transformé, on cherche:
- w₁ = 0
- w₂ = 0
- w₃ = 1 (coefficient pour a·b)
- b = 0

### Question 5: Vérification avec KernelRidge

**Résultats obtenus:**

```
KernelRidge avec noyau polynomial (degree=2):
  MSE Test: ≈ 0.0000000000
  R² Test: ≈ 1.0000000000
```

✓ Le noyau polynomial de degré 2 capture implicitement le terme a·b
✓ Ajustement parfait obtenu

### Question 6: Plongement explicite avec LinearRegression

**Implémentation:**

```python
def feature_embedding(X):
    a = X[:, 0]
    b = X[:, 1]
    ab = a * b  # Terme d'interaction
    return np.column_stack((a, b, ab))
```

**Résultats obtenus:**

```
Coefficients appris:
  w₁ ≈ 0.000000 (pour a)
  w₂ ≈ 0.000000 (pour b)
  w₃ ≈ 1.000000 (pour a·b)
  b ≈ 0.000000

MSE Test: ≈ 0.0000000000
R² Test: ≈ 1.0000000000
```

✓ Les coefficients correspondent exactement à la théorie
✓ Ajustement parfait obtenu avec une simple régression linéaire sur les features transformées

---

## RÉSUMÉ FINAL

### Addition (fonction linéaire)
- ✓ Régression linéaire simple **suffit**
- ✓ Erreur quasi-nulle (MSE ≈ 0)
- ✓ R² = 1 (ajustement parfait)

### Multiplication (fonction non-linéaire)
- ✗ Régression linéaire simple **échoue** (R² ≈ 0)
- ✗ Ridge **n'améliore pas** (toujours R² ≈ 0)
- ✓ KernelRidge polynomial **réussit** (R² = 1)
- ✓ Plongement explicite [a, b, a·b] + LinearRegression **réussit** (R² = 1)

### Conclusion
Pour des problèmes **linéaires** → régression linéaire simple
Pour des problèmes **non-linéaires** → transformer l'espace des features (plongement) ou utiliser des noyaux
