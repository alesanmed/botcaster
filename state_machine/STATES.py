from enum import IntEnum


class UploadStates(IntEnum):
    """
    Possible states the user can go through when uploading a new
    episode
    """

    SELECT_PROGRAM = 1
    SET_TITLE = 2
    SET_DESCRIPTION = 3
    SET_GENDER = 4
    SET_LANGUAGE = 5
    SET_SUBCATEGORY = 6
    SET_TAGS = 7
    SET_IMAGE = 8
    SET_AUDIO = 9
