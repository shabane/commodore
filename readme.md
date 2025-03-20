# commodore

as simple as editing a `yaml` file!
set your key as the bot command and set its corresponding value
to send to the user whenever user sent the command.

### YAML syntax

a list of key/value pair. key as the command and the value as the answerer

```yaml
    commands:
      - key: help
        value: this bot can do something 

      - key: foo
        value: bar
```

### How to run?
- set `API_KEY` for bot token
- python3 -m venv .env
- source .env/bin/activate
- ./main.py

> docker version is in the way so don't worry, you will just need
> to simply set the `API_KEY`, thats all.
