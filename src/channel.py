import json
import os
import sys

from googleapiclient.discovery import build


class Channel:
    """Класс для ютуб-канала"""
    api_key: str = os.getenv('YOUTUBE_API_KEY')

    youtube = build('youtube', 'v3', developerKey=api_key)

    def __init__(self, channel_id: str):
        """
        Экземпляр инициализируется id канала. Дальше все данные будут подтягиваться по API.
        :param channel_id: id канала
        """
        self.id = channel_id
        self.info = Channel.take_dict_to_print(channel_id)
        self.title = self.info['items'][0]['snippet']['title']
        self.description = self.info['items'][0]['snippet']['description']
        self.url = "https://www.youtube.com/channel/" + self.info['items'][0]['snippet']['customUrl']
        self.subscribers = self.info['items'][0]['statistics']['subscriberCount']
        self.view_count = self.info['items'][0]['statistics']['viewCount']
        self.video_count = self.info['items'][0]['statistics']['videoCount']

    @classmethod
    def take_dict_to_print(cls, channel_id: str):
        """
        создает словарь с данными по каналу
        :returns: Dictionary with info about the channel
        """
        yt_chanel_all_info = cls.youtube.channels().list(id=channel_id, part='snippet,statistics').execute()
        return yt_chanel_all_info

    @staticmethod
    def get_service():
        """Возвращает объект для работы с YouTube API"""
        api_object = Channel.youtube
        return api_object

    #return json.dumps(self.id, indent=2, ensure_ascii=False, sort_keys=True, separators=(',', ': '))

    def print_info(self):
        """Выводит в консоль информацию о канале."""
        print(self.info)

    def to_json(self, filename):
        """Cоздает файл 'filename' в данными по каналу"""
        with open(filename, 'w') as sys.stdout:
            print(self.info)
