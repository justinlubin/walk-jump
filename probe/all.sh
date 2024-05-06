if [ "$1" != "train" ] && [ "$1" != "sample" ]; then
  echo "error: first argument must be either 'train' or 'sample'"
  exit 1
fi

bash probe/$1.sh 0_0001 0 1
bash probe/$1.sh 0_001 0 1
bash probe/$1.sh 0_01 0 1
bash probe/$1.sh 0_1 0 1
bash probe/$1.sh 0_33 0 1
bash probe/$1.sh 0_5 0 1
bash probe/$1.sh 1 0 1

bash probe/$1.sh 0_0001 0 3
bash probe/$1.sh 0_001 0 3
bash probe/$1.sh 0_01 0 3
bash probe/$1.sh 0_1 0 3
bash probe/$1.sh 0_33 0 3
bash probe/$1.sh 0_5 0 3
bash probe/$1.sh 1 0 3

bash probe/$1.sh 0_0001 0 5
bash probe/$1.sh 0_001 0 5
bash probe/$1.sh 0_01 0 5
bash probe/$1.sh 0_1 0 5
bash probe/$1.sh 0_33 0 5
bash probe/$1.sh 0_5 0 5
bash probe/$1.sh 1 0 5

bash probe/$1.sh 0_0001 0 7
bash probe/$1.sh 0_001 0 7
bash probe/$1.sh 0_01 0 7
bash probe/$1.sh 0_1 0 7
bash probe/$1.sh 0_33 0 7
bash probe/$1.sh 0_5 0 7
bash probe/$1.sh 1 0 7

bash probe/$1.sh 0_0001 0 9
bash probe/$1.sh 0_001 0 9
bash probe/$1.sh 0_01 0 9
bash probe/$1.sh 0_1 0 9
bash probe/$1.sh 0_33 0 9
bash probe/$1.sh 0_5 0 9
bash probe/$1.sh 1 0 9
