# discord-init-tracker-bot
discord-init-tracker-bot

# Use discord as your initiative tracker tool
Do quite literally as the title said!

## To use

You need to 
1. Create and assign your own discord bot.
2. Run or use this main.py and bot.py script in your python idle.



## Command List

`!cb set`
- use to set up the initiative, and prompt anyone to join.

`!cb join [num/dice roll]` or `!cb j [num/dice roll`
- use to add member to the encounter round, will do nothing if no encounter is running.
- will require num or dice roll to arrange the order, num should be an integer while dice go in the format of XdY (in X = a number of dice and Y = side of dice (i.e. 2d20 = roll 2 of 20 sided dice)).

`!cb start`
- use to start the combat, should be used after everyone is ready.
- will show the full list of combatants in order.

`!cb next`
- use to move turn from the current combatant to the next in order.
- if reach the end of the list, will move back to the first in order while counting as a next round.

`!cb remove [index]`
- use to remove combatant from combat, need integer index to select.

`!cb end`
- use to end the combat phase.

`!cb list`
- use to show full order list.


`!cb roll`
- use to roll the dice with the format of XdY, can add modification of XdY+A
## License

[MIT](https://choosealicense.com/licenses/mit/)
