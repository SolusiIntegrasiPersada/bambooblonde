odoo.define('sol_pos.receipt', function (require) {
    "use strict";
    const Registries = require('point_of_sale.Registries');
    const OrderReceipt = require('point_of_sale.OrderReceipt');
    const models = require("point_of_sale.models");
    
    models.load_fields("product.product", ["is_shooping_bag", "is_price_pos_editable", "is_produk_diskon", "is_produk_promotion", "is_voucher"]);

    // extending the pos receipt screen
    const PosResOrderReceipt = OrderReceipt =>
        class extends OrderReceipt {
            get receiptEnv() {
                const receipt_render_env = super.receiptEnv;

                if (!this.env.pos.config.is_custom_receipt) {
                    return receipt_render_env;
                }

                const receipt_design = this.env.pos.config.design_receipt;
                const order = this.env.pos.get_order();
                const receipts = order.export_for_printing();
                const code = receipts.client?.coupon_promo_id;
                const promo = code && this.env.pos.coupon_programs_by_id[code];

                const order_line = order.get_orderlines();

                // Filter order line
                const filteredOrderLine = order_line.filter((line) => !(
                    line.product.is_shooping_bag ||
                    line.product.is_produk_promotion ||
                    line.product.is_voucher ||
                    line.product.is_produk_diskon
                ));

                const filteredOrderLineVoucher = order_line.filter((line) => (line.product.is_produk_promotion));
                const totalPrice_voucher = filteredOrderLineVoucher.reduce((accumulator, line) => {
                    return accumulator + line.get_price_with_tax();
                }, 0);

                const filteredOrderLineAsArray = filteredOrderLine.map((line) => {
                    return {
                        product_id: line.product.id,
                        product_name: line.product.display_name,
                        quantity: line.get_quantity(),
                        price: line.get_price_with_tax(),
                        discount: line.get_discount(),
                    };
                });

                if (promo) {
                    const validProductIds = promo.valid_product_ids;
                    filteredOrderLineAsArray.forEach((line) => {
                        if (validProductIds.has(line.product_id)) {
                            line.price = (line.price - (line.price * promo.discount_percentage / 100));
                        }
                        line.discount = promo.discount_percentage;
                    });
                }

                const data = {
                    widget: this.env,
                    pos: this.env.pos,
                    order: order,
                    receipt: order.export_for_printing(),
                    orderlines: order.get_orderlines(),
                    filterorderlines: filteredOrderLineAsArray,
                    paymentlines: order.get_paymentlines(),
                    moment: moment,
                    promo: promo,
                    vouchers: Math.abs(totalPrice_voucher),
                };

                const parser = new DOMParser();
                const xmlDoc = parser.parseFromString(receipt_design, "text/xml");
                const s = new XMLSerializer();
                const newXmlStr = s.serializeToString(xmlDoc);
                const qweb = new QWeb2.Engine();
                qweb.add_template('<templates><t t-name="receipt_design">'
                    + newXmlStr + '</t></templates>');
                const receipt = qweb.render('receipt_design', data);
                $('div.pos-receipt').replaceWith(receipt);

                return receipt_render_env;
            }
        };

    Registries.Component.extend(OrderReceipt, PosResOrderReceipt);

    return OrderReceipt;
});
