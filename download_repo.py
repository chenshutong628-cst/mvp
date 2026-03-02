#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import requests
import zipfile
import os

def download_and_extract_github_repo():
    repo_url = "https://github.com/xiajingkang17/mvp"

    # 尝试下载 main 分支，如果失败则尝试 master 分支
    branches = ["main", "master"]
    success = False

    for branch in branches:
        zip_url = f"{repo_url}/archive/refs/heads/{branch}.zip"
        try:
            print(f"尝试下载 {branch} 分支...")
            response = requests.get(zip_url, timeout=30)
            if response.status_code == 200:
                zip_filename = f"mvp-{branch}.zip"
                with open(zip_filename, "wb") as f:
                    f.write(response.content)
                print(f"下载完成: {zip_filename}")

                # 解压
                print("正在解压...")
                with zipfile.ZipFile(zip_filename, "r") as zip_ref:
                    zip_ref.extractall(".")

                # 删除zip文件
                os.remove(zip_filename)
                print(f"已删除 {zip_filename}")

                success = True
                break
            else:
                print(f"{branch} 分支不存在，状态码: {response.status_code}")
        except Exception as e:
            print(f"下载 {branch} 分支时出错: {e}")

    if success:
        print("下载并解压完成")
    else:
        print("下载失败，请检查网络连接或仓库地址")

if __name__ == "__main__":
    download_and_extract_github_repo()
