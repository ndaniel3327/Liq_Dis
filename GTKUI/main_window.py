import gi
gi.require_version("Gtk", "3.0")
from gi.repository import Gtk, GLib

import threading

from gsm.gsm_controller import GSMController
from gpio.gpio_controller import GPIOController


class ControlPanelWindow(Gtk.Window):
    def __init__(self):
        super().__init__(title="Distance Measurement Control Panel")
        self.set_default_size(1280, 720)
        self.fullscreen()

        # --- Controllers ---
        self.gsm = GSMController()
        self.gpio = GPIOController()

        self.phone_number = ""
        self.gsm_status = "GSM Ready"
        self.last_distance = "Ultima distanță: –"

        # --- UI Layout ---
        vbox = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=20)
        vbox.set_margin_top(20)
        vbox.set_margin_bottom(20)
        vbox.set_margin_start(40)
        vbox.set_margin_end(40)
        self.add(vbox)

        # Status labels
        self.status_label = Gtk.Label(label="Așteptare...")
        vbox.pack_start(self.status_label, False, False, 0)

        self.current_distance_label = Gtk.Label(label="Apasă butonul pentru a măsura")
        self.current_distance_label.set_markup(f"<span size='xx-large'><b>{self.current_distance_label.get_text()}</b></span>")
        vbox.pack_start(self.current_distance_label, False, False, 0)

        self.last_distance_label = Gtk.Label(label=self.last_distance)
        vbox.pack_start(self.last_distance_label, False, False, 0)

        # Measurement button
        measure_button = Gtk.Button(label="Măsoară distanța")
        measure_button.connect("clicked", self.on_measure_clicked)
        vbox.pack_start(measure_button, False, False, 0)

        # MOSFET controls
        mosfet_box = Gtk.Box(spacing=20)
        mosfet_on_btn = Gtk.Button(label="MOSFET PORNIT")
        mosfet_on_btn.connect("clicked", self.on_mosfet_on_clicked)
        mosfet_box.pack_start(mosfet_on_btn, True, True, 0)

        mosfet_off_btn = Gtk.Button(label="MOSFET OPRIT")
        mosfet_off_btn.connect("clicked", self.on_mosfet_off_clicked)
        mosfet_box.pack_start(mosfet_off_btn, True, True, 0)

        vbox.pack_start(mosfet_box, False, False, 0)

        # GSM Controls
        gsm_label = Gtk.Label(label="GSM Control")
        gsm_label.set_markup("<span size='x-large'>GSM Control</span>")
        vbox.pack_start(gsm_label, False, False, 0)

        self.phone_entry = Gtk.Entry()
        self.phone_entry.set_placeholder_text("Introdu numărul de telefon")
        self.phone_entry.connect("changed", self.on_phone_changed)
        vbox.pack_start(self.phone_entry, False, False, 0)

        gsm_buttons_box = Gtk.Box(spacing=20)
        sms_btn = Gtk.Button(label="Trimite SMS")
        sms_btn.connect("clicked", self.on_sms_clicked)
        gsm_buttons_box.pack_start(sms_btn, True, True, 0)

        call_btn = Gtk.Button(label="Inițiază apel")
        call_btn.connect("clicked", self.on_call_clicked)
        gsm_buttons_box.pack_start(call_btn, True, True, 0)

        vbox.pack_start(gsm_buttons_box, False, False, 0)

        self.gsm_status_label = Gtk.Label(label=self.gsm_status)
        vbox.pack_start(self.gsm_status_label, False, False, 0)

        self.show_all()

    # --- Signal handlers ---

    def on_phone_changed(self, entry):
        self.phone_number = entry.get_text()

    def on_measure_clicked(self, button):
        self.status_label.set_text("Se măsoară...")
        self.current_distance_label.set_text("Măsurare în curs...")
        threading.Thread(target=self._do_measure_thread).start()

    def _do_measure_thread(self):
        try:
            distance = self.gpio.measure_distance()
            GLib.idle_add(self.current_distance_label.set_text, f"Distanța curentă: {distance} cm")
            GLib.idle_add(self.last_distance_label.set_text, f"Ultima distanță: {distance} cm")
            GLib.idle_add(self.status_label.set_text, "Măsurare finalizată")
        except Exception as e:
            GLib.idle_add(self.current_distance_label.set_text, "Eroare la măsurare")
            GLib.idle_add(self.status_label.set_text, f"Eroare: {e}")

    def on_mosfet_on_clicked(self, button):
        self.gpio.mosfet_on()
        self.status_label.set_text("MOSFET: PORNIT (3.3V pe GPIO25)")

    def on_mosfet_off_clicked(self, button):
        self.gpio.mosfet_off()
        self.status_label.set_text("MOSFET: OPRIT (0V pe GPIO25)")

    def on_sms_clicked(self, button):
        if not self.phone_number.strip():
            self.gsm_status_label.set_text("Introdu un număr valid!")
            return
        threading.Thread(target=self._send_sms_thread).start()

    def _send_sms_thread(self):
        try:
            self.gsm.send_sms(self.phone_number.strip(), "Salut! Aceasta este o masuratoare automatizata.")
            GLib.idle_add(self.gsm_status_label.set_text, f"SMS trimis către {self.phone_number}")
        except Exception as e:
            GLib.idle_add(self.gsm_status_label.set_text, f"Eroare la trimitere SMS: {e}")

    def on_call_clicked(self, button):
        if not self.phone_number.strip():
            self.gsm_status_label.set_text("Introdu un număr valid!")
            return
        threading.Thread(target=self._make_call_thread).start()

    def _make_call_thread(self):
        try:
            self.gsm.make_call(self.phone_number.strip())
            GLib.idle_add(self.gsm_status_label.set_text, f"Apel către {self.phone_number} inițiat...")
        except Exception as e:
            GLib.idle_add(self.gsm_status_label.set_text, f"Eroare apel: {e}")
