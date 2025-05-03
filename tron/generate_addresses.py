"""
TRON Address Generator

Генерирует адреса TRON из BIP-39 seed фразы
Путь деривации: m/44'/195'/0'/0/{index}
"""

from bip32utils import BIP32Key
from tronpy.keys import PrivateKey
import hashlib
import base58
import json

# ВАЖНО: Используйте этот код только на ОФФЛАЙН-устройстве!
# Замените на вашу 24-словную seed-фразу
seed_phrase = "your seed phrase"

if "your seed phrase" in seed_phrase:
    print("ОШИБКА: Вы не изменили seed-фразу!")
    print("Замените 'your seed phrase' на вашу 24-словную мнемоническую фразу")
    sys.exit(1) 

# Генерация seed из seed-фразы
mnemonic = seed_phrase.encode()
seed = hashlib.pbkdf2_hmac('sha512', mnemonic, b'mnemonic', 2048)[:64]

# Список стандартных путей для 1000 адресов (заменить на нужное количество)
paths = [f"m/44'/195'/0'/0/{i}" for i in range(1000)]

# Генерация адресов
addresses = []
for path in paths:
    # Разбор пути
    indices = [int(x.strip("'")) + (0x80000000 if x.endswith("'") else 0) for x in path.split("/")[1:]]
    key = BIP32Key.fromEntropy(seed)
    for index in indices:
        key = key.ChildKey(index)
    private_key = PrivateKey(bytes(key.PrivateKey()))
    address = private_key.public_key.to_base58check_address()
    addresses.append({"path": path, "address": address})

# Сохранение адресов в файл
with open("tron_addresses.json", "w") as f:
    json.dump(addresses, f, indent=4)

print(f"Сгенерировано {len(addresses)} адресов. Результаты сохранены в tron_addresses.json")
print("Скопируйте файл tron_addresses.json на онлайн-устройство и используйте check_balances.py для проверки балансов.")