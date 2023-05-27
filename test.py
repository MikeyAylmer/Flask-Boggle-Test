from unittest import TestCase
from app import app
from flask import session
from boggle import Boggle


class FlaskTests(TestCase):

    # TODO -- write tests for every view function / feature!
    def setUp(self):
        """setUp before everytest"""
        self.client = app.tes_client()
        app.config['TESTING'] = True

    def test_display_board(self):
        """make sure html is displaying"""
        with self.client:
            res = self.client.get('/')
            self.assertIn('board', session)
            self.assertIn(b'Score:', res.data)
            self.assertIn(b'<p>High SCore:', res.data)
            self.assertIn(b'Seconds left:', res.data)
            self.assertIsNone(session.get('highscore'))
            self.assertIsNone(session.get('nplays'))

    def test_invalid_word(self):
        """Test if word is valid"""

        self.client.get('/')
        response = self.client.get('/check-word?word=impossible')
        self.assertEqual(response.json['result'], 'not-on-board')

    def non_english_word(self):
        """Test if word is on the board"""

        self.client.get('/')
        response = self.client.get(
            '/check-word?word=lalalaaa')
        self.assertEqual(response.json['result'], 'not-word')
