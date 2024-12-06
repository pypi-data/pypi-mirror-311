from typing import List  # , Union
from .tool_runner import ToolRunner
from nbitk.config import Config


class Vsearch(ToolRunner):
    """
    A subclass of ToolRunner specifically for running Vsearch.

    Examples:

        >>> from nbitk.Tools.vsearch import Vsearch
        >>> from nbitk.config import Config

        >>> config = Config()
        >>> config.load_config('path/to/config.yaml')
        >>> vsearch_runner.set_params({
        >>>     "threads": "8",
        >>>     "maxaccepts": "10",
        >>>     "maxrejects": "5",
        >>>     "id": "0.97" })
        >>> return_code = vsearch_runner.run()
    """

    def __init__(self, config: Config):
        """
        Initialize the Vsearchrunner with a configuration object.

        :param config: Configuration object containing tool and logger settings.
        :type config: Config
        """
        super().__init__(config)
        self.tool_name = "vsearch"

    def set_params(self, params: dict) -> None:
        """
        Set multiple command-line parameters for Vsearch.

        Args:
            params (dict): A dictionary where keys are parameter names (str) and
                        values are the parameter value (str or any type that
                        can be converted to a string).

        Example:

            >>> from nbitk.Tools.vsearch import Vsearch
            >>> from nbitk.config import Config # could also load params from a confing
            >>> vsearch_runner.set_params({
            >>>     "threads": "8",
            >>>     "maxaccepts": "10",
            >>>     "maxrejects": "5",
            >>>     "id": "0.97"
            >>> })
            >>> vsearch_runner.run()

            This will call `set_parameter` for each parameter in the dictionary,
            setting them for the Vsearch tool instance.

        Returns:
            None
        """
        vsearch_valid_params = self.get_valid_tool_params("--help")
        for param, value in params.items():
            try:
                assert f'--{param}' in vsearch_valid_params, f"{param} is not a valid {self.tool_name} parameter"
                self.set_parameter(param, value)
                self.logger.info(f"Set parameter --{param} to {value}")
            except AssertionError as e:
                self.logger.error(str(e))

    def build_command(self) -> List[str]:
        """
        Build the vsearch merge fastq command with all set parameters.

        :return: The complete command as a list of strings.
        :rtype: List[str]
        """
        command = super().build_command()

        return command

    @staticmethod
    def long_arg_prefix() -> str:
        """
        Get the appropriate prefix for a long command-line argument

        :return: The appropriate prefix for a long argument
        :rtype: str
        """
        return "--"
