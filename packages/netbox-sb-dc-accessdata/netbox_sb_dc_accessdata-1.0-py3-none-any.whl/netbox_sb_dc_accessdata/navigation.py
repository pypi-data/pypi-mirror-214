from extras.plugins import PluginMenuItem
from extras.plugins import PluginMenuButton, PluginMenuItem
from utilities.choices import ButtonColorChoices

keycard_buttons = [
    PluginMenuButton(
        link='plugins:netbox_sb_dc_accessdata:keycard_add',
        title='Add',
        icon_class='mdi mdi-plus-thick',
        color=ButtonColorChoices.GREEN
    )
]

key_buttons = [
    PluginMenuButton(
        link='plugins:netbox_sb_dc_accessdata:key_add',
        title='Add',
        icon_class='mdi mdi-plus-thick',
        color=ButtonColorChoices.GREEN
    )
]

menu_items = (
    PluginMenuItem(
        link='plugins:netbox_sb_dc_accessdata:keycard_list',
        link_text='Keycard',
        buttons=keycard_buttons
    ),
    PluginMenuItem(
        link='plugins:netbox_sb_dc_accessdata:key_list',
        link_text='Key',
        buttons=key_buttons
    ),
)