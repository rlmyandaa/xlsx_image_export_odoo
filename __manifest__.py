# -*- coding: utf-8 -*-
{
    'name': "XLSX Image Export",

    'summary': """
        Export image from image fields to excel to human readable image rather than base64 value.""",

    'description': """
        Export image from image fields to excel to human readable image rather than base64 value.
    """,

    'author': "Hersyanda Putra Adi",
    'website': "https://www.hrsynd.site",
    'category': 'Uncategorized',
    'version': '1.0',

    # any module necessary for this one to work correctly
    'depends': ['base', 'web'],

    # always loaded
    'data': [
        'views/res_config_settings_view.xml',
    ],
    # only loaded in demonstration mode
    'demo': [
    ],
}
