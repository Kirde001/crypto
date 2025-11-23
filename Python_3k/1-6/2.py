import sys

def extended_gcd(a, b):
    if a == 0:
        return b, 0, 1
    else:
        g, y, x = extended_gcd(b % a, a)
        return g, x - (b // a) * y, y

def mod_inverse(a, m):
    g, x, y = extended_gcd(a, m)
    if g != 1:
        return None
    else:
        return (x % m + m) % m

class Poly:
    def __init__(self, coeffs):
        self.coeffs = coeffs

    def mul_scalar(self, s, m):
        return Poly([(c * s) % m for c in self.coeffs])

    def mul_poly(self, other, m):
        res = [0] * (len(self.coeffs) + len(other.coeffs) - 1)
        for i in range(len(self.coeffs)):
            for j in range(len(other.coeffs)):
                res[i+j] = (res[i+j] + self.coeffs[i] * other.coeffs[j]) 
        return Poly([c % m for c in res]) 

    def __str__(self):
        parts = []
        deg = len(self.coeffs) - 1
        for i, c in enumerate(self.coeffs):
            power = deg - i
            if c == 0: continue
            
     
            if i == 0: 
                term = f"{c}" if c != 1 or power == 0 else ""
            else:
                term = f"+ {c}" 
            

            if power == 0:
                if i == 0 and c == 1: term = "1" 
            elif power == 1:
                term += "x"
            else:
                term += f"x^{power}"
            parts.append(term)
        return " ".join(parts)


def solve_manual_style():
    print("=== Калькулятор восстановления секрета (как на фото) ===")
    
    try:
        P = int(input("Введите модуль P (например, 13): "))
        N = int(input("Введите количество точек (например, 3): "))
        
        points_x = []
        points_y = []
        
        print(f"Введите точки (X Y):")
        for i in range(N):
            line = input(f"Точка {i+1}: ").replace(',', ' ').split()
            points_x.append(int(line[0]))
            points_y.append(int(line[1]))
            
    except ValueError:
        print("Ошибка ввода чисел.")
        return

    print("\n" + "="*60)
    print(f"РЕШЕНИЕ (Модуль m = {P})")
    print(f"Точки: " + ", ".join([f"x{i+1}={x}" for i, x in enumerate(points_x)]))
    print("="*60)

    basis_polys = [] 

    for i in range(N):
        xi = points_x[i]
        print(f"\n---> Вычисляем l_{i+1}(x) для x_{i+1}={xi}:")
        
        numerator_poly = Poly([1]) 
        denominator_val = 1
        numerator_str = []
        denominator_str = []
        
        for j in range(N):
            if i == j: continue
            xj = points_x[j]
            

            term_poly = Poly([1, -xj]) 
            numerator_poly = numerator_poly.mul_poly(term_poly, 999999) 
            numerator_str.append(f"(x - {xj})")
            
            diff = xi - xj
            denominator_val = denominator_val * diff
            denominator_str.append(f"({xi}-{xj})")

        numerator_poly_mod = Poly([(c % P) for c in numerator_poly.coeffs])
        
        denom_mod = denominator_val % P
        denom_inv = mod_inverse(denom_mod, P)
        
        if denom_inv is None:
            print("ОШИБКА: Обратного элемента не существует!")
            return

        print(f"Числитель (раскрыли скобки): {numerator_poly.coeffs}") 

        poly_text = []
        deg = len(numerator_poly.coeffs) - 1
        for idx, c in enumerate(numerator_poly.coeffs):
            pwr = deg - idx
            if c == 0: continue
            sign = "+" if c >= 0 and idx > 0 else ""
            term = f"{sign}{c}"
            if pwr == 1: term += "x"
            if pwr > 1: term += f"x^{pwr}"
            poly_text.append(term)
        print(f"l_{i+1}(x) = ({' '.join(poly_text)}) / {denominator_val}")
        
        print(f"Обратный к знаменателю: {denominator_val} mod {P} -> {denom_mod}^(-1) = {denom_inv}")
        

        final_l = numerator_poly_mod.mul_scalar(denom_inv, P)
        basis_polys.append(final_l)
        
        print(f"Итог l_{i+1}(x) = {denom_inv} * ({' '.join(poly_text)}) mod {P}")
        print(f"l_{i+1}(x) = {final_l}")

    print("\n" + "-"*40)
    print("Составляем F(x) = sum( y_i * l_i(x) )")
    parts_str = []
    for i in range(N):
        parts_str.append(f"{points_y[i]}*l_{i+1}(x)")
    print(f"F(x) = {' + '.join(parts_str)}")

    weighted_polys = []
    for i in range(N):
        wp = basis_polys[i].mul_scalar(points_y[i], P)
        weighted_polys.append(wp)
        print(f"Слагаемое {i+1}: {wp}") 

    degree = N - 1
    final_coeffs = [0] * (degree + 1)
    
    print("\nПодсчет коэффициентов (снизу вверх, как в тетради):")
    
    coeff_names = []
    if degree == 2: coeff_names = ["a2 (при x^2)", "a1 (при x)", "M (свободный член)"]
    else: coeff_names = [f"a{degree-i}" for i in range(degree+1)]

    for i in range(degree + 1):
        terms = []
        val_sum = 0
        for j in range(N):
            val = weighted_polys[j].coeffs[i]
            raw_val = points_y[j] * basis_polys[j].coeffs[i] 
            terms.append(f"{points_y[j]}*{basis_polys[j].coeffs[i]}")
            val_sum += val
        
        final_val = val_sum % P
        print(f"{coeff_names[i]}: {' + '.join(terms)} = {val_sum} = {final_val} mod {P}")
        final_coeffs[i] = final_val

    final_poly = Poly(final_coeffs)
    print("\n" + "#"*40)
    print(f"F(x) = {final_poly} mod {P}")
    print(f"Секрет (M) = {final_coeffs[-1]}")
    print("#"*40)

if __name__ == "__main__":
    solve_manual_style()