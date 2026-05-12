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
root = Command("root")

root.option("--verbose", "-v", action=store_true_action)
root.option("--count", "-c", action=count_presence_action)

source = "root -v -c -c"
print(root.parse_input(source))
```

---

## Example: Subcommands

```py
root = Command("root")

mv = root.subcommand("mv")
mv.positional("src")
mv.positional("dest")

cp = root.subcommand("cp")
cp.positional("src")
cp.positional("dest")

source = "cp a.txt b.txt"
print(root.parse_input(source))
```

---

## Example: Mutex Option Groups

```py
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

## NArgs

Controls how many values an argument consumes:

```py
class NArgs(StrEnum):
    OPTIONAL = "?"
    ZERO_OR_MORE = "*"
    ONE_OR_MORE = "+"
```

---

## Built-in Actions

### store_value_action
```py
store_value_action(option, values)
```

### store_present_action
```py
store_present_action(option, values)
```

### store_true_action
```py
store_true_action(option, values)
```

### store_false_action
```py
store_false_action(option, values)
```

### append_present_action
```py
append_present_action(option, values)
```

### append_value_action
```py
append_value_action(option, values)
```

### extend_value_action
```py
extend_value_action(option, values)
```

### count_presence_action
```py
count_presence_action(option, values)
```

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
