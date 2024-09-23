import matplotlib.pyplot as plt
import numpy as np

# Crear una figura y un conjunto de ejes
fig, ax = plt.subplots(figsize=(6, 1))

# Crear una matriz de ejemplo que contenga valores de 0 a 1
gradient = np.linspace(0, 1, 256).reshape(1, 256)

# Mostrar la imagen del gradiente con el colormap 'coolwarm'
ax.imshow(gradient, aspect='auto', cmap='coolwarm')

# Eliminar los ejes
ax.set_axis_off()

# Guardar la figura como SVG
plt.savefig("coolwarm_gradient.svg", format="svg", bbox_inches='tight', pad_inches=0, transparent=True)

# Mostrar la figura en pantalla
plt.show()