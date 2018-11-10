# RadioBot for Discord

## Requirements
### Library
- `sudo apt-get install libffi-dev`
- `python3 -m pip install -U discord.py[voice]`
### Opus
- [Download](https://archive.mozilla.org/pub/opus/opus-1.3.tar.gz)
- `tar -xzf opus-1.3.tar.gz`
- `cd opus-1.3`
- `./configure && make`
- `sudo make install`
### FFmpeg
- `sudo apt-get install ffmpeg`

## How to run:
- Edit `config.py` and enter the required information.
- Run `radio.py`!
