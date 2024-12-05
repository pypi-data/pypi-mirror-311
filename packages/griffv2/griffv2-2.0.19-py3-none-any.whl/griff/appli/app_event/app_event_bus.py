from injector import inject

from griff.appli.app_event.app_event import AppEvent
from griff.appli.app_event.app_event_dispatcher import AppEventDispatcher
from griff.appli.message.message_bus import MessageBus
from griff.appli.app_event.app_event_handler import AppEventHandler


class AppEventBus(MessageBus[AppEvent, None, AppEventHandler]):
    @inject
    def __init__(self, dispatcher: AppEventDispatcher) -> None:
        super().__init__(dispatcher)  # pragma: no cover
