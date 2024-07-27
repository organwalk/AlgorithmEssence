# 一次性密码本加密方案
# 将原始 str 以字节形式表示的 int 与一个随机生成且位长相同的 int（由 random_key()生成）进行异或操作
# 返回的密钥对就是假数据和加密结果
from secrets import token_bytes
from typing import Tuple


# 生成随机密钥
def random_key(length: int) -> int:
    tb: bytes = token_bytes(length)
    return int.from_bytes(tb, "big")  # 大端整数


# 加密
def encrypt(original: str) -> Tuple[int, int]:
    original_bytes: bytes = original.encode()  # 原始内容转为字节序列
    dummy: int = random_key(len(original_bytes))  # 生成与原始内容长度相等的随机密钥
    original_key = int.from_bytes(original_bytes, "big")  # 原始字节序列化为大端整数
    encrypted: int = original_key ^ dummy
    return dummy, encrypted


def decrypt(i_dummy: int, i_encrypted: int) -> str:
    decrypted: int = i_dummy ^ i_encrypted
    temp: bytes = decrypted.to_bytes((decrypted.bit_length() + 7) // 8, "big")
    return temp.decode()


if __name__ == "__main__":
    res_dummy, res_encrypted = encrypt("Hello World!")
    result: str = decrypt(res_dummy, res_encrypted)
    print(result)
