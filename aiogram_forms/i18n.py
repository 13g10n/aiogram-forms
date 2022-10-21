"""
Library translation helpers
"""
from pathlib import Path

from aiogram import Dispatcher
from aiogram.contrib.middlewares.i18n import I18nMiddleware

from aiogram_forms.const import I18N_DOMAIN, LOCALES_DIR

BASE_DIR = Path(__file__).parent.parent


class FormsI18nMiddleware(I18nMiddleware):
    """
    Custom forms i18n middleware.
    """
    _registered: bool = False

    def __init__(self):
        super().__init__(I18N_DOMAIN, BASE_DIR / LOCALES_DIR)

    def register(self, dispatcher: Dispatcher) -> None:
        """
        Register i18n middleware

        :param dispatcher: Dispatcher
        """
        if not self._registered:
            dispatcher.setup_middleware(self)
            self._registered = True


i18n = FormsI18nMiddleware()
_ = i18n.lazy_gettext
