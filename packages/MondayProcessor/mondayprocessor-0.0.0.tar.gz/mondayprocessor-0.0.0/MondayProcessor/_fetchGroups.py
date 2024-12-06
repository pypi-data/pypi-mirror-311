from typing import List

from .MondayProcessorExceptions_ import (
    MondayProcessorBoardNotFound,
    MondayProcessorNoColumInBoard
)

def _fetchGroups(self, board_id:int) -> List[str]:
    data = self.monday.groups.get_groups_by_board(board_ids=board_id)
    boards = data['data']['boards']
    if(len(boards) <1):
        raise MondayProcessorBoardNotFound(f"Monday board id ({board_id}) not found when perform MondayProcessor._searchConfColumnIds")
    groups = boards[0]['groups']
    if(len(groups) < 1):
        raise MondayProcessorNoColumInBoard(f"No column in board {board_id}")
    ret = {x["id"]:x["title"] for x in groups}
#         print(groups)
    # print(ret)
    return ret