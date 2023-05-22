# Odoo XLSX Image Export

Export image from image fields directly to Excel and get valid image, rather than raw base64 value when using Odoo export feature.

## Features

- Global setting in Odoo Setting menu to globally enable this plugin, and configure max image height size and spacing tolerance in exported excel file.
- Export from any image fields in any model.
- Row and column will in exported excel file will be properly sized.

## Usage

- Enable the module in setting menu, set image height size and spacing tolerance.
- Do some export from any model.

## Screenshot
<img width="848" alt="Screenshot 2023-05-17 at 09 08 27" src="https://github.com/rlmyandaa/xlsx_image_export_odoo/assets/49233604/f60b5a8b-9248-4aee-b48b-a50c57a65bc6">
<img width="1440" alt="Screenshot 2023-05-17 at 09 18 33" src="https://github.com/rlmyandaa/xlsx_image_export_odoo/assets/49233604/4ab544f2-7213-4e56-a1af-e5a1e0e0c47a">
<img width="1440" alt="Screenshot 2023-05-17 at 09 18 45" src="https://github.com/rlmyandaa/xlsx_image_export_odoo/assets/49233604/eeebcd1a-330a-464f-b91f-2e1e1b9d8f11">


## Limitation

- Currently .webp image is not supported, so in the exported file it will become raw base64 value.
- Due to xlsxwriter x_scale and y_scale often output strange result in the final excel file, image will be resized first so that there will be no scaling config used when using xlsxwriter.
- The downside is that due to the image are being resized, there might be some quality loss especially if user tries to upscale the image in the final excel file.

## Changelog

See release

## Bug Tracking

Bugs are tracked on [GitHub Issues](https://github.com/rlmyandaa/odoo_data_migration_tools/issues). In case of trouble, please check there if your issue has already been reported. Any feedback or feature suggestion are welcomed.
