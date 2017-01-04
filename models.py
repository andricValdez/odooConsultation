# -*- coding: utf-8 -*-

from openerp import models, fields, api
from datetime import date, datetime

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
        #
        # report_obj = self.env['report']
        # report = report_obj._get_report_from_name('consultas.reports_template')
        # docargs = {
        #     'doc_ids': self._ids,
        #     'doc_model': report.model,
        #     'docs': self,
        # }
        # return report_obj.render('consultas.reports_template', docargs)


# ***********************************************************************

#
# class ParticularReport(models.AbstractModel):
#     _name = 'report.consultas.report_template'
#     @api.multi
#     def render_html(self, data=None):
#         report_obj = self.env['report']
#         report = report_obj._get_report_from_name('consultas.report_template')
#         docargs = {
#             'doc_ids': self._ids,
#             'doc_model': report.model,
#             'docs': self,
#         }
#         return report_obj.render('consultas.report_template', docargs)
