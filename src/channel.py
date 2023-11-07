import json
import os

from googleapiclient.discovery import build

api_key: str = os.getenv('YOUTUBE_API_KEY')

youtube = build('youtube', 'v3', developerKey=api_key)


class Channel:
    """Класс для ютуб-канала"""

    def __init__(self, channel_id: str):
        """Экземпляр инициализируется id канала. Дальше все данные будут подтягиваться по API."""
        self.channel_id = channel_id
        self.channel = None

    def take_dict_to_print(self):
        """
        создает словарь с данными по каналу
        :returns: Dictionary with info about the channel
        """
        self.channel: object = youtube.channels().list(id=self.channel_id, part='snippet,statistics').execute()
        return self.channel

    def print_info(self, dict_to_print):
        """Выводит в консоль информацию о канале."""
        print(json.dumps(dict_to_print, indent=2, ensure_ascii=False))
