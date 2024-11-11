from django import forms

class TrianguloForm(forms.Form):
    cateto1 = forms.FloatField(required=False, label='Cateto 1')
    cateto2 = forms.FloatField(required=False, label='Cateto 2')
    hipotenusa = forms.FloatField(required=False, label='Hipotenusa')

    def clean(self):
        cleaned_data = super().clean()
        cateto1 = cleaned_data.get("cateto1")
        cateto2 = cleaned_data.get("cateto2")
        hipotenusa = cleaned_data.get("hipotenusa")
        
        # Verificar que los valores sean positivos y mayores que cero
        if cateto1 is not None and cateto1 <= 0:
            raise forms.ValidationError("Cateto 1 debe ser un número positivo mayor que cero.")
        if cateto2 is not None and cateto2 <= 0:
            raise forms.ValidationError("Cateto 2 debe ser un número positivo mayor que cero.")
        if hipotenusa is not None and hipotenusa <= 0:
            raise forms.ValidationError("La hipotenusa debe ser un número positivo mayor que cero.")

        # Verificar cuántos valores se ingresaron
        valores = [v for v in [cateto1, cateto2, hipotenusa] if v is not None]
        if len(valores) == 2:
            # Si se ingresaron dos valores, el formulario está listo para calcular el faltante
            pass
        elif len(valores) == 3:
            # Si se ingresaron los tres valores, verificar si forman una terna pitagórica
            if not self.es_terna_pitagorica(cateto1, cateto2, hipotenusa):
                raise forms.ValidationError("Los valores ingresados no forman una terna pitagórica.")
        else:
            raise forms.ValidationError("Por favor, ingresa exactamente dos o tres valores.")

    def es_terna_pitagorica(self, cateto1, cateto2, hipotenusa):
        """Verifica si los valores dados forman una terna pitagórica."""
        # Asegurarse de que hipotenusa es el valor más grande
        if hipotenusa == max(cateto1, cateto2, hipotenusa):
            return round(cateto1**2 + cateto2**2, 5) == round(hipotenusa**2, 5)
        elif cateto1 == max(cateto1, cateto2, hipotenusa):
            # Si cateto1 es el mayor, entonces debe ser la "hipotenusa" en una terna
            return round(cateto2**2 + hipotenusa**2, 5) == round(cateto1**2, 5)
        else:
            # Si cateto2 es el mayor, entonces debe ser la "hipotenusa" en una terna
            return round(cateto1**2 + hipotenusa**2, 5) == round(cateto2**2, 5)



