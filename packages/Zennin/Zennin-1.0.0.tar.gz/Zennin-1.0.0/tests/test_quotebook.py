import unittest
from zennin import QuoteBook
import tempfile
import os
import random


QUOTES = [
'''Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor
incididunt ut labore et dolore magna aliqua. Tincidunt ornare massa eget
egestas purus. Posuere sollicitudin aliquam ultrices sagittis orci a
scelerisque purus semper. Sit amet tellus cras adipiscing enim eu turpis
egestas. Fermentum et sollicitudin ac orci. Lorem dolor sed viverra ipsum nunc
aliquet bibendum. Commodo nulla facilisi nullam vehicula ipsum a arcu cursus.
Praesent tristique magna sit amet purus gravida quis. Sed vulputate mi sit amet
mauris commodo. Sed augue lacus viverra vitae congue eu consequat ac felis.
Elit scelerisque mauris pellentesque pulvinar pellentesque habitant morbi.
Congue nisi vitae suscipit tellus mauris a diam maecenas. Placerat vestibulum
lectus mauris ultrices eros in cursus turpis massa. Sed elementum tempus
egestas sed sed risus. Sapien eget mi proin sed libero. Suspendisse in est ante
in nibh mauris cursus mattis.''',


'''Nec feugiat in fermentum posuere urna nec tincidunt praesent semper. Augue
interdum velit euismod in pellentesque massa placerat. Fermentum dui faucibus
in ornare quam viverra orci.''',


'''Elit duis tristique sollicitudin nibh sit amet commodo nulla facilisi. Integer
feugiat scelerisque varius morbi enim nunc faucibus. Ac tortor vitae purus
faucibus ornare suspendisse.''',


'''Nunc congue nisi vitae suscipit tellus mauris a diam. Habitant morbi tristique
senectus et netus et malesuada fames ac. Donec ac odio tempor orci dapibus
ultrices in iaculis. Quis imperdiet massa tincidunt nunc pulvinar sapien et.
Leo integer malesuada nunc vel risus commodo. Sodales ut etiam sit amet. Amet
consectetur adipiscing elit pellentesque habitant morbi tristique senectus. Eu
facilisis sed odio morbi quis commodo odio aenean sed. Accumsan tortor posuere
ac ut consequat. Enim diam vulputate ut pharetra sit amet aliquam. Donec
adipiscing tristique risus nec feugiat in fermentum posuere. Magnis dis
parturient montes nascetur ridiculus mus mauris vitae ultricies.

Tristique nulla aliquet enim tortor at. Suspendisse in est ante in nibh mauris
cursus mattis. Lorem ipsum dolor sit amet consectetur adipiscing elit
pellentesque. Scelerisque felis imperdiet proin fermentum leo vel. Tortor
pretium viverra suspendisse potenti nullam ac.''',


'''Consectetur purus ut faucibus pulvinar elementum integer.''',
]

NUM_OF_QUOTES_IN_TEST_FILE = 100

random_quotes = random.choices(QUOTES, k=NUM_OF_QUOTES_IN_TEST_FILE)

DEFAULT_SEPARATOR = "'''"
RANDOM_SEPARATOR = "***"

DEFAULT_SEPARATOR_QUOTE_BOOK_CONTENT = ""

for quote in random_quotes:
    DEFAULT_SEPARATOR_QUOTE_BOOK_CONTENT += f"{DEFAULT_SEPARATOR}\n"
    DEFAULT_SEPARATOR_QUOTE_BOOK_CONTENT += quote
    DEFAULT_SEPARATOR_QUOTE_BOOK_CONTENT += f"\n{DEFAULT_SEPARATOR}\n"
    DEFAULT_SEPARATOR_QUOTE_BOOK_CONTENT += f"\n\n"

RANDOM_SEPARATOR_QUOTE_BOOK_CONTENT = ""
for quote in random_quotes:
    RANDOM_SEPARATOR_QUOTE_BOOK_CONTENT += f"{RANDOM_SEPARATOR}\n"
    RANDOM_SEPARATOR_QUOTE_BOOK_CONTENT += quote
    RANDOM_SEPARATOR_QUOTE_BOOK_CONTENT += f"\n{RANDOM_SEPARATOR}\n"
    RANDOM_SEPARATOR_QUOTE_BOOK_CONTENT += f"\n\n"


class TestZennin(unittest.TestCase):

    def setUp(self):
        '''
        This will be runned before every test
        '''
        self.default_separator_quote_book = tempfile.NamedTemporaryFile().name
        with open(self.default_separator_quote_book, mode="w") as file:
            file.write(DEFAULT_SEPARATOR_QUOTE_BOOK_CONTENT)

        self.random_separator_quote_book = tempfile.NamedTemporaryFile().name
        with open(self.random_separator_quote_book, mode="w") as file:
            file.write(RANDOM_SEPARATOR_QUOTE_BOOK_CONTENT)

        self.default_separator_book = QuoteBook(self.default_separator_quote_book)
        self.random_separator_book = QuoteBook(self.random_separator_quote_book, quote_separator=RANDOM_SEPARATOR)


    def tearDown(self):
        '''
        This will be runned after every test
        '''
        os.remove(self.default_separator_quote_book)
        os.remove(self.random_separator_quote_book)


    def test_QuoteBook_class(self):
        expected_quotes = random_quotes
        self.assertEqual(self.default_separator_book.quotes, expected_quotes)
        self.assertEqual(self.random_separator_book.quotes, expected_quotes)


    # TODO: A better way to test this using mock or wathever
    def test_print_quotes(self):
        print('NEXT QUOTES MUST BE ON THE LEFT')
        self.default_separator_book.print_quote(1, "left")
        self.random_separator_book.print_quote(1, "left")
        print('NEXT QUOTES MUST BE ON THE RIGHT')
        self.default_separator_book.print_quote(1, "right")
        self.random_separator_book.print_quote(1, "right")
        print('NEXT QUOTES MUST BE ON THE CENTER')
        self.default_separator_book.print_quote(1, "center")
        self.random_separator_book.print_quote(1, "center")


if __name__ == '__main__':
    unittest.main()
