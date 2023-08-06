from nonebot import get_driver
from nonebot.plugin import PluginMetadata

from . import utils,models

__plugin_meta__ = PluginMetadata(
    name='nonebot-plugin-grouplock',
    description='一个可以锁定群聊人数的插件',
    usage='...',
    homepage="https://github.com/ZM25XC/nonebot-plugin-grouplock",
    type="application",
    supported_adapters={"~onebot.v11"},
    extra={
        'author': 'ZM25XC',
        'version': '0.0.1',
        'priority': 50,
    }
)
DRIVER = get_driver()


@DRIVER.on_startup
async def startup():
    await utils.path.connect()


DRIVER.on_shutdown(utils.path.disconnect)


@DRIVER.on_bot_connect
async def bot_connect():
    await utils.handel.group_init()
