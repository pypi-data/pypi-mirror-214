# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['nonebot_plugin_grouplock',
 'nonebot_plugin_grouplock.models',
 'nonebot_plugin_grouplock.utils']

package_data = \
{'': ['*']}

install_requires = \
['nonebot-adapter-onebot>=2.2.3,<3.0.0',
 'nonebot2>=2.0.0,<3.0.0',
 'tortoise-orm>=0.19.3,<0.20.0']

setup_kwargs = {
    'name': 'nonebot-plugin-grouplock',
    'version': '0.0.2',
    'description': '一个基于nonebot2和go-cqhttp的群聊人数锁定插件',
    'long_description': '<p align="center">\n  <a href="https://v2.nonebot.dev/"><img src="https://v2.nonebot.dev/logo.png" width="200" height="200" alt="nonebot"></a>\n</p>\n\n<div align="center">\n\n#  nonebot-plugin-grouplock\n一个基于nonebot2和go-cqhttp的群聊人数锁定插件\n\n## 指令\n\n\n| 命令 | 示例 |\n|:--------:|:-------------:|\n| 锁定人数  |  锁定人数开 锁定人数500 锁定人数关 |\n|检查人数|   检查人数开 检查人数关 检查人数|',
    'author': 'ZM25XC',
    'author_email': 'xingling25@qq.com',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'https://github.com/ZM25XC/nonebot-plugin-grouplock',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
