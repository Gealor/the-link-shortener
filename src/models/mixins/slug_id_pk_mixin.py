from sqlalchemy.orm import Mapped
from sqlalchemy.orm import mapped_column


class SlugIdPrimaryKeyMixin:
    slug: Mapped[str] = mapped_column(primary_key=True)
