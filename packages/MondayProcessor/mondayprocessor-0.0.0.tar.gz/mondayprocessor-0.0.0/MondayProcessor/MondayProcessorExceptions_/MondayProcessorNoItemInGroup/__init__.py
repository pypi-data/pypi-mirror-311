
from ..MondayProcessorException import MondayProcessorException
        
class MondayProcessorNoItemInGroup(MondayProcessorException):
    def __init__(self, *args: object) -> None:
        super().__init__(*args)