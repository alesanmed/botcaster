from connectors.ivoox import IvooxConnector
from state_machine.STATES import UploadStates


class StateMachine:
    def __init__(self, connector: IvooxConnector) -> None:
        self.connector = connector
        self.current_state = UploadStates.SELECT_PROGRAM
