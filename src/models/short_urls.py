from sqlalchemy.orm import Mapped
from sqlalchemy.orm import mapped_column

from models.base import Base
from models.mixins.slug_id_pk_mixin import SlugIdPrimaryKeyMixin


class ShortURL(Base, SlugIdPrimaryKeyMixin):
    __tablename__ = "short_urls"

    full_url: Mapped[str] = mapped_column(unique=True, nullable=False)

