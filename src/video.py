from src.channel import Channel


class Video(Channel):

    def __init__(self, id_video):
        """инициализируется по id видео"""
        self.id_video = id_video
        self.info = Video.create_video_response(id_video)
        self.name_video = self.info['items'][0]['snippet']['title']
        self.url_video = "https://youtu.be/" + self.id_video
        self.count_views = self.info['items'][0]['statistics']['viewCount']
        self.count_likes = self.info['items'][0]['statistics']['likeCount']

    @classmethod
    def create_video_response(cls, id_video):
        """Создает словарь с данными по видео"""
        return cls.youtube.videos().list(id=id_video, part='snippet,statistics').execute()

    def __str__(self):
        """Возвращает имя видео"""
        return self.name_video


class PLVideo(Video):
    def __init__(self, id_video, playlist_id):
        """инициализируется по 'id видео' и 'id плейлиста' """
        super().__init__(id_video)
        self.playlist_id = playlist_id
