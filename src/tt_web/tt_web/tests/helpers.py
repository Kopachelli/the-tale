
import asyncio

from aiohttp import web
from aiohttp import test_utils

from tt_protocol.protocol import base_pb2

from .. import log


class BaseTests(test_utils.AioHTTPTestCase):

    def setUp(self):
        super().setUp()
        asyncio.set_event_loop(self.loop)


    def get_app(self, loop):
        application = self.create_application()

        application.on_startup.append(self.clean_environment)
        application.on_cleanup.insert(0, self.clean_environment)

        return application


    async def check_answer(self, request, Data=None, api_status=base_pb2.ApiResponse.SUCCESS, error=None):
        self.assertEqual(request.status, 200)
        content = await request.content.read()
        response = base_pb2.ApiResponse.FromString(content)
        self.assertEqual(response.status, api_status)

        if error is not None:
            self.assertEqual(response.error.code, error)

        if Data is None:
            return None

        response_data = Data()
        response.data.Unpack(response_data)

        await request.release()

        return response_data

    async def check_success(self, request, Data=None):
        result = await self.check_answer(request, Data=Data, api_status=base_pb2.ApiResponse.SUCCESS)
        return result

    async def check_error(self, request, error):
        await self.check_answer(request, api_status=base_pb2.ApiResponse.ERROR, error=error)

    async def clean_environment(self, app=None):
        pass

    def create_application(self):
        app = web.Application(loop=self.loop)

        app['config'] = {}

        log.initilize({'level': 'critical'})

        return app
