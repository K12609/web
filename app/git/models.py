

# -*- coding: utf-8 -*-
"""Define models.

Copyright (C) 2021 Gitcoin Core

This program is free software: you can redistribute it and/or modify
it under the terms of the GNU Affero General Public License as published
by the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
GNU Affero General Public License for more details.

You should have received a copy of the GNU Affero General Public License
along with this program. If not, see <http://www.gnu.org/licenses/>.

"""
import logging

from django.db import models

from economy.models import SuperModel

logger = logging.getLogger(__name__)


class GitCache(SuperModel):
    """Model used for storing serialized pygithub objects.

    Attributes:
        handle (str): The unique (within a category) handle for the data
        category (str): the category of the data (user, repo, ...).
        data (binary): The serialized object data.

    """

    class Category:
        USER = "user"
        REPO = "repo"

    CATEGORY_CHOICES = [
        (Category.USER, 'User'),
        (Category.REPO, 'Repository'),
    ]

    handle = models.CharField(max_length=200, null=False, blank=True)
    category = models.CharField(max_length=20, null=False, blank=True, choices=CATEGORY_CHOICES)
    data = models.BinaryField()

    class Meta:
        unique_together = ["handle", "category"]

    def __str__(self):
        """Return the string representation of a model."""
        return f"[{self.category}] {self.handle}"

    @classmethod
    def get_user(self, handle):
        """Utility function to retreive a user object"""
        try:
            return self.objects.get(category=GitCache.Category.USER, handle=handle)
        except self.DoesNotExist:
            raise

    def update_data(self, data):
        """Update the data field if it has changed."""
        if self.data != data:
            self.data = data
            self.save()
