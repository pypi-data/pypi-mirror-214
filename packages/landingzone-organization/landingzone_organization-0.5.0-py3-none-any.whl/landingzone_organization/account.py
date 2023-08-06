from __future__ import annotations

from dataclasses import dataclass
from typing import Optional

from landingzone_organization.filtering import resolve_account_environment


@dataclass
class Account:
    """
    Understands AWS Accounts
    """

    name: str
    account_id: str

    @property
    def environment(self) -> Optional[str]:
        return resolve_account_environment(self.name)
