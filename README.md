# infer_parser
A simple script to automate the use of infer_experiment.py provided in the REsQC package.

Output of infer_experiment.py can be pipep into infer_parser or used as an argument.

Example usage:
infer_experiment -i aligment.sam -r reference.bed | ./infer_parser.py
or
./infer_parser.py infer_experiment_output.txt

Args:
    filename, output of infer_experiment, can be pipep via stdin alternativelly
    -i, --ignore_failed, ignore the failed to determine fraction
    -m, --max_failed, float fraction of maximum allowed for the failed to determine fraction. Default = 0.1
    -s, --simple, Simple output, for usage in scripts/pipelines.
