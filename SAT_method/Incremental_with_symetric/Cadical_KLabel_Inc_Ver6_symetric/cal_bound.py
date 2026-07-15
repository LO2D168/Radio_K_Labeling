def get_k_from_filename(dist):
    valid = [d for row in dist for d in row if d >= 0]
    diam = max(valid) if valid else 0
    return diam

def get_upper_bound(filename, n, k, dist):
    fname = filename.lower()
    valid = [d for row in dist for d in row if d >= 0]
    diam = max(valid) if valid else 0
    return n*(k+1) - diam

def find_lowerbound(n, adj):
    return int(max(len(adj[ver]) for ver in range(1, n + 1)) /2)