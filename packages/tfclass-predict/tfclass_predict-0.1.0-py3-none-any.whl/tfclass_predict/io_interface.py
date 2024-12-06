import csv
import os
import pysam
import numpy as np
import pandas as pd


class IOInterface:
    def __init__(self, bed_file: str, genome_file: str, res_dir: str):
        """
        Processes and validates inputs.
        :param bed_file: Path to BED file from e.g. ATAC-seq regions or any other NGS-DNA strategy.
        :param genome_file: Path to Fasta file from a recent human genome.
        :param res_dir: Path to output directory.
        """
        self.bed_file = bed_file

        _file_name = os.path.split(bed_file)[-1]
        self.file_name = os.path.splitext(_file_name)[-2]

        self.genome_file = pysam.FastaFile(genome_file)

        # Ensure the results directory exists
        if not os.path.exists(res_dir):
            os.makedirs(res_dir)
        self.res_dir = res_dir

    def read_atac_seq_data(self):
        """
        Reads ATAC-seq regions from BED file that was given in the initalizer.
        :return: BED file input as pd.DataFrame.
        """
        # Try reading the file with 'strength' column
        try:
            atac_seq_columns = ["seqnames", "start", "end", "name", "strength"]
            atac_seq_data = pd.read_csv(self.bed_file, sep='\t', usecols=[0, 1, 2, 3, 4], names=atac_seq_columns,
                                        header=None)
            atac_seq_data = atac_seq_data.loc[atac_seq_data.groupby('name')['strength'].idxmax()]
        except ValueError:
            atac_seq_columns = ["seqnames", "start", "end"]
            atac_seq_data = pd.read_csv(self.bed_file, sep='\t', usecols=[0, 1, 2], names=atac_seq_columns, header=None)
            atac_seq_data['name'] = "default_name"  # Add default 'name' column
            atac_seq_data['strength'] = 0  # Add default 'strength' column

        return atac_seq_data

    def write_predictions(self, counts_vec, pred_dict, bed_data):
        """
        Writes predictions and count vectors to output files.
        :param counts_vec: Count vectors from Predictor.predict function.
        :param pred_dict: Dictionary from Predictor.predict function.
        :param bed_data: Dataframe from BED file.
        :return:
        """
        print(self.res_dir)
        count_vectors_path = os.path.join(self.res_dir,
                                          f"{self.file_name}_counts_CLASSLEVEL.npy")
        print(count_vectors_path)
        np.save(count_vectors_path, counts_vec)

        pred_dict_path = os.path.join(self.res_dir, f"{self.file_name}_predictions.csv")
        with open(pred_dict_path, mode='w', newline='') as file:
            writer = csv.writer(file)
            writer.writerow(['Sequence Index', 'Name', 'Strength', 'Prediction Array'])
            for index, preds in pred_dict.items():
                name = bed_data.at[index, 'name'] if 'name' in bed_data.columns else "default_name"
                strength = bed_data.at[index, 'strength'] if 'strength' in bed_data.columns else 0
                for pred in preds:
                    writer.writerow([index, name, strength, *pred])


