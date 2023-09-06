#=========== ThePao's Code =======#
import discord
from discord.ext import commands
import os
import random

intents = discord.Intents.all()
intents.members = True
client = discord.Client(intents=intents)
GUILD = 871501115454283797
teamA = []
teamB = []
underCover = []
teamA_active = False
teamB_active = False
voteA_status = False
voteB_status = False
teamSize = 5
game_status = False


@client.event
async def on_ready():
  print("We have logged in as {0.user}".format(client))
  print("TestCommand Ready!")


@client.event
async def on_message(message):
  global teamA_active, teamB_active, game_status, voteA_status, voteB_status,teamA,teamB
####定义check 函数
  def check_team_choice(m):
    return m.author == message.author and m.channel == message.channel and m.content.lower() in ['a', 'b']
  if message.author == client.user:
    return
  
  if message.content == '开始内战':
    await startGame()
    await message.channel.send("选择开始组建A队或B队，输入'A'或者'B'")
    
  if message.content == "公布内鬼" and teamA_active and teamB_active:
    await message.channel.send(f"内鬼是{underCover[0]}, {underCover[1]}")
    print(f"===============内鬼是{underCover[0]}, {underCover[1]}")
    return
  if message.content == "开始投票" and teamA_active and teamB_active:
    await message.channel.send(f"请输入为A队或B队投票，输入'A'或者'B'")
    team_choice_response = await client.wait_for('message',
                                                 check=check_team_choice)
    team_choice = team_choice_response.content.lower()
    if team_choice == 'a' and not voteA_status:
      voteA_status = True
      await vote(message,team_choice)
    if team_choice == 'b'and not voteB_status:
      voteB_status = True
      await vote(message,team_choice)
    
  if game_status:
    team_choice_response = await client.wait_for('message',
                                                 check=check_team_choice)
    team_choice = team_choice_response.content.lower()
    if team_choice == 'a' and not teamA_active:
      teamA_active = True
      await listenToTeam(message, team_choice_response, team_choice)
      return
    elif team_choice == 'b' and not teamB_active:
      teamB_active = True
      await listenToTeam(message, team_choice_response, team_choice)
      return


async def vote(message,team_choice):
  global teamA_active, teamB_active, game_status,teamA,teamB
  team = teamA if team_choice == 'a' else teamB
  result = ','.join(str(i+1) + "号:" + x.global_name for i, x in enumerate(team))
  await message.channel.send(f"{team_choice.upper()}队人员编号为：{result}")
  await message.channel.send("请开始投票")
  

async def startGame():
  global teamA_active, teamB_active, game_status, voteA_status, voteB_status,teamA,teamB
  print('Start Game!!!!')
  game_status = True
  teamB_active = False
  teamA_active = False
  teamA = []
  teamB = []
  underCover = []


async def listenToTeam(message, team_choice_response, team_choice):
  global teamA, teamB
  team = teamA if team_choice == 'a' else teamB

  await message.channel.send(
      f"{team_choice_response.author} 选择了 {team_choice.upper()}队.")

  await message.channel.send(f"请@出{team_choice.upper()}队的成员:")

  def check(m):
    return m.author == message.author and m.channel == message.channel
  user_response = await client.wait_for('message', check=check)
  message = user_response
  if message.mentions:
    mentioned_users = message.mentions
    for a in mentioned_users:
      if len(team) < teamSize:
        team.append(a)
      else:
        await message.channel.send(
            f'{team_choice.upper()}队不能超过{teamSize}人，请重新输入')
    res = ','.join(x.global_name for x in team)
    await message.channel.send(f'{team_choice.upper()}队: {res}')
    choosed_user = random.choice(mentioned_users)
    underCover.append(choosed_user.global_name)
    await message.channel.send(f'内鬼已经选出，请查看Discord私信')

    await choosed_user.send('你是内鬼，收到回复（回复任何字符都可）')

  def check_yes(m):
    return m.author == choosed_user and len(m.content) != 0 and isinstance(
        m.channel, discord.DMChannel)

  user_response = await client.wait_for('message', check=check_yes)

  if len(user_response.content) != 0:
    await message.channel.send(f'已收到 {team_choice.upper()} 队内鬼的回复')


client.run(os.getenv('TOKEN'))