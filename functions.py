import pandas as pd
import csv
import openai
import subprocess

from openai import OpenAI
client = openai.OpenAI(
    api_key = "COPY-API-KEY-HERE"
)

def zero_shot_predict(protein_name):
    try:
        sequence = ''
        with open(protein_name + '.fasta', 'r') as file:
            for line in file:
                if not line.startswith(">"):
                    sequence += line.strip()
        subprocess.run(['python', 'predict.py', 
                        '--model-location', 'esm2_t36_3B_UR50D', 
                        '--sequence', sequence,
                        '--dms-input', protein_name + '.csv',
                        '--mutation-col', 'mutant',
                        '--dms-output', protein_name + '_esm.csv',
                        '--offset-idx', '1',
                        '--scoring-strategy', 'masked-marginals'])
    
    except ValueError:
        return "zero-shot prediction failed error"

if __name__ == "__main__":
    zero_shot_predict('AtHMT')