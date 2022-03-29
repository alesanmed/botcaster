import itertools
from typing import List

from telegram import InlineKeyboardButton, InlineKeyboardMarkup, Update
from telegram.ext import (
    CallbackContext,
    CallbackQueryHandler,
    CommandHandler,
    Dispatcher,
)

from connectors import USERS_CONNECTOR, USERS_EPISODES
from state_machine.STATES import UploadStates
from state_machine.user_states import USER_STATES
from utils import get_user_id_and_message


def init(dispatcher: Dispatcher):
    """
    Register handlers
    """
    dispatcher.add_handler(CommandHandler("set_language", set_language))
    dispatcher.add_handler(
        CallbackQueryHandler(set_language, pattern=r"/set_language \d+")
    )


def set_language(update: Update, context: CallbackContext):
    """
    Sets the language in the new episode flow

    Args:
        update (Update): The update received
    """
    user_and_message = get_user_id_and_message(update)

    if user_and_message is None:
        return

    user_id = user_and_message["user_id"]
    message = user_and_message["message"]

    if user_id not in USER_STATES:
        return

    user_machine = USER_STATES[user_id]

    if user_machine.current_state != UploadStates.SET_LANGUAGE:
        return

    language_id = None

    if update.callback_query is not None:
        update.callback_query.answer("")
        language_id = update.callback_query.data.split(" ")[1]

        if language_id is None:
            return
    elif context.args is not None:
        language_id = context.args[0]
    else:
        return

    try:
        language_id = int(language_id)
    except ValueError:
        return

    program_dto = USERS_EPISODES[user_id]

    program_dto.language_id = language_id

    user_machine.current_state = UploadStates.SET_SUBCATEGORY

    connector = USERS_CONNECTOR[user_id]

    categories = connector.get_categories()

    subcategories = list(
        itertools.chain(*list(map(lambda cat: cat.subcategories, categories)))
    )

    keyboard: List[List[InlineKeyboardButton]] = []
    keyboard_col = []
    columns = 2

    for subcategory in subcategories:
        if len(keyboard_col) == columns:
            keyboard.append(keyboard_col)
            keyboard_col = []

        keyboard_col.append(
            InlineKeyboardButton(
                subcategory.name, callback_data=f"/set_subcategory {subcategory.id}"
            )
        )

    message.reply_text(
        "Ahora elige la categoría",
        reply_markup=InlineKeyboardMarkup(keyboard),
    )
