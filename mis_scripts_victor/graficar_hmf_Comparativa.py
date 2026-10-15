import h5py
import matplotlib.pyplot as plt
import numpy as np
import matplotlib
matplotlib.use('Agg') # Evita errores en el servidor

# Lista de archivos basada en tu imagen (excluyendo el M200c.h5 base)
archivos = [
    'HMF_TOTAL_Rockstar_out87.h5',
    'HMF_TOTAL_Rockstar_out87_Mvir_Corte1_Centrales.h5', 'HMF_TOTAL_Rockstar_out87_Mvir_Corte1_Satelites.h5',
    'HMF_TOTAL_Rockstar_out87_Mvir_Corte2_Centrales.h5', 'HMF_TOTAL_Rockstar_out87_Mvir_Corte2_Satelites.h5',
    'HMF_TOTAL_Rockstar_out87_Mvir_Corte3_Centrales.h5', 'HMF_TOTAL_Rockstar_out87_Mvir_Corte3_Satelites.h5',
    'HMF_TOTAL_Rockstar_out87_Mvir_Corte4_Centrales.h5', 'HMF_TOTAL_Rockstar_out87_Mvir_Corte4_Satelites.h5',
    'HMF_TOTAL_Rockstar_out87_M200c_Corte1_Centrales.h5', 'HMF_TOTAL_Rockstar_out87_M200c_Corte1_Satelites.h5',
    'HMF_TOTAL_Rockstar_out87_M200c_Corte2_Centrales.h5', 'HMF_TOTAL_Rockstar_out87_M200c_Corte2_Satelites.h5',
    'HMF_TOTAL_Rockstar_out87_M200c_Corte3_Centrales.h5', 'HMF_TOTAL_Rockstar_out87_M200c_Corte3_Satelites.h5',
    'HMF_TOTAL_Rockstar_out87_M200c_Corte4_Centrales.h5', 'HMF_TOTAL_Rockstar_out87_M200c_Corte4_Satelites.h5'
]

plt.figure(figsize=(12, 8))

# Bucle para procesar cada archivo
for i, file_path in enumerate(archivos):
    try:
        with h5py.File(file_path, 'r') as f:
            edges = f['bin_edges'][:]
            phi = f['phi'][:]
        
        # Calcular centros de bines
        bin_centers = (edges[:-1] + edges[1:]) / 2.0
        mask = phi > 0
        
        # Crear una etiqueta (label) limpia extrayendo info del nombre del archivo
        label_name = file_path.replace('HMF_TOTAL_Rockstar_out87_', '').replace('.h5', '')
        if label_name == 'HMF_TOTAL_Rockstar_out87': label_name = 'Total Rockstar'
        
        # Diferenciar estilos: Mvir con línea continua, M200c con línea discontinua
        line_style = '-' if 'Mvir' in file_path or 'out87.h5' in file_path else '--'
        
        plt.plot(bin_centers[mask], phi[mask], ls=line_style, label=label_name, alpha=0.8)
        
    except FileNotFoundError:
        print(f"⚠️ Archivo no encontrado: {file_path}")
    except Exception as e:
        print(f"❌ Error procesando {file_path}: {e}")

# Configuración de la gráfica
plt.yscale('log')
plt.xlabel(r'$\log_{10}(M_{halo} / M_\odot h^{-1})$', fontsize=13)
plt.ylabel(r'$\phi = dn / d\log_{10}M$ [$h^3$ Mpc$^{-3}$]', fontsize=13)
plt.title('Comparativa HMF: Mvir vs M200c (Centrales y Satélites)', fontsize=15)
plt.grid(True, which="both", ls="--", alpha=0.5)

# Ajustar leyenda para que no tape la gráfica (fuera a la derecha)
plt.legend(fontsize=9, bbox_to_anchor=(1.05, 1), loc='upper left')

# Guardar
output_name = 'HMF_Comparativa_Completa.png'
plt.savefig(output_name, dpi=300, bbox_inches='tight')
print(f"✅ ¡Éxito! Gráfica comparativa guardada como: {output_name}")
