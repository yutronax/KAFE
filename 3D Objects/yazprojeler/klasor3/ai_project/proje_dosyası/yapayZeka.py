# Regression ve Classification modelleri nasıl çalışır?

def linear_regression(x):
    # Doğrusal regresyon: y = mx + b
    m = 2.5
    b = 7
    return m * x + b

def polynomial_regression(x):
    # y = ax^2 + bx + c
    a, b, c = 1, -2, 3
    return a * x**2 + b * x + c

def logistic_regression(x):
    # Sınıflandırma: Sigmoid fonksiyonuyla çalışır
    import math
    z = 2.5 * x - 4
    return 1 / (1 + math.exp(-z))

def decision_tree_classifier(x):
    # Basit karar kuralları ile sınıflandırma yapar
    if x < 50:
        return "Düşük"
    elif x < 80:
        return "Orta"
    else:
        return "Yüksek"

def knn_classifier(x, data, labels, k=3):
    # En yakın komşulara bakarak sınıf tahmini
    from math import sqrt
    distances = [(sqrt((x - d)**2), l) for d, l in zip(data, labels)]
    distances.sort()
    top_k = [label for _, label in distances[:k]]
    return max(set(top_k), key=top_k.count)

# Örnek kullanımlar:
print("Linear Regression (x=5):", linear_regression(5))
print("Polynomial Regression (x=2):", polynomial_regression(2))
print("Logistic Regression (x=3):", logistic_regression(3))
print("Decision Tree (x=75):", decision_tree_classifier(75))
print("KNN (x=7):", knn_classifier(7, [5, 8, 12], ['A', 'B', 'B']))
