"""
Utility functions for the style config module.
"""

from typing import Type

from deepmerge import always_merger
from pydantic import BaseModel


def merge_models[
    M: BaseModel
](model_a: M, model_b: M, model: Type[M], override_with_none: bool = False,) -> M:
    """
    This function (partially) overrides the field values of copy of
    `model_a` with the fields values of `model_b`.

    :param model_a: Instance to be overridden
    :type model_a: ModelType
    :param model_b: Instance to take the overriding values from
    :type model_b: ModelType
    :param model: Model class to use for creating the returned Model
    :type model: Type[ModelType]
    :param override_with_none: If `True`, overrides `model_a` with `None` values of `model_b`

    :return: Corresponding new model instance
    :rtype: ModelType
    """

    # I'm aware of the fact that this solution looks more than cursed.
    # This is due to the fact, that Pydantic does not allow for creating/updating
    # a new/updated model from an existing one via methods like `.model_update()`
    # or `.model_construct()` due to lacking validation. Thus, nested models will not
    # be instantiated but rather the dict describing the nested model directly assigned
    # to the corresponding attribute.
    # Details on this can be found in the documentation and the
    # following Pydantic GitHub Discussion:
    # https://github.com/pydantic/pydantic/discussions/10035
    # Therefore, the current workaround is to merge the dumped python models and
    # create an entirely new model class as return value.

    model_a_dict = model_a.model_dump()
    model_b_dict = model_b.model_dump(exclude_none=not override_with_none)

    merged_model_dict = always_merger.merge(model_a_dict, model_b_dict)

    return model(**merged_model_dict)
