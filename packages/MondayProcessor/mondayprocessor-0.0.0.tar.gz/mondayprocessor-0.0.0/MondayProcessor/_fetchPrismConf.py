from typing import List

def _fetchPrismConf(self, board_id:int)->List[dict]:
    confColumnIds = self._searchConfColumnIds(board_id=board_id)
    groupIds = self._fetchGroups(board_id=board_id)
    ret = []
    for gId in groupIds:
        items = self._fetchPrismConfByGroup(board_id=board_id, groupId=gId, columns=confColumnIds)
        ret.extend(items)
    return ret