from aiohttp import web


async def redirect_to_index(request):
    raise web.HTTPFound('/index.html')
