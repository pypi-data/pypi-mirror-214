#!/usr/bin/env python3

# SPDX-FileCopyrightText: © 2022-2023 Decompollaborate
# SPDX-License-Identifier: MIT

from __future__ import annotations

__version_info__ = (1, 14, 3)
__version__ = ".".join(map(str, __version_info__))
__author__ = "Decompollaborate"

from . import common
from . import elf32
from . import mips

# Front-end scripts
from . import frontendCommon
from . import disasmdis
from . import rspDisasm
from . import elfObjDisasm
from . import singleFileDisasm
