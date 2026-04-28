# Faugus Launcher - GTK 4 + Libadwaita Refactoring Guide

## Overview

This document describes the refactored version of Faugus Launcher, migrated from GTK 3 to **GTK 4 + Libadwaita 1.x**. The new implementation provides a modern, polished UI that fits the WhiteSur-Dark theme and follows GNOME HIG guidelines.

## New Files

### `faugus/launcher_gtk4.py`
The main application entry point using GTK 4 and Libadwaita:
- Uses `Adw.Application` as the base application class
- Implements `Adw.ApplicationWindow` for the main window
- Uses `Adw.ToastOverlay` for non-intrusive notifications
- Manages dark mode via `Adw.StyleManager`

### `faugus/settings_adw.py`
Modern settings dialog using Libadwaita's preferences system:
- Extends `Adw.PreferencesDialog`
- Uses `Adw.PreferencesPage` and `Adw.PreferencesGroup` for organized settings
- Maps all existing config options to `Adw.ActionRow` elements with appropriate widgets
- Integrates with `ConfigManager` for loading/saving settings

## Key Changes from GTK 3

### 1. Application Structure

**GTK 3 (Old):**
```python
class FaugusApp(Gtk.Application):
    def do_startup(self):
        Gtk.Application.do_startup(self)
        apply_dark_theme()  # Custom function
```

**GTK 4 + Libadwaita (New):**
```python
class FaugusLauncher(Adw.Application):
    def do_startup(self):
        Adw.Application.do_startup(self)
        style_manager = Adw.StyleManager.get_default()
        style_manager.set_color_scheme(Adw.ColorScheme.PREFER_DARK)
```

### 2. Main Window

**GTK 3 (Old):**
```python
class Main(Gtk.ApplicationWindow):
    def __init__(self, app):
        super().__init__(application=app, title="Faugus Launcher")
        self.add(main_box)  # GTK 3 uses add()
```

**GTK 4 + Libadwaita (New):**
```python
class MainWindow(Adw.ApplicationWindow):
    def __init__(self, app, config_manager):
        super().__init__(application=app, title="Faugus Launcher")
        self.set_child(toast_overlay)  # GTK 4 uses set_child()
```

### 3. Header Bar

**GTK 3 (Old):**
```python
header_bar = Gtk.HeaderBar()
header_bar.set_show_close_button(True)
self.set_titlebar(header_bar)
```

**GTK 4 + Libadwaita (New):**
```python
header_bar = Adw.HeaderBar()
main_box.append(header_bar)  # Integrated into layout
```

### 4. Notifications

**GTK 3 (Old):**
```python
dialog = Gtk.MessageDialog(...)
dialog.run()
dialog.destroy()
```

**GTK 4 + Libadwaita (New):**
```python
toast = Adw.Toast(title=message, timeout=3)
self.toast_overlay.add_toast(toast)
```

### 5. Settings Dialog

**GTK 3 (Old):**
```python
class Settings(Gtk.Dialog):
    # Manual layout with Gtk.Grid, Gtk.Box
    # Individual widgets for each setting
```

**GTK 4 + Libadwaita (New):**
```python
class SettingsWindow(Adw.PreferencesDialog):
    def build_preferences(self):
        page = Adw.PreferencesPage()
        group = Adw.PreferencesGroup()
        row = Adw.ActionRow()
        row.add_suffix(switch)
```

## Configuration Integration

The refactored code fully integrates with `config_manager.py`:

```python
from faugus.config_manager import ConfigManager

# Load config
config_manager = ConfigManager()
cfg = config_manager.config

# Access settings
interface_mode = cfg.get('interface-mode', 'List')
mangohud_enabled = cfg.get('mangohud', 'False') == 'True'

# Save settings
config_manager.set_value('interface-mode', 'Blocks')
config_manager.save_config()
```

## Preserved Functionality

The following functionality is preserved from the original:
- ✅ Game library management (load, display, search)
- ✅ Configuration persistence via `config_manager.py`
- ✅ Subprocess logic for launching games (to be integrated)
- ✅ Running games tracking
- ✅ All user settings mapped to new UI

## Modern Features Added

1. **Toast Notifications**: Non-blocking notifications using `Adw.ToastOverlay`
2. **Search Functionality**: Built-in search bar in header
3. **Responsive Layout**: Uses `Adw.Clamp` for optimal content width
4. **Dark Mode Management**: Automatic via `Adw.StyleManager`
5. **Preferences Organization**: Grouped settings with descriptions
6. **Card-style Game Widgets**: Modern card-based game entries

## Dependencies

```python
import gi
gi.require_version('Adw', '1')
from gi.repository import Adw, Gtk, Gdk, GLib, Gio, Pango
```

Required system packages:
- `libadwaita-1-dev` (or `libadwaita-1-0`)
- `gir1.2-adw-1`
- `python3-gi`
- `python3-gi-cairo`

## Running the Application

```bash
python3 faugus/launcher_gtk4.py
```

## Migration Checklist

- [x] Create `Adw.Application` subclass
- [x] Create `Adw.ApplicationWindow` main window
- [x] Implement `Adw.HeaderBar` with proper layout
- [x] Add `Adw.ToastOverlay` for notifications
- [x] Setup `Adw.StyleManager` for dark mode
- [x] Create `Adw.PreferencesDialog` for settings
- [x] Map all config options to `Adw.ActionRow` elements
- [x] Integrate with `ConfigManager` for load/save
- [x] Preserve subprocess launch logic
- [ ] Complete game launch integration
- [ ] Add Proton Manager integration
- [ ] Implement context menus for games
- [ ] Add gamepad navigation support

## Style Guidelines

The new UI follows these principles:
1. **Clean**: Minimal visual clutter, clear hierarchy
2. **Modular**: Separated concerns (UI, config, logic)
3. **Performance-oriented**: Efficient widget creation, lazy loading
4. **Consistent**: Follows GNOME HIG and Libadwaita patterns

## Next Steps

To complete the migration:

1. **Integrate Game Launching**: Port the subprocess logic from `runner.py`
2. **Add Game Dialog**: Create `Adw.Dialog` or modal for adding/editing games
3. **Context Menus**: Implement `Gtk.PopoverMenu` for right-click actions
4. **Proton Manager**: Create dedicated preferences page for Proton management
5. **System Tray**: Use `Gtk.StatusIcon` or portal-based tray integration
6. **Testing**: Verify all settings persist correctly across sessions
