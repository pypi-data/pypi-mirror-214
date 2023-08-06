# Maestro

<img src="https://framagit.org/Blaireau/maestro/-/raw/main/icons/maestro.svg" height="64">

A keyboard-centric configurable music player

<img src="https://framagit.org/Blaireau/maestro/-/raw/main/screenshots/collection.png" height="512">

<img src="https://framagit.org/Blaireau/maestro/-/raw/main/screenshots/queue.png" height="512">

## Design principles

- **focus on user interaction**:  
maestro is a only a front-end application, playing the actual audio is delegated to well-know applications like mpv or vlc

- **keyboard driven**:  
all interaction with maestro is done through keyboard shortcuts and command lines, which allows for a clean and minimalist interface

- **configurable**:  
the modular command system and the various configuration options allows you to adapt maestro to your workflow (and not the opposite)

## Requirements

Maestro is made with python. You need `python>=3.10` to run maestro.

You also need one of the supported audio backend to play the music.
Currently supported backends are [mpv](https://mpv.io/) and [vlc](https://www.videolan.org/vlc/).
Install whichever you like or whichever works best for you.

As an optional dependency, you may install `xdotool`, which is used to properly set the `WM_CLASS` attribute of the window. This will help you if you want to add specific rules for maestro in your window manager.

## Installation

Clone the repository and run the `install` script.

```
git clone https://framagit.org/Blaireau/maestro.git
cd maestro
./install
```

This will install maestro on your system (setup desktop file and icons and put maestro on your path).

After installation, you will need to setup a few things before you can use maestro.
See `maestro help setup`.

## Documentation

All the documentation is included with the application.
Simply type `maestro help` to get started.
    
## Support: getting help or reporting bugs

Please use the [issue tracker](https://framagit.org/Blaireau/maestro/-/issues) or contact [rabbitstemplate@disroot.org](mailto:rabbitstemplate@disroot.org).

## Reinstalling, uninstalling

In case you don’t want to use maestro anymore, or want to uninstall it before reinstalling it, you can run the following commands.

```
cd maestro
./uninstall
```

This will remove maestro and all it’s associated files from your system, except for configuration files and the cloned repository, you will have to remove those manually. 

## Contributing

You are welcome to contribute to the project !
You can report bugs, improve the documentation, suggest new features… 
For that, use the [issue tracker](https://framagit.org/Blaireau/maestro/-/issues) or send an email to [rabbitstemplate@disroot.org](mailto:rabbitstemplate@disroot.org).

## License

Maestro is [free software](https://en.wikipedia.org/wiki/Free_software), released under GPLv3 with the exception of a few assets which are under their respective license.

## Credits

A huge thanks to all the tools this project relies on:
- the programming language [python](https://www.python.org/)
- the graphical interface library [kivy](https://kivy.org/)
- [mpv](https://mpv.io/) and [vlc](https://www.videolan.org/vlc/) for the audio backend

And on specific points:

For how to handle the recycle view:
- https://github.com/FilipeMarch/Smart-RecycleView-Kivy

For the monospaced font:
- https://fontlibrary.org/en/font/natural-mono
