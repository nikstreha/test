from collections.abc import Iterable

from dishka import Provider

from authorization.composition.ioc.application import _application_provider
from authorization.composition.ioc.configuration import ConfigurationProvider
from authorization.composition.ioc.domain import DomainProvider
from authorization.composition.ioc.infrastructure import _infrastructure_provider
from authorization.composition.ioc.presentation import PresentationProvider


def get_provider() -> Iterable[Provider]:
    return [
        ConfigurationProvider(),
        DomainProvider(),
        *_infrastructure_provider(),
        *_application_provider(),
        PresentationProvider(),
    ]
