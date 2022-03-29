import os

from telegram import Update
from telegram.ext import CallbackContext, Dispatcher, MessageHandler
from telegram.ext.filters import Filters

from connectors import USERS_CONNECTOR, USERS_EPISODES
from state_machine.STATES import UploadStates
from state_machine.user_states import USER_STATES
from utils import get_user_id


def init(dispatcher: Dispatcher):
    """
    Register handlers
    """
    dispatcher.add_handler(
        MessageHandler(filters=Filters.photo, callback=handle_message)
    )


def handle_message(update: Update, _: CallbackContext):
    """
    Handles image messages according to new episode flow

    Args:
        update (Update): The update received
    """
    user_id = get_user_id(update)
    message = update.message

    if user_id is None:
        return

    user_machine = USER_STATES[user_id]

    if user_machine.current_state != UploadStates.SET_IMAGE:
        return

    photo = update.message.photo[-1].get_file()
    image_path = os.path.join(
        os.path.dirname(__file__), f"../tmp/{photo.file_unique_id}"
    )
    photo.download(image_path)

    connector = USERS_CONNECTOR[user_id]

    image_res = connector.upload_image(image_path)

    program_dto = USERS_EPISODES[user_id]

    program_dto.image = image_res.url

    user_machine.current_state = UploadStates.SET_AUDIO

    message.reply_text("Por último, envíame el audio de tu episodio (en MP3)")
