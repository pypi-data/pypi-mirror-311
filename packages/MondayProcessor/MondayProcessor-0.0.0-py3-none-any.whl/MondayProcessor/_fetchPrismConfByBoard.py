
from typing import List
import requests

from .MondayProcessorExceptions_ import (
    MondayProcessorBoardNotFound,
    MondayProcessorNoColumInBoard,
    MondayProcessorNoItemInGroup
)


def _fetchPrismConfByBoard(self, board_id:int, columns:List[str]):
        
    column_ids = []
    
    for column_name in columns:
        for column_id in self._searchColumnIdsByName(board_id, column_name=column_name):
            column_ids.append(column_id)
    
    columns_str = '["' + '","'.join(column_ids) + '"]'
    columns_index = ["ct", "phase", "channel", "sn", "powerSupplyPhase"]
    columnsDict = dict(zip(columns,columns_index))
    headers = {"Authorization": self._token}
    data = {"query": f'''query {{
        boards (ids:{board_id}){{
            id
            name
            groups(){{
                id
                title
                items_page(limit:500) {{
                    cursor
                    items{{
                        id
                        name
                        column_values(ids:{columns_str}){{
                            column{{title}}
                            text
                        }}
                }}
                }}
                
            }}
        }}
    }}'''}
    r = requests.post('https://api.monday.com/v2', headers=headers, data=data)
    data = r.json()
    print(data)
    boards = data['data']['boards']
    if(len(boards) <1):
        raise MondayProcessorBoardNotFound(f"Monday board id ({board_id}) not found when perform MondayProcessor._searchConfColumnIds")
    groups = boards[0]['groups']
    if(len(groups) < 1):
        raise MondayProcessorNoColumInBoard(f"No column in board {board_id}")
    
    ret = []
    for group in groups:
        groupId = group['id']
        items = group['items_page']['items']
        if(len(items) < 1):
            raise MondayProcessorNoItemInGroup(f"No column in board {board_id}, group {groupId}")

        for item in items:
            print('item:', item)
            tmpDict = {}
            if 'Name' in columns:
                tmpDict['Name'] = item['name']
            tmpDict['building_name'] = group["title"]
            for v in item["column_values"]:
                tmpDict[v["column"]["title"]] = v["text"]
#                 key = v["id"]
#                 ai = v["additional_info"]
#                 tmpDict[key]= None if ai== None else json.loads(ai)["label"]
#             try:
#                 ch = tmpDict["channel"]
#                 chN = int(ch)
#                 tmpDict["channel"] = chN
#             except:
#                 tmpDict["channel"] = None
            ret.append(tmpDict)
    return ret