# -*- coding: utf-8 -*-

from openerp import models, fields, api

class consultas(models.Model):
    _name = 'consultas.consultas'

    name = fields.Char(string="Nombre", required=True)
    date = fields.Date(string="Fecha de Nacimiento", required=True)
    observaciones = fields.Text()

    citas_id = fields.Many2one('consultas.citas',
        ondelete='cascade', string="Hacer cita", required=True)


class citas(models.Model):
    _name = 'consultas.citas'
    date = fields.Date(string="Fecha de la cita", required=True)

    citas_id = fields.Many2one('consultas.consultas',
        ondelete='cascade', string="Paciente", required=True)
