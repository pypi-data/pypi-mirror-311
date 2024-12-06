#!/usr/bin/env python
# -*- coding: utf-8 -*-
#author: Xiao Wang 
# x.wang@cloudfmgroup.com
# Created: 05/04/2023

from abc import ABC

class DataProcessor(ABC):

    from .launchInteractiveProcess import launchInteractiveProcess

    def __init__(self) -> None:
        super().__init__()