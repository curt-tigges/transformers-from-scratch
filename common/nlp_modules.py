import torch as t
from torch.utils.data import Dataset
import numpy as np

class WordsDataset(Dataset):
    def __init__(self, seq_len, filename, tokenizer, truncate=None):
        self.seq_len = seq_len
        self.filename = filename
        
        with open(filename, 'r') as textfile:
            text = textfile.read()
        
        tokenizer.build_dict(text)
        self.tokens = tokenizer.encode(text)
        
        word_count = len(self.tokens)

        if truncate:
            word_count = int(word_count * truncate)

        self.x_seqs, self.y_seqs = [], []
        
        for pos in range(0, word_count - seq_len - 1):
            self.x_seqs.append(t.tensor(self.tokens[pos:pos+self.seq_len]))
            self.y_seqs.append(t.tensor(self.tokens[pos+1:pos+self.seq_len+1]))
        self.x_seqs = t.stack(self.x_seqs)
        self.y_seqs = t.stack(self.y_seqs)

    def __len__(self):
        return len(self.x_seqs)

    def __getitem__(self, idx):
        return self.x_seqs[idx], self.y_seqs[idx]


from typing import Optional, Union
import re

class WordsTokenizer():
    model_max_length: int

    def __init__(self, model_max_length):
        self.word_id_map = dict()
        self.id_word_map = dict()
        self.model_max_length = model_max_length

    def build_dict(self, initial_text):

        split_text = re.split(r"\b", initial_text)
        

        # create token id mapping
        unique_tokens = set(split_text)
        self.word_id_map = {word:id for id, word in enumerate(unique_tokens)}
        self.id_word_map = {id:word for word, id in self.word_id_map.items()}

    def encode(self, text: str, return_tensors: Optional[str] = None) -> Union[list, t.Tensor]:
        '''
        Tokenizes initial_text, then returns the token ids.

        Return type is list by default, but if return_tensors="pt" then it is returned as a tensor.
        '''
        split_text = re.split(r"\b", text)
        split_text = list(filter(None, split_text))
        
        encoded = [self.word_id_map[word] for word in split_text]

        if return_tensors == "pt":
            encoded = t.tensor(encoded)
        elif return_tensors == "np":
            encoded = np.array(encoded)
        
        return encoded 

    def decode(self, list_of_ids: Union[t.Tensor, list]) -> str:
        '''
        Converts ids to a list of tokens, then joins them into a single string.
        '''
        words = [self.id_word_map[id] for id in list_of_ids]
        return "".join(words)

    def __call__(self, initial_text: str, return_tensors: Optional[str] = None) -> Union[list, t.Tensor]:
        '''
        Returns results of self.encode.
        '''
        return self.encode(initial_text, return_tensors)