# -*-coding:utf-8-*-
from odoo import models, fields, api
#from plainbox.impl.unit.validators import compute_value_map

class EventEvent(models.Model):
    _inherit = 'event.event'
    
    vendor = fields.Boolean(string='Vendor?')
    
class EventRegistration(models.Model):
    _inherit = 'event.registration'
    
    vendor = fields.Boolean(string='Vendor?', related='event_id.vendor', readonly=True)
    
    business = fields.Char(string='Business')
    
    address = fields.Text(string='Address')
    
    city = fields.Text(string='City')
    
    business_phone = fields.Char(string='Business Phone')
    
    bus_state = fields.Text(string='State')
    
    website = fields.Char(string='Website')
    
    sells = fields.Char(string='List of items you sell')
    
    sale_order_id = fields.Many2one(
        comodel_name='sale.order',
        string='Sale Order'
        )
    
    total = fields.Monetary(
        string='Total',
        related='sale_order_id.amount_total')
    
    quantity = fields.Float(
        string='Quantity(Number of Tickets)',
        related='sale_order_id.quantities')
    
    currency_id = fields.Many2one("res.currency", related='sale_order_id.pricelist_id.currency_id', string="Currency", readonly=True, required=True)
    
    state = fields.Selection([
        ('draft', 'Unconfirmed'), ('paid', 'Paid'), ('cancel', 'Cancelled'),
        ('open', 'Confirmed'), ('done', 'Done')],
        string='Status', default='draft', readonly=True, required=True, copy=False,
        help="If event is created, the status is 'Draft'. If event is confirmed for the particular dates the status is set to 'Confirmed'. If the event is over, the status is set to 'Done'. If event is cancelled the status is set to 'Cancelled'.")
    
    @api.multi
    def reg_paid(self):
        self.write({'state': 'paid'})
        return {}

class SaleOrder(models.Model):
    _inherit = "sale.order"
    
    quantities = fields.Float(
        string='Quantity(Number of Tickets)',
        compute='_total_unit', readonly=True)
    
    @api.depends('order_line.product_uom_qty')
    def _total_unit(self):
        quantities = 0.0
        for line in self.order_line:
            self.quantities += line.product_uom_qty