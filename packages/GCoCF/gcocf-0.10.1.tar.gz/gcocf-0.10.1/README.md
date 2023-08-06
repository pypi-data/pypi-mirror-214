# GCoCF (Clash of Clans War Monitor)

![PyPI](https://img.shields.io/pypi/v/GCoCF)

GCoCF is a Discord service that monitors Clash of Clans wars and sends updates to a Discord server through webhooks.

## Installation

First clone and enter the repository, run the following commands:

```bash
git clone https://github.com/GILLESMaster/GCoCF
cd GCoCF/
```

To install the package and its dependencies, run the following commands:

```bash
pip install flit
pip3 install flit
flit install --extras=all
```

To install the dependencies for the bot service, run the following commands:

```bash
cd GCoCF_Bot/
pip install -r requirements.txt
pip3 install -r requirements.txt
```

To update the package and its dependencies, run the following commands:

```bash
git pull
flit install --extras=all
```

To install the package and its dependencies from PyPI, run the following command:

```bash
pip isntall GCoCF
```
or
```bash
pip3 install GCoCF
```

## Running the Bot

After installing, you can run the bot by using the following command:

```bash
GCoCF --coc-token {token_here} --clan-tag {tag_here} --webhook-url {url_here}
```

### Extra Options

- ```--mute-attacks```: Mutes notification for attacks
- ```--warlog```: Path to warlog.db
- ```--loglevel```: Sets the logging level
- ```--dryrun```: Runs the bot without sending notifications or saving data

## Running Tests

You can run the test cases by using the following command:

Webhook program:

```bash
pytest test_everything.py -v --capture=no
```

Bot service program:

```bash
cd GCoCF_Bot/
pytest test_everything.py -v --capture=no
```