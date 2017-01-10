# -*- coding: utf-8 -*-

from openerp import models, fields, api
from datetime import date, datetime

# ***********************************************************************
#                         Submodulo CONSULTAS
# ***********************************************************************

class consultas(models.Model):
    _name = 'consultas.consultas'
    todayDate = datetime.today()

    name = fields.Char(string="Nombre", required=True)
    date = fields.Date(string="Fecha de Nacimiento", required=True)
    observaciones = fields.Text()

    citas_id = fields.Many2one('consultas.citas',
        ondelete='cascade', string="Hacer cita", required=True)

    _defaults = {
        'date': fields.Date.today(),
    }

    @api.onchange('name', 'date') #Decorador
    def _onchange_observaciones(self):
        #print "hello"
        self.observaciones = str(self.name) + ' fue creado el ' + str(self.date)


    @api.multi
    def crear_cita(self):
        cr = self.env.cr #
        uid = self.env.uid #id de usuario
        att_obj = self.pool.get('consultas.citas') #Tomar datos de otro módulo
        identifier = self.id
        att_id = att_obj.create(cr,uid,{
            'date': self.todayDate,
            'citas_id': identifier
        }, context=None)

        return att_id


# ***********************************************************************
#                         Submodulo CITAS
# ***********************************************************************

class citas(models.Model):
    _name = 'consultas.citas'
    date = fields.Date(string="Fecha de la cita", required=True)
    observaciones = fields.Text();
    citas_id = fields.Many2one('consultas.consultas',
        ondelete='cascade', string="Paciente", required=True)

    @api.multi
    def generar_reporte(self, data=None, context=None):
        self.ensure_one()
        identifier = self.id
        return self.env['report'].get_action(self, "consultas.reports_template")


# ***********************************************************************
#                         Submodulo REPORTES
# ***********************************************************************

class reportes(models.Model):
    _name = 'consultas.reportes'
    begin_date = fields.Date(string="Fecha inicio", required=True)
    end_date = fields.Date(string="Fecha fin", required=True)
    paciente_id_reportes = fields.Many2one('consultas.consultas',
        ondelete='cascade', string="Paciente")
    tags = fields.Text();

    @api.multi
    def generar_reporte_prueba(self, data=None, context=None):
        self.env.cr.execute("some_sql", param1, param2, param3)
