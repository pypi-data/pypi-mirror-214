from importlib import import_module
from platform import python_version

from haidar import *
from haidar.config import *
from haidar.modules import loadPremiumModule, loadBasicModule, loadMediumModule
from pyrogram import __version__
from pyrogram.types import InlineKeyboardButton, InlineKeyboardMarkup

from haidarlibs.dar.utils.db import *


async def loadprem(gol):
    if gol == '3':
        modules = loadBasicModule()
    elif gol == '2':
        modules = loadMediumModule()
    elif gol == '3':
        modules = loadPremiumModule()
    for mod in modules:
        imported_module = import_module(f"haidar.modules.{mod}")
        if hasattr(imported_module, "__MODULE__") and imported_module.__MODULE__:
            imported_module.__MODULE__ = imported_module.__MODULE__
            if hasattr(imported_module, "__HELP__") and imported_module.__HELP__:
                CMD_HELP[
                    imported_module.__MODULE__.replace(" ", "_").lower()
                ] = imported_module


# async def load_all(gol):
#     if gol == '3':
#         modules = loadBasicModule()
#     elif gol == '2':
#         modules = loadMediumModule()
#     elif gol == '3':
#         modules = loadPremiumModule()
#     for mod in modules:
#         imported_module = import_module(f"haidar.modules.{mod}")
#         if hasattr(imported_module, "__MODULE__") and imported_module.__MODULE__:
#             imported_module.__MODULE__ = imported_module.__MODULE__
#             if hasattr(imported_module, "__HELP__") and imported_module.__HELP__:
#                 CMD_HELP[
#                     imported_module.__MODULE__.replace(" ", "_").lower()
#                 ] = imported_module
#     print(f"[🤖 @{app.me.username} 🤖] [🔥 BERHASIL DIAKTIFKAN! 🔥]")
#     await app.send_message(
#         LOGS,
#         f"""
# <b>🔥 {app.me.mention} Berhasil Diaktifkan</b>
# <b>📘 Python: {python_version()}</b>
# <b>📙 Pyrogram: {__version__}</b>
# <b>👮‍♂ User: {len(bots._bots)}</b>
# """,
#         reply_markup=InlineKeyboardMarkup(
#             [[InlineKeyboardButton("🗑 TUTUP 🗑", callback_data="0_cls")]],
#         ),
#     )
