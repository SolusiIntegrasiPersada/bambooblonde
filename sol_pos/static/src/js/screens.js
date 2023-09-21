odoo.define("pos_absolute_discount.screens", function (require) {
    "use strict";
    var core = require('web.core');
	var QWeb = core.qweb;
	var models = require("point_of_sale.models");
    const Chrome = require('point_of_sale.Chrome');
    const NumpadWidget = require("point_of_sale.NumpadWidget");
    const Orderline = require('point_of_sale.Orderline');
    const OrderReceipt = require("point_of_sale.OrderReceipt");
    const PaymentScreen = require('point_of_sale.PaymentScreen');
    const ProductScreen = require("point_of_sale.ProductScreen");
    const Registries = require("point_of_sale.Registries");
	const RegionControlButton = require('sol_region_pos.RegionControlButton');
	models.load_fields("product.product", ["is_shooping_bag", "is_price_pos_editable"]);

    const PosChrome = (Chrome) =>
		class extends Chrome {
			async click_apply_promotions(event) {
				var self = this;
				var order = self.env.pos.get_order();
				if (order.is_offer_applied) {
					const { confirmed } = await self.showPopup('ConfirmPopup', {
						title: self.env._t('Remove Offer ?'),
						body: self.env._t('All Offer Products and Offers will be removed.'),
					});
					if (confirmed) {
						order.is_offer_applied = false;
						$('.fa.fa-gift').css({ "color": "white" });
						$('.fa.fa-gift.show_promotions').css({ "color": "tomato" });
						self.remove_offer_products();
					}
				} else {
					order.is_offer_applied = true;
					$('.apply_promotions .fa.fa-gift').css({ "color": "#6EC89B" });

					_.each(order.get_orderlines(), function (line) {
						if (!line.is_offer_product) {
							let qty = line.quantity
							line.set_quantity(qty);
						}
					})
				}
				this.render();
			}
			remove_offer_products() {
				var self = this;
				var order = self.env.pos.get_order();
				if (order) {
					var orderlines = self.env.pos.get_order().get_orderlines();
					if (orderlines.length) {
						_.each(orderlines, function (line) {
							if (line) {
								if (line.is_offer_product) {
									if (line.is_buy_x_get_y_product) {
										order.remove_orderline(line.id)
										return
									}
									if (line.is_buy_x_get_y__qty_product) {
										order.remove_orderline(line.id)
										return
									}
									if (line.free_product) {
										order.remove_orderline(line.id)
										return
									}
									line.is_offer_product = false
									line.is_discounted_product = false
									line.related_product_id = false
									line.set_discount(0);
								}
							}
						});
						self.render()
					}
					var orderlines = self.env.pos.get_order().get_orderlines();
					if (orderlines.length) {
						_.each(orderlines, function (line) {
							if (line) {
								// if(line.is_offer_product){
								if (line.is_discount_product) {
									order.remove_orderline(line.id)
									return
								}
								// }
							}
						});
						self.render()
					}
				}
			}
		};

    const PosNumpadWidget = (_NumpadWidget) =>
        class extends _NumpadWidget {
            async changeMode(mode) {
				if (mode === "price") {
					var order = this.env.pos.get_order();
					const selectedOrderLine = order.orderlines.models.find(orderLine => orderLine.selected);
					if (!selectedOrderLine.product.is_price_pos_editable) {
						await this.showPopup('ErrorPopup', {
							title: 'Cannot Price',
							body: 'Produk not Editable Price',
						});
						return ; 
					}
				} 
                super.changeMode(mode);
                if (mode === "discount") {
                    $(".mode-button:eq(1)").addClass("selected-mode");
                } else {
                    $(".mode-button:eq(1)").removeClass(
                        "selected-absolute-discount-mode"
                    );
                    $(".mode-button:eq(1)").removeClass("selected-mode");
                }
					

            }
			
        };

    const PosOrderline = (Orderline) => class extends Orderline {
		selectLine(event) {
			var self = this;
			super.selectLine(event);
			if ($(event.target).attr('class') == "fa fa-gift show_promotions") {
				$('#info_tooltip').remove();
				var x = event.pageX
				var y = event.pageY
				var inner_html = self.generate_html(this.props.line.product);
				$('.product-screen').prepend(inner_html);
				$('#info_tooltip').css("top", (y - 50) + 'px');
				$('#info_tooltip').css("left", (x - 3) + 'px');
				$('#info_tooltip').css("border-top-left-radius", "7%");
				$(".cross_img_bottom").hide();
				$('#info_tooltip').slideDown(100);
				$(".close_button").on("click", function () {
					$('#info_tooltip').remove();
				});
			}
		}
		generate_html(product) {
			var self = this;
			var offers = self.get_offers(product);
			var offer_details_html = QWeb.render('OfferDetails', {
				widget: self,
				offers: offers,
			});
			return offer_details_html;
		}
		get_offers(product) {
			var self = this;
			var product_id = product.id;
			var offers = []
			_.each(self.env.pos.db.promotions_by_sequence_id, function (promotions) {
				if (promotions.offer_type == 'discount_on_products') {
					if (self.env.pos.db.discount_items) {
						var flag = false
						var discount_val = 0
						var val = 0
						_.each(self.env.pos.db.discount_items, function (item) {
							flag = false
							if (promotions.discounted_ids.includes(item.id)) {
								if (!flag && item.apply_on == "1_products") {
									if (item.product_id[0] == product.id) {
										discount_val = item.percent_discount
										flag = true
									}
								}
								if (!flag && item.apply_on == "2_categories") {
									if (item.categ_id[0] == product.categ_id[0]) {
										discount_val = item.percent_discount
										flag = true
									}
								}
								if (!flag && item.apply_on == "3_all") {
									discount_val = item.percent_discount
									flag = true
								}
								if (flag) {
									if (val == 0) {
										val += 1
										item['offer_name'] = "Get " + item.discount + " Discount"
										offers.push(item)
									}
								}
							}
						});
					}
				} else if (promotions.offer_type == 'buy_x_get_y') {
					if (self.env.pos.db.buy_x_get_y) {
						for (var i = 1; i <= self.env.pos.db.buy_x_get_y.length; i++) {
							var item = self.env.pos.db.buy_x_get_y[self.env.pos.db.buy_x_get_y.length - i]
							if (promotions.buy_x_get_y_ids.includes(item.id)) {
								if (item.product_x_id[0] == product_id) {
									item['offer_name'] = "Buy " + item.qty_x + " " + product.display_name + " & Get " + item.product_y_id[1]
									offers.push(item)
								}
							}
						}
					}
				} else if (promotions.offer_type == 'buy_x_get_y_qty') {
					if (self.env.pos.db.buy_x_get_y_qty) {
						for (var i = 1; i <= self.env.pos.db.buy_x_get_y_qty.length; i++) {
							var item = self.env.pos.db.buy_x_get_y_qty[self.env.pos.db.buy_x_get_y_qty.length - i]
							if (promotions.buy_x_get_y_qty_ids.includes(item.id)) {
								if (item.product_x_id[0] == product_id) {
									item['offer_name'] = "Buy " + item.qty_x + " " + product.display_name + " & Get " + item.qty_y + " " + item.product_y_id[1]
									offers.push(item)
								}
							}
						}
					}
				} else if (promotions.offer_type == 'buy_x_get_discount_on_y') {
					if (self.env.pos.db.buy_x_get_discount_on_y) {
						for (var i = 1; i <= self.env.pos.db.buy_x_get_discount_on_y.length; i++) {
							var item = self.env.pos.db.buy_x_get_discount_on_y[self.env.pos.db.buy_x_get_discount_on_y.length - i]
							if (promotions.buy_x_get_discount_on_y_ids.includes(item.id)) {
								if (item.product_x_id[0] == product_id) {
									item['offer_name'] = "Buy " + item.qty_x + " " + product.display_name + " & Get " + item.discount + "% Discount on" + item.product_y_id[1]
									offers.push(item)
								}
							}
						}
					}
				}
			})
			return offers
		}
	};

    const PosOrderReceipt = (_OrderReceipt) =>
        class extends _OrderReceipt {
            isSimple(line) {
                return (
                    line.discount === 0 &&
                    line.unit_name === "Units" &&
                    line.absolute_discount === 0 &&
                    line.quantity === 1 &&
                    !(
                        line.display_discount_policy === "without_discount" &&
                        line.price !== line.price_lst
                    )
                );
            }
        };

    const PosPaymentScreen = (PaymentScreen) =>
		class extends PaymentScreen {
			async validateOrder(isForceValidate) {
				var self = this;
				super.validateOrder(isForceValidate)
				var current_order = self.env.pos.get_order();
				if (current_order.is_paid()) {
					self.env.pos.pos_session.order_count += 1;
					if (self.env.pos.get_order().get_client()) {
						self.env.pos.pos_session.customer_count += 1;
						self.env.pos.get_order().get_client().pos_order_count += 1;
					}
				}
			}
		};

    const PosProductScreen = (_ProductScreen) =>
        class extends _ProductScreen {
            constructor() {
                super(...arguments);
                this.absolute_discount_active = true;
                if (!this.env.pos.config.show_apply_promotion) {
					$(".apply_promotions").hide();
				}
            }

            _setValue(val) {
                if (
                    this.currentOrder.get_selected_orderline() &&
                    this.state.numpadMode === "discount"
                ) {
                    if (this.absolute_discount_active) {
                        this.currentOrder
                            .get_selected_orderline()
                            .set_absolute_discount(Number(val));
                    } else {
                        this.currentOrder.get_selected_orderline().set_discount(val);
                    }
                } else {
                    super._setValue(val);
                }
            }

            change_discount_type() {
                if (this.absolute_discount_active) {
                    this.absolute_discount_active = false;
                    $(".mode-button:eq(1)").removeClass(
                        "selected-absolute-discount-mode"
                    );
                } else {
                    this.absolute_discount_active = true;
                    $(".mode-button:eq(1)").addClass("selected-absolute-discount-mode");
                }
            }

            _setNumpadMode(event) {
                super._setNumpadMode(event);
                const {mode} = event.detail;
                if (mode === "discount") {
                    this.change_discount_type();
                }
            }

			async _onClickPay() {
				var region_data = this.env.pos.get_order().get_region();
				// console.log(region_data);
				// console.log(!region_data);
				// console.log('Custom _onClickPay function called.');
				// Memeriksa apakah region tidak kosong
				if (!region_data) {
					// Menampilkan pesan kesalahan jika region kosongs
					await this.showPopup('ErrorPopup', {
						title: 'Region Cannot be Empty',
						body: 'Please select Region',
					});
				} else {
					// Melanjutkan dengan operasi _super() jika region tidak kosong
					super._onClickPay();
				}
						}
        };

    Registries.Component.extend(Chrome, PosChrome);
    Registries.Component.extend(Orderline, PosOrderline);
    Registries.Component.extend(OrderReceipt, PosOrderReceipt);
    Registries.Component.extend(PaymentScreen, PosPaymentScreen);
    Registries.Component.extend(ProductScreen, PosProductScreen);
    Registries.Component.extend(NumpadWidget, PosNumpadWidget);
    return {Chrome, Orderline, OrderReceipt, PaymentScreen, ProductScreen, NumpadWidget};
});
