from sqlalchemy.orm import Mapped
from sqlalchemy.orm import mapped_column

from src.models.base import Base
from src.models.mixins.id_pk_mixin import IdPrimaryKeyMixin
from src.models.mixins.updated_at_mixin import UpdatedAtMixin


class User(Base, IdPrimaryKeyMixin, UpdatedAtMixin):
    __tablename__ = "users"

    nickname: Mapped[str] = mapped_column(nullable=False, unique=True)
    password: Mapped[str] = mapped_column(nullable=False)  # тут хранится хэш пароля

    is_active: Mapped[bool] = mapped_column(default=True, nullable=False)
