from telegram import InlineKeyboardButton, InlineKeyboardMarkup, Update
from telegram.ext import (
    CallbackContext,
    CallbackQueryHandler,
    CommandHandler,
    Dispatcher,
)

from connectors import USERS_EPISODES
from connectors.ivoox.LANGUAGES import LANGUAGES
from state_machine.STATES import UploadStates
from state_machine.user_states import USER_STATES
from utils import get_user_id_and_message


def init(dispatcher: Dispatcher):
    """
    Register handlers
    """
    dispatcher.add_handler(CommandHandler("set_gender", set_gender))
    dispatcher.add_handler(CallbackQueryHandler(set_gender, pattern=r"/set_gender \d+"))


def set_gender(update: Update, context: CallbackContext):
    """
    Sets the gender in the new episode flow

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

    if user_machine.current_state != UploadStates.SET_GENDER:
        return

    gender_id = None

    if update.callback_query is not None:
        update.callback_query.answer("")
        gender_id = update.callback_query.data.split(" ")[1]

        if gender_id is None:
            return
    elif context.args is not None:
        gender_id = context.args[0]
    else:
        return

    try:
        gender_id = int(gender_id)
    except ValueError:
        return

    program_dto = USERS_EPISODES[user_id]

    program_dto.gender_id = gender_id

    user_machine.current_state = UploadStates.SET_LANGUAGE

    languages = [lang.name for lang in LANGUAGES]

    message.reply_text(
        "¿En qué idioma está?",
        reply_markup=InlineKeyboardMarkup(
            list(
                map(
                    lambda language: [
                        InlineKeyboardButton(
                            language.title(),
                            callback_data=f"/set_language {LANGUAGES[language]}",
                        )
                    ],
                    languages,
                )
            )
        ),
    )
