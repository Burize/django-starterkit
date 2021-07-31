from dataclasses import dataclass
from uuid import UUID


@dataclass
class AccountDTO:
    id: UUID
    email: str
