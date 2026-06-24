from aiohttp import web
import os

async def handle(request):
    return web.Response(text="Bot is running")

app = web.Application()
app.add_routes([web.get('/', handle)])

if __name__ == '__main__':
    web.run_app(app, port=int(os.environ.get("PORT", 8080)))
