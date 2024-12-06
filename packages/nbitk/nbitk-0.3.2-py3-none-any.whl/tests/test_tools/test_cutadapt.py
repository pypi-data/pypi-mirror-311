import os
import pytest
from pathlib import Path
from Bio import SeqIO
from nbitk.Tools.cutadapt import Cutadapt
from nbitk.config import Config

# Construct the path to the config file
CONFIG_PATH = Path(__file__).parent.parent.parent / 'config' / 'config.yaml'

@pytest.fixture
def config():
    """Fixture to create and load a Config object for each test."""
    cfg = Config()
    cfg.load_config(CONFIG_PATH)
    cfg.set('log_level', 'ERROR')
    return cfg

@pytest.fixture
def temp_input_fastq(tmp_path):
    """Fixture to create a temporary input FASTQ file with adapters."""
    temp_fastq_path = tmp_path / "temp_input.fastq"
    
    example_sequences = [
        ("SEQ_ID_1", "AGATCGGAAGAGCACACGTCTGAACTCCAGTCAACGTGATCGTAGCTAGCTA", "IIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIII"),
        ("SEQ_ID_2", "ACGTGATCGTAGCTAGCTAGATCGGAAGAGCACACGTCTGAACTCCAGTCA", "IIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIII"),
        ("SEQ_ID_3", "TTAGCTAGCTAGCTAGCTAGCTAGATCGGAAGAGCACACGTCTGAACTCCA", "IIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIII"),
    ]

    with open(temp_fastq_path, "w") as f:
        for seq_id, sequence, quality in example_sequences:
            f.write(f"@{seq_id}\n{sequence}\n+\n{quality}\n")

    return temp_fastq_path

@pytest.fixture
def temp_input_fasta(tmp_path):
    """Fixture to create a temporary input FASTA file with adapters."""
    temp_fasta_path = tmp_path / "temp_input.fasta"
    
    example_sequences = [
        ("SEQ_ID_1", "AGATCGGAAGAGCACACGTCTGAACTCCAGTCAACGTGATCGTAGCTAGCTA"),
        ("SEQ_ID_2", "ACGTGATCGTAGCTAGCTAGATCGGAAGAGCACACGTCTGAACTCCAGTCA"),
        ("SEQ_ID_3", "TTAGCTAGCTAGCTAGCTAGCTAGATCGGAAGAGCACACGTCTGAACTCCA"),
    ]

    with open(temp_fasta_path, "w") as f:
        for seq_id, sequence in example_sequences:
            f.write(f">{seq_id}\n{sequence}\n")

    return temp_fasta_path

# single end
def test_cutadapt_run_fastq(config, temp_input_fastq, tmp_path):
    """Test running Cutadapt with the FASTQ input file and adapter trimming."""
    output_file = tmp_path / "cutadapt_output.fastq"
    
    cutadapt_runner = Cutadapt(config)
    cutadapt_runner.set_input_1(str(temp_input_fastq))
    cutadapt_runner.set_output_1(str(output_file))
    cutadapt_runner.set_adapter_1("AGATCGGAAGAGCACACGTCTGAACTCCAGTCA")
    cutadapt_runner.set_min_length(20)
    cutadapt_runner.set_quality_cutoff(20)
    cutadapt_runner.set_overlap(3)
    cutadapt_runner.set_error_rate(0.1)
    cutadapt_runner.trim_n = True
    cutadapt_runner.discard_untrimmed = True
    

    return_code = cutadapt_runner.run()

    assert return_code == 0, "Cutadapt failed to run successfully with FASTQ input"
    assert os.path.exists(output_file), "Cutadapt output file was not created"

    with open(output_file, "r") as f:
        trimmed_sequences = list(SeqIO.parse(f, "fastq"))
    assert len(trimmed_sequences) > 0, "No sequences were trimmed and written to the output"

def test_cutadapt_run_fasta(config, temp_input_fasta, tmp_path):
    """Test running Cutadapt with the FASTA input file and adapter trimming."""
    output_file = tmp_path / "cutadapt_output.fasta"
    
    cutadapt_runner = Cutadapt(config)
    cutadapt_runner.set_input_1(str(temp_input_fasta))
    cutadapt_runner.set_output_1(str(output_file))
    cutadapt_runner.set_adapter_1("AGATCGGAAGAGCACACGTCTGAACTCCAGTCA")
    cutadapt_runner.set_min_length(20)
    cutadapt_runner.set_overlap(3)
    cutadapt_runner.set_error_rate(0.1)
    cutadapt_runner.trim_n = True
    cutadapt_runner.discard_untrimmed = False
    

    return_code = cutadapt_runner.run()

    assert return_code == 0, "Cutadapt failed to run successfully with FASTA input"
    assert os.path.exists(output_file), "Cutadapt output file was not created"

    with open(output_file, "r") as f:
        trimmed_sequences = list(SeqIO.parse(f, "fasta"))
    assert len(trimmed_sequences) > 0, "No sequences were trimmed and written to the output"
