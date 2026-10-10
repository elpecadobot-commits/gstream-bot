import asyncio
import os
import re
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
            {"id": "d_1m", "nombre": "Disney+ (1 Mes)", "precio_str": "$45 MXN", "precio_num": 45},
            {"id": "d_6m", "nombre": "Disney+ (6 Meses)", "precio_str": "$95 MXN", "precio_num": 95},
            {"id": "d_1a", "nombre": "Disney+ (1 Año)", "precio_str": "$150 MXN", "precio_num": 150},
            {"id": "nf_std", "nombre": "Netflix Estándar (1 Mes)", "precio_str": "$95 MXN", "precio_num": 95},
            {"id": "nf_4k", "nombre": "Netflix 4K (1 Mes)", "precio_str": "$150 MXN", "precio_num": 150},
            {"id": "nf_perf", "nombre": "Netflix Perfil 4K (1 Mes)", "precio_str": "$40 MXN", "precio_num": 40},
            {"id": "vix_2m", "nombre": "ViX Premium (2 Meses)", "precio_str": "$30 MXN", "precio_num": 30},
            {"id": "vix_1a", "nombre": "ViX Premium (1 Año)", "precio_str": "$40 MXN", "precio_num": 40},
            {"id": "pv_1m", "nombre": "Prime Video (1 Mes)", "precio_str": "$45 MXN", "precio_num": 45},
            {"id": "pv_6m", "nombre": "Prime Video (6 Meses)", "precio_str": "$95 MXN", "precio_num": 95},
            {"id": "pv_perf", "nombre": "Prime Video Perfil (1 Mes)", "precio_str": "$20 MXN", "precio_num": 20},
            {"id": "hbo_std", "nombre": "HBO Max Estándar (1 Mes)", "precio_str": "$40 MXN", "precio_num": 40},
            {"id": "hbo_plat", "nombre": "HBO Max Platino (1 Mes)", "precio_str": "$55 MXN", "precio_num": 55},
            {"id": "hbo_p1m", "nombre": "HBO Perfil (1 Mes)", "precio_str": "$20 MXN", "precio_num": 20},
            {"id": "hbo_p6m", "nombre": "HBO Perfil (6 Meses)", "precio_str": "$100 MXN", "precio_num": 100},
            {"id": "hbo_p1a", "nombre": "HBO Perfil (1 Año)", "precio_str": "$150 MXN", "precio_num": 150},
            {"id": "cr_1m", "nombre": "Crunchyroll Mega Fan (1 Mes)", "precio_str": "$40 MXN", "precio_num": 40},
            {"id": "cr_1a", "nombre": "Crunchyroll Mega Fan (1 Año)", "precio_str": "$100 MXN", "precio_num": 100},
            {"id": "cr_perf", "nombre": "Crunchyroll Perfil (1 Mes)", "precio_str": "$15 MXN", "precio_num": 15},
            {"id": "pm_1m", "nombre": "Paramount+ (1 Mes)", "precio_str": "$40 MXN", "precio_num": 40},
            {"id": "pm_1a", "nombre": "Paramount+ (1 Año)", "precio_str": "$80 MXN", "precio_num": 80},
            {"id": "pm_perf", "nombre": "Paramount+ Perfil (1 Mes)", "precio_str": "$20 MXN", "precio_num": 20},
        ],
    },
    "musica": {
        "titulo": "Spotify Premium",
        "productos": [
            {"id": "sp_md_1m", "nombre": "Spotify Mi Dominio (1 Mes)", "precio_str": "$20 MXN", "precio_num": 20},
            {"id": "sp_md_3m", "nombre": "Spotify Mi Dominio (3 Meses)", "precio_str": "$45 MXN", "precio_num": 45},
            {"id": "sp_md_6m", "nombre": "Spotify Mi Dominio (6 Meses)", "precio_str": "$55 MXN", "precio_num": 55},
            {"id": "sp_md_1a", "nombre": "Spotify Mi Dominio (1 Año)", "precio_str": "$90 MXN", "precio_num": 90},
            {"id": "sp_td_1m", "nombre": "Spotify Tu Dominio (1 Mes)", "precio_str": "$40 MXN", "precio_num": 40},
            {"id": "sp_td_3m", "nombre": "Spotify Tu Dominio (3 Meses)", "precio_str": "$80 MXN", "precio_num": 80},
            {"id": "sp_td_6m", "nombre": "Spotify Tu Dominio (6 Meses)", "precio_str": "$100 MXN", "precio_num": 100},
            {"id": "sp_td_1a", "nombre": "Spotify Tu Dominio (1 Año)", "precio_str": "$180 MXN", "precio_num": 180},
        ],
    },
    "herramientas_ia": {
        "titulo": "IA, Software y VPN",
        "productos": [
            {"id": "gemini_pro", "nombre": "Gemini Pro (18M / 5 TB)", "precio_str": "$85 MXN", "precio_num": 85},
            {"id": "canva_1m", "nombre": "Canva Pro (1 Mes)", "precio_str": "$10 MXN", "precio_num": 10},
            {"id": "canva_2m", "nombre": "Canva Pro (2 Meses)", "precio_str": "$15 MXN", "precio_num": 15},
            {"id": "canva_3m", "nombre": "Canva Pro (3 Meses)", "precio_str": "$20 MXN", "precio_num": 20},
            {"id": "canva_5m", "nombre": "Canva Pro (5 Meses)", "precio_str": "$25 MXN", "precio_num": 25},
            {"id": "canva_1a", "nombre": "Canva Pro (1 Año)", "precio_str": "$35 MXN", "precio_num": 35},
            {"id": "ms_office", "nombre": "Microsoft Office (1 Año)", "precio_str": "$100 MXN", "precio_num": 100},
            {"id": "nord_6d", "nombre": "NordVPN 6 disp (1 Año)", "precio_str": "$65 MXN", "precio_num": 65},
            {"id": "nord_4d", "nombre": "NordVPN 4 disp (1 Año)", "precio_str": "$65 MXN", "precio_num": 65},
            {"id": "express_vpn", "nombre": "ExpressVPN Móvil (1 Año)", "precio_str": "$40 MXN", "precio_num": 40},
            {"id": "cyber_vpn", "nombre": "CyberGhost VPN (1 Año)", "precio_str": "$60 MXN", "precio_num": 60},
            {"id": "mullvad_vpn", "nombre": "Mullvad VPN (1 Año)", "precio_str": "$60 MXN", "precio_num": 60},
        ],
    },
    "gaming_redes": {
        "titulo": "Gaming y Redes Sociales",
        "productos": [
            {"id": "mc_pc", "nombre": "Minecraft Java+Bedrock PC", "precio_str": "$150 MXN", "precio_num": 150},
            {"id": "fn_800", "nombre": "Fortnite 800-1200 PaVos", "precio_str": "$120 MXN", "precio_num": 120},
            {"id": "fn_1500", "nombre": "Fortnite 1500-2800 PaVos", "precio_str": "$180 MXN", "precio_num": 180},
            {"id": "fn_5000", "nombre": "Fortnite 5000-8000 PaVos", "precio_str": "$740 MXN", "precio_num": 740},
            {"id": "ig_1k_nr", "nombre": "1k Seguidores IG (Sin refill)", "precio_str": "$35 MXN", "precio_num": 35},
            {"id": "ig_1k_wr", "nombre": "1k Seguidores IG (Con refill)", "precio_str": "$50 MXN", "precio_num": 50},
        ],
    },
    "servicios": {
        "titulo": "Pago de Servicios",
        "productos": [
            {"id": "srv_cfe", "nombre": "CFE / Luz", "precio_str": "Cotizar", "precio_num": 0},
            {"id": "srv_telmex", "nombre": "Telmex / Infinitum", "precio_str": "Cotizar", "precio_num": 0},
            {"id": "srv_izzi", "nombre": "izzi Telecom", "precio_str": "Cotizar", "precio_num": 0},
            {"id": "srv_megacable", "nombre": "Megacable", "precio_str": "Cotizar", "precio_num": 0},
            {"id": "srv_totalplay", "nombre": "Totalplay", "precio_str": "Cotizar", "precio_num": 0},
            {"id": "srv_movil", "nombre": "Telefonía (Telcel/AT&T/Movistar)", "precio_str": "Cotizar", "precio_num": 0},
            {"id": "srv_tiendas", "nombre": "Créditos (Mercado Pago/Kueski)", "precio_str": "Cotizar", "precio_num": 0},
        ],
    },
    "vuelos": {
        "titulo": "Vuelos con Descuento",
        "productos": [
            {"id": "vue_viva", "nombre": "Viva Aerobus (Hasta 50%)", "precio_str": "Cotizar", "precio_num": 0},
            {"id": "vue_volaris", "nombre": "Volaris (Hasta 50%)", "precio_str": "Cotizar", "precio_num": 0},
            {"id": "vue_aero", "nombre": "Aeroméxico (Hasta 50%)", "precio_str": "Cotizar", "precio_num": 0},
        ],
    },
}

def buscar_producto(item_id):
    for sec in CATALOGO.values():
        for p in sec["productos"]:
            if p["id"] == item_id:
                return p
    return None

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = update.effective_user
    carrito = context.user_data.get("carrito", {})
    total_items = sum(carrito.values())

    texto = (
        "🔥 *GSTREAMING — TIENDA DIGITAL* 🔥\n\n"
        "👻 *¡Precios de miedo, entretenimiento de otro mundo!* 🛸\n\n"
        "Tu portal de confianza para cuentas de streaming, licencias oficiales, VPNs y servicios digitales al mejor precio del mercado con activación rápida y garantía.\n\n"
        "👤 *Cliente:* " + str(user.first_name) + "\n"
        "🆔 *ID:* `" + str(user.id) + "`\n"
        "🛒 *Artículos en carrito:* " + str(total_items) + "\n\n"
        "Explora nuestras categorías y arma tu pedido:"
    )

    teclado = [
        [InlineKeyboardButton("🎞️ Streaming y Cuentas", callback_data="cat_streaming")],
        [InlineKeyboardButton("🎵 Spotify Premium", callback_data="cat_musica")],
        [InlineKeyboardButton("💻 IA, Programas y VPN", callback_data="cat_herramientas_ia")],
        [InlineKeyboardButton("🎮 Gaming y Redes Sociales", callback_data="cat_gaming_redes")],
        [InlineKeyboardButton("⚡ Pago de Servicios", callback_data="cat_servicios")],
        [InlineKeyboardButton("✈️ Vuelos con Descuento", callback_data="cat_vuelos")],
        [InlineKeyboardButton("🛒 Ver Carrito (" + str(total_items) + ")", callback_data="ver_carrito")],
        [InlineKeyboardButton("💳 Métodos de Pago", callback_data="info_pagos")],
        [InlineKeyboardButton("❌ Cerrar menú", callback_data="cerrar")],
    ]
    markup = InlineKeyboardMarkup(teclado)

    if update.callback_query:
        try:
            await update.callback_query.message.edit_text(
                texto, reply_markup=markup, parse_mode=ParseMode.MARKDOWN
            )
        except Exception:
            await update.callback_query.message.reply_text(
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

    carrito = context.user_data.get("carrito", {})
    total_items = sum(carrito.values())

    texto = (
        "📦 *" + seccion["titulo"].upper() + "*\n\n"
        "Toca un producto para añadirlo a tu carrito 🛒:"
    )
    teclado = []

    for item in seccion["productos"]:
        cant = carrito.get(item["id"], 0)
        marca_cant = " [" + str(cant) + " en carrito]" if cant > 0 else ""
        etiqueta_boton = "➕ " + item["nombre"] + " • " + item["precio_str"] + marca_cant
        teclado.append(
            [InlineKeyboardButton(etiqueta_boton, callback_data="add_" + item["id"] + "_" + clave)]
        )

    teclado.append([InlineKeyboardButton("🛒 Ver Carrito (" + str(total_items) + ")", callback_data="ver_carrito")])
    teclado.append([InlineKeyboardButton("🏠 Volver al inicio", callback_data="inicio")])
    teclado.append([InlineKeyboardButton("❌ Cerrar", callback_data="cerrar")])

    try:
        await query.message.edit_text(
            texto,
            reply_markup=InlineKeyboardMarkup(teclado),
            parse_mode=ParseMode.MARKDOWN,
        )
    except Exception:
        pass

async def agregar_carrito(update: Update, context: ContextTypes.DEFAULT_TYPE, data: str):
    query = update.callback_query
    # formato data: add_<item_id>_<clave_categoria>
    partes = data.split("_", 2)
    if len(partes) < 3:
        await query.answer("Error al agregar producto")
        return
    item_id = partes[1]
    clave = partes[2]

    if "carrito" not in context.user_data:
        context.user_data["carrito"] = {}

    context.user_data["carrito"][item_id] = context.user_data["carrito"].get(item_id, 0) + 1

    prod = buscar_producto(item_id)
    nombre = prod["nombre"] if prod else "Producto"
    await query.answer("Agregado al carrito: " + nombre)

    # Refresca la vista de la sección
    await mostrar_seccion(update, context, clave)

async def ver_carrito(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()

    carrito = context.user_data.get("carrito", {})

    if not carrito or sum(carrito.values()) == 0:
        texto = (
            "🛒 *TU CARRITO DE COMPRAS*\n\n"
            "Tu carrito está actualmente vacío.\n"
            "Explora el catálogo y añade los servicios que deseas adquirir."
        )
        teclado = [
            [InlineKeyboardButton("🏠 Volver al catálogo", callback_data="inicio")],
        ]
        try:
            await query.message.edit_text(
                texto, reply_markup=InlineKeyboardMarkup(teclado), parse_mode=ParseMode.MARKDOWN
            )
        except Exception:
            pass
        return

    texto = "🛒 *RESUMEN DE TU CARRITO:*\n\n"
    total_pesos = 0
    hay_cotizacion = False

    for item_id, cantidad in list(carrito.items()):
        prod = buscar_producto(item_id)
        if prod:
            if prod["precio_num"] > 0:
                subtotal = prod["precio_num"] * cantidad
                total_pesos += subtotal
                texto += "• *" + prod["nombre"] + "* x" + str(cantidad) + " — `$" + str(subtotal) + " MXN`\n"
            else:
                hay_cotizacion = True
                texto += "• *" + prod["nombre"] + "* x" + str(cantidad) + " — *(Cotización)*\n"

    texto += "\n━━━━━━━━━━━━━━━━━━━\n"
    texto += "💰 *TOTAL A PAGAR:* `$" + str(total_pesos) + " MXN`"
    if hay_cotizacion:
        texto += " *(+ servicios por cotizar)*"

    texto += (
        "\n\n🏦 *Datos para transferencia STP:*\n"
        "• CLABE: `646180402346077527`\n"
        "• Titular: *YOLANDA ARREDONDO MICHEL*\n\n"
        "📌 *¿Listo para ordenar?* Toca *Confirmar y Enviar Pedido* para generar tu orden con el administrador."
    )

    teclado = [
        [InlineKeyboardButton("✅ Confirmar y Enviar Pedido", callback_data="confirmar_pedido")],
        [InlineKeyboardButton("🗑️ Vaciar Carrito", callback_data="vaciar_carrito")],
        [InlineKeyboardButton("➕ Seguir Comprando", callback_data="inicio")],
        [InlineKeyboardButton("❌ Cerrar", callback_data="cerrar")],
    ]

    try:
        await query.message.edit_text(
            texto, reply_markup=InlineKeyboardMarkup(teclado), parse_mode=ParseMode.MARKDOWN
        )
    except Exception:
        pass

async def vaciar_carrito(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    context.user_data["carrito"] = {}
    await query.answer("Carrito vaciado")
    await start(update, context)

async def confirmar_pedido(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    user = update.effective_user
    await query.answer()

    carrito = context.user_data.get("carrito", {})
    if not carrito:
        await query.answer("El carrito está vacío.")
        await start(update, context)
        return

    resumen_items = ""
    total_pesos = 0
    hay_cotizacion = False

    for item_id, cantidad in list(carrito.items()):
        prod = buscar_producto(item_id)
        if prod:
            if prod["precio_num"] > 0:
                sub = prod["precio_num"] * cantidad
                total_pesos += sub
                resumen_items += "• " + prod["nombre"] + " x" + str(cantidad) + " = $" + str(sub) + " MXN\n"
            else:
                hay_cotizacion = True
                resumen_items += "• " + prod["nombre"] + " x" + str(cantidad) + " (Cotización requerida)\n"

    texto_cliente = (
        "🎉 *¡PEDIDO GENERADO CON ÉXITO!*\n\n"
        "📦 *Tu orden incluye:*\n" + resumen_items + "\n"
        "💰 *TOTAL A PAGAR:* `$" + str(total_pesos) + " MXN`\n\n"
        "🏦 *Cuenta STP para pago:*\n"
        "• CLABE: `646180402346077527` (Toca para copiar)\n"
        "• Titular: *YOLANDA ARREDONDO MICHEL*\n\n"
        "📩 *Pasos para recibir tu pedido:*\n"
        "1. Realiza tu transferencia por el monto exacto.\n"
        "2. Toca el botón abajo para abrir chat con el administrador y mandar tu comprobante de pago."
    )

    teclado = [
        [
            InlineKeyboardButton(
                "💬 Enviar Comprobante al Admin",
                url="tg://user?id=" + str(ADMIN_ID),
            )
        ],
        [InlineKeyboardButton("🏠 Menú Principal", callback_data="inicio")],
    ]

    # Notificar al Administrador en un solo mensaje detallado
    alias = user.username if user.username else "Sin alias"
    aviso_admin = (
        "🚨 *NUEVO PEDIDO MULTIPRODUCTO RECIBIDO*\n\n"
        "👤 *Cliente:* " + str(user.full_name) + " (@" + alias + ")\n"
        "🆔 *ID Telegram:* `" + str(user.id) + "`\n\n"
        "🛒 *Detalle de compra:*\n" + resumen_items + "\n"
        "💵 *TOTAL A COBRAR:* $" + str(total_pesos) + " MXN"
    )
    if hay_cotizacion:
        aviso_admin += " (+ productos a cotizar)"

    try:
        await context.bot.send_message(
            chat_id=ADMIN_ID,
            text=aviso_admin,
            parse_mode=ParseMode.MARKDOWN,
        )
    except Exception:
        pass

    # Limpiar carrito tras confirmar
    context.user_data["carrito"] = {}

    try:
        await query.message.edit_text(
            texto_cliente,
            reply_markup=InlineKeyboardMarkup(teclado),
            parse_mode=ParseMode.MARKDOWN,
        )
    except Exception:
        pass

async def info_pagos(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    texto = (
        "💳 *FORMAS DE PAGO*\n\n"
        "🏦 *Entidad / Banco:* STP\n"
        "👤 *Titular:* YOLANDA ARREDONDO MICHEL\n"
        "🔢 *Cuenta CLABE:* `646180402346077527`\n\n"
        "📌 *Instrucciones:*\n"
        "• Transferencia bancaria directa (SPEI / OXXO / Mercado Pago).\n"
        "• Toca la CLABE para copiarla automáticamente.\n"
        "• Guarda y envía tu comprobante para activar tu servicio de inmediato."
    )
    teclado = [[InlineKeyboardButton("↩️ Volver al inicio", callback_data="inicio")]]
    try:
        await query.message.edit_text(
            texto, reply_markup=InlineKeyboardMarkup(teclado), parse_mode=ParseMode.MARKDOWN
        )
    except Exception:
        pass

async def cerrar_menu(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    try:
        await query.message.delete()
    except Exception:
        pass

async def handler_callback(update: Update, context: ContextTypes.DEFAULT_TYPE):
    data = update.callback_query.data
    if data == "inicio":
        await start(update, context)
    elif data.startswith("cat_"):
        await mostrar_seccion(update, context, data.replace("cat_", ""))
    elif data.startswith("add_"):
        await agregar_carrito(update, context, data)
    elif data == "ver_carrito":
        await ver_carrito(update, context)
    elif data == "vaciar_carrito":
        await vaciar_carrito(update, context)
    elif data == "confirmar_pedido":
        await confirmar_pedido(update, context)
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
    app.add_handler(CommandHandler("carrito", ver_carrito))
    app.add_handler(CallbackQueryHandler(handler_callback))

    await app.initialize()
    await app.start()
    await app.updater.start_polling()

    while True:
        await asyncio.sleep(3600)

if __name__ == "__main__":
    asyncio.run(main())