import unittest
from unittest.mock import patch
from declareMastermind import *

class TestSuite(unittest.TestCase):

    def test_color_parse(self):
        # Testing valid colors
        self.assertEqual(Colour.parse('r'), Colour.red)
        self.assertEqual(Colour.parse('g'), Colour.green)
        self.assertEqual(Colour.parse('b'), Colour.blue)
        self.assertEqual(Colour.parse('y'), Colour.yellow)
        self.assertEqual(Colour.parse('o'), Colour.orange)
        self.assertEqual(Colour.parse('p'), Colour.purple)
        self.assertEqual(Colour.parse('i'), Colour.indigo)
        self.assertEqual(Colour.parse('v'), Colour.violet)
        # Testing invalid colors
        self.assertIsNone(Colour.parse('x')) # Doesn't exist

    def test_pattern_parse(self):
        # Testing valid pattern parsing
        pattern = Pattern.parse('rgby')
        self.assertIsNotNone(pattern)
        self.assertEqual(pattern, Pattern(Colour.red, Colour.green, Colour.blue, Colour.yellow))
        # Testing invalid pattern parsing
        self.assertIsNone(Pattern.parse('rgbyx')) # Pattern too long
        self.assertIsNone(Pattern.parse('rgb')) # Pattern too short

    def test_feedback(self):
        code = Pattern(Colour.red, Colour.green, Colour.blue, Colour.yellow)

        # Test feedback for a correct guess
        guess = Pattern(Colour.red, Colour.green, Colour.blue, Colour.yellow)
        feedback = Feedback.giveFeedback(code, guess)
        self.assertEqual(feedback, [Feedback.Black, Feedback.Black, Feedback.Black, Feedback.Black])

        # Test feedback with correct coloprs but some in different positions
        guess = Pattern(Colour.red, Colour.blue, Colour.green, Colour.yellow)
        feedback = Feedback.giveFeedback(code, guess)
        self.assertEqual(feedback.count(Feedback.Black), 2)
        self.assertEqual(feedback.count(Feedback.White), 2)

        # Test feedback with correct colors but all in different positions
        guess = Pattern(Colour.yellow, Colour.red, Colour.green, Colour.blue)
        feedback = Feedback.giveFeedback(code, guess)
        self.assertEqual(feedback.count(Feedback.White), 4)
        self.assertEqual(feedback.count(Feedback.Black), 0)

        # Test feedback with wrong colors
        guess = Pattern(Colour.purple, Colour.orange, Colour.indigo, Colour.violet)
        feedback = Feedback.giveFeedback(code, guess)
        self.assertEqual(feedback.count(Feedback.White), 0)
        self.assertEqual(feedback.count(Feedback.Black), 0)

    def test_feedback_length(self):
        # Test feedback length to ensure it's 4
        code = Pattern(Colour.red, Colour.green, Colour.blue, Colour.yellow)
        guess = Pattern(Colour.red, Colour.green, Colour.blue, Colour.yellow)
        feedback = Feedback.giveFeedback(code, guess)
        self.assertEqual(len(feedback), 4)

    def test_board_display(self):
        # Test that the board generates a properly generated string
        feedback = [Feedback.Black, Feedback.White, Feedback.Null, Feedback.Null]
        guess = Pattern(Colour.red, Colour.blue, Colour.green, Colour.yellow)
        board = Generateboard(feedback, guess)
        self.assertIn("Guess: ", board)
        self.assertIn("Feedback: ['Black', 'White', 'Null', 'Null']", board)
        self.assertIn("Current Board:", board)

    @patch('builtins.input', return_value='rgby') # Mocking user input, correct guess
    def test_correct_guess(self, mock_input):
        # Test if the game is won when a correct guess is made
        code = Pattern(Colour.red, Colour.green, Colour.blue, Colour.yellow)
        result = guessing(code)
        self.assertTrue(result)

    @patch('builtins.input', side_effect=['poiv']*10) # Mocking user input 10 times, incorrect guesses
    def test_out_of_guesses_loses(self, mock_input):
        # Test 10 incorrect guesses result in a loss
        code = Pattern(Colour.red, Colour.green, Colour.blue, Colour.yellow)
        self.assertFalse(guessing(code))

    def test_game_mode_parse(self):
        # Test parsing game modes
        self.assertEqual(GameMode.parse('1'), GameMode.PVP)
        self.assertEqual(GameMode.parse('2'), GameMode.PVCPU)
        self.assertEqual(GameMode.parse('3'), GameMode.CAMPAIGN)
        self.assertEqual(GameMode.parse('4'), GameMode.QUIT)
        self.assertIsNone(GameMode.parse('5'))

if __name__ == '__main__':
    unittest.main()