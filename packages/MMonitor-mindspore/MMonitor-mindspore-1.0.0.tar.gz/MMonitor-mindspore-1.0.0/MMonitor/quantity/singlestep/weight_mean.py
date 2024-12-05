from .base_class import SingleStepQuantity

import mindspore.ops as ops

class WeightMean(SingleStepQuantity):

    def _compute(self, global_step):
        data = self._module.weight
        return ops.mean(data)