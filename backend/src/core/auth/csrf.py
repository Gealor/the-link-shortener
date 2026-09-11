from typing import Annotated

from fastapi import Depends
from fastapi_csrf_protect import CsrfProtect

from src.core.config import settings

CSRF_Secure = Annotated[CsrfProtect, Depends()]

@CsrfProtect.load_config
def get_csrf_config():
  return settings.csrf
