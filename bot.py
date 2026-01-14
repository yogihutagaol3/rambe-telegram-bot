
from telegram import (
    InlineKeyboardButton,
    InlineKeyboardMarkup,
    ReplyKeyboardMarkup,
    InputMediaPhoto
)
from telegram.ext import (
    Updater,
    CommandHandler,
    MessageHandler,
    Filters,
    CallbackQueryHandler
)


TOKEN = "8260828098:AAFj8fWNqp6OISNOsEPDeA0EWV1f5tbp9_I"
NO_WA = "6285821952414"  # ganti nomor WA admin


# ================= START =================
def start(update, context):
    menu = [
        ["🏨 Tipe Kamar"],
        ["💰 Harga", "🛎️ Fasilitas"],
        ["🏞️ View Pemandangan"],
        ["📍 Alamat", "📲 Booking"]
    ]

    update.message.reply_text(
        "👋 *Selamat Datang di Homestay Kami*\n\n"
        "Kami siap membantu kebutuhan menginap Anda 😊\n\n"
        "Silakan pilih menu atau ketik pertanyaan:",
        reply_markup=ReplyKeyboardMarkup(menu, resize_keyboard=True),
        parse_mode="Markdown"
    )

# ================= HANDLE CHAT =================
def handle_message(update, context):
    text = update.message.text.lower()
    chat_id = update.message.chat_id

    # ---- TIPE KAMAR ----
    if "kamar" in text or "tipe" in text:
        keyboard = [
            [InlineKeyboardButton("🛏️ Standar", callback_data="standar")],
            [InlineKeyboardButton("🛏️ Superior", callback_data="superior")],
            [InlineKeyboardButton("🛏️ Deluxe", callback_data="deluxe")]
        ]
        update.message.reply_text(
            "🏨 *Silakan pilih tipe kamar:*",
            reply_markup=InlineKeyboardMarkup(keyboard),
            parse_mode="Markdown"
        )

    # ---- HARGA ----
    elif "harga" in text or "tarif" in text:
        update.message.reply_text(
            "💰 *Daftar Harga Kamar*\n\n"
            "🏨 Standar  : Rp300.000 / malam\n"
            "🏨 Superior : Rp450.000 / malam\n"
            "🏨 Deluxe   : Rp600.000 / malam\n\n"
            "Ketik *booking* untuk memesan kamar 😊",
            parse_mode="Markdown"
        )

    # ---- FASILITAS ----
    elif "fasilitas" in text:
        update.message.reply_text(
            "🛎️ *Fasilitas Homestay*\n\n"
            "✅ AC\n"
            "✅ TV\n"
            "✅ WiFi\n"
            "✅ Kamar mandi dalam\n"
            "✅ Air panas (Superior & Deluxe)\n"
            "✅ Snorkling\n"
            "✅ Barbeque",
            parse_mode="Markdown"
        )

    # ---- VIEW ----
    elif "view" in text or "pemandangan" in text:
        media = [
            InputMediaPhoto(open("foto/ok.jpg", "rb"), caption="🏞️ View pemandangan sekitar homestay"),
            InputMediaPhoto(open("foto/no.jpg", "rb")),
            InputMediaPhoto(open("foto/vs.jpg", "rb"))
        ]
        context.bot.send_media_group(chat_id=chat_id, media=media)

    # ---- ALAMAT ----
    elif "alamat" in text or "lokasi" in text:
        update.message.reply_text(
            "📍 *Alamat Homestay*\n\n"
            "Teluk Melinau\n"
            "Pulau Lemukutan,\n"
            "Kabupaten Bengkayang",
            parse_mode="Markdown"
        )

    # ---- BOOKING ----
    elif "booking" in text or "pesan" in text:
        wa_link = f"https://wa.me/6285821952414?text=Halo%20saya%20ingin%20booking%20kamar"
        keyboard = [[InlineKeyboardButton("📲 Booking via WhatsApp", url=wa_link)]]
        update.message.reply_text(
            "Silakan klik tombol di bawah untuk booking 👇",
            reply_markup=InlineKeyboardMarkup(keyboard)
        )

    # ---- SAPAAN ----
    elif "halo" in text or "hai" in text:
        update.message.reply_text(
            "Halo 👋\nSilakan tanya *harga*, *fasilitas*, atau *booking* 😊",
            parse_mode="Markdown"
        )

    # ---- DEFAULT ----
    
        
    if "terimakasih" in text or "makasih" in text or "terimakasih" in text or "thanks" in text:
        update.message.reply_text(
            "bapak-ibu makan kurma di kos SAMA-SAMA BOS🤣😂",
            parse_mode="Markdown"
        )

# ================= BUTTON KAMAR =================
def button_handler(update, context):
    query = update.callback_query
    query.answer()
    chat_id = query.message.chat_id

    if query.data == "standar":
        photo = "foto/ygi.jpg"
        nama = "Standar"
        harga = "Rp300.000 / malam"
        fasilitas = "Kipas Angin, Air Mineral, Maks 3 Org"

    elif query.data == "superior":
        photo = "foto/images.jpg"
        nama = "Superior"
        harga = "Rp450.000 / malam"
        fasilitas = "AC, TV, Air Mineral, Air panas, Breakfast, Maks 6 Org, Wifi "

    elif query.data == "deluxe":
        photo = "foto/yhi.jpg"
        nama = "Deluxe"
        harga = "Rp600.000 / malam"
        fasilitas = "AC, TV,Air Mineral, Air panas, Breakfast, Wifi, Barbeque, Untuk Keluarga Besar"

    wa_text = f"Halo admin, saya ingin booking kamar {nama}"
    wa_link = f"https://wa.me/6285821952414?text={wa_text.replace(' ', '%20')}"

    keyboard = [[InlineKeyboardButton("📲 Booking via WhatsApp", url=wa_link)]]

    context.bot.send_photo(
        chat_id=chat_id,
        photo=open(photo, "rb"),
        caption=(
            f"🏨 *Kamar {nama}*\n"
            f"💰 {harga}\n\n"
            f"🛎️ Fasilitas:\n{fasilitas}\n\n"
            "🙏 Terima kasih telah menghubungi kami"
        ),
        parse_mode="Markdown",
        reply_markup=InlineKeyboardMarkup(keyboard)
    )

# ================= MAIN =================
def main():
    updater = Updater(TOKEN, use_context=True)
    dp = updater.dispatcher

    dp.add_handler(CommandHandler("start", start))
    dp.add_handler(CallbackQueryHandler(button_handler))
    dp.add_handler(MessageHandler(Filters.text & ~Filters.command, handle_message))

    updater.start_polling()
    updater.idle()

if __name__ == "__main__":
    main()