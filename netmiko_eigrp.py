from netmiko import ConnectHandler

# CONFIGURACIÓN DE CONEXIÓN SSH (Datos reales de tu lab)
DEVICE = {
    "device_type": "cisco_ios",
    "host": "192.168.56.102",
    "username": "cisco",
    "password": "cisco123",
}

print("==========================================")
print("     CONEXIÓN NETMIKO - ROUTER CSR        ")
print("==========================================")
print(f"[INFO] Conectando a {DEVICE['host']} vía SSH...")

try:
    # 1. Establecer la conexión SSH con Netmiko
    net_connect = net_connect = ConnectHandler(**DEVICE)
    print("[✅] Conexión SSH establecida con éxito.")
    
    # 2. Comandos de configuración para EIGRP Nombrado
    config_commands = [
        "router eigrp DUOC",
        "address-family ipv4 unicast autonomous-system 10",
        "network 11.11.11.11 0.0.0.0",
        "network 22.22.22.22 0.0.0.0",
        "exit-address-family"
    ]
    
    print("[INFO] Configurando EIGRP Nombrado 'DUOC' (AS 10)...")
    output_config = net_connect.send_config_set(config_commands)
    print("[✅] Configuración enviada al router.")
    
    print("\n==========================================")
    print("      VERIFICACIÓN DE PROTOCOLOS          ")
    print("==========================================")
    
    # 3. Ejecutar comando para ver los protocolos activos
    output_protocols = net_connect.send_command("show ip protocols")
    print(output_protocols)
    
    print("\n==========================================")
    print("         TABLA DE ENRUTAMIENTO            ")
    print("==========================================")
    
    # 4. Ejecutar comando para ver la tabla de rutas
    output_routes = net_connect.send_command("show ip route")
    print(output_routes)
    
    # 5. Cerrar la sesión de forma limpia
    net_connect.disconnect()
    print("\n[INFO] Conexión SSH cerrada correctamente.")
    
except Exception as e:
    print(f"[❌] Error crítico en la automatización: {e}")

print("==========================================")
