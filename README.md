# Odoo XLSX Image Export

  

Export image from image fields directly to exported Excel file. For Odoo version before 17, check related version from branch list. 

## Features

  

- Global setting in Odoo Setting menu to globally enable this plugin
  
- Configurable image sizing by customizing max image height size and spacing tolerance in exported excel file.

- Export from any image fields in any model.

- Row and column will in exported excel file will be properly sized.

  

## Usage

  

- Enable the module in setting menu, set image height size and spacing tolerance.
<img width="1435" alt="Screenshot 2024-01-29 at 16 13 24" src="https://github.com/rlmyandaa/xlsx_image_export_odoo/assets/49233604/a9db9281-0f32-4010-99e2-2dc413d996a8">


- Do some export from any model.

  

## Screenshot

<img width="1435" alt="image" src="https://github.com/rlmyandaa/xlsx_image_export_odoo/assets/49233604/d42326f3-7fde-48be-a028-d382c4aa455d">

<img width="1435" alt="image" src="https://github.com/rlmyandaa/xlsx_image_export_odoo/assets/49233604/bfa381ed-36c7-4a5d-b0d5-a81576b40dda">

<img width="1435" alt="image" src="https://github.com/rlmyandaa/xlsx_image_export_odoo/assets/49233604/0f6c4d5c-f2ef-42de-8e58-68443ab54207">

  
  

## Limitation

  

- Currently .webp image is not supported, so in the exported file it will become raw base64 value.

- Due to xlsxwriter x_scale and y_scale often output strange result in the final excel file, image will be resized first so that there will be no scaling config used when using xlsxwriter. The downside is that due to the image are being resized, there might be some quality loss especially if user tries to upscale the image in the final excel file.

  

## Changelog

  

See release

  

## Bug Tracking

  

Bugs are tracked on [GitHub Issues](https://github.com/rlmyandaa/odoo_data_migration_tools/issues). In case of trouble, please check there if your issue has already been reported. Any feedback or feature suggestion are welcomed.
