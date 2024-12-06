import functools
import math

import keras as ks
import tensorflow as tf

import mlable.ops
import mlable.sampling
import mlable.utils

# CATEGORICAL #################################################################

@ks.saving.register_keras_serializable(package='metrics', name='categorical_group_accuracy')
def categorical_group_accuracy(y_true: tf.Tensor, y_pred: tf.Tensor, depth: int=-1, groups: iter=[4], axes: iter=[-1], dtype: tf.dtypes.DType=None) -> tf.Tensor:
    __dtype = dtype or y_true.dtype
    # category indexes
    __yt = mlable.sampling.categorical(prediction=y_true, depth=depth, random=False)
    __yp = mlable.sampling.categorical(prediction=y_pred, depth=depth, random=False)
    # matching
    __match = tf.equal(__yt, __yp)
    # group all the predictions for a given token
    for __g, __a in zip(groups, axes):
        # repeat values so that the reduced tensor has the same shape as the original
        __match = mlable.ops.reduce_all(data=__match, group=__g, axis=__a, keepdims=True)
    # cast
    return tf.cast(__match, dtype=__dtype)

@ks.saving.register_keras_serializable(package='metrics')
class CategoricalGroupAccuracy(tf.keras.metrics.MeanMetricWrapper):
    def __init__(self, depth: int=-1, group: int=4, axis: int=-1, name: str='categorical_group_accuracy', dtype: tf.dtypes.DType=None, **kwargs):
        # serialization wrapper
        __wrap = ks.saving.register_keras_serializable(package='metrics', name='categorical_group_accuracy')
        # allow to specify several groups / axes
        __axes = [axis] if isinstance(axis, int) else list(axis)
        __groups = [group] if isinstance(group, int) else list(group)
        # adapt the measure
        __fn = __wrap(functools.partial(categorical_group_accuracy, depth=depth, groups=__groups, axes=__axes, dtype=dtype))
        # init
        super(CategoricalGroupAccuracy, self).__init__(fn=__fn, name=name, dtype=dtype, **kwargs)
        # config
        self._config = {'group': group}
        # sould be maximized
        self._direction = 'up'

    def get_config(self) -> dict:
        __config = super(CategoricalGroupAccuracy, self).get_config()
        __config.update(self._config)
        return __config

# BINARY ######################################################################

@ks.saving.register_keras_serializable(package='metrics', name='binary_group_accuracy')
def binary_group_accuracy(y_true: tf.Tensor, y_pred: tf.Tensor, depth: int=-1, groups: iter=[4], axes: iter=[-1], threshold: float=0.5, dtype: tf.dtypes.DType=None) -> tf.Tensor:
    __dtype = dtype or y_true.dtype
    # category indexes
    __yt = mlable.sampling.binary(prediction=y_true, depth=depth, threshold=threshold, random=False)
    __yp = mlable.sampling.binary(prediction=y_pred, depth=depth, threshold=threshold, random=False)
    # matching
    __match = tf.equal(__yt, __yp)
    # group all the predictions for a given token
    for __g, __a in zip(groups, axes):
        # repeat values so that the reduced tensor has the same shape as the original
        __match = mlable.ops.reduce_all(data=__match, group=__g, axis=__a, keepdims=True)
    # mean over sequence axis
    return tf.cast(__match, dtype=__dtype)

@ks.saving.register_keras_serializable(package='metrics')
class BinaryGroupAccuracy(tf.keras.metrics.MeanMetricWrapper):
    def __init__(self, depth: int=-1, group: int=4, axis: int=-1, threshold: float=0.5, name: str='binary_group_accuracy', dtype: tf.dtypes.DType=None, **kwargs):
        # serialization wrapper
        __wrap = ks.saving.register_keras_serializable(package='metrics', name='binary_group_accuracy')
        # allow to specify several groups / axes
        __axes = [axis] if isinstance(axis, int) else list(axis)
        __groups = [group] if isinstance(group, int) else list(group)
        # adapt the measure
        __fn = __wrap(functools.partial(binary_group_accuracy, depth=depth, groups=__groups, axes=__axes, threshold=threshold, dtype=dtype))
        # init
        super(BinaryGroupAccuracy, self).__init__(fn=__fn, name=name, dtype=dtype, **kwargs)
        # config
        self._config = {'group': group, 'threshold': threshold}
        # sould be maximized
        self._direction = 'up'

    def get_config(self) -> dict:
        __config = super(BinaryGroupAccuracy, self).get_config()
        __config.update(self._config)
        return __config

# BINARY ######################################################################

@ks.saving.register_keras_serializable(package='metrics', name='raw_group_accuracy')
def raw_group_accuracy(y_true: tf.Tensor, y_pred: tf.Tensor, factor: float=256.0, groups: iter=[1], axes: iter=[-1], dtype: tf.dtypes.DType=None) -> tf.Tensor:
    __dtype = dtype or y_true.dtype
    # category indexes
    __yt = mlable.sampling.raw(prediction=y_true, factor=factor, random=False)
    __yp = mlable.sampling.raw(prediction=y_pred, factor=factor, random=False)
    # matching
    __match = tf.equal(__yt, __yp)
    # group all the predictions for a given token
    for __g, __a in zip(groups, axes):
        # repeat values so that the reduced tensor has the same shape as the original
        __match = mlable.ops.reduce_all(data=__match, group=__g, axis=__a, keepdims=True)
    # mean over sequence axis
    return tf.cast(__match, dtype=__dtype)

@ks.saving.register_keras_serializable(package='metrics')
class RawGroupAccuracy(tf.keras.metrics.MeanMetricWrapper):
    def __init__(self, factor: float=256.0, group: int=1, axis: int=-1, name: str='raw_group_accuracy', dtype: tf.dtypes.DType=None, **kwargs):
        # serialization wrapper
        __wrap = ks.saving.register_keras_serializable(package='metrics', name='raw_group_accuracy')
        # allow to specify several groups / axes
        __axes = [axis] if isinstance(axis, int) else list(axis)
        __groups = [group] if isinstance(group, int) else list(group)
        # adapt the measure
        __fn = __wrap(functools.partial(raw_group_accuracy, factor=factor, groups=__groups, axes=__axes, dtype=dtype))
        # init
        super(RawGroupAccuracy, self).__init__(fn=__fn, name=name, dtype=dtype, **kwargs)
        # config
        self._config = {'group': group, 'factor': factor}
        # sould be maximized
        self._direction = 'up'

    def get_config(self) -> dict:
        __config = super(RawGroupAccuracy, self).get_config()
        __config.update(self._config)
        return __config
