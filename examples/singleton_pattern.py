#!/usr/bin/env python3
"""
Python 单例模式 - 多种实现方式
Singleton Pattern - Multiple Implementation Approaches
"""

# ============================================================================
# 方法1: 使用装饰器实现单例模式 (推荐 - 最简洁)
# ============================================================================

def singleton(cls):
    """单例装饰器"""
    instances = {}

    def get_instance(*args, **kwargs):
        if cls not in instances:
            instances[cls] = cls(*args, **kwargs)
        return instances[cls]

    return get_instance


@singleton
class DatabaseConnection1:
    """使用装饰器实现的单例类"""

    def __init__(self):
        self.connection = None
        print("初始化数据库连接...")

    def connect(self):
        self.connection = "Connected to Database"
        return self.connection


# ============================================================================
# 方法2: 使用元类实现单例模式 (最pythonic)
# ============================================================================

class SingletonMeta(type):
    """单例元类"""
    _instances = {}

    def __call__(cls, *args, **kwargs):
        if cls not in cls._instances:
            cls._instances[cls] = super().__call__(*args, **kwargs)
        return cls._instances[cls]


class DatabaseConnection2(metaclass=SingletonMeta):
    """使用元类实现的单例类"""

    def __init__(self):
        self.connection = None
        print("初始化数据库连接 (元类方式)...")

    def connect(self):
        self.connection = "Connected to Database"
        return self.connection


# ============================================================================
# 方法3: 使用类方法实现单例模式 (最灵活)
# ============================================================================

class DatabaseConnection3:
    """使用类方法实现的单例类"""

    _instance = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
            cls._instance._initialized = False
        return cls._instance

    def __init__(self):
        if not self._initialized:
            self.connection = None
            print("初始化数据库连接 (__new__ 方式)...")
            self._initialized = True

    def connect(self):
        self.connection = "Connected to Database"
        return self.connection


# ============================================================================
# 方法4: 模块级单例 (最简单)
# ============================================================================

class _DatabaseConnection:
    """模块级单例内部类"""

    def __init__(self):
        self.connection = None
        print("初始化数据库连接 (模块级)...")

    def connect(self):
        self.connection = "Connected to Database"
        return self.connection


# 在模块级别创建唯一实例
database_connection = _DatabaseConnection()


# ============================================================================
# 方法5: 线程安全的单例模式 (多线程环境)
# ============================================================================

import threading


class ThreadSafeSingleton:
    """线程安全的单例类"""

    _instance = None
    _lock = threading.Lock()

    def __new__(cls):
        if cls._instance is None:
            with cls._lock:
                if cls._instance is None:
                    cls._instance = super().__new__(cls)
                    cls._instance._initialized = False
        return cls._instance

    def __init__(self):
        if not self._initialized:
            self.connection = None
            print("初始化线程安全的数据库连接...")
            self._initialized = True

    def connect(self):
        self.connection = "Connected to Database"
        return self.connection


# ============================================================================
# 使用示例和测试
# ============================================================================

if __name__ == "__main__":
    print("=" * 60)
    print("Python 单例模式演示")
    print("=" * 60)

    # 测试方法1: 装饰器
    print("\n【方法1: 装饰器实现】")
    db1_a = DatabaseConnection1()
    db1_b = DatabaseConnection1()
    print(f"db1_a is db1_b: {db1_a is db1_b}")  # True
    print(f"连接: {db1_a.connect()}")

    # 测试方法2: 元类
    print("\n【方法2: 元类实现】")
    db2_a = DatabaseConnection2()
    db2_b = DatabaseConnection2()
    print(f"db2_a is db2_b: {db2_a is db2_b}")  # True
    print(f"连接: {db2_a.connect()}")

    # 测试方法3: __new__
    print("\n【方法3: __new__ 实现】")
    db3_a = DatabaseConnection3()
    db3_b = DatabaseConnection3()
    print(f"db3_a is db3_b: {db3_a is db3_b}")  # True
    print(f"连接: {db3_a.connect()}")

    # 测试方法4: 模块级单例
    print("\n【方法4: 模块级单例】")
    print(f"连接: {database_connection.connect()}")

    # 测试方法5: 线程安全
    print("\n【方法5: 线程安全单例】")
    ts_a = ThreadSafeSingleton()
    ts_b = ThreadSafeSingleton()
    print(f"ts_a is ts_b: {ts_a is ts_b}")  # True
    print(f"连接: {ts_a.connect()}")

    # 性能对比
    print("\n" + "=" * 60)
    print("性能对比 (创建1000个实例)")
    print("=" * 60)

    import time

    # 方法1
    start = time.time()
    for _ in range(1000):
        DatabaseConnection1()
    print(f"装饰器方式: {(time.time() - start) * 1000:.3f}ms")

    # 方法2
    start = time.time()
    for _ in range(1000):
        DatabaseConnection2()
    print(f"元类方式: {(time.time() - start) * 1000:.3f}ms")

    # 方法3
    start = time.time()
    for _ in range(1000):
        DatabaseConnection3()
    print(f"__new__方式: {(time.time() - start) * 1000:.3f}ms")

    # 方法5
    start = time.time()
    for _ in range(1000):
        ThreadSafeSingleton()
    print(f"线程安全方式: {(time.time() - start) * 1000:.3f}ms")

    print("\n" + "=" * 60)
    print("✓ 所有单例模式实现演示完成！")
    print("=" * 60)
