import os
import mmap
import time
from concurrent.futures import ThreadPoolExecutor
from Crypto.Cipher import AES, PKCS1_OAEP
from Crypto.PublicKey import RSA
from tqdm import tqdm
import warnings

# 用于引发警告的警告模块
class ModeWarning(Warning):
    pass

def warning(message):
    warnings.warn(message, ModeWarning)

# 自定义的文件错误异常
class FileError(Exception):
    def __init__(self, message):
        self.message = message

    def __str__(self):
        return self.message

# 删除重复文件的模块
def remove_duplicate_file(backpath, show_feedback):
    if not show_feedback:
        os.remove(backpath)
    else:
        none = True
        while none:
            check = str(input('输出文件已存在，是否删除它 (Y/N)\n'))
            if check == 'Y' or check == 'y':
                os.remove(backpath)
                print('删除完成')
                none = False
            elif check == 'N' or check == 'n':
                none = False
                raise FileError('重复文件')
            else:
                print('未知输入值')

# 生成RSA密钥对的模块
def generate_rsa_keypair_file(priv_file, pub_file, show_feedback):
    if os.path.exists(priv_file):
        remove_duplicate_file(priv_file, show_feedback)
    if os.path.exists(pub_file):
        remove_duplicate_file(pub_file, show_feedback)
    key = RSA.generate(2048)
    private_key = key.export_key()
    public_key = key.publickey().export_key()
    with open(priv_file, 'w') as pvk, open(pub_file, 'w') as puk:
        pvk.write(private_key)
        puk.write(public_key)
    if show_feedback:
        print(f'生成成功，私钥保存至 {priv_file}，公钥保存至 {pub_file}')

# 混合加密模块
def rsa_aes_encrypt(file_path, backpath, rsa_cipher, show_feedback):
    with open(file_path, 'rb') as r, open(backpath, 'wb') as wr:
        with mmap.mmap(r.fileno(), length=0, access=mmap.ACCESS_READ) as mmapped_file:
            data = mmapped_file.read()
            aes_key = os.urandom(32)
            enc_aes_key = rsa_cipher.encrypt(aes_key)
            cipher = AES.new(aes_key, AES.MODE_EAX)
            ciphertext, tag = cipher.encrypt_and_digest(data)
            wr.write(enc_aes_key + cipher.nonce + tag + ciphertext)
    if show_feedback:
        print(f'加密完成，加密文件保存在：{backpath}')

# 混合解密模块
def rsa_aes_decrypt(file_path, backpath, rsa_cipher, show_feedback):
    with open(file_path, 'rb') as r, open(backpath, 'wb') as wr:
        with mmap.mmap(r.fileno(), length=0, access=mmap.ACCESS_READ) as mmapped_file:
            enc_aes_key = mmapped_file.read(256)
            ciphertext = mmapped_file.read()
            aes_key = rsa_cipher.decrypt(enc_aes_key)
            nonce = ciphertext[:16]
            tag = ciphertext[16:32]
            enc_data = ciphertext[32:]
            cipher = AES.new(aes_key, AES.MODE_EAX, nonce)
            data = cipher.decrypt_and_verify(enc_data, tag)
            wr.write(data)
    if show_feedback:
        print(f'解密完成，解密后的文件保存在：{backpath}')

# 纯RSA加密模块
def rsa_encrypt(file_path, backpath, cipher, use_multithreading, show_progress, show_feedback):
    warning("不考虑文件大小和必要性盲目使用纯RSA加密是愚蠢的。尽管纯RSA非常安全，但也非常低效。")
    chunk_size = 200
    results = {}
    if show_feedback:
        print(f'开始加密，请稍候。')
    t = time.time()
    file_size = os.path.getsize(file_path)
    pbar = None
    if show_progress:
        pbar = tqdm(total=file_size, unit='B', unit_scale=True)

    def func(i, cipher, data, results):
        encrypted_data = cipher.encrypt(data)
        results[i] = encrypted_data
        if show_progress:
            pbar.update(len(data))

    with open(file_path, 'rb') as read_file, open(backpath, 'ab') as write_file:
        with mmap.mmap(read_file.fileno(), length=0, access=mmap.ACCESS_READ) as read_mmap:
            if use_multithreading:
                executor = ThreadPoolExecutor(max_workers=None)
            else:
                executor = None

            def threaded(i):
                offset = i * chunk_size
                data = read_mmap[offset:offset + chunk_size]
                func(i, cipher, data, results)

            for i in range(file_size // chunk_size + 1):
                if use_multithreading:
                    executor.submit(threaded, i)
                else:
                    threaded(i)

            if use_multithreading:
                executor.shutdown(wait=True)

        for i in range(file_size // chunk_size + 1):
            if i in results:
                data = results[i]
                if data:
                    write_file.write(data)

    if pbar:
        pbar.close()
    spendtime = time.time() - t
    if show_feedback:
        print(f'加密完成，耗时：{spendtime:.2f}秒。加密后的文件保存在：{backpath}')

# 纯RSA解密模块
def rsa_decrypt(file_path, backpath, cipher, use_multithreading, show_progress, show_feedback):
    warning("不考虑文件大小和必要性盲目使用纯RSA加密是愚蠢的。尽管纯RSA非常安全，但也非常低效。")
    chunk_size = 256
    results = {}
    if show_feedback:
        print(f'开始解密，请稍候。')
    t = time.time()
    file_size = os.path.getsize(file_path)
    pbar = None
    if show_progress:
        pbar = tqdm(total=file_size, unit='B', unit_scale=True)

    def func(i, cipher, data, results):
        encrypted_data = cipher.decrypt(data)
        results[i] = encrypted_data
        if show_progress:
            pbar.update(len(data))

    with open(file_path, 'rb') as read_file, open(backpath, 'ab') as write_file:
        with mmap.mmap(read_file.fileno(), length=0, access=mmap.ACCESS_READ) as read_mmap:
            if use_multithreading:
                executor = ThreadPoolExecutor(max_workers=None)
            else:
                executor = None

            def threaded(i):
                offset = i * chunk_size
                data = read_mmap[offset:offset + chunk_size]
                func(i, cipher, data, results)

            for i in range(file_size // chunk_size + 1):
                if use_multithreading:
                    executor.submit(threaded, i)
                else:
                    threaded(i)

            if use_multithreading:
                executor.shutdown(wait=True)

        for i in range(file_size // chunk_size + 1):
            if i in results:
                data = results[i]
                if data:
                    write_file.write(data)

    if pbar:
        pbar.close()
    spendtime = time.time() - t
    if show_feedback:
        print(f'解密完成，耗时：{spendtime:.2f}秒。解密后的文件保存在：{backpath}')

# 函数调度器
def process_file(file_path: str, key_path: str, backpath: str,
                 enc: bool, aes: bool,
                 use_multithreading: bool, show_progress: bool, show_feedback: bool):
    with open(key_path, 'r') as key_file:
        key_data = key_file.read()

    rsa_key = RSA.import_key(key_data)
    cipher = PKCS1_OAEP.new(rsa_key)

    if os.path.exists(backpath):
        remove_duplicate_file(backpath, show_feedback)

    if not os.path.exists(key_path):
        raise FileError('密钥文件不存在')

    if aes:
        if enc:
            rsa_aes_encrypt(file_path, backpath, cipher, show_feedback)
        else:
            rsa_aes_decrypt(file_path, backpath, cipher, show_feedback)
    else:
        if enc:
            rsa_encrypt(file_path, backpath, cipher, use_multithreading, show_progress, show_feedback)
        else:
            rsa_decrypt(file_path, backpath, cipher, use_multithreading, show_progress, show_feedback)


# 以下是指南部分

def generate_rsa_keypair(priv_file, pub_file, show_feedback: bool = True):
    """
    生成密钥对，并把私钥和公钥写入文件.

    Args:
        priv_file: 私钥保存的文件路径。
        pub_file: 公钥保存的文件路径。
        show_feedback: (可选) 是否显示反馈信息。默认为True。
    """
    generate_rsa_keypair_file(priv_file, pub_file, show_feedback)


def rsa_aes_encrypt_file(file_path: str, key_path: str, backpath: str,
                         show_feedback: bool = True):
    """
    使用混合RSA-AES加密方案加密文件。

    Args:
        file_path: 要加密的文件路径。
        key_path: RSA密钥文件路径。
        backpath: 保存加密文件的路径。
        show_feedback: (可选) 是否显示反馈信息。默认为True。
    """
    enc = True
    aes = True
    process_file(file_path, key_path, backpath, enc, aes,
                 False, False, show_feedback)


def rsa_aes_decrypt_file(file_path: str, key_path: str, backpath: str,
                         show_feedback: bool = True):
    """
    使用混合RSA-AES加密方案解密文件。

    Args:
        file_path: 加密文件的路径。
        key_path: RSA密钥文件的路径。
        backpath: 保存解密文件的路径。
        show_feedback: (可选) 是否显示反馈信息。默认为True。
    """
    enc = False
    aes = True
    process_file(file_path, key_path, backpath, enc, aes,
                 False, False, show_feedback)


def rsa_encrypt_file(file_path: str, key_path: str, backpath: str,
                     use_multithreading: bool = True, show_progress: bool = True,
                     show_feedback: bool = True):
    """
    使用纯RSA加密方案加密文件。

    Args:
        file_path: 要加密的文件路径。
        key_path: RSA密钥文件路径。
        backpath: 保存加密文件的路径。
        use_multithreading: (可选) 是否使用多线程进行加密。默认为True。
        show_progress: (可选) 是否显示进度条。默认为True。
        show_feedback: (可选) 是否显示反馈信息。默认为True。
    """
    enc = True
    aes = False
    process_file(file_path, key_path, backpath, enc, aes,
                 use_multithreading, show_progress, show_feedback)


def rsa_decrypt_file(file_path: str, key_path: str, backpath: str,
                     use_multithreading: bool = True, show_progress: bool = True,
                     show_feedback: bool = True):
    """
    使用纯RSA加密方案解密文件。

    Args:
        file_path: 加密文件的路径。
        key_path: RSA密钥文件的路径。
        backpath: 保存解密文件的路径。
        use_multithreading: (可选) 是否使用多线程进行解密。默认为True。
        show_progress: (可选) 是否显示进度条。默认为True。
        show_feedback: (可选) 是否显示反馈信息。默认为True。
    """
    enc = False
    aes = False
    process_file(file_path, key_path, backpath, enc, aes,
                 use_multithreading, show_progress, show_feedback)
