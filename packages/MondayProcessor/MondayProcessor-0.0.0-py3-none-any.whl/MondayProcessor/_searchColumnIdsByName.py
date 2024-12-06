from typing import List

from .MondayProcessorExceptions_ import (
    MondayProcessorBoardNotFound,
    MondayProcessorNoColumInBoard,
    MondayProcessorBoardColumnNotMatch
)

def _searchColumnIdsByName(self, board_id:int, column_name:str) -> List[str]:
    data = self.monday.boards.fetch_columns_by_board_id(board_ids=board_id)
    boards = data['data']['boards']
    if(len(boards) <1):
        raise MondayProcessorBoardNotFound(f"Monday board id ({board_id}) not found when perform MondayProcessor._searchConfColumnIds")
    columns = boards[0]['columns']
    if(len(columns) < 1):
        raise MondayProcessorNoColumInBoard(f"No column in board {board_id}")
    #  = boards[0][groups]
    # print("columns: ", columns)
    ColumnId = self._searchConfColumnIdsMatch(columns=columns,includeList=[column_name])
    if (ColumnId == None): raise MondayProcessorBoardColumnNotMatch("cannot find a column with this name")

    ret = [ColumnId]
    return ret