import datetime
from wsqluse import wsqluse
from gtki_module_exex.mixins import XlsCreator, TemplateCreator, DataFiller, IshbDailyReportTemplate
from ar_qdk.main import ARQDK

class CreateExcel(XlsCreator, TemplateCreator, DataFiller):
    def __init__(self, file_name, data_list, column_names=None):
        if column_names:
            self.column_names = column_names
        self.data_list = data_list
        self.file_name = file_name
        self.workbook = self.create_workbook()
        self.worksheet = self.create_worksheet()

    def create_document(self):
        self.create_template()
        row_num = 1
        for row in self.data_list:
            self.create_row(row, row_num)
            row_num += 1
        self.workbook.close()


class CreateExcelActs(CreateExcel):
    def __init__(self, file_name, acts_list, amount_info,
                 column_names=None):
        super().__init__(file_name, acts_list, column_names)
        self.amount_info = amount_info

    def create_amount(self, amount_info):
        merge_format = self.workbook.add_format({'align': 'center',
                                                 'bold': True})
        merge_format.set_font_size(14)
        self.worksheet.merge_range('A2:L2', amount_info, merge_format)

    def create_document(self):
        self.create_template()
        self.create_amount(self.amount_info)
        row_num = 2
        for row in self.data_list:
            self.create_row(row, row_num)
            row_num += 1
        self.workbook.close()


class CreateExcelDailyReport(XlsCreator):
    def __init__(self, file_name, ar_ip, ar_port,
                 column_names=None):
        self.file_name = file_name
        self.ar_qdk = ARQDK(ip=ar_ip, port=ar_port)
        self.ar_qdk.make_connection()
        self.workbook = self.create_workbook()
        self.worksheet = self.create_worksheet()
        #super().__init__(file_name, acts_list, column_names)
        self.column_names = ["Категория", "Клиент", "Перевозчик", "Количество \nрейсов",
                    "Общий вес,\nтонн", "Выручка, руб.", "Ошибки"]
        self.header_format = self.workbook.add_format({'bold': True,
                                                  'align': 'center',
                                                  'valign': 'center',
                                                  'font_size': 11})
        self.header_format.set_font_size(11)
        self.header_format.set_center_across()

    def create_day_header(self, day=None):
        merge_format = self.workbook.add_format({'align': 'center'})
        merge_format.set_font_size(14)
        self.worksheet.merge_range('A1:G1', day, merge_format)

    def operate_trash_cat(self, trash_cat, day, start_row):
        #records = self.get_records(trash_cat, day)
        records = self.ar_qdk.execute_method("get_daily_report",
                                             trash_cat=trash_cat,
                                             day=day,
                                             get_response=True)
        if records['status']:
            records = records['info']
        if not records:
            return
        self.worksheet.write(start_row, 0, trash_cat, self.header_format)
        for rec in records:
            self.set_record(rec['client_name'], rec['carrier_name'], rec['amount'], rec['tonnage'], start_row)
            start_row += 1
        amount, tonnage = self.get_amount(records)
        return self.set_amount(amount, tonnage, start_row+1)


    def get_amount(self, records):
        amount = 0
        tonnage = 0
        for rec in records:
            amount += rec['amount']
            tonnage += rec['tonnage']
        return amount, tonnage


    def set_record(self, client, carrier, amount, tonnage, start_row):
        self.worksheet.write(start_row, 1, client)
        self.worksheet.write(start_row, 2, carrier)
        self.worksheet.write(start_row, 3, amount)
        self.worksheet.write(start_row, 4, tonnage)
        return

    @wsqluse.getTableDictStripper
    def get_records(self, trash_cat, day):
        return self.sql_shell.get_table_dict(
            "select c.name as client_name, cr.name as carrier_name, "
            "sum(r.cargo) as tonnage, count(r.id) as amount "
            "from records r left join clients c on (r.client_id=c.id) "
            "left join clients cr on (r.carrier=cr.id) "
            f"where r.trash_cat=(select id from trash_cats where name='{trash_cat}') "
            f"and time_in::date='{day}' group by (c.name, cr.name);"
        )

    def set_amount(self, amount, tonnage, row=2):
        self.worksheet.write(row, 0, "ИТОГО", self.header_format)
        self.worksheet.write(row, 3, amount, self.header_format)
        self.worksheet.write(row, 4, tonnage, self.header_format)
        return row

    def set_trash_cat(self, cat_name, row):
        self.worksheet.write(row, 0, cat_name, self.header_format)

    def create_document(self, day=None):
        if not day:
            day = datetime.datetime.now()
        self.create_day_header(day.strftime("%#d/%m/%Y"))
        self.set_column_width()
        start_row = self.set_column_names()
        start_row += 1
        for tc in ["ТКО", "ПО", "Хвосты"]:
            start_row = self.operate_trash_cat(tc, day.strftime("%Y.%m.%d"), start_row=start_row)
            if start_row:
                start_row += 2
        self.workbook.close()

    def set_column_names(self):
        col_num = 0
        self.worksheet.set_row_pixels(1, 42)
        for col_name in self.column_names:
            self.worksheet.write(1, col_num, col_name, self.header_format)
            col_num += 1
        return 1

    def set_column_width(self):
        self.worksheet.set_column_pixels(0, 0, 109)
        self.worksheet.set_column_pixels(1, 1, 198)
        self.worksheet.set_column_pixels(2, 2, 169)
        self.worksheet.set_column_pixels(3, 3, 78)
        self.worksheet.set_column_pixels(4, 4, 101)
        self.worksheet.set_column_pixels(5, 5, 99)
        self.worksheet.set_column_pixels(6, 6, 156)
