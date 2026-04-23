"""Script para inicializar la base de datos con productos de ejemplo.

Usa sqlite3 directamente para evitar problemas de compatibilidad con SQLAlchemy.

Uso:
    python scripts/init_db.py

Este script crea la tabla de productos e inserta 10 zapatos de ejemplo
si la base de datos está vacía.
"""
import sqlite3
import os
from typing import List, Tuple
from datetime import datetime


def get_db_path() -> str:
    """Obtiene la ruta de la base de datos SQLite.
    
    Retorna:
        str: Ruta absoluta de la base de datos.
    """
    return os.path.join(os.path.dirname(__file__), "..", "ecommerce.db")


def create_tables(conn: sqlite3.Connection) -> None:
    """Crea las tablas necesarias en la base de datos.
    
    Parámetros:
        conn: Conexión a la base de datos SQLite.
    """
    cursor = conn.cursor()
    
    # Crear tabla de productos
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS products (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name VARCHAR(200) NOT NULL,
            brand VARCHAR(100) NOT NULL,
            category VARCHAR(100) NOT NULL,
            size VARCHAR(10) NOT NULL,
            color VARCHAR(100) NOT NULL,
            price FLOAT NOT NULL,
            stock INTEGER NOT NULL,
            created_at DATETIME NOT NULL,
            UNIQUE(name, brand, size, color)
        )
    """)
    
    # Crear tabla de mensajes de chat
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS chat_messages (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            session_id VARCHAR(200) NOT NULL,
            role VARCHAR(20) NOT NULL,
            message TEXT NOT NULL,
            timestamp DATETIME NOT NULL
        )
    """)
    
    # Crear índices
    cursor.execute("""
        CREATE INDEX IF NOT EXISTS ix_products_brand ON products(brand)
    """)
    
    cursor.execute("""
        CREATE INDEX IF NOT EXISTS ix_products_category ON products(category)
    """)
    
    cursor.execute("""
        CREATE INDEX IF NOT EXISTS ix_chat_messages_session_id ON chat_messages(session_id)
    """)
    
    conn.commit()


def get_products_data() -> List[Tuple]:
    """Retorna la lista de 10 productos de ejemplo.
    
    Retorna:
        List[Tuple]: Lista de tuplas con datos de productos.
    """
    # Usar formato sin microsegundos para compatibilidad con SQLAlchemy 1.4 + SQLite
    now = datetime.utcnow().strftime('%Y-%m-%d %H:%M:%S')
    
    productos = [
        ("Air Zoom Pegasus", "Nike", "Running", "42", "Negro", 120.0, 5, now),
        ("Ultraboost 21", "Adidas", "Running", "41", "Blanco", 150.0, 3, now),
        ("Suede Classic", "Puma", "Casual", "40", "Azul", 80.0, 10, now),
        ("Air Max 90", "Nike", "Casual", "43", "Rojo", 130.0, 7, now),
        ("NMD R1", "Adidas", "Running", "42", "Negro", 110.0, 4, now),
        ("RS-X Efekt", "Puma", "Casual", "41", "Gris", 90.0, 8, now),
        ("Cortez", "Nike", "Casual", "44", "Blanco", 100.0, 6, now),
        ("Boost 350", "Adidas", "Running", "40", "Amarillo", 140.0, 2, now),
        ("Thunder Spectra", "Puma", "Running", "42", "Verde", 95.0, 9, now),
        ("Jordan 1", "Nike", "Casual", "43", "Negro/Rojo", 160.0, 3, now),
    ]
    
    return productos


def main() -> None:
    """Inicializa la base de datos con 10 productos de ejemplo."""
    try:
        db_path = get_db_path()
        
        print("📦 Conectando a base de datos...")
        conn = sqlite3.connect(db_path)
        
        print("📦 Creando tabla de productos...")
        create_tables(conn)
        print("✅ Tabla creada/verificada")
        
        cursor = conn.cursor()
        
        # Verificar si ya existen productos
        cursor.execute("SELECT COUNT(*) FROM products")
        count = cursor.fetchone()[0]
        
        if count > 0:
            print(f"⚠️  La base de datos ya contiene {count} productos. Saliendo...")
            conn.close()
            return
        
        # Insertar productos
        print("🛒 Preparando 10 productos de ejemplo...")
        productos = get_products_data()
        
        print("⏳ Insertando productos en la base de datos...")
        cursor.executemany(
            """
            INSERT INTO products 
            (name, brand, category, size, color, price, stock, created_at)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?)
            """,
            productos,
        )
        conn.commit()
        
        # Verificar inserción
        cursor.execute("SELECT COUNT(*) FROM products")
        total = cursor.fetchone()[0]
        print(f"✅ Base de datos poblada exitosamente con {total} productos!")
        
        # Mostrar resumen
        print("\n📋 Resumen de productos insertados:")
        cursor.execute("SELECT id, name, brand, category, price, stock FROM products ORDER BY id")
        for row in cursor.fetchall():
            producto_id, name, brand, category, price, stock = row
            print(
                f"  {producto_id:2}. {name:20} | {brand:7} | {category:8} | "
                f"${price:6.2f} | Stock: {stock}"
            )
        
        conn.close()
        print(f"\n💾 Base de datos guardada en: {db_path}")
        
    except Exception as e:
        print(f"❌ Error al poblar la base de datos: {str(e)}")
        raise


if __name__ == "__main__":
    main()
