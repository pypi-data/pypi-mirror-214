from CharmCord.CharmErrorHandling import CharmErrorHandling
Errors = CharmErrorHandling()
async def username(user):
    from CharmCord.Functions.AoiCore import bots
    try:
        int(user)
        new_user = await bots.fetch_user(user)
    except ValueError:
        Errors.Errors(1, user)
    return new_user


async def authorName(emp):
    from CharmCord.Functions.AoiCore import Context
    return Context.author.name


async def authorID(emp):
    from CharmCord.Functions.AoiCore import Context
    return Context.author.id


async def send(args: str):
    from CharmCord.Functions.AoiCore import bots
    split = args.split(";")
    channel_id = split[0]
    message = split[1]
    channel = await bots.fetch_channel(int(channel_id))
    await channel.send(message)
    return


async def pyeval(code):
    answer = eval(code)
    return answer
