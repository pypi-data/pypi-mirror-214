import os

import tweepy

from twtr.common import log
from twtr.core.Tweet import Tweet


class Twitter:
    def __init__(self):
        bearer_token = os.environ.get('TWTR_BEARER_TOKEN')
        # API Key and Secret (also known as Consumer Key and Secret)
        consumer_key = os.environ.get('TWTR_API_KEY')
        consumer_secret = os.environ.get('TWTR_API_KEY_SECRET')
        access_token = os.environ.get('TWTR_ACCESS_TOKEN')
        access_token_secret = os.environ.get('TWTR_ACCESS_TOKEN_SECRET')

        if (
            bearer_token is None
            or consumer_key is None
            or consumer_secret is None
            or access_token is None
            or access_token_secret is None
        ):
            self.__client__ = None
            self.__api__ = None
        else:
            self.__client__ = tweepy.Client(
                bearer_token=bearer_token,
                consumer_key=consumer_key,
                consumer_secret=consumer_secret,
                access_token=access_token,
                access_token_secret=access_token_secret,
            )

            auth = tweepy.OAuth1UserHandler(
                consumer_key=consumer_key,
                consumer_secret=consumer_secret,
                access_token=access_token,
                access_token_secret=access_token_secret,
            )
            self.__api__ = tweepy.API(auth)

    def check_api_and_client(self):
        if self.__client__ is None:
            raise ValueError('Client is not valid')

    def __media_upload__(self, image_path: str) -> int:
        if not os.path.exists(image_path):
            raise FileNotFoundError(f'Image not found: {image_path}')

        self.check_api_and_client()
        media = self.__api__.media_upload(image_path)
        log.debug(f'{media=}')
        media_id = media.media_id
        log.debug(f'Uploaded media {image_path} to {media_id}.')
        return media_id

    def __media_upload_all__(self, image_path_list: list[str]) -> list[int]:
        media_ids = []
        for image_path in image_path_list:
            media_id = self.__media_upload__(image_path)
            media_ids.append(media_id)

        n = len(media_ids)
        log.debug(f'Uploaded {n} media to Twitter.')
        return media_ids

    def __create_tweet__(self, tweet: Tweet) -> int:
        log.debug(f'Sending tweet: {tweet.text}...')
        media_ids = self.__media_upload_all__(tweet.image_path_list)

        self.check_api_and_client()

        if len(media_ids) > 0:
            log.debug(f'{media_ids=}')
            response = self.__client__.create_tweet(
                text=tweet.text,
                media_ids=media_ids,
            )
        else:
            response = self.__client__.create_tweet(
                text=tweet.text,
            )

        log.debug(f'{response=}')
        tweet_id = response.data['id']
        log.debug(f'Sent tweet ({tweet_id}).')
        return tweet_id

    def send(self, tweet: Tweet):
        try:
            return self.__create_tweet__(tweet)
        except Exception as e:
            log.error(f'Failed to send tweet: {e}')
            return None


if __name__ == '__main__':
    tweet = Tweet('Hello World!')
    twitter = Twitter()
    print(twitter.send(tweet))
