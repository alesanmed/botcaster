import json
import os
import random
from typing import Callable, List

import magic
import requests
from GENDER import GENDER
from LANGUAGES import LANGUAGES
from requests import HTTPError


class IvooxConnector:
    """Connector for logging in and uploading an episode to IVOOX"""

    BASE_API_URL = "https://core.ivoox.com/v1"
    BASE_FILES_URL = "https://files.ivoox.com/ffmpeg/uploadHTML5.php"

    def __init__(self, user: str, password: str) -> None:
        self.token = None
        self.user = user
        self.password = password

    def __handle_auth_error(func: Callable):  # type: ignore # pylint: disable=no-self-argument, unused-private-member
        """Decorator for handling authentication errors

        Args:
            func (function): Function thatt will be decorated
        """

        def inner(self, *args, **kwargs):
            try:
                return func(self, *args, **kwargs)  # pylint: disable=not-callable
            except HTTPError as err:
                if err.response.status_code == 401 or err.response.status_code == 403:
                    self.__login()  # pylint: disable=protected-access
                    return func(self, *args, **kwargs)  # pylint: disable=not-callable
                else:
                    raise err

        return inner

    def __login(self) -> None:
        """Logs in to your IVOOX

        Args:
            user (str): the username (email)
            password (str): your password. WARNING, is in plaintext

        Raises:
            AuthenticationError: Raised if login doesn't go well
        """
        body = {
            "name": None,
            "email": self.user,
            "password": self.password,
            "notifyNewsletters": False,
        }

        response = requests.post(f"{self.BASE_API_URL}/authentication/login", json=body)

        response.raise_for_status()

        self.token = response.json().get("data")

    @__handle_auth_error
    def upload_audio(self, path: str):
        """Uploads an audio file to ivoox

        Args:
            path (str): Path of the audio to upload

        Raises:
            FileNotFoundError: Raised if the file does not exists
        """
        if not os.path.exists(path):
            raise FileNotFoundError()

        if self.token is None:
            self.__login()

        file_name = os.path.basename(path)

        mime = magic.Magic(mime=True)
        mime_type = mime.from_file(path)

        response = requests.post(
            self.BASE_FILES_URL,
            headers={
                "Authorization": f"Bearer {self.token}",
                "filename": file_name,
                "Accept-Encoding": "gzip, deflate, br",
                "Accept": "application/json, text/plain, */*",
                "Accept-Language": "es",
                "Connection": "keep-alive",
            },
            files=[
                (
                    "files[]",
                    (file_name, open(path, "rb"), mime_type),
                )
            ],
        )

        response.raise_for_status()

        return response.json()

    @__handle_auth_error
    def upload_image(self, path: str):
        """Uploads the episode image to IVOOX

        Args:
            path (str): The path to the image

        Raises:
            FileNotFoundError: Raised if the file doesn't exists

        Returns:
            Dict: The Dict with the response from IVOOX
        """
        if not os.path.exists(path):
            raise FileNotFoundError()

        if self.token is None:
            self.__login()

        file_name = os.path.basename(path)

        mime = magic.Magic(mime=True)
        mime_type = mime.from_file(path)

        response = requests.post(
            f"{self.BASE_API_URL}/private/image-file-upload?objectType=AUDIO",
            headers={
                "Authorization": f"Bearer {self.token}",
                "filename": file_name,
            },
            files=[
                (
                    "image",
                    (file_name, open(path, "rb"), mime_type),
                )
            ],
        )

        response.raise_for_status()

        return response.json()["data"][0]

    def get_categories(self):
        """
        Returns the list of categories

        Returns:
            List: List of categories
        """
        if self.token is None:
            self.__login()

        response = requests.get(
            f"{self.BASE_API_URL}/public/categories",
            headers={
                "Content-Type": "application/json;charset=UTF-8",
            },
        )

        response.raise_for_status()

        return response.json()["data"]

    def get_tags(self, subcategory_id: int):
        """
        Returns the list of tags for the specified subcategory

        Args:
            subcategory_id (int): The subcategory id

        Returns:
            List: List of tags
        """
        if self.token is None:
            self.__login()

        response = requests.get(
            f"{self.BASE_API_URL}/public/subcategories/{subcategory_id}/tags",
            headers={
                "Content-Type": "application/json;charset=UTF-8",
            },
        )

        response.raise_for_status()

        return response.json()["data"]["items"]

    @__handle_auth_error
    def get_programs(self):
        """
        Returns the programs available for the logged user

        Returns:
            Dict: IVOOX programs response
        """
        if self.token is None:
            self.__login()

        response = requests.get(f"{self.BASE_API_URL}/private/programs")

        response.raise_for_status()

        return response.json()["data"]["items"]

    @__handle_auth_error
    def publish_episode(
        self,
        description: str,
        gender: GENDER,
        image_link: str,
        program: int,
        language: LANGUAGES,
        subcategory: int,
        tags: List[str],
        title: str,
        upload_reference: str,
        upload_server: str,
        upload_extension: str,
        file_name: str,
    ):
        """
        Publishes the episode with the audio and images previously uploaded

        Args:
            description (str): Episode description
            gender (GENDER): Gender ID
            image_link (str): Link of the uploaded image
            program (int): Program ID
            language (LANGUAGES): Language ID
            subcategory (int): Subcategory ID
            tags (List[str]): List of episode tags (max 5)
            title (str): Episode title
            upload_reference (str): Reference of the uploaded audio
            upload_server (str): Server where the audio has been uploaded
            upload_extension (str): Uploaded audio extension
            file_name (str): Uploaded audio file name

        Returns:
            Dict: Response data from IVOOX
        """

        if self.token is None:
            self.__login()

        response = requests.post(
            f"{self.BASE_API_URL}/private/audios",
            headers={
                "Authorization": f"Bearer {self.token}",
                "Content-Type": "application/json;charset=UTF-8",
            },
            data=json.dumps(
                {
                    "description": description,
                    "genderId": gender.value,
                    "image": image_link,
                    "programId": program,
                    "languageId": language.value,
                    "subcategoryId": subcategory,
                    "mediaUrl": None,
                    "tags": tags,
                    "title": title,
                    "type": "PUBLIC",
                    "uploadDate": None,
                    "schedule": False,
                    "visible": True,
                    "premiereRelease": None,
                    "percentageOfListensCompleted": None,
                    "iTunesType": "full",
                    "scheduleDate": None,
                    "uploadReference": upload_reference,
                    "uploadServer": upload_server,
                    "uploadExtension": upload_extension,
                    "listId": None,
                    "share": {},
                    "fileName": file_name,
                    "fileUrl": None,
                },
                ensure_ascii=False,
            ).encode("utf-8"),
        )

        response.raise_for_status()

        return response.json()["data"]


if __name__ == "__main__":
    connector = IvooxConnector(
        os.environ.get("IVOOX_USER", ""), os.environ.get("IVOOX_PASS", "")
    )

    audio_data = connector.upload_audio(
        "/mnt/d/Documents/Km 64/4 - Catacumbas/Catacumbas/Catacumbas_mezcla.mp3"
    )

    image_data = connector.upload_image("/mnt/d/Downloads/food_up.jpg")

    categories = connector.get_categories()

    chosen_category = random.sample(categories, 1)

    chosen_subcategory = random.sample(chosen_category[0]["subcategories"], 1)[0]["id"]

    tags = connector.get_tags(chosen_subcategory)

    chosen_tags = random.sample(tags, 5)

    uploaded_data = connector.publish_episode(
        (
            "Este episodio ha sido publicado con un metodo muy guay. "
            "Que es básicamente subiendo un audio y una imagen a la "
            "plataforma y dandole al boton de publicar."
        ),
        GENDER.PODCASTING,
        image_data["url"],
        1487989,
        LANGUAGES.SPANISH,
        chosen_subcategory,
        list(map(lambda tag: tag["name"], chosen_tags)),
        "Quizás la última prueba",
        audio_data["ref"],
        audio_data["server"],
        audio_data["ext"],
        audio_data["name"],
    )

    print(uploaded_data)
