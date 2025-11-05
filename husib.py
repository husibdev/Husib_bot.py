import requests
import time

BOT_TOKEN = "7859158396:AAHssIxDFDcK-scB1ZOFGbiZhBOMKFy22Tc"
URL = f"https://api.telegram.org/bot{BOT_TOKEN}/"

PRICES = {
    "Prevyu": 15000,
    "Avatar": 10000,
    "Banner": 20000,
    "Other": 12000
}

carts = {}
last_update_id = 0


def get_updates():
    global last_update_id
    try:
        resp = requests.get(URL + "getUpdates", params={"offset": last_update_id + 1})
        data = resp.json()
        if "result" in data and data["result"]:
            for update in data["result"]:
                last_update_id = update["update_id"]
                handle_update(update)
    except Exception as e:
        print("Xato:", e)


def send_message(chat_id, text, reply_markup=None):
    data = {"chat_id": chat_id, "text": text, "parse_mode": "HTML"}
    if reply_markup:
        data["reply_markup"] = reply_markup
    requests.post(URL + "sendMessage", data=data)


def make_keyboard(buttons):
    return '{"keyboard":' + str(buttons).replace("'", '"') + ', "resize_keyboard":true}'


def handle_update(update):
    message = update.get("message")
    if not message:
        return

    chat_id = message["chat"]["id"]
    text = message.get("text", "")

    if text == "/start":
        buttons = [["Prevyu", "Avatar"], ["Banner", "Other"], ["🛒 Savat", "📞 Support"]]
        send_message(chat_id, "Salom! Men grafik dizayn zakaz botman 🎨", make_keyboard(buttons))

    elif text in PRICES:
        price = PRICES[text]
        buttons = [[f"{text} qo‘shish 🛒"], ["⬅️ Ortga"]]
        send_message(chat_id, f"{text} narxi: {price} so‘m", make_keyboard(buttons))

    elif text.endswith("qo‘shish 🛒"):
        item = text.split()[0]
        carts.setdefault(chat_id, []).append(item)
        send_message(chat_id, f"✅ {item} savatga qo‘shildi!")

    elif text == "🛒 Savat":
        items = carts.get(chat_id, [])
        if not items:
            send_message(chat_id, "Savat bo‘sh 🫠")
        else:
            total = sum(PRICES[i] for i in items)
            matn = "🛍 <b>Savatdagi mahsulotlar:</b>\n"
            for i in items:
                matn += f"• {i} — {PRICES[i]} so‘m\n"
            matn += f"\n<b>Jami:</b> {total} so‘m\n\nTo‘lov uchun @husib bilan bog‘laning 💳"
            send_message(chat_id, matn)

    elif text == "📞 Support":
        send_message(chat_id, "Bog‘lanish uchun: @husib")

    elif text == "⬅️ Ortga":
        buttons = [["Prevyu", "Avatar"], ["Banner", "Other"], ["🛒 Savat", "📞 Support"]]
        send_message(chat_id, "Asosiy menyu:", make_keyboard(buttons))


def main():
    print("✅ Bot ishga tushdi! Telegramni tekshiryapti...")
    while True:
        get_updates()
        time.sleep(1)


if __name__ == "__main__":
    main()