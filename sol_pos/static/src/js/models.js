odoo.define("sol_pos.models", function (require) {
    "use strict";
    var models = require("point_of_sale.models");
    var core = require('web.core');
    var utils = require('web.utils');
    var PosDB = require("point_of_sale.DB");
    var _t = core._t;
    var round_pr = utils.round_precision;

    models.load_fields('res.partner', 'ref');

    models.PosModel.prototype.models.some(function (model) {
        if (model.model !== "product.product") {
            return false;
        }
        const superContext = model.context;
        model.context = function () {
            const context = superContext.apply(this, arguments);
            context.display_default_code = true;
            return context;
        };
        return true; // Exit early the iteration of this.models
    });

    PosDB.include({
        _partner_search_string: function (partner) {
            var str = partner.name || '';
            if (partner.barcode) {
                str += '|' + partner.barcode;
            }
            if (partner.address) {
                str += '|' + partner.address;
            }
            if (partner.phone) {
                str += '|' + partner.phone.split(' ').join('');
            }
            if (partner.mobile) {
                str += '|' + partner.mobile.split(' ').join('');
            }
            if (partner.email) {
                str += '|' + partner.email;
            }
            if (partner.vat) {
                str += '|' + partner.vat;
            }
            if (partner.ref) {
                str += '|' + partner.ref;
            }
            str = '' + partner.id + ':' + str.replace(':', '').replace(/\n/g, ' ') + '\n';
            return str;
        },
    });

    var _super_orderline = models.Orderline.prototype;
    models.Orderline = models.Orderline.extend({
        initialize: function (attr, options) {
            this.absolute_discount = 0;
            _super_orderline.initialize.apply(this, arguments);
        },
        init_from_JSON: function (json) {
            _super_orderline.init_from_JSON.apply(this, arguments);
            if (json.absolute_discount) {
                this.set_absolute_discount(json.absolute_discount);
            }
        },
        set_discount: function (discount) {
            if (this.get_absolute_discount()) {
                this.set_absolute_discount(0);
            }
            _super_orderline.set_discount.apply(this, arguments);
        },
        // Sets a absolute discount
        set_absolute_discount: function (discount) {
            var self = this;
            if (this.price < discount) {
                Gui.showPopup("ErrorPopup", {
                    title: _t("Warning"),
                    body: _t(
                        "It is not allowed to create a credit by discount: " +
                            discount +
                            self.pos.currency.symbol +
                            ". \r\n" +
                            "The discount value should not be higher than unit price " +
                            self.price +
                            self.pos.currency.symbol
                    ),
                });
                return false;
            }
            if (this.get_discount()) {
                this.set_discount(0);
            }
            this.absolute_discount = discount || 0;
            this.absolute_discountStr = String(this.absolute_discount);
            this.trigger("change", this);
        },
        // Returns the absolute discount
        get_absolute_discount: function () {
            return this.absolute_discount;
        },
        get_absolute_discount_str: function () {
            return this.absolute_discountStr;
        },
        clone: function () {
            var res = _super_orderline.clone.apply(this, arguments);
            res.absolute_discount = this.absolute_discount;
            return res;
        },
        // When we add an new orderline we want to merge it with the last line to see reduce the number of items
        // in the orderline. This returns true if it makes sense to merge the two
        can_be_merged_with: function (orderline) {
            // We don't merge discounted orderlines
            if (this.get_absolute_discount() > 0) {
                return false;
            }
            return _super_orderline.can_be_merged_with.apply(this, arguments);
        },
        export_as_JSON: function () {
            var res = _super_orderline.export_as_JSON.apply(this, arguments);
            res.absolute_discount = this.get_absolute_discount();
            res.absolute_discountStr = this.get_absolute_discount_str();
            return res;
        },
        // Used to create a json of the ticket, to be sent to the printer
        export_for_printing: function () {
            var res = _super_orderline.export_for_printing.apply(this, arguments);
            res.absolute_discount = this.get_absolute_discount();
            res.absolute_discountStr = this.get_absolute_discount_str();
            return res;
        },
        get_base_price: function () {
            var rounding = this.pos.currency.rounding;
            if (this.get_absolute_discount()) {
                return round_pr(
                    (this.get_unit_price() - this.get_absolute_discount()) *
                        this.get_quantity(),
                    rounding
                );
            }
            return _super_orderline.get_base_price.apply(this, arguments);
        },
        get_all_prices: function () {
            var res = _super_orderline.get_all_prices.apply(this, arguments);
            if (this.get_absolute_discount()) {
                var price_unit = this.get_unit_price() - this.get_absolute_discount();
                var taxtotal = 0;

                var product = this.get_product();
                var taxes_ids = product.taxes_id;
                var taxes = this.pos.taxes;
                var taxdetail = {};
                var product_taxes = [];

                _(taxes_ids).each(function (el) {
                    product_taxes.push(
                        _.detect(taxes, function (t) {
                            return t.id === el;
                        })
                    );
                });

                var all_taxes = this.compute_all(
                    product_taxes,
                    price_unit,
                    this.get_quantity(),
                    this.pos.currency.rounding
                );
                _(all_taxes.taxes).each(function (tax) {
                    taxtotal += tax.amount;
                    taxdetail[tax.id] = tax.amount;
                });
                res.priceWithTax = all_taxes.total_included;
                res.priceWithoutTax = all_taxes.total_excluded;
                res.tax = taxtotal;
                res.taxDetails = taxdetail;
            }
            return res;
        },
        get_display_price_without_discount: function () {
            if (this.pos.config.iface_tax_included) {
                return this.get_price_with_tax_without_discount();
            }
            return this.get_price_without_discount();
        },
        // Get orderline price without discount
        get_price_without_discount: function () {
            var rounding = this.pos.currency.rounding;
            return round_pr(this.get_unit_price() * this.get_quantity(), rounding);
        },
        get_price_with_tax_without_discount: function () {
            return this.get_all_prices_without_discounts().priceWithTax;
        },
        get_all_prices_without_discounts: function () {
            var price_unit = this.get_unit_price();
            var taxtotal = 0;

            var product = this.get_product();
            var taxes_ids = product.taxes_id;
            var taxes = this.pos.taxes;
            var taxdetail = {};
            var product_taxes = [];

            _(taxes_ids).each(function (el) {
                product_taxes.push(
                    _.detect(taxes, function (t) {
                        return t.id === el;
                    })
                );
            });

            var all_taxes = this.compute_all(
                product_taxes,
                price_unit,
                this.get_quantity(),
                this.pos.currency.rounding
            );
            _(all_taxes.taxes).each(function (tax) {
                taxtotal += tax.amount;
                taxdetail[tax.id] = tax.amount;
            });
            return {
                priceWithTax: all_taxes.total_included,
                priceWithoutTax: all_taxes.total_excluded,
                tax: taxtotal,
                taxDetails: taxdetail,
            };
        },
        apply_ms_data: function (data) {
            // This methods is added for compatibility with module https://www.odoo.com/apps/modules/12.0/pos_multi_session/
            if (_super_orderline.apply_ms_data) {
                _super_orderline.apply_ms_data.apply(this, arguments);
            }
            this.absolute_discount = data.absolute_discount;
            this.absolute_discountStr = data.absolute_discountStr;
            // Rerender Orderline Widget after updating data
            this.trigger("change", this);
        },
    });

    var _super_order = models.Order.prototype;
    models.Order = models.Order.extend({
        add_product: function (product, options) {
            _super_order.add_product.apply(this, arguments);
            var line = this.get_selected_orderline();
            if (line && options && typeof options.absolute_discount !== "undefined") {
                line.set_absolute_discount(options.absolute_discount);
            }
        },
        get_total_absolute_discount: function () {
            return round_pr(
                this.orderlines.reduce(function (sum, orderLine) {
                    return (
                        sum +
                        orderLine.get_absolute_discount() * orderLine.get_quantity()
                    );
                }, 0),
                this.pos.currency.rounding
            );
        },
        get_total_discount: function () {
            return (
                _super_order.get_total_discount.apply(this, arguments) +
                this.get_total_absolute_discount()
            );
        },
        set_order_note: function(order_note) {
            this.order_note = order_note;
        },
        get_order_note: function() {
            return this.order_note;
        },
        export_as_JSON: function() {
            var selectedOrder = _super_order.export_as_JSON.call(this);
            $.extend(selectedOrder, {note: this.get_order_note()});
            return selectedOrder;
        },
        export_for_printing: function(){
            var orders = _super_order.export_for_printing.call(this);
            $.extend(orders, {note: this.get_order_note() || ''});
            return orders;
        },
    });
});
