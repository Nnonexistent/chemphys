from django.utils import translation
from django.conf import settings

from django.middleware.locale import LocaleMiddleware


class LocaleMiddlewareEx(LocaleMiddleware):
    LANG_GET_KEY = 'lang'

    def process_request(self, request):
        check_path = self.is_language_prefix_patterns_used()
        language = self.get_lang_from_GET(request) or translation.get_language_from_request(request, check_path=check_path)
        translation.activate(language)
        request.LANGUAGE_CODE = translation.get_language()

    @classmethod
    def get_lang_from_GET(cls, request):
        finded = []
        for lang_code, lang in settings.LANGUAGES:
            if lang_code in request.GET.getlist(cls.LANG_GET_KEY):
                finded.append(lang_code)

        if not finded:
            return

        if len(finded) == 1:
            return finded[0]

        if settings.LANGUAGE_CODE in finded:
            return settings.LANGUAGE_CODE

        # for deterministic result
        finded.sort()
        return finded[0]