from typing import List

from .MondayProcessorExceptions_ import (
    MondayProcessorBoardNotFound,
    MondayProcessorNoColumInBoard,
    MondayProcessorBoardColumnNotMatch
)

def _searchConfColumnIds(self, board_id:int) -> List[str]:
    data = self.monday.boards.fetch_columns_by_board_id(board_ids=board_id)
    boards = data['data']['boards']
    if(len(boards) <1):
        raise MondayProcessorBoardNotFound(f"Monday board id ({board_id}) not found when perform MondayProcessor._searchConfColumnIds")
    columns = boards[0]['columns']
    if(len(columns) < 1):
        raise MondayProcessorNoColumInBoard(f"No column in board {board_id}")
    #  = boards[0][groups]
    ctColumnId = self._searchConfColumnIdsMatch(columns=columns,includeList=["ct","type"])
    if (ctColumnId == None): raise MondayProcessorBoardColumnNotMatch("cannot find CT type column")
    phaseColumnId = self._searchConfColumnIdsMatch(columns=columns,includeList=["L1","L2","L3"], excludeList=["supply"])
    if (phaseColumnId == None): raise MondayProcessorBoardColumnNotMatch("cannot find circuit phase column")
    channelColumnId = self._searchConfColumnIdsMatch(columns=columns,includeList=["channel","no"])
    if (channelColumnId == None): raise MondayProcessorBoardColumnNotMatch("cannot find PRISM channel column")
    snColumnId = self._searchConfColumnIdsMatch(columns=columns,includeList=["ID","PRISM"])
    if (snColumnId == None): raise MondayProcessorBoardColumnNotMatch("cannot find PRISM SN column")
    powerSupplyPhaseColumnId = self._searchConfColumnIdsMatch(columns=columns,includeList=["PRISM","supply","phase"])
    if (powerSupplyPhaseColumnId == None): raise MondayProcessorBoardColumnNotMatch("cannot find PRISM power supply phase column")

    ret = [ctColumnId, phaseColumnId, channelColumnId, snColumnId, powerSupplyPhaseColumnId]
    return ret