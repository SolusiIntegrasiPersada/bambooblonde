odoo.define("sol_pos.models", function (require) {
    "use strict";
    var models = require("point_of_sale.models");
    var core = require('web.core');
    var utils = require('web.utils');
    var PosDB = require("point_of_sale.DB");
    var _t = core._t;

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
});
