# Copyright 2018 VIM IT

{
    'name': 'DoctorAnyTime workflow',
    'version': '11.2.3',
    'category': 'Customization',
    'license': 'AGPL-3',
    'author': "RealDev ",
    'depends': ['base', 'crm','web' ,'sale_subscription'],
    'data': [

        'security/ir.model.access.csv',
        'views/res_partner_fields_view.xml',
        'views/res_partner_view.xml',
        'views/account_invoice_view.xml',
        'views/target_report.xml',
        'views/sale_subscription_view.xml',

        'static/src/xml/template.xml',

        'rview/subscription_report.xml',
        'rview/partner_activity_report_views.xml',
        'rview/stage_track_report_views.xml',
        'rview/partner_sub_report_views.xml',
        'rview/stage_retired_track_report_views.xml',
        'rview/partner_activity_report_div_bd_views.xml',
        'rview/partner_report_div_bd_views.xml',
        'rview/ftof_signed_report_views.xml',
        'rview/call_ftof_report_views.xml',
        'rview/called_signed_report_views.xml',

    ],
    'installable': True,
}
