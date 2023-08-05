# -*- coding: utf-8 -*-
#
# This file is part of Invenio.
# Copyright (C) 2015-2023 CERN.
#
# Invenio is free software; you can redistribute it and/or modify it
# under the terms of the MIT License; see LICENSE file for more details.

"""Advanced usage docs."""

from .ext import InvenioOAuthClient, InvenioOAuthClientREST
from .proxies import current_oauthclient

__version__ = "3.0.0"

__all__ = (
    "__version__",
    "current_oauthclient",
    "InvenioOAuthClient",
    "InvenioOAuthClientREST",
)
