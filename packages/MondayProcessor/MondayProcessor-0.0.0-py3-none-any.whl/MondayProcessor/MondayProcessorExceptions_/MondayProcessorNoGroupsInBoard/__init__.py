from ..MondayProcessorException import MondayProcessorException

class MondayProcessorNoGroupsInBoard(MondayProcessorException):
    def __init__(self, *args: object) -> None:
        super().__init__(*args)