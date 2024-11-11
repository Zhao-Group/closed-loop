# A Generalized Platform for Artificial Intelligence-powered Autonomous Protein Engineering
This repository contains the code used in the mauscript titled: A Generalized Platform for Artificial Intelligence-powered Autonomous Protein Engineering, including the zero-shot prediction using ESM-2 and supervised learning.

## zero-shot prediction using ESM-2
ESM-2 is a transformer-based protein language model designed by Rives et al. (https://www.biorxiv.org/content/10.1101/2021.07.09.450648v1) In this work, we used the workflow implement in ESM-2 to make the prediction with the model esm2_t36_3B_UR50D. To download and make predictions using ESM-2:
```
git clone https://github.com/facebookresearch/esm
```
For our work, we used esm2_t36_3B_UR50D model with the following command:

```
python predict.py \
--model-location esm2_t36_3B_UR50D \
--sequence SEQUENCEOFPROTEIN \
--dms-input ./data/phytase.csv \
--mutation-col mutant \
--dms-output ./data/phytase.csv \
--offset-idx 0 \
--scoring-strategy masked-marginals
```

## Supervised learning
For each round of engineering, we trained a supervised prediction model based on all experimentally measured variant fitness data from current round and all rounds prior. In this work, we trained the supervised model by modifying the workflow implement by Hsu et al (https://www.nature.com/articles/s41587-021-01146-5). To access Hsu et al's repository:
```
git clone https://github.com/chloechsu/combining-evolutionary-and-assay-labelled-data
```
We modified the original training script and used the command to predict and infer the variants candidates: 

```
python src/evaluate.py phytase onehot --n_seeds=1 --n_threads=1 --n_train=-1
```

## User Interface
As an early effort, we sought to replace python command lines with natual langauage, which can be achieved by leveraging assistant API. Users can run demo.py to ask for zero-shot predictions of AtHMT for example or expand the current collection of functions. 
```
python demo.py
```
