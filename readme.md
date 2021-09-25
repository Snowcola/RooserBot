# RoosterBot v2


## Using Docker & VScode
- install the `Docker` and `Remote - Containers` extensions
- ctrl+shift+p to open the command palette, enter Remote-Containers: Open Folder in Container
- select the project folder
- choose use existing dockerfile

VScode will build and run the container according to the dockerfile and mount the dev workspace as a volume

to run the bot:
```bash
python app/main.py
```
if you have added new slash commands run the bot with the `-s` flag. **Discord has very restrictive rate limiting on this action, perform sparringly**

## Using Docker & PyCharm
- build the container
```bash 
docker build -t roosterbot
```
- follow [PyCharm Docker Integration](https://www.jetbrains.com/help/pycharm/using-docker-as-a-remote-interpreter.html#config-docker) using the `roosterbot` image


## Environment variables

### Required:
- `DISCORD_TOKEN`: Bot token from the discord developer portal

### Optional:
- `BOT_LOG_LEVEL`: log level for RoosterBot [debug, info, warn, critical, fatal]
- `DISCORD_LOG_LEVEL`: log level for Discord.py [debug, info, warn, critical, fatal]
- `APP_ID`: Application ID from the discord developer portal: REQUIRED to update commands via manage.py

## Adding, Updating and Removing Commands
- [Discord API Documentation](https://discord.com/developers/docs/interactions/application-commands)

## Dependencies
- `libiffi-dev`
- `libnacl-dev`
- `python3-dev`
- `ffmpeg`