import os 
import json
from datetime import datatime
from core.storage import cargar_json, archivo_gastos
def reporte_detallado (fecha_inicio,fecha_fin,categoria=none):
    gastos = cargar_json (archivo_gastos)
    
    incio = datatime.striptime (fecha_inicio, "%y-%m-%d")

    fin = datatime.striptime (fecha_fin, "%y-%m-%d")

    filtrados = []

    for g in gastos:

        fecha_g = datatime.striptime (g["fecha"], "%Y-&m-%d")

        if inicio <= fecha_g <= fin:

            if categoria is None or g["categoria"]== categoria:

                filtrados.append(g)

                os.makedirs ("repors", exist_ok=True)

                total_general = sum (g["monto"] for g in filtrados)

                total_categoria = {}

                for g in filtrados:
                    total_categoria[g["categoria"]]= total_categoria.get (g["categoria"],0) + g["monto"]

                    reporte = { "rango_de_fechas": { "inicio": fecha_inicio,
                    "fin": fecha_fin},
                    "categoria": categoria if categoria else "todas_las_categorias",
                    "cantidad_gastos": len (filtrados), "total_general": total_general,
                    "total_categorias": total_categoria,
                    "gastos": filtrados} 

                    with open ("reports/reporte_detallado_gastos.json","w", econding="utf-8") as f:

                        json.dump (reporte,f, indent=4)
                        
                        print (f"el reporte generado- gastos encontrados:{len(filtrados)}")

                        print (f"total todo lo gastado: {total_general}")
                        