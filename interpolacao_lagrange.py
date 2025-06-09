import sympy as sp
import numpy as np
import matplotlib.pyplot as plt


def calculate_divided_differences(points):
    n = len(points)
    x_coords = [p[0] for p in points]
    # A primeira coluna da tabela são os valores de y
    table = [[p[1] for p in points]]

    for j in range(1, n):
        prev_col = table[-1]
        new_col = []
        # Cada nova coluna é calculada a partir da anterior
        for i in range(len(prev_col) - 1):
            numerator = prev_col[i+1] - prev_col[i]
            denominator = x_coords[i+j] - x_coords[i]
            divided_diff = numerator / denominator
            new_col.append(divided_diff)
        table.append(new_col)

    # Os coeficientes são o primeiro elemento de cada coluna
    newton_coeffs = [col[0] for col in table]
    return newton_coeffs


def newton_coefficients(points):
    x = sp.Symbol('x')
    x_coords = [p[0] for p in points]
    
    # 1. Obter os coeficientes da forma de Newton (a0, a1, a2, ...)
    # P(x) = a0 + a1(x-x0) + a2(x-x0)(x-x1) + ...
    newton_coeffs = calculate_divided_differences(points)

    # 2. Construir a expressão simbólica do polinômio
    polynomial_expr = 0
    term_product = 1  # Representa os produtos (x-x0)(x-x1)...
    
    for i in range(len(newton_coeffs)):
        polynomial_expr += newton_coeffs[i] * term_product
        # Prepara o termo para a próxima iteração
        term_product *= (x - x_coords[i])

    # 3. Expandir a expressão para a forma c0 + c1*x + c2*x^2 + ...
    expanded_poly = sp.expand(polynomial_expr)
    poly_obj = sp.Poly(expanded_poly, x)
    coeffs_high_to_low = poly_obj.all_coeffs()
    
    # Inverte para que o índice corresponda à potência
    coeffs_low_to_high = coeffs_high_to_low[::-1]
    
    return [float(c) for c in coeffs_low_to_high]



def lagrange_coefficients(points):

    x = sp.Symbol('x')
    polynomial_expr = 0
    
    
    for i, (xi, yi) in enumerate(points):
        li_expr = 1
        for j, (xj, _) in enumerate(points):
            if i != j:
                li_expr *= (x - xj) / (xi - xj)
        polynomial_expr += yi * li_expr
        
    expanded_poly = sp.expand(polynomial_expr)
    poly_obj = sp.Poly(expanded_poly, x)
    coeffs_high_to_low = poly_obj.all_coeffs()
    coeffs_low_to_high = coeffs_high_to_low[::-1]
    return [float(c) for c in coeffs_low_to_high]



metodo = 0
if(metodo == 0):
    metodo = int(input("[1] metodo de lagrange, [2] para metodo de newton: "))


data_points = []
grau = 0
grau = int(input("digite o grau do polinomio: "))

if(grau!=0):
    N = grau

for i in range(N+1):
    x_i  = float(input(f"x_{i}: "))
    y_i  = float(input(f"y_{i}: "))
    data_points.append((x_i, y_i))

x_novo = float(input(f"digite o valor (x) que deseja aproximar: "))



# Encontre os coeficientes do polinômio interpolador
if(metodo == 1):
    print("Calculando polinomio pelo metodo de lagrange")
    factors = lagrange_coefficients(data_points)

if(metodo == 2):
    factors = newton_coefficients(data_points)

print(f"Pontos de dados: {data_points}")
print("-" * 30)
print(f"Coeficientes (fatores) do polinômio [c0, c1, c2, ...]:")
print(factors)
print("-" * 30)




x_sym = sp.Symbol('x')
reconstructed_poly = sum(c * x_sym**i for i, c in enumerate(factors))
print("Polinômio reconstruído a partir dos coeficientes:")
sp.pprint(reconstructed_poly, use_unicode=True)
# Para plotar, usamos a função de polinômio do numpy
# Ela espera os coeficientes da maior potência para a menor, então invertemos a lista
coeffs_for_numpy = factors[::-1]
p = np.poly1d(coeffs_for_numpy)


x_data, y_data = zip(*data_points)


x_range = np.linspace(min(x_data) - 1, max(x_data) + 1, 400)
y_range = p(x_range)

print(f"f({x_novo}) = {p(x_novo)}")


plt.figure(figsize=(10, 6))
plt.plot(x_range, y_range, label='Polinômio Interpolador (a partir dos coeficientes)')
plt.plot(x_data, y_data, 'o', label='Pontos de Dados', markersize=8)
plt.title('Interpolação de Lagrange')
plt.xlabel('x')
plt.ylabel('y')
plt.legend()
plt.grid(True)
plt.show()
