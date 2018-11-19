# -*- coding: utf-8 -*-
{
    'name': "Tamerri",

    'summary': """
        Tamerri Modules""",

    'description': """
        Long description of module's purpose
    """,

    'author': "MCEE Solutions",
    'website': "http://www.mceesolutions.com",

    # Categories can be used to filter modules in modules listing
    # Check https://github.com/odoo/odoo/blob/master/odoo/addons/base/module/module_data.xml
    # for the full list
    'category': 'Tamerri',
    'version': '0.3',


    # any module necessary for this one to work correctly
    'depends': ['base','sale','website','website_event', ],

    # always loaded
    'data': [
        'views/website_events_template.xml',
        'views/event_registration_view.xml',
    ],
    # only loaded in demonstration mode
    'demo': [
    ],
}
