# Copyright 2024 Luminary Cloud, Inc. All Rights Reserved.
from dataclasses import dataclass
from luminarycloud.params._param_wrappers import ParamGroupWrapper
from luminarycloud._proto.output import output_pb2 as outputpb
from luminarycloud.params.outputs import Output


@dataclass(kw_only=True)
class StoppingCondition(ParamGroupWrapper[outputpb.StoppingCondition]):
    """Stopping condition for the solver"""

    output: Output
    threshold: float

    def _to_proto(self) -> outputpb.StoppingCondition:
        _proto = outputpb.StoppingCondition()
        _proto.output.CopyFrom(self.output._to_proto())
        _proto.threshold.value = self.threshold
        return _proto

    def _from_proto(self, proto: outputpb.StoppingCondition):
        self.output = Output._from_proto(proto.output)
        self.threshold = proto.threshold.value
