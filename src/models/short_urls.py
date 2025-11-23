from sqlalchemy.orm import Mapped, mapped_column


from models.mixins.slug_id_pk_mixin import SlugIdPrimaryKeyMixin
from models.base import Base


class ShortURL(Base, SlugIdPrimaryKeyMixin):
    __tablename__ = "short_urls"

    full_url: Mapped[str] = mapped_column(nullable=False)

