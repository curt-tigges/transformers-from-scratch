# transformers-from-scratch
This repo contains my from-scratch implementations of three transformers:
- A basic decoder-only transformer, trained on Shakespeare's collected works
- An implementation of GPT-2, not yet trained but implemented
- An implementation of BERT, not yet trained but implemented

# Usage

## Decoder Transformer
The Shakespeare transformer can be tried out through the Gradio notebook included in the `decoder_transformer` folder (which also contains the notebook used to train the transformer). Simply run the `gradio_prototype.ipynb` file, and a Gradio window will open in the notebook (or can be opened in a browser). Enter any text and see what the Shakespeare emulation produces.

## BERT and GPT-2
Currently implementation code only is available for these transformers.

# Contents
- `common` - This folder contains my from-scratch modules for all transformers, including my implementations of multi-head attention, linear layers, etc. as well as specifications for complete models.
- `decoder_transformer` - This contains training and demo code for the decoder-only transformer trained on Shakespeare (along with trained weights).
- `bert` - This contains code to implement BERT, as well as code to compare layers and parameter counts to the official implementation and to load in the pretrained weights. TODO: Finetune the pretrained model.
- `gpt-2` - The `gpt_notebook.ipynb` file contains code to implement GPT, as well as code to compare layers and parameter counts to the official implementation and to load in the pretrained weights. TODO: Finetune the pretrained model.

# Enviroment
See the `environment.yml` file for details.