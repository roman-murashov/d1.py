# d1.py

This project provides scripts for interacting with Diablo 1 from Python.

## Installation on Windows

1. Install [MSYS2](https://www.msys2.org/).
2. Launch MSYS2 terminal.
3. `pacman -Sy mingw-w64-x86_64-llvm mingw-w64-x86_64-lldb`
4. `go get -u github.com/mewkiz/cmd/sar`
5. `make -C typ`

**Note**, the MSYS2 Windows port of LLDB is currently lacking Python support (see [upstream issue](https://github.com/Alexpux/MINGW-packages/issues/3222)).

## Installation on Linux

1. `pacman -Sy lldb`
2. `go get -u github.com/mewkiz/cmd/sar`
3. `make -C typ`

## Usage

The following example changes the name of the item equipped in the right hand to *Hello from Python*.

```bash
$ sudo python2 -i d1.py
>>> player = get_player()
>>> player.x
75
>>> player.y
68
>>> stream = BytesIO(b'Hello from Python')
>>> stream.readinto(ffi.buffer(player.body_items[4].unidentified_name))
>>> set_player(player)
```

![Interacting with Diablo 1 from Python](https://raw.githubusercontent.com/sanctuary/graphics/master/djavul/screenshot_2018-04-21.png)
