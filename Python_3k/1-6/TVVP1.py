# from scapy.all import *

# filename = 'C:/Users/kirde/Downloads/11 вариант/1 задание/dump.pcapng'

# try:
#     print("[-] Загружаю pcap (это может занять пару секунд)...")
#     packets = rdpcap(filename)
    
#     raw_flag = ""
#     clean_flag = ""
#     last_char = ""

#     print("[-] Анализируем и чистим...")

#     for pkt in packets:
#         if IP in pkt:
#             dst_ip = pkt[IP].dst
            
#             if not dst_ip.startswith("239.") and not dst_ip.endswith(".255"):
#                 try:
#                     val = int(dst_ip.split('.')[-1])

#                     if val < 32 or val > 126:
#                         continue
                        
#                     char = chr(val)

#                     if char == last_char:
#                         continue
                    
#                     clean_flag += char
#                     last_char = char
                    
#                 except:
#                     pass

#     print(f"\n[+] ЧИСТЫЙ ФЛАГ: {clean_flag}")

# except Exception as e:
#     print(f"Ошибка: {e}")







from scapy.all import *
import logging

# Отключаем лишние предупреждения scapy, чтобы не засорять консоль
logging.getLogger("scapy.runtime").setLevel(logging.ERROR)

# Укажите путь к вашему файлу
filename = 'C:/Users/kirde/Downloads/11 вариант/1 задание/dump.pcapng'

try:
    print("[-] Загружаю pcap...")
    packets = rdpcap(filename)
    
    clean_flag = ""
    last_char = ""

    print("[-] Процесс декодирования:")

    for pkt in packets:
        if IP in pkt:
            dst_ip = pkt[IP].dst
            
            # Отсеиваем мультикаст (239.x.x.x) и броадкаст (.255)
            if not dst_ip.startswith("239.") and not dst_ip.endswith(".255"):
                try:
                    # Извлекаем последний октет IP-адреса
                    val = int(dst_ip.split('.')[-1])

                    # Фильтруем только печатные символы ASCII (от 32 до 126)
                    if val < 32 or val > 126:
                        continue
                        
                    char = chr(val)

                    # Дедупликация: если символ совпадает с предыдущим, пропускаем его
                    if char == last_char:
                        continue
                    
                    # === ВЫВОД ДЛЯ ОТЧЕТА ===
                    # Выводим строку только если это новый символ
                    print(f"\t{val} – {char} по таблице ASCII;")
                    
                    clean_flag += char
                    last_char = char
                    
                except:
                    pass

    print(f"\n[+] ПОЛУЧЕННЫЙ ФЛАГ: {clean_flag}")

except Exception as e:
    print(f"Ошибка: {e}")