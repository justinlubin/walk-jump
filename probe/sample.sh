  /usr/bin/time -p -o "probe/sampletimes/sampletime-data-$1-sigma-$2_$3.txt" \
    walkjump_sample \
      model.checkpoint_path="../wj-checkpoints/data-$1-sigma-$2_$3.ckpt" \
      designs.output_csv="probe/samples/data-$1-sigma-$2_$3.csv" \
