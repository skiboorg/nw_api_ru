APP_ID = '524988531760824341'
PUBLIC_KEY = '9804530e9e58ae3db70cc75741c3f157af259e4e15a2667b58cb469eb014f445'
TOKEN = 'NTI0OTg4NTMxNzYwODI0MzQx.XBpzqw.-Rjlx4riQYBCx7z918GNx8pFBR4'

import discord
from discord.ext import commands
from discord.ext.commands import Bot

client = Bot(command_prefix="!",intents = discord.Intents.all())


# client = discord.Client()

@client.command()
async def test(ctx):
    pass
    # print(ctx)
    # embed = discord.Embed(title=f"Привет . Добро пожаловать в RED SKY",
    #                       description="Предлагаю познакомиться поближе, заполнив небольшую информацио о себе",
    #                       color=0xff0000)
    # embed.add_field(name="1. Ваш возраст", value='Просто цифры будет дотаточно;)', inline=False)
    # embed.add_field(name="2. Что ожидаешь от игры и клана", value='Нам важно понимать с какой целью ты тут', inline=False)
    # embed.add_field(name="3. Опыт в MMO играх", value='Буквально в 2х словах', inline=False)
    # embed.add_field(name="4. Сколько времени можешь уделять игре", value='У нас нет обязательного прайма, эта информация просто к сведению', inline=False)
    # embed.add_field(name="5. Предпочтения в игре (PVP,PVE,крафт)", value='Чтобы знать, кто у нас чем любит заниматься', inline=False)
    # embed.add_field(name="Пример, как можно ответить", value='25,Хочу играть,опыт 10лет в разные игры, могу играть 5-6 часов, нагибатор;))', inline=False)
    # await ctx.send(embed=embed)
    # await ctx.send('Для заполнения заявки просто ответь мне тут')


@client.event
async def on_message(message):
    if message.channel.id == message.author.dm_channel.id: # dm only
        print(message.author)
        channel = client.get_channel(861299235525230622)
        await channel.send(f"От: {message.author.mention}| Заявка: {message.content}")
        await message.author.send('Спасибо за предоставленную информацию, с тобой обязательно свяжутся. '
                                  'Если есть какие либо вопросы можешь смело писать <@404284131451863040> или <@288595376360128512>')
        #:question:U+003F
    elif not message.guild: # group dm only
        print(2)
    else: # server text channel
        print(3)



created_channels = []

@client.event
async def on_member_join(member):
    embed = discord.Embed(title=f"Привет . Добро пожаловать в RED SKY",
                          description="Предлагаю познакомиться поближе, рассказав немного о себе",
                          color=0xff0000)
    embed.add_field(name="1. Возраст", value='Просто цифры будет дотаточно;)', inline=False)
    embed.add_field(name="2. Что ожидаешь от игры и клана", value='Нам важно понимать с какой целью ты тут',
                    inline=False)
    embed.add_field(name="3. Опыт в MMO играх", value='Буквально в 2х словах', inline=False)
    embed.add_field(name="4. Сколько времени можешь уделять игре",
                    value='У нас нет обязательного прайма, эта информация просто к сведению', inline=False)
    embed.add_field(name="5. Предпочтения в игре (PVP,PVE,крафт)", value='Чтобы знать, кто у нас чем любит заниматься',
                    inline=False)
    embed.add_field(name="Пример, как можно ответить",
                    value='25,Хочу играть,опыт 10лет в разные игры, могу играть 5-6 часов, нагибатор;))', inline=False)
    await member.send(embed=embed)
    await member.send('Для заполнения заявки просто ответь мне тут в свободном формате')
    role = discord.utils.get(member.guild.roles, id=861263214468923412)
    await member.add_roles(role)


    print("{} joined to channel! Role: {}".format(member, role.id))


@client.event
async def on_member_remove(member):
    #860463581634887700
    channel = client.get_channel(860463581634887700)
    await channel.send(f"Свалил: {member.mention}| Не помним, не любим, не скорбим ;)")


@client.event
async def on_ready():
    print('Bot logged in as {0.user}'.format(client))

@client.event
async def on_voice_state_update(member, before, after):

    # await createChannel()
    try:
        print('before', before.channel.id)
        if before.channel.id in created_channels:
            print('created channel in array')
            channel = client.get_channel(before.channel.id)
            members = channel.members
            print('members count', len(members))
            if len(members) == 0:
                created_channels.remove(before.channel.id)
                print('created_channels', created_channels)
                await channel.delete()
    except:
        print('not before')
    try:
        print('after', after.channel.id)
        if after.channel.id == 860435297560035338:
            print('create new')
            guild = member.guild
            category = discord.utils.get(guild.categories, name="Голосовые каналы")

            channel = await member.guild.create_voice_channel(f'Группа {member.display_name.upper()}',
                                                              category=category)
            created_channels.append(channel.id)
            print('created_channels', created_channels)
            await member.move_to(channel)
    except:
        print('not after')






client.run(TOKEN)