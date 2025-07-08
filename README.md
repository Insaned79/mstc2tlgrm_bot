# mstc2tlgrm_bot

![Python](https://img.shields.io/badge/python-3.8%2B-blue)
![License](https://img.shields.io/github/license/Insaned79/mstc2tlgrm_bot)

---

## 📑 Оглавление
- [⚠️ Важно](#️-важно)
- [📝 Описание](#-описание)
- [🚀 Быстрый старт](#-быстрый-старт)
- [⚙️ Пример конфига](#-пример-конфига)
- [🗂 Структура файлов](#-структура-файлов)
- [🖼 Пример работы](#-пример-работы)
- [🛠 TODO / Планы](#-todo--планы)
- [🔗 Полезные ссылки](#-полезные-ссылки)
- [💬 Обратная связь](#-обратная-связь)

---

## ⚠️ Важно
**Проект находится в активной разработке и может быть нестабилен. Используйте на свой страх и риск.**

---

## 📝 Описание
Бот для пересылки сообщений из сети Meshtastic в Telegram. Поддерживает работу с несколькими нодами, защиту от дублей, подробное логирование и простую настройку через конфиг.

---

## 🚀 Быстрый старт
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

## ⚙️ Пример конфига
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

## 🗂 Структура файлов
- `tg_meshtastic_forwarder.py` — основной бот-пересылщик
- `log_mqtt.py`, `log_mqtt_bin.py` — логгеры для отладки
- `config.py.example` — пример конфига
- `requirements.txt` — зависимости
- [`LICENSE`](LICENSE) — лицензия

---

## 🖼 Пример работы
*Скриншот работы бота в Telegram (пример):*
```
[Telegram]
Text message from 1234567890 to 4294967295: <b>Hello from Meshtastic!</b>
RSSI: -120 | Hop start: 2 | Hops away: 1 | Time: 2025-07-08 09:00:09
```

---

## 🛠 TODO / Планы
- [ ] Улучшить обработку ошибок и диагностику
- [ ] Добавить поддержку TLS для MQTT
- [ ] Автоматическое определение пользователей Meshtastic
- [ ] Веб-интерфейс для управления подписками
- [ ] CI/CD для автоматической проверки
- [ ] Документация по интеграции с другими системами

---

## 🔗 Полезные ссылки
- [Meshtastic](https://meshtastic.org/)
- [Telegram Bot API](https://core.telegram.org/bots/api)
- [Issues](https://github.com/Insaned79/mstc2tlgrm_bot/issues)
- [Pull Requests](https://github.com/Insaned79/mstc2tlgrm_bot/pulls)

---

## 💬 Обратная связь
Пишите вопросы и баги в [Issues](https://github.com/Insaned79/mstc2tlgrm_bot/issues) на GitHub.


---

# mstc2tlgrm_bot

![Python](https://img.shields.io/badge/python-3.8%2B-blue)
![License](https://img.shields.io/github/license/Insaned79/mstc2tlgrm_bot)

---

## 📑 Table of Contents
- [⚠️ Important](#️-important)
- [📝 Description](#-description)
- [🚀 Quick Start](#-quick-start)
- [⚙️ Config Example](#-config-example)
- [🗂 File Structure](#-file-structure)
- [🖼 Example Output](#-example-output)
- [🛠 TODO / Plans](#-todo--plans)
- [🔗 Useful Links](#-useful-links)
- [💬 Feedback](#-feedback)

---

## ⚠️ Important
**This project is under active development and may be unstable. Use at your own risk.**

---

## 📝 Description
A bot for forwarding messages from the Meshtastic network to Telegram. Supports multiple nodes, deduplication, detailed logging, and easy configuration.

---

## 🚀 Quick Start
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

## ⚙️ Config Example
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

## 🗂 File Structure
- `tg_meshtastic_forwarder.py` — main forwarder bot
- `log_mqtt.py`, `log_mqtt_bin.py` — loggers for debugging
- `config.py.example` — config example
- `requirements.txt` — dependencies
- [`LICENSE`](LICENSE) — license

---

## 🖼 Example Output
*Sample output in Telegram:*
```
[Telegram]
Text message from 1234567890 to 4294967295: <b>Hello from Meshtastic!</b>
RSSI: -120 | Hop start: 2 | Hops away: 1 | Time: 2025-07-08 09:00:09
```

---

## 🛠 TODO / Plans
- [ ] Improve error handling and diagnostics
- [ ] Add TLS support for MQTT
- [ ] Automatic Meshtastic user detection
- [ ] Web interface for subscription management
- [ ] CI/CD for automated checks
- [ ] Integration documentation

---

## 🔗 Useful Links
- [Meshtastic](https://meshtastic.org/)
- [Telegram Bot API](https://core.telegram.org/bots/api)
- [Issues](https://github.com/Insaned79/mstc2tlgrm_bot/issues)
- [Pull Requests](https://github.com/Insaned79/mstc2tlgrm_bot/pulls)

---

## 💬 Feedback
Please use [Issues](https://github.com/Insaned79/mstc2tlgrm_bot/issues) on GitHub for questions and bug reports. 