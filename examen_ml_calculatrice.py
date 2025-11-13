"""
Examen Apprentissage automatique - Calculatrice par IA
Création de modèles de régression pour l'addition et la multiplication
"""

import numpy as np
from sklearn.linear_model import LinearRegression, Ridge
from sklearn.kernel_ridge import KernelRidge
from sklearn.model_selection import train_test_split, GridSearchCV
from sklearn.metrics import mean_squared_error, r2_score
import pickle

print("="*60)
print("EXAMEN ML - CALCULATRICE PAR APPRENTISSAGE ARTIFICIEL")
print("="*60)

# ============================================================================
# PARTIE 1 - CRÉATION DES JEUX DE DONNÉES
# ============================================================================
print("\n[PARTIE 1] Création des jeux de données")
print("-"*60)

# 1. Construire deux listes aléatoires A et B de 1000 entiers dans [-100, 100]
np.random.seed(42)  # Pour la reproductibilité
A = np.random.randint(-100, 101, size=1000)
B = np.random.randint(-100, 101, size=1000)

print(f"Liste A créée: {len(A)} entiers")
print(f"Liste B créée: {len(B)} entiers")
print(f"Exemple: A[0]={A[0]}, B[0]={B[0]}")

# 2. Construire les listes Yf et Yg
Yf = A + B  # Addition
Yg = A * B  # Multiplication

print(f"\nYf (addition) créé: {len(Yf)} valeurs")
print(f"Yg (multiplication) créé: {len(Yg)} valeurs")
print(f"Exemple: {A[0]} + {B[0]} = {Yf[0]}")
print(f"Exemple: {A[0]} * {B[0]} = {Yg[0]}")

# 3. Construire le tableau X de 1000 lignes et 2 colonnes
X = np.column_stack((A, B))

print(f"\nTableau X créé: {X.shape} (lignes x colonnes)")
print(f"Première ligne X[0]: {X[0]}")

# 4. Découper les jeux de données (30% pour l'évaluation)
X_train, X_test, Yf_train, Yf_test, Yg_train, Yg_test = train_test_split(
    X, Yf, Yg, test_size=0.3, random_state=42
)

print(f"\nDécoupage effectué:")
print(f"  Training set: {X_train.shape[0]} exemples")
print(f"  Test set: {X_test.shape[0]} exemples")

# Sauvegarder les données (optionnel)
# with open("data-2024.pkl", "wb") as f:
#     pickle.dump((X_train, X_test, Yf_train, Yf_test, Yg_train, Yg_test), f)


# ============================================================================
# PARTIE 2 - ADDITION
# ============================================================================
print("\n" + "="*60)
print("[PARTIE 2] Addition avec régression linéaire")
print("="*60)

# Question 1: Pourquoi une régression linéaire peut résoudre parfaitement cette tâche?
print("\nQ1: Pourquoi la régression linéaire fonctionne-t-elle parfaitement?")
print("Réponse: L'addition est une fonction LINÉAIRE des variables.")
print("         f(a,b) = a + b = 1*a + 1*b + 0")
print("         C'est exactement de la forme: y = w1*x1 + w2*x2 + b")

# Question 2: Quelles valeurs auront les coefficients?
print("\nQ2: Valeurs attendues des coefficients:")
print("    w1 = 1, w2 = 1, b = 0")

# Question 3: Fonction objective de la régression linéaire
print("\nQ3: Fonction objective de la régression linéaire:")
print("    L(w, b) = (1/n) * Σ(yi - (w·xi + b))²")
print("    On minimise l'erreur quadratique moyenne (MSE)")

# Question 4: Vérification expérimentale avec sklearn
print("\nQ4: Vérification expérimentale avec sklearn")
print("-"*60)

model_f = LinearRegression()
model_f.fit(X_train, Yf_train)

print(f"Coefficients appris: w1={model_f.coef_[0]:.6f}, w2={model_f.coef_[1]:.6f}")
print(f"Intercept appris: b={model_f.intercept_:.6f}")

Yf_pred_train = model_f.predict(X_train)
Yf_pred_test = model_f.predict(X_test)

mse_train = mean_squared_error(Yf_train, Yf_pred_train)
mse_test = mean_squared_error(Yf_test, Yf_pred_test)
r2_train = r2_score(Yf_train, Yf_pred_train)
r2_test = r2_score(Yf_test, Yf_pred_test)

print(f"\nPerformances:")
print(f"  MSE Train: {mse_train:.10f}")
print(f"  MSE Test: {mse_test:.10f}")
print(f"  R² Train: {r2_train:.10f}")
print(f"  R² Test: {r2_test:.10f}")

# Test manuel
test_a, test_b = 25, 17
test_pred = model_f.predict([[test_a, test_b]])[0]
test_real = test_a + test_b
print(f"\nTest manuel: {test_a} + {test_b} = {test_pred:.2f} (attendu: {test_real})")


# Question 5: Coder la régression linéaire sans sklearn
print("\nQ5: Implémentation manuelle de la régression linéaire")
print("-"*60)

def train_linear_regression(X, y):
    """
    Entraîne un modèle de régression linéaire en utilisant la solution analytique.
    Formule: w = (X^T X)^-1 X^T y
    """
    # Ajouter une colonne de 1 pour le biais
    X_bias = np.column_stack((X, np.ones(X.shape[0])))

    # Solution analytique: w = (X^T X)^-1 X^T y
    w = np.linalg.inv(X_bias.T @ X_bias) @ X_bias.T @ y

    # Séparer les coefficients et le biais
    coef = w[:-1]
    intercept = w[-1]

    return coef, intercept

def predict_linear_regression(X, coef, intercept):
    """
    Fait des prédictions avec le modèle de régression linéaire.
    """
    return X @ coef + intercept

# Entraînement manuel
coef_manual, intercept_manual = train_linear_regression(X_train, Yf_train)

print(f"Coefficients appris (manuel): w1={coef_manual[0]:.6f}, w2={coef_manual[1]:.6f}")
print(f"Intercept appris (manuel): b={intercept_manual:.6f}")

# Prédictions manuelles
Yf_pred_manual = predict_linear_regression(X_test, coef_manual, intercept_manual)
mse_manual = mean_squared_error(Yf_test, Yf_pred_manual)
r2_manual = r2_score(Yf_test, Yf_pred_manual)

print(f"\nPerformances (implémentation manuelle):")
print(f"  MSE Test: {mse_manual:.10f}")
print(f"  R² Test: {r2_manual:.10f}")

# Test manuel
test_pred_manual = predict_linear_regression(np.array([[test_a, test_b]]), coef_manual, intercept_manual)[0]
print(f"\nTest manuel: {test_a} + {test_b} = {test_pred_manual:.2f} (attendu: {test_real})")


# ============================================================================
# PARTIE 3 - MULTIPLICATION
# ============================================================================
print("\n" + "="*60)
print("[PARTIE 3] Multiplication avec régression non-linéaire")
print("="*60)

# Question 1: Pourquoi la régression linéaire ne peut pas résoudre cette tâche?
print("\nQ1: Pourquoi la régression linéaire simple échoue?")
print("Réponse: La multiplication g(a,b) = a*b n'est PAS linéaire.")
print("         On ne peut pas écrire a*b = w1*a + w2*b + c")
print("         C'est une fonction QUADRATIQUE (interaction entre a et b)")

# Question 2: Est-ce que Ridge pourrait aider?
print("\nQ2: Est-ce que la régression Ridge pourrait aider?")
print("Réponse: NON. Ridge ajoute seulement une régularisation L2,")
print("         mais reste une régression LINÉAIRE.")
print("         Elle ne peut pas capturer l'interaction a*b.")

# Question 3: Vérification expérimentale avec Ridge
print("\nQ3: Vérification expérimentale avec Ridge")
print("-"*60)

# Test avec régression linéaire simple
model_g_linear = LinearRegression()
model_g_linear.fit(X_train, Yg_train)
Yg_pred_linear = model_g_linear.predict(X_test)
mse_linear = mean_squared_error(Yg_test, Yg_pred_linear)
r2_linear = r2_score(Yg_test, Yg_pred_linear)

print(f"Régression linéaire simple:")
print(f"  MSE Test: {mse_linear:.2f}")
print(f"  R² Test: {r2_linear:.6f}")

# Validation croisée pour trouver le meilleur alpha
alphas = [0.001, 0.01, 0.1, 1, 10, 100, 1000]
ridge_model = Ridge()
grid_search = GridSearchCV(ridge_model, {'alpha': alphas}, cv=5, scoring='r2')
grid_search.fit(X_train, Yg_train)

best_alpha = grid_search.best_params_['alpha']
best_ridge = grid_search.best_estimator_

Yg_pred_ridge = best_ridge.predict(X_test)
mse_ridge = mean_squared_error(Yg_test, Yg_pred_ridge)
r2_ridge = r2_score(Yg_test, Yg_pred_ridge)

print(f"\nRégression Ridge (meilleur alpha={best_alpha}):")
print(f"  MSE Test: {mse_ridge:.2f}")
print(f"  R² Test: {r2_ridge:.6f}")
print(f"\nConclusion: Ridge n'améliore pas significativement les résultats.")

# Question 4: Quel plongement non-linéaire?
print("\nQ4: Quel plongement non-linéaire rend la tâche triviale?")
print("Réponse: Il faut ajouter le TERME D'INTERACTION a*b comme feature.")
print("         Φ(a,b) = [a, b, a*b]")
print("         Alors: g(a,b) = 0*a + 0*b + 1*(a*b) + 0")

# Question 5: Vérification avec KernelRidge
print("\nQ5: Vérification avec KernelRidge")
print("-"*60)

# Test avec noyau polynomial (degree=2 pour capturer a*b)
kernel_ridge = KernelRidge(kernel='poly', degree=2, alpha=0.001, coef0=1)
kernel_ridge.fit(X_train, Yg_train)

Yg_pred_kernel = kernel_ridge.predict(X_test)
mse_kernel = mean_squared_error(Yg_test, Yg_pred_kernel)
r2_kernel = r2_score(Yg_test, Yg_pred_kernel)

print(f"KernelRidge (noyau polynomial degree=2):")
print(f"  MSE Test: {mse_kernel:.10f}")
print(f"  R² Test: {r2_kernel:.10f}")

# Test manuel
test_pred_kernel = kernel_ridge.predict([[test_a, test_b]])[0]
test_real_mult = test_a * test_b
print(f"\nTest manuel: {test_a} * {test_b} = {test_pred_kernel:.2f} (attendu: {test_real_mult})")

# Question 6: Plongement explicite avec LinearRegression
print("\nQ6: Plongement explicite + LinearRegression")
print("-"*60)

def feature_embedding(X):
    """
    Crée un plongement non-linéaire explicite.
    Φ(a,b) = [a, b, a*b]
    """
    a = X[:, 0]
    b = X[:, 1]
    ab = a * b  # Terme d'interaction

    return np.column_stack((a, b, ab))

# Appliquer le plongement
X_train_embedded = feature_embedding(X_train)
X_test_embedded = feature_embedding(X_test)

print(f"Features originales: {X_train.shape[1]} dimensions")
print(f"Features avec plongement: {X_train_embedded.shape[1]} dimensions")
print(f"Exemple: [{test_a}, {test_b}] → [{test_a}, {test_b}, {test_a*test_b}]")

# Entraîner le modèle linéaire sur les features transformées
model_g_embedded = LinearRegression()
model_g_embedded.fit(X_train_embedded, Yg_train)

print(f"\nCoefficients appris: w1={model_g_embedded.coef_[0]:.6f}, "
      f"w2={model_g_embedded.coef_[1]:.6f}, w3={model_g_embedded.coef_[2]:.6f}")
print(f"Intercept: b={model_g_embedded.intercept_:.6f}")
print(f"\nAttendus: w1=0, w2=0, w3=1, b=0")

Yg_pred_embedded = model_g_embedded.predict(X_test_embedded)
mse_embedded = mean_squared_error(Yg_test, Yg_pred_embedded)
r2_embedded = r2_score(Yg_test, Yg_pred_embedded)

print(f"\nPerformances avec plongement explicite:")
print(f"  MSE Test: {mse_embedded:.10f}")
print(f"  R² Test: {r2_embedded:.10f}")

# Test manuel
test_embedded = feature_embedding(np.array([[test_a, test_b]]))
test_pred_embedded = model_g_embedded.predict(test_embedded)[0]
print(f"\nTest manuel: {test_a} * {test_b} = {test_pred_embedded:.2f} (attendu: {test_real_mult})")


# ============================================================================
# RÉSUMÉ FINAL
# ============================================================================
print("\n" + "="*60)
print("RÉSUMÉ FINAL")
print("="*60)

print("\n[ADDITION]")
print(f"  Régression linéaire simple: R²={r2_test:.10f}, MSE={mse_test:.10f}")
print(f"  → Fonctionne PARFAITEMENT (problème linéaire)")

print("\n[MULTIPLICATION]")
print(f"  Régression linéaire simple: R²={r2_linear:.6f}, MSE={mse_linear:.2f}")
print(f"  Régression Ridge: R²={r2_ridge:.6f}, MSE={mse_ridge:.2f}")
print(f"  KernelRidge (poly-2): R²={r2_kernel:.10f}, MSE={mse_kernel:.10f}")
print(f"  Plongement explicite: R²={r2_embedded:.10f}, MSE={mse_embedded:.10f}")
print(f"  → Nécessite un plongement NON-LINÉAIRE pour capturer a*b")

print("\n" + "="*60)
print("EXAMEN TERMINÉ")
print("="*60)
