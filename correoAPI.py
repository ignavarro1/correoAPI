#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
#Coded by: Ignacio Navarro
#Version: 1.0

import requests
import pandas as pd
import argparse
import re

urlBase = 'https://api.correoargentino.com.ar/backendappcorreo/api/api/shipping-tracking-'
tipos = ['1- Origen y destino nacional PLUS', '2- Origen y destino nacional', '3- Origen nacional y destino internacional',
         '4- Origen internacional y destino nacional', '5- Dni', '6- Pasaporte', '7- Mercado Libre', '8- E-commerce']
regex = re.compile(
        r'^(?:http|ftp)s?://' # http:// or https://
        r'(?:(?:[A-Z0-9](?:[A-Z0-9-]{0,61}[A-Z0-9])?\.)+(?:[A-Z]{2,6}\.?|[A-Z0-9-]{2,}\.?)|' #domain...
        r'localhost|' #localhost...
        r'\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3})' # ...or ip
        r'(?::\d+)?' # optional port
        r'(?:/?|[/?]\S+)$', re.IGNORECASE)

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('-n', '--numero', help='numero de seguimiento')
    parser.add_argument('-t', '--tipo', help='tipo de seguimiento: {}'.format(', '.join(tipos)))
    args = parser.parse_args()

    tipo = args.tipo
    numero = args.numero

    if not numero or not tipo:
        tipo, numero = getDatos()

    urlFin = getUrl(tipo, numero)

    if re.match(regex, urlFin) is not None:
        response = requests.get(urlFin).json()
        if response['code'] == 0:
            data = response['data']
            if 'msg' not in data:
                print ('Cantidad de movimientos: {}\n'.format(len(data['eventos'])))
                print pd.DataFrame(data['eventos'], columns=['fecha', 'planta', 'evento'])
                print ('\n')
                print ('Id pedido: {}'.format(data['id_pedido']))
                print ('Id cliente: {}'.format(data['id_cliente']))
            else:
                print (u'\nERROR: {}'.format(data['msg']))
        else:
            print ('\n')
            res = response['data']['msg']
            for errors in res:
                for i in range(len(res[errors])):
                    print (u'ERROR: {}'.format(res[errors][i]))
    else:
        print ('\nERROR: Verificar los parametros')


def getDatos():
    print ('Tipos de seguimientos: ')
    for i in range(len(tipos)):
        print (tipos[i])
    tipo = raw_input('Seleccione su tipo de seguimiento: ')
    numero = raw_input('Ingrese su numero de seguimiento: ')

    return tipo, numero


def getUrl(tipo, numero):
    urlFin = ''
    if tipo in ['1', '2', '3']:
        prefijo = raw_input('Ingrese su identificador de envio(2 letras): ')
        destination = 'NacP'
        if tipo == '2':
            destination = 'Nac'
        elif tipo == '3':
            destination = 'Int'
        urlFin = urlBase + 'nac?product_code={}&id_shipping={}&destination={}'.format(prefijo, numero, destination)
    elif tipo in ['5', '6']:
        document = 'Dni'
        if tipo == '6':
            document = 'Pasaport'
        urlFin = urlBase + 'document?id_shipping={}&document={}'.format(numero, document)
    elif tipo in ['4', '7', '8']:
        urlFin = urlBase + 'int-nac?number_shipping={}'.format(numero)
        if tipo == '7':
            urlFin = urlBase + 'ml?number_shipping={}'.format(numero)
        elif tipo == '8':
            urlFin = urlBase + 'ec?number_shipping={}'.format(numero)

    return urlFin


if __name__ == '__main__': main()