# RoosterBot v2


## Dev using docker & VScode
- install the `Docker` and `Remote - Containers` extensions
- ctrl+shift+p to open the command palette, enter Remote-Containers: Open Folder in Container
- select the project folder
- choose use existing dockerfile

VScode will build and run the container according to the dockerfile and mount the dev workspace as a volume

to run the bot:
```bash
python app/main.py
```


## Dev using docker && pycharm
- build the container
```bash 
docker build -t roosterbot
```
- follow [PyCharm Docker Integration](https://www.jetbrains.com/help/pycharm/using-docker-as-a-remote-interpreter.html#config-docker) using the `roosterbot` image
