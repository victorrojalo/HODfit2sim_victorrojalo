import pandas as pd

#ANTES, EN MI LÍNEA DE COMANDO
## 1. Copia la cabecera a un archivo nuevo
#head -17 /data8/adrian/MN5/SEP_UNI/N2048_L250_fid/ROCKSTAR/outputs/out_128.list > test_halos.list

# 2. Filtra los halos con Np > 20 y guarda solo 5000
#awk 'NR > 17 && $8 > 20 {print $0; count++} count == 5000 {exit}' /data8/adrian/MN5/SEP_UNI/N2048_L250_fid/ROCKSTAR/outputs/out_128.list >> test_halos.list




# 1. Ruta al archivo PEQUEÑO que has creado con awk
# (Asegúrate de que el archivo 'test_halos.list' esté en la misma carpeta que este script)
f_h = 'test_halos.list'

# 2. Cargar el archivo
# Seguimos usando skiprows=range(1,17) porque el comando awk que te di
# también copió las 17 líneas de cabecera para que el formato sea idéntico.
df_h = pd.read_csv(f_h, sep='\s+', skiprows=range(1,17), header=0)

# 3. Comprobación rápida (Opcional pero recomendado)
print(f"Cargados {len(df_h)} halos de prueba.")
print(df_h.head())
