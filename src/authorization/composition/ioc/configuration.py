from dishka import Provider, Scope, from_context

from authorization.composition.configuration.settings import Settings


class ConfigurationProvider(Provider):
    scope = Scope.APP

    configuration = from_context(provides=Settings)
