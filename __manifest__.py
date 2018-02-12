# Copyright 2018 VIM IT

{
    'name': 'DoctorAnyTime workflow',
    'version': '11.0.1',
    'category': 'Customization',
    'license': 'AGPL-3',
    'author': "RealDev ",
    'depends': ['base', 'crm','web'],
        # ,'sale_subscription'],
    'data': [

        'views/res_partner_view.xml',
        # 'views/sale_subscription_view.xml',
        'views/res_partner_fields_view.xml',

        'static/src/xml/template.xml',
        'report/partner_activity_report_views.xml',
        'report/stage_track_report_views.xml',

    ],
    'installable': True,
}
