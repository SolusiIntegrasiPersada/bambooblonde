odoo.define('sol_pos.PaymentScreen', function(require) {
    'use strict';

    const { Gui } = require('point_of_sale.Gui');
    const PaymentScreen = require('point_of_sale.PaymentScreen');
    const Registries = require('point_of_sale.Registries');

    const PosNotePaymentScreen = PaymentScreen => class extends PaymentScreen {
        async validateOrder(isForceValidate) {
            if(this.env.pos.config.is_order_note) {
                var selectedOrder = this.env.pos.get_order();
                var cashier = $('#pos_order_note').val()
                if (cashier === '') {
                    await Gui.showPopup('ErrorPopup', {
                        title: ('Cashier Cannot be Empty'),
                        body: ('Please input cashier')
                    });
                } else {
                    selectedOrder.set_order_note(cashier);
                    super.validateOrder(...arguments);
                }
            }
        }
    };

    Registries.Component.extend(PaymentScreen, PosNotePaymentScreen);

    return PaymentScreen;
});
