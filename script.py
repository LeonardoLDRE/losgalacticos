import pandas as pd
import matplotlib.pyplot as plt 

# Cree un dataframe con datos no reales
data = {
    "Producto": ["Laptop", "Teclado", "Mouse", "Monitor", "Laptop", "Teclado"],
    "Cantidad": [15, 50, 50, 50, 15, 50],
    "Precio": [800, 50, 25, 300, 850, 55]
}

df = pd.DataFrame(data)

# calcula el total de ventas por productos
df["Total"] = df["Cantidad"] * df["Precio"]
ventas_por_producto = df.groupby("Producto")["Total"].sum()

# grafico de las ventas de los productos
plt.figure(figsize=(8, 5))
ventas_por_producto.plot(kind="bar", color="blue")
plt.title("Ventas por Producto")
plt.xlabel("Producto")
plt.ylabel("Total de Ventas ($)")
plt.xticks(rotation=45)
plt.grid(axis="y", linestyle="--", alpha=0.7)

# guardar el gráfico en un archivo PNG para mostrar los datos del dataframe
plt.savefig("grafico.png")  # guardar el grafica en la carpeta actual
plt.show()
