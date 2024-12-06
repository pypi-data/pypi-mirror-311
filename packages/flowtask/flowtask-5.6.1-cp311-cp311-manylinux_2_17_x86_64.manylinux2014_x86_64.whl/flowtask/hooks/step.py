from typing import Union
from collections.abc import Callable, Awaitable
import importlib
from navconfig.logging import logging
from ..exceptions import ConfigError, FlowTaskError
from .actions.abstract import AbstractAction


def import_component(component: str, classpath: str, package: str = "components"):
    module = importlib.import_module(classpath, package=package)
    obj = getattr(module, component)
    return obj


class StepAction:
    def __init__(self, action: str, params: dict) -> None:
        self.name = action
        self._step: Union[Callable, Awaitable] = None
        try:
            self._action: AbstractAction = import_component(
                action,
                "flowtask.hooks.actions",
                "actions"
            )
        except (ImportError, RuntimeError) as exc:
            raise FlowTaskError(f"Unable to load Action {action}: {exc}") from exc
        self.params = params

    def __repr__(self) -> str:
        return f"<StepAction.{self.name}: {self.params!r}>"

    @property
    def component(self):
        return self._action

    async def run(self, hook, *args, **kwargs):
        """Run action involved"""
        try:
            self._step = self._action(hook, **self.params)
            try:
                async with self._step as step:
                    result = await step.run(*args, **kwargs)
                return result
            except Exception as exc:
                logging.error(f"Error running action {self._action!s}: {exc}")
        except Exception as exc:
            logging.error(f"Unable to load Action {self._action}: {exc}")
            raise
