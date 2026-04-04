from typing import Literal

from fastapi import Response


class CookieProvider:
    def __init__(
        self,
        key: str,
        max_age: int,
        path: str = "/",
        secure: bool = True,
        httponly: bool = True,
        samesite: Literal["lax", "strict", "none"] = "lax",
    ) -> None:
        self._key = key
        self._max_age = max_age
        self._path = path
        self._secure = secure
        self._httponly = httponly
        self._samesite = samesite

    def set(self, response: Response, value: str) -> None:
        response.set_cookie(
            key=self._key,
            value=value,
            max_age=self._max_age,
            path=self._path,
            httponly=self._httponly,
            samesite=self._samesite,
            secure=self._secure,
        )

    def delete(self, response: Response) -> None:
        response.delete_cookie(key=self._key, path=self._path)


class RefreshTokenCookieProvider(CookieProvider): ...
