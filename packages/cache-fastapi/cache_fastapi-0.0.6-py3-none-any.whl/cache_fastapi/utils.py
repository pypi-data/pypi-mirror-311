from functools import wraps

from fastapi import Request


def cache_endpoint(max_age=60):
    def decorator(func):
        @wraps(func)
        async def wrapper(*args, **kwargs):
            # Ensure the request is part of kwargs
            request: Request = kwargs.get('request')
            if request:
                print("From decorator", request)
            return await func(*args, **kwargs)

        return wrapper

    return decorator
