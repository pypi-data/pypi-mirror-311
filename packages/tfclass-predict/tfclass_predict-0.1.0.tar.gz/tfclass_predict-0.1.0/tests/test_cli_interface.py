from src.tfclass_predict import cli_interface
import numpy as np
from os.path import join

bed_file = 'tests/GSM6915056_P1_summits_100.bed'  # smaller bed file for testing
genome_file = "hg38.fa"
tfclass_model = "model/Classlevel.h5"
bert_model = "model/6-new-12w-0"
res_dir_kmers = "tests/temp_kmers"
res_dir = "tests/temp_kmers"
col3 = 'tests/3col.bed'
window_size = 20
stride_length = 15
num_cpus = 2


def test_parser():
    """ Tests if the CLI parses the input correctly. """
    parser = cli_interface.create_parser()

    args = parser.parse_args([bed_file, genome_file, tfclass_model, bert_model, res_dir, '--window_size', str(window_size), '--stride_length', str(stride_length)])

    assert args.bed_file == bed_file
    assert args.hg_file == genome_file
    assert args.tfclass_model == tfclass_model
    assert args.dnabert == bert_model
    assert args.output_dir == res_dir
    assert args.num_cpus == num_cpus
    assert args.window_size == window_size
    assert args.stride_length == stride_length


def test_run_ATAC():
    """ Tests if the CLI returns the expected result for the classlevel model. """

    expected_cv = np.load("tests/res/GSM6915056_P1_summits_100_kmer_counts_CLASSLEVEL.npy")

    parser = cli_interface.create_parser()
    args = parser.parse_args([bed_file, genome_file, tfclass_model, bert_model, res_dir_kmers, "--stride_length", '15'])
    cli_interface.run(args)

    observed = np.load(join(res_dir, "GSM6915056_P1_summits_100_counts_CLASSLEVEL.npy"))

    assert np.all(expected_cv == observed)


def test_run_BED():
    """ Tests if the CLI returns the expected result for the classlevel model. """

    expected_cv = np.load("tests/res/3col_counts_kmer_CLASSLEVEL.npy")

    parser = cli_interface.create_parser()
    args = parser.parse_args([col3, genome_file, tfclass_model, bert_model, res_dir_kmers,  "--stride_length", '15'])
    cli_interface.run(args)

    observed = np.load(join(res_dir, "3col_counts_CLASSLEVEL.npy"))

    assert np.all(expected_cv == observed)

def test_run_sliding_ATAC():
    """ Tests if the CLI returns the expected result for the classlevel model. """

    expected_cv = np.load("tests/res/GSM6915056_P1_summits_100_counts_CLASSLEVEL.npy")

    parser = cli_interface.create_parser()
    args = parser.parse_args([bed_file, genome_file, tfclass_model, bert_model, res_dir])
    cli_interface.run(args)

    observed = np.load(join(res_dir, "GSM6915056_P1_summits_100_counts_CLASSLEVEL.npy"))

    assert np.all(expected_cv == observed)


def test_run_sliding_BED():
    """ Tests if the CLI returns the expected result for the classlevel model. """

    expected_cv = np.load("tests/res/3col_counts_CLASSLEVEL.npy")

    parser = cli_interface.create_parser()
    args = parser.parse_args([col3, genome_file, tfclass_model, bert_model, res_dir])
    cli_interface.run(args)

    observed = np.load(join(res_dir, "3col_counts_CLASSLEVEL.npy"))

    assert np.all(expected_cv == observed)