odoo.define('sol_pos.receipt', function (require) {
    "use strict";
    const Registries = require('point_of_sale.Registries');
    const OrderReceipt = require('point_of_sale.OrderReceipt');
    const models = require("point_of_sale.models");

    models.load_fields("product.product", ["is_shooping_bag", "is_price_pos_editable", "is_produk_diskon", "is_produk_promotion", "is_voucher"]);

    const PosResOrderReceipt = (OrderReceipt) =>
        class extends OrderReceipt {
            get receiptEnv() {
                const receipt_render_env = super.receiptEnv;

                if (!this.env.pos.config.is_custom_receipt) {
                    return receipt_render_env;
                }

                const receipt_design = this.env.pos.config.design_receipt;
                const order = this.env.pos.get_order();
                const receipts = order.export_for_printing();
                let promo_member = null;
                let promo_promotion = this.env.pos.db.all_promo_message;
                const code = receipts.client?.coupon_promo_id;

                if (code) {
                    promo_member = this.env.pos.coupon_programs_by_id[code[0]];
                }

                const order_line = order.get_orderlines();
                // debugger ; 
                const filteredOrderLine = order_line.filter((line) => !(
                    line.product.is_shooping_bag ||
                    line.product.is_produk_promotion ||
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
                        price_real: line.get_price_with_tax(),
                        discount: line.get_discount(),
                        is_diskon_promotion : line.check_if_offer_can_be_applied()
                    };
                });

                
                if (promo_member) {
                    const validProductIds = promo_member.valid_product_ids;
                    promo_promotion = null ;
                    filteredOrderLineAsArray.forEach((line) => {
                        if (validProductIds.has(line.product_id)) {
                            if (line.discount <= 0) {
                                const discountedPrice = line.price - (line.price * promo_member.discount_percentage / 100);
                                line.price = Math.max(discountedPrice, 0);
                                line.discount = promo_member.discount_percentage;
                            } else {
                                const discountedPriceReal = line.price_real + (line.price_real * promo_member.discount_percentage / 100);
                                line.price_real = discountedPriceReal;
                            }
                        }
                    });
                }

                const hasDiskonPromotion = filteredOrderLineAsArray.some((line) => line.is_diskon_promotion);

                if (!hasDiskonPromotion) {
                    promo_promotion = null;
                }
                    
                const pos_promotion_diskon = this.env.pos.db.discount_product;
                filteredOrderLineAsArray.forEach((line) => {
                    if (line.discount >= 0 && line.is_diskon_promotion) {
                        promo_member = null ;
                        const discountedPriceReal = line.price_real / (1 - (pos_promotion_diskon[0].percent_discount / 100));
                        line.price_real = discountedPriceReal;
                    }

                });

                const data = {
                    widget: this.env,
                    pos: this.env.pos,
                    order: order,
                    receipt: order.export_for_printing(),
                    orderlines: order.get_orderlines(),
                    filterorderlines: filteredOrderLineAsArray,
                    paymentlines: order.get_paymentlines(),
                    moment: moment,
                    promo: promo_member ? promo_member : null,
                    promo_promotion: promo_promotion ? promo_promotion : null,
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
