import xml.etree.ElementTree as ET

def generar_ui():
    """Genera el archivo clientes.ui basado en el diseño proporcionado."""
    ui = ET.Element("ui", attrib={"version": "4.0"})
    
    # MainWindow
    widget = ET.SubElement(ui, "widget", attrib={"class": "QMainWindow", "name": "MainWindow"})
    property_title = ET.SubElement(widget, "property", attrib={"name": "windowTitle"})
    ET.SubElement(property_title, "string").text = "Clientes"
    
    # Geometry
    property_geometry = ET.SubElement(widget, "property", attrib={"name": "geometry"})
    rect = ET.SubElement(property_geometry, "rect")
    ET.SubElement(rect, "x").text = "100"
    ET.SubElement(rect, "y").text = "100"
    ET.SubElement(rect, "width").text = "800"
    ET.SubElement(rect, "height").text = "600"
    
    # Central widget
    central_widget = ET.SubElement(widget, "widget", attrib={"class": "QWidget", "name": "centralwidget"})
    
    # TableWidget
    table = ET.SubElement(central_widget, "widget", attrib={"class": "QTableWidget", "name": "tableWidget"})
    table_geometry = ET.SubElement(table, "property", attrib={"name": "geometry"})
    table_rect = ET.SubElement(table_geometry, "rect")
    ET.SubElement(table_rect, "x").text = "10"
    ET.SubElement(table_rect, "y").text = "10"
    ET.SubElement(table_rect, "width").text = "780"
    ET.SubElement(table_rect, "height").text = "400"
    column_count = ET.SubElement(table, "property", attrib={"name": "columnCount"})
    ET.SubElement(column_count, "number").text = "6"
    ET.SubElement(table, "property", attrib={"name": "rowCount"})
    ET.SubElement(column_count, "number").text = "0"
    
    # Buttons
    buttons = [
        ("btnAgregar", "Agregar", 10, 420, 100, 30),
        ("btnEditar", "Editar", 120, 420, 100, 30),
        ("btnEliminar", "Eliminar", 230, 420, 100, 30),
        ("btnActualizar", "Actualizar", 340, 420, 100, 30),
    ]
    for name, text, x, y, width, height in buttons:
        button = ET.SubElement(central_widget, "widget", attrib={"class": "QPushButton", "name": name})
        button_geometry = ET.SubElement(button, "property", attrib={"name": "geometry"})
        button_rect = ET.SubElement(button_geometry, "rect")
        ET.SubElement(button_rect, "x").text = str(x)
        ET.SubElement(button_rect, "y").text = str(y)
        ET.SubElement(button_rect, "width").text = str(width)
        ET.SubElement(button_rect, "height").text = str(height)
        button_text = ET.SubElement(button, "property", attrib={"name": "text"})
        ET.SubElement(button_text, "string").text = text
    
    # Add to main layout
    layout = ET.SubElement(widget, "layout", attrib={"class": "QVBoxLayout", "name": "verticalLayout"})
    
    # Menubar and Statusbar
    menubar = ET.SubElement(widget, "widget", attrib={"class": "QMenuBar", "name": "menubar"})
    ET.SubElement(menubar, "property", attrib={"name": "geometry"})
    statusbar = ET.SubElement(widget, "widget", attrib={"class": "QStatusBar", "name": "statusbar"})
    
    tree = ET.ElementTree(ui)
    with open("clientes.ui", "wb") as f:
        tree.write(f, encoding="utf-8", xml_declaration=True)

if __name__ == "__main__":
    generar_ui()
    print("Archivo clientes.ui generado correctamente.")
