import argparse
from .prediction_manager import PredictionManager


def entry():
    """
    Commandline interface to execute the program.
    """

    parser = create_parser()
    args = parser.parse_args()
    run(args)


def create_parser():
    parser = argparse.ArgumentParser(
        prog='tfclass_predict',
        description='tfclass_predict allows to estimate transcription factor bindingsites in the TFClass hierarchy.',
    )
    parser.add_argument('bed_file', type=str, help='Path to bed file of ATAC-seq or other NGS experiment.')
    parser.add_argument('hg_file', type=str, help='Path to human genome reference (.fa).')
    parser.add_argument('tfclass_model', type=str, help='Path to TFClass model (.h5).')
    parser.add_argument('dnabert', type=str, help='Path to DNABERT model directory.')
    parser.add_argument('output_dir', type=str, help='Path to output directory.')
    parser.add_argument("--window_size", type=int, help='Window size by which a read will be scanned.', required=False, default=15)
    parser.add_argument("--stride_length", type=int, help='Number of bp a window will be moved in each iteration.', required=False, default=1)
    parser.add_argument("--gpu_memory", type=int, help='Amount memory used per GPU.', required=False, default=None)
    parser.add_argument("--num_cpus", type=int, help='Number of cpus used.', required=False, default=2)
    parser.add_argument("--num_gpus", type=int, help='Number of gpus used.', required=False, default=0)
    parser.add_argument("--num_threads", type=int, help='Number of threads used per CPU / GPU.', required=False,
                        default=4)
    return parser


def run(args):
    tfargs = {"memory_limit": args.gpu_memory,
              "num_cpus": args.num_cpus,
              "num_gpus": args.num_gpus,
              "num_threads": args.num_threads}
    pm = PredictionManager(args.bed_file, args.hg_file, args.output_dir, args.dnabert, args.tfclass_model, tfargs)
    pm.predict(subseq_length=args.window_size, stride_length=args.stride_length)
    pm.save_results()
