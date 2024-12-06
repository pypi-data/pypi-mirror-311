import pandas as pd
from abc import ABC, abstractmethod

@abstractmethod
def launchInteractiveProcess(self) -> pd.DataFrame:
    pass