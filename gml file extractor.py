import igraph as ig
import os
import sys
import torch
from tqdm import tqdm
import numpy

if __name__ == "__main__":
    assert len(sys.argv) == 2
    nci1_data_path = sys.argv[1]
    nodes = list()
    node2graph = list()
    with open(os.path.join(nci1_data_path, "ENZYMES_graph_indicator.txt"), "r") as f:
        for n_id, g_id in enumerate(f):
            g_id = int(g_id) - 1
            node2graph.append(g_id)
            if g_id == len(nodes):
                nodes.append(list())
                print(n_id, g_id, len(nodes))
            elif g_id == len(nodes) + 1:
                nodes.append(list())
                nodes.append(list())
                print(n_id, g_id, len(nodes))
            nodes[-1].append(n_id)

    edges = [list() for _ in range(len(nodes))]
    with open(os.path.join(nci1_data_path, "ENZYMES_A.txt"), "r") as f:
        for e in f:
            e = [int(v) - 1 for v in e.split(",")]
            g_id = node2graph[e[0]]
            # print(g_id)
            edges[g_id].append((e[0] - nodes[g_id][0], e[1] - nodes[g_id][0]))

    graphlabels = list()
    with open(os.path.join(nci1_data_path, "ENZYMES_graph_labels.txt"), "r") as f:
        for nl in f:
            nl = int(nl)
            graphlabels.append(nl)


    nodeattr = [list() for _ in range(len(nodes))]
    with open(os.path.join(nci1_data_path, "ENZYMES_node_attributes.txt"), "r") as f:
        _nodeattr = list()
        data=f.readlines()
        for line in data:
            _nodeattr.append(line)
        '''for nl in f:
            nl = float(nl)
            _nodeattr.append(nl)'''
        n_idx = 0
        for g_idx in range(len(nodes)):
            for _ in range(len(nodes[g_idx])):
                nodeattr[g_idx].append(_nodeattr[n_idx])
                n_idx += 1
        del _nodeattr



    os.makedirs(os.path.join(nci1_data_path, "raw"), exist_ok=True)
    max_n_num = 0
    max_e_num = 0
    max_nlabel_num = 0
    classnum = 2
    node_feature_dim=128
    num_per_class = torch.zeros(classnum)
    count=torch.zeros(6)
    # counter = 0
    for g_id in tqdm(range(len(nodes))):
        graph = ig.Graph(directed=True)
        vcount = len(nodes[g_id])
        vfeature=nodeattr[g_id]
        graph.add_vertices(vcount)
        graph.add_edges(edges[g_id])
        enum=graph.ecount()
        elabels=torch.zeros(enum,dtype=int)
        elabels=elabels.numpy().tolist()
        graph["feature"]=vfeature
        graph.es["label"] = elabels
        graph.es["key"] = [0] * len(edges[g_id])
        graph["label"]=graphlabels[g_id]-1
        count[graph["label"]]+=1
        graph_id = "G_N%d_E%d_GL%d_%d" % (
            vcount, len(edges[g_id]), graph["label"], g_id)
        if vcount > max_n_num:
            max_n_num = vcount
        if len(edges[g_id]) > max_e_num:
            max_e_num = len(edges[g_id])

        filename = os.path.join(nci1_data_path, "raw", graph_id)
        graph.write(filename + ".gml")
  
    print("max_n_num: ", max_n_num)
    print("max_e_num: ", max_e_num)
    print("max_nlabel_num: ", max_nlabel_num)
    print("graph_label_num:", count)