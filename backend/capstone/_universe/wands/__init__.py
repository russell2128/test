from __future__ import annotations

import abc


class AbstractBaseWand(abc.ABC):
    def __init__(self, central_hub_):
        import capstone._universe.centralhub

        self.__central_hub: capstone._universe.centralhub.WandsCentralHub = central_hub_

    @property
    def master_central_hub(self):
        return self.__central_hub