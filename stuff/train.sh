if [ -d "checkpoints/" ]; then
  echo "checkpoints directory already exists"
  exit 1
fi

DATA_DIR="data/poas-$1.csv.gz"

if [ ! -f "$DATA_DIR" ]; then
  echo "data file for percent '$1' does not exist"
  exit 2
fi

WANDB_MODE=offline walkjump_train data.csv_data_path="$DATA_DIR"
mv checkpoints/last.ckpt "../wj-checkpoints/data-$1-sigma-0_5"
rm -rf checkpoints/
