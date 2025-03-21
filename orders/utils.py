from io import BytesIO
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas

def generate_pdf(cart_items, total_paid, payment_method, user):
    buffer = BytesIO()

    pdf = canvas.Canvas(buffer, pagesize=letter)

    pdf.setFont("Helvetica-Bold", 16)
    pdf.drawString(50, 750, "Factura de Compra")
    pdf.setFont("Helvetica", 12)
    pdf.drawString(50, 730, f"Usuario: {user.username}")
    pdf.drawString(50, 710, f"Método de pago: {payment_method}")
    pdf.drawString(50, 690, f"Total pagado: ${total_paid}")

    pdf.drawString(50, 660, "Productos:")
    y = 640
    for item in cart_items:
        pdf.drawString(50, y, f"- {item.product.name} (Cantidad: {item.quantity}, Precio: ${item.product.price})")
        y -= 20

    pdf.showPage()
    pdf.save()

    buffer.seek(0)
    return buffer