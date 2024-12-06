"""
Hook Actions.

Actions are the Components called by a Hook Definition.
"""

from .abstract import AbstractAction
from .dummy import Dummy
from .jira import JiraTicket
from .zammad import Zammad

__all__ = (
    "AbstractAction",
    "Dummy",
    "JiraTicket",
    "Zammad",
)
