from telegram import Update
from telegram.ext import (
    CallbackContext,
    CallbackQueryHandler,
    CommandHandler,
    Dispatcher,
)

from connectors import USERS_EPISODES
from models.ivoox_episode import IvooxEpisode
from state_machine.STATES import UploadStates
from state_machine.user_states import USER_STATES
from utils import get_user_id_and_message


def init(dispatcher: Dispatcher):
    """
    Register handlers
    """
    dispatcher.add_handler(CommandHandler("set_program", set_program))
    dispatcher.add_handler(
        CallbackQueryHandler(set_program, pattern=r"/set_program \d+")
    )


def set_program(update: Update, context: CallbackContext):
    """
    Sets the program in the new episode flow

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

    if user_machine.current_state != UploadStates.SELECT_PROGRAM:
        return

    program_id = None

    if update.callback_query is not None:
        program_id = update.callback_query.data.split(" ")[1]
        update.callback_query.answer("")

        if program_id is None:
            return
    elif context.args is not None:
        program_id = context.args[0]
    else:
        return

    try:
        program_id = int(program_id)
    except ValueError:
        return

    program_dto = IvooxEpisode()
    program_dto.program_id = program_id

    USERS_EPISODES[user_id] = program_dto

    user_machine.current_state = UploadStates.SET_TITLE

    message.reply_text("Perfecto, ahora dime el título del episodio")
