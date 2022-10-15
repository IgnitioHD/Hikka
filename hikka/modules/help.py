#             █ █ ▀ █▄▀ ▄▀█ █▀█ ▀
#             █▀█ █ █ █ █▀█ █▀▄ █
#              © Copyright 2022
#           https://t.me/hikariatama
#
# 🔒      Licensed under the GNU AGPLv3
# 🌐 https://www.gnu.org/licenses/agpl-3.0.html

import difflib
import inspect
import logging

from telethon.tl.types import Message

from .. import loader, utils

logger = logging.getLogger(__name__)


@loader.tds
class HelpMod(loader.Module):
    """Shows help for modules and commands"""

    strings = {
        "name": "Help",
        "bad_module": "<b>🚫 <b>Module</b> <code>{}</code> <b>not found</b>",
        "single_mod_header": (
            "<emoji document_id=5188377234380954537>🌘</emoji> <b>{}</b>:"
        ),
        "single_cmd": "\n▫️ <code>{}{}</code> {}",
        "undoc_cmd": "🦥 No docs",
        "all_header": (
            "<emoji document_id=5188377234380954537>🌘</emoji> <b>{} mods available,"
            " {} hidden:</b>"
        ),
        "mod_tmpl": "\n{} <code>{}</code>",
        "first_cmd_tmpl": ": ( {}",
        "cmd_tmpl": " | {}",
        "no_mod": "🚫 <b>Specify module to hide</b>",
        "hidden_shown": (
            "<emoji document_id=5188377234380954537>🌘</emoji> <b>{} modules hidden,"
            " {} modules shown:</b>\n{}\n{}"
        ),
        "ihandler": "\n🎹 <code>{}</code> {}",
        "undoc_ihandler": "🦥 No docs",
        "support": (
            "{} <b>Link to </b><a href='https://t.me/hikka_talks'>support chat</a>"
        ),
        "partial_load": (
            "<emoji document_id=5472105307985419058>☝️</emoji> <b>Userbot is not"
            " fully loaded, so not all modules are shown</b>"
        ),
        "not_exact": (
            "<emoji document_id=5472105307985419058>☝️</emoji> <b>No exact match"
            " occured, so the closest result is shown instead</b>"
        ),
        "request_join": "You requested link for Hikka support chat",
        "core_notice": (
            "<emoji document_id=5472105307985419058>☝️</emoji> <b>This is a core"
            " module. You can't unload it nor replace</b>"
        ),
    }

    strings_ru = {
        "bad_module": "<b>🚫 <b>Модуль</b> <code>{}</code> <b>не найден</b>",
        "single_mod_header": (
            "<emoji document_id=5188377234380954537>🌘</emoji> <b>{}</b>:"
        ),
        "single_cmd": "\n▫️ <code>{}{}</code> {}",
        "undoc_cmd": "🦥 Нет описания",
        "all_header": (
            "<emoji document_id=5188377234380954537>🌘</emoji> <b>{} модулей доступно,"
            " {} скрыто:</b>"
        ),
        "mod_tmpl": "\n{} <code>{}</code>",
        "first_cmd_tmpl": ": ( {}",
        "cmd_tmpl": " | {}",
        "no_mod": "🚫 <b>Укажи модуль(-и), которые нужно скрыть</b>",
        "hidden_shown": (
            "<emoji document_id=5188377234380954537>🌘</emoji> <b>{} модулей скрыто,"
            " {} модулей показано:</b>\n{}\n{}"
        ),
        "ihandler": "\n🎹 <code>{}</code> {}",
        "undoc_ihandler": "🦥 Нет описания",
        "support": (
            "{} <b>Ссылка на </b><a href='https://t.me/hikka_talks'>чат помощи</a>"
        ),
        "_cls_doc": "Показывает помощь по модулям",
        "partial_load": (
            "<emoji document_id=5472105307985419058>☝️</emoji> <b>Юзербот еще не"
            " загрузился полностью, поэтому показаны не все модули</b>"
        ),
        "not_exact": (
            "<emoji document_id=5472105307985419058>☝️</emoji> <b>Точного совпадения"
            " не нашлось, поэтому было выбрано наиболее подходящее</b>"
        ),
        "request_join": "Вы запросили ссылку на чат помощи Hikka",
        "core_notice": (
            "<emoji document_id=5472105307985419058>☝️</emoji> <b>Это встроенный"
            " модуль. Вы не можете его выгрузить или заменить</b>"
        ),
    }

    strings_de = {
        "bad_module": "<b>🚫 <b>Modul</b> <code>{}</code> <b>nicht gefunden</b>",
        "single_mod_header": (
            "<emoji document_id=5188377234380954537>🌘</emoji> <b>{}</b>:"
        ),
        "single_cmd": "\n▫️ <code>{}{}</code> {}",
        "undoc_cmd": "🦥 Keine Dokumentation",
        "all_header": (
            "<emoji document_id=5188377234380954537>🌘</emoji> <b>{} Module verfügbar,"
            " {} versteckt:</b>"
        ),
        "mod_tmpl": "\n{} <code>{}</code>",
        "first_cmd_tmpl": ": ( {}",
        "cmd_tmpl": " | {}",
        "no_mod": "🚫 <b>Gib das Modul an, das du verstecken willst</b>",
        "hidden_shown": (
            "<emoji document_id=5188377234380954537>🌘</emoji> <b>{} Module versteckt,"
            " {} Module angezeigt:</b>\n{}\n{}"
        ),
        "ihandler": "\n🎹 <code>{}</code> {}",
        "undoc_ihandler": "🦥 Keine Dokumentation",
        "support": (
            "{} <b>Link zum </b><a href='https://t.me/hikka_talks'>Supportchat</a>"
        ),
        "_cls_doc": "Zeigt Hilfe zu Modulen an",
        "partial_load": (
            "<emoji document_id=5472105307985419058>☝️</emoji> <b>Der Userbot ist noch"
            " nicht vollständig geladen, daher werden nicht alle Module angezeigt</b>"
        ),
        "not_exact": (
            "<emoji document_id=5472105307985419058>☝️</emoji> <b>Es wurde kein exakter"
            " Treffer gefunden, daher wird das nächstbeste Ergebnis angezeigt</b>"
        ),
        "request_join": "Du hast den Link zum Supportchat angefordert",
        "core_notice": (
            "<emoji document_id=5472105307985419058>☝️</emoji> <b>Dies ist ein"
            " eingebauter Modul. Du kannst ihn nicht entladen oder ersetzen</b>"
        ),
    }

    strings_tr = {
        "bad_module": "<b>🚫 <b>Modül</b> <code>{}</code> <b>bulunamadı</b>",
        "single_mod_header": (
            "<emoji document_id=5188377234380954537>🌘</emoji> <b>{}</b>:"
        ),
        "single_cmd": "\n▫️ <code>{}{}</code> {}",
        "undoc_cmd": "🦥 Dokümantasyon yok",
        "all_header": (
            "<emoji document_id=5188377234380954537>🌘</emoji> <b>{} modül mevcut,"
            " {} gizli:</b>"
        ),
        "mod_tmpl": "\n{} <code>{}</code>",
        "first_cmd_tmpl": ": ( {}",
        "cmd_tmpl": " | {}",
        "no_mod": "🚫 <b>Gizlemek istediğin modülü belirt</b>",
        "hidden_shown": (
            "<emoji document_id=5188377234380954537>🌘</emoji> <b>{} modül gizlendi,"
            " {} modül gösterildi:</b>\n{}\n{}"
        ),
        "ihandler": "\n🎹 <code>{}</code> {}",
        "undoc_ihandler": "🦥 Dokümantasyon yok",
        "support": "{} <b> </b><a href='https://t.me/hikka_talks'>Destek sohbeti</a>",
        "_cls_doc": "Modül yardımını gösterir",
        "partial_load": (
            "<emoji document_id=5472105307985419058>☝️</emoji> <b>Kullanıcı botu"
            " henüz tam olarak yüklenmediğinden, tüm modüller görüntülenmez</b>"
        ),
        "not_exact": (
            "<emoji document_id=5472105307985419058>☝️</emoji> <b>Herhangi bir"
            " eşleşme bulunamadığından, en uygun sonuç görüntülenir</b>"
        ),
        "request_join": "Destek sohbeti bağlantısını istediniz",
        "core_notice": (
            "<emoji document_id=5472105307985419058>☝️</emoji> <b>Bu bir"
            " dahili modül. Sen onu kaldıramaz veya değiştiremezsin</b>"
        ),
    }

    strings_hi = {
        "bad_module": "<b>🚫 <b>मॉड्यूल</b> <code>{}</code> <b>नहीं मिला</b>",
        "single_mod_header": (
            "<emoji document_id=5188377234380954537>🌘</emoji> <b>{}</b>:"
        ),
        "single_cmd": "\n▫️ <code>{}{}</code> {}",
        "undoc_cmd": "🦥 दस्तावेज़ीकरण नहीं",
        "all_header": (
            "<emoji document_id=5188377234380954537>🌘</emoji> <b>{} मॉड्यूल उपलब्ध हैं,"
            " {} छिपा हुआ:</b>"
        ),
        "mod_tmpl": "\n{} <code>{}</code>",
        "first_cmd_tmpl": ": ( {}",
        "cmd_tmpl": " | {}",
        "no_mod": "🚫 <b>छिपाने के लिए मॉड्यूल दर्ज करें</b>",
        "hidden_shown": (
            "<emoji document_id=5188377234380954537>🌘</emoji> <b>{} मॉड्यूल छिपा हुआ,"
            " {} मॉड्यूल दिखाया गया:</b>\n{}\n{}"
        ),
        "ihandler": "\n🎹 <code>{}</code> {}",
        "undoc_ihandler": "🦥 दस्तावेज़ीकरण नहीं",
        "support": "{} <b> </b><a href='https://t.me/hikka_talks'>सपोर्ट चैट</a>",
        "_cls_doc": "मॉड्यूल सहायता दिखाता है",
        "partial_load": (
            "<emoji document_id=5472105307985419058>☝️</emoji> <b>उपयोगकर्ता बॉट अभी भी"
            " पूरी तरह से लोड नहीं हुई है, इसलिए सभी मॉड्यूल दिखाई नहीं देते हैं</b>"
        ),
        "not_exact": (
            "<emoji document_id=5472105307985419058>☝️</emoji> <b>कोई मैच नहीं मिला,"
            " इसलिए सबसे अनुकूल परिणाम दिखाया गया है</b>"
        ),
        "request_join": "आपने सपोर्ट चैट लिंक का अनुरोध किया है",
        "core_notice": (
            "<emoji document_id=5472105307985419058>☝️</emoji> <b>यह एक अंतर्निहित"
            " मॉड्यूल है, आप इसे नहीं अटक सकते या बदल सकते हैं</b>"
        ),
    }

    strings_uz = {
        "bad_module": "<b>🚫 <b>Modul</b> <code>{}</code> <b>topilmadi</b>",
        "single_mod_header": (
            "<emoji document_id=5188377234380954537>🌘</emoji> <b>{}</b>:"
        ),
        "single_cmd": "\n▫️ <code>{}{}</code> {}",
        "undoc_cmd": "🦥 Hujjatlanmagan",
        "all_header": (
            "<emoji document_id=5188377234380954537>🌘</emoji> <b>{} taqdim etilgan"
            " modullar, {} yashirin:</b>"
        ),
        "mod_tmpl": "\n{} <code>{}</code>",
        "first_cmd_tmpl": ": ( {}",
        "cmd_tmpl": " | {}",
        "no_mod": "🚫 <b>Yashirish uchun modul kiriting</b>",
        "hidden_shown": (
            "<emoji document_id=5188377234380954537>🌘</emoji> <b>{} yashirin,"
            " {} modullar ko'rsatilgan:</b>\n{}\n{}"
        ),
        "ihandler": "\n🎹 <code>{}</code> {}",
        "undoc_ihandler": "🦥 Hujjatlanmagan",
        "support": "{} <b> </b><a href='https://t.me/hikka_talks'>Yordam chat</a>",
        "_cls_doc": "Modul yordamini ko'rsatadi",
        "partial_load": (
            "<emoji document_id=5472105307985419058>☝️</emoji> <b>Foydalanuvchi boti"
            " hali to'liq yuklanmaganligi sababli, barcha modullar ko'rsatilmaydi</b>"
        ),
        "not_exact": (
            "<emoji document_id=5472105307985419058>☝️</emoji> <b>Hech qanday moslik"
            " topilmadi, shuning uchun eng mos natija ko'rsatildi</b>"
        ),
        "request_join": "Siz yordam chat havolasini so'radingiz",
        "core_notice": (
            "<emoji document_id=5472105307985419058>☝️</emoji> <b>Bu bir qo'shimcha"
            " modul, uni o'chirib yoki o'zgartirib bo'lmaysiz</b>"
        ),
    }

    def __init__(self):
        self.config = loader.ModuleConfig(
            loader.ConfigValue(
                "core_emoji",
                "▪️",
                lambda: "Core module bullet",
                validator=loader.validators.Emoji(length=1),
            ),
            loader.ConfigValue(
                "hikka_emoji",
                "🌘",
                lambda: "Hikka-only module bullet",
                validator=loader.validators.Emoji(length=1),
            ),
            loader.ConfigValue(
                "plain_emoji",
                "▫️",
                lambda: "Plain module bullet",
                validator=loader.validators.Emoji(length=1),
            ),
            loader.ConfigValue(
                "empty_emoji",
                "🙈",
                lambda: "Empty modules bullet",
                validator=loader.validators.Emoji(length=1),
            ),
        )

    @loader.command(
        ru_doc=(
            "<модуль или модули> - Спрятать модуль(-и) из помощи\n*Разделяй модули"
            " пробелами"
        )
    )
    async def helphide(self, message: Message):
        """<module or modules> - Hide module(-s) from help
        *Split modules by spaces"""
        modules = utils.get_args(message)
        if not modules:
            await utils.answer(message, self.strings("no_mod"))
            return

        mods = [i.__class__.__name__ for i in self.allmodules.modules]

        modules = list(filter(lambda module: module in mods, modules))
        currently_hidden = self.get("hide", [])
        hidden, shown = [], []
        for module in modules:
            if module in currently_hidden:
                currently_hidden.remove(module)
                shown += [module]
            else:
                currently_hidden += [module]
                hidden += [module]

        self.set("hide", currently_hidden)

        await utils.answer(
            message,
            self.strings("hidden_shown").format(
                len(hidden),
                len(shown),
                "\n".join([f"👁‍🗨 <i>{m}</i>" for m in hidden]),
                "\n".join([f"👁 <i>{m}</i>" for m in shown]),
            ),
        )

    async def modhelp(self, message: Message, args: str):
        exact = True
        module = self.lookup(args)

        if not module:
            _args = args.lower()
            _args = _args[1:] if _args.startswith(self.get_prefix()) else _args
            if _args in self.allmodules.commands:
                module = self.allmodules.commands[_args].__self__

        if not module:
            module = self.lookup(
                next(
                    (
                        reversed(
                            sorted(
                                [
                                    module.strings["name"]
                                    for module in self.allmodules.modules
                                ],
                                key=lambda x: difflib.SequenceMatcher(
                                    None,
                                    args.lower(),
                                    x,
                                ).ratio(),
                            )
                        )
                    ),
                    None,
                )
            )

            exact = False

        try:
            name = module.strings("name")
        except KeyError:
            name = getattr(module, "name", "ERROR")

        _name = (
            "{} (v{}.{}.{})".format(
                utils.escape_html(name),
                module.__version__[0],
                module.__version__[1],
                module.__version__[2],
            )
            if hasattr(module, "__version__")
            else utils.escape_html(name)
        )

        reply = self.strings("single_mod_header").format(_name)
        if module.__doc__:
            reply += "<i>\nℹ️ " + utils.escape_html(inspect.getdoc(module)) + "\n</i>"

        commands = {
            name: func
            for name, func in module.commands.items()
            if await self.allmodules.check_security(message, func)
        }

        if hasattr(module, "inline_handlers"):
            for name, fun in module.inline_handlers.items():
                reply += self.strings("ihandler").format(
                    f"@{self.inline.bot_username} {name}",
                    (
                        utils.escape_html(inspect.getdoc(fun))
                        if fun.__doc__
                        else self.strings("undoc_ihandler")
                    ),
                )

        for name, fun in commands.items():
            reply += self.strings("single_cmd").format(
                self.get_prefix(),
                name,
                (
                    utils.escape_html(inspect.getdoc(fun))
                    if fun.__doc__
                    else self.strings("undoc_cmd")
                ),
            )

        await utils.answer(
            message,
            reply
            + (f"\n\n{self.strings('not_exact')}" if not exact else "")
            + (
                f"\n\n{self.strings('core_notice')}"
                if module.__origin__.startswith("<core")
                else ""
            ),
        )

    @loader.unrestricted
    @loader.command(ru_doc="[модуль] [-f] - Показать помощь")
    async def help(self, message: Message):
        """[module] [-f] - Show help"""
        args = utils.get_args_raw(message)
        force = False
        if "-f" in args:
            args = args.replace(" -f", "").replace("-f", "")
            force = True

        if args:
            await self.modhelp(message, args)
            return

        count = 0
        for i in self.allmodules.modules:
            try:
                if i.commands or i.inline_handlers:
                    count += 1
            except Exception:
                pass

        hidden = self.get("hide", [])

        reply = self.strings("all_header").format(
            count,
            0
            if force
            else len(
                [
                    module
                    for module in self.allmodules.modules
                    if module.__class__.__name__ in hidden
                ]
            ),
        )
        shown_warn = False

        plain_ = []
        core_ = []
        inline_ = []
        no_commands_ = []

        for mod in self.allmodules.modules:
            if not hasattr(mod, "commands"):
                logger.debug("Module %s is not inited yet", mod.__class__.__name__)
                continue

            if mod.__class__.__name__ in self.get("hide", []) and not force:
                continue

            tmp = ""

            try:
                name = mod.strings["name"]
            except KeyError:
                name = getattr(mod, "name", "ERROR")

            inline = (
                hasattr(mod, "callback_handlers")
                and mod.callback_handlers
                or hasattr(mod, "inline_handlers")
                and mod.inline_handlers
            )

            if not inline:
                for cmd_ in mod.commands.values():
                    try:
                        inline = "await self.inline.form(" in inspect.getsource(
                            cmd_.__code__
                        )
                    except Exception:
                        pass

            core = mod.__origin__.startswith("<core")

            if core:
                emoji = self.config["core_emoji"]
            elif inline:
                emoji = self.config["hikka_emoji"]
            else:
                emoji = self.config["plain_emoji"]

            if (
                not getattr(mod, "commands", None)
                and not getattr(mod, "inline_handlers", None)
                and not getattr(mod, "callback_handlers", None)
            ):
                no_commands_ += [
                    self.strings("mod_tmpl").format(self.config["empty_emoji"], name)
                ]
                continue

            tmp += self.strings("mod_tmpl").format(emoji, name)
            first = True

            commands = [
                name
                for name, func in mod.commands.items()
                if await self.allmodules.check_security(message, func) or force
            ]

            for cmd in commands:
                if first:
                    tmp += self.strings("first_cmd_tmpl").format(cmd)
                    first = False
                else:
                    tmp += self.strings("cmd_tmpl").format(cmd)

            icommands = [
                name
                for name, func in mod.inline_handlers.items()
                if await self.inline.check_inline_security(
                    func=func,
                    user=message.sender_id,
                )
                or force
            ]

            for cmd in icommands:
                if first:
                    tmp += self.strings("first_cmd_tmpl").format(f"🎹 {cmd}")
                    first = False
                else:
                    tmp += self.strings("cmd_tmpl").format(f"🎹 {cmd}")

            if commands or icommands:
                tmp += " )"
                if core:
                    core_ += [tmp]
                elif inline:
                    inline_ += [tmp]
                else:
                    plain_ += [tmp]
            elif not shown_warn and (mod.commands or mod.inline_handlers):
                reply = (
                    "<i>You have permissions to execute only these"
                    f" commands</i>\n{reply}"
                )
                shown_warn = True

        plain_.sort(key=lambda x: x.split()[1])
        core_.sort(key=lambda x: x.split()[1])
        inline_.sort(key=lambda x: x.split()[1])
        no_commands_.sort(key=lambda x: x.split()[1])
        no_commands_ = "".join(no_commands_) if force else ""

        partial_load = (
            ""
            if self.lookup("Loader")._fully_loaded
            else f"\n\n{self.strings('partial_load')}"
        )

        await utils.answer(
            message,
            "{}\n{}{}{}{}{}".format(
                reply,
                "".join(core_),
                "".join(plain_),
                "".join(inline_),
                no_commands_,
                partial_load,
            ),
        )

    @loader.command(ru_doc="Показать ссылку на чат помощи Hikka")
    async def support(self, message):
        """Get link of Hikka support chat"""
        if message.out:
            await self.request_join("@hikka_talks", self.strings("request_join"))

        await utils.answer(
            message,
            self.strings("support").format(
                '<emoji document_id="5192765204898783881">🌘</emoji><emoji'
                ' document_id="5195311729663286630">🌘</emoji><emoji'
                ' document_id="5195045669324201904">🌘</emoji>'
                if self._client.hikka_me.premium
                else "🌘",
            ),
        )
