# commodore

as simple as editing a `yaml` file!
set your key as the bot command and set its corresponding value
to send to the user whenever user sent the command.

### YAML syntax

a list of key/value pair. key as the command and the message as the answerer.
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
- set `API_KEY` for bot token
- python3 -m venv .env
- source .env/bin/activate
- ./main.py

> docker version is in the way so don't worry, you will just need
> to simply set the `API_KEY`, thats all.
