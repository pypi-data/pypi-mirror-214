#!/usr/bin/env python3

import shutil

class QuoteBook:
    '''
    Creates a quotebook
    :param1: String. Path of file with quotes
    :param2: String. Character or set of characters used to separate each
             different quote in the file. Tree single quotes are the default
    '''

    def __init__(self, quotes_file, quote_separator="'''"):
        self.quotes_file = quotes_file
        self.quote_separator = quote_separator
        self.__create_book()
        self.quotes_quantity = len(self.quotes)


    def __create_book(self):
        '''
        Creates a list from the quotes file. Each quote from the file must be
        separated by the character defined in the separator parameter
        :param1: 
        :param2: String. Character or set of character used to separate each quote
                 in the file.
        :returns: List. Each element of the list is a different quote.
        '''

        with open(self.quotes_file) as quotes_file:
            quotes = quotes_file.read()

        file_list = quotes.split(self.quote_separator)

        # Remove elements in the list that only contains spaces
        # This allows to separate each quote in the file with empty lines,
        # making it more readable.
        quotes_list = []
        for quote in file_list:
            if not quote.isspace() and not len(quote) == 0:
                quotes_list.append(quote.strip())

        self.quotes = quotes_list

        return self.quotes


    def print_quote(self, quote_num, justify_position):
        '''
        :param1: Int. Position of the quote that you want to print.
        :param2: String. Desided justified position. Valid positions: left, right,
                 center.
        :returns: Prints string in the terminal in the desided position.
        '''

        # CYAN = '\033[96m'
        # DARKCYAN = '\033[36m'
        # BLUE = '\033[94m'
        # GREEN = '\033[92m'
        # YELLOW = '\033[93m'
        # RED = '\033[91m'
        # UNDERLINE = '\033[4m'

        BOLD = '\033[1m'
        END = '\033[0m'

        quote_num -= 1 #  So you select the real position of the quote
        try:
            selected_quote = self.quotes[quote_num]
        except IndexError:
            print(f"[ERROR] {quote_num+1} outside of scope")
            print(f"You have {self.quotes_quantity} quotes in your book." )
            exit(1)

        quote_pick = selected_quote.split('\n')
        print(BOLD)
        quote_len = len(quote_pick)
        for sentence in range(quote_len):
            current_sentence = quote_pick[sentence]
            terminal_size = shutil.get_terminal_size().columns
            if justify_position.lower() == "left":
                print(current_sentence.ljust(terminal_size)) #  Left justification

            elif justify_position.lower() == "right":
                print(current_sentence.rjust(terminal_size)) #  Right justification

            elif justify_position.lower() == "center":
                print(current_sentence.center(terminal_size)) #  Center justification
            else:
                print("Invalid parameter. Only left, center or right is allowed")
                exit(1)

        print(END)


    def how_many_quotes(self):
        print(f"You have {self.quotes_quantity} quotes in your book")
