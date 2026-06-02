from __future__ import annotations

from clargparse import Command, ParseMode, actions, numargs


ban = Command("ban", parse_mode=ParseMode.POSITIONAL)
ban.option("delete", "d", action=actions.store_true_action, default=False)
ban.option("until", "u")
ban.option("reason", "r", action=actions.extend_values_action, num_args=numargs.ZERO_OR_MORE)
ban.positional("peers", action=actions.extend_values_action, num_args=numargs.ONE_OR_MORE)

parsed = ban.parse_input("-d 1d @user_1 -r hi 2 ol")

print(parsed.values)  # noqa: T201
