# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

from odoo import http, _
from odoo.addons.website_event.controllers.main import WebsiteEventController
from odoo.http import request

class WebsiteEventSaleController(WebsiteEventController):

    @http.route(['/event/<model("event.event"):event>/registration/confirm'], type='http', auth="public", methods=['POST'], website=True)
    def index(self, event, **post):
        order = request.website.sale_get_order(force_create=1)
        attendee_ids = set()

        registrations = self._process_registration_details(post)
        for registration in registrations:
            ticket = request.env['event.event.ticket'].sudo().browse(int(registration['ticket_id']))
            cart_values = order.with_context(event_ticket_id=ticket.id, fixed_price=True)._cart_update(product_id=ticket.product_id.id, add_qty=1, registration_data=[registration])
            attendee_ids |= set(cart_values.get('attendee_ids', []))

        # free tickets -> order with amount = 0: auto-confirm, no checkout
        if order.amount_total:
            order.action_confirm()  # tde notsure: email sending ?
            attendees = request.env['event.registration'].browse(list(attendee_ids))
            # clean context and session, then redirect to the confirmation page
            request.website.sale_reset()
            return request.render("website_event.registration_complete", {
                'attendees': attendees,
                'event': event,
            })

        return request.redirect("/shop/checkout")

        

class Congratulations(http.Controller):
    
    @http.route('/event/payment_successful', type='http', auth='public', methods=['POST'], website=True, csrf=False)
    def show_congratulation_webpage(self, **kw):
        attendees = request.env['event.registration']
        orders = attendees.reg_paid()
        return http.request.render('tamerri.paid_thank_you', {
            'attendees': attendees,
            'orders': orders})
        
    @http.route('/event/payment_failed', type='http', auth='public', methods=['POST'], website=True, csrf=False)
    def show_failed_webpage(self, **kw):
        attendees = request.env['event.registration']
        return http.request.render('tamerri.payment_failed', {
            'attendees': attendees})