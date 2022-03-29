from telegram import Update
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
    dispatcher.add_handler(CommandHandler("set_subcategory", set_subcategory))
    dispatcher.add_handler(
        CallbackQueryHandler(set_subcategory, pattern=r"/set_subcategory \d+")
    )


def set_subcategory(update: Update, context: CallbackContext):
    """
    Sets the subcategory in the new episode flow

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

    if user_machine.current_state != UploadStates.SET_SUBCATEGORY:
        return

    subcat_id = None

    if update.callback_query is not None:
        update.callback_query.answer("")
        subcat_id = update.callback_query.data.split(" ")[1]

        if subcat_id is None:
            return
    elif context.args is not None:
        subcat_id = context.args[0]
    else:
        return

    try:
        subcat_id = int(subcat_id)
    except ValueError:
        return

    program_dto = USERS_EPISODES[user_id]

    program_dto.subcategory_id = subcat_id

    user_machine.current_state = UploadStates.SET_TAGS

    connector = USERS_CONNECTOR[user_id]

    tags = connector.get_tags(program_dto.subcategory_id)

    message.reply_text(
        (
            "Ahora toca elegir las etiquetas. "
            "Elige hasta un máximo de 5 y escríbemelas separadas por comas. "
            "Aquí tienes algunos ejemplos:\n\n"
            f"{', '.join(list(map(lambda tag: tag.name, tags)))}"
        )
    )
