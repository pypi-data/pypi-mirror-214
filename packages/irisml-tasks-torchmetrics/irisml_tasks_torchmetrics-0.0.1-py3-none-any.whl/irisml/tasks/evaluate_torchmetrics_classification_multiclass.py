import dataclasses
import logging
import torch
import torchmetrics.classification
import irisml.core

logger = logging.getLogger(__name__)


class Task(irisml.core.TaskBase):
    """Evaluate predictions results using torchmetrics classification metrics for multiclass classification problems.

    The following metrics are supported:
    - accuracy
    - average_precision
    - calibration_error
    - f1_score
    - precision
    - recall

    Inputs:
        predictions (Tensor): The predictions. The predictions can be either class indices or logits. The shape is (N, ) or (N, num_classes).
        targets (Tensor): The targets with shape (N, ).
        num_classes (int): The number of classes.
    """

    VERSION = '0.1.0'

    @dataclasses.dataclass
    class Inputs:
        predictions: torch.Tensor  # Shape (N, ) or (N, num_classes)
        targets: torch.Tensor  # Shape (N, )
        num_classes: int

    @dataclasses.dataclass
    class Outputs:
        accuracy: float
        average_precision: float
        calibration_error: float
        f1_score: float
        precision: float
        recall: float

    def execute(self, inputs):
        if len(inputs.predictions) != len(inputs.targets):
            raise ValueError(f"predictions and targets must have the same length, got {len(inputs.predictions)} and {len(inputs.targets)}")

        predictions = inputs.predictions

        # If the predictions are int then we assume they are class indices and we need to convert them to one-hot vectors
        if inputs.predictions.ndim == 1 and not torch.is_floating_point(inputs.predictions):
            predictions = torch.nn.functional.one_hot(inputs.predictions, num_classes=inputs.num_classes).to(torch.float32)

        assert predictions.ndim == 2 and predictions.shape[1] == inputs.num_classes, f"predictions must be a 2D tensor with shape (N, {inputs.num_classes})"

        accuracy = float(torchmetrics.functional.accuracy(torch.argmax(predictions, dim=1), inputs.targets, 'multiclass', num_classes=inputs.num_classes))
        average_precision = float(torchmetrics.functional.average_precision(predictions, inputs.targets, 'multiclass', num_classes=inputs.num_classes))
        calibration_error = float(torchmetrics.functional.calibration_error(predictions, inputs.targets, 'multiclass', num_classes=inputs.num_classes))
        f1_score = float(torchmetrics.functional.f1_score(predictions, inputs.targets, 'multiclass', num_classes=inputs.num_classes))
        precision = float(torchmetrics.functional.precision(predictions, inputs.targets, 'multiclass', num_classes=inputs.num_classes))
        recall = float(torchmetrics.functional.recall(predictions, inputs.targets, 'multiclass', num_classes=inputs.num_classes))

        logger.info(f"accuracy: {accuracy}, average_precision: {average_precision}, calibration_error: {calibration_error}, f1_score: {f1_score}, precision: {precision}, recall: {recall}")

        return self.Outputs(accuracy=accuracy, average_precision=average_precision, calibration_error=calibration_error, f1_score=f1_score, precision=precision, recall=recall)
