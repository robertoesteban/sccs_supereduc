# coding: utf-8
import django_tables2 as tables

from .models import Cometido


class CometidoTable(tables.Table):
    rut = tables.Column()
    nombre = tables.Column()
    actualizado = tables.Column(verbose_name='Ultima fecha de Modificacion')
    creado = tables.Column()
    summary = tables.Column(order_by=("-actualizado"))

    class Meta:
        model = Cometido
