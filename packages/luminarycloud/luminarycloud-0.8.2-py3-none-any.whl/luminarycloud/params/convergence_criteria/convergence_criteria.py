# Copyright 2024 Luminary Cloud, Inc. All Rights Reserved.
from dataclasses import dataclass, field
from luminarycloud.params._param_wrappers import ParamGroupWrapper
from luminarycloud._proto.client import simulation_pb2 as clientpb
from luminarycloud._proto.output import output_pb2 as outputpb
from luminarycloud._proto.quantity import quantity_pb2 as quantitypb
from luminarycloud.params.convergence_criteria import StoppingCondition


@dataclass(kw_only=True)
class ConvergenceCriteria(ParamGroupWrapper[clientpb.ConvergenceCriteria]):
    """Physics configuration for a simulation."""

    max_iterations: int = 2000
    """Maximum number of iterations to run the simulation."""
    stopping_conditions: list[StoppingCondition] = field(default_factory=list)
    """List of stopping conditions."""
    stop_on_any: bool = False
    """If true, the simulation will stop if any stopping condition is satisfied."""

    def _to_proto(self) -> clientpb.ConvergenceCriteria:
        _proto = clientpb.ConvergenceCriteria()
        for sc in self.stopping_conditions:
            sc_proto = sc._to_proto()
            if self.stop_on_any:
                sc_proto.op = outputpb.StoppingConditionOp.STOP_COND_OP_ANY
            else:
                sc_proto.op = outputpb.StoppingConditionOp.STOP_COND_OP_ALL
            _proto.stopping_condition.append(sc_proto)

        max_iterations_sc = outputpb.StoppingCondition()
        max_iterations_sc.output.quantity = quantitypb.ITERATION_INDEX
        max_iterations_sc.threshold.value = self.max_iterations
        max_iterations_sc.op = outputpb.StoppingConditionOp.STOP_COND_OP_FORCE
        _proto.stopping_condition.append(max_iterations_sc)

        return _proto

    def _from_proto(self, proto: clientpb.ConvergenceCriteria):
        self.stopping_conditions = []
        for sc in proto.stopping_condition:
            if sc.output.quantity == quantitypb.ITERATION_INDEX:
                self.max_iterations = sc.threshold.value
            else:
                self.stopping_conditions.append(StoppingCondition.from_proto(sc))
            if sc.op == outputpb.StoppingConditionOp.STOP_COND_OP_ANY:
                self.stop_on_any = True
