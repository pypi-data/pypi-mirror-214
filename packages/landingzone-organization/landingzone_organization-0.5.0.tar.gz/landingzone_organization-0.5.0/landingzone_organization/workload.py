from __future__ import annotations
import re
from typing import List, Optional, Set

from landingzone_organization.account import Account


class Workload:
    def __init__(self, name: str, accounts: List[Account]) -> None:
        self.__name = name
        self.__accounts = accounts

    @property
    def name(self) -> str:
        return self.__name

    @property
    def accounts(self) -> List[Account]:
        return self.__accounts

    @property
    def environments(self) -> Set[str]:
        return set(map(lambda account: str(account.environment), self.accounts))

    def by_environment(self, name: str) -> Optional[Account]:
        def match(account: Account):
            return account.environment == name

        return next(filter(match, self.accounts), None)  # type: ignore

    def append(self, account: Account) -> None:
        self.__accounts.append(account)
