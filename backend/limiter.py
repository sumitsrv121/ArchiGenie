from slowapi import Limiter
from slowapi.util import get_remote_address

# Create a single limiter instance to be shared.
limiter = Limiter(key_func=get_remote_address)
