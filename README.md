# LikahBot
[Trello board](https://trello.com/b/ofVmXaHM/likah-bot)
## What is LikahBot?
LikahBot is an open source general purpose Discord bot utilising the Pycord library. It's a project I originally started when I had minimal knowledge about programming practices. This repository is the complete rewrite of that original project.
## How do I use the bot?
Do note that the bot is in a very very early stage of development currently and following the instructions below will not yet guarantee a usable bot.
### Instructions for Linux users
1. Clone the repository
2. Navigate to the root of the cloned directory
3. Create a new virtual environment
  - e.g. `python3 -m venv botenv`
4. Launch the virtual environment
  - e.g. `source botenv/bin/activate`
5. Install the required dependencies
  - `python3 -m pip install -U requirements.txt`
6. Initialize the bot's database
  - `sqlite3 database/database.db < database/schema.sql`
  - Change the DB_ADDRESS constant in [constants.py](https://github.com/Veloxization/likahbot/blob/main/src/config/constants.py) to reflect whatever name you gave the database
7. Change the DEBUG_GUILDS constant in [constants.py](https://github.com/Veloxization/likahbot/blob/main/src/config/constants.py) to `[]`
  - If you're not going to make the bot public, you can also list the IDs of the guilds you're going to use the bot on
  - Note that making a slash command public may take a while to register
8. Create a new application and bot user through [Discord Developer Portal](https://discord.com/developers/applications)
9. Invite the bot to your Discord server
  - e.g. use link: `https://discord.com/oauth2/authorize?client_id=[your client id here]&scope=bot%20applications.commands&permissions=[your permission integer here]`
  - Select your server from the list
10. Get your bot's secret token from the developer portal and keep it safe
11. Launch the bot
  - `python3 src/bot.py [your secret token here]`
  - Optional ways to launch in the next steps
#### Option 1: Environmental variables
1. Create a new environmental variable
  - e.g. `export BOT_TOKEN=[your secret token here]`
2. Launch the bot using the environmental variable
  - e.g. `python3 src/bot.py $BOT_TOKEN`
#### Option 2: Encrypted file and the `run.sh` script
1. Install `gnupg` on your system
2. Create an extensionless file to store your token
  - `echo [insert your token] > token`
3. Encrypt your token file
  - `gpg -c token`
  - Come up with a strong enough password. You'll be needing it to launch the bot in the future.
  - A file called token.gpg should be created in the root directory
4. Delete the original token file
5. To run the bot, use `./run.sh` (make sure you give it permission to execute)
  - Type in the password if asked
## Planned features
* Dashboard
* Automod
* Logging
* Verification
* Moderation commands
* Punishment histories
* Reminders
* Birthday wishes
* Raffles and polls
* Experience and leveling
* Currency and economy
* and much more
