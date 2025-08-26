#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Windows右键菜单ZIP压缩解压工具
支持文件夹压缩为ZIP和ZIP文件解压
"""

import os
import sys
import zipfile
import argparse
from pathlib import Path


def compress_folder(folder_path, zip_path=None):
    """
    将文件夹压缩为ZIP文件
    
    Args:
        folder_path (str): 要压缩的文件夹路径
        zip_path (str): 输出的ZIP文件路径，如果为None则自动生成
    
    Returns:
        bool: 压缩是否成功
    """
    try:
        folder_path = Path(folder_path)
        
        if not folder_path.exists():
            print(f"错误: 文件夹 '{folder_path}' 不存在")
            return False
            
        if not folder_path.is_dir():
            print(f"错误: '{folder_path}' 不是一个文件夹")
            return False
        
        # 如果没有指定输出路径，则在同级目录创建同名ZIP文件
        if zip_path is None:
            zip_path = folder_path.with_suffix('.zip')
        else:
            zip_path = Path(zip_path)
        
        # 确保输出目录存在
        zip_path.parent.mkdir(parents=True, exist_ok=True)
        
        print(f"正在压缩文件夹: {folder_path}")
        print(f"输出文件: {zip_path}")
        
        with zipfile.ZipFile(zip_path, 'w', zipfile.ZIP_DEFLATED, compresslevel=6) as zipf:
            # 遍历文件夹中的所有文件和子文件夹
            for file_path in folder_path.rglob('*'):
                if file_path.is_file():
                    # 计算相对路径
                    arcname = file_path.relative_to(folder_path)
                    zipf.write(file_path, arcname)
                    print(f"已添加: {arcname}")
        
        print(f"压缩完成: {zip_path}")
        return True
        
    except Exception as e:
        print(f"压缩失败: {str(e)}")
        return False


def extract_zip(zip_path, extract_path=None):
    """
    解压ZIP文件
    
    Args:
        zip_path (str): ZIP文件路径
        extract_path (str): 解压目标目录，如果为None则解压到同名文件夹
    
    Returns:
        bool: 解压是否成功
    """
    try:
        zip_path = Path(zip_path)
        
        if not zip_path.exists():
            print(f"错误: ZIP文件 '{zip_path}' 不存在")
            return False
            
        if not zip_path.is_file():
            print(f"错误: '{zip_path}' 不是一个文件")
            return False
            
        if zip_path.suffix.lower() != '.zip':
            print(f"错误: '{zip_path}' 不是ZIP文件")
            return False
        
        # 如果没有指定解压路径，则创建同名文件夹
        if extract_path is None:
            extract_path = zip_path.parent / zip_path.stem
        else:
            extract_path = Path(extract_path)
        
        # 确保解压目录存在
        extract_path.mkdir(parents=True, exist_ok=True)
        
        print(f"正在解压文件: {zip_path}")
        print(f"解压到目录: {extract_path}")
        
        with zipfile.ZipFile(zip_path, 'r') as zipf:
            # 检查ZIP文件是否有效
            bad_file = zipf.testzip()
            if bad_file:
                print(f"错误: ZIP文件损坏，坏文件: {bad_file}")
                return False
            
            # 获取文件列表
            file_list = zipf.namelist()
            print(f"ZIP文件包含 {len(file_list)} 个文件/文件夹")
            
            # 解压所有文件
            for file_info in zipf.infolist():
                try:
                    # 安全检查：防止路径遍历攻击
                    if '..' in file_info.filename or file_info.filename.startswith('/'):
                        print(f"跳过危险路径: {file_info.filename}")
                        continue
                        
                    zipf.extract(file_info, extract_path)
                    print(f"已解压: {file_info.filename}")
                    
                except Exception as e:
                    print(f"解压文件 {file_info.filename} 失败: {str(e)}")
                    continue
        
        print(f"解压完成: {extract_path}")
        return True
        
    except zipfile.BadZipFile:
        print(f"错误: '{zip_path}' 不是有效的ZIP文件")
        return False
    except Exception as e:
        print(f"解压失败: {str(e)}")
        return False


def main():
    try:
        print("ZIP压缩解压工具启动...")
        print(f"Python版本: {sys.version}")
        print(f"工作目录: {os.getcwd()}")
        print(f"命令行参数: {sys.argv}")
        
        parser = argparse.ArgumentParser(description='ZIP压缩解压工具')
        parser.add_argument('path', help='文件夹路径（压缩）或ZIP文件路径（解压）')
        parser.add_argument('-c', '--compress', action='store_true', help='压缩模式：将文件夹压缩为ZIP')
        parser.add_argument('-x', '--extract', action='store_true', help='解压模式：解压ZIP文件')
        
        args = parser.parse_args()
        
        print(f"输入路径: {args.path}")
        print(f"压缩模式: {args.compress}")
        print(f"解压模式: {args.extract}")
        
        success = False
        
        if args.compress:
            print("开始压缩操作...")
            success = compress_folder(args.path)
        elif args.extract:
            print("开始解压操作...")
            success = extract_zip(args.path)
        
        if success:
            print("操作成功完成！")
        else:
            print("操作失败！")
            
    except Exception as e:
        print(f"程序发生未处理的异常: {str(e)}")
        import traceback
        traceback.print_exc()
        success = False
    
    # Auto exit without waiting for user input
    sys.exit(0 if success else 1)


if __name__ == '__main__':
    main()