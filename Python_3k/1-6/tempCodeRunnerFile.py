from scapy.all import *

filename = 'C:/Users/kirde/Downloads/11 вариант/1 задание/dump.pcapng'

try:
    print("[-] Загружаю pcap (это может занять пару секунд)...")
    packets = rdpcap(filename)
    
    raw_flag = ""
    clean_flag = ""
    last_char = ""

    print("[-] Анализируем и чистим...")

    for pkt in packets:
        if IP in pkt:
            dst_ip = pkt[IP].dst
            
            if not dst_ip.startswith("239.") and not dst_ip.endswith(".255"):
                try:
                    val = int(dst_ip.split('.')[-1])

                    if val < 32 or val > 126:
                        continue
                        
                    char = chr(val)

                    if char == last_char:
                        continue
                    
                    clean_flag += char
                    last_char = char
                    
                except:
                    pass

    print(f"\n[+] ЧИСТЫЙ ФЛАГ: {clean_flag}")

except Exception as e:
    print(f"Ошибка: {e}")

