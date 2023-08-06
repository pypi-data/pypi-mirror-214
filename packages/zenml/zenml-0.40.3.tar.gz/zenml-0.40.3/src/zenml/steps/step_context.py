#  Copyright (c) ZenML GmbH 2022. All Rights Reserved.
#
#  Licensed under the Apache License, Version 2.0 (the "License");
#  you may not use this file except in compliance with the License.
#  You may obtain a copy of the License at:
#
#       http://www.apache.org/licenses/LICENSE-2.0
#
#  Unless required by applicable law or agreed to in writing, software
#  distributed under the License is distributed on an "AS IS" BASIS,
#  WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express
#  or implied. See the License for the specific language governing
#  permissions and limitations under the License.
"""Step context class."""

from typing import (
    TYPE_CHECKING,
    Any,
    Dict,
    Mapping,
    NamedTuple,
    Optional,
    Sequence,
    Type,
)

from zenml.client import Client
from zenml.environment import Environment
from zenml.exceptions import StepContextError

if TYPE_CHECKING:
    from zenml.config.step_run_info import StepRunInfo
    from zenml.materializers.base_materializer import BaseMaterializer
    from zenml.stack import Stack


class StepContextOutput(NamedTuple):
    """Tuple containing materializer class and URI for a step output."""

    materializer_classes: Sequence[Type["BaseMaterializer"]]
    artifact_uri: str


class StepContext:
    """Provides additional context inside a step function.

    This class is used to access pipelines, materializers, and artifacts
    inside a step function. To use it, add a `StepContext` object
    to the signature of your step function like this:

    ```python
    @step
    def my_step(context: StepContext, ...)
        context.get_output_materializer(...)
    ```

    You do not need to create a `StepContext` object yourself and pass it
    when creating the step, as long as you specify it in the signature ZenML
    will create the `StepContext` and automatically pass it when executing your
    step.

    **Note**: When using a `StepContext` inside a step, ZenML disables caching
    for this step by default as the context provides access to external
    resources which might influence the result of your step execution. To
    enable caching anyway, explicitly enable it in the `@step` decorator or when
    initializing your custom step class.
    """

    def __init__(
        self,
        step_name: str,
        output_materializers: Mapping[str, Sequence[Type["BaseMaterializer"]]],
        output_artifact_uris: Mapping[str, str],
    ):
        """Initializes a StepContext instance.

        Args:
            step_name: The name of the step that this context is used in.
            output_materializers: The output materializers of the step that
                this context is used in.
            output_artifact_uris: The output artifacts of the step that this
                context is used in.

        Raises:
            StepContextError: If the keys of the output materializers and
                output artifacts do not match.
        """
        if output_materializers.keys() != output_artifact_uris.keys():
            raise StepContextError(
                f"Mismatched keys in output materializers and output "
                f"artifacts URIs for step '{step_name}'. Output materializer "
                f"keys: {set(output_materializers)}, output artifact URI "
                f"keys: {set(output_artifact_uris)}"
            )

        self.step_name = step_name
        self._outputs = {
            key: StepContextOutput(
                output_materializers[key], output_artifact_uris[key]
            )
            for key in output_materializers.keys()
        }
        self._stack = Client().active_stack

    def _get_output(
        self, output_name: Optional[str] = None
    ) -> StepContextOutput:
        """Returns the materializer and artifact URI for a given step output.

        Args:
            output_name: Optional name of the output for which to get the
                materializer and URI.

        Returns:
            Tuple containing the materializer and artifact URI for the
                given output.

        Raises:
            StepContextError: If the step has no outputs, no output for
                the given `output_name` or if no `output_name` was given but
                the step has multiple outputs.
        """
        output_count = len(self._outputs)
        if output_count == 0:
            raise StepContextError(
                f"Unable to get step output for step '{self.step_name}': "
                f"This step does not have any outputs."
            )

        if not output_name and output_count > 1:
            raise StepContextError(
                f"Unable to get step output for step '{self.step_name}': "
                f"This step has multiple outputs ({set(self._outputs)}), "
                f"please specify which output to return."
            )

        if output_name:
            if output_name not in self._outputs:
                raise StepContextError(
                    f"Unable to get step output '{output_name}' for "
                    f"step '{self.step_name}'. This step does not have an "
                    f"output with the given name, please specify one of the "
                    f"available outputs: {set(self._outputs)}."
                )
            return self._outputs[output_name]
        else:
            return next(iter(self._outputs.values()))

    @property
    def stack(self) -> Optional["Stack"]:
        """Returns the current active stack.

        Returns:
            The current active stack or None.
        """
        return self._stack

    @property
    def pipeline_name(self) -> Optional[str]:
        """Returns the current pipeline name.

        Returns:
            The current pipeline name or None.
        """
        env = Environment().step_environment
        return env.pipeline_name

    @property
    def run_name(self) -> Optional[str]:
        """Returns the current run name.

        Returns:
            The current run name or None.
        """
        env = Environment().step_environment
        return env.run_name

    @property
    def parameters(self) -> Dict[str, Any]:
        """The step parameters.

        Returns:
            The step parameters.
        """
        return self.step_run_info.config.parameters

    @property
    def step_run_info(self) -> "StepRunInfo":
        """Info about the currently running step.

        Returns:
            Info about the currently running step.
        """
        env = Environment().step_environment
        return env.step_run_info

    @property
    def cache_enabled(self) -> bool:
        """Returns whether cache is enabled for the step.

        Returns:
            True if cache is enabled for the step, otherwise False.
        """
        env = Environment().step_environment
        return env.cache_enabled

    def get_output_materializer(
        self,
        output_name: Optional[str] = None,
        custom_materializer_class: Optional[Type["BaseMaterializer"]] = None,
        data_type: Optional[Type[Any]] = None,
    ) -> "BaseMaterializer":
        """Returns a materializer for a given step output.

        Args:
            output_name: Optional name of the output for which to get the
                materializer. If no name is given and the step only has a
                single output, the materializer of this output will be
                returned. If the step has multiple outputs, an exception
                will be raised.
            custom_materializer_class: If given, this `BaseMaterializer`
                subclass will be initialized with the output artifact instead
                of the materializer that was registered for this step output.
            data_type: If the output annotation is of type `Union` and the step
                therefore has multiple materializers configured, you can provide
                a data type for the output which will be used to select the
                correct materializer. If not provided, the first materializer
                will be used.

        Returns:
            A materializer initialized with the output artifact for
            the given output.
        """
        from zenml.utils import materializer_utils

        materializer_classes, artifact_uri = self._get_output(output_name)

        if custom_materializer_class:
            materializer_class = custom_materializer_class
        elif len(materializer_classes) == 1 or not data_type:
            materializer_class = materializer_classes[0]
        else:
            materializer_class = materializer_utils.select_materializer(
                data_type=data_type, materializer_classes=materializer_classes
            )

        return materializer_class(artifact_uri)

    def get_output_artifact_uri(
        self, output_name: Optional[str] = None
    ) -> str:
        """Returns the artifact URI for a given step output.

        Args:
            output_name: Optional name of the output for which to get the URI.
                If no name is given and the step only has a single output,
                the URI of this output will be returned. If the step has
                multiple outputs, an exception will be raised.

        Returns:
            Artifact URI for the given output.
        """
        return self._get_output(output_name).artifact_uri
