from datetime import datetime
import os
import shutil

FRONT_MATTER = '''---
title: {0}
date: {1} +0800
categories: [{2}]
tags: []
---
'''

def get_cur_time_str():
    dt = datetime.now()
    return dt.strftime('%Y-%m-%d %X')

def edit_md(fn, category):
    title = fn.split('.')[0].split('\\')[-1]
    dt = get_cur_time_str()
    fm = FRONT_MATTER.format(title, dt, category)
    with open(fn, 'r+', encoding='utf-8') as f:
        content = f.read()
        f.seek(0, 0)
        f.write(fm+'\n\n'+content)

if __name__ == '__main__':
    VAULT_PATH = r'C:\Users\pzx20\OneDrive - HKUST Connect\Doraemon\文集\文集'
    POSTS_PATH = r'E:\Repos\shimmer\_posts'

    vault_categories = os.listdir(VAULT_PATH)
    posts_categories = os.listdir(POSTS_PATH)

    for category in vault_categories:
        if category.startswith('.'):
            continue
        if category not in posts_categories:
            os.makedirs(os.path.join(POSTS_PATH, category))
        vault_files = os.listdir(os.path.join(VAULT_PATH, category))
        posts_files = os.listdir(os.path.join(POSTS_PATH, category))
        for file in vault_files:
            if file not in posts_files:
                shutil.copy(os.path.join(VAULT_PATH, category, file), os.path.join(POSTS_PATH, category))
                edit_md(os.path.join(POSTS_PATH, category, file), category)
                print(f'created file {category}/{file}')