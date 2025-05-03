# TRON Crypto Scripts

## Требования

- **Python 3.8+**.
- Установите библиотеки:
  ```bash
  pip install requests bip32utils tronpy base58
  ```
- **Оффлайн-устройство** для `generate_addresses.py`.
- **Онлайн-устройство** для `check_balances.py`.
- 24-словная **BIP-39 seed-фраза** для генерации адресов.

## Скрипты

### 1. `generate_addresses.py`

**Назначение**: Генерирует TRON-адреса из BIP-39 seed-фразы (путь: `m/44'/195'/0'/0/{index}`).

**Использование**:
1. На **оффлайн-устройстве** замените `seed_phrase = "your seed phrase"` в скрипте на вашу seed-фразу.
2. Настройте количество адресов в `range(1000)` (по умолчанию: 1000).
3. Выполните:
   ```bash
   python generate_addresses.py
   ```
4. Перенесите `tron_addresses.json` на онлайн-устройство.

**Выход**: `tron_addresses.json` с адресами и путями.

**Важно**: Не используйте seed-фразу на устройстве с интернетом!

### 2. `check_balances.py`

**Назначение**: Проверяет балансы TRX и USDT-TRC20 через API Tronscan.

**Использование**:
1. Убедитесь, что `tron_addresses.json` находится в той же папке.
2. На **онлайн-устройстве** выполните:
   ```bash
   python check_balances.py
   ```
3. Результаты сохраняются в `tron_balances_report.txt`.

**Выход**: `tron_balances_report.txt` с балансами, ошибками и итогами.

**Настройка**: Измените `DELAY_BETWEEN_REQUESTS` (по умолчанию 3 сек.) при проблемах с API.

## Безопасность

- Храните seed-фразу только оффлайн.
- Увеличьте `DELAY_BETWEEN_REQUESTS` при блокировке API.
- Не публикуйте `tron_addresses.json` и `tron_balances_report.txt`.

## Устранение неполадок

- **Нет `tron_addresses.json`**: Проверьте выполнение `generate_addresses.py`.
- **Ошибки API**: Увеличьте `DELAY_BETWEEN_REQUESTS` или проверьте интернет.
- **Неверная seed-фраза**: Убедитесь, что она валидна (24 слова).
- **Проблемы с библиотеками**: Установите `requests`, `bip32utils`, `tronpy`, `base58`.
