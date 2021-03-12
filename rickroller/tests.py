from django.test import TestCase, Client

from rickroller.models import RickrollPost


class TestRickRollRedirection(TestCase):
    bot_user_agents = [
        "Mozilla/5.0 (compatible; Discordbot/2.0; +https://discordapp.com)",
        "WhatsApp/2.20.206.24 A",
        "TelegramBot (like TwitterBot)",
        "Twitterbot/1.0",
    ]
    other_user_agents = [
        "Mozilla/5.0",
        "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.88 Safari/537.36",
        "Mozilla/5.0 (iPhone; CPU iPhone OS 10_3_1 like Mac OS X) AppleWebKit/603.1.30 (KHTML, like Gecko) "
        "Version/10.0 Mobile/14E304 Safari/602.1",
    ]

    def setUp(self):
        self.post = RickrollPost.objects.create(title="Test Title",
                                                description="Test Description",
                                                image="https://example.org")
        self.client = Client()

    def test_bot_user_agents(self):
        for user_agent in self.bot_user_agents:
            response = self.client.get(self.post.get_absolute_url(),
                                       HTTP_USER_AGENT=user_agent)
            self.assertEqual(response.status_code, 200)
            self.assertIn(self.post.title.encode('ascii'), response.content)
            self.assertIn(self.post.description.encode('ascii'), response.content)
            self.assertIn(self.post.image.encode('ascii'), response.content)

    def test_other_user_agents(self):
        for user_agent in self.other_user_agents:
            response = self.client.get(self.post.get_absolute_url(),
                                       HTTP_USER_AGENT=user_agent)
            self.assertEqual(response.status_code, 301)
