import os

def complex_function(x):
    # TODO: 重构这个函数，逻辑太复杂
    if x > 10:
        print("x is large") # DEBUG PRINT
        for i in range(x):
            print(i)
    return x * 2

def insecure_function():
    # 模拟一个潜在的安全问题：硬编码凭证
    db_password = "admin_password_123"
    print(f"Connecting with {db_password}")

if __name__ == "__main__":
    complex_function(15)
