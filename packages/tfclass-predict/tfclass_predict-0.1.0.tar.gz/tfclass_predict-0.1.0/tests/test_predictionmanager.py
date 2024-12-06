from src.tfclass_predict import *
import numpy as np

bed_file = 'tests/GSM6915056_P1_summits_100.bed'  # smaller bed file for testing
genome_file = "hg38.fa"
tfclass_model = "model/Classlevel.h5"
bert_model = "model/6-new-12w-0"
res_dir = "tests/res"
col3 = 'tests/3col.bed'


def test_predict_ATAC():
    """ Tests if the PredicitonManager returns the expected result for the classlevel model on ATAC-seq data. """

    expected_cv = np.load("tests/res/GSM6915056_P1_summits_100_kmer_counts_CLASSLEVEL.npy")
    pm = PredictionManager(bed_file=bed_file, genome_file=genome_file, tfclass_model=tfclass_model, res_dir=res_dir,
                           bert_model=bert_model)

    count_vec, pred_dict = pm.predict(batch_size=200, stride_length=15)
    assert np.all(count_vec == expected_cv)


def test_predict_BED():
    """ Tests if the PredicitonManager returns the expected result for the classlevel model on any other BED file. """

    expected_cv = np.load("tests/res/3col_counts_kmer_CLASSLEVEL.npy")
    pm = PredictionManager(bed_file=col3, genome_file=genome_file, tfclass_model=tfclass_model, res_dir=res_dir,
                           bert_model=bert_model)

    count_vec, pred_dict = pm.predict(batch_size=200, stride_length=15)
    assert np.all(count_vec == expected_cv)

def test_predict_ATAC_sliding_window():
    """ Tests if the PredicitonManager returns the expected result for the classlevel model on ATAC-seq data. """

    expected_cv = np.load("tests/res/GSM6915056_P1_summits_100_counts_CLASSLEVEL.npy")
    pm = PredictionManager(bed_file=bed_file, genome_file=genome_file, tfclass_model=tfclass_model, res_dir=res_dir,
                           bert_model=bert_model)

    count_vec, pred_dict = pm.predict(batch_size=200, stride_length=1)
    assert np.all(count_vec == expected_cv)


def test_predict_BED_sliding_window():
    """ Tests if the PredicitonManager returns the expected result for the classlevel model on any other BED file. """

    expected_cv = np.load("tests/res/3col_counts_CLASSLEVEL.npy")
    pm = PredictionManager(bed_file=col3, genome_file=genome_file, tfclass_model=tfclass_model, res_dir=res_dir,
                           bert_model=bert_model)

    count_vec, pred_dict = pm.predict(batch_size=200, stride_length=1)
    assert np.all(count_vec == expected_cv)
