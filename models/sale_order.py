from odoo import models, fields, api, _
from odoo.exceptions import ValidationError


class SaleOrderPassenger(models.Model):
    _inherit = 'sale.order'

    event_id = fields.Many2one(
        'event.event',
        string='Tour',
        help="Sélectionnez le voyage ou l’événement associé à cette commande."
    )

    @api.onchange('event_id')
    def _onchange_event_id(self):
        """Quand on choisit un tour, ajouter automatiquement les produits associés"""
        if self.event_id and self.event_id.event_ticket_ids:
            self.order_line = [(5, 0, 0)]  # vider les lignes existantes
            lines = []
            for ticket in self.event_id.event_ticket_ids:
                product = ticket.product_id
                if product:
                    lines.append((0, 0, {
                        'product_id': product.id,
                        'product_uom_qty': 1,
                        'price_unit': product.lst_price,
                    }))
            self.order_line = lines
