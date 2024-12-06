from ..MondayProcessorException import MondayProcessorException

class MondayProcessorBoardNotFound(MondayProcessorException):
    def __init__(self, *args: object) -> None:
        super().__init__(*args)