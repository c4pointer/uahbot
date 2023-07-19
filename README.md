# uahbot

## About

This is simple bot for parsing currency data from main and most popular Bank in Ukraine:
- Monobank
- Privat bank

# Telegram Bot Readme

This Markdown readme file provides an overview and explanation of the Python code snippet related to a Telegram bot. The code snippet demonstrates the implementation of a Telegram bot using the Telebot library. The bot performs various functions, such as handling commands, maintaining user information, and displaying chat IDs and topic IDs.

## Requirements

Before running the bot, ensure you have the following prerequisites:

1. Python: The code requires Python to be installed on your system. It is recommended to use Python 3.6 or higher.

2. Telebot Library: The bot is built using the `telebot` library, which is a Python wrapper for the Telegram Bot API. To install the library, use the following command:

   ```bash
   pip install pyTelegramBotAPI
   ```

3. SQLite3: The bot uses an SQLite3 database to store user information. SQLite3 is generally included with Python by default, so no additional installation is required.

## Code Explanation

1. The code starts by importing necessary modules and setting up the Telegram bot token.

2. The `send_welcome` function is the entry point of the bot when a user starts the conversation with the bot. It sets up an inline keyboard to display options to the user. The language of the keyboard and button texts is customized based on the user's language.

3. The `chat_handler` function determines whether the user is interacting with the bot privately or in a group. It checks if the `from_user.id` and `chat.id` are different. If they are, it means the user is in a group, and the function returns `True`, otherwise `False` for private chat.

4. The `update` function is responsible for storing or updating user information in the SQLite database. It connects to the `bot_db.db` database and either inserts a new user or updates the user's information if they already exist in the database.

5. The `send_info` function handles the `/chat_id` command. It sends the user_id in private messages and the group_id in groups. If the conversation is part of a topic, it also displays the topic_id.

6. The `text_handler` function is executed whenever the bot receives a text message. It calls the `chat_handler` function to handle user information updates.

## Database

The code uses an SQLite database named `bot_db.db` to store user information. The database contains a single table, `table_for_users`, with two columns: `chat_id` (INTEGER) and `name` (TEXT). The `chat_id` is used to uniquely identify users, and the `name` stores the username of the user or 'Empty' if the username is not available.

## Running the Bot

To run the bot, ensure that you have completed the requirements mentioned above. Then, follow these steps:

1. Insert your Telegram bot token in the appropriate location in the code.

2. Execute the Python script containing the code.

3. The bot will be up and running, waiting for users to interact with it.

## Interaction with the Bot

- When a user starts a conversation with the bot, an inline keyboard is displayed, allowing the user to view the bank list (translated based on their language).

- If the user interacts with the bot in a group, their information will not be stored in the database.

- If the user interacts with the bot privately, their information will be stored or updated in the SQLite database.

- The `/chat_id` command can be used to obtain the user_id (in private) or group_id (in groups). If the conversation is part of a topic, it will also display the topic_id.

## Note

Please keep in mind that this is a partial code snippet, and the implementation of some functions (e.g., `send_mesaages` and `notify_add`) is not provided. Additionally, make sure to handle exceptions and errors gracefully to ensure smooth functioning of the bot.

Remember to follow Telegram's [Bot API documentation](https://core.telegram.org/bots/api) for more details on available methods and functionalities.