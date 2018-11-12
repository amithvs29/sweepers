import pandas
import logging
import datetime
from common import safe_path


class sweeper(object):
    def __init__(self, swpr, db, em):
        self.swpr = swpr
        self.db = db
        self.em = em
        self.em.new_email()
        now = datetime.datetime.now()
        self.output_filename = 'logs/' + now.strftime("%Y%m%d") + '/' + self.swpr['name'] + '_' + now.strftime("%Y%m%d%H%M") + '.xlsx'
        safe_path(self.output_filename)
        logging.info('Initiated sweeper: ' + self.swpr['name'])

    def get_args(self):
        self.results = []
        query_list = eval(self.swpr['query'])
        for q in query_list:
            self.db.use_db(q[0])
            self.results.append(self.db.execute(q[1]))
        self.args = [len(l.index) for l in self.results]

    def run(self):
        self.get_args()
        writer = pandas.ExcelWriter(self.output_filename, engine='xlsxwriter')
        workbook = writer.book
        for index, df in enumerate(self.results):
            sheet_name = 'Query' + str(index + 1)
            worksheet = workbook.add_worksheet(sheet_name)
            writer.sheets[sheet_name] = worksheet
            df.to_excel(writer, sheet_name=sheet_name, index=False)
        writer.save()
        if sum(self.args) != 0:
            self.em.attach_file(self.output_filename)
        if sum(self.args) or (not eval(self.swpr.get('email_only_when_result', 'False'))):
            self.em.set_recipients(eval(self.swpr['toaddr']))
            em_body = self.swpr['email_body'].format(*self.args)
            em_body += '\n\nThis is an automated email. Please contact techops-scoring@collegeboard.org with any questions.'
            self.em.set_email_content(self.swpr['email_subject'], em_body)
            self.em.send()
        else:
            logging.info('Not sending mail for sweeper ' + self.swpr['name'] + ' as no result was obtained')
        logging.info('Completed running sweeper: ' + self.swpr['name'])
