![](https://repository-images.githubusercontent.com/581593941/15fbc490-038b-44f2-8f94-a52f678e3245)
# RPG Random BOT / Dice Roller

**RPG Random BOT/ Dice Roller** is Discord Bot for rolling dice.

## Installation

[Python 3.9](https://www.python.org/downloads/release/python-3915/) 

[pip](https://pip.pypa.io/en/stable/) to install [discord.py](https://discordpy.readthedocs.io/en/stable/).

```bash
pip install discord numpy matplotlib pandas
```
In **config.json** put your discord bot token in 
```json
{
    "token": "Your_Bot_Token_Or_Ask_Me_For_It",
    "prefix": "!",
    "min": 1,
    "role" : "The_Role_Optionnal_if_you_have_admin_permission"
}
```  
You can also modify the min and the prefix of le bot  

**Or go in [release tab](https://github.com/ekomlenovic/RPG-Random-Bot/releases) and download .exe**  
And add it to your server :  
**https://discord.com/oauth2/authorize?client_id=900518092944326686&scope=bot&permissions=8**

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
!!!!!!!!!!!!!HIDDEN COMMANDS !!!!!!!!!!!!!
!cheat [NAME] min max  # This command creates piped dice for the user
!clear_cheat [NAME] | !cc [NAME] #Clear the cheating dictionnary of the user
```

## Contributing

Pull requests are welcome. For major changes, please open an issue first
to discuss what you would like to change.  

Translator are welcome!

Please make sure to update tests as appropriate.

## Contributor

Special thanks to [Saprinox](https://github.com/Saprinox)

## License

[MIT](https://choosealicense.com/licenses/mit/)
