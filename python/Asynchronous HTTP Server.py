
from aiohttp import web
import os.path
from ProjectCrypto import *
import codecs


async def handler_file(request):
    if '.html' in request.path:
        filepath = os.path.join(os.path.dirname(__file__), '..', 'pages', os.path.basename(request.path))
        return web.Response(body=open(filepath, "r").read(), content_type="text/html")

    if '.css' in request.path:
        filepath = os.path.join(os.path.dirname(__file__), '..', 'css', os.path.basename(request.path))
        return web.Response(body=open(filepath, "r").read(), content_type="text/css")

    if '.php' in request.path:
        filepath = os.path.join(os.path.dirname(__file__), '..', 'php', os.path.basename(request.path))
        return web.Response(body=open(filepath, "r").read(), content_type="text/php")

    if '.js' in request.path:
        filepath = os.path.join(os.path.dirname(__file__), '..', 'js', os.path.basename(request.path))
        return web.Response(body=open(filepath, "r").read(), content_type="text/js")

    if '.png' in request.path:
        filepath = os.path.join(os.path.dirname(__file__), '..', 'img', os.path.basename(request.path))
        return web.Response(body=open(filepath, "rb").read(), content_type="image/png")

    filepath = os.path.join(os.path.dirname(__file__), '..', 'about', os.path.basename(request.path))
    return web.Response(body=open(filepath, "r").read(), content_type="text/html")

    print(f'GOT request for {request.path}')
    return web.Response()

app = web.Application()

app.router.add_route('GET', '/{tail:.*}', handler_file)

web.run_app(app)