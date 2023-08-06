import os
import unittest

from twtr import Tweet, Twitter

TEST_IMG_PATH = os.path.join("tests", "test.png")
TEST_TWITTER = Twitter()
SKIP_REASON_TWITTER = "Calls Twitter API"


class Test(unittest.TestCase):
    @unittest.skip(SKIP_REASON_TWITTER)
    def test_init_(self):
        self.assertIsNotNone(TEST_TWITTER)

    @unittest.skip(SKIP_REASON_TWITTER)
    def test_send_text_only(self):
        tweet_id = TEST_TWITTER.send(Tweet("Hello World!"))
        self.assertIsNotNone(tweet_id)

    @unittest.skip(SKIP_REASON_TWITTER)
    def test_send_text_and_image(self):
        tweet_id = TEST_TWITTER.send(
            Tweet("Hello World!").add_image(TEST_IMG_PATH)
        )
        self.assertIsNotNone(tweet_id)
