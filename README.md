# cliargparse (Beta)

A structured CLI argument parser for Python.

> ⚠️ Beta: API is stable in design, but may still evolve.

---

## Philosophy

Everything is built around a unified model:

- Commands
- Subcommands
- Options
- Positionals
- Mutex option groups

All are first-class and composable.

---

## Example: Basic Positionals

```py
from cliargparse import Command, ParseMode

root = Command("root")

mv = root.subcommand("mv", parse_mode=ParseMode.POSITIONAL)
mv.positional("src")
mv.positional("dest")

source = "mv file1 file2"
print(root.parse_input(source))
```

---

## Example: Options + Actions

```py
from cliargparse import Command
from cliargparse.actions import store_true_action, count_presence_action

root = Command("root")

root.option("--verbose", "-v", action=store_true_action)
root.option("--count", "-c", action=count_presence_action)

source = "root -v -c -c"
print(root.parse_input(source))
```

---

## Example: Subcommands

```py
from cliargparse import Command, ParseMode

root = Command("root")

mv = root.subcommand("mv", parse_mode=ParseMode.POSITIONAL)
mv.positional("src")
mv.positional("dest")

cp = root.subcommand("cp", parse_mode=ParseMode.POSITIONAL)
cp.positional("src")
cp.positional("dest")

source = "cp a.txt b.txt"
print(root.parse_input(source))
```

---

## Example: Mutex Option Groups

```py
from cliargparse import Command
from cliargparse.actions import store_true_action

root = Command("root")

group = root.mutex_option_group(required=True)
group.option("--alpha", "-a", action=store_true_action)
group.option("--beta", "-b", action=store_true_action)
group.option("--ceta", "-c", action=store_true_action)

source = "root --alpha --beta"
print(root.parse_input(source))
```

Only one option in a mutex group can be provided.

---

## Summary

cliargparse is designed to be:

- Predictable
- Strict
- Composable
- Explicit in behavior

---

## License

MIT
