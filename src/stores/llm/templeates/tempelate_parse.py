import os


class TempelateParser:
    def __init__(self, language: str = None, default_lang='en'):
        self.current_path = os.path.dirname(os.path.abspath(__file__))
        self.default_language = default_lang
        self.language = None
        self.set_lang(language)

    def set_lang(self, language):

        if not language:
            return None
        language_path = os.path.join(self.current_path, "locales", language)
        if language and os.path.exists(language_path):
            self.language = language
        else:
            self.language = self.default_language

    def get(self, group, key, vars):
        if not group or not key:
            return None
        group_path = os.path.join(
            self.current_path, "locales", self.language, f"{group}.py")
        target_lang = self.language
        if not os.path.exists(group_path):
            group_path = os.path.join(
                self.current_path, "locales", self.default_language, f"{group}.py")
            target_lang = self.default_language

        if not os.path.exists(group_path):
            return None

        module = __import__(
            f"stores.llm.tempelates.locales.{target_lang}.{group}", fromlist=[group])

        if not module:
            return None
        key_attr = getattr(module, key)

        return key_attr.substitute(vars)
