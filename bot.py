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
        f"🆔 *ID:*