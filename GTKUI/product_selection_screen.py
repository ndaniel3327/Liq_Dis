import gi
gi.require_version("Gtk", "3.0")
from gi.repository import Gtk, GdkPixbuf

from db.db_manager import DBManager

class ProductSelectionScreen(Gtk.Window):
    def __init__(self):
        super().__init__(title="Product Selection")
        self.set_default_size(1280, 720)
        self.fullscreen()

        self.db = DBManager()
        products = self.db.get_all_products()
        num_products = len(products)

        scrolled = Gtk.ScrolledWindow()
        self.add(scrolled)

        grid = Gtk.Grid()
        grid.set_row_spacing(20)
        grid.set_column_spacing(20)
        grid.set_margin_top(20)
        grid.set_margin_bottom(20)
        grid.set_margin_start(20)
        grid.set_margin_end(20)
        scrolled.add(grid)

        if num_products == 1:
            product = products[0]
            box = self.create_product_box(product)
            grid.attach(box, 0, 0, 1, 1)
            grid.set_column_homogeneous(True)
            grid.set_row_homogeneous(True)

        elif num_products == 2:
            grid.set_column_homogeneous(True)
            grid.set_row_homogeneous(True)
            for idx, product in enumerate(products):
                box = self.create_product_box(product)
                grid.attach(box, idx, 0, 1, 1)

        elif num_products == 3:
            grid.set_column_homogeneous(True)
            grid.set_row_homogeneous(True)

            # First two products in top row
            for idx in range(2):
                product = products[idx]
                box = self.create_product_box(product)
                grid.attach(box, idx, 0, 1, 1)

            # Third product in second row, centered
            product = products[2]
            box = self.create_product_box(product)
            grid.attach(box, 0, 1, 2, 1)  # Span two columns to center

        elif num_products >= 4:
            grid.set_column_homogeneous(True)
            grid.set_row_homogeneous(True)

            # First two products in top row
            for idx in range(2):
                product = products[idx]
                box = self.create_product_box(product)
                grid.attach(box, idx, 0, 1, 1)

            # Next two products in second row
            for idx in range(2,4):
                product = products[idx]
                box = self.create_product_box(product)
                grid.attach(box, idx-2, 1, 1, 1)

        self.show_all()

    def create_product_box(self, product):
        vbox = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=10)
        vbox.set_hexpand(True)
        vbox.set_vexpand(True)

        # Image
        img = self.load_image(product["image"], width=400, height=400)
        vbox.pack_start(img, True, True, 0)

        # Price
        price_label = Gtk.Label(label=f"${product['price']:.2f}")
        vbox.pack_start(price_label, False, False, 0)

        # Buttons
        hbox = Gtk.Box(spacing=10)
        main_btn = Gtk.Button(label=product["name"])
        main_btn.connect("clicked", self.on_product_selected, product["name"])

        info_btn = Gtk.Button(label="i")
        info_btn.set_size_request(50, -1)
        info_btn.connect("clicked", self.on_info_requested, product["name"])

        hbox.pack_start(main_btn, True, True, 0)
        hbox.pack_start(info_btn, False, False, 0)

        vbox.pack_start(hbox, False, False, 0)
        return vbox

    def load_image(self, path, width=400, height=400):
        try:
            pixbuf = GdkPixbuf.Pixbuf.new_from_file_at_scale(path, width, height, preserve_aspect_ratio=True)
            img = Gtk.Image.new_from_pixbuf(pixbuf)
        except:
            img = Gtk.Image.new_from_icon_name("image-missing", Gtk.IconSize.DIALOG)
        return img

    def on_product_selected(self, button, name):
        print(f"Selected: {name}")
        # Implement screen switch logic here

    def on_info_requested(self, button, name):
        print(f"Info requested for: {name}")
