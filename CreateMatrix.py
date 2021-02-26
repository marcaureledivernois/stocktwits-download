import os
import json
import numpy as np
import pandas as pd
import progressbar
from nltk.tokenize import word_tokenize
import string
import re


def CreateMatrix(folder_list, dir_path = os.path.join('C:\\Users', 'divernoi', 'Dropbox', 'JSON')):
    bar = progressbar.ProgressBar(maxval=len(folder_list), \
        widgets=[progressbar.Bar('=', '[', ']'), ' ', progressbar.Percentage()])
    bar.start()
    data_mat = []
    for folder in folder_list:
        file_list = os.listdir(os.path.join(dir_path,folder))
        file_list = [file for file in file_list if file[-4:] == ".txt"]
        if not not file_list:
            for file in file_list:
                if file[-4:] in (".txt"):
                    with open(os.path.join(dir_path,folder,file), encoding="utf8") as json_file:
                        json_Data = json.load(json_file)
                        for i in range(0,len(json_Data['messages'])):
                            data_mat.append([folder,
                                             json_Data['messages'][i]['id'],
                                             json_Data['messages'][i]['body'],
                                             json_Data['messages'][i]['created_at'],
                                             json_Data['messages'][i]['entities']['sentiment'],
                                             json_Data['messages'][i]['user']['id'],
                                             json_Data['messages'][i]['user']['followers'],
                                             json_Data['messages'][i]['user']['ideas']
                                             ])
        bar.update(folder_list.index(folder) + 1)
    bar.finish()
    return data_mat
