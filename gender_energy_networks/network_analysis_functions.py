import pandas as pd
import numpy as np
import networkx as nx
from networkx.algorithms import bipartite, centrality, community
from condor import condor_object,bipartite_modularity,initial_community,brim,matrices,qscores,condor
import random

def network_construction(cov_matrix):
    node1 = []
    node2 = []
    value = []
    for i in cov_matrix.columns:
        for j in cov_matrix.index:
            node1.append(i)
            node2.append(j)
            value.append(cov_matrix[i][j])

    network_pd = pd.DataFrame(list(zip(node1,node2,value)),
                         columns=['Classification','Variables','Rep'])

    RepHigh0 = list(network_pd[network_pd.Rep>0][['Classification',
                              'Variables','Rep']].itertuples(index=False, name=None))

    Network = nx.Graph()
    Network.add_nodes_from(node1, bipartite=0)
    Network.add_nodes_from(node2, bipartite=1)
    Network.add_weighted_edges_from(RepHigh0)

    return [Network,node1,node2]

def colors_community(nodes, partitions):
    community_to_color = {
        0: 'blue',1: 'orange',2: 'green',
        3: 'red',4: 'yellow',5: 'purple',
        6: 'cyan'}

    color_map = list()
    n_c = np.arange(len(partitions))
    for node in nodes:
        for n in n_c:
            if node in partitions[n]:
                color_map.append(community_to_color[n])

    return color_map

def coms_from_condor(network):
    net = nx.convert_matrix.to_pandas_edgelist(network)
    co = condor_object(net)
    co = initial_community(co)
    co = brim(co)

    list_commu = list()
    n_coms = co['reg_memb'].com.unique()
    for comu in n_coms:
        N1 = co['tar_memb'][co['tar_memb'].com==comu].tar
        N2 = co['reg_memb'][co['reg_memb'].com==comu].reg
        fs = frozenset(pd.concat([N1,N2]))
        list_commu.append(fs)

    return(list_commu,co)

def community_description(community,var_class):
    node_list = list(community.nodes)
    node_df = pd.DataFrame (node_list, columns = ['nodes_community'])
    node_df.set_index('nodes_community',inplace=True)

    result = pd.concat([node_df,var_class],axis=1, join='inner')
    result.sort_values(by='Type', inplace=True)

    return result

def global_properties(Network, top_nodes, botm_nodes):
    N_nodes = len(nx.nodes(Network[0]))
    N_edges = len(nx.edges(Network[0]))
    density = round(bipartite.basic.density(Network[0],top_nodes),3)
    asortativity = round(nx.degree_assortativity_coefficient(Network[0],weight='weight'),3)
    mean_deg = round(np.mean([val for (node,val) in nx.degree(Network[0])]),3)
    mean_deg_top_nodes = round(np.mean([val for (node,val) in Network[0].degree(top_nodes)]),3)
    mean_deg_botm_nodes = round(np.mean([val for (node,val) in Network[0].degree(botm_nodes)]),3)
    mean_str = round(np.mean([val for (node,val) in nx.degree(Network[0],weight='weight')]),3)
    mean_bet_node = round(np.mean(list(bipartite.centrality.betweenness_centrality(Network[0],
                                                                                   top_nodes).values())),3)
    mean_bet_edge = round(np.mean(list(nx.algorithms.centrality.edge_betweenness_centrality(Network[0],
                                                                                            weight='weight').values())),3)
    diameter = nx.algorithms.distance_measures.diameter(Network[0])
    mean_clustering = round(np.mean(list(bipartite.cluster.clustering(Network[0]).values())),3)

    print('# Nodes:')
    print(N_nodes)
    print('\n')
    print('N_edges:')
    print(N_edges)
    print('\n')
    print('Density:')
    print(density)
    print('\n')
    print('Asortativity:')
    print(asortativity)
    print('\n')
    print('<k>:')
    print(mean_deg)
    print('\n')
    print('<k1>:')
    print(mean_deg_top_nodes)
    print('\n')
    print('<k2>:')
    print(mean_deg_botm_nodes)
    print('\n')
    print('<s>:')
    print(mean_str)
    print('\n')
    print('Mean betweenness node:')
    print(mean_bet_node)
    print('\n')
    print('Mean betweenness edge:')
    print(mean_bet_edge)
    print('\n')
    print('Diameter:')
    print(diameter)
    print('\n')
    print('Mean clustering:')
    print(mean_clustering)
    print('\n')

def Community_Detection(Network):
    N_com = list()
    mod = list()
    com_max_mod = list()
    m0 = 0
    for i in range(0,1000):
        c, co = coms_from_condor(Network[0])
        m1 = co['modularity']
        N_com.append(len(c))
        mod.append(m1)
        if m1>m0:
            com_max_mod.append([c,co])
            m0 = m1

    d = {'No Comunidades':N_com, 'Modularidad':mod}
    df_mod = pd.DataFrame(data=d)
    communities = [com_max_mod[len(com_max_mod)-1][0][i] for i in range(0,len(com_max_mod[len(com_max_mod)-1][0]))]

    return(communities,df_mod)

def df_prop_nodes(Network,yr,CH):
    node_lst = [node for (node, val) in Network[0].degree(weight='weight')]
    strenght_lst = [val for (node, val) in Network[0].degree(weight='weight')] #Strenght

    degree_lst = [val for (node, val) in Network[0].degree()] #Degree

    clustering_lst = list(bipartite.cluster.clustering(Network[0]).values())#clustering

    betweenness_lst = list(bipartite.centrality.betweenness_centrality(Network[0],CH).values()) #betweenness

    dic_prop = {'Nodo':node_lst, 'Fuerza':strenght_lst, 'Clustering':clustering_lst,
                'Betweenness':betweenness_lst, 'Grado':degree_lst}
    df_prop = pd.DataFrame(dic_prop)

    df_prop.sort_values(by='Clustering', ascending=True, inplace=True)

    df_prop['Año'] = yr

    type_lst = [val for val in df_prop['Nodo'].isin(CH)]
    df_prop['Tipo'] = type_lst
    df_prop.replace(True,'CH', inplace=True)
    df_prop.replace(False,'Variable', inplace=True)

    return(df_prop)

def Dynamic_coefficients(yr1,yr2):
    set_yr1 = set(yr1)
    set_yr2 = set(yr2)

    dif_yr1_yr2 = len(set_yr1-set_yr2)
    dif_yr2_yr1 = len(set_yr2-set_yr1)
    inter = len(set_yr1.intersection(set_yr2))
    union = len(set_yr1.union(set_yr2))

    Nuevos = round(dif_yr2_yr1/union,2)
    Permanecen = round(inter/union,2)
    Desplazados = round(dif_yr1_yr2/union,2)

    return([Nuevos,Permanecen,Desplazados])
