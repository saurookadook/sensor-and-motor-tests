# sensor-and-motor-tests

## Overview

Just some initial attempts at using sensors and motors for the LEGO EV3 Brick.

_...and will likely becoming a sort of place for misfit code_ 🙃

---

## General Dev

- [Connecting to EV3dev Using SSH](https://www.ev3dev.org/docs/tutorials/connecting-to-ev3dev-with-ssh/)

```bash
$ ssh robot@ev3dev.local
```
_default password is `maker`_


Printing to VS Code terminal:
- https://github.com/ev3dev/ev3dev/issues/1307

---

### Debugging Snippets

```python
all_motors = list_devices("dc-motor", "*")

print(("-" * 30) + " all_motors " + ("-" * 30), file=sys.stderr)
    for motor in all_motors:
        print(motor, file=sys.stderr)
        motor_members = getmembers(motor)
        for member_tup in motor_members:
            name, value = member_tup
            print("name: {}".format(name), file=sys.stderr)
            print("value: {}".format(value), file=sys.stderr)


```

---

### Quirks

- https://stackoverflow.com/questions/57483794/python-shlex-no-closing-quotations-error-how-to-deal-with
- [\[Question\] How can we ev3devBrowser.download.exclude multiple patterns? #104](https://github.com/ev3dev/vscode-ev3dev-browser/issues/104)
    - **answer**: use `ev3devBrowser.download.exclude: "GlobPattern"` _(see [Glob-Patterns](https://github.com/ev3dev/vscode-ev3dev-browser/wiki/Glob-Patterns))_
    - _suggested:_ `"ev3devBrowser.download.exclude": "{**/.*/*,**/tests/*}",`

---

### Resources

- [ev3dev-lang-python](https://github.com/ev3dev/ev3dev-lang-python)
- [Mindstorms EV3 - Building Instructions](https://education.lego.com/en-us/product-resources/mindstorms-ev3/downloads/building-instructions)
