from os import close

from flask import Flask, url_for, render_template, request, session, redirect, make_response
import pymysql
import time

from inject import Inject

class Order:    #класс заявок

    def __init__(self, id, shop_id, date=[], shop='', target='Пустая', status_out='new', status_in='new', photo = [], estimate = [], material = [], works = [], comments = [], color = '', shop_adress = ''):
        self.id = id
        self.date = date if date else [time.time(), 0, 0]
        self.shop = shop  #название магазина
        self.shop_id = shop_id   #номер магазина
        self.shop_adress = shop_adress #адрес магазина
        self.target = target    #Цель заявки
        self.status_out = status_out #статус keepUp
        self.status_in = status_in #статус Эллипс
        self.photo = photo #фотографии заявок
        self.estimate = estimate  #смета
        self.material = material  #материалы
        self.works = works #техники
        self.comments = comments  #комментарии
        self.color = color  #цвет заявки

    def change_shop(self, shop_id):
        self.shop_id = shop_id
        return self

    def change_status(self, status_out, status_in):
        self.status_out = status_out  # статус keepUp
        self.status_in = status_in  # статус Эллипс
        return self

DATABASE = 'VH39.spaceweb.ru'

try:
    connection = pymysql.connect(
        host=DATABASE,
        port=3306,
        user='dasmirf_ellipse',
        password='Acc13215',
        database='dasmirf_ellipse',
        cursorclass=pymysql.cursors.DictCursor
    )
    print("successfully connected...")
    print("#" * 20)

    try:
        pass

    finally:
        connection.close()

except Exception as ex:
    print("Base don't connected...")
    print(ex)
    print("#" * 20)


app = Flask(__name__)
app.secret_key = "abc"

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.args.get('shop_id'):
        filter_shop = request.args.get('shop_id')
    else:
        filter_shop = False
    try:
        connection = pymysql.connect(
            host=DATABASE,
            port=3306,
            user='dasmirf_ellipse',
            password='Acc13215',
            database='dasmirf_ellipse',
            cursorclass=pymysql.cursors.DictCursor
        )
        print("successfully connected...")
        print("#" * 20)

        try:
            with connection.cursor() as cursor:
                cursor.execute('''SELECT * FROM orders''')
                bufer = cursor.fetchall()

        except Exception as ex:
            print("Base don't connected...")
            print(ex)
            print("#" * 20)

        try:
            with connection.cursor() as cursor:
                cursor.execute('''SELECT * FROM shops''')
                bufer_shops = cursor.fetchall()

        except Exception as ex:
            print("Base don't connected...")
            print(ex)
            print("#" * 20)

    finally:
        connection.close()

    order_card = []
    for id in bufer:
        if filter_shop and filter_shop != 'all':
            if str(filter_shop) != str(id['shop_id']):
                continue
        order_card.append(Order(id=id['id'], shop_id=id['shop_id'], shop=id['shop'], target=id['target'], status_in=id['status_in'], status_out=id['status_out'], color=id['color'], shop_adress=id['shop_adress']))
        print(id)

    return render_template('index.html', title='Home', bufer=order_card, len=len(order_card), filter_shop=filter_shop, bufer_shops=bufer_shops)

@app.route('/add_order', methods=['GET', 'POST'])
def make_order():
    try:
        connection = pymysql.connect(
            host=DATABASE,
            port=3306,
            user='dasmirf_ellipse',
            password='Acc13215',
            database='dasmirf_ellipse',
            cursorclass=pymysql.cursors.DictCursor
        )
        print("successfully connected...")
        print("#" * 20)

        try:
            with connection.cursor() as cursor:
                cursor.execute('''SELECT * FROM shops''')
                bufer = cursor.fetchall()

        except Exception as ex:
            print("Base don't connected...")
            print(ex)
            print("#" * 20)

    finally:
        connection.close()

    dict_shop = []
    for i in bufer:
        dict_shop.append(i['shop_id'])

    if request.method == 'POST':
        id = request.form.get('id')
        shop_id = request.form.get('shop_id')
        target = request.form.get('target')

        try:
            connection = pymysql.connect(
                host=DATABASE,
                port=3306,
                user='dasmirf_ellipse',
                password='Acc13215',
                database='dasmirf_ellipse',
                cursorclass=pymysql.cursors.DictCursor
            )
            print("successfully connected...")
            print("#" * 20)

            try:
                shop, shop_adress = 'noname', 'noadress'
                for j in bufer:
                    if str(j['shop_id']) == str(shop_id):
                        shop, shop_adress = j['shop_name'], j['shop_adress']
                        break
                with connection.cursor() as cursor:
                    insert = '''INSERT INTO orders (id, shop_id, shop, shop_adress, target) VALUES ('{}', '{}', '{}', '{}', '{}');'''.format(id, shop_id, shop, shop_adress, target)
                    cursor.execute(insert)
                    connection.commit()

            except Exception as ex:
                return ex

            finally:
                connection.close()
                return redirect(f'/edit_order/{id}')

        except Exception as ex:
            print("Base don't connected...")
            print(ex)
            print("#" * 20)

    return render_template('add_order.html', title='MakeOrder', dict_shop=dict_shop)

@app.route('/add_shop', methods=['GET', 'POST'])
def add_shop():
    if request.method == 'POST':
        shop_id = request.form.get('shop_id')
        shop_name = request.form.get('shop_name')
        shop_adress = request.form.get('shop_adress')
        shop_direct = request.form.get('shop_direct')
        shop_engeener = request.form.get('shop_engeener')
        shop_secure = request.form.get('shop_secure')
        direct_phone = request.form.get('direct_phone')
        engeener_phone = request.form.get('engeener_phone')
        secure_phone = request.form.get('secure_phone')

        try:
            connection = pymysql.connect(
                host=DATABASE,
                port=3306,
                user='dasmirf_ellipse',
                password='Acc13215',
                database='dasmirf_ellipse',
                cursorclass=pymysql.cursors.DictCursor
            )
            print("successfully connected...")
            print("#" * 20)

            try:
                with connection.cursor() as cursor:
                    insert = '''INSERT INTO shops (shop_id, shop_name, shop_adress, shop_direct, shop_engeener, shop_secure, direct_phone, engeener_phone, secure_phone) VALUES ('{}', '{}', '{}', '{}', '{}', '{}', '{}', '{}', '{}');'''.format(shop_id, shop_name, shop_adress, shop_direct, shop_engeener, shop_secure, direct_phone, engeener_phone, secure_phone)
                    cursor.execute(insert)
                    connection.commit()

            except Exception as ex:
                return ex

            finally:
                connection.close()
                return redirect(url_for('index'))

        except Exception as ex:
            print("Base don't connected...")
            print(ex)
            print("#" * 20)

    return render_template('add_shop.html', title='AddShop')


@app.route('/edit_order/<id>', methods=['GET', 'POST'])
def edit_order(id):
    print(time.time())
    if request.method == 'POST':

        print('прием данных')
        status_out = request.form.get('status_out')
        status_in = request.form.get('status_in')
        material = request.form.get('material')
        comments = request.form.get('comments')
        target = request.form.get('target')
        if status_in == 'Выполнена':
            color = '0, 255, 0, 0.3'
        elif status_in == 'На согласовании':
            color = '0, 255, 255, 0.3'
        elif status_in == 'Не отработана':
            color = '255, 0, 0, 0.3'
        elif status_in == 'Отклонена':
            color = '255, 255, 255, 0.3'
        elif status_in == 'Подписать акт':
            color = '255, 255, 100, 0.6'
        elif status_in == 'Согласовано':
            color = '255, 255, 0, 0.3'
        else:
            color = '0, 0, 0, 0.3'

        print(id, status_out, status_in, material, comments, target)

        try:
            connection = pymysql.connect(
                host=DATABASE,
                port=3306,
                user='dasmirf_ellipse',
                password='Acc13215',
                database='dasmirf_ellipse',
                cursorclass=pymysql.cursors.DictCursor
            )
            print("successfully connected...")
            print("#" * 20)

            try:
                with connection.cursor() as cursor:
                    update = '''UPDATE orders SET status_out=%s, status_in=%s, material=%s, comments=%s, target=%s, color=%s WHERE id = %s'''
                    data = [status_out, status_in, material, comments, target, color, id]
                    cursor.execute(update, data)
                    connection.commit()

            except Exception as ex:
                return ex

            finally:
                connection.close()
                return redirect(url_for('index'))

        except Exception as ex:
            print("Base don't connected...")
            print(ex)
            print("#" * 20)

    try:
        connection = pymysql.connect(
            host=DATABASE,
            port=3306,
            user='dasmirf_ellipse',
            password='Acc13215',
            database='dasmirf_ellipse',
            cursorclass=pymysql.cursors.DictCursor
        )
        print("successfully connected...")
        print("#" * 20)

        try:
            with connection.cursor() as cursor:
                cursor.execute('''SELECT * FROM orders WHERE id = ('{}')'''.format(id))
                bufer = cursor.fetchall()

        except Exception as ex:
            print("Base don't connected...")
            print(ex)
            print("#" * 20)

    except Exception as ex:
        print("Base don't connected...")
        print(ex)
        print("#" * 20)

    finally:
        connection.close()

    return render_template('edit_order.html', title='EditOrder', bufer=bufer)

@app.route('/edit_shop/<shop_id>', methods=['GET', 'POST'])
def edit_shop(shop_id):
    if request.method == 'POST':
        print('прием данных')
        shop_name = request.form.get('shop_name')
        shop_adress = request.form.get('shop_adress')
        shop_direct = request.form.get('shop_direct')
        shop_engeener = request.form.get('shop_engeener')
        shop_secure = request.form.get('shop_secure')
        direct_phone = request.form.get('direct_phone')
        engeener_phone = request.form.get('engeener_phone')
        secure_phone = request.form.get('secure_phone')

        try:
            connection = pymysql.connect(
                host=DATABASE,
                port=3306,
                user='dasmirf_ellipse',
                password='Acc13215',
                database='dasmirf_ellipse',
                cursorclass=pymysql.cursors.DictCursor
            )
            print("successfully connected...")
            print("#" * 20)

            try:
                with connection.cursor() as cursor:
                    update = '''UPDATE shops SET shop_name=%s, shop_adress=%s, shop_direct=%s, shop_engeener=%s, shop_secure=%s, direct_phone=%s, engeener_phone=%s, secure_phone=%s WHERE shop_id = %s'''
                    data = [shop_name, shop_adress, shop_direct, shop_engeener, shop_secure, direct_phone, engeener_phone, secure_phone, shop_id]
                    cursor.execute(update, data)
                    connection.commit()

            except Exception as ex:
                return ex

            finally:
                connection.close()
                return redirect(url_for('index'))

        except Exception as ex:
            print("Base don't connected...")
            print(ex)
            print("#" * 20)

    try:
        connection = pymysql.connect(
            host=DATABASE,
            port=3306,
            user='dasmirf_ellipse',
            password='Acc13215',
            database='dasmirf_ellipse',
            cursorclass=pymysql.cursors.DictCursor
        )
        print("successfully connected...")
        print("#" * 20)

        try:
            with connection.cursor() as cursor:
                cursor.execute('''SELECT * FROM shops WHERE shop_id = ('{}')'''.format(shop_id))
                bufer = cursor.fetchall()

        except Exception as ex:
            print("Base don't connected...")
            print(ex)
            print("#" * 20)

    except Exception as ex:
        print("Base don't connected...")
        print(ex)
        print("#" * 20)

    finally:
        connection.close()
    print(bufer)
    return render_template('edit_shop.html', title='EditShop', bufer=bufer)

@app.route('/inject', methods=['GET', 'POST'])
def inject():
    data = Inject('static/import_orders.csv')
    try:
        data.inject_csv()
        bufer = []
        shops = [{}, {}]

        try:
            connection = pymysql.connect(
                host=DATABASE,
                port=3306,
                user='dasmirf_ellipse',
                password='Acc13215',
                database='dasmirf_ellipse',
                cursorclass=pymysql.cursors.DictCursor
            )
            print("successfully connected...")
            print("#" * 20)

            try:
                with connection.cursor() as cursor:
                    cursor.execute('''SELECT * FROM shops''')
                    bufer_shops = cursor.fetchall()

            except Exception as ex:
                print("Base don't connected...")
                print(ex)
                print("#" * 20)

        except Exception as ex:
            print("Base don't connected...")
            print(ex)
            print("#" * 20)

        finally:
            connection.close()

        for i in bufer_shops:
            shops[0][str(i['shop_id'])] = str(i['shop_name'])
            shops[1][str(i['shop_id'])] = str(i['shop_adress'])
        for j in data.data:
            if j[0] in shops[0]:
                j.append(shops[0][j[0]])
                j.append(shops[1][j[0]])
                j[1] = j[1].replace('/', '-')
                print(j)
                bufer.append(j)

        if request.args.get('accept'):
            try:
                connection = pymysql.connect(
                    host=DATABASE,
                    port=3306,
                    user='dasmirf_ellipse',
                    password='Acc13215',
                    database='dasmirf_ellipse',
                    cursorclass=pymysql.cursors.DictCursor
                )
                print("successfully connected...")
                print("#" * 20)

                for k in bufer:
                    time.sleep(0.2)
                    try:
                        with connection.cursor() as cursor:
                            print('Попытка импортировать:', k)
                            insert = '''INSERT INTO orders (id, shop_id, shop, shop_adress, target, status_out, date) VALUES ('{}', '{}', '{}', '{}', '{}', '{}', '{}');'''.format(
                                k[1], k[0], k[7], k[8], k[2], k[5], k[3])
                            cursor.execute(insert)
                            connection.commit()
                            print('Импортирована заявка номер', k[1])

                    except Exception as ex:
                        return ex
                        print('Не импортирована заявка', k)


            except Exception as ex:
                print("Base don't connected...")
                print(ex)
                print("#" * 20)

            finally:
                connection.close()
                print('Импорт произведен')

    except:
        print('Файл для импорта не найден')
        bufer = ['Error']

    print(bufer)
    print(len(bufer))
    return render_template('inject.html', title='Import', bufer=bufer)

if __name__ == "__main__":
    app.run(debug='True')