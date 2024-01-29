"""
Add features in excel export to automatically convert raw base64 of an image to human readable image.
We will overide some function in /odoo/addons/web/controllers/main.py on ExportXlsxWriter.
"""

from odoo.exceptions import UserError
from odoo.tools import pycompat, ImageProcess
from odoo.tools.translate import _
import datetime
import random
import time
import io
import base64
import xlsxwriter
from odoo.http import request
from odoo.addons.base.models.ir_config_parameter import IrConfigParameter
from .utils import pixels_to_height, pixels_to_width, get_tolerance, CONFIG_PREFIX

"""
Set the max height pixel value for image column and toleration value.
Toleration value will be used to give some spacing for the image column.
"""
MAX_HEIGHT_IMAGE_CELL = 150
IMAGE_CELL_TOLERATION_PERCENT = 10


def write_cell(self, row, column, cell_value):
    """Overide write_cell function in ExportXlsxWriter.
    We will add some code to base64 to image in image column.

    Args:
        row (_type_): row
        column (_type_): column
        cell_value (_type_): cell value

    Raises:
        UserError: _description_
    """
    cell_style = self.base_style

    # Create a counter to skip normal writing when writing a image to cell.
    skip = False

    if isinstance(cell_value, bytes):
        try:
            # because xlsx uses raw export, we can get a bytes object
            # here. xlsxwriter does not support bytes values in Python 3 ->
            # assume this is base64 and decode to a string, if this
            # fails note that you can't export

            # Use try catch so that this image writing will only done when a binnary is a valid image.
            if self.enable_xlsx_image_export:
                try:
                    self.write_image(row, column, cell_value)
                    # Skip normal writing
                    skip = True
                except UserError:
                    # If not a valid image base64, fallback to original function
                    skip = False

            # If not an image, fallback to original function
            if not skip:
                cell_value = pycompat.to_text(cell_value)

        except UnicodeDecodeError:
            raise UserError(
                _("Binary fields can not be exported to Excel unless their content is base64-encoded. That does not seem to be the case for %s.") % self.field_names[column])

    if isinstance(cell_value, str):
        if len(cell_value) > self.worksheet.xls_strmax:
            cell_value = _(
                "The content of this cell is too long for an XLSX file (more than %s characters). Please use the CSV format for this export.") % self.worksheet.xls_strmax
        else:
            cell_value = cell_value.replace("\r", " ")
    elif isinstance(cell_value, datetime.datetime):
        cell_style = self.datetime_style
    elif isinstance(cell_value, datetime.date):
        cell_style = self.date_style
    if not skip:
        self.write(row, column, cell_value, cell_style)


def _update_max_width(self, column, new_width):
    """Update max_width information for final formating.

    Args:
        column (_type_): column
        new_width (_type_): new width value
    """
    self.use_max_width = True
    if self.max_width < new_width:
        self.max_width = new_width

    self.max_width_column.add(column)


def close(self):
    """Overide close function in ExportXlsxWriter.
    We will add some code to do final formating for all image column.
    """
    # Check if there are any image column, then set the correct column width for all image column.
    if self.use_max_width:
        for col in self.max_width_column:
            self.worksheet.set_column(
                col, col, width=pixels_to_width(self.max_width))

    self.workbook.close()
    with self.output:
        self.value = self.output.getvalue()


def write_image(self, row, column, base64_source: ImageProcess):
    """Custom write cell function to write base64 image to human readable image.

    Args:
        row (_type_): row
        column (_type_): column
        base64_source (ImageProcess): raw base64 value
    """
    # Generate a filename for the image
    filename = str(random.randint(1, 9999999)) + str(time.time()) + '.jpg'

    # Process the image.
    # Due to xlsxwriter x_scale and y_scale often output strange result in the final excel file,
    # we will resize the image first so that there will be no scaling.
    # The downside is that due to the image are being resized, there might be some quality loss
    # especially if user tries to upscale the image in the final excel file.
    # Use PNG to get the best quality.
    image_obj = ImageProcess(base64_source)
    image_obj.resize(max_height=self.cell_max_height_px)
    resized_img_b64 = image_obj.image_base64(
        quality=False,
        output_format='PNG'
    )

    # Convert to bytesio
    image_data = io.BytesIO(base64.b64decode(resized_img_b64))

    # Set row height, add some tolerance to get some spacing in the cell.
    self.worksheet.set_row(row, height=pixels_to_height(get_tolerance(self.cell_image_spacing_percent,
                                                                      self.cell_max_height_px)))

    # Update max_width value. We will use the highest max_width value to set the image column width
    # so that all image in the cell will correctly placed.
    self._update_max_width(column, get_tolerance(self.cell_image_spacing_percent,
                                                 image_obj.image.width))
    self.worksheet.insert_image(row, column, filename, {
                                "image_data": image_data, 'object_position': 1})


def __init__(self, field_names, row_count=0):
    self.field_names = field_names
    self.output = io.BytesIO()
    self.workbook = xlsxwriter.Workbook(self.output, {'in_memory': True})
    self.base_style = self.workbook.add_format({'text_wrap': True})
    self.header_style = self.workbook.add_format({'bold': True})
    self.header_bold_style = self.workbook.add_format(
        {'text_wrap': True, 'bold': True, 'bg_color': '#e9ecef'})
    self.date_style = self.workbook.add_format(
        {'text_wrap': True, 'num_format': 'yyyy-mm-dd'})
    self.datetime_style = self.workbook.add_format(
        {'text_wrap': True, 'num_format': 'yyyy-mm-dd hh:mm:ss'})
    self.worksheet = self.workbook.add_worksheet()
    self.value = False

    # XLSX Image Export variables
    self.use_max_width = False
    self.max_width = 0
    self.max_width_column = set()
    self.enable_xlsx_image_export = False
    self.cell_max_height_px = 0
    self.cell_image_spacing_percent = 0
    self._check_xlsx_image_export()

    if row_count > self.worksheet.xls_rowmax:
        raise UserError(_('There are too many rows (%s rows, limit: %s) to export as Excel 2007-2013 (.xlsx) format. Consider splitting the export.') %
                        (row_count, self.worksheet.xls_rowmax))


def _check_xlsx_image_export(self):
    ir_config_param: IrConfigParameter = request.env['ir.config_parameter'].sudo(
    )
    enable_xlsx_image_export = ir_config_param.get_param(
        '{}.enable_xlsx_image_export'.format(CONFIG_PREFIX))
    if enable_xlsx_image_export:
        self.enable_xlsx_image_export = True
        self.cell_max_height_px = float(ir_config_param.get_param(
            '{}.cell_max_height_px'.format(CONFIG_PREFIX))) or MAX_HEIGHT_IMAGE_CELL
        self.cell_image_spacing_percent = (float(ir_config_param.get_param(
            '{}.cell_image_spacing_percent'.format(CONFIG_PREFIX))) * 100) or IMAGE_CELL_TOLERATION_PERCENT
