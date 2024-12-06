class SequenceProcessor:
    """ Class for processing sequences. """
    def __init__(self, tokenizer, genome):
        self.tokenizer = tokenizer
        self.genome = genome

    def extract_fasta_sequences(self, chromosome, start_str, end_str, desired_length=150):
        """
        Extracts a genomic sequence of a specified length from the provided chromosome coordinates.
        Standardizes chromosome names and adjusts coordinates to ensure the sequence meets the desired length.

        :param chromosome: Chromosome coordinates in hg38.
        :param start_str: Start of the sequence in bp.
        :param end_str: End of the sequence in bp.
        :param desired_length: Length of the sequence in bp.
        :return: A genomic sequence of the specified length.
        """
        start = int(start_str)
        end = int(end_str)
        chromosome = chromosome.replace('chr', '')

        if chromosome.isdigit() or chromosome.upper() in ['X', 'Y', 'MT']:
            standardized_chromosome_name = 'chr' + chromosome.upper()
        else:
            raise ValueError(f"Invalid chromosome name: {chromosome}")

        # Adjust the start and end to ensure the sequence is at least `desired_length` bp long
        if end - start < desired_length:
            mid = (start + end) // 2
            start = max(0, mid - desired_length // 2)
            end = start + desired_length

        sequence = self.genome.fetch(standardized_chromosome_name, start, end)
        return sequence.upper()

    def sequence_to_kmers(self, sequence, k=6):
        """
        Splits a string into defined kmers.
        :param sequence: String to split.
        :param k: kmer size.
        :return: List of kmers.
        """
        sequence = sequence.upper()
        return [sequence[i:i + k] for i in range(len(sequence) - k + 1)]

    def kmers_to_tokens(self, kmers, max_length=15):
        """
        Converts kmers into tokens using DNABERT.
        :param kmers: List of kmers.
        :param max_length: Max length of tokens.
        :return: List of tokens.
        """
        kmers = [kmer if 'N' not in kmer else '0' for kmer in kmers]
        tokens = self.tokenizer.convert_tokens_to_ids(kmers)
        if len(tokens) < max_length:
            tokens += [0] * (max_length - len(tokens))
        return tokens[:max_length]
