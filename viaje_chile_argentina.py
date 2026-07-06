import requests


API_KEY = "b908c5b2-0797-4707-9768-553f1dabf6a5"
URL_GEO = "https://graphhopper.com/api/1/geocode"
URL_ROUTE = "https://graphhopper.com/api/1/route"

print("==========================================")
print("   SISTEMA DE PLANIFICACIÓN DE VIAJES     ")
print("==========================================")

while True:
    
    origen = input("Ciudad de Origen (Chile) [o 's' para salir]: ").strip()
    if origen.lower() == 's':
        break
        
    
    destino = input("Ciudad de Destino (Argentina) [o 's' para salir]: ").strip()
    if destino.lower() == 's':
        break
    
    
    print("\nSeleccione el medio de transporte:")
    print("1. Auto (car)")
    print("2. Bicicleta (bike)")
    print("3. Pie (foot)")
    opcion = input("Opción (1/2/3): ").strip()
    
    if opcion == "2":
        vehiculo = "bike"
    elif opcion == "3":
        vehiculo = "foot"
    else:
        vehiculo = "car"
    
    print("\n[INFO] Buscando coordenadas de las ciudades...")
    
   
    params_orig = {"q": origen, "locale": "es", "limit": 1, "key": API_KEY}
    res_orig = requests.get(URL_GEO, params=params_orig)
    
   
    params_dest = {"q": destino, "locale": "es", "limit": 1, "key": API_KEY}
    res_dest = requests.get(URL_GEO, params=params_dest)
    
   
    if res_orig.status_code == 200 and res_dest.status_code == 200:
        data_orig = res_orig.json()
        data_dest = res_dest.json()
        
        if data_orig["hits"] and data_dest["hits"]:
            
            point_orig = data_orig["hits"][0]["point"]
            point_dest = data_dest["hits"][0]["point"]
            
            lat_o, lng_o = point_orig["lat"], point_orig["lng"]
            lat_d, lng_d = point_dest["lat"], point_dest["lng"]
            
            
            params_ruta = {
                "point": [f"{lat_o},{lng_o}", f"{lat_d},{lng_d}"],
                "vehicle": vehiculo,
                "locale": "es",
                "instructions": "true",
                "key": API_KEY
            }
            
            res_ruta = requests.get(URL_ROUTE, params=params_ruta)
            
            if res_ruta.status_code == 200:
                data_ruta = res_ruta.json()
                path = data_ruta["paths"][0]
                
                
                distancia_km = path["distance"] / 1000
                distancia_mi = distancia_km * 0.621371
                
                
                duracion_min = path["time"] / 60000
                horas = int(duracion_min // 60)
                minutos = int(duracion_min % 60)
                
                
                print("\n==========================================")
                print("           RESUMEN DEL VIAJE              ")
                print("==========================================")
                print(f"Ruta: {origen} -> {destino} (Medio: {vehiculo})")
                print(f"Distancia: {distancia_km:.2f} km / {distancia_mi:.2f} millas")
                print(f"Duración: {horas} horas y {minutos} minutos")
                print("==========================================")
                
                
                print("\n📖 NARRATIVA DEL VIAJE:")
                for paso in path["instructions"]:
                    texto_paso = paso["text"]
                    dist_paso = paso["distance"] / 1000
                    if dist_paso > 0:
                        print(f"- {texto_paso} ({dist_paso:.2f} km)")
                    else:
                        print(f"- {texto_paso}")
                print("==========================================\n")
            else:
                print(f"\n[ERROR] No se pudo trazar la ruta terrestre entre las ciudades (Código {res_ruta.status_code}).")
        else:
            print("\n[ERROR] No se encontraron resultados geográficos para una o ambas ciudades.")
    else:
        print("\n[ERROR] Error de conexión con la API de Graphhopper. Verifica tu API_KEY.")

print("\n👋 Programa finalizado con éxito.")
