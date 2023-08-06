from mtmtool.pool import map_pool, MapPool

def test_MapPool():
    def add(a, b):
        return a + b
    pow = MapPool(add, max_workers=1, ptype="Thread")
    result = pow(10,5)
    assert result == 15

    pow = MapPool(add, max_workers=2, ptype="Thread")
    result = pow(10,5)
    result = pow(10,5)
    assert list(pow.result()) == [15, 15]

    pow = MapPool(add, max_workers=2, ptype="process")
    result = pow(10,5)
    result = pow(10,5)
    assert list(pow.result()) == [15, 15]

    pow = MapPool(add, max_workers=1, ptype="process")
    result = pow(10,5)
    assert result == 15

def test_map_pool():
    # 构造装饰器后的函数
    @map_pool(max_workers=2, pool_type="Thread")
    def add(a, b):
        return a + b
    
    # 单线程运行
    assert add(1, 2, workers=1) == 3

    # 多线程运行
    add(1, 2)
    add(1, 3)
    assert list(add.result(pool_type="Thread")) == [3, 4]

    # 多进程运行
    add(1, 2)
    add(1, 3)
    assert list(add.result(pool_type="Process")) == [3, 4]

    # 测试装饰器后的函数属性
    assert add.__name__ == "add"
    assert add.__qualname__ == "test_map_pool.<locals>.add"
    assert add.__doc__ == None
    assert add.__module__ == "test_map_pool" or add.__module__ == "__main__"

    # 测试装饰器后更改max_workers，是否生效
    add.max_workers = 1
    assert add(1, 2) == 3
    add.max_workers = 2
    add(1, 2)
    assert list(add.result(pool_type="Process")) == [3]
    add(1, 2)
    assert list(add.result(pool_type="Process")) == [3]

if __name__ == '__main__':
    test_map_pool()