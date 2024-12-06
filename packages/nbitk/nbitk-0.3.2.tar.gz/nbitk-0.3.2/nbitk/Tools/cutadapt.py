from typing import List, Union
from .tool_runner import ToolRunner
from nbitk.config import Config


class Cutadapt(ToolRunner):
    """
    A subclass of ToolRunner specifically for running Cutadapt.

    Examples:
        >>> config = Config()
        >>> config.load_config('path/to/config.yaml')
        >>> cutadapt_runner = Cutadapt(config)
        >>> cutadapt_runner.set_input_1('input.fastq')
        >>> cutadapt_runner.set_output_1('output1.fastq')
        >>> cutadapt_runner.set_output_2('output2.fastq') #if paired end
        >>> cutadapt_runner.set_adapter_1('AGATCGGAAGAGCACACGTCTGAACTCCAGTCA')
        >>> cutadapt_runner.set_min_length(20)
        >>> cutadapt_runner.set_quality_cutoff(20)
        >>> cutadapt_runner.set_overlap(3)
        >>> cutadapt_runner.trim_n = True
        >>> return_code = cutadapt_runner.run()
    """

    def __init__(self, config: Config):
        """
        Initialize the Cutadapt runner with a configuration object.

        :param config: Configuration object containing tool and logger settings.
        :type config: Config
        """
        super().__init__(config)
        self.tool_name = "cutadapt"
        self.set_min_length(0)  # Default minimum length
        self.set_quality_cutoff(0)  # Default quality cutoff
        self.set_overlap(3)  # Default overlap length
        self.set_error_rate(0.1)  # Default error rate
        self.trim_n = False  # Default for trimming 'N's
        self.discard_untrimmed = False
        self.paired_end = False

    def set_input_1(self, input_file_1: str) -> None:
        """
        Set the input file name.

        :param input_file: Path to the input file.
        :type input_file: str
        """
        self.set_parameter("input_1", input_file_1)  # input has no prefix

    def set_input_2(self, input_file_2: str) -> None:
        """
        Set the input file name. only applicable for paired end

        :param input_file: Path to the input file.
        :type input_file: str
        """
        self.set_parameter("input_2", input_file_2)

    def set_output_1(self, output_file_1: str) -> None:
        """
        Set the output file name.
        :param output_file: Path to the output file.
        :type output_file: str
        """
        self.set_parameter("output", output_file_1)

    def set_output_2(self, output_file_2: str) -> None:
        """
        Set the output file name. only applicable for paired end

        :param output_file: Path to the output file.
        :type output_file: str
        """
        self.set_parameter("paired-output", output_file_2)

    def set_adapter_1(self, adapter_1: str) -> None:
        """
        Set the adapter 1 sequence to be trimmed.

        :param adapter: Adapter sequence.
        :type adapter: str
        """
        self.set_parameter("adapter", adapter_1)

    def set_adapter_2(self, adapter_2: str) -> None:
        """
        Set the adapter 2 sequence to be trimmed.

        :param adapter: Adapter sequence.
        :type adapter: str
        """
        self.set_parameter("front", adapter_2)

    def set_min_length(self, min_length: int) -> None:
        """
        Set the minimum length of reads to keep.

        :param min_length: Minimum length (0 to disable).
        :type min_length: int
        """
        self.set_parameter("minimum-length", str(min_length))

    def set_quality_cutoff(self, quality_cutoff: Union[int, str]) -> None:
        """
        Set the quality cutoff score for trimming.

        :param quality_cutoff: Quality cutoff (can be a single integer or a range "low,high").
        :type quality_cutoff: Union[int, str]
        """
        self.set_parameter("quality-cutoff", str(quality_cutoff))

    def set_overlap(self, overlap: int) -> None:
        """
        Set the minimum overlap length between adapter and read.

        :param overlap: Minimum overlap length.
        :type overlap: int
        """
        self.set_parameter("overlap", str(overlap))

    def set_error_rate(self, error_rate: float) -> None:
        """
        Set the maximum allowed error rate.

        :param error_rate: Error rate (0.0 to 1.0).
        :type error_rate: float
        """
        self.set_parameter("error-rate", str(error_rate))

    def set_max_n(self, max_n: int) -> None:
        """
        Set the maximum number of 'N's allowed in a read.

        :param max_n: Maximum number of 'N's allowed.
        :type max_n: int
        """
        self.set_parameter("max-n", str(max_n))

    def set_cores(self, n_cores: int = 0) -> None:
        """
        Set the number of CPUs to use.

        :param n_cores: number of CPUS.
        :type n_cores: int (zero to autodetect)
        """

        self.set_parameter("cores", n_cores)

    def set_output_format(self, output_format: str) -> None:
        """
        Set the output format (fasta or fastq).

        :param output_format: Output format.
        :type output_format: str
        """
        self.set_parameter("output", output_format)  # need fixing to use only fasta

    def set_json_report(self, json_file: str) -> None:
        """
        Dump report in JSON format to FILE

        :param json_file: json file path.
        :type json_file: str pathlike
        """
        self.set_parameter("json", json_file)

    def set_report(self, report_type: str = "full") -> None:
        """
        Which type of report to print

        :param report_type: one of {full,minimal}.
        :type report_type: str
        """
        self.set_parameter("report", report_type)

    def build_command(self) -> List[str]:
        """
        Build the Cutadapt command with all set parameters.

        :return: The complete Cutadapt command as a list of strings.
        :rtype: List[str]
        """
        # if n cores were not set; set to 0 to autodetect
        if not self.get_parameter("cores"):
            self.set_parameter("cores", 0)

        command = super().build_command()

        # handling boolean params
        if self.trim_n:
            command.append("--trim-n")
        if self.discard_untrimmed:
            command.append("--discard-untrimmed")

        # Handle inputs params since they do not have prefixes
        command.pop(command.index(self.get_parameter("input_1")))
        command.pop(command.index("--input_1"))
        command.append(self.get_parameter("input_1"))

        if "--input_2" in command:
            # Handle input2  params since they do not have prefixes
            command.pop(command.index(self.get_parameter("input_2")))
            command.pop(command.index("--input_2"))
            command.append(self.get_parameter("input_2"))

        # Handle adapters incase of paired reads
        if self.paired_end or "--input_2" in command:  # also try to guese in case the user forgot to set paired to true
            # ensure --adapter points to 3' and --front point to 5' in the case of paired end
            adapter1_index, adapter2_index = command.index("--adapter"), command.index("--front")
            command[adapter1_index], command[adapter2_index] = command[adapter2_index], command[adapter1_index]

        return command

    @staticmethod
    def long_arg_prefix() -> str:
        """
        Get the appropriate prefix for a long command-line argument

        :return: The appropriate prefix for a long argument
        :rtype: str
        """
        return "--"
