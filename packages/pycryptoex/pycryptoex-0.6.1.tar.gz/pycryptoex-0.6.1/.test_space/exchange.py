from __future__ import annotations

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from typing import Any, Optional


# Пример реализации интерфейса между http и websocket


class BaseExchange:
    async def request(
        self,
        path: str,
        signed: bool = False,
        params: Optional[dict[str, Any]] = None,
        headers: Optional[dict[str, Any]] = None,
        method: str = "GET",
        **request_kwargs: Any
    ) -> Any:
        if method in ("GET", "DELETE"):
            return await self._request(
                path=path,
                signed=signed,
                params=params,
                headers=headers,
                method=method
            )
        else:
            return await self._request(
                path=path,
                signed=signed,
                data=params,
                headers=headers,
                method=method
            )

    async def _request(
        self,
        path: str,
        signed: bool = False,
        params: Optional[dict[str, Any]] = None,
        data: Optional[dict[str, Any]] = None,
        headers: Optional[dict[str, Any]] = None,
        method: str = "GET",
        **request_kwargs: Any
    ) -> Any:
        ...
