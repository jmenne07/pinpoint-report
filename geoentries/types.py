from typing import TYPE_CHECKING, Protocol

from django.contrib.auth.models import Group
from django.http.request import HttpRequest

if TYPE_CHECKING:
    from django.http.request import HttpRequest

    class UserLike(Protocol):
        is_superuser: bool
        groups: "Group"

    class AdminRequest(HttpRequest):
        user: UserLike
