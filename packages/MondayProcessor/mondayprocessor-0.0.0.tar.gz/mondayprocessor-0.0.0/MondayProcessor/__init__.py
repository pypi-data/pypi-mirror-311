#!/usr/bin/env python
# -*- coding: utf-8 -*-
#author: Xiao Wang 
# x.wang@cloudfmgroup.com
# Created: 05/04/2023

from .DataProcessor import DataProcessor
from monday import MondayClient

class MondayProcessor(DataProcessor):

    from .launchInteractiveProcess import launchInteractiveProcess
    from ._fetchBoardById import _fetchBoardById
    from ._fetchBoardLogsById import _fetchBoardLogsById
    from ._fetchGroups import _fetchGroups
    from ._fetchPrismConf import _fetchPrismConf
    from ._fetchPrismConfByBoard import _fetchPrismConfByBoard
    from ._fetchPrismConfByGroup import _fetchPrismConfByGroup
    from ._fetchColumnValueByGroup import _fetchColumnValueByGroup
    from ._searchConfColumnIds import _searchConfColumnIds
    from ._searchColumnIdsByName import _searchColumnIdsByName
    from ._searchConfColumnIdsMatch import _searchConfColumnIdsMatch
    
    def __init__(self, MONDAY_TOKEN) -> None:
        super().__init__()
        self._token = MONDAY_TOKEN
        self.monday = MondayClient(self._token)
    

if __name__ == "__main__":

    mp = MondayProcessor()
    # mp._fetchBoardById(4246692749)
    # mp._fetchPrismConfByGroup(board_id=4246692749, groupId="topics", columns=["ct_type",  "color",  "prism_channel_no_9", "status1" ])
    ConfColumnIds = mp._searchConfColumnIds(4246692749)
    mp._fetchPrismConfByGroup(board_id=4246692749, groupId="topics", columns=ConfColumnIds)
    # mp._fetchGroups(4246692749)
    # mp._fetchPrismConf(4246692749)
    # df = mp.launchInteractiveProcess(4246692749)
    # print(df)
