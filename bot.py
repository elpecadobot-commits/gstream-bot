import asyncio
import os
from aiohttp import web
from telegram import InlineKeyboardButton, InlineKeyboardMarkup, Update
from telegram.constants import ParseMode
from telegram.ext import (
    Application,
    CallbackQueryHandler,
    CommandHandler,
    ContextTypes,
)

TOKEN = "8731401630:AAGwJrBrFzg0IyhpTVCvMMswmQCXB7td51Q"
ADMIN_ID = 8431567592

CATALOGO = {
    "streaming": {
        "titulo": "Streaming y Cuentas",
        "productos": [
            {"id": "d_1m", "nombre": "Disney+ Premium (1 Mes)", "precio": "$35 MXN"},
            {"id": "d_6m", "nombre": "Disney+ Premium (6 Meses)", "precio": "$75 MXN"},
            {"id": "d_1a", "nombre": "Disney+ Premium (1 Año)", "precio": "$105 MXN"},
            {"id": "nf_std", "nombre": "Netflix Estándar Completa (1 Mes)", "precio": "$85 MXN"},
            {"id": "nf_4k", "nombre": "Netflix 4K Completa (1 Mes)", "precio": "$105 MXN"},
            {"id": "nf_perf", "nombre": "Netflix Perfil 4K (1 Mes)", "precio": "$20 MXN"},
            {"id": "vix_2m", "nombre": "ViX Premium (2 Meses)", "precio": "$15 MXN"},
            {"id": "vix_1a", "nombre": "ViX Premium (1 Año)", "precio": "$25 MXN"},
            {"id": "pv_1m", "nombre": "Prime Video (1 Mes)", "precio": "$35 MXN"},
            {"id": "pv_6m", "nombre": "Prime Video (6 Meses)", "precio": "$75 MXN"},
            {"id": "pv_perf", "nombre": "Prime Video Perfil (1 Mes)", "precio": "$15 MXN"},
            {"id": "hbo_std", "nombre": "HBO Max Estándar (1 Mes)", "precio": "$30 MXN"},
            {"id": "hbo_plat", "nombre": "HBO Max Platino (1 Mes)", "precio": "$45 MXN"},
            {"id": "hbo_p1m", "nombre": "HBO Max Perfil (1 Mes)", "precio": "$10 MXN"},
            {"id": "hbo_p6m", "nombre": "HBO Max Perfil (6 Meses)", "precio": "$75 MXN"},
            {"id": "hbo_p1a", "nombre": "HBO Max Perfil (1 Año)", "precio": "$105 MXN"},
            {"id": "cr_1m", "nombre": "Crunchyroll Mega Fan (1 Mes)", "precio": "$30 MXN"},
            {"id": "cr_1a", "nombre": "Crunchyroll Mega Fan (1 Año)", "precio": "$75 MXN"},
            {"id": "cr_perf", "nombre": "Crunchyroll Perfil (1 Mes)", "precio": "$8 MXN"},
            {"id": "pm_1m", "nombre": "Paramount+ (1 Mes)", "precio": "$18 MXN"},
            {"id": "pm_1a", "nombre": "Paramount+ (1 Año)", "precio": "$45 MXN"},
            {"id": "pm_perf", "nombre": "Paramount+ Perfil (1 Mes)", "precio": "$10 MXN"},
        ],
    },
    "musica": {
        "titulo": "Spotify Premium",
        "productos": [
            {"id": "sp_md_1m", "nombre": "Spotify Mi Dominio (1 Mes)", "precio": "$12 MXN"},
            {"id": "sp_md_3m", "nombre": "Spotify Mi Dominio (3 Meses)", "precio": "$25 MXN"},
            {"id": "sp_md_6m", "nombre": "Spotify Mi Dominio (6 Meses)", "precio": "$30 MXN"},
            {"id": "sp_md_1a", "nombre": "Spotify Mi Dominio (1 Año)", "precio": "$40 MXN"},
            {"id": "sp_td_1m", "nombre": "Spotify Tu Dominio (1 Mes)", "precio": "$15 MXN"},
            {"id": "sp_td_3m", "nombre": "Spotify Tu Dominio (3 Meses)", "precio": "$30 MXN"},
            {"id": "sp_td_6m", "nombre": "Spotify Tu Dominio (6 Meses)", "precio": "$35 MXN"},
            {"id": "sp_td_1a", "nombre": "Spotify Tu Dominio (1 Año)", "precio": "$45 MXN"},
        ],
    },
    "herramientas_ia": {
        "titulo": "IA, Programas y VPN",
        "productos": [
            {"id": "gemini_pro", "nombre": "Gemini Pro (18 Meses / 5 TB)", "precio": "$65 MXN"},
            {"id": "canva_1m", "nombre": "Canva Pro (1 Mes)", "precio": "$2 MXN"},
            {"id": "canva_2m", "nombre": "Canva Pro (2 Meses)", "precio": "$4 MXN"},
            {"id": "canva_3m", "nombre": "Canva Pro (3 Meses)", "precio": "$6 MXN"},
            {"id": "canva_5m", "nombre": "Canva Pro (5 Meses)", "precio": "$8 MXN"},
            {"id": "canva_1a", "nombre": "Canva Pro (1 Año)", "precio": "$15 MXN"},
            {"id": "ms_office", "nombre": "Office Completo (1 Año)", "precio": "$80 MXN"},
            {"id": "nord_6d", "nombre": "NordVPN 6 disp (1 Año)", "precio": "$45 MXN"},
            {"id": "nord_4d", "nombre": "NordVPN 4 disp (1 Año)", "precio": "$45 MXN"},
            {"id": "express_vpn", "nombre": "ExpressVPN Móvil (1 Año)", "precio": "$20 MXN"},
            {"id": "cyber_vpn", "nombre": "CyberGhost VPN (1 Año)", "precio": "$40 MXN"},
            {"id": "mullvad_vpn", "nombre": "Mullvad VPN (1 Año)", "precio": "$40 MXN"},
        ],
    },
    "gaming_redes": {
        "titulo": "Videojuegos y Redes",
        "productos": [
            {"id": "mc_pc", "nombre": "Minecraft Java+Bedrock PC", "precio": "$90 MXN"},
            {"id": "fn_800", "nombre": "Fortnite 800-1200 PaVos", "precio": "$100 MXN"},
            {"id": "fn_1500", "nombre": "Fortnite 1500-2800 PaVos", "precio": "$153 MXN"},
            {"id": "fn_5000", "nombre": "Fortnite 5000-8000 PaVos", "precio": "$640 MXN"},
            {"id": "ig_1k_nr", "nombre": "1000 Seguidores IG Sin Refill", "precio": "$22 MXN"},
            {"id": "ig_1k_wr", "nombre": "1000 Seguidores IG Con Refill", "precio": "$30 MXN"},
        ],
    },
}


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = update.effective_user
    texto = (
        f"👋 *Hola {user.first_name}*\n\n"
        f"🆔 *ID:* `{user.id}`\n\n"
        "🎉 *Bienvenido a GStreaming*\n"
        "Selecciona una categoría:"
    )
    teclado = [
        [InlineKeyboardButton("🎞️ Streaming y Cuentas", callback_data="cat_streaming")],
        [InlineKeyboardButton("🎵 Spotify Premium", callback_data="cat_musica")],
        [InlineKeyboardButton("💻 IA, Programas y VPN", callback_data="cat_herramientas_ia")],
        [InlineKeyboardButton("🎮 Gaming y Redes Sociales", callback_data="cat_gaming_redes")],
        [InlineKeyboardButton("💳 Métodos de Pago", callback_data="info_pagos")],
        [InlineKeyboardButton("❌ Cerrar menú", callback_data="cerrar")],
    ]
    markup = InlineKeyboardMarkup(teclado)

    if update.callback_query:
        await update.callback_query.message.edit_text(
            texto, reply_markup=markup, parse_mode=ParseMode.MARKDOWN
        )
    else:
        await update.message.reply_text(
            texto, reply_markup=markup, parse_mode=ParseMode.MARKDOWN
        )


async def mostrar_seccion(update: Update, context: ContextTypes.DEFAULT_TYPE, clave: str):
    query = update.callback_query
    await query.answer()

    seccion = CATALOGO.get(clave)
    if not seccion:
        return

    texto = f"📦 *{seccion['titulo'].upper()}*\n\nSelecciona el servicio que deseas solicitar:\n\n"
    teclado = []

    for item in seccion["productos"]:
        texto += f"• *{item['nombre']}* — `{item['precio']}`\n"
        teclado.append(
            [InlineKeyboardButton(f"🛒 Pedir: {item['nombre']}", callback_data=f"pedir_{item['id']}")]
        )

    teclado.append([InlineKeyboardButton("🏠 Volver al inicio", callback_data="inicio")])
    teclado.append([InlineKeyboardButton("❌ Cerrar menú", callback_data="cerrar")])

    await query.message.edit_text(
        texto,
        reply_markup=InlineKeyboardMarkup(teclado),
        parse_mode=ParseMode.MARKDOWN,
    )


async def procesar_pedido(update: Update, context: ContextTypes.DEFAULT_TYPE, item_id: str):
    query = update.callback_query
    user = update.effective_user
    await query.answer()

    producto = None
    for sec in CATALOGO.values():
        for p in sec["productos"]:
            if p["id"] == item_id:
                producto = p
                break

    if not producto:
        return

    texto_cliente = (
        f"✅ *SOLICITUD GENERADA*\n\n"
        f"📦 *Producto:* {producto['nombre']}\n"
        f"💵 *Monto:* {producto['precio']}\n\n"
        "📌 *Instrucciones para completar el pedido:*\n"
        "1. Realiza tu pago mediante transferencia bancaria (SPEI / OXXO / Mercado Pago).\n"
        "2. Toca el botón de abajo para enviar tu comprobante al administrador.\n"
        "3. El administrador validará el pago y te entregará tu acceso."
    )

    teclado = [
        [
            InlineKeyboardButton(
                "💬 Enviar Comprobante al Admin",
                url=f"tg://user?id={ADMIN_ID}",
            )
        ],
        [InlineKeyboardButton("🏠 Volver al menú principal", callback_data="inicio")],
    ]

    await query.message.edit_text(
        texto_cliente,
        reply_markup=InlineKeyboardMarkup(teclado),
        parse_mode=ParseMode.MARKDOWN,
    )

    try:
        await context.bot.send_message(
            chat_id=ADMIN_ID,
            text=(
                f"🚨 *NUEVO PEDIDO RECIBIDO*\n\n"
                f"👤 *Cliente:* {user.full_name} (@{user.username or 'Sin alias'})\n"
                f"🆔 *ID del Cliente:* `{user.id}`\n"
                f"📦 *Producto:* {producto['nombre']}\n"
                f"💰 *Total:* {producto['precio']}"
            ),
            parse_mode=ParseMode.MARKDOWN,
        )
    except Exception:
        pass


async def info_pagos(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    texto = (
        "💳 *FORMAS DE PAGO*\n\n"
        "• Transferencia bancaria en pesos mexicanos (MXN)\n"
        "• SPEI / OXXO / Mercado Pago\n\n"
        "Envía tu comprobante de pago al realizar tu pedido para agilizar la entrega."
    )
    teclado = [[InlineKeyboardButton("↩️ Volver", callback_data="inicio")]]
    await query.message.edit_text(
        texto, reply_markup=InlineKeyboardMarkup(teclado), parse_mode=ParseMode.MARKDOWN
    )


async def cerrar_menu(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    await query.message.delete()


async def handler_callback(update: Update, context: ContextTypes.DEFAULT_TYPE):
    data = update.callback_query.data
    if data == "inicio":
        await start(update, context)
    elif data.startswith("cat_"):
        await mostrar_seccion(update, context, data.replace("cat_", ""))
    elif data.startswith("pedir_"):
        await procesar_pedido(update, context, data.replace("pedir_", ""))
    elif data == "info_pagos":
        await info_pagos(update, context)
    elif data == "cerrar":
        await cerrar_menu(update, context)


async def handle_ping(request):
    return web.Response(text="Bot is running!")


async def run_web_server():
    app = web.Application()
    app.router.add_get("/", handle_ping)
    port = int(os.environ.get("PORT", 8080))
    runner = web.AppRunner(app)
    await runner.setup()
    site = web.TCPSite(runner, "0.0.0.0", port)
    await site.start()


async def main():
    await run_web_server()

    app = Application.builder().token(TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CallbackQueryHandler(handler_callback))

    await app.initialize()
    await app.start()
    await app.updater.start_polling()

    while True:
        await asyncio.sleep(3600)


if __name__ == "__main__":
    asyncio.run(main())