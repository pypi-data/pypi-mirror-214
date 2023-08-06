from zennin.quotebook import QuoteBook
import random
import argparse
import os

CONFIG_FOLDER = os.path.expanduser("~/.config/zennin")
CONFIG_FILE_PATH = os.path.join(CONFIG_FOLDER, "quotebook.txt")
EXAMPLE_FILE_PATH = "/etc/quotebook.txt"

DEFAULT_JUSTIFICATION_POSITION = "center"


def main():
    '''
    Main function
    '''
    parser = argparse.ArgumentParser()
    parser.add_argument("-j", "--justify",
                        help="Justification position. Accepted values are left, center, right,",
                        choices=["left", "right", "center"])
    parser.add_argument("-f", "--file", help="Specify a file with quotes")
    parser.add_argument("-p", "--print", help="Print a specific quote", type=int)
    parser.add_argument("-n", "--number",
                        help="Tells how many quotes you have in your file",
                        action="store_true")

    args = parser.parse_args()

    if args.justify == "center":
        justification_position = "center"
    elif args.justify == "right":
        justification_position = "right"
    elif args.justify == "left":
        justification_position = "left"
    else:
        justification_position = DEFAULT_JUSTIFICATION_POSITION

    if args.file:
        file_path = args.file
    else:
        file_path = CONFIG_FILE_PATH

    try:
        zennin = QuoteBook(file_path)
    except FileNotFoundError:
        try:
            zennin = QuoteBook(EXAMPLE_FILE_PATH)
            print(f"{file_path} Doesn't exist. Using example file")
        except FileNotFoundError:
            print("No configuration file found")
            exit(1)

    if args.number:
        print(f"You have {zennin.quotes_quantity} quotes in your Quote Book")
        exit(0)

    if args.print:
        quote_num = args.print
    else:
        quote_num=random.randint(1, zennin.quotes_quantity)

    try:
        zennin.print_quote(quote_num, justification_position)
    except IndexError:
        print("Quote number outside of scope")
        print(f"You have {zennin.quotes_quantity} quotes")
        exit(1)


if __name__ == "__main__":
    main()
