def explain_legendre_detailed(a, p):
    print(f"\n--- Шаг 0. Проверка разрешимости (Символ Лежандра ({a}/{p})) ---")
    
    current_a = a % p
    current_sign = 1
    
    if current_a != a:
        print(f"1) Упрощаем a: {a} ≡ {current_a} (mod {p})")
    
    if current_a == p - 1:
        print(f"   Заметим, что {current_a} ≡ -1 (mod {p})")
        power = (p - 1) // 2
        res = pow(-1, power)
        val_str = "1" if res == 1 else "-1"
        print(f"   (-1/{p}) = (-1)^({power}) = {val_str}")
        print(f"   РЕЗУЛЬТАТ: {val_str}. Решение {'есть' if res==1 else 'нет'}.")
        return res
    squares = [4, 9, 16, 25, 36]
    for sq in squares:
        while current_a % sq == 0 and current_a > 0:
            print(f"   Выносим полный квадрат {sq}: {current_a} = {sq} * {current_a // sq}")
            print(f"   ({sq}/{p}) = 1, остается ({current_a // sq}/{p})")
            current_a //= sq

    while current_a % 2 == 0 and current_a > 0:
        print(f"   Выносим множитель 2: {current_a} = 2 * {current_a // 2}")
        power_2 = (p**2 - 1) // 8
        sign_2 = 1 if power_2 % 2 == 0 else -1
        sign_str = "1" if sign_2 == 1 else "-1"
        print(f"   (2/{p}) = (-1)^(({p}^2-1)/8) = {sign_str}")
        current_sign *= sign_2
        current_a //= 2

    if current_a > 1:
        power = (p - 1) // 2
        euler_val = pow(current_a, power, p)
        val_str = "-1" if euler_val == p - 1 else str(euler_val)
        print(f"   Для остатка {current_a} применяем критерий Эйлера:")
        print(f"   {current_a}^(({p}-1)/2) = {current_a}^{power} (mod {p}) ≡ {val_str}")
        final_result = current_sign * (1 if euler_val == 1 else -1)
    else:
        final_result = current_sign

    res_str = "1" if final_result == 1 else "-1"
    print(f"   ИТОГОВЫЙ СИМВОЛ: {res_str}. Решение {'есть' if final_result==1 else 'нет'}.")
    return final_result

def solve_pocklington_detailed():
    print("\n=== КАЛЬКУЛЯТОР ПОКЛИНГТОНА (ОЧЕНЬ ПОДРОБНО) ===")
    try:
        a_in = int(input("Введите a: "))
        p_in = int(input("Введите p: "))
    except ValueError:
        return

    a = a_in % p_in
    print(f"\nРешаем: x^2 ≡ {a} (mod {p_in})")
    
    ls = explain_legendre_detailed(a_in, p_in)
    if ls != 1: return

    print(f"\n--- Шаг 1: Анализ модуля p и поиск k ---")
    if p_in % 4 == 3:
        k = (p_in - 3) // 4
        print(f"p = {p_in}. Проверяем остаток от деления на 4: {p_in} = 4*{k} + 3.")
        print(f"Это простой случай (4k+3). k = {k}.")
        print("\n--- Шаг 2: Вычисление корня ---")
        print(f"Формула: x ≡ ± a^(k+1)")
        print(f"Подставляем: x ≡ ± {a}^({k}+1) ≡ ± {a}^{k+1}")
        res = pow(a, k+1, p_in)
        print(f"Считаем: {a}^{k+1} mod {p_in} = {res}")
        print(f"\nОтвет: {res} (mod {p_in}) и {p_in - res} (mod {p_in})")

    elif p_in % 8 == 5:
        k = (p_in - 5) // 8
        print(f"p = {p_in}. Проверяем остаток от деления на 8.")
        print(f"{p_in} = 8*{k} + 5. Это случай (8k+5).")
        print(f"Следовательно, k = {k}.")
        
        print("\n--- Шаг 2: Вычисляем двух кандидатов (ПОДРОБНО) ---")
        
        print(f"\n1) ПЕРВЫЙ КАНДИДАТ (x1):")
        print(f"   Формула: x1 ≡ ± a^(k+1) (mod p)")
        print(f"   Подставляем k={k}: x1 ≡ ± {a}^({k}+1)")
        print(f"   Упрощаем степень: x1 ≡ ± {a}^{k+1}")
        
        cand1 = pow(a, k+1, p_in)
        raw_val = a**(k+1)
        if raw_val < 10000:
            print(f"   Считаем: {a}^{k+1} = {raw_val}")
            print(f"   Берем по модулю {p_in}: {raw_val} mod {p_in} = {cand1}")
        else:
            print(f"   Считаем по модулю {p_in}: {a}^{k+1} ≡ {cand1}")
        
        print(f"   Итог по x1: ± {cand1}")

        print(f"\n2) ВТОРОЙ КАНДИДАТ (x2):")
        print(f"   Формула: x2 ≡ ± 2^(2k+1) * a^(k+1) (mod p)")
        print(f"   Здесь добавляется множитель '2' в степени (2k+1).")
        
        pow2_exp = 2*k + 1
        print(f"   а) Считаем степень двойки: 2^(2*{k}+1) = 2^{pow2_exp}")
        val_2 = pow(2, pow2_exp, p_in)
        raw_2 = 2**pow2_exp
        if raw_2 < 1000:
            print(f"      2^{pow2_exp} = {raw_2}")
            print(f"      {raw_2} mod {p_in} = {val_2}")
        else:
            print(f"      2^{pow2_exp} mod {p_in} = {val_2}")

        print(f"   б) Умножаем на часть из x1 (которая равна {cand1}):")
        print(f"      x2 ≡ ± {val_2} * {cand1}")
        prod = val_2 * cand1
        cand2 = prod % p_in
        print(f"      {val_2} * {cand1} = {prod}")
        print(f"      {prod} mod {p_in} = {cand2}")
        print(f"   Итог по x2: ± {cand2}")

        print("\n--- Шаг 3: Проверка кандидатов (возведение в квадрат) ---")
        
        sq1 = pow(cand1, 2, p_in)
        print(f"Проверяем первого кандидата ({cand1}):")
        print(f"{cand1}^2 = {cand1*cand1} ≡ {sq1} (mod {p_in})")
        if sq1 == a:
            print(f"Так как {sq1} == {a} (исходное а), то ЭТО ВЕРНЫЙ ОТВЕТ.")
            ans = cand1
        else:
            print(f"Так как {sq1} != {a}, этот кандидат НЕ подходит.")
            
            sq2 = pow(cand2, 2, p_in)
            print(f"\nПроверяем второго кандидата ({cand2}):")
            print(f"{cand2}^2 = {cand2*cand2} ≡ {sq2} (mod {p_in})")
            if sq2 == a:
                print(f"Так как {sq2} == {a}, то ЭТО ВЕРНЫЙ ОТВЕТ.")
                ans = cand2
            else:
                print("Ошибка! Никто не подошел.")
                return

        print(f"\n=== ИТОГОВЫЙ ОТВЕТ ===")
        print(f"x ≡ {ans} (mod {p_in})")
        print(f"x ≡ {p_in - ans} (mod {p_in})")

    else:
        print("Случай не подходит под алгоритм Поклингтона (требуется Тонелли-Шенкс).")

if __name__ == "__main__":
    solve_pocklington_detailed()