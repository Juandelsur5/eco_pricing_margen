# -*- coding: utf-8 -*-

from odoo import models
from odoo.exceptions import UserError


class Pricelist(models.Model):
    _inherit = 'product.pricelist'

    def _compute_price_rule(self, products_qty_partner, date=False, uom_id=False):
        # Ejecutar primero el motor nativo
        result = super()._compute_price_rule(products_qty_partner, date, uom_id)

        # Determinar canal según nombre de la lista
        pricelist_name = (self.name or '').upper()
        margin_field = None

        if 'T.A.T' in pricelist_name or 'PRECIO T.A.T' in pricelist_name:
            margin_field = 'x_margin_tat'
        elif 'MAYORISTA' in pricelist_name or 'MAYORISTAS' in pricelist_name:
            margin_field = 'x_margin_mayorista'
        elif 'P.O.S' in pricelist_name or 'POS' in pricelist_name:
            margin_field = 'x_margin_pos'
        elif 'OFERTA' in pricelist_name or 'OFERTAS' in pricelist_name:
            margin_field = 'x_margin_oferta'

        # Si la lista no corresponde a un canal controlado, no intervenir
        if not margin_field:
            return result

        # Recalcular precio por producto según utilidad del producto
        for product_id, qty, partner in products_qty_partner:
            if product_id not in result:
                continue

            product = self.env['product.product'].browse(product_id)
            if not product.exists():
                continue

            tmpl = product.product_tmpl_id
            margin_value = getattr(tmpl, margin_field, False)

            # Bloqueo real: sin utilidad definida no se vende por este canal
            if not margin_value or margin_value <= 0:
                raise UserError(
                    f'El producto "{tmpl.display_name}" no tiene utilidad definida '
                    f'para el canal de esta lista de precios.'
                )

            costo = tmpl.standard_price
            if not costo or costo <= 0:
                continue

            utilidad = margin_value / 100.0
            precio = costo / (1 - utilidad)

            # Respetar contrato del motor de precios
            result[product_id] = (False, precio)

        return result
