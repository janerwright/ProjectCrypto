from pyfiglet import figlet_format
import ProjectCrypto.python.mongoDB.Mongo_Interaction_Connect_Query as mongolib
from aiohttp import web
import os.path
import os


async def handler_file(request):
    request_type = ((request.path).split("."))[-1]

    if 'png' == request_type:
        filepath = os.path.join(os.path.dirname(__file__), '../..', 'img', os.path.basename(request.path))
        return web.Response(body=open(filepath, "rb").read(), content_type="image/png")

    else:
        try:
            container_file = request_type
            if request_type == "html":
                container_file = "pages"

            filepath = os.path.join(os.path.dirname(__file__), '../..', container_file, os.path.basename(request.path))
            return web.Response(body=open(filepath, "r").read(), content_type=f"{request_type}")
        except:
            print(f"file : {request.path} not found")
            if request_type == "html":
                filepath = os.path.join(os.path.dirname(__file__), '../..', 'pages', "contact.html")
                return web.Response(body=open(filepath, "r").read(), content_type="text/html")




    print(f'GOT request for {request.path}')
    return web.Response()


def main():
    upload_files()
    # print(figlet_format('DeCryptMe', font='starwars'))
    # app = web.Application()
    #
    # app.router.add_route('GET', '/{tail:.*}', handler_file)
    #
    # web.run_app(app)

main()