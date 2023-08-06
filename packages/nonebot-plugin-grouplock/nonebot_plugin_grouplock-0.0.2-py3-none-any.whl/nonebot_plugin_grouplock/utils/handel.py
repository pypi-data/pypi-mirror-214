import re
import time

from nonebot import get_bot, on_command
from nonebot.adapters.onebot.v11 import Bot, GroupMessageEvent, GroupIncreaseNoticeEvent, GroupDecreaseNoticeEvent
from nonebot.adapters.onebot.v11 import Message, GROUP_ADMIN, GROUP_OWNER
from nonebot.message import run_postprocessor, run_preprocessor
from nonebot.params import CommandArg

from ..models.group import GroupSetting, GroupMember

auto_kick = on_command("auto_kick", aliases={"锁定人数", "锁定群人数"}, permission=GROUP_OWNER | GROUP_ADMIN,
                       priority=50)
check_status = on_command("check_status", aliases={"自动检查人数", "检查人数"}, permission=GROUP_OWNER | GROUP_ADMIN,
                          priority=50)


async def group_init():
    bot: Bot = get_bot()
    group_list_result = await bot.get_group_list()
    for item in group_list_result:
        group_id = item["group_id"]
        group_name = item["group_name"]
        group_memo = None
        group_create_time = item["group_create_time"]
        group_level = item["group_level"]
        member_count = item["member_count"]
        max_member_count = item["max_member_count"]
        result = await GroupSetting.filter(group_id=group_id).values()
        if result:
            await GroupSetting.filter(group_id=group_id).update(
                group_name=group_name,
                group_memo=group_memo,
                group_create_time=group_create_time,
                group_level=group_level,
                member_count=member_count,
                max_member_count=max_member_count
            )
        else:
            await GroupSetting.create(
                time=time.time(),
                group_id=group_id,
                group_level=group_level,
                group_create_time=group_create_time,
                group_memo=group_memo,
                group_name=group_name,
                member_count=member_count,
                max_member_count=max_member_count,
                set_count=max_member_count - 1,
                check_status=False,
                auto_kick=False
            )
        group_member_result = await bot.get_group_member_list(group_id=group_id)
        for item2 in group_member_result:
            user_id = item2["user_id"]
            nickname = item2["nickname"]
            card = item2["card"]
            sex = item2["sex"]
            age = item2["age"]
            area = item2["area"]
            join_time = item2["join_time"]
            last_sent_time = item2["last_sent_time"]
            level = item2["level"]
            role = item2["role"]
            unfriendly = item2["unfriendly"]
            title = item2["title"]
            title_expire_time = item2["title_expire_time"]
            card_changeable = item2["card_changeable"]
            shut_up_timestamp = item2["shut_up_timestamp"]
            member_result = await GroupMember.filter(group_id=group_id, user_id=user_id).values()
            if member_result:
                await GroupMember.filter(group_id=group_id, user_id=user_id).update(
                    nickname=nickname,
                    card=card,
                    sex=sex,
                    age=age,
                    area=area,
                    join_time=join_time,
                    last_sent_time=last_sent_time,
                    level=level,
                    role=role,
                    unfriendly=unfriendly,
                    title=title,
                    title_expire_time=title_expire_time,
                    card_changeable=card_changeable,
                    shut_up_timestamp=shut_up_timestamp
                )
            else:
                await GroupMember.create(
                    time=time.time(),
                    group_id=group_id,
                    user_id=user_id,
                    nickname=nickname,
                    card=card,
                    sex=sex,
                    age=age,
                    area=area,
                    join_time=join_time,
                    last_sent_time=last_sent_time,
                    level=level,
                    role=role,
                    unfriendly=unfriendly,
                    title=title,
                    title_expire_time=title_expire_time,
                    card_changeable=card_changeable,
                    shut_up_timestamp=shut_up_timestamp
                )


@run_postprocessor
async def refresh_status(event: GroupMessageEvent):
    user_id = event.user_id
    group_id = event.group_id
    last_sent_time = event.time
    await GroupMember.filter(group_id=group_id, user_id=user_id).update(
        last_sent_time=last_sent_time
    )


@run_preprocessor
async def group_increase(bot: Bot, event: GroupIncreaseNoticeEvent):
    group_id = event.group_id
    user_id = event.user_id
    member_result = await bot.get_group_member_info(group_id=group_id, user_id=user_id)
    member_result["time"] = time.time()
    result = await GroupSetting.filter(group_id=group_id).values()
    status = await GroupMember.filter(group_id=group_id, user_id=user_id).values("id")
    if result[0]["auto_kick"]:
        if (result[0]["member_count"] + 1) >= result[0]["set_count"]:
            member = await GroupMember.filter(group_id=group_id, role="member").order_by("-last_sent_time").limit(
                result[0]["member_count"] + 1 - result[0]["set_count"]).values()
            if member:
                for item in member:
                    await bot.set_group_kick(group_id=group_id, user_id=item["user_id"])
                await GroupSetting.filter(group_id=group_id).update(
                    member_count=result[0]["set_count"] - 1
                )
    if status:
        return
    await GroupMember.create(
        **member_result
    )
    await GroupSetting.filter(group_id=group_id).update(
        member_count=result[0]["member_count"] + 1
    )


@run_postprocessor
async def group_decrease(event: GroupDecreaseNoticeEvent):
    group_id = event.group_id
    user_id = event.user_id
    result = await GroupSetting.filter(group_id=group_id).values()
    status = await GroupMember.filter(group_id=group_id, user_id=user_id).values("id")
    if status:
        await GroupMember.filter(id=status[0]["id"]).delete()
    await GroupSetting.filter(group_id=group_id).update(
        member_count=result[0]["member_count"] - 1
    )


@auto_kick.handle()
async def auto_kick_(event: GroupMessageEvent, msg: Message = CommandArg()):
    group_id = event.group_id
    if str(msg).strip() in ["open", "开", "start", "开启"]:
        await GroupSetting.filter(group_id=group_id).update(
            auto_kick=True
        )
        await auto_kick.finish(message="群人数锁定开启成功！", at_sender=True, reply_message=True)
    elif str(msg).strip() in ["close", "关", "down", "关闭"]:
        await GroupSetting.filter(group_id=group_id).update(
            auto_kick=False
        )
        await auto_kick.finish(message="群人数锁定关闭成功！", at_sender=True, reply_message=True)
    elif re.findall(r"\b(3000|[12]?\d{1,3})\b", str(msg)):
        count = int(re.findall(r"\b(3000|[12]?\d{1,3})\b", str(msg))[0])
        group = await GroupSetting.filter(group_id=group_id).values()
        if count > group[0]["max_member_count"]:
            await auto_kick.finish(message=f"超过群人数上限，锁定群人数：{count} 失败", at_sender=True,
                                   reply_message=True)
        await GroupSetting.filter(group_id=group_id).update(
            set_count=count
        )
        await auto_kick.finish(message=f"锁定群人数：{count} 成功", at_sender=True,
                               reply_message=True)
    else:
        return


@check_status.handle()
async def check_status_(bot: Bot, event: GroupMessageEvent, msg: Message = CommandArg()):
    group_id = event.group_id
    if str(msg).strip() in ["open", "开", "start", "开启"]:
        await GroupSetting.filter(group_id=group_id).update(
            check_status=True
        )
        await check_status.finish(message="群人数检查开启成功！", at_sender=True, reply_message=True)
    elif str(msg).strip() in ["close", "关", "down", "关闭"]:
        await GroupSetting.filter(group_id=group_id).update(
            check_status=False
        )
        await check_status.finish(message="群人数检查关闭成功！", at_sender=True, reply_message=True)
    elif str(msg).strip() == "":
        result = await GroupSetting.filter(group_id=group_id).values()
        if (result[0]["member_count"] + 1) >= result[0]["set_count"]:
            member = await GroupMember.filter(group_id=group_id, role="member").order_by("-last_sent_time").limit(
                result[0]["member_count"] + 1 - result[0]["set_count"]).values()
            if member:
                for item in member:
                    await bot.set_group_kick(group_id=group_id, user_id=item["user_id"])
                await GroupSetting.filter(group_id=group_id).update(
                    member_count=result[0]["set_count"] - 1
                )
        await check_status.finish(message="群人数检查成功！", at_sender=True, reply_message=True)
    else:
        return
