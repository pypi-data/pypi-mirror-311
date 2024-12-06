import sys
import unittest
from unittest.mock import patch

# Add the src directory to the path before importing
sys.path.insert(0, "./src")

# Import the function from the correct file
from gutentag_world.say_hello import say_hello  # Import from say_hello.py


class TestSayHello(unittest.TestCase):
    @patch("builtins.print")  # Patch the built-in print function
    def test_say_hello(self, mock_print):
        # Call the function
        say_hello()

        # Assert that print was called with the correct string
        mock_print.assert_called_once_with("Gutentag, World!")


if __name__ == "__main__":
    unittest.main()
