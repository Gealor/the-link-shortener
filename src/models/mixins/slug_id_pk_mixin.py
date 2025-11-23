from sqlalchemy.orm import Mapped, mapped_column


class SlugIdPrimaryKeyMixin:
    slug: Mapped[str] = mapped_column(primary_key=True)