def legendre_symbol(a, p):
    ls = pow(a, (p - 1) // 2, p)
    if ls == p - 1:
        return -1
    return ls

def tonelli_shanks_notebook_style():
    print("--- КАЛЬКУЛЯТОР ТОНЕЛЛИ-ШЕНКСА ---")
    
    try:
        a = int(input("Введите число a (x^2 = a mod p): "))
        p = int(input("Введите модуль p (простое число): "))
    except ValueError:
        print("Ошибка: Введите целые числа.")
        return

    print("\n" + "="*30)
    print(f"Решение сравнения: x^2 ≡ {a} (mod {p})")
    print("="*30 + "\n")
    ls = legendre_symbol(a, p)
    print(f"0) Проверка разрешимости (Символ Лежандра):")
    if ls == -1:
        print(f"({a}/{p}) = -1. Решений нет.")
        return
    elif ls == 0:
        print(f"({a}/{p}) = 0. x ≡ 0 (mod {p})")
        return
    else:
        print(f"({a}/{p}) = 1. Решение существует.\n")

    Q = p - 1
    S = 0
    while Q % 2 == 0:
        Q //= 2
        S += 1
    
    print(f"1) Представим p - 1 = Q * 2^S:")
    print(f"   {p} - 1 = {p-1} = {Q} * 2^{S}")
    print(f"   Q = {Q}, S = {S}\n")

    z = 2
    while legendre_symbol(z, p) != -1:
        z += 1
    
    print(f"2) Найдем квадратичный невычет z:")
    print(f"   z = {z}, так как ({z}/{p}) = -1\n")
    c = pow(z, Q, p)
    R = pow(a, (Q + 1) // 2, p)
    t = pow(a, Q, p)
    M = S

    print(f"3) Инициализация (полагаем):")
    print(f"   c ≡ z^Q mod p ≡ {z}^{Q} mod {p} ≡ {c}")
    print(f"   R ≡ a^((Q+1)/2) mod p ≡ {a}^{ (Q + 1) // 2 } mod {p} ≡ {R}")
    print(f"   t ≡ a^Q mod p ≡ {a}^{Q} mod {p} ≡ {t}")
    print(f"   M = S = {M}\n")

    print(f"4) Цикл:")
    
    while True:
        print(f"   Проверка t: {t} ≡ 1 (mod {p})?")
        if t == 1:
            print("   t = 1, цикл завершен.\n")
            break
        
        print("   t ≠ 1, ищем наименьшее i (0 < i < M), такое что t^(2^i) ≡ 1 (mod p)")

        i = 0
        temp_t = t
        for k in range(1, M):
            temp_t = pow(temp_t, 2, p)
            if temp_t == 1:
                i = k
                break
        
        print(f"   Найдено i = {i} (так как {t}^(2^{i}) ≡ 1)")
        
        pow_of_2 = pow(2, M - i - 1)
        b = pow(c, pow_of_2, p)
        
        print(f"   b ≡ c^(2^(M-i-1)) ≡ {c}^(2^{M - i - 1}) ≡ {c}^{pow_of_2} ≡ {b} (mod {p})")
        
        old_R = R
        R = (R * b) % p
        print(f"   R ≡ R * b ≡ {old_R} * {b} ≡ {R} (mod {p})")
        
        b2 = pow(b, 2, p)
        old_t = t
        t = (t * b2) % p
        print(f"   t ≡ t * b^2 ≡ {old_t} * {b2} ≡ {t} (mod {p})")
        
        c = b2
        print(f"   c ≡ b^2 ≡ {c} (mod {p})")

        M = i
        print(f"   M = {M}")
        print("   --- конец итерации ---\n")

    x1 = R
    x2 = p - R
    print("="*30)
    print(f"Ответ: {x1} mod {p}, {x2} mod {p}")
    print("="*30)

if __name__ == "__main__":
    tonelli_shanks_notebook_style()