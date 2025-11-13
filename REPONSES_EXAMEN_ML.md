# Réponses Examen ML - Calculatrice par IA

## PARTIE 2 - Addition

**Q1: Pourquoi une régression linéaire peut résoudre parfaitement cette tâche?**

L'addition est linéaire: f(a,b) = a + b = 1·a + 1·b + 0
C'est exactement la forme d'une régression linéaire: y = w₁x₁ + w₂x₂ + b

**Q2: Valeurs des coefficients?**

w₁ = 1, w₂ = 1, b = 0

**Q3: Fonction objective**

MSE: L(w,b) = (1/n) Σ(yᵢ - (w·xᵢ + b))²

**Q4: Résultats sklearn**

Coefs ≈ [1, 1], Intercept ≈ 0, R² = 1.0

**Q5: Implémentation manuelle**

Formule: w = (X^T X)^-1 X^T y
Résultats identiques à sklearn

## PARTIE 3 - Multiplication

**Q1: Pourquoi la régression linéaire échoue?**

La multiplication est non-linéaire: a·b ≠ w₁a + w₂b + c
C'est une fonction quadratique avec interaction entre a et b.

**Q2: Ridge peut-elle aider?**

Non, Ridge reste linéaire (juste de la régularisation L2).

**Q3: Résultats**

Linear: R² ≈ 0
Ridge: R² ≈ 0 (pas d'amélioration)

**Q4: Plongement nécessaire?**

Il faut ajouter le terme d'interaction: Φ(a,b) = [a, b, a·b]
Alors: g(a,b) = 0·a + 0·b + 1·(a·b) + 0

**Q5: KernelRidge**

Noyau polynomial degree=2 → R² = 1.0 (capture implicitement a·b)

**Q6: Plongement explicite**

Features transformées: [a, b, a·b]
Régression linéaire → Coefs: [0, 0, 1], R² = 1.0
