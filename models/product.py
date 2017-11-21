from openerp import models, fields, api
from datetime import date
import StringIO
import base64

class Product(models.Model):
    _inherit = 'product.template'

    qty_low_stock_notify = fields.Integer(string='Quantite Minimum', default=50, help='Notifier quand la quantite est inferieur a la valeur specifiee')
    is_stock_alert = fields.Boolean(string='Stock Alert?', default=False)
    def send_low_stock_via_email(self, cr, uid, context=None):
        header_label_list=["Reference Interne", "Nom", "Caracteristiques", "Quantite Disponible", "Quantite Entrant"]
        # Get email template
        template_obj = self.pool.get('mail.template')
        template_ids = template_obj.search(cr, uid, [('name', '=', 'Dexxys Cameroon Stock Alert Template')])
        template     = template_obj.browse(cr, uid, template_ids)
        if template:
            default_body = template.body_html
            custom_body  = """
                <table>
                    <th style="padding-left:25px; text-align:left">%s</th>
                    <th style="padding-left:25px; text-align:left">%s</th>
                    <th style="padding-left:25px; text-align:left">%s</th>
                    <th style="padding-left:25px; text-align:left">%s</th>
                    <th style="padding-left:25px; text-align:left">%s</th>
            """ %(header_label_list[0], header_label_list[1], header_label_list[2], header_label_list[3], header_label_list[4])
            # Check for low stock products
            product_obj  = self.pool.get('product.product')
            product_attr_obj = self.pool.get('product.attribute.value')
            product_ids  = product_obj.search(cr, uid, [('active', '=', True), ('sale_ok', '=', True),  ('is_stock_alert', '=', True), ('default_code', '!=', False)])
            for product in product_obj.browse(cr, uid, product_ids):
                product_sku = product.default_code
                variant = ", ".join([v.name for v in product.attribute_value_ids])
                variant_display = ", ".join([v.display_name for v in product.attribute_value_ids])
                name = variant and "%s (%s)" % (product.name, variant) or product.name
                print variant + " " + name
                if not product_sku or product_sku == '':
                    continue
                qty_available = product.qty_available
                qty_incoming  = product.incoming_qty
                qty_low_stock_notify = product.qty_low_stock_notify
                if qty_available <= qty_low_stock_notify and qty_low_stock_notify >= 0: ## set low_stock_notify = -1 to never be notified
                    custom_body += """
                        <tr style="font-size:14px;">
                            <td style="padding-left:25px; text-align:left">%s</td>
                            <td style="padding-left:25px; text-align:left">%s</td>
                            <td style="padding-left:25px; text-align:left">%s</td>
                            <td style="padding-left:25px; text-align:left">%s</td>
                            <td style="padding-left:25px; text-align:left">%s</td>
                        </tr>
                    """ %(product_sku, product_sku, product_sku, str(qty_available), str(qty_incoming))
            custom_body  += "</table>"
            template.body_html = default_body + custom_body
            send_email         = template_obj.send_mail(cr, uid, template.id, uid, force_send=True, context=context)
            template.body_html = default_body
            return True
