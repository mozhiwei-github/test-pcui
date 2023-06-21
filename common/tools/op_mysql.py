import pymysql

class mysql(object):
    def op_mysql(self):
        conn = pymysql.connect(host="10.46.27.141", port=61197, user="pcwallpaper_pro", password="uquiw3e6tqqn2mkggaz0o07kg7hzqo2", database="pcwallpaper_k8s_test",
                               charset="utf8")
        cur = conn.cursor()
        sql = 'select id, likes, (download_add+download_real) as download_count from wallpaper_live where id in(341234)'
        cur.execute(sql)
        res = cur.fetchone()
        print(res)
        cur.close()
        conn.close()


if __name__ == '__main__':
    op = mysql()
    op.op_mysql()