import os

from googleapiclient.discovery import build


class Video:
    api_key: str = os.getenv('YOUTUBE_API_KEY')

    youtube = build('youtube', 'v3', developerKey=api_key)

    def __init__(self, id_video):
        """Инициализируется по id видео"""
        self.id_video = id_video
        self.info = Video.create_video_response(id_video)
        try:
            self.name_video = self.info['items'][0]['snippet']['title']
            self.url_video = "https://youtu.be/" + self.id_video
            self.count_views = self.info['items'][0]['statistics']['viewCount']
            self.count_likes = self.info['items'][0]['statistics']['likeCount']
        except Exception:
            raise Exception("Некорректный id видео")

    @classmethod
    def create_video_response(cls, id_video):
        """Создает словарь с данными по видео"""
        try:
            response = cls.youtube.videos().list(id=id_video, part='snippet,statistics').execute()
        except Exception:
            raise Exception("что то пошло не так")
        return response

    def __str__(self):
        """Возвращает имя видео"""
        return self.name_video


class PLVideo(Video):
    def __init__(self, id_video, playlist_id):
        """инициализируется по 'id видео' и 'id плейлиста' """
        super().__init__(id_video)
        self.playlist_id = playlist_id
