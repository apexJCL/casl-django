from django.conf import LazySettings

_settings = LazySettings()


class Config:
    SUBJECT_MAX_LENGTH = 128
    ACTION_MAX_LENGTH = 128
    USER_MODEL = None

    def __init__(self, subject_length: int = None, action_length: int = None, user_model: str = None) -> None:
        super().__init__()
        assert (user_model is not None), "Expected user model reference, got None"
        self.USER_MODEL = user_model
        if subject_length:
            self.SUBJECT_MAX_LENGTH = subject_length
        if action_length:
            self.ACTION_MAX_LENGTH = action_length


_casl_config = {} if not hasattr(_settings, 'CASL_DJANGO') else _settings.CASL_DJANGO
config = Config(subject_length=_casl_config.get('subject_length', None),
                action_length=_casl_config.get('action_length', None),
                user_model=_settings.AUTH_USER_MODEL)
