if [ -d "checkpoints/" ]; then
  echo "error: checkpoints directory already exists"
  exit 1
fi

DATA_FILE="data/poas-$1.csv.gz"

if [ ! -f "$DATA_FILE" ]; then
  echo "error: data file for percent '$1' does not exist"
  exit 2
fi

WANDB_MODE=offline \
  /usr/bin/time -p -o "probe/traintimes/traintime-data-$1-sigma-$2_$3.txt" \
    walkjump_train \
      data.csv_data_path="$DATA_FILE" \
      model.model_cfg.hyperparameters.sigma="$2.$3"

mv checkpoints/last.ckpt "../wj-checkpoints/data-$1-sigma-$2_$3.ckpt"
rm -rf checkpoints/
