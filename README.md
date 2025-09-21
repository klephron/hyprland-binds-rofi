# hyprland-binds-rofi

Access and execute defined binds using rofi.

## Preview

![image](https://github.com/user-attachments/assets/689ca6c6-1ece-447a-a2c3-2e7d2e2b2d4b)

## Requirements

- `python`
- `rofi`
- `hyprland`

## Installation

1. Download the script [`main.py`](./main.py)

2. Configure hyprland to execute it. For example:

```
# SUPER + ?
bind = SUPER_SHIFT, slash, exec, python $XDG_CONFIG_HOME/hypr/scripts/rofi_binds.py
```

## Acknowledgements

Appreciation to the contributors, which provided important inspiration and reference for the development:

- [mellotanica/rofi-hyprland-keybinds-cheatsheet](https://github.com/mellotanica/rofi-hyprland-keybinds-cheatsheet)
