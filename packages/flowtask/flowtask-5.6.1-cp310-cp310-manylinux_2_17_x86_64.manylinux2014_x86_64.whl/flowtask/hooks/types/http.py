from navigator.views import BaseHandler
from navigator.libs.json import JSONContent
from navigator.types import WebApp
from .base import BaseHook


class HTTPHook(BaseHook, BaseHandler):
    """HTTPHook.

    Base Hook for all HTTP-based hooks.

    """
    methods: list = ["GET", "POST"]
    default_status: int = 202

    def __init__(self, *args, **kwargs):
        self.method: str = kwargs.pop('method', None)
        if self.method:
            self.methods = [self.method]
        super(HTTPHook, self).__init__(*args, **kwargs)
        self._base_url = kwargs.get('base_url', '/api/v1/webhook/')
        self.url = f"{self._base_url}{self.trigger_id}"
        self._json = JSONContent()

    async def start(self):
        pass

    async def stop(self):
        pass

    def setup(self, app: WebApp) -> None:
        super().setup(app)
        self.logger.notice(
            f"Set the unique URL Trigger to: {self.url}"
        )
        for method in self.methods:
            cls = getattr(self, method.lower())
            if cls:
                self.app.router.add_route(
                    method,
                    self.url,
                    cls
                )
