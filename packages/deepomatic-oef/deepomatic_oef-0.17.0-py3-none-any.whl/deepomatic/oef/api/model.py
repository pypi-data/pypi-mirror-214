from abc import ABC, abstractmethod
from typing import Dict, List, Tuple, Any

import tensorflow as tf


# -----------------------------------------------------------------------------#

class ModelInterface(ABC):
    """
    This is the base class for any specific model implementation that is part of
    the `model` OneOf field of ../protos/model.proto
    """
    pass


# -----------------------------------------------------------------------------#


class MetricsEvaluator(ABC):
    """
    Base class for specific implementations of metrics. The subclass should inherit from this abstract class.
    It should also inherit from a tf.keras.metrics and call `super()` method in `reset_state()`, `update_state()`
    and `result()`.
    """

    @abstractmethod
    def update_state(self, y_true: Dict[str, tf.Tensor], y_pred: Dict[str, tf.Tensor], sample_weight: float):
        """
        Apply the metric base operation on one sample and update the metric state.
        """

    @abstractmethod
    def result(self) -> Dict[str, float]:
        """
        Aggregates results stored in the metric state.
        Returns a dictionary where each key is a single metric.
        """

    @abstractmethod
    def reset_state(self):
        """
        Reset the accumulator
        """

    def get_key_name_mapping(self) -> Dict[str, str]:
        """
        Retruns a dictionnary with
           - keys that are the same as the ones in the .result() dictionary output
           - values that are pretty names for display purposes
        """

# -----------------------------------------------------------------------------#


class TensorflowModelInterface(ModelInterface):

    @abstractmethod
    def get_feature_extractor_scopes(self):
        """
        Return the TF variable scope for the feature extractor on top of the backbone scope,
        without a trailing slash. This is used to decide whether the provided checkpoint file
        is a backbone chekpoint or a full model chekpoint.

        If the model does not have something else than a backbone part, it should return None.

        For example: ['FirstStageFeatureExtractor']

        Return
            scopes: A list of feature extractor scopes (string) or None if there is nothing else than a feature extractor.
        """

    @abstractmethod
    def get_groundtruth(self, mode, annotations):
        """
        Returns groundtruth tensors.

        Args:
            mode (tf.estimator.ModeKeys): tf.estimator.ModeKeys.TRAIN / EVAL / PREDICT
            annotations: Dictionary of groundtruth tensors.
                labels[fields.InputDataFields.num_groundtruth_boxes] is a [batch_size]
                    int32 tensor indicating the number of groundtruth boxes.
                labels[fields.InputDataFields.groundtruth_boxes] is a
                    [batch_size, num_boxes, 4] float32 tensor containing the corners of
                    the groundtruth boxes in the order (ymin, xmin, ymax, xmax)
                labels[fields.InputDataFields.groundtruth_classes] is a
                    [batch_size, num_boxes, num_classes] float32 k-hot tensor of
                    classes.
                labels[fields.InputDataFields.groundtruth_weights] is a
                    [batch_size, num_boxes] float32 tensor containing groundtruth weights
                    for the boxes.
                -- Optional --
            For Segmentation Tasks
                labels[fields.InputDataFields.groundtruth_instance_masks] is a
                    [batch_size, num_boxes, H, W] float32 tensor containing only binary
                    values, which represent instance masks for objects.
            For Keypoint Detection Tasks
                labels[fields.InputDataFields.groundtruth_keypoints] is a
                    [batch_size, num_boxes, num_keypoints, 2] float32 tensor containing
                    keypoints for each box.
                labels[fields.InputDataFields.groundtruth_weights] is a
                    [batch_size, num_boxes, num_keypoints] float32 tensor containing
                    groundtruth weights for the keypoints.
                labels[fields.InputDataFields.groundtruth_visibilities] is a
                    [batch_size, num_boxes, num_keypoints] bool tensor containing
                    groundtruth visibilities for each keypoint.
            For Dense pose models (3D Pose estimation)
                labels[fields.InputDataFields.groundtruth_dp_num_points] is a
                    [batch_size, num_boxes] int32 tensor with the number of sampled
                    DensePose points per object.
                labels[fields.InputDataFields.groundtruth_dp_part_ids] is a
                    [batch_size, num_boxes, max_sampled_points] int32 tensor with the
                    DensePose part ids (0-indexed) per object.
                labels[fields.InputDataFields.groundtruth_dp_surface_coords] is a
                    [batch_size, num_boxes, max_sampled_points, 4] float32 tensor with the
                    DensePose surface coordinates. The format is (y, x, v, u), where (y, x)
                    are normalized image coordinates and (v, u) are normalized surface part
                    coordinates.
            For Tracking
                labels[fields.InputDataFields.groundtruth_track_ids] is a
                    [batch_size, num_boxes] int32 tensor with the track ID for each object.


        Return:
            A groundtruth object that will be passed to `get_prediction_dict`, `get_losses` and `get_eval_metrics`.
        """

    @abstractmethod
    def get_predictions(self, mode, input_data, groundtruth=None):
        """
        Returns raw predictions (typically logits).

        Args:
            mode (tf.estimator.ModeKeys): tf.estimator.ModeKeys.TRAIN / EVAL / PREDICT
            input_data (dict of tensors): the dictionary of input tensors
            groundtruth: the ground truth as returned by get_groundtruth.
                         Some models like Faster-RCNN need ground-truth at training time to
                         properly balance sampled proposals. In prediction mode, this parameter
                         will be None.

        Returns:
            A predictions object that will be passed to `postprocess_predictions` and `get_eval_metrics`
        """

    @abstractmethod
    def get_postprocessed_predictions(self, input_data, predictions):
        """
        Apply a final post-processing step to predictions.

        Args:
            input_data (dict of tensors): the dictionary of input tensors
            predictions (object): the predictions object as returned by `get_predictions`

        Returns:
            A dictionary of tensors with keys being the same as the dict returned by
            `get_export_tensors_fn_dict`
        """

    @abstractmethod
    def get_losses(self, input_data, predictions, groundtruth):
        """
        Returns a list of losses

        Args:
            input_data (dict of tensors): the dictionary of input tensors
            predictions (object): the predictions object as returned by `get_predictions`
            groundtruth (object): the groundtruth object as returned by `get_groundtruth`

        Returns:
            A list of tuple (pretty_name (str), loss_tensor).
        """

    @abstractmethod
    def get_regularization_losses(self, model):
        """
        Returns a list of regularization losses
        """

    @abstractmethod
    def get_update_ops(self):
        """
        Returns tensorflow update ops
        """

    @abstractmethod
    def get_eval_metrics(self, model, input_data, postprocessed_predictions, groundtruth):
        """
        Returns a list of metrics

        Args:
            model (object): the model as returned by `model_fn`
            input_data (dict of tensors): the dictionary of input tensors
            postprocessed_predictions (dict of tensors): the post-processed predictions object as returned by `postprocess_predictions`
            groundtruth (object): the groundtruth object as returned by `get_groundtruth`

        Returns:
            A list of tuples: (pretty_name (str), display_in_metrics_summary (bool), metric_tensor)
        """

    @abstractmethod
    def get_export_tensors_fn_dict(self):
        """
        Return output tensor names.

        Return:
            outputs: A list of string.
        """


# -----------------------------------------------------------------------------#

class KerasModelInterface(ModelInterface):

    @abstractmethod
    def get_model(self) -> tf.keras.Model:
        """
        Returns a (non-compiled) Keras model
        """

    @abstractmethod
    def get_groundtruth(self, annotations: Dict[str, tf.Tensor]) -> Dict[str, tf.Tensor]:
        """
        Returns a dict of ground-truth tensors, with keys matching (i) the loss tensor_name
        and (ii) the output tensor of the model on which loss is applied.

        Args:
            annotations: Dictionary of groundtruth tensors.
                labels[fields.InputDataFields.num_groundtruth_boxes] is a [batch_size]
                    int32 tensor indicating the number of groundtruth boxes.
                labels[fields.InputDataFields.groundtruth_boxes] is a
                    [batch_size, num_boxes, 4] float32 tensor containing the corners of
                    the groundtruth boxes in the order (ymin, xmin, ymax, xmax)
                labels[fields.InputDataFields.groundtruth_classes] is a
                    [batch_size, num_boxes, num_classes] float32 k-hot tensor of
                    classes.
                labels[fields.InputDataFields.groundtruth_weights] is a
                    [batch_size, num_boxes] float32 tensor containing groundtruth weights
                    for the boxes.
                -- Optional --
            For Segmentation Tasks
                labels[fields.InputDataFields.groundtruth_instance_masks] is a
                    [batch_size, num_boxes, H, W] float32 tensor containing only binary
                    values, which represent instance masks for objects.
            For Keypoint Detection Tasks
                labels[fields.InputDataFields.groundtruth_keypoints] is a
                    [batch_size, num_boxes, num_keypoints, 2] float32 tensor containing
                    keypoints for each box.
                labels[fields.InputDataFields.groundtruth_weights] is a
                    [batch_size, num_boxes, num_keypoints] float32 tensor containing
                    groundtruth weights for the keypoints.
                labels[fields.InputDataFields.groundtruth_visibilities] is a
                    [batch_size, num_boxes, num_keypoints] bool tensor containing
                    groundtruth visibilities for each keypoint.
            For Dense pose models (3D Pose estimation)
                labels[fields.InputDataFields.groundtruth_dp_num_points] is a
                    [batch_size, num_boxes] int32 tensor with the number of sampled
                    DensePose points per object.
                labels[fields.InputDataFields.groundtruth_dp_part_ids] is a
                    [batch_size, num_boxes, max_sampled_points] int32 tensor with the
                    DensePose part ids (0-indexed) per object.
                labels[fields.InputDataFields.groundtruth_dp_surface_coords] is a
                    [batch_size, num_boxes, max_sampled_points, 4] float32 tensor with the
                    DensePose surface coordinates. The format is (y, x, v, u), where (y, x)
                    are normalized image coordinates and (v, u) are normalized surface part
                    coordinates.
            For Tracking
                labels[fields.InputDataFields.groundtruth_track_ids] is a
                    [batch_size, num_boxes] int32 tensor with the track ID for each object.
        """

    @abstractmethod
    def get_eval_metrics(self) -> List[MetricsEvaluator]:
        """
        Returns the list of metric evaluators to use to report the performance of the model during training.
        Generally metric evaluators are specific to a task.
        Returns:
            A list of MetricsEvaluator
        """

    @abstractmethod
    def get_losses(self) -> List[Tuple[str, bool, str, tf.keras.losses.Loss, float]]:
        """
        Returns a list of losses

        Args:
            input_data (dict of tensors): the dictionary of input tensors
            predictions (object): the predictions object as returned by `get_predictions`
            groundtruth (object): the groundtruth object as returned by `get_groundtruth`

        Returns:
            A list of tuples (pretty_name (str), display_in_metrics_summary (bool), tensor_name (str), loss, weight)
        """

    @abstractmethod
    def get_postprocessed_predictions(self, postprocessed_prediction: Any) -> Dict[str, tf.Tensor]:
        """
        Post-process predictions and standardize them for metric computation. The resulting dictionary keys should
        match those in the groundtruth and be adapted to your custom metric implementation.
        Args:
            raw_model_output (any): The raw output of the model when is_training = True (the model used for training)
        Return:
            standardized_pred (dict): Dictionary of prediction tensors adapted to custom metrics computation
        """
