import os

import isodate
from googleapiclient.discovery import build
from datetime import timedelta


class PlayList:
    api_key: str = os.getenv('YOUTUBE_API_KEY')

    youtube = build('youtube', 'v3', developerKey=api_key)

    def __init__(self, playlist_id):
        """инициализируется по 'id плейлиста' """
        self.playlist_info = PlayList.playlist_response(playlist_id)
        self.playlist_id = self.playlist_info['items'][0]['contentDetails']['videoId']
        self.title = self.playlist_info['items'][0]['snippet']['title']
        self.url = f'https://www.youtube.com/playlist?list={playlist_id}'

    @classmethod
    def playlist_response(cls, playlist_id):
        """Создание объекта для работы с информацией плейлста"""
        playlist_response = cls.youtube.playlistItems().list(playlistId=playlist_id,
                                                             part='contentDetails, snippet',
                                                             maxResults=50).execute()
        return playlist_response

    def show_best_video(self):
        """Возвращает ссылку на лучшее видео"""
        #создаем спиосок id всех видео из плейлиста
        video_ids: list[str] = [video['contentDetails']['videoId'] for video in self.playlist_info['items']]
        #создаем объекты для работы через api с каждым из видео, через join
        video_response = self.youtube.videos().list(part='contentDetails,statistics',
                                                    id=','.join(video_ids)
                                                    ).execute()
        max_like_count = 0
        #цикл по видео из плейлиста и поиск лучшего
        for video in video_response["items"]:
            like = video["statistics"]["likeCount"]
            if max_like_count < int(like):
                max_like_count = int(like)
                best_video = video['id']
        return f"https://youtu.be/{best_video}"

    @property
    def total_duration(self):
        """Возвращет общую продолжительность плейлиста"""
        video_ids: list[str] = [video['contentDetails']['videoId'] for video in self.playlist_info['items']]
        video_response = self.youtube.videos().list(part='contentDetails,statistics',
                                                    id=','.join(video_ids)
                                                    ).execute()
        time_all_duration = timedelta(seconds=0)

        for video in video_response['items']:
            # # YouTube video duration is in ISO 8601 format
            iso_8601_duration = video['contentDetails']['duration']
            duration = isodate.parse_duration(iso_8601_duration)
            time_all_duration += duration
        return time_all_duration

    # def total_seconds(self):
    #     return PlayList.total_duration.seconds


pl1 = PlayList('PLv_zOGKKxVpj-n2qLkEM2Hj96LO6uqgQw')
pl1.show_best_video()
