from typing import Optional, TypedDict

from telegram import Message, Update


class UserIdAndMessage(TypedDict):
    """
    Return type for user_id and message extractor
    """

    user_id: int
    message: Message


def get_user_id_and_message(update: Update) -> Optional[UserIdAndMessage]:
    """
    Extracts the user id and message from an update, regardless if it's a
    normal update or a callback update
    """
    user_id = None
    message = None

    if update.message is not None:
        user_id = update.message.from_user.id
        message = update.message
    elif update.effective_user is not None and update.effective_message is not None:
        user_id = update.effective_user.id
        message = update.effective_message
    else:
        return

    return {"user_id": user_id, "message": message}


def get_user_id(update: Update) -> Optional[int]:
    """
    Extracts the user id from an update, regardless if it's a
    normal update or a callback update
    """

    user_id = None

    if update.message is not None:
        user_id = update.message.from_user.id
    elif update.effective_user is not None:
        user_id = update.effective_user.id
    else:
        return

    return user_id
