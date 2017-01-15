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

    # citas_id = fields.Many2one('consultas.citas',
    #     ondelete='cascade', string="Hacer cita", required=True)

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
    # reportes_id = fields.Many2one('consultas.reportes',
    #     ondelete='cascade', string="Reportes")

    # reportes_ids = fields.Many2many('consultas.reportes')

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
    paciente = fields.Many2one('consultas.consultas',
        ondelete='cascade', string="Paciente")
    tags = fields.Text();
    citas_ids = fields.Many2many('consultas.citas')

    @api.multi
    def generar_reporte_prueba(self, data=None, context=None):
        self.ensure_one()
        queryFilter = []

        #Filtros:
        #******************************* 1)

        if ((self.paciente.id == False) and (self.tags == False)):
            print("Filer 1:")
            # self.env.cr.execute("SELECT * FROM consultas_citas WHERE date="+str(self.begin_date))
            # queryFilter = self.env["consultas.citas"].search_read([],['citas_id'])
            queryFilter = self.env["consultas.citas"].search([('date', '>=', self.begin_date), ('date', '<=', self.end_date)])
            self.env.cr.fetchall()

        #******************************* 2)

        elif ((self.paciente.id == False) and (self.tags != False)):
            print("Filer 2:")
            queryFilter = self.env["consultas.citas"].search([('date', '>=', self.begin_date), ('date', '<=', self.end_date), ('observaciones', '=ilike', self.tags)])
            self.env.cr.fetchall()

        #******************************* 3)

        elif ((self.paciente.id != False) and (self.tags == False)):
            print("Filer 3:")
            queryFilter = self.env["consultas.citas"].search([('date', '>=', self.begin_date), ('date', '<=', self.end_date), ('citas_id', '=', self.paciente.id)])
            self.env.cr.fetchall()

        #******************************* 4)

        else:
            print("Filer 4:")
            queryFilter = self.env["consultas.citas"].search([('date', '>=', self.begin_date), ('date', '<=', self.end_date), ('observaciones', '=ilike', self.tags), ('citas_id', '=', self.paciente.id)])
            self.env.cr.fetchall()

        idsArray = []
        print queryFilter
        for record in queryFilter:
            idsArray.append(record.id)
            print record.citas_id.name

        self.citas_ids = [(6, 0, idsArray)]


        #**** Generar reporte
        return self.env['report'].get_action(self, "consultas.reports_template")
