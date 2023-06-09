import asyncio
import logging

from aiogram import Bot

import config
import format_mail
import receive_mail
import spam_checker

bot = Bot(token=config.TOKEN, parse_mode="HTML")


async def check_mail(username, password):
    try:
        conn = receive_mail.get_conn(username, password)
        for m in receive_mail.receive_mail(conn):
            message_text = format_mail.mail_to_text(m)
            if (spam_checker.is_spam(message_text)):
                continue
            await bot.send_message(chat_id=config.TG_RECEIVER, text=message_text)
            logging.info(f"Sent message from {username} mailbox")
            await asyncio.sleep(1.5)
        else:
            logging.info(f"No new messages in {username} mailbox")
    except Exception as ex:
        logging.info(f"Failed to send message to user {config.TG_RECEIVER}")
        return


async def check_daemon(timeout):
    while True:
        try:
            for username, password in config.MAIL_BOXES:
                await check_mail(username, password)
        except Exception as ex:
            logging.exception("check_daemon")
        await asyncio.sleep(timeout)


if __name__ == '__main__':
    asyncio.run(check_daemon(config.UPDATE_INTERVAL))


