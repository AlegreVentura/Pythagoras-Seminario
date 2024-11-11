# triangulo_app/views.py
from django.shortcuts import render
from .forms import TrianguloForm
import math
import matplotlib
matplotlib.use('Agg')  # Usar backend no interactivo para evitar problemas con hilos
import matplotlib.pyplot as plt
import io
import urllib, base64

def calcular_faltante(request):
    resultado = None
    tipo_mensaje = "success"
    img_data = None
    
    if request.method == "POST":
        form = TrianguloForm(request.POST)
        if form.is_valid():
            cateto1 = form.cleaned_data['cateto1']
            cateto2 = form.cleaned_data['cateto2']
            hipotenusa = form.cleaned_data['hipotenusa']

            # Calcular el valor faltante o verificar la terna
            if hipotenusa is None:
                hipotenusa = math.sqrt(cateto1**2 + cateto2**2)
                mensaje = f"La hipotenusa calculada es: {hipotenusa:.2f}"
            elif cateto1 is None:
                cateto1 = math.sqrt(hipotenusa**2 - cateto2**2)
                mensaje = f"El cateto 1 calculado es: {cateto1:.2f}"
            elif cateto2 is None:
                cateto2 = math.sqrt(hipotenusa**2 - cateto1**2)
                mensaje = f"El cateto 2 calculado es: {cateto2:.2f}"
            else:
                if form.es_terna_pitagorica(cateto1, cateto2, hipotenusa):
                    mensaje = "Los valores ingresados forman una terna pitagórica."
                    tipo_mensaje = "success"
                else:
                    mensaje = "Los valores ingresados NO forman una terna pitagórica."
                    tipo_mensaje = "error"

            # Calcular el ángulo de la hipotenusa
            angulo = math.degrees(math.atan2(cateto2, cateto1))

            # Generar el gráfico del triángulo mejorado
            fig, ax = plt.subplots(figsize=(5, 5))
            ax.plot([0, cateto1, 0, 0], [0, 0, cateto2, 0], color='blue', linestyle='-', linewidth=4, marker='o', markersize=8, markerfacecolor='blue')
            ax.plot([cateto1, 0], [0, cateto2], color='red', linestyle='-', linewidth=4, marker='o', markersize=8, markerfacecolor='red')
            
            # Etiquetas para los lados con un diseño mejorado
            ax.text(cateto1 / 2, -0.6, f"Cateto 1: {cateto1:.2f}", ha="center", fontsize=12, color="blue", weight="bold")
            ax.text(-0.6, cateto2 / 2, f"Cateto 2: {cateto2:.2f}", va="center", rotation=90, fontsize=12, color="blue", weight="bold")
            ax.text(cateto1 / 2, cateto2 / 2, f"Hipotenusa: {hipotenusa:.2f}", color="red", ha="center", fontsize=12, weight="bold", rotation=-angulo)

            # Personalizar el gráfico
            ax.set_aspect('equal')
            ax.set_xlim(-1, max(cateto1, cateto2) + 1)
            ax.set_ylim(-1, max(cateto1, cateto2) + 1)
            ax.axis('off')
            ax.grid(True, which='both', linestyle='--', linewidth=0.5, color='lightgray')

            # Guardar la imagen en un buffer
            buf = io.BytesIO()
            plt.savefig(buf, format='png', bbox_inches='tight', pad_inches=0.5)
            buf.seek(0)
            img_data = base64.b64encode(buf.getvalue()).decode('utf-8')
            buf.close()

            plt.close(fig)

            return render(request, 'triangulo_app/calculo.html', {
                'form': form, 
                'resultado': mensaje, 
                'tipo_mensaje': tipo_mensaje,
                'img_data': img_data
            })
    else:
        form = TrianguloForm()

    return render(request, 'triangulo_app/calculo.html', {
        'form': form, 
        'resultado': None, 
        'tipo_mensaje': tipo_mensaje
    })



