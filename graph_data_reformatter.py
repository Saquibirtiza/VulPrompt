import os
import re
from collections import defaultdict
import numpy as np
from torch_geometric.data import Data
import torch
import sent2vec
import re
import random

# Set ratio of vulnerable class between 0 and 1
ratio = 1
trained_model_path = "./data_model.bin"
global sent2vec_model
sent2vec_model = sent2vec.Sent2vecModel()
sent2vec_model.load_model(trained_model_path)

def sentence_embedding(sentence):
    emb = sent2vec_model.embed_sentence(sentence)
    return emb[0]


classlabels = ["Vul", "No-Vul"]
lst_data = []

for classlabel in classlabels:
  path = "./reveal_pdgs/"+classlabel
  dir_list = os.listdir(path)

  if classlabel == "Vul":
    label = 1
  else:
    label = 0
    ratio = 1

  filecount = 0
  for filename in dir_list:
    print(filecount)
    num_instance = int(len(dir_list) * ratio)

    if filecount >= num_instance:
      break
    if ".dot" in filename:
      filecontent = open("./reveal_pdgs/"+str(classlabel)+"/"+filename,"r")
      nodecount = 0
      iddict = defaultdict(int)
      edges_x = []
      edges_y = []
      line_vec_lst = []
      for line in filecontent.readlines():
        if "->" in line:
          #for lines with edge information
          splittedline = line.strip().split("\"")
          edges_x.append(iddict[splittedline[1]])
          edges_y.append(iddict[splittedline[3]])


        else:
          #for lines with node information
          splittedline = line.strip().split("\"")
          if "digraph" in splittedline[0] or len(splittedline) < 2:
            continue
          iddict[splittedline[1]] = nodecount
          # print(re.findall('<.*>', splittedline[2]))
          line_vec = sentence_embedding(re.findall('<.*>', splittedline[2])[0])

          lv = [float(i) for i in line_vec]
          line_vec_lst.append(lv)
          nodecount += 1

      temp = torch.tensor(np.array([edges_x, edges_y]))
      data_temp = Data(edge_index=temp, y=torch.tensor([label]), x=torch.tensor(line_vec_lst), f=str(filename))
      lst_data.append(data_temp)

      filecount += 1


seed = 1314
random.seed(seed)
random.shuffle(lst_data)

with open("./reveal_data/DS_graph_indicator.txt","w") as gindicator:
  with open("./reveal_data/DS_node_indicator.txt","w") as nindicator:
    with open("./reveal_data/DS_graph_label.txt","w") as glabel:
      with open("./reveal_data/DS_A.txt","w") as adj:
        with open("./reveal_data/DS_filename_map.txt","w") as fname:
          graph_num = 1
          node_num = 1

          for data in lst_data:
            label = int(data.y + 1)
            label = str(label)+"\n"
            glabel.write(label)
            fname.write(str(data.f)+'\n')

            for feature in data.x:
              gindicator.write(str(graph_num)+'\n')
              line_vec = np.array(feature)
              np.savetxt(nindicator, line_vec, fmt="%1.3f", newline=", ")
              nindicator.write("\n")

            for idx, startnode in enumerate(data.edge_index[0]):
              adj.write(str(int(np.array(startnode))+node_num)+","+str(int(np.array(data.edge_index[1][idx]))+node_num)+"\n")

            node_num += len(data.x)
            graph_num += 1