# encoding: utf-8

import os

from telegram import InlineKeyboardButton, InlineKeyboardMarkup, Update
from telegram.ext import (CallbackContext, CallbackQueryHandler,
                          CommandHandler, Dispatcher)

from connectors import USERS_CONNECTOR
from connectors.ivoox import IvooxConnector
from state_machine import StateMachine
from state_machine.user_states import USER_STATES
from utils import get_user_id_and_message


def init(dispatcher: Dispatcher):
    """Provide handlers initialization."""
    dispatcher.add_handler(CommandHandler("new_episode", new_episode))
    dispatcher.add_handler(CallbackQueryHandler(new_episode, pattern="/new_episode"))


def new_episode(update: Update, _: CallbackContext):
    """
    Starts a new process for uploading an episode

    Args:
        update (Update): The update received
    """

    user_and_message = get_user_id_and_message(update)

    if user_and_message is None:
        return
    
    if update.callback_query:
        update.callback_query.answer("")

    user_id = user_and_message["user_id"]
    message = user_and_message["message"]

    connector = IvooxConnector(
        os.environ.get("IVOOX_USER", ""), os.environ.get("IVOOX_PASS", "")
    )
    USER_STATES[user_id] = StateMachine(connector)
    USERS_CONNECTOR[user_id] = connector

    user_programs = connector.get_programs()

    message.reply_text(
        "Para subir un nuevo capítulo, empieza por elegir a qué programa subirlo",
        reply_markup=InlineKeyboardMarkup(
            list(
                map(
                    lambda program: [
                        InlineKeyboardButton(
                            program.name, callback_data=f"/set_program {program.id}"
                        )
                    ],
                    user_programs,
                )
            )
        ),
    )
