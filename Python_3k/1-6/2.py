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

    def mul_poly(self, other):
        res = [0] * (len(self.coeffs) + len(other.coeffs) - 1)
        for i in range(len(self.coeffs)):
            for j in range(len(other.coeffs)):
                res[i+j] += self.coeffs[i] * other.coeffs[j]
        return Poly(res)

    def apply_mod(self, p):
        return Poly([(c % p) for c in self.coeffs])

    def __str__(self):
        if not self.coeffs: return "0"
        parts = []
        deg = len(self.coeffs) - 1
        for i, c in enumerate(self.coeffs):
            if c == 0: continue
            power = deg - i
            
            sign = ""
            val = c
            if i > 0:
                sign = "+ " if c >= 0 else "- "
                val = abs(c)
            else:
                if c < 0: 
                    sign = "-"
                    val = abs(c)

            if val == 1 and power != 0:
                val_str = ""
            else:
                val_str = str(val)

            var_str = ""
            if power == 1: var_str = "x"
            elif power > 1: var_str = f"x^{power}"

            parts.append(f"{sign}{val_str}{var_str}")
        
        return "".join(parts) if parts else "0"


def solve_notebook_style():
    print("\n=== Генератор решения 'Как в тетради' ===")
    print("Введите данные из вашего задания.")

    try:
        P = int(input("Введите модуль P (например, 13): "))
        N = int(input("Введите количество точек (k): "))
        
        points_x = []
        points_y = []
        print(f"\nВведите точки (x y):")
        for i in range(N):
            line = input(f"Точка {i+1}: ").replace(',', ' ').split()
            points_x.append(int(line[0]))
            points_y.append(int(line[1]))
    except ValueError:
        print("Ошибка ввода.")
        return

    print("\n" + "="*60)
    print(f"РЕШЕНИЕ (P = {P})")
    print("="*60)

    l_polys_coeffs = [] 

    for i in range(N):
        xi = points_x[i]
        print(f"\n---> 1.{i+1}) Вычисляем l_{i+1}(x) для x_{i+1} = {xi}:")
        
        top_str_parts = []
        bot_str_parts = []
        
        num_poly = Poly([1]) 
        denom_val = 1
        
        for j in range(N):
            if i == j: continue
            xj = points_x[j]
            
            term = Poly([1, -xj])
            num_poly = num_poly.mul_poly(term)
            top_str_parts.append(f"(x - {xj})")
            
  
            diff = xi - xj
            denom_val *= diff
            bot_str_parts.append(f"({xi} - {xj})")


        print(f"l_{i+1}(x) = [{' * '.join(top_str_parts)}] / [{' * '.join(bot_str_parts)}]")
        print(f"        = ({num_poly}) / {denom_val}")
        
        denom_mod = denom_val % P
        inv_denom = mod_inverse(denom_mod, P)
        
        if inv_denom is None:
            print(f"ОШИБКА: Обратного элемента для {denom_mod} не существует!")
            return

        print(f"        (обратный к {denom_val} (mod {P}) -> {denom_mod}^-1 = {inv_denom})")
        print(f"        = {inv_denom} * ({num_poly})")
        
        final_poly_coeffs = [(c * inv_denom) % P for c in num_poly.coeffs]
        l_polys_coeffs.append(final_poly_coeffs)
        
        final_poly_obj = Poly(final_poly_coeffs)
        print(f"        = {final_poly_obj} (mod {P})")

    print("\n" + "-"*60)
    print("2) Составляем F(x) и находим коэффициенты:")
    print(f"F(x) = {points_y[0]}*l_1(x) + {points_y[1]}*l_2(x) + {points_y[2]}*l_3(x)")
    

    deg = N - 1

    coeff_names = []
    if deg == 2:
        coeff_names = ["a_2", "a_1", "M"]
    else:
        for d in range(deg, -1, -1):
            coeff_names.append(f"a_{d}" if d > 0 else "M")

    final_coeffs_result = []

    for power_idx in range(N):
        current_power_coeffs = []
        calculation_str_parts = []
        val_sum = 0
        

        for i in range(N):
            y = points_y[i]
            l_coeff = l_polys_coeffs[i][power_idx] 
            
            term = y * l_coeff
            val_sum += term
            
            calculation_str_parts.append(f"{y}*{l_coeff}")
        
        val_mod = val_sum % P
        final_coeffs_result.append(val_mod)

        name = coeff_names[power_idx]
        calc_str = " + ".join(calculation_str_parts)
        print(f"{name} = {calc_str} = {val_sum} = {val_mod} (mod {P})")

    print("\n" + "="*60)
    final_poly_obj = Poly(final_coeffs_result)
    print(f"Итоговый полином F(x) = {final_poly_obj}")
    print(f"СЕКРЕТ (M) = {final_coeffs_result[-1]}")
    print("="*60)

if __name__ == "__main__":
    solve_notebook_style()