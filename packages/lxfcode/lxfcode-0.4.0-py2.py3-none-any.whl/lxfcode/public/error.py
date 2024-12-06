class IncidentAngleNotAList(Exception):
    def __init__(self, *args: object) -> None:
        super().__init__(*args)

    pass


class XYNotSingle(Exception):
    def __init__(self, *args: object) -> None:
        super().__init__(*args)

    pass


class MultipleIncidentAngles(Exception):
    def __init__(self, *args: object) -> None:
        super().__init__(*args)
