from typing import List, Union

def _searchConfColumnIdsMatch(self, columns, includeList:List[str], excludeList:List[str] = [])-> Union[str,None]:
    for c in columns:
        title:str = c["title"]
        id = c["id"]
        flag = True
        for item in includeList:
            if item.lower() not in title.lower():
                flag = False
                break
        if(not flag): continue
        flag = True
        for item in excludeList:
            if item.lower() in title.lower():
                flag = False
                break
        if(not flag): continue
        return id
    return None