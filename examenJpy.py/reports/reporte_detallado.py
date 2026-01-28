import os
import json
from datetime import datetime
from core.storage import loadData

def reporte_detallado(fecha_inicio, fecha_fin, categoria=None):
    data = loadData()
    gastos = data["gastos"]
    
    try:
        inicio = datetime.strptime(fecha_inicio, "%Y-%m-%d")
        fin = datetime.strptime(fecha_fin, "%Y-%m-%d")
    except ValueError:
        print(" Error: Formato de fecha inválido. Use YYYY-MM-DD.")
        return None
    
    if inicio > fin:
        print(" Error: La fecha de inicio no puede ser mayor que la fecha de fin.")
        return None
    
    filtrados = []
    
    for g in gastos:
        try:
            fecha_g = datetime.strptime(g["fecha"], "%Y-%m-%d")
            
            if inicio <= fecha_g <= fin:
                if categoria is None or g["categoria"].lower() == categoria.lower():
                    filtrados.append(g)
        except ValueError:
            continue
    
    os.makedirs("reports", exist_ok=True)
    
    total_general = sum(g["cantidad"] for g in filtrados)
    
    total_categoria = {}
    for g in filtrados:
        cat = g["categoria"]
        total_categoria[cat] = total_categoria.get(cat, 0) + g["cantidad"]
    
    reporte = {
        "rango_de_fechas": {
            "inicio": fecha_inicio,
            "fin": fecha_fin
        },
        "categoria": categoria if categoria else "todas",
        "cantidad_gastos": len(filtrados),
        "total_general": total_general,
        "total_por_categoria": total_categoria,
        "gastos": filtrados
    }
    
    archivo_salida = "reports/reporte_detallado_gastos.json"
    
    try:
        with open(archivo_salida, "w", encoding="utf-8") as f:
            json.dump(reporte, f, indent=4, ensure_ascii=False)
        
        print(f"\n Reporte generado exitosamente: {archivo_salida}")
        print(f" Gastos encontrados: {len(filtrados)}")
        print(f" Total gastado: ${total_general:.2f}")
        
        if total_categoria:
            print("\n Totales por categoría:")
            for cat, monto in total_categoria.items():
                print(f"   - {cat.capitalize()}: ${monto:.2f}")
        
        return reporte
        
    except Exception as e:
        print(f" Error al guardar el reporte: {e}")
        return None