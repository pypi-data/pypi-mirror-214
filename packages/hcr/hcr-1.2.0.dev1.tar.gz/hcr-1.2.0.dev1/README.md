# Handwritten-Character-Recognition

Unstable, dev version.


## Installation



## FAQ



## Limitations

- can only be used in fullscreen mode
- the UI layout is specifically designed for 64x64 inputs and has 36 outputs
- the UI layout is customized for the 1366x768 display size
- The hidden layers are hardcoded with three layers (50, 40, 35)


## Troubleshoot

- To report bugs, please open an issue/pull request, or you can reach me [here](https://nvfp.github.io/contact).


## Changelog

- 1.2.0 (June 13, 2023):

    **Motivation**: To provide a cleaner UI and restructure the codebase.

    - Removed feature: uptime display
    - Removed feature: metadata display (the one in the TL corner)
    - Removed feature: datasets stats display (the one in the TR corner)
    - Removed feature: static labels ("64x64", "size: [...]")
    - File name changed: `main/misc.py` -> `main/constants.py`
    - Dependencies updates: `mykit==1.0.0` -> `mykit==2.0.2`
    - Added 'settings' and 'CLI' feature
- 1.1.0 (June 11, 2023):
    - removed `carbon_plug`, using [mykit](https://github.com/nvfp/mykit) instead
- v1.0.1 (May 10, 2023):
    - BUG FIXED: Renamed `carbon` to `carbon_plug` to prevent conflicts with the original `carbon` module (if installed).


## License

This project is licensed under the MIT license.
