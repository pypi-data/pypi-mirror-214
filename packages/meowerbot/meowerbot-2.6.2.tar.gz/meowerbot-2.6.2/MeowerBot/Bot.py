import threading
import shlex

from .cl import CloudLink
import sys

import json
import traceback

import requests


import time

from .command import AppCommand
from .context import CTX

import time
import logging

from .API import MeowerAPI

from websocket._exceptions import WebSocketConnectionClosedException, WebSocketException

import sys

if sys.version_info >= (3, 11):
    from enum import StrEnum
else:
    from backports.strenum import StrEnum

from typing import Union

class cbids(StrEnum):
        error = "error"
        __raw__ = "__raw__"
        login = "login"
        close = "close"
        statuscode = "statuscode"
        ulist = "ulist"
        message = "message"
        raw_message = "raw_message"
        chat_list = "chat_list"
        direct = "direct"

class Bot:
    """
    A class that holds all of the networking for a meower bot to function and run

    """
    __bridges__ = [
			"Discord",
			"Revower",
			"revolt"
		]

    BOT_TAKEN_LISTENERS = [
        "__meowerbot__send_ip",
        "__meowerbot__send_message",
        "__meowerbot__login",
        "__meowerbot__cloudlink_trust",
    ]

    BOT_NO_PMSG_RESPONSE = [
        "I:500 | Bot",
        "I: 500 | Bot"
    ]

    def _t_ping(self):
        while True:
            time.sleep(60)

            self.wss.sendPacket({"cmd": "ping", "val": ""})

    def __init__(self, prefix=None, autoreload: int or None = None ): #type: ignore
        self.wss = CloudLink()
        self.callbacks = {}
        self._last_to = "Home"

        self.wss.callback(
            "on_packet", self._debug_fix
        )  # self._debug_fix catches all errors
        self.wss.callback("on_error", self.__handle_error__)  # handle uncought errors
        self.wss.callback("on_close", self.__handle_close__)  # Websocket disconnected
        self.wss.callback(
            "on_connect", self.__handle_on_connect__
        )  # signing in and stuff like that

        # to be used in start
        self.username = None
        self.password = None
        self.logger_in = False

        if autoreload:
            self.autoreload = True
            self.autoreload_time = min(autoreload, 1)
            self.autoreload_original = min(autoreload, 1)
        else:
            self.autoreload = False
            self.autoreload_time = 0
            self.autoreload_original = 0

        self.commands = {}
        self.prefix = prefix
        self._t_ping_thread = threading.Thread(target=self._t_ping, daemon=True)  # (:
        self.logger = logging.getLogger("MeowerBot")
        self.bad_exit = False
        self.server = None

        self.cogs = {}

    def run_cb(self, cbid, args=(), kwargs=None):  # cq: ignore
        if cbid not in self.callbacks:
            return  # ignore

        if not kwargs:
            kwargs = {}
        
        if cbid == "error" and isinstance(args[0], KeyboardInterrupt()): 
            self.logger.error("KeyboardInterrupt")
            self.bad_exit = True
            self.stop()
            return 

        kwargs["bot"] = self
        for callback in self.callbacks[cbid]:
            try:
                callback(
                    *args, **kwargs
                )  # multi callback per id is supported (unlike cloudlink 0.1.7.3 LOL)
            except Exception as e:  # cq ignore

                self.logger.error(traceback.format_exc())
                self.run_cb("error", args=(e,))

    def __handle_error__(self, e):
        self.run_cb("error", args=(e,))
        if type(e) == WebSocketConnectionClosedException and self.autoreload:
            self.__handle_close__()
            return

        if (type(e)) == KeyboardInterrupt:
            #kill all bot threads
            self.bad_exit = True

            self.wss = None # effectively kill the bot
            self.__handle_close__(            )            
            return
 
    def _debug_fix(self, packet):
        packet = json.loads(packet)  # Server bug workaround

        try:
            self.__handle_packet__(packet)
        except BaseException as e:  # cq: skip #IDC ABOUT GENERAL EXCP
            self.__handle_error__(e)
            self.logger.error(traceback.format_exc())
            self.run_cb("error", args=(e, ))

        try:
            self.run_cb("__raw__", args=(packet, ))  # raw packets
        except BaseException as e:  # cq: skip #IDC ABOUT GENERAL EXCP
            self.__handle_error__(e)
            self.logger.error(traceback.format_exc())
            self.run_cb("error", args=(e, ))

    def __handle_on_connect__(self):
        self.wss.sendPacket(
            {
                "cmd": "direct",
                "val": {"cmd": "type", "val": "py"},
            }
        )
        self.wss.sendPacket(
            {
                "cmd": "direct",
                "val": "meower",
                "listener": "__meowerbot__cloudlink_trust",
            }
        )

    def command(self, aname=None, args=0):
        def inner(func):
            if aname is None:
                name = func.__name__
            else:
                name = aname

            cmd = AppCommand(func, name=name, args=args)

            info = cmd.info()
            info[cmd.name]["command"] = cmd

            self.commands.update(info)

            return cmd #allow subcommands without a cog

        return inner

    def register_cog(self, cog):
        info = cog.get_info()
        self.cogs[cog.__class__.__name__] = cog
        self.commands.update(info)

    def deregister_cog(self, cogname):
        for cmd in self.cogs[cogname].get_info().values():
            del self.commands[cmd.name]
        del self.cogs[cogname]

    def _handle_status(self, status, listener):
        if status == "I:112 | Trusted Access enabled":
            return

        if self.logger_in:
            self.logger_in = False

            if status != "I:100 | OK":
                raise RuntimeError("CloudLink Trust Failed")

            auth_packet = {
                "cmd": "direct",
                "val": {
                    "cmd": "authpswd",
                    "val": {"username": self.username, "pswd": self._password},
                },
                "listener": "__meowerbot__login",
            }
            self.wss.sendPacket(auth_packet)

        elif listener == "__meowerbot__login":
            if status == "E:104 | Internal":
                requests.post(
                    "https://webhooks.meower.org/post/home",
                    json={
                        "post": "ERROR: MeowerBot.py Webhooks Logging\n\n Account Softlocked.",
                        "username": self.username,
                    },
                    timeout=5
                )
                print("CRITICAL ERROR! ACCOUNT SOFTLOCKED!!!!.", file=sys.__stdout__)
                self.bad_exit = True
                del self.wss
                
                return

            if status != "I:100 | OK":
                raise RuntimeError("Password Or Username Is Incorrect")

            time.sleep(0.5)
            self.run_cb("login", args=(), kwargs={})

        elif listener == "__meowerbot__send_message":
            if status == "I:100 | OK":
                self.autoreload_time = self.autoreload_original
                return

            raise RuntimeError("Post Failed to send")

    def callback(self, callback, cbid: Union[Union[cbids,  None], str] =None):
        """Connects a callback ID to a callback
        """
        if cbid is None:
            cbid = callback.__name__

        if cbid not in self.callbacks:
            self.callbacks[cbid] = []
        self.callbacks[cbid].append(callback)

    def __handle_close__(self, *args, **kwargs):
        if self.autoreload:
            self.autoreload = False #to stop race condisons 
            self.logger_in = True
            self.autoreload_time *= 1.2 
            
            
            time.sleep(self.autoreload_time)
            self.autoreload = True #reset this, as i set it to false above.

            self.wss.state = 0 #type: ignore
            self.wss.client(self.server) #type: ignore
            return #dont want the close callback to be called here

        self.run_cb("close", args=args, kwargs=kwargs)

    def handle_bridges(self, packet):
        if packet["val"]["u"] in self.__bridges__ and ": " in packet["val"]["p"]:
                split = packet["val"]["p"].split(": ", 1)
                packet["val"]["p"] = split[1]
                packet["val"]["u"] = split[0]
        
        if packet["val"]["p"].startswith(self.prefix+"#0000"):
            packet["val"]["p"] = packet["val"]["p"].replace("#0000", "")
        
        return packet

    def __handle_packet__(self, packet):
        if packet["cmd"] == "statuscode":

            self._handle_status(packet["val"], packet.get("listener", None))

            listener = packet.get("listener", None)
            return self.run_cb("statuscode", args=(packet["val"], listener))

        elif packet["cmd"] == "ulist":
            self.run_cb("ulist", self.wss.statedata["ulist"]["usernames"])

        elif packet["cmd"] == "direct" and "post_origin" in packet["val"]:
            packet = self.handle_bridges(packet)

            ctx = CTX(packet["val"], self)
            if "message" in self.callbacks:
                self.run_cb("message", args=(ctx.message,))

            else:

                if ctx.user.username == self.username:
                    return
                if not ctx.message.data.startswith(self.prefix):
                    return

                ctx.message.data = ctx.message.data.split(self.prefix, 1)[1]

                self.run_command(ctx.message)

            self.run_cb("raw_message", args=(packet["val"],))

        elif packet["cmd"] == "direct":
            listener = packet.get("listener")

            if listener == "mb_get_chat_list":
                self.run_cb("chat_list", args=(packet["val"]["payload"], listener))
            elif listener == "__meowerbot__login":
                self.api.login(packet['val']['payload']['token'])
            self.run_cb("direct", args=(packet["val"], listener))

        

        else:
            listener = packet.get("listener")
            self.run_cb(packet["cmd"], args=(packet["val"], listener))

        
        if (packet["cmd"] == "pmsg") and  (packet["val"] not in self.BOT_NO_PMSG_RESPONSE):
            self.wss.sendPacket({
                "cmd": "pmsg",
                "val": "I:500 | Bot",
                "id": packet["origin"]
            })

    def run_command(self, message):
        args = shlex.split(str(message))

        try:
            self.commands[args[0]]["command"].run_cmd(message.ctx, *args[1:])
        except KeyError as e:
            self.logger.error(traceback.format_exc())
            self.run_cb("error", args=(e,))

    def send_msg(self, msg, to="home"):
        self._last_to = to
        self._last_sent = msg
        try:
            if to == "home":
                self.wss.sendPacket(
                    {
                        "cmd": "direct",
                        "val": {"cmd": "post_home", "val": msg},
                        "listener": "__meowerbot__send_message",
                    }
                )
            else:
                self.wss.sendPacket(
                    {
                        "cmd": "direct",
                        "val": {"cmd": "post_chat", "val": {"chatid": to, "p": msg}},
                        "listener": "__meowerbot__send_message",
                    }
                )
        #socket is closed, use webhooks
        except WebSocketException as e:
            self.run_cb(cbid="error", args=(e,))

    def send_typing(self, to="home"):
        if  to == "home":
            self.wss.sendPacket(
                {
                    "cmd": "direct",
                    "val": {
                        "cmd": "set_chat_state",
                        "val": {
                            "chatid": "livechat",
                            "state": 101,
                        },
                    },
                }
            )
        else:
          self.wss.sendPacket(
            {
                "cmd": "direct",
                "val": {
                    "cmd": "set_chat_state",
                    "val": {
                        "chatid": to,
                        "state": 100,
                    },
                },
            }
          )
        
    def enter_chat(self, chatid="livechat"):
        self.wss.sendPacket(
            {
                "cmd": "direct",
                "val": {
                    "cmd": "set_chat_state",
                    "val": {
                        "chatid": chatid,
                        "state": 1,
                    },
                },
            }
        )

    def create_chat(self, name):
        """
        Unstable, use at your own risk

        comes with callbacks: chat_list 
        """
        self.wss.sendPacket({
            "cmd": "direct",
            "val": {
                "cmd": "create_chat",
                "val": name
            },
            "listener": "mb_create_chat"
        })

        time.sleep(secs=0.5)

        self.wss.sendPacket({
            "cmd": "direct",
            "val": {
                "cmd": "get_chat_list",
                "val": {
                    "page": 1
                }
            },
            "listener": "mb_get_chat_list"
        })

    def run(self, username, password, server="wss://server.meower.org"):
        """
        Runs The bot (Blocking)
        """
        self.username = username
        self._password = password
        self.logger_in = True

        self._t_ping_thread.start()
        if self.prefix is None:
            self.prefix = "@" + self.username
        self.logger = logging.getLogger(f"MeowerBot {self.username}")
        self.server = server
        self.api = MeowerAPI(username=username)
        self.wss.client(server)
        
        if self.bad_exit:
            raise BaseException("Bot Account Softlocked")
