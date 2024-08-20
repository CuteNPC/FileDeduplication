import sys
import os
from pathlib import Path
import hashlib
import tqdm



def get_file_hash_and_size(file_path, hash_type='sha256'):
    # 检查文件是否存在
    if not os.path.isfile(file_path):
        print(f"文件不存在: {file_path}")
        return None

    # 选择哈希类型
    hash_func = None
    if hash_type == 'md5':
        hash_func = hashlib.md5()
    elif hash_type == 'sha1':
        hash_func = hashlib.sha1()
    elif hash_type == 'sha256':
        hash_func = hashlib.sha256()
    else:
        print(f"不支持的哈希类型: {hash_type}")
        return None

    # 计算哈希值
    with open(file_path, 'rb') as file:
        while chunk := file.read(8192):
            hash_func.update(chunk)

    file_hash = hash_func.hexdigest()
    file_size = os.path.getsize(file_path)

    return (file_hash, file_size)


def main():

    if len(sys.argv) != 2:
        raise RuntimeError
    folder = str(sys.argv[1])

    if not os.path.isdir(folder):
        raise RuntimeError
    folder = Path(folder)

    dicts = dict()
    all_lists = []

    file_list = os.listdir(folder)
    for file in tqdm.tqdm(file_list):
        file_path = folder / file
        if os.path.isdir(file_path):
            continue
        key = get_file_hash_and_size(file_path)
        value = str(file_path)
        if key not in dicts.keys():
            dicts[key] = list()
        dicts[key].append(value)
        all_lists.append(value)

    def get_key(string: str):
        return (len(string), string)
    save_lists = [sorted(value, key=get_key)[0] for _, value in dicts.items()]

    remove_list = [e for e in all_lists if e not in save_lists]

    os_name = os.name
    remove_func = print
    if os_name == 'nt':
        from send2trash import send2trash
        remove_func = send2trash
    elif os_name == 'posix':
        remove_func = os.remove
    
    for elem in remove_list:
        remove_func(elem)


if __name__ == "__main__":
    sys.argv.append("D:\\下载")
    main()
