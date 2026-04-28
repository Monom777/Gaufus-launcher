#!/usr/bin/python3
"""
Faugus Launcher - GTK 4 + Libadwaita Version
A modern system utility launcher for games and applications.
"""

import json
import os
import re
import shutil
import subprocess
import sys
import threading
from pathlib import Path

import gi
gi.require_version('Adw', '1')
from gi.repository import Adw, Gtk, Gdk, GLib, Gio, Pango

from faugus.config_manager import ConfigManager
from faugus.path_manager import PathManager
from faugus.components import update_umu, check_for_updates
from faugus.settings_adw import SettingsWindow

VERSION = "2.0.0"
IS_FLATPAK = 'FLATPAK_ID' in os.environ or os.path.exists('/.flatpak-info')

# Paths
faugus_launcher_dir = PathManager.user_config('faugus-launcher')
prefixes_dir = str(Path.home() / 'Faugus')
logs_dir = PathManager.user_config('faugus-launcher/logs')
icons_dir = PathManager.user_config('faugus-launcher/icons')
banners_dir = PathManager.user_config('faugus-launcher/banners')
config_file_dir = PathManager.user_config('faugus-launcher/config.ini')
envar_dir = PathManager.user_config('faugus-launcher/envar.txt')
games_json = PathManager.user_config('faugus-launcher/games.json')
running_games = PathManager.user_data('faugus-launcher/running_games.json')

# Ensure directories exist
os.makedirs(faugus_launcher_dir, exist_ok=True)
os.makedirs(logs_dir, exist_ok=True)
os.makedirs(icons_dir, exist_ok=True)
os.makedirs(banners_dir, exist_ok=True)

# Initialize running games file
if not os.path.exists(running_games):
    os.makedirs(os.path.dirname(running_games), exist_ok=True)
    with open(running_games, 'w') as f:
        json.dump({}, f)


class Game:
    """Represents a game entry."""
    def __init__(self, gameid, title, path, prefix, runner, favorite=False, hidden=False, playtime=0):
        self.gameid = gameid
        self.title = title
        self.path = path
        self.prefix = prefix
        self.runner = runner
        self.favorite = favorite
        self.hidden = hidden
        self.playtime = playtime


class FaugusLauncher(Adw.Application):
    """Main application class using GTK 4 and Libadwaita."""
    
    def __init__(self):
        super().__init__(application_id="io.github.Faugus.faugus-launcher",
                        flags=Gio.ApplicationFlags.FLAGS_NONE)
        
        self.window = None
        self.config_manager = ConfigManager()
        self.games = []
        self.running = {}
        self.processes = {}
        self.interface_mode = "List"
        
    def do_startup(self):
        """Application startup - setup styles and resources."""
        Adw.Application.do_startup(self)
        
        # Setup dark mode using Adw.StyleManager
        style_manager = Adw.StyleManager.get_default()
        style_manager.set_color_scheme(Adw.ColorScheme.PREFER_DARK)
        
        # Load configuration
        self.load_config()
        
    def do_activate(self):
        """Application activation - show main window."""
        if not self.window:
            self.window = MainWindow(self, self.config_manager)
            
        self.window.present()
        
    def load_config(self):
        """Load application configuration."""
        cfg = self.config_manager.config
        self.interface_mode = cfg.get('interface-mode', 'List')
        

class MainWindow(Adw.ApplicationWindow):
    """Main application window."""
    
    def __init__(self, app, config_manager):
        super().__init__(application=app, title="Gaufus Launcher")
        self.set_default_size(1200, 800)
        
        self.app = app
        self.config_manager = config_manager
        self.toast_overlay = None
        self.games = {}  # Ініціалізація словника для ігор
        self.game_buttons = {}  # Ініціалізація словника для кнопок
        
        # Build UI
        self.build_ui()
        
        # Load games
        self.load_games()
        
        # Start periodic check for running games
        GLib.timeout_add_seconds(1, self.check_running())
        
    def build_ui(self):
        """Build the main UI layout."""
        # Toast overlay for notifications
        self.toast_overlay = Adw.ToastOverlay()
        self.set_child(self.toast_overlay)
        
        # Main vertical box
        main_box = Gtk.Box(orientation=Gtk.Orientation.VERTICAL)
        self.toast_overlay.set_child(main_box)
        
        # Header bar
        header_bar = Adw.HeaderBar()
        header_bar.set_show_end_title_buttons(True)
        main_box.append(header_bar)
        
        # Search entry (hidden by default)
        search_entry = Gtk.SearchEntry()
        search_entry.set_placeholder_text("Search games...")
        search_entry.connect('search-changed', self.on_search_changed)
        search_entry.set_hexpand(True)
        search_entry.set_max_width_chars(30)
        
        # Clamp for centered content
        clamp = Adw.Clamp()
        clamp.set_maximum_size(600)
        clamp.set_child(search_entry)
        
        header_bar.pack_start(clamp)
        
        # Settings button
        settings_button = Gtk.Button()
        settings_icon = Gtk.Image.new_from_icon_name("preferences-system-symbolic")
        settings_button.set_child(settings_icon)
        settings_button.set_tooltip_text("Settings")
        settings_button.connect('clicked', self.on_settings_clicked)
        header_bar.pack_end(settings_button)
        
        # Add game button
        add_button = Gtk.Button()
        add_icon = Gtk.Image.new_from_icon_name("list-add-symbolic")
        add_button.set_child(add_icon)
        add_button.set_tooltip_text("Add Game")
        add_button.connect('clicked', self.on_add_game_clicked)
        header_bar.pack_end(add_button)
        
        # Stack for different views
        self.stack = Gtk.Stack()
        self.stack.set_vexpand(True)
        self.stack.set_transition_type(Gtk.StackTransitionType.CROSSFADE)
        main_box.append(self.stack)
        
        # Games view
        games_scrolled = Gtk.ScrolledWindow()
        games_scrolled.set_policy(Gtk.PolicyType.NEVER, Gtk.PolicyType.AUTOMATIC)
        games_scrolled.set_vexpand(True)
        
        # FlowBox for games list
        self.flowbox = Gtk.FlowBox()
        self.flowbox.set_selection_mode(Gtk.SelectionMode.SINGLE)
        self.flowbox.set_min_children_per_line(1)
        self.flowbox.set_max_children_per_line(4)
        self.flowbox.set_row_spacing(10)
        self.flowbox.set_column_spacing(10)
        self.flowbox.set_homogeneous(True)
        self.flowbox.connect('child-activated', self.on_game_activated)
        
        games_scrolled.set_child(self.flowbox)
        self.stack.add_named(games_scrolled, "games")
        
        # Empty state view
        empty_box = Gtk.Box(orientation=Gtk.Orientation.VERTICAL)
        empty_box.set_spacing(20)
        empty_box.set_halign(Gtk.Align.CENTER)
        empty_box.set_valign(Gtk.Align.CENTER)
        
        empty_image = Gtk.Image.new_from_icon_name("folder-saved-search-symbolic")
        empty_image.set_pixel_size(128)
        empty_box.append(empty_image)
        
        empty_label = Gtk.Label(label="No games added yet.\nClick the + button to add your first game.")
        empty_label.set_justify(Gtk.Justification.CENTER)
        empty_box.append(empty_label)
        
        self.stack.add_named(empty_box, "empty")
        
        # Status bar
        status_bar = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL)
        status_bar.set_css_classes(["statusbar"])
        status_bar.set_margin_start(10)
        status_bar.set_margin_end(10)
        status_bar.set_margin_top(5)
        status_bar.set_margin_bottom(5)
        
        self.status_label = Gtk.Label(label="Ready")
        self.status_label.set_halign(Gtk.Align.START)
        self.status_label.set_hexpand(True)
        status_bar.append(self.status_label)
        
        main_box.append(status_bar)
        
    def load_games(self):
        """Load games from JSON file."""
        try:
            with open(games_json, "r", encoding="utf-8") as f:
                games_data = json.load(f)
                
            self.games = {}  # Reset dictionary
            for game_data in games_data:
                game_id = game_data.get("gameid", "")
                game = Game(
                    gameid=game_id,
                    title=game_data.get("title", ""),
                    path=game_data.get("path", ""),
                    prefix=game_data.get("prefix", ""),
                    runner=game_data.get("runner", ""),
                    favorite=game_data.get("favorite", False),
                    hidden=game_data.get("hidden", False),
                    playtime=game_data.get("playtime", 0)
                )
                self.games[game_id] = game
                
            # Sort games by title
            sorted_games = sorted(self.games.values(), key=lambda x: x.title.lower())
            self.games = {g.gameid: g for g in sorted_games}
            
            # Update UI
            self.update_games_list()
            
        except FileNotFoundError:
            self.show_empty_state()
        except json.JSONDecodeError as e:
            self.show_toast(f"Error reading games file: {e}")
            
    def update_games_list(self):
        """Update the games FlowBox."""
        # Clear existing children
        child = self.flowbox.get_first_child()
        while child:
            next_child = child.get_next_sibling()
            self.flowbox.remove(child)
            child = next_child
            
        if not self.games:
            self.show_empty_state()
            return
            
        # Add games to FlowBox
        for game_id, game in self.games.items():
            widget = self.create_game_widget(game)
            self.flowbox.append(widget)
            
        self.stack.set_visible_child_name("games")
        
    def create_game_widget(self, game):
        """Create a widget for a game entry."""
        box = Gtk.Box(orientation=Gtk.Orientation.VERTICAL)
        box.set_css_classes(["card"])
        box.set_margin_start(10)
        box.set_margin_end(10)
        box.set_margin_top(10)
        box.set_margin_bottom(10)
        
        # Icon
        icon_path = f"{icons_dir}/{game.gameid}.ico"
        if not os.path.exists(icon_path):
            icon_path = None
            
        if icon_path and os.path.exists(icon_path):
            try:
                pixbuf = GdkPixbuf.Pixbuf.new_from_file_at_scale(icon_path, 64, 64, True)
                image = Gtk.Image.new_from_pixbuf(pixbuf)
            except:
                image = Gtk.Image.new_from_icon_name("applications-games")
                image.set_pixel_size(64)
        else:
            image = Gtk.Image.new_from_icon_name("applications-games")
            image.set_pixel_size(64)
            
        image.set_halign(Gtk.Align.CENTER)
        box.append(image)
        
        # Title label
        label = Gtk.Label(label=game.title)
        label.set_wrap(True)
        label.set_lines(2)
        label.set_ellipsize(Pango.EllipsizeMode.END)
        label.set_justify(Gtk.Justification.CENTER)
        label.set_margin_top(5)
        box.append(label)
        
        # Store game reference
        box.game = game
        
        return box
        
    def show_empty_state(self):
        """Show empty state view."""
        self.stack.set_visible_child_name("empty")
        
    def on_game_activated(self, flowbox, child):
        """Handle game activation (double-click)."""
        box = child.get_child()
        game = getattr(box, 'game', None)
        if game:
            self.launch_game(game)
            
    def launch_game(self, game):
        """Launch a game."""
        self.show_toast(f"Launching {game.title}...")
        # TODO: Implement actual game launching logic
        # This would use the existing subprocess logic from the original launcher
        
    def on_search_changed(self, entry):
        """Handle search text change."""
        search_text = entry.get_text().lower()
        
        child = self.flowbox.get_first_child()
        while child:
            box = child.get_child()
            game = getattr(box, 'game', None)
            if game:
                visible = search_text in game.title.lower()
                child.set_visible(visible)
            child = child.get_next_sibling()
            
    def on_settings_clicked(self, button):
        """Open settings dialog."""
        settings_dialog = SettingsWindow(self, self.config_manager)
        settings_dialog.load_config()
        settings_dialog.present(self)
        
    def on_add_game_clicked(self, button):
        """Open add game dialog."""
        self.show_toast("Add game functionality coming soon")
        
    def show_toast(self, message, timeout=3):
        """Show a toast notification."""
        toast = Adw.Toast(title=message, timeout=timeout)
        self.toast_overlay.add_toast(toast)
        
    def check_running(self):
        """Periodically check for running games."""
        # Check processes we started
        for gameid, proc in list(self.processes.items()):
            if proc.poll() is not None:
                self.processes.pop(gameid, None)
                self.running.pop(gameid, None)
                
        # Save running games state
        try:
            with open(running_games, 'w') as f:
                json.dump(self.running, f)
        except:
            pass
            
        return GLib.SOURCE_CONTINUE


def main():
    """Main entry point."""
    app = FaugusLauncher()
    app.run(sys.argv)


if __name__ == "__main__":
    main()
