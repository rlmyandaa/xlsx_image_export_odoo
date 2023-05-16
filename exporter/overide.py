from odoo.addons.web.controllers.main import ExportXlsxWriter
from .xlsx_image import _check_xlsx_image_export, __init__, _update_max_width, write_cell, write_image, close

"""OVERIDE FUNCTION IN ExportXlsxWriter"""
setattr(ExportXlsxWriter, '_check_xlsx_image_export', _check_xlsx_image_export)
setattr(ExportXlsxWriter, '__init__', __init__)
setattr(ExportXlsxWriter, '_update_max_width', _update_max_width)
setattr(ExportXlsxWriter, 'write_image', write_image)
setattr(ExportXlsxWriter, 'write_cell', write_cell)
setattr(ExportXlsxWriter, 'close', close)
