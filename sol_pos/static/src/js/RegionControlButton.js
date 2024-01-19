odoo.define('sol_pos.RegionControlButton', function (require) {
    'use strict';
    const PosComponent = require('point_of_sale.PosComponent');
    const ProductScreen = require('point_of_sale.ProductScreen');
    const Registries = require('point_of_sale.Registries');
    const { useListener } = require('web.custom_hooks');
  
    const models = require('point_of_sale.models');

    models.load_models({
        model:  'visitor.region',
        fields: ['id', 'name'],
        loaded: function(self, regions){
            self.regions = regions;
        },
    });

    var _super_order = models.Order.prototype;

    models.Order = models.Order.extend({
        initialize: function(attributes,options){
            this.set({region:null});
            _super_order.initialize.apply(this, arguments);
            return this;
        },
        init_from_JSON: function(json) {
            _super_order.init_from_JSON.apply(this, arguments);
            this.set_region(json.region_id);
        },
        set_region: function(region){
            this.assert_editable();
            this.set('region', region);
        },
        get_region: function(){
            return this.get('region');
        },
        export_as_JSON: function(){
            var json = _super_order.export_as_JSON.apply(this,arguments);
            json.region_id = this.get_region() ? this.get_region(): false;
            return json;
        },
    });

    models.PosModel = models.PosModel.extend({
        get_region: function() {
            var order = this.get_order();
            if (order) {
                return order.get_region();
            }
            return null;
        },
    }); 


    class RegionControlButton extends PosComponent {
        constructor() {
            super(...arguments);
            useListener('click', this._onClick);
        }

        async _onClick() {
            const currentRegion =  this.region;
            const { confirmed, payload: newRegion } = await this.showTempScreen('RegionScreenList', {region: currentRegion });

            if (confirmed) {
                this.env.pos.get_order().set_region(newRegion);
            }


        }

        get region(){
            return this.env.pos.get_order().get_region();
        }
    }

    RegionControlButton.template = 'RegionControlButton';

    ProductScreen.addControlButton({
        component: RegionControlButton,
        condition: function () {
            return true;
        },
        position: ['before', 'SetPricelistButton'],
    });

    Registries.Component.add(RegionControlButton);
    
    return RegionControlButton;
});