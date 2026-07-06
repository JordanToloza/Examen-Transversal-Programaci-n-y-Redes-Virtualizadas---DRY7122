# Script para listar los integrantes del grupo
# Examen Transversal - DRY7122

integrantes = [
    "Melissa Crisosto",
    "Jordan Toloza"
]

print("==========================================")
print("   INTEGRANTES DEL GRUPO - EXAMEN ET   ")
print("==========================================")

for i, integrante in enumerate(integrantes, start=1):
    print(f"{i}. {integrante}")
    
print("==========================================")
