# -*- coding: utf-8 -*-
##############################################################################
#
#    OpenERP, Open Source Management Solution
#    Copyright (C) 2004-2009 Tiny SPRL (<http://tiny.be>).
#
#    This program is free software: you can redistribute it and/or modify
#    it under the terms of the GNU Affero General Public License as
#    published by the Free Software Foundation, either version 3 of the
#    License, or (at your option) any later version.
#
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU Affero General Public License for more details.
#
#    You should have received a copy of the GNU Affero General Public License
#    along with this program.  If not, see <http://www.gnu.org/licenses/>.
#
##############################################################################

import openerp
from openerp import SUPERUSER_ID, tools
from openerp.osv import fields, osv
from openerp.tools.translate import _
from openerp import api, tools
import datetime
from datetime import datetime,timedelta

class res_company(osv.Model):
    _inherit = 'res.company'
    _columns = {
        'out_mail_count':fields.integer('Out Going Mails Count',help='Number of Mails should sent by ERP at a Time'),
    }
    _defaults={
               'out_mail_count':1,
               }  

class mail_mail(osv.Model):
    """ Update of mail_mail class, to add the signin URL to notifications. """
    _inherit = 'mail.mail'
       
    def send(self, cr, uid, ids, auto_commit=False, raise_exception=False, context=None):
        from_queue = False
        if context is None:
            context = {}
        if auto_commit and isinstance(auto_commit,dict) and 'from_queue' in auto_commit:
            context['from_queue'] = auto_commit['from_queue']
                    
        if context.has_key('from_queue') and context['from_queue']:
            user = self.pool.get("res.users").browse(cr, SUPERUSER_ID, SUPERUSER_ID, context=context)
            if ids and len(ids)>0:
                out_mail_count = user.company_id.out_mail_count
                ids = sorted(ids)[:out_mail_count]
                current_date=datetime.now()
                self.write(cr, uid, ids, {'date':current_date}, context=context)
                
            return super(mail_mail,self).send(cr, uid, ids, auto_commit=auto_commit, raise_exception=raise_exception, context=context)    
        return True    
        
    @api.cr_uid
    def process_email_queue(self, cr, uid, ids=None, context=None):
        if context is None:
            context = {} 
        context['from_queue'] = True
        return super(mail_mail,self).process_email_queue(cr, uid, ids=ids, context=context) 
    
        
