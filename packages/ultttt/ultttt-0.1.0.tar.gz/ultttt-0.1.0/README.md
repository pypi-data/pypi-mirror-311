# Ultimate tic-tac-toe

♟️ Ultimate tic-tac-toe game GUI application using Python and PyGame

<p align=center>
  <img src="https://github.com/user-attachments/assets/c6fd92b5-f10a-4507-8627-4acdddd829ba">
</p>

🎨 Has a GUI! \
🤖 Uses GitHub Actions to produce PyInstaller binaries \
🏫 Made for UW-Whitewater Introduction to Python Programming final project \
🧠 Learned about [uv](https://docs.astral.sh/uv/)

## Installation

![GitHub](https://img.shields.io/static/v1?style=for-the-badge&message=GitHub&color=181717&logo=GitHub&logoColor=FFFFFF&label=)
![PyPI](https://img.shields.io/static/v1?style=for-the-badge&message=PyPI&color=3775A9&logo=PyPI&logoColor=FFFFFF&label=)

The best way to install this application is to download the platform-specific precompiled binary from [the latest release](https://github.com/jcbhmr/ultttt/releases/latest).

<dl>
<dt>Windows x86-64
<dd>https://github.com/jcbhmr/ultttt/releases/latest/download/ultttt-win_amd64.zip
<dt>macOS x86-64
<dd>https://github.com/jcbhmr/ultttt/releases/latest/download/ultttt-win_amd64.zip
<dt>macOS AArch64
<dd>https://github.com/jcbhmr/ultttt/releases/latest/download/ultttt-win_amd64.zip
<dt>Linux x86-64
<dd>https://github.com/jcbhmr/ultttt/releases/latest/download/ultttt-win_amd64.zip
</dl>

This package is also published to PyPI if you prefer to install it from there:

```sh
uv tool install ultttt
```

## Development

![Python](https://img.shields.io/static/v1?style=for-the-badge&message=Python&color=3776AB&logo=Python&logoColor=FFFFFF&label=)
![uv](https://img.shields.io/static/v1?style=for-the-badge&message=uv&color=DE5FE9&logo=uv&logoColor=FFFFFF&label=)

This project uses [uv](https://docs.astral.sh/uv/) as its Python toolchain. Why uv and not Poetry or something else? Because uv unifies everything _including installing the right Python version_. uv is [not a task runner yet](https://github.com/astral-sh/uv/issues/5903) and as such we use [Poe the Poet](https://poethepoet.natn.io/) to define our tasks.

The most interesting thing to do is build the `ultttt` executable binary using [PyInstaller](https://pyinstaller.org/):

```sh
uv run poe build-exe
```
