import os
import unittest

from twtr import Tweet, Twitter

TEST_TWEET_TEXT = "Hello World!"
TEST_IMG_PATH = os.path.join("tests", "test.png")
TEST_IMG_PATH2 = os.path.join("tests", "test2.png")
TEST_TWITTER = Twitter()
SKIP_REASON_TWITTER = "Calls Twitter API"


class Test(unittest.TestCase):
    @unittest.skip(SKIP_REASON_TWITTER)
    def test_init_(self):
        self.assertIsNotNone(TEST_TWITTER)

    @unittest.skip(SKIP_REASON_TWITTER)
    def test_send_text_only(self):
        tweet_id = TEST_TWITTER.send(Tweet(TEST_TWEET_TEXT))
        self.assertIsNotNone(tweet_id)

    @unittest.skip(SKIP_REASON_TWITTER)
    def test_send_text_and_image(self):
        tweet_id = TEST_TWITTER.send(
            Tweet(TEST_TWEET_TEXT).add_images([TEST_IMG_PATH, TEST_IMG_PATH2])
        )
        self.assertIsNotNone(tweet_id)
