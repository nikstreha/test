from typing import NewType

from sqlalchemy.ext.asyncio import AsyncSession

ReaderSession = NewType("ReaderSession", AsyncSession)
WriterSession = NewType("WriterSession", AsyncSession)
