from extras.plugins import PluginConfig

class SBDCAccessdataDataConfig(PluginConfig):
    name = 'netbox_sb_dc_accessdata'
    verbose_name = 'Datacenter Accessdata'
    description = 'SB DC Accessdata'
    version = '1.1'
    base_url = 'accessdata'

config = SBDCAccessdataDataConfig