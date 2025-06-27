#!/usr/bin/env python3
from gi.repository import Gtk
from product_selection_screen import ProductSelectionScreen

if __name__ == "__main__":
    app = ProductSelectionScreen()
    app.connect("destroy", Gtk.main_quit)
    Gtk.main()
