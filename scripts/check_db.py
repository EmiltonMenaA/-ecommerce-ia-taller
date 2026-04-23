"""Script para verificar los productos en la base de datos."""
import sqlite3

conn = sqlite3.connect("ecommerce.db")
cursor = conn.cursor()

# Contar productos
cursor.execute("SELECT COUNT(*) FROM products")
total = cursor.fetchone()[0]
print(f"✅ Total productos en BD: {total}")

# Mostrar primeros 5
print("\n📋 Primeros 5 productos:")
cursor.execute("SELECT id, name, brand, price, stock FROM products LIMIT 5")
for row in cursor.fetchall():
    producto_id, name, brand, price, stock = row
    print(f"  {producto_id}. {name:20} ({brand:7}) - ${price:6.2f} | Stock: {stock}")

# Mostrar por categoría
print("\n📊 Productos por categoría:")
cursor.execute("SELECT category, COUNT(*) FROM products GROUP BY category")
for category, count in cursor.fetchall():
    print(f"  {category:10} - {count} productos")

# Mostrar por marca
print("\n🏷️  Productos por marca:")
cursor.execute("SELECT brand, COUNT(*) FROM products GROUP BY brand")
for brand, count in cursor.fetchall():
    print(f"  {brand:10} - {count} productos")

conn.close()
