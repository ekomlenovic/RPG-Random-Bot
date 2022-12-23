# RPG Random BOT / Dice Roller

**RPG Random BOT/ Dice Roller** is Discord Bot for rolling dice.

## Installation

[Python 3.9](https://www.python.org/downloads/release/python-3915/) 

[pip](https://pip.pypa.io/en/stable/) to install [discord.py](https://discordpy.readthedocs.io/en/stable/).

```bash
pip install discord numpy matplotlib 
```
In main.py put your discord bot token in 
```python
bot.run('Your_TOKEN')
```

## Usage

Create a [Discord Bot](https://discord.com/developers/applications) and invite it on your server.  
Put your APPLICATION ID in this link in order to invite the bot to your Discord.  
```python
https://discord.com/oauth2/authorize?client_id=your_APPLICATION_ID&scope=bot&permissions=8
```
When the Bot joins your server, you can use the following commands:

```python
!help to see commands
!r [number of sides] # example: !r 20 it's beween 0 and 20
```

## Contributing

Pull requests are welcome. For major changes, please open an issue first
to discuss what you would like to change.  

Translator are welcome!

Please make sure to update tests as appropriate.

## License

[MIT](https://choosealicense.com/licenses/mit/)