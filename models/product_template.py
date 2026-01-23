# -*- coding: utf-8 -*-

from odoo import models, fields, api


class ProductTemplate(models.Model):
    _inherit = 'product.template'

    x_margin_tat = fields.Float(string='Margen T.A.T (%)')
    x_margin_mayorista = fields.Float(string='Margen Mayorista (%)')
    x_margin_pos = fields.Float(string='Margen P.O.S (%)')
    x_margin_oferta = fields.Float(string='Margen Ofertas (%)')

    x_price_tat_sin_iva = fields.Float(string='Precio T.A.T sin IVA', compute='_compute_prices', store=False)
    x_price_tat_con_iva = fields.Float(string='Precio T.A.T con IVA', compute='_compute_prices', store=False)
    x_price_mayorista_sin_iva = fields.Float(string='Precio Mayorista sin IVA', compute='_compute_prices', store=False)
    x_price_mayorista_con_iva = fields.Float(string='Precio Mayorista con IVA', compute='_compute_prices', store=False)
    x_price_pos_sin_iva = fields.Float(string='Precio P.O.S sin IVA', compute='_compute_prices', store=False)
    x_price_pos_con_iva = fields.Float(string='Precio P.O.S con IVA', compute='_compute_prices', store=False)
    x_price_oferta_sin_iva = fields.Float(string='Precio Ofertas sin IVA', compute='_compute_prices', store=False)
    x_price_oferta_con_iva = fields.Float(string='Precio Ofertas con IVA', compute='_compute_prices', store=False)

    @api.depends('standard_price', 'x_margin_tat', 'x_margin_mayorista', 'x_margin_pos', 'x_margin_oferta', 'taxes_id')
    def _compute_prices(self):
        for record in self:
            record.x_price_tat_sin_iva = 0.0
            record.x_price_tat_con_iva = 0.0
            record.x_price_mayorista_sin_iva = 0.0
            record.x_price_mayorista_con_iva = 0.0
            record.x_price_pos_sin_iva = 0.0
            record.x_price_pos_con_iva = 0.0
            record.x_price_oferta_sin_iva = 0.0
            record.x_price_oferta_con_iva = 0.0

