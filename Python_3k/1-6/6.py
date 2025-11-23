def solve_feistel_detailed():
    print("--- ВВОД ДАННЫХ ---")
    p_hex = input("Введите исходный текст (HEX, например AB): ").strip().upper()
    k_bin = input("Введите ключ (BIN, например 1111): ").strip()
    rounds = int(input("Количество раундов (обычно 4): "))

    print("\n" + "="*40)
    print("   РЕШЕНИЕ (ПОДРОБНОЕ)")
    print("="*40 + "\n")

    scale = 16 
    num_bits = len(p_hex) * 4
    p_int = int(p_hex, 16)
    p_bin = f"{p_int:0{num_bits}b}"
    
    mid = len(p_bin) // 2
    L = p_bin[:mid]
    R = p_bin[mid:]
    
    K = k_bin

    print(f"Дано:")
    print(f"Текст P = {p_hex} (16-рич.)")
    print(f"Ключ  K = {K} (2-ич.)")
    print(f"Раундов: {rounds}")
    print("-" * 30)
    
    print("1) Преобразование в двоичный код:")
    hex_map = {
        '0':'0000', '1':'0001', '2':'0010', '3':'0011',
        '4':'0100', '5':'0101', '6':'0110', '7':'0111',
        '8':'1000', '9':'1001', 'A':'1010', 'B':'1011',
        'C':'1100', 'D':'1101', 'E':'1110', 'F':'1111'
    }
    conversion_str = " ".join([f"{char}->{hex_map[char]}" for char in p_hex])
    print(f"   {conversion_str}")
    print(f"   P_bin = {p_bin}")

    print("\n2) Разделение на блоки L0 и R0:")
    print(f"   C0 (старт): {L} {R}")
    print(f"   L0: {L}")
    print(f"   R0: {R}")
    print("=" * 40)

    cur_L = L
    cur_R = R
    
    for i in range(1, rounds + 1):
        print(f"\n--- РАУНД {i} ---")
        
        prev_idx = i - 1
        curr_idx = i
        
        print(f"Формулы раунда:")
        print(f"   L{curr_idx} = R{prev_idx}")
        print(f"   R{curr_idx} = L{prev_idx} ⊕ F(R{prev_idx}, K)")
        print(f"   (где F - это просто XOR с ключом: R{prev_idx} ⊕ K)") 
        
        val_L_prev = int(cur_L, 2)
        val_K = int(K, 2)
        res_xor = val_L_prev ^ val_K 
        
        width = len(cur_L)
        new_R_str = f"{res_xor:0{width}b}"
        new_L_str = cur_R 
        
        print(f"\nВычисление R{curr_idx}:")
        print(f"     {cur_L} (L{prev_idx})")
        print(f"   ⊕ {K} (Key)")
        print(f"   -------")
        print(f"     {new_R_str} (Результат)")

        print(f"\nИтог раунда {i}:")
        print(f"   L{curr_idx}: {new_L_str} (взято из R{prev_idx})")
        print(f"   R{curr_idx}: {new_R_str}")
        print(f"   C{curr_idx}: {new_L_str} {new_R_str}")
        
        cur_L = new_L_str
        cur_R = new_R_str
        print("-" * 20)

    final_bin = cur_L + cur_R
    final_hex = hex(int(final_bin, 2))[2:].upper()
    
    print("\n" + "="*40)
    print("   РЕЗУЛЬТАТ")
    print("="*40)
    print(f"Финальный блок C{rounds}: {cur_L} {cur_R}")
    print(f"Перевод в HEX: {cur_L}{cur_R} -> {final_hex}16")
    print(f"Ответ: {final_hex}16")

if __name__ == "__main__":
    solve_feistel_detailed()