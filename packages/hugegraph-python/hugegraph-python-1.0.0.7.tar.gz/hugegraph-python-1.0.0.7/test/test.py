from hugegraph import PHugeGraph

if __name__ == '__main__':
    client = PHugeGraph("10.21.3.10", "8080", user="admin", pwd="admin", graph="hugegraph")

    """system"""
    res = client.get_graphinfo()
    print(res)

    res = client.get_all_graphs()
    print(res)

    res = client.get_version()
    print(res)

    res = client.get_graph_config()
    print(res)

    """schema"""
    schema = client.schema()
    res = schema.getVertexLabels()
    print(res)

    """graph"""
    g = client.graph()
    res = g.getVertexById("1:tom").label
    # g.removeVertexById("1:vadas")
    print(res)
    g.close()
