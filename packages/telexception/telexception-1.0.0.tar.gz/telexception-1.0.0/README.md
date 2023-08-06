# Telexception

![Python](https://img.shields.io/badge/python-v3.6+-blue.svg)
![GitHub last commit](https://img.shields.io/github/last-commit/UrNickName16/Telexception)
![License](https://img.shields.io/badge/license-MIT-green.svg)

Telexception is a Python module that helps track raised exceptions in your code. When an exception is raised, Telexception sends a message to a specified Telegram chat.

## Features

- Sends automatic notifications to Telegram when exceptions are raised
- Can send traceback and log files for more detailed troubleshooting
- Easy to integrate into existing Python projects

## Installation

You can install Telexception using pip:

```bash
pip install telexception
```

## Usage

- Create telegram bot via @BotFather and get API_KEY

- Get user_id (you can find other telegram bots who can provide this information like @userinfobot)

- initialize the bot with your API key and user ID:

```python
bot = Telexception("api_key", "user_id")
```

Also you can send traceback or log file:

```python
bot = Telexception("api_key", "user_id", send_traceback=True, path_to_logs='path/to/logs.log')
```

Then, use the exception_handler decorator on any function you want to track:

```Python
@bot.exception_handler
def some_function_with_problems(*args, **kwargs):
    pass
```

When some_function_with_problems raises an exception, a message will be sent to the specified Telegram chat.

## License

This project is licensed under the terms of the MIT license.