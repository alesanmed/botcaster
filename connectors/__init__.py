from typing import Dict

from models.ivoox_episode import IvooxEpisode

from .ivoox import IvooxConnector

USERS_CONNECTOR: Dict[int, IvooxConnector] = {}

USERS_EPISODES: Dict[int, IvooxEpisode] = {}
