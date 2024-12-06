from transformers import BertTokenizer
import tensorflow as tf
from collections import defaultdict
import numpy as np
from tensorflow.python.keras import backend as K
from .io_interface import IOInterface
from .predictor import Predictor

from .constants import NUM_CLASSES


def _generate_count_vectors(predictions, sequence_indices, num_classes=NUM_CLASSES):
    """
    Generates count vectors from prediction results.
    :param predictions: Aggregated predictions from Predictor.predict_bed_data()
    :param sequence_indices: Indices of each sequence in predictions.
    :param num_classes: Number of classes that were predicted.
    :return: Count vectors and prediction dictionary.
    """
    count_vectors = []
    predictions_dict = defaultdict(list)

    for index, pred in zip(sequence_indices, predictions):
        predictions_dict[index].append(pred.tolist())

    for index, sequence_pred in predictions_dict.items():
        count_vector = np.zeros(num_classes)
        for pred_array in sequence_pred:
            count_vector += np.array(pred_array)
        count_vectors.append(count_vector)

    return count_vectors, predictions_dict


class PredictionManager:
    """ Prediction manager class. Coordinates the prediction for a single bed file. """
    def __init__(self, bed_file, genome_file, res_dir, bert_model, tfclass_model, tfargs=None):
        """
        :param bed_file: Path to BED file cotaining at least CHROM, START, END entries.
        :param genome_file: Path to reference genome file.
        :param res_dir: Output directory.
        :param bert_model: Path to BERT model directory.
        :param tfclass_model: Path to TFClass model file.
        :param tfargs: Directory conatining arguments for TFClass. Possible keys are: num_threads, num_gpus, num_cpus, memory_limit
        """
        self.iointerface = IOInterface(bed_file, genome_file, res_dir)
        tokenizer = self._init_BERT(bert_model)

        if tfargs is not None:
            self._init_devices(tfargs["num_threads"], tfargs["num_gpus"], tfargs["num_cpus"], tfargs["memory_limit"])
        else:
            self._init_devices(1, 0, 2, None)


        self.bed_data = self.iointerface.read_atac_seq_data()
        self.predictor = Predictor(self.bed_data, tokenizer, tfclass_model, self.iointerface.genome_file)
        self.count_vec, self.pred_dict = None, None

    def _init_BERT(self, bert_model):
        """
        Initalizes the BERT tokenizer.

        :param bert_model: Path to BERT model directory.
        """
        tokenizer = BertTokenizer.from_pretrained(bert_model, local_files_only=True)
        return tokenizer

    def _init_devices(self, num_threads, num_gpus, num_cpus, memory_limit):
        """
        Initializes the devices, i.e. GPU and CPU usages.

        :param num_threads: Number of threads used.
        :param num_gpus: Number of GPUs.
        :param num_cpus: Number of CPUs.
        :param memory_limit: Memory limit per GPU.
        """
        config = tf.compat.v1.ConfigProto(intra_op_parallelism_threads=num_threads,
                                inter_op_parallelism_threads=num_threads,
                                allow_soft_placement=True,
                                device_count={'CPU': num_cpus,
                                              'GPU': num_gpus}
                                )

        session = tf.compat.v1.Session(config=config)
        K.set_session(session)

        if num_gpus >= 1:
            self._init_GPU(memory_limit)

    def _init_GPU(self, memory_limit=None):
        """ Initializes GPU usage and enables memory growth. """
        gpus = tf.config.experimental.list_physical_devices('GPU')
        for gpu in gpus:
            tf.config.experimental.set_memory_growth(gpu, True)

        if memory_limit is not None:
            gpus = tf.config.experimental.list_physical_devices('GPU')
            for gpu in gpus:
                try:
                    tf.config.experimental.set_virtual_device_configuration(gpu, [
                        tf.config.experimental.VirtualDeviceConfiguration(memory_limit=memory_limit)])
                except RuntimeError as e:
                    print(e)

    def predict(self, subseq_length=15, stride_length=1, batch_size=2000):
        """
        Start the prediction.
        :param subseq_length: Length in which a read should be split into subsequences.
        :param stride_length: Defines the number of basepairs a window will move in the next step. (=1 sliding window, =subseq_length k_mer splits)
        :param batch_size: Number of intervals that should be processed in one batch.
        :return: Count vectors and prediction dictionary.
        """

        print(f"Starting Prediction...")

        if self.count_vec is None or self.pred_dict is None:
            aggregated_predictions, sequence_indices = self.predictor.predict_bed_data(
                subseq_length=subseq_length,
                stride_length=stride_length,
                batch_size=batch_size
            )

            self.count_vec, self.pred_dict = _generate_count_vectors(aggregated_predictions, sequence_indices,
                                                                     num_classes=NUM_CLASSES)
        return self.count_vec, self.pred_dict

    def save_results(self):
        """ Saves the prediction results to disk. """
        if self.count_vec is None or self.pred_dict is None:
            ValueError("Predictions not initialized! Run 'predict' first.")
        else:
            self.iointerface.write_predictions(self.count_vec, self.pred_dict, self.bed_data)
