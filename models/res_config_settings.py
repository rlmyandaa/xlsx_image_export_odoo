from email.policy import default
from odoo import fields, models, api
from odoo.addons.base.models.ir_config_parameter import IrConfigParameter
from ..exporter.utils import CONFIG_PREFIX


class ResConfigSettings(models.TransientModel):
    _inherit = 'res.config.settings'

    enable_xlsx_image_export = fields.Boolean(
        string='Enable XLSX Image Export')
    cell_max_height_px = fields.Float(
        string='Max Height for Image in Cell', default=150)
    cell_image_spacing_percent = fields.Float(
        string='Spacing in percent for Image in Cell (in Percent)', default=10)

    def set_values(self):
        res = super(ResConfigSettings, self).set_values()
        ir_config_param: IrConfigParameter = self.env['ir.config_parameter']
        ir_config_param.set_param(
            '{}.enable_xlsx_image_export'.format(CONFIG_PREFIX), self.enable_xlsx_image_export
        )
        ir_config_param.set_param(
            '{}.cell_max_height_px'.format(CONFIG_PREFIX), self.cell_max_height_px
        )
        ir_config_param.set_param(
            '{}.cell_image_spacing_percent'.format(CONFIG_PREFIX), self.cell_image_spacing_percent / 100
        )
        return res

    def get_values(self):
        res = super(ResConfigSettings, self).get_values()
        ir_config_param: IrConfigParameter = self.env['ir.config_parameter'].sudo(
        )
        enable_xlsx_image_export = ir_config_param.get_param(
            '{}.enable_xlsx_image_export'.format(CONFIG_PREFIX))
        cell_max_height_px = float(ir_config_param.get_param(
            '{}.cell_max_height_px'.format(CONFIG_PREFIX)))
        cell_image_spacing_percent = float(ir_config_param.get_param(
            '{}.cell_image_spacing_percent'.format(CONFIG_PREFIX)))
        res.update(
            enable_xlsx_image_export=enable_xlsx_image_export,
            cell_max_height_px=cell_max_height_px or 150,
            cell_image_spacing_percent=cell_image_spacing_percent or 0.1
        )
        return res
