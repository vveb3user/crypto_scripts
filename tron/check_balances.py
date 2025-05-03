"""
TRON Balance Checker

Проверяет балансы TRX и USDT-TRC20 через API Tronscan
Для избежания бана IP используйте DELAY_BETWEEN_REQUESTS
"""

import json
import time
import requests
from datetime import datetime

# Конфигурация
TRONSCAN_API_URL = "https://apilist.tronscan.org/api/account"
USDT_CONTRACT = "TR7NHqjeKQxGTCi8q8ZY4pL8otSzgjLj6t"  # Контракт USDT-TRC20
OUTPUT_FILE = "tron_balances_report.txt"
DELAY_BETWEEN_REQUESTS = 3  # # Задержка между запросами к API

def get_tron_balances(address):
    """Получает балансы TRX и USDT для адреса через TRONSCAN API"""
    try:
        response = requests.get(f"{TRONSCAN_API_URL}?address={address}")
        response.raise_for_status()
        data = response.json()
        
        # Баланс TRX (1 TRX = 1_000_000 SUN)
        trx_balance = float(data.get('balance', 0)) / 1_000_000
        
        # Поиск баланса USDT среди TRC20-токенов
        usdt_balance = 0.0
        for token in data.get('trc20token_balances', []):
            if token.get('tokenId') == USDT_CONTRACT:
                usdt_balance = float(token.get('balance', 0)) / 1_000_000  # USDT имеет 6 знаков после запятой
                break
        
        return {
            'TRX': trx_balance,
            'USDT': usdt_balance
        }
        
    except requests.RequestException as e:
        raise Exception(f"API error: {str(e)}")
    except (KeyError, ValueError) as e:
        raise Exception(f"Data parsing error: {str(e)}")

def save_results(results, filename):
    """Сохраняет результаты в файл"""
    with open(filename, 'w', encoding='utf-8') as f:
        # Заголовок с датой
        f.write(f"TRON Balance Report ({datetime.now().strftime('%Y-%m-%d %H:%M:%S')})\n")
        f.write("=" * 50 + "\n\n")
        
        # Записи по адресам
        for item in results:
            f.write(f"Адрес: {item['address']}\n")
            f.write(f"Путь: {item['path']}\n")
            f.write(f"TRX: {item['balances']['TRX']:.6f}\n")
            f.write(f"USDT: {item['balances']['USDT']:.6f}\n")
            if item.get('error'):
                f.write(f"Ошибка: {item['error']}\n")
            f.write("-" * 50 + "\n")
        
        # Итоги
        total_trx = sum(item['balances']['TRX'] for item in results if not item.get('error'))
        total_usdt = sum(item['balances']['USDT'] for item in results if not item.get('error'))
        error_count = sum(1 for item in results if item.get('error'))
        
        f.write("\nИтоги:\n")
        f.write(f"Всего адресов: {len(results)}\n")
        f.write(f"Ошибки: {error_count}\n")
        f.write(f"Общий баланс TRX: {total_trx:.6f}\n")
        f.write(f"Общий баланс USDT: {total_usdt:.6f}\n")

def main():
    # Загрузка адресов
    try:
        with open("tron_addresses.json", "r", encoding='utf-8') as f:
            addresses = json.load(f)
    except FileNotFoundError:
        print("Ошибка: Файл tron_addresses.json не найден!")
        return
    except json.JSONDecodeError:
        print("Ошибка: Некорректный формат JSON в файле tron_addresses.json!")
        return

    # Проверка балансов
    results = []
    print(f"Начинаем проверку {len(addresses)} адресов...")
    
    for i, item in enumerate(addresses, 1):
        address = item['address']
        path = item['path']
        
        try:
            balances = get_tron_balances(address)
            results.append({
                'address': address,
                'path': path,
                'balances': balances,
                'error': None
            })
            print(f"{i}. {address} | TRX: {balances['TRX']:.6f} | USDT: {balances['USDT']:.6f}")
        except Exception as e:
            results.append({
                'address': address,
                'path': path,
                'balances': {'TRX': 0.0, 'USDT': 0.0},
                'error': str(e)
            })
            print(f"{i}. {address} | Ошибка: {str(e)}")
        
        if i < len(addresses):
            time.sleep(DELAY_BETWEEN_REQUESTS)  # Задержка между запросами
    
    # Сохранение результатов
    save_results(results, OUTPUT_FILE)
    print(f"\nОтчёт сохранён в файл: {OUTPUT_FILE}")

if __name__ == "__main__":
    main()