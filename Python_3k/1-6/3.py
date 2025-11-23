def legendre_symbol(a, p):
    """Вычисляет символ Лежандра (a/p)"""
    ls = pow(a, (p - 1) // 2, p)
    if ls == p - 1:
        return -1
    return ls

def solve_pocklington_interactive():
    print("--- АЛГОРИТМ ПОКЛИНГТОНА (РЕШЕНИЕ x^2 = a mod p) ---")
    
    # 1. Ввод данных пользователем
    try:
        a = int(input("Введите значение a: "))
        p = int(input("Введите значение p (простое число): "))
    except ValueError:
        print("Ошибка: Пожалуйста, введите целые числа.")
        return

    print(f"\nРешаем сравнение: x^2 ≡ {a} (mod {p})")

    # 2. Проверка разрешимости (Слайд 7)
    ls = legendre_symbol(a, p)
    print(f"1. Вычисляем символ Лежандра ({a}/{p}):")
    if ls == -1:
        print(f"   Результат: -1. Решений нет (a — квадратичный невычет).")
        return
    elif ls == 0:
        print(f"   Результат: 0. x = 0.")
        return
    else:
        print(f"   Результат: 1. Решение существует.")

    # 3. Определение случая
    # Случай А: p = 4k + 3 (Слайд 4)
    if p % 4 == 3:
        k = (p - 3) // 4
        print(f"\n2. Анализ модуля p:")
        print(f"   p = {p} имеет вид 4k + 3.")
        print(f"   {p} = 4 * {k} + 3 => k = {k}")
        print("   Используем формулу (Слайд 4): x ≡ ± a^(k+1) (mod p)")
        
        # Вычисление
        exp = k + 1
        x = pow(a, exp, p)
        
        print(f"\n3. Вычисление корня:")
        print(f"   x ≡ ± {a}^{exp} (mod {p})")
        print(f"   x ≡ ± {x} (mod {p})")
        
        print(f"\nОТВЕТ: {x} (mod {p}) и {p - x} (mod {p})")

    # Случай Б: p = 8k + 5 (Слайды 5-7)
    elif p % 8 == 5:
        k = (p - 5) // 8
        print(f"\n2. Анализ модуля p:")
        print(f"   p = {p} имеет вид 8k + 5 (p ≡ 5 mod 8).")
        print(f"   {p} = 8 * {k} + 5 => k = {k}")
        print("   Формируем два кандидата на решение (Слайд 6).")
        
        # Кандидат 1 (Слайд 6: x = ± a^(k+1))
        exp1 = k + 1
        cand1 = pow(a, exp1, p)
        print(f"\n3. Кандидат №1 (по формуле ± a^(k+1)):")
        print(f"   x1 ≡ ± {a}^{k+1} ≡ ± {cand1} (mod {p})")
        
        # Кандидат 2 (Слайд 6: x = ± 2^(2k+1) * a^(k+1))
        # Используем 2 как квадратичный невычет, как указано в лекции
        term_2 = pow(2, 2*k + 1, p)
        term_a = pow(a, k + 1, p)
        cand2 = (term_2 * term_a) % p
        
        print(f"\n4. Кандидат №2 (по формуле ± 2^(2k+1) * a^(k+1)):")
        print(f"   x2 ≡ ± 2^(2*{k}+1) * {a}^{k+1}")
        print(f"   x2 ≡ ± {term_2} * {term_a} ≡ ± {cand2} (mod {p})")
        
        # Проверка (Слайд 7)
        print(f"\n5. Проверка кандидатов возведением в квадрат:")
        
        # Проверяем кандидата 1
        check1 = pow(cand1, 2, p)
        print(f"   Проверка x1: ({cand1})^2 ≡ {check1} (mod {p})")
        if check1 == a:
            print(f"   {check1} == {a} -> ЭТО ВЕРНЫЙ КОРЕНЬ.")
            ans = cand1
        else:
            print(f"   {check1} != {a} -> Не подходит.")
            
            # Если первый не подошел, проверяем второго
            check2 = pow(cand2, 2, p)
            print(f"   Проверка x2: ({cand2})^2 ≡ {check2} (mod {p})")
            if check2 == a:
                print(f"   {check2} == {a} -> ЭТО ВЕРНЫЙ КОРЕНЬ.")
                ans = cand2
            else:
                print("   Ошибка: ни один кандидат не подошел.")
                return

        print(f"\nОТВЕТ: {ans} (mod {p}) и {p - ans} (mod {p})")

    # Случай p = 8k + 1
    else:
        print(f"\n2. Анализ модуля p:")
        print(f"   p = {p}. Это случай 8k + 1.")
        print("   ВНИМАНИЕ: Согласно лекции, для этого случая алгоритм Поклингтона не применяется напрямую.")
        print("   Используйте алгоритм Тонелли-Шенкса (задание №5).")

if __name__ == "__main__":
    solve_pocklington_interactive()