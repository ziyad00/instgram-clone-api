from django.apps import AppConfig


class AccountConfig(AppConfig):
    name = 'account'
    def ready(self):
        import accounts.signals