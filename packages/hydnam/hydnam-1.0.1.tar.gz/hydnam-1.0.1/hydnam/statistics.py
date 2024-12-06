import dataclasses
import json


@dataclasses.dataclass
class Statistics:
    nse: float = None
    rmse: float = None
    fbias: float = None

    def __str__(self):
        return json.dumps(self.__dict__, indent=4)
