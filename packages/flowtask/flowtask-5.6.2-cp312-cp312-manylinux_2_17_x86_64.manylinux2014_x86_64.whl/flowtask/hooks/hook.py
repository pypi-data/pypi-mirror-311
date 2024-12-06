from functools import partial
from uuid import uuid4
from navconfig.logging import logger
from ..exceptions import ConfigError
from .step import StepAction, import_component


class Hook:
    """Hook.

    Compile a Hook (Triggers and Actions) and got every step on the hook.
    """

    def __init__(self, hook: dict):
        self.triggers: list = []
        self._id = hook.pop("id", uuid4())
        self.name = hook.pop("name")
        try:
            triggers = hook["When"]
        except KeyError as exc:
            raise ConfigError(
                "Hook Error: Unable to find Trigger: *When* parameter"
            ) from exc
        try:
            actions = hook["Then"]
        except KeyError as exc:
            raise ConfigError(
                "Hook Error: Unable to get list of Actions: *Then* parameter"
            ) from exc
        ## build Hook Component:
        self.build(triggers, actions)
        logger.debug(
            f":: Loading Hook {self.name}"
        )

    def build(self, triggers: list, actions: list):
        self._actions: list = []
        # Then: Load Actions
        for step in actions:
            for step_name, params in step.items():
                action = StepAction(step_name, params)
                self._actions.append(action)
        for step in triggers:
            for step_name, params in step.items():
                trigger = import_component(step_name, "flowtask.hooks.types", "types")
                # start trigger:
                args = {"name": self.name, "actions": self._actions}
                args = {**args, **params}
                hook = partial(trigger, **args)
                self.triggers.append(hook)
