"""Module for the decorator."""
import time
from typing import Any, Callable, Optional, TypeVar

from t_pom_dentaquest import logger
from t_pom_dentaquest.exceptions import SessionExpiredException

F = TypeVar("F", bound=Callable[..., Any])


def relogin_and_retry_if_error(retries: int = 3) -> Callable[[F], F]:
    """Decorator to relogin and retry the function if a Web-related error occurs."""

    def decorator(func: F) -> F:
        def wrapper(self: Any, *args: Any, **kwargs: Any) -> Any:
            tries = 0
            exception: Optional[BaseException] = None
            while tries < retries:
                try:
                    result = func(self, *args, **kwargs)
                    return result  # Return result immediately if successful
                except SessionExpiredException as e:
                    tries += 1
                    logger.warning(f"Failed to process due to error: {str(e)}. Retry = {tries}")
                    exception = e
                    time.sleep(90)
            if exception is not None:
                raise exception

        return wrapper  # type: ignore

    return decorator
