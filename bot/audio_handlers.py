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
        MessageHandler(filters=Filters.audio, callback=handle_message)
    )


def handle_message(update: Update, _: CallbackContext):
    """
    Handles audio messages according to new episode flow

    Args:
        update (Update): The update received
    """
    user_id = get_user_id(update)
    message = update.message

    if user_id is None:
        return

    user_machine = USER_STATES[user_id]

    if user_machine.current_state != UploadStates.SET_AUDIO:
        return

    audio = update.message.audio.get_file()
    audio_path = os.path.join(
        os.path.dirname(__file__), f"../tmp/{audio.file_unique_id}"
    )
    audio.download(audio_path)

    program_dto = USERS_EPISODES[user_id]

    connetor = USERS_CONNECTOR[user_id]

    audio_res = connetor.upload_audio(audio_path)

    program_dto.upload_reference = audio_res.ref
    program_dto.upload_server = audio_res.server
    program_dto.upload_extension = audio_res.ext
    program_dto.file_name = audio_res.name

    episode_res = connetor.publish_episode(program_dto)

    del USER_STATES[user_id]
    del USERS_EPISODES[user_id]
    del USERS_CONNECTOR[user_id]

    message.reply_text(
        f"Listo! El audio se está procesando, estará disponible aquí:\n{episode_res.shortUrl}"
    )
