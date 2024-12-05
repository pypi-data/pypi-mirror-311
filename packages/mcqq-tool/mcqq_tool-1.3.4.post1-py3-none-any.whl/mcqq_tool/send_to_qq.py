import re
from typing import Union

from nonebot import logger, get_bot
from nonebot.adapters.qq import Bot as QQBot
from nonebot.adapters.qq import AuditException
from nonebot.adapters.onebot.v11 import Bot as OneBot

from .config import plugin_config


async def send_mc_msg_to_qq(server_name: str, result: str):
    msg_result = re.sub(r"[&§].", "", result)
    if server := plugin_config.server_dict.get(server_name):
        if plugin_config.display_server_name:
            msg_result = f"[{server_name}] {msg_result}"

        for group in server.group_list:
            if bot := __get_target_bot(group.bot_id, True, group.group_id, msg_result):
                if group.adapter == "onebot":
                    bot: OneBot
                    await bot.send_group_msg(
                        group_id=int(group.group_id), message=msg_result
                    )
                elif group.adapter == "qq":
                    bot: QQBot
                    # TODO: 未实现，一个月主动就四条，还是算了吧。
                    # await bot.send_to_c2c(openid=group.group_id, message=msg_result)
                    logger.debug(
                        f"[MC_QQ]丨未实现的适配器: {group.adapter}，发送至群聊 {group.group_id}失败：一个月主动就四条，还是算了吧。"
                    )
                else:
                    logger.error(f"[MC_QQ]丨未知的适配器: {group.adapter}")

        for guild in server.guild_list:
            if bot := __get_target_bot(
                    guild.bot_id, False, guild.channel_id, msg_result
            ):
                if guild.adapter == "onebot":
                    bot: OneBot
                    await bot.send_guild_channel_msg(
                        guild_id=guild.guild_id,
                        channel_id=guild.channel_id,
                        message=msg_result,
                    )
                elif guild.adapter == "qq":
                    try:
                        bot: QQBot
                        await bot.send_to_channel(
                            channel_id=guild.channel_id, message=msg_result
                        )
                    except AuditException as e:
                        logger.debug(
                            f"[MC_QQ]丨发送至子频道 {guild.channel_id} 的消息：{msg_result} 正在审核中"
                        )
                        audit_result = await e.get_audit_result(3)
                        logger.debug(
                            f"[MC_QQ]丨审核结果：{audit_result.get_event_name()}"
                        )
    else:
        logger.error(f"未知的服务器: {server_name}")


def __get_target_bot(
        bot_id: str, is_group: bool, target_group_id: str, message: str
) -> Union[QQBot, OneBot, None]:
    target_type = "群聊" if is_group else "子频道"
    try:
        bot = get_bot(bot_id)
    except KeyError:
        logger.error(
            f'[MC_QQ]丨未找到bot: {bot_id}，发送至 [{target_type}@{target_group_id}] 失败: "{message}"'
        )
    except ValueError:
        logger.error(
            f'[MC_QQ]丨当前没有任何Bot可用，发送至 [{target_type}@{target_group_id}] 失败: "{message}"'
        )
    else:
        return bot


__all__ = ["send_mc_msg_to_qq"]
