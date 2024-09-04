# Voice Cloner

Welcome to the DiscordLLM repository ! This project provides a discord bot to chat with Deepseek-Chat V2.

## Table of Contents

- [Features](#features)
- [Requirements](#requirements)
- [Installation](#installation)
- [Usage](#usage)
- [Improvements](#Improvements)
- [Contributing](#contributing)
- [License](#license)



## Features
- Discord bot with a command to start a chat with a LLM (needs to be a Open AI Server)

  
## Requirements
- python = >=3.10,<3.12
- Poetry (https://python-poetry.org/)

## Installation
```bash
git clone https://github.com/greg2705/DiscordLLM
cd DiscordLLM
poetry lock
poetry install
```
## Usage
Create a .env file with your API_key (change the base_url too) and the discord_token. 
```bash
poetry shell
cd discordllm
poetry python bot.py
```


## Improvements
- More commands
- More backends
  
## Contributing
The code is not perfect and may contains bugs, don't hesitate to open a PR or a Issues.
## License
This project is licensed under the Apache 2.0 License - see the LICENSE file for details.
