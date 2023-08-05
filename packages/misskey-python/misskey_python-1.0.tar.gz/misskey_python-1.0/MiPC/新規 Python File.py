from MiPC import StreamingClient

class Stream(StreamingClient):

    async def on_ready(self):
        print("起動完了")
        #await client.connect("homeTimeline")
        await mibot.connect("globalTimeline")

    async def on_note(self, ctx):
        print("-----------------------------------------------")
        print(ctx.raw)
        print("-----------------------------------------------")

mibot = Stream("misskey.io", "9P9GpLCr6IHqJKxOzT51EcomBnLaZju0")
mibot.run()