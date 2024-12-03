import fpdf
from PyQt6.QtWidgets import QDialog, QMessageBox
from PyQt6 import uic
from src.database.connection import DBConnection
import pymysql
import os
from src.views.cliente import ClienteDialog 


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
        self.btnRegistrarCliente.clicked.connect(self.abrir_formulario_cliente)
        self.comboBotes.currentIndexChanged.connect(self.calcular_subtotal)
        self.lineHoras.textChanged.connect(self.calcular_subtotal)
        self.lineDias.textChanged.connect(self.calcular_subtotal)
        self.lineGarantia.textChanged.connect(self.calcular_total)

    def abrir_formulario_cliente(self):
        """Abre el formulario para registrar un nuevo cliente."""
        cliente_dialog = ClienteDialog()
        cliente_dialog.exec()

        # Recargar los datos de los clientes después de registrar uno nuevo
        self.cargar_datos()
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
        """Guarda un nuevo registro en renta_bote y genera un PDF."""
        try:
            conn = self.db_connection.connection()
            if conn is None:
                QMessageBox.critical(self, "Error", "No se pudo conectar a la base de datos.")
                return

            cursor = conn.cursor()

            # Obtener datos del formulario
            id_bote = self.comboBotes.currentData()
            id_cliente = self.comboClientes.currentData()
            horas = self.lineHoras.text()
            dias = self.lineDias.text()
            costo = self.lineCosto.text()
            garantia = self.lineGarantia.text()

            # Validar datos
            if not id_bote or not id_cliente or not horas or not dias or not costo or not garantia:
                QMessageBox.warning(self, "Advertencia", "Todos los campos son obligatorios.")
                return

            # Validar que horas y días sean numéricos
            if not horas.isdigit() or not dias.isdigit():
                QMessageBox.warning(self, "Advertencia", "Las horas y los días deben ser valores numéricos.")
                return

            # Insertar en la base de datos
            query = """
                INSERT INTO renta_bote (id_bote_fk, id_cliente_fk, horas, dias, costo, garantia, estatus)
                VALUES (%s, %s, %s, %s, %s, %s, '1')
            """
            cursor.execute(query, (id_bote, id_cliente, horas, dias, costo, garantia))
            conn.commit()

            # Obtener el ID de la renta recién insertada
            renta_id = cursor.lastrowid

            # Generar el PDF
            self.generar_pdf(renta_id)

            # Mostrar mensaje de éxito y abrir el archivo automáticamente
            QMessageBox.information(self, "Éxito", "La renta se ha registrado correctamente. Abriendo el archivo PDF...")
            os.startfile(f"renta_{renta_id}.pdf")  # Abre el archivo PDF automáticamente

            cursor.close()
            self.db_connection.close()
            self.close()
        except Exception as e:
            QMessageBox.critical(self, "Error", f"Error al guardar la renta: {e}")

    def generar_pdf(self, renta_id):
        """Genera un archivo PDF con los detalles de la renta."""
        try:
            # Conectar a la base de datos
            conn = self.db_connection.connection()
            if conn is None:
                QMessageBox.critical(self, "Error", "No se pudo conectar a la base de datos.")
                return

            cursor = conn.cursor(pymysql.cursors.DictCursor)

            # Consulta SQL actualizada para incluir horas, días, costo, subtotal, total y garantía
            query = """
                SELECT 
                    r.id_renta,
                    CONCAT(c.nombre, ' ', c.apellido_paterno) AS cliente_nombre, 
                    c.email AS cliente_email, 
                    b.nombre AS bote_nombre, 
                    b.modelo AS bote_modelo, 
                    r.horas,
                    r.dias,
                    r.costo AS subtotal,
                    r.garantia,
                    (r.costo + r.garantia) AS total
                FROM renta_bote r
                INNER JOIN clientes c ON r.id_cliente_fk = c.id
                INNER JOIN botes b ON r.id_bote_fk = b.id_bote
                WHERE r.id_renta = %s
            """
            cursor.execute(query, (renta_id,))
            renta = cursor.fetchone()

            cursor.close()
            self.db_connection.close()

            if not renta:
                QMessageBox.critical(self, "Error", "No se encontraron los detalles de la renta.")
                return

            # Crear el documento PDF
            pdf = fpdf.FPDF()
            pdf.add_page()
            pdf.set_font("Arial", size=12)

            # Agregar logo
            logo_path = os.path.abspath("public/img/logo-SRB.png")
            pdf.image(logo_path, x=10, y=8, w=33)  # Ajusta la ruta y tamaño
            pdf.set_font("Arial", style="B", size=16)
            pdf.cell(200, 10, txt="Detalles de la Renta", ln=True, align="C")
            pdf.ln(20)  # Espacio adicional

            # Información de la renta
            pdf.set_font("Arial", style="B", size=12)
            pdf.cell(0, 10, txt="Información de la Renta:", ln=True)
            pdf.set_font("Arial", size=12)
            pdf.cell(0, 10, txt=f"Renta ID: {renta['id_renta']}", ln=True)
            pdf.cell(0, 10, txt=f"Horas rentadas: {renta['horas']}", ln=True)
            pdf.cell(0, 10, txt=f"Días rentados: {renta['dias']}", ln=True)
            pdf.ln(10)  # Espacio

            # Información del cliente
            pdf.set_font("Arial", style="B", size=12)
            pdf.cell(0, 10, txt="Información del Cliente:", ln=True)
            pdf.set_font("Arial", size=12)
            pdf.cell(0, 10, txt=f"Nombre: {renta['cliente_nombre']}", ln=True)
            pdf.cell(0, 10, txt=f"Email: {renta['cliente_email']}", ln=True)
            pdf.ln(10)  # Espacio

            # Información del bote
            pdf.set_font("Arial", style="B", size=12)
            pdf.cell(0, 10, txt="Información del Bote:", ln=True)
            pdf.set_font("Arial", size=12)
            pdf.cell(0, 10, txt=f"Nombre: {renta['bote_nombre']}", ln=True)
            pdf.cell(0, 10, txt=f"Modelo: {renta['bote_modelo']}", ln=True)
            pdf.ln(10)  # Espacio

            # Resumen de costos
            pdf.set_font("Arial", style="B", size=12)
            pdf.cell(0, 10, txt="Resumen de la Renta:", ln=True)
            pdf.set_font("Arial", size=12)
            pdf.cell(0, 10, txt=f"Subtotal: ${renta['subtotal']:.2f}", ln=True)
            pdf.cell(0, 10, txt=f"Garantía: ${renta['garantia']:.2f}", ln=True)
            pdf.cell(0, 10, txt=f"Total: ${renta['total']:.2f}", ln=True)

            # Guardar el archivo PDF
            pdf.output(f"renta_{renta_id}.pdf")

            # Confirmación y apertura del archivo
            QMessageBox.information(self, "Éxito", f"El archivo PDF para la renta {renta_id} fue generado exitosamente.")
            os.startfile(f"renta_{renta_id}.pdf")

        except Exception as e:
            QMessageBox.critical(self, "Error", f"Error al generar el PDF: {e}")
