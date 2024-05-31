from typing import Annotated

from sqlalchemy import String
from sqlalchemy.orm import mapped_column


pk = Annotated[int, mapped_column(primary_key=True)]
custom_string = Annotated[str, mapped_column(String(30))]
