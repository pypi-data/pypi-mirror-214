from typing import Callable
from typing import List
from typing import Optional
from typing import Union

from matplotlib.figure import Figure

from .abstract import AbstractOutput
from .button import ButtonOutput
from .field import FieldOutput
from .field_attribute import FieldAttribute
from .field_type_enum import FieldType
from .figure import FigureOutput
from .image import ImageOutput
from .option import Option
from .option_group import OptionGroupOutput
from .paragraph import ParagraphOutput
from .table import TableOutput
from .table_cell import TableCell
from ..latex import Latex
from ..serializer import Serializer


class OutputBuilder:
    def __init__(self, serializer: Serializer):
        self._serializer: Serializer = serializer
        self._output: list[AbstractOutput] = []
        self._score: Optional[float] = None

    @property
    def _index(self):
        return len(self._output)

    def add_paragraph(self, text: Union[str, Latex]) -> 'OutputBuilder':
        """Add a paragraph to the output. Can be used for normal text output.

        :param text: The text to print.
        :return: The current output builder instance.
        """
        paragraph: ParagraphOutput = ParagraphOutput(self._index, text)

        self._output.append(paragraph)

        return self

    def add_latex(self, text: str) -> 'OutputBuilder':
        """Add LaTeX to the output.

        :param text: The text to print.
        :return: The current output builder instance.
        """
        paragraph: ParagraphOutput = ParagraphOutput(self._index, Latex(text))

        self._output.append(paragraph)

        return self

    def add_image(self, path: str, description: str = None) -> 'OutputBuilder':
        """Add an image to the output. The path can either be absolute or relative to the working directory,
        which is normally the project root folder.

        :param path: The path to the image.
        :param description: An optional description of the image.
        :return: The current output builder instance.
        """
        image: ImageOutput = ImageOutput(self._index, path, description)

        self._output.append(image)

        return self

    def add_figure(
            self,
            figure: Figure,
            description: str = None,
            dpi: int = None,
            as_png: bool = None
    ) -> 'OutputBuilder':
        """Add a figure to the output.

        :param figure: The figure to show.
        :param description: An optional description of the figure.
        :param dpi: DPI resolution for the figure. Default is 300.
        :param as_png: Output the figure as PNG. Default is SVG.
        :return: The current output builder instance.
        """
        graph: FigureOutput = FigureOutput(self._index, figure, description, dpi, as_png)

        self._output.append(graph)

        return self

    def add_table(self, data: List[List[Union[str, int, float, Latex, TableCell]]]) -> 'OutputBuilder':
        """Add a table to the output.

        :param data: The data to display.
        :return: The current output builder instance.
        """
        table: TableOutput = TableOutput(self._index, data)

        self._output.append(table)

        return self

    def add_text_field(
            self,
            name: str,
            label: Union[str, Latex],
            value: str = None,
            required: bool = True,
            max_length: int = None
    ) -> 'OutputBuilder':
        """Add a text input field. The input will be handled as string.
        Use :meth:`add_number_field` to add a numeric input field.

        :param name: The name of the text field, should be unique.
        :param label: The label for the text field.
        :param value: The default value to display.
        :param required: Mark the field as required.
        :param max_length: The maximum length of this text field.
        :return: The current output builder instance.
        """
        field: FieldOutput = FieldOutput(self._index, FieldType.TEXT, name, label, value, required, **{
            FieldAttribute.MAX_LENGTH: max_length
        })

        self._output.append(field)

        return self

    def add_number_field(
            self,
            name: str,
            label: Union[str, Latex],
            value: float = None,
            required: bool = True,
            min_value: float = None,
            max_value: float = None,
            step: float = None
    ) -> 'OutputBuilder':
        """Add a numeric input field. The input will be handled as float.
        Use :meth:`add_text_field` to add a text input field.

        :param name: The name of the input field, should be unique.
        :param label: The label for the input field.
        :param value: The default value to display.
        :param required: Mark the field as required.
        :param min_value: The minimum value to accept.
        :param max_value: The maximum value to accept.
        :param step: The granularity of the input.
        :return: The current output builder instance.
        """
        field: FieldOutput = FieldOutput(self._index, FieldType.NUMBER, name, label, value, required, **{
            FieldAttribute.MIN: min_value,
            FieldAttribute.MAX: max_value,
            FieldAttribute.STEP: step
        })

        self._output.append(field)

        return self

    def add_option_group(
            self,
            name: str,
            label: Union[str, Latex, None],
            options: List[Union[Option, str, int, float]],
            required: bool = True,
            inline: bool = True
    ) -> 'OutputBuilder':
        """Add a radio fields. The user can choose between the provided options.

        :param name: The name of the input field, should be unique.
        :param label: The label for the input field, should be unique.
        :param options: A list of available options to choose from.
        :param required: Mark the field as required.
        :param inline: Display the options inline.
        :return: The current output builder instance.
        """
        option_group: OptionGroupOutput = OptionGroupOutput(
            self._index,
            name,
            label,
            options,
            required,
            inline,
            False)

        self._output.append(option_group)

        return self

    def add_selection_group(
            self,
            name: str,
            label: Union[str, Latex, None],
            options: List[Union[Option, str, int, float, bool]],
            required: bool = True,
            inline: bool = True
    ) -> 'OutputBuilder':
        """Add a checkbox fields. The user can choose multiple values from the provided options.

        :param name: The name of the input field, should be unique.
        :param label: The label for the input field, should be unique.
        :param options: A list of available options to choose from.
        :param required: Mark the field as required.
        :param inline: Display the options inline.
        :return: The current output builder instance.
        """
        selection_group: OptionGroupOutput = OptionGroupOutput(
            self._index,
            name,
            label,
            options,
            required,
            inline,
            True)

        self._output.append(selection_group)

        return self

    def add_action(self, title: str, action: Callable[..., 'OutputBuilder'], **kwargs) -> 'OutputBuilder':
        """Add an action button. Creates a button, if the user clicks on it, he will be redirected to the specified
        action. The action should be a method reference to another action in the exercise class.

        :param title: The title for the button, e.g. Submit.
        :param action: A method reference to the next action.
        :param kwargs: Additional arguments to pass to the action method.
        :return: The current output builder instance.
        """
        button: ButtonOutput = ButtonOutput(self._index, self._serializer, title, action.__name__, kwargs)

        self._output.append(button)

        return self

    def add_score(self, score: float) -> 'OutputBuilder':
        """Set a score. The score will be submitted to the connected LMS (e.g. Moodle).

        :param score: The score to set. Must be in the range 0.0 - 1.0.
        :return: The current output builder instance.
        """

        self._score = score

        return self

    def to_json(self) -> dict:
        output: List[dict] = list(map(self._output_to_json, self._output))
        score: Optional[float] = self._score

        return {
            'items': output,
            'score': score
        }

    @staticmethod
    def _output_to_json(output: AbstractOutput) -> dict:
        return {
            **output.to_json(),
            '_type': output.get_type()
        }
