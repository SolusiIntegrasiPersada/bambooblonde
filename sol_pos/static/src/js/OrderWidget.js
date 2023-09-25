odoo.define("sol_pos.OrderWidget", function (require) {
    "use strict";

    const models = require("point_of_sale.models");
    const OrderWidget = require("point_of_sale.OrderWidget");
    const Registries = require("point_of_sale.Registries");
    models.load_fields("product.product", ["is_shooping_bag", "is_price_pos_editable","is_produk_diskon","is_produk_promotion","is_voucher"]);

    const OrderLineCount = OrderWidget => class extends OrderWidget {
        _updateSummary() {
            var result = super._updateSummary;
            var self = this;
            var order = self.env.pos.get_order();
            const total = self.order ? self.order.get_total_with_tax() : 0;
            const tax = self.order ? total - self.order.get_total_without_tax() : 0;
            self.state.total = self.env.pos.format_currency(total);
            self.state.tax = self.env.pos.format_currency(tax);

            let total_qty = 0;
            const lines = order.get_orderlines();
            
            lines.map(function (line) {
                // Memeriksa apakah produk adalah produk diskon atau voucher
                const diskon_coupon_shopping_bag = line.product.is_produk_diskon || line.product.is_voucher || line.product.is_shooping_bag || line.product.is_produk_promotion;
                // console.log('product name ===================', line.product.name)
                // console.log('product is_produk_diskon', line.product.is_produk_diskon)
                // console.log('product is_voucher', line.product.is_voucher)
                // console.log('product is_shooping_bag', line.product.is_shooping_bag)
                if (!diskon_coupon_shopping_bag) {
                    total_qty += line.quantity;
                } 
            });
            order.set_total_qty(total_qty)

            $('.tot-qty').html(total_qty);
            self.render();
        }
    }

    const _super_order = models.Order.prototype;
    models.Order = models.Order.extend({
        set_total_qty: function (total_qty) {
            this.total_qty = total_qty;
        },
    });

    // ProductsList.include({
    //     template: 'ProductList',
    //     init: function (parent, options) {
    //         parent.t = this.template;
    //         const self = this;
    //         this._super(parent, options);
    //
    //         this.keypress_product_handler = function (ev) {
    //             // React only to SPACE to avoid interfering with barcode scanner which sends ENTER
    //             if (ev.which != 13) {
    //                 return;
    //             }
    //             ev.preventDefault();
    //             const product = self.pos.db.get_product_by_id(this.dataset.productId);
    //             options._clickProduct(product);
    //             // $(".selected-mode").focus();
    //             // $(".numpad").focus();
    //         };
    //     },
    // });
    Registries.Component.extend(OrderWidget, OrderLineCount);
    return OrderWidget
});
