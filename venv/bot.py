import re
import discord
import random

combat_list = []
is_active_battle = False
is_ready = False
round_count = 0
current_index = 0

# Send messages
async def send_message(message, text):
    try:
        await message.channel.send(text)
    except Exception as e:
        print(e)


async def reply_message(message, text):
    try:
        await message.reply(text)
    except Exception as e:
        print(e)


def run_discord_bot():
    TOKEN = '' # place your token here
    intents = discord.Intents.default()
    intents.message_content = True
    client = discord.Client(intents=intents)

    @client.event
    async def on_ready():
        print(f'{client.user} is now running!')

    @client.event
    async def on_message(message):
        global is_active_battle, round_count, is_ready, current_index
        if message.author == client.user:
            return
        username = str(message.author)
        user_message = str(message.content)
        channel = str(message.channel)
        print(f"{username} said: '{user_message}' ({channel})")
        if user_message[:3] == '!cb':
            u_msg_list = user_message.split()
            command = u_msg_list[1]
            if command == "set":
                if not is_active_battle:
                    is_active_battle = True
                    await send_message(message, "**=== The encounter is about to start! ===**\n use `!cb join` to join!")
                else:
                    await send_message(message, "Encounter is already running")
                    return
            elif command == "join" or command == "j":
                if not is_active_battle:
                    await send_message(message, "No encounter running")
                    return
                name = u_msg_list[2]
                roll_list = []
                if 'd' in u_msg_list[3]:
                    roll_list, roll_result = dice(u_msg_list[3])
                else:
                    roll_result = u_msg_list[3]
                combatant = {
                    "name": name,
                    "init": int(roll_result),
                    "user": username,
                    "is_active": False
                }
                combat_list.append(combatant)
                combat_list.sort(key=lambda x: x["init"], reverse=True)
                if roll_list:
                    await reply_message(message, f"**{name}** join the encounter with ({u_msg_list[3]}) => **{roll_result}**!")
                else:
                    await reply_message(message, f"**{name}** join the encounter with **{roll_result}**!")
                return
            elif command == "start" or command == "s":
                if not is_active_battle:
                    await send_message(message, "No encounter running")
                    return
                combat_list[0]["is_active"] = True
                await show_list(message, combat_list, round_count)
                is_ready = True
                return
            elif command == "next" or command == "n":
                if not is_active_battle:
                    await send_message(message, "No encounter running")
                    return
                if current_index < len(combat_list)-1:
                    combat_list[current_index]["is_active"] = False
                    current_index += 1
                    combat_list[current_index]["is_active"] = True
                else:
                    combat_list[current_index]["is_active"] = False
                    round_count += 1
                    current_index = 0
                    combat_list[current_index]["is_active"] = True
                await show_list(message, combat_list, round_count)
                return
            elif command == "remove" or command == "r":
                if not is_active_battle:
                    await send_message(message, "No encounter running")
                    return
                remove_index = int(u_msg_list[2]) - 1
                await send_message(message, f"Remove **{combat_list[remove_index]['name']}** from the encounter!")
                combat_list.pop(remove_index)
                return
            elif command == "end" or command == "e":
                if not is_active_battle:
                    await send_message(message, "No encounter running")
                else:
                    is_active_battle = False
                    is_ready = False
                    await send_message(message, "**=== THE ENCOUNTER IS END! ===**")
                return
            elif command == "list":
                await show_list(message, combat_list, round_count)
            elif command == "roll":
                dice_arr, total = dice(u_msg_list[2])
                await reply_message(message, f"You rolled: {dice_arr} \n**★ SUM => {total}**")
    client.run(TOKEN)

async def show_list(message, combat_list, round_count):
    try:
        title = f"Battle List - Round {round_count}"
        desctp = ""
        loop_count = 0
        for c in combat_list:
            desctp += f"{loop_count+1}. {c['name']}"
            if c["is_active"]:
                desctp += " ⚔️⚔️⚔️ \n"
            else:
                desctp += "\n"
            loop_count += 1
        embed = discord.Embed(title=title, description=desctp, color=0xdb0000)
        await message.channel.send(embed=embed)
    except Exception as e:
        print(e)


def dice(dice_string):
    pattern = re.compile(r'(\d*)d(\d+)')
    matches = pattern.finditer(dice_string)
    roll_list = []
    total = 0
    round_count = 0
    for match in matches:
        dice_count = int(match.group(1) or '1')
        dice_sides = int(match.group(2))
        roll = [random.randint(1, dice_sides) for _ in range(dice_count)]
        roll_list.append(roll)
        result = sum(roll)
        total += result
        round_count+=1
    modifier = []
    modifier = re.findall(r'([+-](?!\d*d)\d*\w*)', dice_string)
    if modifier:
        for mod in modifier:
            total = eval(f"{total}{mod}")
    return roll_list, total



