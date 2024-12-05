"""
Created on 2022-08-10
@author:刘飞
@description: 加密python代码为pyc/pyd/so
"""

import os
import re
import shutil
import tempfile
import compileall
from setuptools import setup
from setuptools.command.build_py import build_py
from typing import Union, List
from Cython.Build import cythonize
from pyencrypt3.log import logger


def get_package_dir(*args, **kwargs):
    return ""


# 重写get_package_dir， 否者生成的so文件路径有问题
build_py.get_package_dir = get_package_dir


class TemporaryDirectory:
    """
    创建临时文件存储
    """

    def __enter__(self):
        self.name = tempfile.mkdtemp()
        return self.name

    def __exit__(self, exc_type, exc_value, traceback):
        shutil.rmtree(self.name)


def _search(content, regexp):
    """
    是否有匹配的搜索项
    """
    if isinstance(regexp, str):
        return re.search(regexp, content)

    for regex in regexp:
        if re.search(regex, content):
            return True


def walk_file(file_path):
    """
    获取文件路径
    """
    if os.path.isdir(file_path):
        for current_path, sub_folders, files_name in os.walk(file_path):
            for file in files_name:
                file_path = os.path.join(current_path, file)
                yield file_path

    else:
        yield file_path


def copy_files(src_path, dst_path):
    if os.path.isdir(src_path):
        if os.path.exists(dst_path):
            shutil.rmtree(dst_path)

        def _callable(src, names: list):
            if _search(src, dst_path):
                return names
            return ["dist", ".git", "venv", ".idea", "__pycache__"]

        shutil.copytree(src_path, dst_path, ignore=_callable)
    else:
        if not os.path.exists(dst_path):
            os.makedirs(dst_path)
        shutil.copyfile(src_path, os.path.join(dst_path, os.path.basename(src_path)))


def get_py_files(files, ignore_files: Union[List, str, None] = None):
    """
    @summary:
    ---------
    @param files: 文件列表
    @param ignore_files: 忽略的文件，支持正则
    ---------
    @result:
    """
    for file in files:
        if file.endswith(".py"):
            if ignore_files and _search(file, regexp=ignore_files):  # 该文件是忽略的文件
                pass
            else:
                yield file


def filter_cannot_encrypted_py(files, except_main_file):
    """
    过滤掉不能加密的文件，如 log.py __main__.py 以及包含 if __name__ == "__main__": 的文件
    Args:
        files:
        except_main_file:
    Returns:
    """
    _files = []
    for file in files:
        if _search(file, regexp="__.*?.py"):
            continue
        if except_main_file:
            with open(file, "r", encoding="utf-8") as f:
                content = f.read()
                if _search(content, regexp="__main__"):
                    continue
        _files.append(file)
    return _files


def encrypt_py(py_files: list):
    encrypted_py = []
    with TemporaryDirectory() as td:
        total_count = len(py_files)
        for i, py_file in enumerate(py_files):
            try:
                dir_name = os.path.dirname(py_file)
                file_name = os.path.basename(py_file)
                os.chdir(dir_name)
                logger.debug(f"正在加密 {i + 1}/{total_count},  {file_name}")
                setup(ext_modules=cythonize([file_name], quiet=True, language_level=3),
                      script_args=["build_ext", "-t", td, "--inplace"])
                encrypted_py.append(py_file)
                logger.debug(f"加密成功 {file_name}")
            except Exception as e:
                logger.exception(f"加密失败 {py_file} , error {e}")
                temp_c = py_file.replace(".py", ".c")
                if os.path.exists(temp_c):
                    os.remove(temp_c)
        return encrypted_py


def encrypt_pyc(py_files: list):
    """
    编译成pyc文件
    :param py_files:
    :return:
    """
    encrypted_py = []
    total_count = len(py_files)
    for i, py_file in enumerate(py_files):
        try:
            dir_name = os.path.dirname(py_file)
            file_name = os.path.basename(py_file)
            os.chdir(dir_name)
            logger.debug(f"正在加密 {i + 1}/{total_count},  {file_name}")
            compileall.compile_file(py_file, force=True, legacy=True)
            encrypted_py.append(py_file)
            logger.debug(f"加密成功 {file_name}")
        except Exception as e:
            logger.exception(f"加密失败 {py_file} , error {e}")
            temp_c = py_file.replace(".py", ".c")
            if os.path.exists(temp_c):
                os.remove(temp_c)
    return encrypted_py


def delete_files(files_path):
    """
    @summary: 删除文件
    ---------
    @param files_path: 文件路径 py 及 c 文件
    ---------
    @result:
    """
    # 删除python文件及c文件
    for file in files_path:
        try:
            os.remove(file)  # py文件
            os.remove(file.replace(".py", ".c"))  # c文件
        except Exception as e:
            pass
            # logger.error('删除文件报错', exc_info=True)


def rename_encrypted_file(output_file_path):
    files = walk_file(output_file_path)
    for file in files:
        if file.endswith(".pyd") or file.endswith(".so"):
            new_filename = re.sub("(.*)\..*\.(.*)", r"\1.\2", file)
            os.rename(file, new_filename)


def start_encrypt(
        input_file_path,
        output_file_path: str = None,
        ignore_files: Union[List, str, None] = None,
        except_main_file: int = 0,
        pyc: int = 0):
    """
    :param input_file_path: 待加密文件或文件夹路径，可是相对路径或绝对路径
    :param output_file_path: 加密后的文件输出路径，默认在input_file_path下创建dist文件夹，存放加密后的文件
    :param ignore_files: 不需要加密的文件或文件夹，逗号分隔
    :param except_main_file: 不加密包含__main__的文件(主文件加密后无法启动), 值为(0-加密、1-不加密)。 默认为0
    :param pyc: 默认未so或者pyd格式加密，pyc为真时编译成pyc码(1-编译为pyc)[pyc为弱加密，容易被反编译。其他形式编译不成功时，可选]
    :return:
    """
    # 参数校验
    assert input_file_path, "input_file_path cannot be null"
    assert (input_file_path != output_file_path), "output_file_path must be diffent with input_file_path"
    if output_file_path and os.path.isfile(output_file_path):
        raise ValueError("output_file_path need a dir path")

    # 路径处理
    input_file_path = os.path.abspath(input_file_path)
    if not output_file_path:  # 无输出路径
        if os.path.isdir(input_file_path):  # 如果输入路径是文件夹 则输出路径为input_file_path/dist/project_name
            output_file_path = os.path.join(input_file_path, "dist", os.path.basename(input_file_path))
        else:
            output_file_path = os.path.join(os.path.dirname(input_file_path), "dist")
    else:
        output_file_path = os.path.abspath(output_file_path)
    input_file_path = input_file_path.replace('\\', '/')  # 兼容windows
    output_file_path = output_file_path.replace('\\', '/')  # 兼容windows

    # 主逻辑处理
    # 拷贝原文件到目标文件
    copy_files(input_file_path, output_file_path)
    # 获取输出文件夹内的所有文件
    files = walk_file(output_file_path)
    # 过滤掉需要跳过的文件【用户指定】
    py_files = get_py_files(files, ignore_files)

    # 过滤掉不需要加密的文件[__xx__.py文件 或者包含__main__的py文件]
    need_encrypted_py = filter_cannot_encrypted_py(py_files, except_main_file)
    if pyc:
        # 编译成pyc文件
        encrypted_py = encrypt_pyc(need_encrypted_py)
    else:
        # 文件加密
        encrypted_py = encrypt_py(need_encrypted_py)

    delete_files(encrypted_py)
    rename_encrypted_file(output_file_path)

    logger.debug(
        f"加密完成\ntotal_count:{len(need_encrypted_py)}\nsuccess_count:{len(encrypted_py)}\n生成到:{output_file_path}")
