from odoo import fields, models, api, _
from xlsxwriter.utility import xl_range
from xlsxwriter.utility import xl_rowcol_to_cell
from xlsxwriter.utility import xl_cell_to_rowcol


class CashflowXlsx(models.AbstractModel):
    _name = 'report.lan_cashflow.cashflow_report_xlsx'
    _inherit = 'report.report_xlsx.abstract'

    def get_cash_and_bank(self, company, account, start_date, end_date):
        filt_account = ""
        if account:
            if len(account) == 1:
                filt_account = "where aa.id = %s" % account.id
            else:
                filt_account = "where aa.id in %s" % str(tuple(account.ids)) 
        query = """ with master_account as (
        select aa.id, concat(aa.code, ' ', aa.name) as name
        from account_account aa
        %s
        ),

        master_journal as (
        select aml.account_id, sum(aml.balance) as balance
        from account_move_line aml
        where aml.company_id = %s and aml.date BETWEEN '%s' and '%s'
        group by aml.account_id
        )
        select ma.name as account_name, coalesce(mj.balance, 0) as balance
        from master_account ma
        left join master_journal mj on mj.account_id = ma.id
        group by ma.name, mj.balance """ % (filt_account, company.id, start_date, end_date)
        self._cr.execute(query)
        return self._cr.dictfetchall()

    def get_income(self, company, sales, deduction, start_date, end_date):
        filt_sales = ""
        filt_deduction = ""
        if sales:
            filt_sales = "and aml.account_id = %s" % sales.id
        if deduction:
            if len(deduction) == 1:
                filt_deduction = "and aml.account_id = %s" % deduction.id
            else:
                filt_deduction = "and aml.account_id in %s" % str(tuple(deduction.ids)) 
        query = """ with master_sales as (
        select aml.account_id, sum(aml.credit) as credit
        from account_move_line aml
        where aml.company_id = %s and aml.date BETWEEN '%s' and '%s' %s
        group by aml.account_id
        ),
		master_deduction as (
        select aml.account_id, sum(aml.credit) as credit
        from account_move_line aml
        where aml.company_id = %s and aml.date BETWEEN '%s' and '%s' %s
        group by aml.account_id
        )
        select coalesce(ms.credit - (select md.credit from master_deduction md),0) as balance
        from master_sales ms
        """ % (company.id, start_date, end_date, filt_sales, company.id, start_date, end_date, filt_deduction)
        self._cr.execute(query)
        return self._cr.dictfetchone()

    def get_other_payable(self, company, start_date, end_date):
        query = """ with master_account as (
        select aa.id, aa.name
        from account_account aa
        where code = '21120'
        ),

        master_journal as (
        select aml.account_id, sum(aml.debit) as debit
        from account_move_line aml
        where aml.company_id = %s and aml.date BETWEEN '%s' and '%s'
        group by aml.account_id
        )
        select ma.name as account_name, coalesce(mj.debit, 0) as balance
        from master_account ma
        left join master_journal mj on mj.account_id = ma.id
        group by ma.name, mj.debit
        """ % (company.id, start_date, end_date)
        self._cr.execute(query)
        return self._cr.dictfetchone()

    def get_ap_trade(self, company, start_date, end_date):
        query = """ with master_account as (
        select aa.id, aa.name
        from account_account aa
        where code = '21110'
        ),

        master_journal as (
        select aml.account_id, sum(aml.debit) as debit
        from account_move_line aml
        where aml.company_id = %s and aml.date BETWEEN '%s' and '%s'
        group by aml.account_id
        )
        select ma.name as account_name, coalesce(mj.debit, 0) as balance
        from master_account ma
        left join master_journal mj on mj.account_id = ma.id
        group by ma.name, mj.debit
        """ % (company.id, start_date, end_date)
        self._cr.execute(query)
        return self._cr.dictfetchone()

    def get_other_income(self, company, start_date, end_date):
        query = """ with master_account as (
        select aa.id, aa.name
        from account_account aa
        where code = '81020'
        ),

        master_journal as (
        select aml.account_id, sum(aml.balance) as balance
        from account_move_line aml
        where aml.company_id = %s and aml.date BETWEEN '%s' and '%s'
        group by aml.account_id
        )
        select ma.name as account_name, coalesce(mj.balance, 0) as balance
        from master_account ma
        left join master_journal mj on mj.account_id = ma.id
        group by ma.name, mj.balance
        """ % (company.id, start_date, end_date)
        self._cr.execute(query)
        return self._cr.dictfetchone()

    def get_financing_activity(self, company, start_date, end_date):
        query = """ with master_account as (
        select aa.id, aa.name
        from account_account aa
        where name in ('Legal Fees','Office Supplies', 'Stationaries', 'Advertising', 'Entertainment', 'Travelling', 'Professional Fee') and aa.company_id = %s
        ),
        master_journal as (
        select aml.account_id, sum(aml.balance) as balance
        from account_move_line aml
        where aml.company_id = %s and aml.date BETWEEN '%s' and '%s'
        group by aml.account_id
        )
        select ma.name as account_name, coalesce(mj.balance, 0) as balance
        from master_account ma
        left join master_journal mj on mj.account_id = ma.id
        group by ma.name, mj.balance """ % (company.id, company.id, start_date, end_date)
        self._cr.execute(query)
        return self._cr.dictfetchall()

    def get_payment_to_supplier(self, company, start_date, end_date):
        query = """ 
        select coalesce(sum(aml.debit),0) as balance
        from account_move_line aml
        where aml.company_id = %s and aml.date BETWEEN '%s' and '%s' and aml.account_id in (21110, 21120, 21130)
        group by aml.account_id
         """ % (company.id, start_date, end_date)
        self._cr.execute(query)
        return self._cr.dictfetchone()

    def generate_xlsx_report(self, workbook, data, obj):
        money_format = workbook.add_format({'font_size': 12, 'align': 'right', 'valign': 'vcenter', 'bold':True, 'num_format': 'Rp#,##0.00' })
        text_style = workbook.add_format({'font_size': 12, 'align': 'left', 'valign': 'vcenter', 'bold':True })
        heading_format = workbook.add_format({'font_size': 14,  'align': 'center', 'valign': 'vcenter', 'bold': True })
      
        worksheet = workbook.add_worksheet('Cashflow Report')

        # utility
        push_right = " " * 8

        # Get Data
        cash_data = self.get_cash_and_bank(obj.company_id, obj.company_id.cash_bank_cashflow_ids, obj.start_date, obj.end_date)
        income = self.get_income(obj.company_id, obj.company_id.sales_income_cashflow_id, obj.company_id.sales_deduction_cashflow_ids, obj.start_date, obj.end_date)
        other_payable = self.get_other_payable(obj.company_id, obj.start_date, obj.end_date)
        ap_trade = self.get_ap_trade(obj.company_id, obj.start_date, obj.end_date)
        other_income = self.get_other_income(obj.company_id, obj.start_date, obj.end_date)
        payment_supplier = self.get_payment_to_supplier(obj.company_id, obj.start_date, obj.end_date)
        financing_activity = self.get_financing_activity(obj.company_id, obj.start_date, obj.end_date)

        # Set default value
        fa_total = 0
        cash_total = 0
        net_increase_total = 0

        # CONFIGURE ROW AND COLUMN
        worksheet.set_column('A:A', 4)
        worksheet.set_column('B:B', 60)
        worksheet.set_column('C:C', 30)

        worksheet.write("C1","Cashflow Report Periode %s - %s" % (obj.start_date.strftime("%d/%b/%Y"), obj.end_date.strftime("%d/%b/%Y")), heading_format)
        worksheet.write("A3","Cash and bank equivalents", text_style)
        worksheet.write("A4","cash and bank equivalents, beginning of period", text_style)

        row = 4

        # Cash
        for cash in cash_data:
            worksheet.write(row, 1, cash['account_name'], text_style)
            worksheet.write(row, 2, cash['balance'], money_format)
            cash_total += cash['balance']
            row +=1 

        worksheet.write(row, 0,"Total Cash and cash equivalents, beginning of period", text_style)
        worksheet.write(row,2, cash_total, money_format)				
        row += 2

        # Net Increase
        net_increase_row = row
        worksheet.write(row, 0, "Net increase in cash and cash equivalents", text_style)
        worksheet.write(row + 1, 1, "Cash flows from operating activities", text_style)
        worksheet.write(row + 1, 2, income['balance'] + other_payable['balance'] + ap_trade['balance'], money_format)

        row += 2
        worksheet.write(row, 1, push_right + "Income", text_style)
        worksheet.write(row, 2, income['balance'], money_format)

        row += 1
        worksheet.write(row, 1, "Cash received for operating activities", text_style)
        worksheet.write(row, 2,  income['balance'], money_format)

        row += 1
        if obj.company_id.name == 'PT. BAMBOO FASHION BALI':
            worksheet.write(row, 1, push_right + "Payment to Other Supplier", text_style)
            worksheet.write(row, 2,  other_payable['balance'], money_format)

            worksheet.write(row + 1, 1, push_right + "Payment to Taboo Trading", text_style)
            worksheet.write(row + 1, 2,  ap_trade['balance'], money_format)

            row += 2
            worksheet.write(row, 1, "Cash paid for operating activities", text_style)
            worksheet.write(row, 2,  other_payable['balance'] + ap_trade['balance'], money_format)
        else:
            worksheet.write(row, 1, push_right + "Payment to supplier", text_style)
            worksheet.write(row, 2,  payment_supplier['balance'] if payment_supplier else 0, money_format)

            row += 1
            worksheet.write(row, 1, "Cash paid for operating activities", text_style)
            worksheet.write(row, 2,  payment_supplier['balance'] if payment_supplier else 0, money_format)

        row += 1
        worksheet.write(row, 1, "Cash flows from extraordinary activities", text_style)
        worksheet.write(row, 2,  other_income['balance'], money_format)
        worksheet.write(row + 1, 1, push_right + "Sales of Fixed Asset", text_style)
        worksheet.write(row + 1, 2,  other_income['balance'], money_format)

        row += 2
        fa_first_row = row
        worksheet.write(row, 1, "Cash flows from financing activities", text_style)
        row += 1
        for fa in financing_activity:
            worksheet.write(row, 1, push_right + fa['account_name'], text_style)
            worksheet.write(row, 2, fa['balance'], money_format)
            fa_total += fa['balance']
            row +=1 
        worksheet.write(fa_first_row, 2, fa_total, money_format)
        worksheet.write(row, 1, "Cash paid for  financing activities", text_style)
        worksheet.write(row, 2, fa_total, money_format)

        # Total Net Increase
        net_increase_total = income['balance'] + other_income['balance'] + fa_total
        worksheet.write(net_increase_row, 2, net_increase_total, money_format)

        row += 2
        worksheet.write(row, 1, "Cash and cash equivalents, closing balance", text_style)
        worksheet.write(row, 2, cash_total + net_increase_total, money_format)

