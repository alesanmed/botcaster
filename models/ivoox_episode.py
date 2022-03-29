import json
from typing import List


class IvooxEpisode:
    """
    Class for holding all data for an episode
    """

    @property
    def program_id(self):
        return self.__program_id

    @program_id.setter
    def program_id(self, program_id: int):
        self.__program_id = program_id

    @property
    def title(self):
        return self.__title

    @title.setter
    def title(self, title: str):
        self.__title = title

    @property
    def description(self):
        return self.__description

    @description.setter
    def description(self, description: str):
        self.__description = description

    @property
    def gender_id(self):
        return self.__gender_id

    @gender_id.setter
    def gender_id(self, gender_id: int):
        self.__gender_id = gender_id

    @property
    def language_id(self):
        return self.__language_id

    @language_id.setter
    def language_id(self, language_id: int):
        self.__language_id = language_id

    @property
    def subcategory_id(self):
        return self.__subcategory_id

    @subcategory_id.setter
    def subcategory_id(self, subcategory_id: int):
        self.__subcategory_id = subcategory_id

    @property
    def tags(self):
        return self.__tags

    @tags.setter
    def tags(self, tags: List[str]):
        self.__tags = tags

    @property
    def image(self):
        return self.__image

    @image.setter
    def image(self, image: str):
        self.__image = image

    @property
    def upload_reference(self):
        return self.__upload_reference

    @upload_reference.setter
    def upload_reference(self, upload_reference: str):
        self.__upload_reference = upload_reference

    @property
    def upload_server(self):
        return self.__upload_server

    @upload_server.setter
    def upload_server(self, upload_server: str):
        self.__upload_server = upload_server

    @property
    def upload_extension(self):
        return self.__upload_extension

    @upload_extension.setter
    def upload_extension(self, upload_extension: str):
        self.__upload_extension = upload_extension

    @property
    def file_name(self):
        return self.__file_name

    @file_name.setter
    def file_name(self, file_name: str):
        self.__file_name = file_name

    def to_json(self):
        return json.dumps(self, default=lambda o: o.__dict__, sort_keys=True, indent=4)
