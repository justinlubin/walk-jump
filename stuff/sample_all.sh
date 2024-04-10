for filename in ../wj-checkpoints/*.ckpt; do
  bn=$(basename $filename)
  label="${bn%.*}"
  walkjump_sample \
    "model.checkpoint_path=../wj-checkpoints/${label}.ckpt" \
    "designs.output_csv=stuff/samples/${label}.csv" \
    "++designs.limit_seeds=$1"
done
