from .abstract import AbstractAction


class Dummy(AbstractAction):
    """Dummy.

    Simply Print the Action object.
    """

    async def open(self):
        print('Opening Action on Dummy.')

    async def run(self, *args, **kwargs):
        print(
            f"Running action from hook {self._hook_} with arguments:",
            args,
            self._args,
            kwargs,
            self._kwargs
        )

    async def close(self):
        print("Closing Action on Dummy.")
