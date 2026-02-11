import ctypes
import json
import time
import os
import platform


class ASignature:
    def __init__(self,):
        # 根据操作系统选择库文件
        system = platform.system().lower()
        print(system)

        if system == "linux":
            lib_filename = "libencrypt.so"
        elif system == "darwin":  # macOS
            lib_filename = "libencrypt.dylib"
        else:
            lib_filename = "libencrypt.dll"

        base_dir = os.path.dirname(os.path.abspath(__file__))
        lib_path = os.path.join(base_dir, lib_filename)

        # 检查库文件是否存在
        if not os.path.exists(lib_path):
            raise FileNotFoundError(f"加密库文件不存在: {lib_path}")

        try:
            self.lib = ctypes.CDLL(lib_path)


        except OSError as e:
            raise OSError(f"加载加密库失败: {e}")

        # 定义函数签名
        self.lib.generate_signature.argtypes = [
            ctypes.c_char_p,  # app_id
            ctypes.c_char_p,  # enterprise_code
            ctypes.c_char_p,  # app_secret
            ctypes.c_char_p,  # request_body
            ctypes.c_longlong  # timestamp
        ]
        self.lib.generate_signature.restype = ctypes.c_char_p

        self.lib.free_string.argtypes = [ctypes.c_char_p]
        self.lib.free_string.restype = None

        # 注册 hex_to_string 函数签名
        self.lib.hex_to_string.argtypes = [ctypes.c_char_p]
        self.lib.hex_to_string.restype = ctypes.c_char_p

    def generate_signature(self, credential: dict, request_body: str) -> str:
        """生成十六进制格式的签名"""
        app_id = credential.get("app_id", "")
        enterprise_code = credential.get("enterprise_code", "")
        app_secret = credential.get("app_secret", "")

        timestamp = int(time.time() * 1000)

        # 调用C函数
        result = self.lib.generate_signature(
            app_id.encode('utf-8'),
            enterprise_code.encode('utf-8'),
            app_secret.encode('utf-8'),
            request_body.encode('utf-8'),
            timestamp
        )

        # 复制结果并释放C端内存
        signature_hex = result.decode('utf-8')

        return signature_hex

    def create_signature(self, request_body: str, credential: dict={}) -> str:
        """
        该方法用于用户生成签名使用，自动从环境中加载变量信息
        """
        app_id = credential.get("app_id", os.getenv("APP_ID", ""))
        enterprise_code = credential.get("enterprise_code", os.getenv("ENTERPRISE_CODE", ""))
        app_secret = credential.get("app_secret", os.getenv("APP_SECRET", ""))

        timestamp = int(time.time() * 1000)

        # 调用C函数
        result = self.lib.generate_signature(
            app_id.encode('utf-8'),
            enterprise_code.encode('utf-8'),
            app_secret.encode('utf-8'),
            request_body.encode('utf-8'),
            timestamp
        )

        # 复制结果并释放C端内存
        signature_hex = result.decode('utf-8')

        return signature_hex

    def hex_to_string(self, hex_str: str) -> str:
        """
        将十六进制字符串转换为字符串
        """
        return self.lib.hex_to_string(hex_str.encode('utf-8')).decode("utf-8")


# 使用示例
if __name__ == "__main__":
    signature_gen = ASignature()

    credential = {
        "app_id": "your_app_id",
        "enterprise_code": "your_enterprise_code",
        "app_secret": "your_app_secret",
    }

    request_body = json.dumps({"key": "value"}, separators=(',', ':'), ensure_ascii=False)  # 示例请求体

    hex_signature = signature_gen.generate_signature(credential, request_body)
    print(f"Hex Signature: {hex_signature}")
    print(f"hex_to_string: {signature_gen.hex_to_string(hex_signature)}")

    from dotenv import load_dotenv
    load_dotenv("/Users/aiden/wrk/ad/aflow-client-python/demo/.env")
    hex_signature = signature_gen.gen_signature(request_body)
    print(f"Hex Signature: {hex_signature}")

    temp_sig='7B22656E7465727072697365436F6465223A2261666C6F775F7169776569222C226170704964223A22777837663964376232383463393065663436222C2274696D657374616D70223A313737303736393735393634392C22636970686572223A226530353464303133366132636339343366323937366232663131363236656339227D'
    print(signature_gen.hex_to_string(temp_sig))
