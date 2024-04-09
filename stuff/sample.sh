walkjump_sample \
  "model.checkpoint_path=../wj-checkpoints/$1.ckpt" \
  "designs.output_csv=stuff/samples/$1.csv" \
  "designs.num_samples=$2"
