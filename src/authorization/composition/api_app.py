from contextlib import asynccontextmanager

from dishka import AsyncContainer, Provider, make_async_container
from dishka.integrations.fastapi import FastapiProvider, setup_dishka
from fastapi import FastAPI

from authorization.composition.configuration.settings import Settings
from authorization.composition.ioc.provider_registry import get_provider
from authorization.infrastructure.persistence.sqla.mapper.all import map_table
from authorization.presentation.http.api_router import api_router
from authorization.presentation.http.exception_handler import setup_exception_handlers


def create_ioc_container(
    configuration: Settings,
    *di_providers: Provider,
) -> AsyncContainer:
    return make_async_container(
        *get_provider(),
        *di_providers,
        FastapiProvider(),
        context={Settings: configuration},
    )


def create_api_app(container: AsyncContainer) -> FastAPI:
    @asynccontextmanager
    async def lifespan(app: FastAPI):
        map_table()
        yield
        if hasattr(app.state, "dishka_container"):
            await app.state.dishka_container.close()

    app = FastAPI(debug=True, lifespan=lifespan)
    setup_exception_handlers(app)
    app.include_router(api_router)
    setup_dishka(container, app)

    return app


def build_api_app() -> FastAPI:
    configuration = Settings()  # type: ignore
    container = create_ioc_container(configuration)
    return create_api_app(container)
