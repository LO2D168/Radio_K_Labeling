from scipy.io import mmread
import networkx as nx
import os
def read_mtx_to_adj(filename):
    base_dir = os.path.dirname(os.path.abspath(__file__))

    mtx_path = os.path.join(base_dir, '../..', '..', 'dataset', filename)
    mtx_path = os.path.normpath(mtx_path)
    try:
        A = mmread(mtx_path).tocoo()
    except Exception as e:
        print("Lỗi đọc file .mtx:", e)
        return 0, 0, []


    G = nx.Graph()
    G.add_edges_from(zip(A.row, A.col))
    G.remove_edges_from(nx.selfloop_edges(G))
    G = nx.convert_node_labels_to_integers(G)

    n = G.number_of_nodes()

    adj = [[] for _ in range(n + 1)]
    for u, v in G.edges():
        adj[u + 1].append(v + 1)
        adj[v + 1].append(u + 1)
    return n, G.number_of_edges(), adj