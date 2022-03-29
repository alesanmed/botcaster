# encoding: utf-8

from logging import getLogger

from telegram import InlineKeyboardButton, InlineKeyboardMarkup, Update
from telegram.ext import CallbackContext, CommandHandler, Dispatcher

# Init logger
logger = getLogger(__name__)


def init(dispatcher: Dispatcher):
    """Provide handlers initialization."""
    dispatcher.add_handler(CommandHandler("start", start))


def start(update: Update, _: CallbackContext):
    """Process a /start command."""
    update.message.reply_text(
        text="Buenas! Soy el bot definitivo para los podcasters. ¿Qué quieres hacer?",
        reply_markup=InlineKeyboardMarkup(
            [[InlineKeyboardButton("Nuevo episodio", callback_data="/new_episode")]]
        ),
    )
