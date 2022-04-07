"""The main file that handles launching the bot."""

import sys
from setup.client import BotClient

def main():
    """The main function launches the bot.
    The function assumes that, upon launch, the bot token is given as an argument.
    The bot token should NEVER be hard-coded into the program. Either copy-paste
    it as an argument on each launch or store it in an encrypted file and use the
    decrypted value as an argument."""

    client = BotClient()
    client.run(str(sys.argv[1]))

if __name__ == "__main__":
    main()
