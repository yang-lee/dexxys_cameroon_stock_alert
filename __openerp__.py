{
    'name' : 'Dexxys Cameroon Stock Alert',
    'version' : '2.0',
    'author' : 'Dexxys Cameroon',
    'summary' : 'Inventory Managers Product',
    'description' : 'Alert Managers about stock quantities',
    'category' : 'Sales and Inventory Management',
    'depends' : ['base', 'mail', 'product'],
    'data':[
    			'data/email_template.xml',
                'views/product_template.xml',
                'views/ir_cron.xml'
    		],
    'installable': True
}
