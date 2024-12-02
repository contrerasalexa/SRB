import fpdf
from PyQt6.QtWidgets import QDialog, QMessageBox
from PyQt6 import uic
from src.database.connection import DBConnection
import pymysql

import os


class RentaDialog(QDialog):
    def __init__(self):
        super().__init__()
        uic.loadUi("src/views/renta.ui", self)
        self.db_connection = DBConnection()  # Instancia de conexión a la base de datos

        # Cargar datos en los widgets
        self.cargar_datos()

        # Conectar botones
        self.btnGuardarRenta.clicked.connect(self.guardar_renta)
        self.btnBuscarCliente.clicked.connect(self.buscar_cliente)
        self.comboBotes.currentIndexChanged.connect(self.calcular_subtotal)
        self.lineHoras.textChanged.connect(self.calcular_subtotal)
        self.lineDias.textChanged.connect(self.calcular_subtotal)
        self.lineGarantia.textChanged.connect(self.calcular_total)

    def cargar_datos(self):
        """Carga los datos existentes en los combos."""
        try:
            conn = self.db_connection.connection()
            if conn is None:
                QMessageBox.critical(self, "Error", "No se pudo conectar a la base de datos.")
                return

            cursor = conn.cursor(pymysql.cursors.DictCursor)

            # Cargar botes disponibles
            cursor.execute("SELECT id_bote, nombre FROM botes WHERE id_estatus = 1")
            botes = cursor.fetchall()
            for bote in botes:
                self.comboBotes.addItem(bote["nombre"], bote["id_bote"])

            # Cargar clientes activos
            cursor.execute("SELECT id, nombre FROM clientes WHERE estatus = '1'")
            clientes = cursor.fetchall()
            for cliente in clientes:
                self.comboClientes.addItem(cliente["nombre"], cliente["id"])

            cursor.close()
            self.db_connection.close()
        except Exception as e:
            QMessageBox.critical(self, "Error", f"Error al cargar datos: {e}")

    def buscar_cliente(self):
        """Busca un cliente en la base de datos y lo muestra en el combo."""
        try:
            criterio = self.lineBuscarCliente.text().strip()
            if not criterio:
                QMessageBox.warning(self, "Advertencia", "Introduce un nombre o email para buscar.")
                return

            conn = self.db_connection.connection()
            if conn is None:
                QMessageBox.critical(self, "Error", "No se pudo conectar a la base de datos.")
                return

            cursor = conn.cursor(pymysql.cursors.DictCursor)

            # Buscar clientes por nombre o email
            query = "SELECT id, nombre FROM clientes WHERE (nombre LIKE %s OR email LIKE %s) AND estatus = '1'"
            cursor.execute(query, (f"%{criterio}%", f"%{criterio}%"))
            clientes = cursor.fetchall()

            # Limpiar y cargar resultados en comboClientes
            self.comboClientes.clear()
            if clientes:
                for cliente in clientes:
                    self.comboClientes.addItem(cliente["nombre"], cliente["id"])
            else:
                QMessageBox.information(self, "Sin resultados", "No se encontraron clientes.")

            cursor.close()
            self.db_connection.close()
        except Exception as e:
            QMessageBox.critical(self, "Error", f"Error al buscar clientes: {e}")

    def calcular_subtotal(self):
        """Calcula el subtotal en base al tiempo de renta y el bote seleccionado."""
        try:
            # Obtener datos
            id_bote = self.comboBotes.currentData()
            horas = self.lineHoras.text()
            dias = self.lineDias.text()

            # Validar campos
            if not id_bote or (not horas and not dias):
                self.lineCosto.setText("0.00")
                return

            # Conectar a la base de datos
            conn = self.db_connection.connection()
            if conn is None:
                QMessageBox.critical(self, "Error", "No se pudo conectar a la base de datos.")
                return

            cursor = conn.cursor(pymysql.cursors.DictCursor)

            # Obtener costos del bote
            cursor.execute("SELECT costo_dia, costo_hora FROM botes WHERE id_bote = %s", (id_bote,))
            bote = cursor.fetchone()
            if not bote:
                self.lineCosto.setText("0.00")
                return

            # Calcular subtotal
            subtotal = 0.0
            if dias:
                subtotal += float(dias) * float(bote["costo_dia"])
            if horas:
                subtotal += float(horas) * float(bote["costo_hora"])

            # Mostrar subtotal
            self.lineCosto.setText(f"{subtotal:.2f}")

            cursor.close()
            self.db_connection.close()
        except Exception as e:
            QMessageBox.critical(self, "Error", f"Error al calcular el subtotal: {e}")

    def calcular_total(self):
        """Calcula el total sumando la garantía al subtotal."""
        try:
            subtotal = float(self.lineCosto.text() or 0)
            garantia = float(self.lineGarantia.text() or 0)
            total = subtotal + garantia
            self.valueTotal.setText(f"${total:.2f}")
        except ValueError:
            self.valueTotal.setText("$0.00")

    def guardar_renta(self):
        """Guarda un nuevo registro en renta_bote."""
        try:
            conn = self.db_connection.connection()
            if conn is None:
                QMessageBox.critical(self, "Error", "No se pudo conectar a la base de datos.")
                return

            cursor = conn.cursor()

            # Obtener datos del formulario
            id_bote = self.comboBotes.currentData()
            id_cliente = self.comboClientes.currentData()
            costo = self.lineCosto.text()
            fecha_disponible_id = 1  # Cambiar si agregas selección de fecha

            # Validar datos
            if not id_bote or not id_cliente or not costo:
                QMessageBox.warning(self, "Advertencia", "Todos los campos son obligatorios.")
                return

            # Insertar en la base de datos
            query = """
                INSERT INTO renta_bote (id_bote_fk, id_cliente_fk, id_fecha_fk, costo)
                VALUES (%s, %s, %s, %s)
            """
            cursor.execute(query, (id_bote, id_cliente, fecha_disponible_id, costo))
            conn.commit()
            QMessageBox.information(self, "Éxito", "La renta se ha registrado correctamente.")

            cursor.close()
            self.db_connection.close()
            self.close()
        except Exception as e:
            QMessageBox.critical(self, "Error", f"Error al guardar la renta: {e}")
