# commodore

as simple as editing a `yaml` file!
set your key as the bot command and set its corresponding value as response message
to send it to user whenever user sent that command.

> this is **NOT STABLE** yet, and this will be 2en version.

> in the peace of code i used feature rich library `python-telgram-bot` to interact with telegram bots.
> in the previous version i write my own peace of sh*t that used telegram API to send files, and
> also i used the shiteist library ever `telebot` which does not support anything but send/receive simple
> text messages.
> in this version, the code will support business messages too.
> also i will add some more other feature to yaml syntax to support **captions** for any files.

### YAML syntax

a list of key/value pair. key as the command and the message as the answare.
you can have a list of each **photos, audios, documents, videos**.

```yaml
commands:
    - key: foo
      message: bar
      photos:
        - "path/2/1.jpg"
        - "assets/2.jpg"

    - key: foo2
      message: bar2
      audios:
        - "assets/audio.ogg"
      photos:
        - "assets/1.jpg"
      documents:
        - "assets/1.pdf"
      videos:
        - "assets/1.mp4"

    - key: hi
      message: hi there, how are you?
```

### How to run?

- run `git clone --depth 1 https://github.com/shabane/commodore.git && cd commodore`
- set `API_KEY` for bot token
- python3 -m venv .env
- source .env/bin/activate
- pip install -r ./requirements.txt
- ./main.py

> dont forget to add your command to `prompts.yaml` file.

or just use docker!

### Docker

at first you should add your commands to `prompts.yaml` file, then if you have any other files, add them to any dir you want.
remember that you should specifiy this path in your `prompts.yaml`. then just volume this dir and files to the container.

```bash
docker run -d -v ./prompts.yaml:/code/prompts.yaml -v ./assets:/code/assets -e API_KEY='<API_KEY>' mshabane/commodore:1.0.0
```

> if you make any changes in `PPROMPTS_FILE`, the script will auto reload! **so you do not need to `docker restart`**

### Evn

|           key | value example |          description    |   required    |
|:-------------:|:-------------:|:-----------------------:|:-------------:|
|     API_KEY   |   xxxx:yyyy   | this is you bot api key |     require   |
| WRONG_CMD_MSG | "wrong command" | message to send if user enter wront command | optional |
| PROMPTS_FILE  | ./prompts.yaml | YAML file that contain list of commands | optional |

