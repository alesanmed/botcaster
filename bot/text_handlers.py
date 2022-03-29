from telegram import InlineKeyboardButton, InlineKeyboardMarkup, Message, Update
from telegram.ext import CallbackContext, Dispatcher, MessageHandler
from telegram.ext.filters import Filters

from connectors import USERS_EPISODES
from connectors.ivoox.GENDER import GENDER
from models.ivoox_episode import IvooxEpisode
from state_machine import StateMachine
from state_machine.STATES import UploadStates
from state_machine.user_states import USER_STATES
from utils import get_user_id_and_message


def init(dispatcher: Dispatcher):
    """
    Register handlers
    """
    dispatcher.add_handler(
        MessageHandler(filters=Filters.update, callback=handle_message)
    )


def handle_message(update: Update, _: CallbackContext):
    """
    Handles text messages according to new episode flow

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
    program_dto = USERS_EPISODES[user_id]

    if user_machine.current_state == UploadStates.SET_TITLE:
        set_title(message, user_machine, program_dto)
    elif user_machine.current_state == UploadStates.SET_DESCRIPTION:
        set_description(message, user_machine, program_dto)
    elif user_machine.current_state == UploadStates.SET_TAGS:
        set_tags(message, user_machine, program_dto)
    else:
        return


def set_title(
    message: Message, user_machine: StateMachine, program_dto: IvooxEpisode
) -> None:
    """
    Sets the title of the episode in the flow

    Args:
        message (Message): Message object received
        user_machine (StateMachine): User state machine
        program_dto (IvooxEpisode): Episode DTO holding all added data
    """
    program_dto.title = message.text
    user_machine.current_state = UploadStates.SET_DESCRIPTION

    message.reply_text(
        "Mándame ahora la descripción del episodio (mínimo 150 caracteres)"
    )


def set_description(
    message: Message, user_machine: StateMachine, program_dto: IvooxEpisode
) -> None:
    """
    Sets the description of the episode in the flow

    Args:
        message (Message): Message object received
        user_machine (StateMachine): User state machine
        program_dto (IvooxEpisode): Episode DTO holding all added data
    """
    program_dto.description = message.text

    if len(message.text) < 150:
        message.reply_text(
            (
                "La descripción debe tener al menos 150 caracteres. "
                "Añade algo más y envíala de nuevo, por favor"
            )
        )

        return

    user_machine.current_state = UploadStates.SET_GENDER

    gender_names = [s.name for s in GENDER]

    message.reply_text(
        "¿Cuál es el género del podcast?",
        reply_markup=InlineKeyboardMarkup(
            list(
                map(
                    lambda gender_name: [
                        InlineKeyboardButton(
                            gender_name.title().replace("_", "/"),
                            callback_data=f"/set_gender {GENDER[gender_name]}",
                        )
                    ],
                    gender_names,
                )
            )
        ),
    )


def set_tags(message: Message, user_machine: StateMachine, program_dto: IvooxEpisode):
    """
    Sets the subcategory in the new episode flow

    Args:
        update (Update): The update received
    """

    tags = message.text

    tags = list(filter(None, map(lambda tag: tag and tag.strip(), tags.split(","))))

    if len(tags) > 5:
        message.reply_text("Por favor, mándame de nuevo un máximo de 5 categorías")
        return

    program_dto.tags = tags

    user_machine.current_state = UploadStates.SET_IMAGE

    message.reply_text(
        "Ahora mándame la foto que quieres que tenga tu episodio (envíala como imagen, no como archivo)"
    )
