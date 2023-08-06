from botty import dp, bot, Message, reply, bot


@dp.command("test")
async def _(msg: Message):
    print(bot.url)
    print(bot.start_url)
    print(bot.startgroup_url)
    await reply(msg, "test1")


@dp.command("test").state().has_reply
def _(msg: Message):
    return reply(msg, "test*")


@dp.sticker()
async def _(msg: Message):
    r = await bot.get_sticker_set(msg.sticker.set_name)
    await bot.create_new_sticker_set(
        user_id=msg.from_user.id,
        name="chloya",
        title="Хлоя @anime4_arts",
    )
    print(r)


dp.run()
