class NotConnectedError(Exception):
    def __init__(self) -> None:
        super().__init__()
        self.args = ("The connection to the Revolt API is not formalised.",)