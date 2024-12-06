from typing import Optional, List

from .basin_def import BasinDef
from .bsd_flow_node import FlowNode
from .parameters import SinkParameters


class Sink(FlowNode):
    def __init__(
            self, name: str,
            downstream: Optional[BasinDef] = None,
            upstream: Optional[List[BasinDef]] = None,
            paramters: SinkParameters = SinkParameters()
    ):
        super().__init__(name, downstream, upstream)
        self._parameters = paramters
