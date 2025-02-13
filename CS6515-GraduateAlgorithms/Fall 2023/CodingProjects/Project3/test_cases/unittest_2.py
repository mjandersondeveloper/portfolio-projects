from mst import unionFind

def test_creation():
    uf = unionFind(10)
    assert uf.pi == [0,1,2,3,4,5,6,7,8,9]
    assert uf.rank == [0,0,0,0,0,0,0,0,0,0]


def test_basic_union():
    uf = unionFind(2)
    uf.union(0,1)
    assert (uf.pi == [1,1] and uf.rank == [0,1]) or (uf.pi == [0,0] and uf.rank == [1,0])
    assert uf.find(0) == uf.find(1)


def test_big_union_find():
    uf = unionFind(10)
    uf.union(0,1)
    uf.union(2,3)
    uf.union(4,5)
    uf.union(6,7)
    uf.union(8,9)
    uf.union(0,2)
    uf.union(4,6)
    uf.union(8,0)
    # Disjoint sets
    # 0, 1, 2, 3, 8, 9
    # 4, 5, 6, 7
    assert uf.find(0) == uf.find(1) == uf.find(2) == uf.find(3) == uf.find(8) == uf.find(9)
    assert uf.find(4) == uf.find(5) == uf.find(6) == uf.find(7)
    assert uf.find(0) != uf.find(4)