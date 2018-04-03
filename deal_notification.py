from glob import glob
from os import environ
import psycopg2
from psycopg2.extras import NamedTupleCursor
import smtplib
from email.MIMEMultipart import MIMEMultipart
from email.MIMEText import MIMEText

class DealNotification(object):

    def __init__(self):
        self._config_files = []
        self._sql = self._get_notification_query_sql()
        self._db_cxn = self._get_database_connection()

        self._get_config_files()

    def _get_database_connection(self):
        connection_string = "dbname='{}' user='{}' host='{}' password='{}'".format(environ['DB_NAME'],
                                                                                   environ['DB_USER'],
                                                                                   environ['DB_HOST'],
                                                                                   environ['DB_PASS'])
        print connection_string
        conn = psycopg2.connect(connection_string, cursor_factory=NamedTupleCursor)
        conn.autocommit = True
        cur = conn.cursor()
        return cur

    def _get_config_files(self):
        self._config_files = glob('notification_configs/*.config')

    def _get_notification_query_sql(self):
        sql = open('sql/query_for_deal.sql', 'r').read()

        return sql

    def _parse_config_file(self, config_file):
        email = None
        deals = []
        configs = open(config_file, 'r').readlines()
        for config_line in configs:
            config_line = config_line.strip('\n')
            if not email:
                email = config_line.split("=")[1]
            else:
                deals.append(config_line)

        return dict(email=email, deals=deals)

    def _query_notification(self, keyword_array):
        deal_title, query_params = keyword_array.split('|')
        query_params = query_params.split(',')
        queries = []
        for query in query_params:
            keywords = query.split('&')
            keywords_and = []
            for word in keywords:
                keywords_and.append(" LOWER(item) LIKE '%%{}%%' ".format(word))
            queries.append(' AND '.join(keywords_and))

        query_params_sql = ' OR '.join(queries)
        query_params_sql = ' AND {} '.format(query_params_sql)
        sql = self._sql.format(ITEM_DETAILS=query_params_sql)

        self._db_cxn.execute(sql)
        deals = []
        if self._db_cxn.rowcount > 0:
            rows = self._db_cxn.fetchall()
            for deal in rows:
                deals.append(' {}   {}   {}   {}   {}'.format(deal.start_dt, deal.source, deal.item, deal.value, deal.details))

        if deals:
            deal_text = '{}\n'.format(deal_title)
            deal_text += '\n'.join(deals)
            deal_text += '\n\n'
        else:
            deal_text = None

        return deal_text

    def send_notification_email(self, email_address, notification_text):
        fromaddr = "juliedonald@gmail.com   "
        toaddr = "jheckman324@gmail.com"
        msg = MIMEMultipart()
        msg['From'] = fromaddr
        msg['To'] = toaddr
        msg['Subject'] = "Deal Alert!"

        body = notification_text
        msg.attach(MIMEText(body, 'plain'))

        server = smtplib.SMTP('smtp.gmail.com', 587)
        server.starttls()
        server.login(fromaddr, "bhszycylneziuszr")
        text = msg.as_string()
        server.sendmail(fromaddr, toaddr, text)
        server.quit()

    def run_notifications(self):
        for config_file in self._config_files:
            results = self._parse_config_file(config_file)

            notifications = []
            for deal in results['deals']:
                query_results = self._query_notification(deal)
                if query_results:
                    notifications.append(query_results)

            if notifications:
                self.send_notification_email(results['email'], '\n'.join(notifications))


if __name__ == '__main__':
    p =DealNotification()
    p.run_notifications()