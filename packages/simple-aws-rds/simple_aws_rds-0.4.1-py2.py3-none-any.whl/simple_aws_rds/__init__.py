# -*- coding: utf-8 -*-

from ._version import __version__

__short_description__ = "Simple AWS RDS dev tools."
__license__ = "MIT"
__author__ = "Sanhe Hu"
__author_email__ = "husanhe@gmail.com"
__github_username__ = "MacHu-GWU"

try:
    from .api import (
        RDSDBInstanceStatusEnum,
        RDSDBInstance,
        RDSDBInstanceIterProxy,
    )
except ImportError as e:  # pragma: no cover
    pass
