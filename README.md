## CORREO ARGENTINO - Seguimientos

Este script en Python permite obtener el seguimiento de diferentes tipos de paquetes de manera agil, sin tener que completar captchas.

**Aviso**: Usar responsablemente. 

### Setup

Script probado en Python2.7

Los requerimientos se instalan por medio de:

```
$ pip install -r requirements.txt
```

### Cómo usarlo
<pre>
usage: correoAPI.py [-h] [-n NUMERO] [-t TIPO]

optional arguments:
  -h, --help            show this help message and exit
  -n NUMERO, --numero NUMERO
                        numero de seguimiento
  -t TIPO, --tipo TIPO
                        tipo de seguimiento: 1- Origen y destino nacional
                        PLUS, 2- Origen y destino nacional, 3- Origen nacional
                        y destino internacional, 4- Origen internacional y
                        destino nacional, 5- Dni, 6- Pasaporte, 7- Mercado
                        Libre, 8- E-commerce

</pre>