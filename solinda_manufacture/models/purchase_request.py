from odoo import _, api, fields, models
from datetime import date, datetime
from odoo.exceptions import ValidationError


class PurchaseRequest(models.Model):
    _inherit = 'purchase.request'

    bom_id = fields.Many2one('mrp.bom', string='BoM', copy=False)
    mrp_id = fields.Many2one('mrp.production', string='MO', copy=False)
    mrp_ids = fields.Many2many('mrp.production', string='MO', copy=False)
    mrp_count = fields.Integer('Mrp Count', compute='_compute_mrp_count')
    is_create_pps = fields.Boolean('Is Create Pre-Production Sample')

    @api.depends('mrp_ids')
    def _compute_mrp_count(self):
        for record in self:
            record.mrp_count = len(record.mrp_ids.ids)

    def show_mrp_prod(self):
        if self.mrp_count == 1:
            return {
                'name': _('Manufacturing Order'),
                'view_mode': 'form',
                'res_model': 'mrp.production',
                'type': 'ir.actions.act_window',
                'target': 'current',
                'res_id': self.mrp_id.id,
                'domain': [('id', 'in', self.mrp_ids.ids)],
                'context': {'create': False}
            }
        else:
            return {
                'name': _('Manufacturing Order'),
                'view_mode': 'tree,form', 'res_model': 'mrp.production',
                'type': 'ir.actions.act_window',
                'target': 'current',
                'domain': [('id', 'in', self.mrp_ids.ids)],
                'context': {'create': False}
            }

    def show_pps(self):
        return {
            'name': _('Pre-Production Sample'),
            'view_mode': 'form',
            'res_model': 'mrp.bom',
            'type': 'ir.actions.act_window',
            'target': 'current',
            'res_id': self.bom_id.id,
            'domain': [('id', '=', self.bom_id.id)],
            'context': {'create': False}
        }

    def get_location(self, product):
        company = self.env['res.company'].sudo().search([('is_manufacturing', '=', True)], limit=1)

        location_by_company = self.env['stock.location'].read_group(
            [('company_id', 'in', company.ids), ('usage', '=', 'production')],
            ['company_id', 'ids:array_agg(id)'], ['company_id'])

        location_by_company = {lbc['company_id'][0]: lbc['ids'] for lbc in location_by_company}
        if product:
            location = product.with_company(company).property_stock_production
        else:
            location = location_by_company.get(company.id)[0]
        return location

    def create_pps(self):
        for record in self:
            if record.is_create_pps:
                return record.show_pps()
            else:
                costing = 'costing_proto'
                if record.state == 'done':
                    costing = 'costing_product'
                tender_bom = self.env['tender.bom']
                label_hardware_ids = []
                for label in record.label_hardware_ids:
                    label_hardware_ids.append(
                        (0, 0, {
                            'description': label.description,
                            'color': label.color.id,
                            'qty_label': label.qty_label
                        })
                    )
                for line in record.line_ids:
                    material_ids = [
                        (0, 0, {'product_id': line.fabric_smp.id}),
                        (0, 0, {'product_id': line.lining_smp.id})
                    ]

                    parent_bom_id = tender_bom.create({
                        'name': line.product_id.name,
                        'product_tmpl_id': line.product_id.product_tmpl_id.id,
                        'date': date.today(),
                        'costing': costing
                    })
                    parent_bom_id.new_bom()
                    bom_id = self.env['mrp.bom'].search([('tender_id', '=', parent_bom_id.id)], limit=1)
                    bom_id.write({
                        'bom_line_ids': material_ids,
                        'label_hardware_ids': label_hardware_ids
                    })
                    bom_id._onchange_bom_line_variant_ids()
                    record.bom_id = bom_id.id

                record.is_create_pps = True
                return record.show_pps()

    def create_mo_production(self):
        mrp, mo_line, by_prod_temp, update = [], [], [], []
        BoM, location = False, False
        company = self.env['res.company'].search([('is_manufacturing', '=', True)], limit=1)
        company_bb = self.env['res.company'].search([('is_manufacturing', '=', False)], limit=1)
        if not company:
            raise ValidationError('Company for manufacture is not defined')
        if not company_bb:
            raise ValidationError('Company for SO is not defined')
        for data in self.sudo().line_ids:
            update.append(
                [0, 0, {
                    'product_id': data.product_id.id,
                    'name': data.name,
                    'product_uom_qty': data.product_qty,
                    'price_unit': 0,
                    'price_subtotal': 0
                }])

        so = self.env['sale.order'].create({
            'partner_id': company_bb.partner_id.id,
            'company_id': company.id,
            'order_line': update,
        })

        for i in self:
            if i.mrp_count > 0:
                return i.show_mrp_prod()
            else:
                prod_template = i.line_ids.mapped('product_id.product_tmpl_id')
                for pt in prod_template:
                    header_product = i.line_ids.filtered(
                        lambda x: x.product_id.detailed_type in ['consu', 'product']
                                  and x.product_id.product_tmpl_id.id == pt.id)[0]
                    prodpo_line = i.line_ids.filtered(
                        lambda x: x.product_id.detailed_type in ['consu', 'product']
                                  and x.product_id.product_tmpl_id.id == pt.id)
                    by_prod_temp = []
                    for o in prodpo_line:
                        by_prod_temp.append(
                            (0, 0, {
                                'product_id': o.product_id.id,
                                'product_uom_qty': o.product_qty,
                                'product_uom_id': o.product_uom_id.id,
                                'fabric_por_id': o.fabric_smp.id,
                                'lining_por_id': o.lining_smp.id,
                                'colour': o.colour, 'size': o.size
                            }))

                    for l in header_product:
                        if l.product_id:
                            # material_variant = []
                            # picking_type_id = False
                            # picking_type = self.env['stock.picking.type'].search([('warehouse_id','=',i.picking_type_id.warehouse_id.id),('code','=','mrp_operation')],limit=1)
                            # if picking_type:
                            #     picking_type_id = picking_type
                            location = i.get_location(l.product_id)
                            if l.product_id.bom_count > 0:
                                # BoM = self.env['mrp.bom'].search([('product_tmpl_id', '=', l.product_id.product_tmpl_id.id),('is_final', '=', True)])
                                BoM = self.env['mrp.bom'].search(
                                    [('product_tmpl_id', '=', l.product_id.product_tmpl_id.id)], limit=1)
                                if not BoM:
                                    # statement = 'BoM final is not defined in product %s.\nPlease choose the final BoM first!' % l.product_id.product_tmpl_id.name
                                    statement = 'BoM is not defined in product %s.\nPlease choose the BoM first!' % l.product_id.product_tmpl_id.name
                                    raise ValidationError(statement)
                                if not BoM.picking_type_id:
                                    statement = 'BoM Operation is not defined in product %s.\nPlease choose the operation first!' % l.product_id.product_tmpl_id.name
                                    raise ValidationError(statement)
                                if len(BoM) > 1:
                                    raise ValidationError('BoM more than 1!')  # if BoM:  #     for b in BoM.bom_line_variant_ids:  #         material_variant.append((0,0, {  #                 'product_id' : b.product_id.id,  #                 'product_qty' : b.product_qty,  #                 'product_uom_id' : b.product_uom_id.id,  #                 'supplier' : b.supplier.id,  #                 'ratio' : b.ratio,  #                 'sizes' : b.sizes,  #                 'shrinkage' : b.shrinkage,  #         }))
                            else:
                                statement = 'There is no BoM in product %s!' % l.product_id.product_tmpl_id.name
                                raise ValidationError(statement)
                            mp = self.env['mrp.production'].create({
                                'name': _('New'),
                                'product_id': l.product_id.id,
                                'product_qty': l.product_qty,
                                'product_uom_id': l.product_uom_id.id,
                                'bom_id': BoM.id,
                                'date_planned_start': datetime.now(),
                                'user_id': i.env.user.id,
                                'company_id': company.id,
                                'purchase_request_id': i.id,
                                'is_sample': True,
                                # 'purchase_id':i.id,
                                'sales_order_id': so.id,
                                'picking_type_id': BoM.picking_type_id.id,
                                'location_src_id': BoM.picking_type_id.default_location_src_id.id,
                                'location_dest_id': BoM.picking_type_id.default_location_dest_id.id,
                                'production_location_id': location.id,
                                # 'mrp_bom_variant_ids':material_variant,
                            })

                            if mp:
                                # mp.move_raw_ids = [(2, move.id) for move in mp.move_raw_ids.filtered(lambda m: m.bom_line_id)]
                                mrp.append(mp.id)
                                for j in i.line_ids:
                                    if j.product_id:
                                        mo_line.append(
                                            (0, 0, {
                                                'name': _('New'),
                                                'product_id': j.product_id.id,
                                                'location_dest_id': mp.location_dest_id.id,
                                                'location_id': location.id,
                                                'product_uom_qty': j.product_qty,
                                                'product_uom': j.product_id.uom_id.id
                                            }))
                                mp.bom_id = BoM.id
                                list_move_raw = [(4, move.id) for move in
                                                 mp.move_raw_ids.filtered(lambda m: not m.bom_line_id)]
                                moves_raw_values = mp._get_moves_raw_values()
                                move_raw_dict = {move.bom_line_id.id: move for move in
                                                 mp.move_raw_ids.filtered(lambda m: m.bom_line_id)}

                                for move_raw_values in moves_raw_values:
                                    if move_raw_values['bom_line_id'] in move_raw_dict:
                                        # update existing entries
                                        list_move_raw += [
                                            (1, move_raw_dict[move_raw_values['bom_line_id']].id, move_raw_values)]
                                    else:
                                        # add new entries
                                        list_move_raw += [(0, 0, move_raw_values)]
                                mp.move_raw_ids = list_move_raw
                                mp._onchange_workorder_ids()
                                mp.update({'move_byproduct_ids': mo_line, 'by_product_ids': by_prod_temp})
                                mp.update_qty_variant()
                                mp.update_qty_consume_with_variant()
                i.write({'mrp_ids': [(6, 0, mrp)], 'mrp_id': mp.id})
                return i.show_mrp_prod()
