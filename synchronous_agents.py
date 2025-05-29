from uagents import Agent, Bureau, Context, Model


class Message(Model):
    message: str


alice = Agent(name="alice", seed="alice seed phrase", port=8001)
bob = Agent(name="bob", seed="bob seed phrase", port=8002)
clyde = Agent(name="clyde", seed="clyde seed phrase", port=8003)


@alice.on_interval(period=5.0)
async def send_message(ctx: Context):
    msg = Message(message="Hey Bob, how's Clyde?")
    ctx.logger.info(f"Alice is sending a message to Bob: {msg.message}")
    reply, status = await ctx.send_and_receive(bob.address, msg, response_type=Message)
    if isinstance(reply, Message):
        ctx.logger.info(f"Received awaited response from Bob: {reply.message}")
    else:
        ctx.logger.info(f"Failed to receive response from Bob: {status}")


@bob.on_message(model=Message)
async def handle_message_and_reply(ctx: Context, sender: str, msg: Message):
    ctx.logger.info(f"Bob received message from {sender}: {msg.message}")
    new_msg = Message(message="How are you, Clyde?")
    ctx.logger.info(f"Bob is sending a message to Clyde: {new_msg.message}")
    reply, status = await ctx.send_and_receive(
        clyde.address, new_msg, response_type=Message
    )
    if isinstance(reply, Message):
        ctx.logger.info(f"Bob received awaited response from Clyde: {reply.message}")
        await ctx.send(sender, Message(message="Clyde is doing alright!"))
    else:
        ctx.logger.info(f"Bob failed to receive response from Clyde: {status}")


@clyde.on_message(model=Message)
async def handle_message(ctx: Context, sender: str, msg: Message):
    ctx.logger.info(f"Clyde received message from {sender}: {msg.message}")
    ctx.logger.info("Clyde is responding")
    await ctx.send(sender, Message(message="I'm doing alright!"))


bureau = Bureau(agents=[alice, bob, clyde], port=8000)

if __name__ == "__main__":
    print("Starting synchronous communication demonstration")
    print("Press Ctrl+C to exit")
    print("-" * 50)
    bureau.run() 