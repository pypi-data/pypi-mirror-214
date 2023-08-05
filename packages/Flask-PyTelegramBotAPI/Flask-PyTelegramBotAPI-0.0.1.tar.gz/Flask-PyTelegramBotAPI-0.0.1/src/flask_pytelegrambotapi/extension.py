from __future__ import annotations
from typing import Any, Callable, List, Optional, Union

import json
import time
import telebot
from werkzeug.local import LocalProxy
from telebot.handler_backends import State, StatesGroup
from telebot.storage import StateMemoryStorage, StatePickleStorage
import logging
from flask import Flask, request, abort, g, current_app


def get_user():
    tg_user = current_app._tg_user

    if current_app.pytelegrambotapi._user_callback is not None:
        tg_user = current_app.pytelegrambotapi._user_callback(tg_user)

    return tg_user


def get_chat():
    tg_chat = current_app._tg_chat
    return tg_chat


current_user = LocalProxy(get_user)
current_chat = LocalProxy(get_chat)


class PyTelegramBotApi:

    def __init__(self,
                 app: Flask | None = None, token: str | None = None, threaded: Optional[bool] = None) -> None:
        token = token or app.config.setdefault('TELEBOT_BOT_TOKEN', None)

        if not token:
            raise RuntimeError(
                "Either 'TELEBOT_BOT_TOKEN' must be set."
            )
        self.bot = None

        self._args = {}
        if 'TELEBOT_THREADED' in app.config:
            self._args['threaded'] = app.config['TELEBOT_THREADED']

        if threaded:
            self._args['threaded'] = threaded

        self.logger = telebot.logger
        telebot.logger.setLevel(logging.DEBUG)

        if app is not None:
            self.init_app(app)

    def init_app(self, app: Flask) -> None:
        state_storage = StatePickleStorage()

        self.bot: telebot.TeleBot = telebot.TeleBot(app.config['TELEBOT_BOT_TOKEN'], state_storage=state_storage,
                                                    **self._args)

        WEBHOOK_URL_PATH = "/%s/" % (app.config['TELEBOT_BOT_TOKEN'])

        @app.route(WEBHOOK_URL_PATH, methods=['POST'])
        def webhook():
            if request.headers.get('content-type') == 'application/json':
                json_string = request.get_data().decode('utf-8')
                update = telebot.types.Update.de_json(json_string)
                self.bot.process_new_updates([update])
                return ''
            else:
                abort(403)

        @app.before_request
        def _load_user():
            json_string = request.get_data().decode('utf-8')

            contact = None

            from pprint import pprint
            update = telebot.types.Update.de_json(json_string)
            pprint(update.__dict__)


            from pprint import pprint

            if update.callback_query:
                current_app._tg_user = update.callback_query.message.from_user
                current_app._tg_chat = update.callback_query.message.chat
                pprint(update.callback_query.__dict__)
            elif update.message:
                current_app._tg_user = update.message.from_user
                current_app._tg_chat = update.message.chat
                contact = update.message.contact
            elif update.edited_message:
                current_app._tg_user = update.edited_message.from_user
                current_app._tg_chat = update.edited_message.chat
                contact = update.edited_message.contact

            if contact:
                pprint(contact.__dict__)


        time.sleep(1)
        telebot.logger.info('Удаляем старые webhook')
        self.bot.remove_webhook()

        time.sleep(0.5)
        telebot.logger.info('Устанавливаем новые webhook')
        self.bot.set_webhook(url=app.config['TELEBOT_WEBHOOK_URL_BASE'] + WEBHOOK_URL_PATH)

        app.pytelegrambotapi = self

    def load_user(self, callback):
        print(callback)
        self._user_callback = callback
        return callback

    def __getattr__(self, item):
        if item in dir(self.bot):
            return getattr(self.bot, item)

        raise AttributeError("'{}' object has no attribute '{}'".format(type(self).__name__, item))
