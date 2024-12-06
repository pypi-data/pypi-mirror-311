"""
Hook Types.

Hook Types are triggers that can be executed when an event is triggered.

1. FSWatchdog: Watches a specified directory for changes.
"""
from .fs import FSWatchdog
from .web import WebHook
from .imap import IMAPWatchdog
from .tagged import TaggedIMAPWatchdog
from .ssh import SFTPWatchdog
# from .upload import UploadHook
