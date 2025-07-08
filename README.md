# mstc2tlgrm_bot

![Python](https://img.shields.io/badge/python-3.8%2B-blue)
![License](https://img.shields.io/github/license/Insaned79/mstc2tlgrm_bot)

---

## ⚠️ Important Note
**This bot receives messages only from MQTT and only from the general (broadcast) channel.**

---

## 📑 Table of Contents
- [Important Note](#️-important-note)
- [Description](#description)
- [Quick Start](#quick-start)
- [Config Example](#config-example)
- [File Structure](#file-structure)
- [Example Output](#example-output)
- [Useful Links](#useful-links)
- [Feedback](#feedback)

---

## Description
A bot for forwarding messages from the Meshtastic network to Telegram. It listens to MQTT and only the general channel (wildcard topic). Supports multiple nodes, deduplication, detailed logging, and easy configuration.

---

## Quick Start
1. **Clone the repository:**
   ```bash
   git clone https://github.com/Insaned79/mstc2tlgrm_bot.git
   cd mstc2tlgrm_bot
   ```
2. **Copy and edit the config:**
   ```bash
   cp config.py.example config.py
   # Edit config.py and set your parameters (Telegram token, MQTT, etc.)
   ```
3. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```
4. **Run the main bot:**
   ```bash
   python tg_meshtastic_forwarder.py
   ```
   For logging/debugging you can also run:
   ```bash
   python log_mqtt.py
   python log_mqtt_bin.py
   ```

---

## Config Example
```python
TELEGRAM_BOT_TOKEN = "your_bot_token"
MQTT_BROKER = "broker_address"
MQTT_PORT = 1883
# You can use # to listen to all nodes:
MQTT_TOPIC = "meshtastic/krd/2/e/#"
MQTT_USERNAME = "mqtt_username"
MQTT_PASSWORD = "mqtt_password"
MQTT_JSON_TOPIC = "meshtastic/krd/2/json/#"
```
- **MQTT_TOPIC** with `#` allows you to listen to multiple nodes. Duplicate messages will NOT be sent to Telegram due to built-in deduplication.

---

## File Structure
- `tg_meshtastic_forwarder.py` — main forwarder bot
- `log_mqtt.py`, `log_mqtt_bin.py` — loggers for debugging
- `config.py.example` — config example
- `requirements.txt` — dependencies
- [`LICENSE`](LICENSE) — license

---

## Example Output
*Sample output in Telegram:*
```
2025-07-08 09:03:46
<b>Hello from Meshtastic!</b>
1234567890 to 4294967295
RSSI: -120
Hop(s): 2, away: 1
```

---

## Useful Links
- [Meshtastic](https://meshtastic.org/)
- [Telegram Bot API](https://core.telegram.org/bots/api)
- [Issues](https://github.com/Insaned79/mstc2tlgrm_bot/issues)
- [Pull Requests](https://github.com/Insaned79/mstc2tlgrm_bot/pulls)

---

## Feedback
Please use [Issues](https://github.com/Insaned79/mstc2tlgrm_bot/issues) on GitHub for questions and bug reports.


---

# mstc2tlgrm_bot (Русская версия)

![Python](https://img.shields.io/badge/python-3.8%2B-blue)
![License](https://img.shields.io/github/license/Insaned79/mstc2tlgrm_bot)

---

## ⚠️ Важно
**Бот получает сообщения только из MQTT и только из общего (broadcast) канала.**

---

## 📑 Оглавление
- [Важно](#️-важно)
- [Описание](#описание)
- [Быстрый старт](#быстрый-старт)
- [Пример конфига](#пример-конфига)
- [Структура файлов](#структура-файлов)
- [Пример работы](#пример-работы)
- [Полезные ссылки](#полезные-ссылки)
- [Обратная связь](#обратная-связь)

---

## Описание
Бот для пересылки сообщений из сети Meshtastic в Telegram. Слушает только MQTT и только общий канал (wildcard topic). Поддерживает несколько нод, защиту от дублей, подробное логирование и простую настройку.

---

## Быстрый старт
1. **Клонируйте репозиторий:**
   ```bash
   git clone https://github.com/Insaned79/mstc2tlgrm_bot.git
   cd mstc2tlgrm_bot
   ```
2. **Скопируйте и настройте конфиг:**
   ```bash
   cp config.py.example config.py
   # Откройте config.py и укажите свои параметры (токен Telegram, MQTT и т.д.)
   ```
3. **Установите зависимости:**
   ```bash
   pip install -r requirements.txt
   ```
4. **Запустите основной бот:**
   ```bash
   python tg_meshtastic_forwarder.py
   ```
   Для логирования сообщений можно использовать:
   ```bash
   python log_mqtt.py
   python log_mqtt_bin.py
   ```

---

## Пример конфига
```python
TELEGRAM_BOT_TOKEN = "your_bot_token"
MQTT_BROKER = "broker_address"
MQTT_PORT = 1883
# Можно использовать # для прослушивания всех нод:
MQTT_TOPIC = "meshtastic/krd/2/e/#"
MQTT_USERNAME = "mqtt_username"
MQTT_PASSWORD = "mqtt_password"
MQTT_JSON_TOPIC = "meshtastic/krd/2/json/#"
```
- **MQTT_TOPIC** с `#` позволяет слушать сразу несколько нод. Дублирующиеся сообщения не будут отправляться в Telegram благодаря встроенной защите.

---

## Структура файлов
- `tg_meshtastic_forwarder.py` — основной бот-пересылщик
- `log_mqtt.py`, `log_mqtt_bin.py` — логгеры для отладки
- `config.py.example` — пример конфига
- `requirements.txt` — зависимости
- [`LICENSE`](LICENSE) — лицензия

---

## Пример работы
*Пример вывода в Telegram:*
```
2025-07-08 09:03:46
<b>Привет из Meshtastic!</b>
1234567890 to 4294967295
RSSI: -120
Hop(s): 2, away: 1
```

---

## Полезные ссылки
- [Meshtastic](https://meshtastic.org/)
- [Telegram Bot API](https://core.telegram.org/bots/api)
- [Issues](https://github.com/Insaned79/mstc2tlgrm_bot/issues)
- [Pull Requests](https://github.com/Insaned79/mstc2tlgrm_bot/pulls)

---

## Обратная связь
Пишите вопросы и баги в [Issues](https://github.com/Insaned79/mstc2tlgrm_bot/issues) на GitHub. 