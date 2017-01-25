# -*- coding: utf-8 -*-

from openerp import models, fields, api
from datetime import date, datetime
from openerp.exceptions import Warning
from openerp import _

# ***********************************************************************
#                         Submodulo CONSULTAS
# ***********************************************************************

class consultas(models.Model):
    _name = 'consultas.consultas'
    todayDate = datetime.today()

    name = fields.Char(string="Nombre", required=True)
    date = fields.Date(string="Fecha de Nacimiento", required=True)
    observaciones = fields.Text()
    dateTest = fields.Date(string="Fecha Test", required=True)

    _defaults = {
        'date': fields.Date.today(),
    }

    @api.onchange('name', 'date') #Decorador
    def _onchange_observaciones(self):
        self.observaciones = str(self.name) + ' fue creado en ' + str(self.date)

    @api.onchange('dateTest') #Decorador
    def _onchange_dateTest(self):
        is_on_holiday = False
        # Días festivos:
        holidaysMEX = [(datetime(2017, 1, 1), "Anio Nuevo [New Year's Day]"), \
        			   (datetime(2017, 2, 6), 'Dia de la Constitucion'), \
        			   (datetime(2017, 3, 20), "Natalicio de Benito Juarez"), \
        			   (datetime(2017, 5, 1), 'Dia del Trabajo'), \
        			   (datetime(2017, 11, 20), 'Dia de la Revolucion'), \
        			   (datetime(2017, 12, 25), 'Navidad')]

        if self.dateTest != False:
            current_date = self.dateTest.split('-')
            is_on_week = datetime(int(current_date[0]), int(current_date[1]), int(current_date[2]))
            for date, name in holidaysMEX:
                if date == is_on_week:
                    is_on_holiday = True

            # .isoweekday = Return the day of the week as an integer, where Monday is 1 and Sunday is 7
            is_on_week = is_on_week.isoweekday() in range(1, 6)

            if (not is_on_week) or is_on_holiday:
                raise Warning(_('No puede seleccionar días festivos o fines de semana'))



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
            queryFilter = self.env["consultas.citas"].search([('date', '>=', self.begin_date), ('date', '<=', self.end_date)])
            self.env.cr.fetchall()

        #******************************* 2)

        elif ((self.paciente.id == False) and (self.tags != False)):
            print("Filer 2:")
            queryFilter = self.env["consultas.citas"].search([('date', '>=', self.begin_date), ('date', '<=', self.end_date), ('observaciones', 'like', self.tags)])
            self.env.cr.fetchall()

        #******************************* 3)

        elif ((self.paciente.id != False) and (self.tags == False)):
            print("Filer 3:")
            queryFilter = self.env["consultas.citas"].search([('date', '>=', self.begin_date), ('date', '<=', self.end_date), ('citas_id', '=', self.paciente.id)])
            self.env.cr.fetchall()

        #******************************* 4)

        else:
            print("Filer 4:")
            queryFilter = self.env["consultas.citas"].search([('date', '>=', self.begin_date), ('date', '<=', self.end_date), ('observaciones', 'like', self.tags), ('citas_id', '=', self.paciente.id)])
            self.env.cr.fetchall()

        idsArray = []
        print queryFilter
        for record in queryFilter:
            idsArray.append(record.id)
            print record.citas_id.name

        self.citas_ids = [(6, 0, idsArray)]


        #**** Generar reporte
        return self.env['report'].get_action(self, "consultas.reports_template")
