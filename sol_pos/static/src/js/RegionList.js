odoo.define('sol_pos.RegionList', function(require) {
    'use strict';

    const PosComponent = require('point_of_sale.PosComponent');
    const Registries = require('point_of_sale.Registries');

    class RegionList extends PosComponent {
        get highlight() {
            return this.props.region !== this.props.selectedRegion ? '' : 'highlight';
        }
    }
    RegionList.template = 'RegionList';

    Registries.Component.add(RegionList);

    return RegionList;
});
