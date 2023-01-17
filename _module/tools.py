from aiogram import types


def is_reply(message: types.Message) -> bool:
    if message.is_topic_message:
        return message.reply_to_message and \
            message.reply_to_message.message_id != message.message_thread_id

    return message.reply_to_message is not None