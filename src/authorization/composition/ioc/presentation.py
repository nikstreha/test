from dishka import Provider, Scope, provide

from authorization.composition.configuration.settings import Settings
from authorization.presentation.http.middleware.rate_limit import LoginRateLimiter


class PresentationProvider(Provider):
    scope = Scope.APP

    @provide
    def get_login_rate_limiter(self, s: Settings) -> LoginRateLimiter:
        return LoginRateLimiter(
            max_attempts=s.RATE_LIMIT_LOGIN_MAX_ATTEMPTS,
            window_seconds=s.RATE_LIMIT_LOGIN_WINDOW_SECONDS,
        )
