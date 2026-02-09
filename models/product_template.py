from odoo import models, fields, api

class ProductTemplate(models.Model):
    _inherit = 'product.template'

    @api.depends('standard_price', 'x_margin_tat', 'x_margin_mayorista', 'x_margin_pos', 'x_margin_oferta', 'taxes_id')
    def _compute_prices(self):
        """Calculadora dinámica: Costo -> Utilidad -> Precio con IVA"""
        for record in self:
            tax_rate = sum(record.taxes_id.mapped('amount')) / 100.0 if record.taxes_id else 0.0
            
            def calc_prices(margin_percent):
                if margin_percent >= 100: return 0.0, 0.0
                precio_neto = record.standard_price / (1 - (margin_percent / 100.0))
                precio_iva = precio_neto * (1 + tax_rate)
                return precio_neto, precio_iva

            record.x_price_tat_sin_iva, record.x_price_tat_con_iva = calc_prices(record.x_margin_tat)
            record.x_price_mayorista_sin_iva, record.x_price_mayorista_con_iva = calc_prices(record.x_margin_mayorista)
            record.x_price_pos_sin_iva, record.x_price_pos_con_iva = calc_prices(record.x_margin_pos)
            record.x_price_oferta_sin_iva, record.x_price_oferta_con_iva = calc_prices(record.x_margin_oferta)
