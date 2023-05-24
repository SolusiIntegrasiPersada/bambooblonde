
odoo.define('sol_region_pos.RegionScreenList', function(require) {
    'use strict';
    const PosComponent = require('point_of_sale.PosComponent');
    const Registries = require('point_of_sale.Registries');
  
    class RegionScreenList extends PosComponent {
        constructor() {
            super (... arguments);
            
            this.state = {
                selectedRegion: this.props.region,
            };

            this.regions = this.env.pos.regions;
       }

        get isNextButtonVisible() {
            return this.state.selectedRegion ? true : false;
        }
    
        get nextButton() {
            if (!this.props.region) {
                return { command: 'set', text: this.env._t('Set Region') };
            } else if (this.props.region &&  this.props.region === this.state.selectedRegion) {
                return { command: 'deselect', text: this.env._t('Deselect Region') };
            } else {
                return { command: 'set', text: this.env._t('Change Region') };
            }
        }

        clickNext() {
            this.state.selectedRegion = this.nextButton.command === 'set' ? this.state.selectedRegion : null;
            this.confirm();
        }

        confirm() {
            this.props.resolve({confirmed: true, payload: this.state.selectedRegion });
            this.trigger('close-temp-screen');
        }


       clickRegion(event){
            let region = event.detail.region;
            if (this.state.selectedRegion === region) {
                this.state.selectedRegion = null;
            } else {
                this.state.selectedRegion = region;
            }
            this.render();
       }
       back() {
            this.trigger('close-temp-screen');
       }
    }
    
    RegionScreenList.template = 'RegionScreenList';
    Registries.Component.add(RegionScreenList);
    
    return RegionScreenList;
  });