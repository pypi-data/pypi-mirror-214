#!/usr/bin/env python
import argparse
import json
import os
from glob import glob

import torch
from sentence_transformers import SentenceTransformer


def parse_args():
    parser = argparse.ArgumentParser(description='Convert JSON files to embeddings')
    parser.add_argument('--input-folder', required=True, help='The folder containing the JSON files')
    parser.add_argument('--embeddings-folder', required=True, help='The folder to save the embeddings to')
    parser.add_argument('--force', action='store_true', help='Overwrite existing embeddings')
    return parser.parse_args()


def info_chunks_to_embeddings(input_folder, embeddings_folder, force):
    # Load the transformer model
    sentence_transformer = SentenceTransformer('paraphrase-multilingual-MiniLM-L12-v2')

    # Ensure the output directory exists
    os.makedirs(embeddings_folder, exist_ok=True)

    # Get all JSON files in the input folder
    json_files = glob(os.path.join(input_folder, '*.json'))

    for json_file in json_files:
        # Construct the output file path
        base_name = os.path.basename(json_file)
        output_file = os.path.join(embeddings_folder, base_name.replace('.json', '.pt'))

        # Skip if the output file already exists and we're not using --force
        if os.path.exists(output_file) and not force:
            print(f'Skipping {json_file} because {output_file} already exists')
            continue

        # Load the JSON file
        with open(json_file, 'r') as f:
            data = json.load(f)

        # Convert the content to an embedding
        content = data['content']
        embedding = sentence_transformer.encode(content, convert_to_tensor=True)

        # Save the embedding
        torch.save(embedding, output_file)


def main():
    args = parse_args()
    info_chunks_to_embeddings(args.input_folder, args.embeddings_folder, args.force)


if __name__ == '__main__':
    main()
