from django.db import models

class Producto(models.Model):
    # Restricción estricta de negocio: ID de máximo 15 caracteres alfanuméricos
    idProducto = models.CharField(max_length=15, primary_key=True)
    nombreProducto = models.CharField(max_length=100)
    precioBase = models.FloatField()
    disponibleStock = models.BooleanField(default=True)

    def __str__(self):
        return f"{self.idProducto} - {self.nombreProducto}"

class Cliente(models.Model):
    # Identificador del cliente limitado a 15 caracteres
    idCliente = models.CharField(max_length=15, primary_key=True)
    tokenDispositivo = models.CharField(max_length=255, blank=True, null=True)
    preferenciaId = models.CharField(max_length=15, blank=True, null=True)

    def __str__(self):
        return f"Cliente: {self.idCliente}"

class PedidoExpress(models.Model):
    # Identificador de orden limitado a 15 caracteres (ej: TKT-0000000001)
    idPedido = models.CharField(max_length=15, primary_key=True)
    idCliente = models.ForeignKey(Cliente, on_delete=models.CASCADE)
    estado = models.CharField(max_length=50, default='Preparando')
    timestampOrden = models.DateTimeField(auto_now_add=True)
    totalPago = models.FloatField()
    nombreLlamado = models.CharField(max_length=100, default='Cliente Express')

    def __str__(self):
        return f"Pedido {self.idPedido} - {self.nombreLlamado}"

class DetallePedido(models.Model):
    # Identificador autoincremental para registros internos de la tabla pivote
    idDetalle = models.AutoField(primary_key=True)
    idPedido = models.ForeignKey(PedidoExpress, on_delete=models.CASCADE, related_name='detalles')
    idProducto = models.ForeignKey(Producto, on_delete=models.CASCADE)
    cantidad = models.IntegerField()
    subtotal = models.FloatField()

    def __str__(self):
        return f"Detalle {self.idDetalle} - Pedido {self.idPedido.idPedido}"