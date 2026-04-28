#!/usr/bin/python3

import gi
gi.require_version('Adw', '1')
from gi.repository import Adw, Gtk, Gdk, GLib, Gio

class SettingsWindow(Adw.PreferencesWindow):
    """Modern settings dialog using Libadwaita preferences system."""
    
    def __init__(self, parent, config_manager):
        super().__init__()
        self.set_title("Settings")
        self.set_modal(True)
        self.set_searchable(True)
        
        self.parent = parent
        self.config_manager = config_manager
        
        # Build the preferences page
        self.build_preferences()
        
    def build_preferences(self):
        """Build the preferences UI using Adw components."""
        page = Adw.PreferencesPage()
        page.set_title("Preferences")
        page.set_icon_name("preferences-system-symbolic")
        
        # Interface Group
        interface_group = Adw.PreferencesGroup()
        interface_group.set_title("Interface")
        interface_group.set_description("Customize the appearance and behavior")
        
        # Interface Mode
        row_interface_mode = Adw.ActionRow()
        row_interface_mode.set_title("Interface Mode")
        
        combo_interface = Gtk.ComboBoxText()
        combo_interface.append("List", "List")
        combo_interface.append("Blocks", "Blocks")
        combo_interface.append("Banners", "Banners")
        combo_interface.set_valign(Gtk.Align.CENTER)
        row_interface_mode.add_suffix(combo_interface)
        row_interface_mode.set_activatable_widget(combo_interface)
        interface_group.add(row_interface_mode)
        
        # Start Maximized
        row_start_maximized = Adw.ActionRow()
        row_start_maximized.set_title("Start maximized")
        switch_start_maximized = Gtk.Switch()
        switch_start_maximized.set_valign(Gtk.Align.CENTER)
        row_start_maximized.add_suffix(switch_start_maximized)
        row_start_maximized.set_activatable_widget(switch_start_maximized)
        interface_group.add(row_start_maximized)
        
        # Start Fullscreen
        row_start_fullscreen = Adw.ActionRow()
        row_start_fullscreen.set_title("Start in fullscreen")
        row_start_fullscreen.set_subtitle("Alt+Enter toggles fullscreen")
        switch_start_fullscreen = Gtk.Switch()
        switch_start_fullscreen.set_valign(Gtk.Align.CENTER)
        row_start_fullscreen.add_suffix(switch_start_fullscreen)
        row_start_fullscreen.set_activatable_widget(switch_start_fullscreen)
        interface_group.add(row_start_fullscreen)
        
        # Show Labels
        row_show_labels = Adw.ActionRow()
        row_show_labels.set_title("Show labels")
        switch_show_labels = Gtk.Switch()
        switch_show_labels.set_valign(Gtk.Align.CENTER)
        row_show_labels.add_suffix(switch_show_labels)
        row_show_labels.set_activatable_widget(switch_show_labels)
        interface_group.add(row_show_labels)
        
        # Smaller Banners
        row_smaller_banners = Adw.ActionRow()
        row_smaller_banners.set_title("Smaller banners")
        switch_smaller_banners = Gtk.Switch()
        switch_smaller_banners.set_valign(Gtk.Align.CENTER)
        row_smaller_banners.add_suffix(switch_smaller_banners)
        row_smaller_banners.set_activatable_widget(switch_smaller_banners)
        interface_group.add(row_smaller_banners)
        
        # Gamepad Navigation
        row_gamepad = Adw.ActionRow()
        row_gamepad.set_title("Gamepad navigation")
        switch_gamepad = Gtk.Switch()
        switch_gamepad.set_valign(Gtk.Align.CENTER)
        row_gamepad.add_suffix(switch_gamepad)
        row_gamepad.set_activatable_widget(switch_gamepad)
        interface_group.add(row_gamepad)
        
        # Show Hidden Games
        row_show_hidden = Adw.ActionRow()
        row_show_hidden.set_title("Show hidden games")
        row_show_hidden.set_subtitle("Press Ctrl+H to show/hide games.")
        switch_show_hidden = Gtk.Switch()
        switch_show_hidden.set_valign(Gtk.Align.CENTER)
        row_show_hidden.add_suffix(switch_show_hidden)
        row_show_hidden.set_activatable_widget(switch_show_hidden)
        interface_group.add(row_show_hidden)
        
        page.add(interface_group)
        
        # Paths Group
        paths_group = Adw.PreferencesGroup()
        paths_group.set_title("Paths")
        paths_group.set_description("Configure default locations")
        
        # Default Prefix
        row_default_prefix = Adw.ActionRow()
        row_default_prefix.set_title("Default Prefixes Location")
        
        entry_default_prefix = Gtk.Entry()
        entry_default_prefix.set_placeholder_text("/path/to/the/prefix")
        entry_default_prefix.set_valign(Gtk.Align.CENTER)
        entry_default_prefix.set_width_chars(30)
        row_default_prefix.add_suffix(entry_default_prefix)
        row_default_prefix.set_activatable_widget(entry_default_prefix)
        paths_group.add(row_default_prefix)
        
        # Lossless Scaling Location
        row_lossless = Adw.ActionRow()
        row_lossless.set_title("Lossless Scaling Location")
        
        entry_lossless = Gtk.Entry()
        entry_lossless.set_placeholder_text("/path/to/Lossless.dll")
        entry_lossless.set_valign(Gtk.Align.CENTER)
        entry_lossless.set_width_chars(30)
        row_lossless.add_suffix(entry_lossless)
        row_lossless.set_activatable_widget(entry_lossless)
        paths_group.add(row_lossless)
        
        page.add(paths_group)
        
        # Proton Group
        proton_group = Adw.PreferencesGroup()
        proton_group.set_title("Proton")
        proton_group.set_description("Configure Proton compatibility tools")
        
        # Default Proton
        row_default_runner = Adw.ActionRow()
        row_default_runner.set_title("Default Proton")
        
        combo_runner = Gtk.ComboBoxText()
        combo_runner.set_valign(Gtk.Align.CENTER)
        row_default_runner.add_suffix(combo_runner)
        row_default_runner.set_activatable_widget(combo_runner)
        proton_group.add(row_default_runner)
        
        # Proton Manager Button
        row_proton_manager = Adw.ActionRow()
        row_proton_manager.set_title("Proton Manager")
        
        button_proton_manager = Gtk.Button(label="Manage Proton Versions")
        button_proton_manager.set_valign(Gtk.Align.CENTER)
        button_proton_manager.get_style_context().add_class("suggested-action")
        row_proton_manager.add_suffix(button_proton_manager)
        row_proton_manager.set_activatable_widget(button_proton_manager)
        proton_group.add(row_proton_manager)
        
        page.add(proton_group)
        
        # Tools Group
        tools_group = Adw.PreferencesGroup()
        tools_group.set_title("Default Prefix Tools")
        
        # Winetricks Button
        row_winetricks = Adw.ActionRow()
        row_winetricks.set_title("Winetricks")
        
        button_winetricks = Gtk.Button(label="Launch Winetricks")
        button_winetricks.set_valign(Gtk.Align.CENTER)
        row_winetricks.add_suffix(button_winetricks)
        row_winetricks.set_activatable_widget(button_winetricks)
        tools_group.add(row_winetricks)
        
        # Winecfg Button
        row_winecfg = Adw.ActionRow()
        row_winecfg.set_title("Wine Configuration")
        
        button_winecfg = Gtk.Button(label="Launch Winecfg")
        button_winecfg.set_valign(Gtk.Align.CENTER)
        row_winecfg.add_suffix(button_winecfg)
        row_winecfg.set_activatable_widget(button_winecfg)
        tools_group.add(row_winecfg)
        
        # Run Button
        row_run = Adw.ActionRow()
        row_run.set_title("Run File")
        row_run.set_subtitle("Run a file inside the prefix")
        
        button_run = Gtk.Button(label="Browse and Run")
        button_run.set_valign(Gtk.Align.CENTER)
        row_run.add_suffix(button_run)
        row_run.set_activatable_widget(button_run)
        tools_group.add(row_run)
        
        page.add(tools_group)
        
        # Launch Options Group
        launch_group = Adw.PreferencesGroup()
        launch_group.set_title("Launch Options")
        launch_group.set_description("Configure game launch behavior")
        
        # Close on Launch
        row_close_launch = Adw.ActionRow()
        row_close_launch.set_title("Close when running a game/app")
        switch_close_launch = Gtk.Switch()
        switch_close_launch.set_valign(Gtk.Align.CENTER)
        row_close_launch.add_suffix(switch_close_launch)
        row_close_launch.set_activatable_widget(switch_close_launch)
        launch_group.add(row_close_launch)
        
        # MangoHud
        row_mangohud = Adw.ActionRow()
        row_mangohud.set_title("MangoHud")
        row_mangohud.set_subtitle("Shows an overlay for monitoring FPS, temperatures, CPU/GPU load and more.")
        switch_mangohud = Gtk.Switch()
        switch_mangohud.set_valign(Gtk.Align.CENTER)
        row_mangohud.add_suffix(switch_mangohud)
        row_mangohud.set_activatable_widget(switch_mangohud)
        launch_group.add(row_mangohud)
        
        # GameMode
        row_gamemode = Adw.ActionRow()
        row_gamemode.set_title("GameMode")
        row_gamemode.set_subtitle("Tweaks your system to improve performance.")
        switch_gamemode = Gtk.Switch()
        switch_gamemode.set_valign(Gtk.Align.CENTER)
        row_gamemode.add_suffix(switch_gamemode)
        row_gamemode.set_activatable_widget(switch_gamemode)
        launch_group.add(row_gamemode)
        
        # Disable Hidraw
        row_disable_hidraw = Adw.ActionRow()
        row_disable_hidraw.set_title("Disable Hidraw")
        switch_disable_hidraw = Gtk.Switch()
        switch_disable_hidraw.set_valign(Gtk.Align.CENTER)
        row_disable_hidraw.add_suffix(switch_disable_hidraw)
        row_disable_hidraw.set_activatable_widget(switch_disable_hidraw)
        launch_group.add(row_disable_hidraw)
        
        # Prevent Sleep
        row_prevent_sleep = Adw.ActionRow()
        row_prevent_sleep.set_title("Prevent Sleep")
        switch_prevent_sleep = Gtk.Switch()
        switch_prevent_sleep.set_valign(Gtk.Align.CENTER)
        row_prevent_sleep.add_suffix(switch_prevent_sleep)
        row_prevent_sleep.set_activatable_widget(switch_prevent_sleep)
        launch_group.add(row_prevent_sleep)
        
        # Discrete GPU
        row_discrete_gpu = Adw.ActionRow()
        row_discrete_gpu.set_title("Use discrete GPU")
        switch_discrete_gpu = Gtk.Switch()
        switch_discrete_gpu.set_valign(Gtk.Align.CENTER)
        row_discrete_gpu.add_suffix(switch_discrete_gpu)
        row_discrete_gpu.set_activatable_widget(switch_discrete_gpu)
        launch_group.add(row_discrete_gpu)
        
        # Disable Splash
        row_splash_disable = Adw.ActionRow()
        row_splash_disable.set_title("Disable splash window")
        switch_splash_disable = Gtk.Switch()
        switch_splash_disable.set_valign(Gtk.Align.CENTER)
        row_splash_disable.add_suffix(switch_splash_disable)
        row_splash_disable.set_activatable_widget(switch_splash_disable)
        launch_group.add(row_splash_disable)
        
        page.add(launch_group)
        
        # System Group
        system_group = Adw.PreferencesGroup()
        system_group.set_title("System")
        system_group.set_description("System integration and advanced settings")
        
        # System Tray
        row_system_tray = Adw.ActionRow()
        row_system_tray.set_title("System tray icon")
        switch_system_tray = Gtk.Switch()
        switch_system_tray.set_valign(Gtk.Align.CENTER)
        row_system_tray.add_suffix(switch_system_tray)
        row_system_tray.set_activatable_widget(switch_system_tray)
        system_group.add(row_system_tray)
        
        # Start Minimized
        row_start_minimized = Adw.ActionRow()
        row_start_minimized.set_title("Start minimized to tray")
        switch_start_minimized = Gtk.Switch()
        switch_start_minimized.set_valign(Gtk.Align.CENTER)
        switch_start_minimized.set_sensitive(False)
        row_start_minimized.add_suffix(switch_start_minimized)
        row_start_minimized.set_activatable_widget(switch_start_minimized)
        system_group.add(row_start_minimized)
        
        # Monochrome Icon
        row_mono_icon = Adw.ActionRow()
        row_mono_icon.set_title("Monochrome icon")
        switch_mono_icon = Gtk.Switch()
        switch_mono_icon.set_valign(Gtk.Align.CENTER)
        switch_mono_icon.set_sensitive(False)
        row_mono_icon.add_suffix(switch_mono_icon)
        row_mono_icon.set_activatable_widget(switch_mono_icon)
        system_group.add(row_mono_icon)
        
        # Start on Boot
        row_start_boot = Adw.ActionRow()
        row_start_boot.set_title("Start on boot")
        switch_start_boot = Gtk.Switch()
        switch_start_boot.set_valign(Gtk.Align.CENTER)
        row_start_boot.add_suffix(switch_start_boot)
        row_start_boot.set_activatable_widget(switch_start_boot)
        system_group.add(row_start_boot)
        
        # Disable Updates
        row_disable_updates = Adw.ActionRow()
        row_disable_updates.set_title("Disable automatic updates")
        switch_disable_updates = Gtk.Switch()
        switch_disable_updates.set_valign(Gtk.Align.CENTER)
        row_disable_updates.add_suffix(switch_disable_updates)
        row_disable_updates.set_activatable_widget(switch_disable_updates)
        system_group.add(row_disable_updates)
        
        # Enable Logging
        row_enable_logging = Adw.ActionRow()
        row_enable_logging.set_title("Enable logging")
        switch_enable_logging = Gtk.Switch()
        switch_enable_logging.set_valign(Gtk.Align.CENTER)
        row_enable_logging.add_suffix(switch_enable_logging)
        row_enable_logging.set_activatable_widget(switch_enable_logging)
        system_group.add(row_enable_logging)
        
        # Wayland Driver
        row_wayland = Adw.ActionRow()
        row_wayland.set_title("Use Wayland driver (experimental)")
        switch_wayland = Gtk.Switch()
        switch_wayland.set_valign(Gtk.Align.CENTER)
        row_wayland.add_suffix(switch_wayland)
        row_wayland.set_activatable_widget(switch_wayland)
        system_group.add(row_wayland)
        
        # Enable HDR
        row_hdr = Adw.ActionRow()
        row_hdr.set_title("Enable HDR (experimental)")
        switch_hdr = Gtk.Switch()
        switch_hdr.set_valign(Gtk.Align.CENTER)
        switch_hdr.set_sensitive(False)
        row_hdr.add_suffix(switch_hdr)
        row_hdr.set_activatable_widget(switch_hdr)
        system_group.add(row_hdr)
        
        # Enable WOW64
        row_wow64 = Adw.ActionRow()
        row_wow64.set_title("Enable WOW64 (experimental)")
        switch_wow64 = Gtk.Switch()
        switch_wow64.set_valign(Gtk.Align.CENTER)
        row_wow64.add_suffix(switch_wow64)
        row_wow64.set_activatable_widget(switch_wow64)
        system_group.add(row_wow64)
        
        page.add(system_group)
        
        # Language Group
        language_group = Adw.PreferencesGroup()
        language_group.set_title("Language")
        language_group.set_description("Select your preferred language")
        
        row_language = Adw.ActionRow()
        row_language.set_title("Language")
        
        combo_language = Gtk.ComboBoxText()
        combo_language.set_valign(Gtk.Align.CENTER)
        row_language.add_suffix(combo_language)
        row_language.set_activatable_widget(combo_language)
        language_group.add(row_language)
        
        page.add(language_group)
        
        # Environment Variables Group
        envar_group = Adw.PreferencesGroup()
        envar_group.set_title("Global Environment Variables")
        envar_group.set_description("One variable per line (e.g., VAR=value)")
        
        # Text view for environment variables
        scrolled_window = Gtk.ScrolledWindow()
        scrolled_window.set_policy(Gtk.PolicyType.NEVER, Gtk.PolicyType.AUTOMATIC)
        scrolled_window.set_min_content_height(150)
        
        text_view = Gtk.TextView()
        text_view.set_monospace(True)
        text_view.set_wrap_mode(Gtk.WrapMode.NONE)
        scrolled_window.set_child(text_view)
        
        row_envar = Adw.ActionRow()
        row_envar.set_title("Environment Variables")
        row_envar.set_child(scrolled_window)
        envar_group.add(row_envar)
        
        page.add(envar_group)
        
        # Support Group
        support_group = Adw.PreferencesGroup()
        support_group.set_title("Support the Project")
        
        # Ko-fi Button
        row_kofi = Adw.ActionRow()
        row_kofi.set_title("Support on Ko-fi")
        
        button_kofi = Gtk.Button(label="Support on Ko-fi")
        button_kofi.set_valign(Gtk.Align.CENTER)
        button_kofi.get_style_context().add_class("suggested-action")
        row_kofi.add_suffix(button_kofi)
        row_kofi.set_activatable_widget(button_kofi)
        support_group.add(row_kofi)
        
        # PayPal Button
        row_paypal = Adw.ActionRow()
        row_paypal.set_title("Donate via PayPal")
        
        button_paypal = Gtk.Button(label="Donate on PayPal")
        button_paypal.set_valign(Gtk.Align.CENTER)
        button_paypal.get_style_context().add_class("suggested-action")
        row_paypal.add_suffix(button_paypal)
        row_paypal.set_activatable_widget(button_paypal)
        support_group.add(row_paypal)
        
        page.add(support_group)
        
        # Backup/Restore Group
        backup_group = Adw.PreferencesGroup()
        backup_group.set_title("Backup/Restore Settings")
        
        # Backup Button
        row_backup = Adw.ActionRow()
        row_backup.set_title("Backup Configuration")
        
        button_backup = Gtk.Button(label="Backup Settings")
        button_backup.set_valign(Gtk.Align.CENTER)
        row_backup.add_suffix(button_backup)
        row_backup.set_activatable_widget(button_backup)
        backup_group.add(row_backup)
        
        # Restore Button
        row_restore = Adw.ActionRow()
        row_restore.set_title("Restore Configuration")
        
        button_restore = Gtk.Button(label="Restore Settings")
        button_restore.set_valign(Gtk.Align.CENTER)
        button_restore.get_style_context().add_class("destructive-action")
        row_restore.add_suffix(button_restore)
        row_restore.set_activatable_widget(button_restore)
        backup_group.add(row_restore)
        
        # Clear Logs Button
        row_clearlogs = Adw.ActionRow()
        row_clearlogs.set_title("Clear Logs")
        
        button_clearlogs = Gtk.Button(label="Clear Log Files")
        button_clearlogs.set_valign(Gtk.Align.CENTER)
        button_clearlogs.get_style_context().add_class("destructive-action")
        row_clearlogs.add_suffix(button_clearlogs)
        row_clearlogs.set_activatable_widget(button_clearlogs)
        backup_group.add(row_clearlogs)
        
        page.add(backup_group)
        
        # Add page to dialog
        self.add(page)
        
        # Store references for later use
        self.widgets = {
            'combo_interface': combo_interface,
            'switch_start_maximized': switch_start_maximized,
            'switch_start_fullscreen': switch_start_fullscreen,
            'switch_show_labels': switch_show_labels,
            'switch_smaller_banners': switch_smaller_banners,
            'switch_gamepad': switch_gamepad,
            'switch_show_hidden': switch_show_hidden,
            'entry_default_prefix': entry_default_prefix,
            'entry_lossless': entry_lossless,
            'combo_runner': combo_runner,
            'button_proton_manager': button_proton_manager,
            'button_winetricks': button_winetricks,
            'button_winecfg': button_winecfg,
            'button_run': button_run,
            'switch_close_launch': switch_close_launch,
            'switch_mangohud': switch_mangohud,
            'switch_gamemode': switch_gamemode,
            'switch_disable_hidraw': switch_disable_hidraw,
            'switch_prevent_sleep': switch_prevent_sleep,
            'switch_discrete_gpu': switch_discrete_gpu,
            'switch_splash_disable': switch_splash_disable,
            'switch_system_tray': switch_system_tray,
            'switch_start_minimized': switch_start_minimized,
            'switch_mono_icon': switch_mono_icon,
            'switch_start_boot': switch_start_boot,
            'switch_disable_updates': switch_disable_updates,
            'switch_enable_logging': switch_enable_logging,
            'switch_wayland': switch_wayland,
            'switch_hdr': switch_hdr,
            'switch_wow64': switch_wow64,
            'combo_language': combo_language,
            'text_view_envar': text_view,
            'button_kofi': button_kofi,
            'button_paypal': button_paypal,
            'button_backup': button_backup,
            'button_restore': button_restore,
            'button_clearlogs': button_clearlogs,
        }
        
        # Connect signals
        self.connect_signals()
        
    def connect_signals(self):
        """Connect all widget signals."""
        # System tray toggle affects start minimized and mono icon sensitivity
        self.widgets['switch_system_tray'].connect('notify::active', 
            self.on_system_tray_toggled)
        
        # Wayland driver toggle affects HDR sensitivity
        self.widgets['switch_wayland'].connect('notify::active',
            self.on_wayland_toggled)
            
    def on_system_tray_toggled(self, switch, param):
        """Handle system tray toggle."""
        active = switch.get_active()
        self.widgets['switch_start_minimized'].set_sensitive(active)
        self.widgets['switch_mono_icon'].set_sensitive(active)
        
    def on_wayland_toggled(self, switch, param):
        """Handle Wayland driver toggle."""
        active = switch.get_active()
        self.widgets['switch_hdr'].set_sensitive(active)
        
    def load_config(self):
        """Load configuration from config_manager into widgets."""
        cfg = self.config_manager.config
        
        # Interface
        self.widgets['combo_interface'].set_active_id(cfg.get('interface-mode', 'List'))
        self.widgets['switch_start_maximized'].set_active(cfg.get('start-maximized', 'False') == 'True')
        self.widgets['switch_start_fullscreen'].set_active(cfg.get('start-fullscreen', 'False') == 'True')
        self.widgets['switch_show_labels'].set_active(cfg.get('show-labels', 'False') == 'True')
        self.widgets['switch_smaller_banners'].set_active(cfg.get('smaller-banners', 'False') == 'True')
        self.widgets['switch_gamepad'].set_active(cfg.get('gamepad-navigation', 'False') == 'True')
        self.widgets['switch_show_hidden'].set_active(cfg.get('show-hidden', 'False') == 'True')
        
        # Paths
        self.widgets['entry_default_prefix'].set_text(cfg.get('default-prefix', '').strip('"'))
        self.widgets['entry_lossless'].set_text(cfg.get('lossless-location', '').strip('"'))
        
        # Proton
        self.widgets['combo_runner'].set_active_id(cfg.get('default-runner', ''))
        
        # Launch Options
        self.widgets['switch_close_launch'].set_active(cfg.get('close-onlaunch', 'False') == 'True')
        self.widgets['switch_mangohud'].set_active(cfg.get('mangohud', 'False') == 'True')
        self.widgets['switch_gamemode'].set_active(cfg.get('gamemode', 'False') == 'True')
        self.widgets['switch_disable_hidraw'].set_active(cfg.get('disable-hidraw', 'False') == 'True')
        self.widgets['switch_prevent_sleep'].set_active(cfg.get('prevent-sleep', 'False') == 'True')
        self.widgets['switch_discrete_gpu'].set_active(cfg.get('discrete-gpu', 'False') == 'True')
        self.widgets['switch_splash_disable'].set_active(cfg.get('splash-disable', 'False') == 'True')
        
        # System
        self.widgets['switch_system_tray'].set_active(cfg.get('system-tray', 'False') == 'True')
        self.widgets['switch_start_minimized'].set_active(cfg.get('start-minimized', 'False') == 'True')
        self.widgets['switch_mono_icon'].set_active(cfg.get('mono-icon', 'False') == 'True')
        self.widgets['switch_start_boot'].set_active(cfg.get('start-boot', 'False') == 'True')
        self.widgets['switch_disable_updates'].set_active(cfg.get('disable-updates', 'False') == 'True')
        self.widgets['switch_enable_logging'].set_active(cfg.get('enable-logging', 'False') == 'True')
        self.widgets['switch_wayland'].set_active(cfg.get('wayland-driver', 'False') == 'True')
        self.widgets['switch_hdr'].set_active(cfg.get('enable-hdr', 'False') == 'True')
        self.widgets['switch_wow64'].set_active(cfg.get('enable-wow64', 'False') == 'True')
        
        # Language
        self.widgets['combo_language'].set_active_id(cfg.get('language', ''))
        
        # Update sensitivity based on current state
        self.on_system_tray_toggled(self.widgets['switch_system_tray'], None)
        self.on_wayland_toggled(self.widgets['switch_wayland'], None)
        
    def save_config(self):
        """Save configuration from widgets to config_manager."""
        cfg = self.config_manager
        
        # Interface
        cfg.set_value('interface-mode', self.widgets['combo_interface'].get_active_id())
        cfg.set_value('start-maximized', str(self.widgets['switch_start_maximized'].get_active()))
        cfg.set_value('start-fullscreen', str(self.widgets['switch_start_fullscreen'].get_active()))
        cfg.set_value('show-labels', str(self.widgets['switch_show_labels'].get_active()))
        cfg.set_value('smaller-banners', str(self.widgets['switch_smaller_banners'].get_active()))
        cfg.set_value('gamepad-navigation', str(self.widgets['switch_gamepad'].get_active()))
        cfg.set_value('show-hidden', str(self.widgets['switch_show_hidden'].get_active()))
        
        # Paths
        cfg.set_value('default-prefix', self.widgets['entry_default_prefix'].get_text())
        cfg.set_value('lossless-location', self.widgets['entry_lossless'].get_text())
        
        # Proton
        cfg.set_value('default-runner', self.widgets['combo_runner'].get_active_id())
        
        # Launch Options
        cfg.set_value('close-onlaunch', str(self.widgets['switch_close_launch'].get_active()))
        cfg.set_value('mangohud', str(self.widgets['switch_mangohud'].get_active()))
        cfg.set_value('gamemode', str(self.widgets['switch_gamemode'].get_active()))
        cfg.set_value('disable-hidraw', str(self.widgets['switch_disable_hidraw'].get_active()))
        cfg.set_value('prevent-sleep', str(self.widgets['switch_prevent_sleep'].get_active()))
        cfg.set_value('discrete-gpu', str(self.widgets['switch_discrete_gpu'].get_active()))
        cfg.set_value('splash-disable', str(self.widgets['switch_splash_disable'].get_active()))
        
        # System
        cfg.set_value('system-tray', str(self.widgets['switch_system_tray'].get_active()))
        cfg.set_value('start-minimized', str(self.widgets['switch_start_minimized'].get_active()))
        cfg.set_value('mono-icon', str(self.widgets['switch_mono_icon'].get_active()))
        cfg.set_value('start-boot', str(self.widgets['switch_start_boot'].get_active()))
        cfg.set_value('disable-updates', str(self.widgets['switch_disable_updates'].get_active()))
        cfg.set_value('enable-logging', str(self.widgets['switch_enable_logging'].get_active()))
        cfg.set_value('wayland-driver', str(self.widgets['switch_wayland'].get_active()))
        cfg.set_value('enable-hdr', str(self.widgets['switch_hdr'].get_active()))
        cfg.set_value('enable-wow64', str(self.widgets['switch_wow64'].get_active()))
        
        # Language
        cfg.set_value('language', self.widgets['combo_language'].get_active_id() or '')
        
        # Save to file
        cfg.save_config()
