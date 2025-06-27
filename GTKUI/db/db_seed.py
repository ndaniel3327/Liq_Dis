from db_manager import DBManager

if __name__ == "__main__":
    db = DBManager()
    db.add_product("Soda", 1.50, "img1.png")
    db.add_product("Chips", 2.00, "img2.png")
    db.add_product("Candy", 1.25, "img3.png")
    db.add_product("Water", 1.00, "img4.png")
    db.conn.close()  # ✅ Ensures data is flushed to disk
