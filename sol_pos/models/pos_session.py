# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

from collections import defaultdict
from datetime import timedelta

from odoo import api, fields, models, _, Command
from odoo.exceptions import AccessError, UserError, ValidationError
from odoo.tools import float_is_zero, float_compare


class PosSession(models.Model):
    _inherit = 'pos.session'
    
    visitor_count = fields.Integer(string='Visitor Count')
    customer_count = fields.Integer(compute="_compute_customer_and_order_cont", string='Customer Count')
    order_count = fields.Integer(compute="_compute_customer_and_order_cont", string="Order Count")

    def _compute_customer_and_order_cont(self):
        for pos_obj in self:
            pos_obj.customer_count = pos_obj.env['pos.order'].search_count(
                [('partner_id', '!=', False), ('session_id', '=', pos_obj.id)])
            pos_obj.order_count = pos_obj.env['pos.order'].search_count([('session_id', '=', pos_obj.id)]) + 1
    
    
    def _validate_session(self, balancing_account=False, amount_to_balance=0, bank_payment_method_diffs=None):
        
        res = super(PosSession,self)._validate_session(balancing_account,amount_to_balance,bank_payment_method_diffs)
        for session in self :
            self.compute_name_journal(session, 'validate')
                
        
        return res

    def compute_name_journal(self, session, param):
        moves = session._get_related_account_moves()
        shift = self.shift or ""
        pos_config = self.config_id.name
        for move in moves :
            if param == 'validate' :
                ref_ori = move.ref or ""
                move.ref_ori = ref_ori
            else :
                ref_ori = move.ref_ori or ""
                
            info_pos = ('-%s/%s' % (pos_config, shift)) if ref_ori else ('%s/%s' % (pos_config, shift)) if shift else pos_config

                    
            ref = ref_ori + info_pos
            
            move.shift = shift
            move.pos_config = pos_config
            move.ref = ref
    
    # @api.onchange('shift')
    # def onchange_shift(self):
    #     if self.shift :
    #         self.compute_name_journal(self, 'onchange')
            
    
    def write(self, values):
        res = super(PosSession,self).write(values)
        if values.get('shift', False) :
            for session in self :
                self.compute_name_journal(session, 'write')
        return res
    
    
