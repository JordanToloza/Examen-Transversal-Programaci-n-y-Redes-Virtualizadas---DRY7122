# Script para validar rangos de VLANs (Normal vs Extendido)
# Examen Transversal - DRY7122

def validar_vlan():
    print("==========================================")
    print("       VALIDADOR DE RANGOS DE VLAN        ")
    print("==========================================")
    
    try:
        # Solicitamos el número de VLAN al usuario
        vlan = int(input("Por favor, ingrese el número de VLAN a consultar: "))
        
        # Evaluamos el número según los estándares de Cisco
        if 1 <= vlan <= 1005:
            print(f"\n[INFO] La VLAN {vlan} pertenece al RANGO NORMAL.")
        elif 1006 <= vlan <= 4094:
            print(f"\n[INFO] La VLAN {vlan} pertenece al RANGO EXTENDIDO.")
        else:
            print(f"\n[ERROR] El número {vlan} está fuera del rango permitido global (1 - 4094).")
            
    except ValueError:
        print("\n[ERROR] Entrada inválida. Por favor, ingrese solo números enteros.")
        
    print("==========================================")

if __name__ == "__main__":
    validar_vlan()
