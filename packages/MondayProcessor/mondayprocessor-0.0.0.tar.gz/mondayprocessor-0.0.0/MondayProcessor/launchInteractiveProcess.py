import pandas as pd 

def launchInteractiveProcess(self, board_id:int) -> pd.DataFrame:
    data = self._fetchPrismConf(board_id)
    df = pd.DataFrame.from_records(data)
    # print(df.head(10))
    return df