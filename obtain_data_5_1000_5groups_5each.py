import csv
import matplotlib.pyplot as plt
import numpy as np
import random
import networkx as nx
from hdt import HDTDocument, IdentifierPosition

sameas = "http://www.w3.org/2002/07/owl#sameAs"
PATH_LOD = "/scratch/wbeek/data/LOD-a-lot/data.hdt"
hdt_file = HDTDocument(PATH_LOD)

sameAs_dic = {}

# path = '/Users/sw-works/Documents/backbone/sameAs_data/id2terms_0-99.csv'
path = '/home/finn/backbone_folder/SameAsEq/generate_data/closure_all/id2terms_all.csv'



def obtain_graph(list_terms):
    g = nx.Graph()
    # add these nodes in it
    g.add_nodes_from(list_terms)
    for n in list_terms:
        # print ('term = ', n)
        (triples, cardi) = hdt_file.search_triples(n, sameas, "")
        for (_,_,o) in triples:
            # print ('\to: ', o)
            if o in list_terms:
                g.add_edge(n, o)
        (triples, cardi) = hdt_file.search_triples("", sameas, n)
        for (s,_,_) in triples:
            if s in list_terms:
                g.add_edge(s, n)
    return g



def export_graph_csv (file_name, graph):
    file =  open(file_name, 'w+', newline='')
    writer = csv.writer(file)
    writer.writerow([ "SUBJECT", "OBJECT"])
    for (l, r) in graph.edges:
        writer.writerow([l, r])

def read_graph_csv(file_name):
    g = nx.Graph()
    eq_file = open(file_name, 'r')
    reader = csv.DictReader(eq_file)
    for row in reader:
        s = row["SUBJECT"]
        o = row["OBJECT"]
        g.add_edge(s, o)
    return g


with open(path) as csv_file:
    csv_reader = csv.reader(csv_file, delimiter=' ')
    count = 0
    for row in csv_reader:
        index = int(row[0])
        terms = []
        for i in range (len (row)):
            if i > 0:
                # print (index, row[i])
                terms.append(row[i])
        sameAs_dic[index] = terms
        # print ('\n')
        count += 1
        if count % 1000000 == 0:
            print (count)
        # if count > 3000000:
        #     break



# step 2:
sample_size = 5
step = (1000 - 50)/5
start = 50
# Generate the VM group
# sameAs_dic
for V in range (5): # 50 - 999, 5 groups
    collect_data_VM = []
    for k in sameAs_dic.keys():
        terms = sameAs_dic[k] # k = group_id
        terms = [ r[1:-1] for r in terms]
        # print (terms)
        VM_id = len(terms)  # an VM id
        if VM_id >= start + (V)*step and VM_id < start + (V+1)*step:
            collect_data_VM.append((k,sameAs_dic[k]))
    # select 100 randomly from them # size
    print ('size = ', len (collect_data_VM))

    Vsample = random.sample(collect_data_VM, sample_size)
    # export these 100 to a file
    for (k, terms) in Vsample:
        file_name = 'ANNit_Nodes_' + str(V) + '_' + str(k) + '.csv'
        file =  open(file_name, 'w+', newline='')
        writer = csv.writer(file)
        writer.writerow([ "Entity"])
        terms = [ r[1:-1] for r in terms]
        for t in terms:
            writer.writerow([t])
        g = obtain_graph(terms)
        # export the graph
        # nx.write_edgelist(g, export_filename)
        print ('edges: ', len (g.edges))
        print ('nodes: ', len (g.nodes))
        export_filename = 'ANNit_Edges_' + str(V) + '_' + str(k) + '_'  + str(len(g.nodes)) + '_' + str(len(g.edges)) +'.csv'
        export_graph_csv(export_filename, g)
    print ('finished exporting for ', V)
