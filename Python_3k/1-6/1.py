import sys

def get_inverse(a, m):
    try:
        return pow(a, -1, m)
    except ValueError:
        return None

def garner_solver():
    print("="*60)
    print(" РЕШЕНИЕ СИСТЕМЫ СРАВНЕНИЙ (АЛГОРИТМ ГАРНЕРА)")
    print("="*60)
    
    try:
        m_input = input("Введите модули (m) через пробел (например: 3 7 11): ")
        r_input = input("Введите остатки (r) через пробел (например: 2 5 4): ")
        
        m = [int(x) for x in m_input.split()]
        r = [int(x) for x in r_input.split()]
    except ValueError:
        print("\n[!] Ошибка: Вводите только целые числа.")
        return

    if len(m) != len(r):
        print(f"\n[!] Ошибка: Количество модулей ({len(m)}) не совпадает с количеством остатков ({len(r)}).")
        return

    n = len(m)
    x = r[0]  

    print("\n" + "-"*60)
    print(f"ДАНО:")
    print(f"  Система из {n} уравнений")
    for i in range(n):
        print(f"  x ≡ {r[i]} (mod {m[i]})")
    print("-" * 60)

    print(f"\nШАГ 1 (Инициализация):")
    print(f"  x_1 = r_1 = {r[0]}")
    print(f"  Текущее значение x = {x}")

    for i in range(1, n):
        print("\n" + "="*40)
        print(f"ШАГ {i+1} (Переход от x_{i} к x_{i+1}):")
        print("="*40)
        
        prev_mods = m[:i]
        M_str = " * ".join(map(str, prev_mods))
        M = 1
        for val in prev_mods:
            M *= val
            
        print(f"  a) Вычисляем произведение предыдущих модулей M:")
        print(f"     M = {M_str} = {M}")

        target_mod = m[i]
        inv_M = get_inverse(M, target_mod)
        
        print(f"  b) Ищем обратный элемент M^(-1) mod {target_mod}:")
        if inv_M is None:
            print(f"     [!] ОШИБКА: Обратного элемента для {M} по модулю {target_mod} не существует.")
            print("     Числа должны быть взаимно простыми.")
            return
        else:
            print(f"     ({M})^(-1) mod {target_mod} = {inv_M}")

        current_r = r[i]
        diff = current_r - x
        diff_mod = diff % target_mod
        
        print(f"  c) Вычисляем разность (r_{i+1} - текущий x):")
        print(f"     {current_r} - {x} = {diff}")
        print(f"     {diff} (mod {target_mod}) = {diff_mod}")

        y = (diff_mod * inv_M) % target_mod
        
        print(f"  d) Вычисляем коэффициент y_{i+1}:")
        print(f"     y_{i+1} = ({diff_mod} * {inv_M}) mod {target_mod}")
        print(f"     y_{i+1} = {diff_mod * inv_M} mod {target_mod} = {y}")

        old_x = x
        x = x + y * M
        
        print(f"  e) Обновляем x (Собираем формулу Гарнера):")
        print(f"     x_{i+1} = x_{i} + y_{i+1} * M")
        print(f"     x_{i+1} = {old_x} + {y} * {M}")
        print(f"     x_{i+1} = {old_x} + {y*M} = {x}")

    print("\n" + "="*60)
    print("ОТВЕТ:")
    
    total_M = 1
    total_M_str = " * ".join(map(str, m))
    for val in m:
        total_M *= val
        
    print(f"  Наименьшее положительное x = {x}")
    print(f"  Общее решение: x ≡ {x} (mod {total_M})")
    print(f"  (Общий модуль N = {total_M_str} = {total_M})")
    print("="*60)

if __name__ == "__main__":
    garner_solver()
    input("\nНажмите Enter, чтобы выйти...")