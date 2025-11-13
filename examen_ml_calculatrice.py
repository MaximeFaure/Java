import numpy as np
from sklearn.linear_model import LinearRegression, Ridge
from sklearn.kernel_ridge import KernelRidge
from sklearn.model_selection import train_test_split, GridSearchCV
from sklearn.metrics import mean_squared_error, r2_score

# PARTIE 1 - Jeux de données
print("PARTIE 1 - Création des données")

# 1 et 2
np.random.seed(42)
A = np.random.randint(-100, 101, size=1000)
B = np.random.randint(-100, 101, size=1000)

Yf = A + B  # addition
Yg = A * B  # multiplication

# 3
X = np.column_stack((A, B))

# 4
X_train, X_test, Yf_train, Yf_test, Yg_train, Yg_test = train_test_split(
    X, Yf, Yg, test_size=0.3, random_state=42)

print(f"Train: {len(X_train)}, Test: {len(X_test)}")


# PARTIE 2 - Addition
print("\nPARTIE 2 - Addition")

# Q4 - sklearn
model_f = LinearRegression()
model_f.fit(X_train, Yf_train)

print(f"Coefs: {model_f.coef_}, Intercept: {model_f.intercept_}")

Yf_pred = model_f.predict(X_test)
print(f"MSE: {mean_squared_error(Yf_test, Yf_pred):.6f}")
print(f"R2: {r2_score(Yf_test, Yf_pred):.6f}")

# Q5 - implémentation manuelle
def train_linear_regression(X, y):
    # ajouter colonne de 1 pour biais
    X_bias = np.column_stack((X, np.ones(X.shape[0])))
    # formule w = (X^T X)^-1 X^T y
    w = np.linalg.inv(X_bias.T @ X_bias) @ X_bias.T @ y
    return w[:-1], w[-1]

def predict_linear_regression(X, coef, intercept):
    return X @ coef + intercept

coef, intercept = train_linear_regression(X_train, Yf_train)
print(f"\nManuel - Coefs: {coef}, Intercept: {intercept}")

Yf_pred_manual = predict_linear_regression(X_test, coef, intercept)
print(f"MSE: {mean_squared_error(Yf_test, Yf_pred_manual):.6f}")
print(f"R2: {r2_score(Yf_test, Yf_pred_manual):.6f}")


# PARTIE 3 - Multiplication
print("\nPARTIE 3 - Multiplication")

# Q3 - Ridge
model_linear = LinearRegression()
model_linear.fit(X_train, Yg_train)
Yg_pred_linear = model_linear.predict(X_test)
print(f"Linear - R2: {r2_score(Yg_test, Yg_pred_linear):.6f}")

alphas = [0.001, 0.01, 0.1, 1, 10, 100, 1000]
grid = GridSearchCV(Ridge(), {'alpha': alphas}, cv=5)
grid.fit(X_train, Yg_train)
best_ridge = grid.best_estimator_

Yg_pred_ridge = best_ridge.predict(X_test)
print(f"Ridge (alpha={grid.best_params_['alpha']}) - R2: {r2_score(Yg_test, Yg_pred_ridge):.6f}")

# Q5 - KernelRidge
kernel_model = KernelRidge(kernel='poly', degree=2, alpha=0.001)
kernel_model.fit(X_train, Yg_train)
Yg_pred_kernel = kernel_model.predict(X_test)
print(f"KernelRidge - R2: {r2_score(Yg_test, Yg_pred_kernel):.6f}")

# Q6 - Plongement explicite
def feature_embedding(X):
    a = X[:, 0]
    b = X[:, 1]
    return np.column_stack((a, b, a * b))

X_train_emb = feature_embedding(X_train)
X_test_emb = feature_embedding(X_test)

model_emb = LinearRegression()
model_emb.fit(X_train_emb, Yg_train)
print(f"\nPlongement - Coefs: {model_emb.coef_}, Intercept: {model_emb.intercept_}")

Yg_pred_emb = model_emb.predict(X_test_emb)
print(f"R2: {r2_score(Yg_test, Yg_pred_emb):.6f}")
