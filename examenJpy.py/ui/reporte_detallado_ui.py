from ui.prompts import inputSeguro
from utils.screenControllers import limpiarPantalla, pausarPantalla
from utils.validators import validarFecha
from core.storage import loadData
from reports.reporte_detallado import reporte_detallado

def generarReporteDetalladoUI():
    limpiarPantalla()
    print("""
=============================================
      Generar Reporte Detallado de Gastos
=============================================
""")
    
    data = loadData()
    
    while True:
        fecha_inicio = inputSeguro("Fecha inicio (YYYY-MM-DD): ")
        if not fecha_inicio:
            print(" Operación cancelada.")
            pausarPantalla()
            return
        if validarFecha(fecha_inicio):
            break
    
    while True:
        fecha_fin = inputSeguro("Fecha fin (YYYY-MM-DD): ")
        if not fecha_fin:
            print(" Operación cancelada.")
            pausarPantalla()
            return
        if validarFecha(fecha_fin):
            break
    
    print("\n¿Desea filtrar por categoría?")
    print("1. Sí")
    print("2. No (todas las categorías)")
    
    opcion = inputSeguro("\nSeleccione una opción: ")
    
    categoria = None
    
    if opcion == "1":
        if not data["categorias"]:
            print(" No hay categorías disponibles.")
            pausarPantalla()
            return
        
        print("\nCategorías disponibles:")
        for idx, cat in enumerate(data["categorias"], start=1):
            print(f"  {idx}. {cat.capitalize()}")
        
        cat_num = inputSeguro("\nSeleccione el número de categoría: ")
        try:
            cat_idx = int(cat_num) - 1
            if 0 <= cat_idx < len(data["categorias"]):
                categoria = data["categorias"][cat_idx]
            else:
                print(" Opción inválida. Se generará reporte de todas las categorías.")
        except ValueError:
            print(" Entrada inválida. Se generará reporte de todas las categorías.")
    
    print("\nGenerando reporte...")
    reporte_detallado(fecha_inicio, fecha_fin, categoria)
    
    pausarPantalla()