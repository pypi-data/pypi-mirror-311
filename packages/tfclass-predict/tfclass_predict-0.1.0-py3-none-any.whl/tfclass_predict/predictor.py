import tensorflow as tf
from tensorflow import keras
from transformers import TFBertModel
import numpy as np

from .sequence_processor import SequenceProcessor

class ClassAUC(tf.metrics.AUC):
    """ Metric used in training steps - needs to be kept for model usage. """
    def __init__(self, name="ClassAUC", **kwargs):
        super(ClassAUC, self).__init__(name=name, **kwargs)


class Predictor:
    """ Predictor class takes care about the prediction / model execution. """
    def __init__(self, bed_data, tokenizer, model_path, genome_file):
        self.tokenizer = tokenizer
        self.bed_data = bed_data
        self.SequenceProcessor = SequenceProcessor(tokenizer, genome_file)

        self.model = self._init_model(model_path)

    def _init_model(self, model_path):
        """
        Load the TFClass model. Initializes the  TFBert model.
        :param model_path: Path to TFClass model.
        :return: Initialized TFClass model.
        """
        # Load the model with custom objects
        custom_objects = {'TFBertModel': TFBertModel, 'ClassAUC': ClassAUC}

        return keras.models.load_model(model_path, custom_objects=custom_objects)

    def predict_bed_data(self, subseq_length, stride_length, batch_size):
        """
        Processes genomic sequences from the bed_data DataFrame, extracts subsequences, converts them into tokenized k-mers,
        and uses the TFClass model to make predictions on these sequences. The predictions are aggregated and associated
        with their corresponding sequence indices.

        Workflow:
        1. Initializes lists to store aggregated predictions and their corresponding sequence indices.
        2. Iterates over each row in the bed_data DataFrame.
        3. For each row:
           - Extracts the genomic sequence based on 'seqnames', 'start', and 'end' with a desired length of 150.
           - Skips sequences that are empty or shorter than the desired length.
           - Generates subsequences from the full sequence.
           - Converts each subsequence into k-mers and then tokenizes them.
           - Accumulates tokenized sequences until the batch size is reached.
           - Uses a machine learning model to make predictions on the batch of tokenized sequences.
           - Stores the predictions and their corresponding indices in the aggregated lists.
        4. Processes any remaining sequences that did not form a complete batch.


        :param subseq_length: Length in which a read should be split into subsequences (i.e. K-mer size).
        :param stride_length: Defines the number of basepairs a window will move in the next step. (=1 sliding window, =subseq_length k_mer splits)
        :param batch_size: Number of intervals that should be processed in one batch.
        :return:
        """
        all_aggregated_predictions = []
        sequence_indices = []

        batch_sequences = []
        batch_indices = []

        for index, row in self.bed_data.iterrows():
            print(f"Processing index: {index}, row: {row.tolist()}")  # Progress indicator with row data
            full_sequence = self.SequenceProcessor.extract_fasta_sequences(row['seqnames'], row['start'], row['end'],
                                                                           150)  # Desired length is 150
            print(
                f"Full sequence: {full_sequence[:50]}... (length: {len(full_sequence)})")  # Print part of the sequence for verification
            if not full_sequence or len(full_sequence) < 150:
                print(f"Skipped: Sequence is too short.")
                continue

            for i in range(0, len(full_sequence) - subseq_length + 1, subseq_length):
                segment = full_sequence[i:i + subseq_length]
                kmers = self.SequenceProcessor.sequence_to_kmers(segment)
                tokenized_sequence = self.SequenceProcessor.kmers_to_tokens(kmers, max_length=15)
                batch_sequences.append(tokenized_sequence)
                batch_indices.append(index)

                if len(batch_sequences) == batch_size:
                    predictions = self.model.predict(np.array(batch_sequences), batch_size=batch_size)
                    for pred_index, prediction in enumerate(predictions):
                        predicted_class = (prediction > 0.5).astype(int)
                        all_aggregated_predictions.append(predicted_class)
                        sequence_indices.append(batch_indices[pred_index])
                    batch_sequences = []
                    batch_indices = []

        if batch_sequences:
            predictions = self.model.predict(np.array(batch_sequences), batch_size=len(batch_sequences))
            for pred_index, prediction in enumerate(predictions):
                predicted_class = (prediction > 0.5).astype(int)
                all_aggregated_predictions.append(predicted_class)
                sequence_indices.append(batch_indices[pred_index])

        return all_aggregated_predictions, sequence_indices
