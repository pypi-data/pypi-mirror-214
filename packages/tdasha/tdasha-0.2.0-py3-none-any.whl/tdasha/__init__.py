#!/usr/bin/env python
# -*- coding: utf-8 -*-
# flake8: noqa

__all__ = [
    "io",
    "compute",
]

from . import io
from . import compute
from pkg_resources import get_distribution

__version__ = get_distribution("tdasha").version
