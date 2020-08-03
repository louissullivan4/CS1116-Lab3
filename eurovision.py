#!/usr/local/bin/python3

from cgitb import enable
enable()

import pymysql as db

from cgi import FieldStorage

from html import escape

print('Content-Type: text/html')
print()

form_data = FieldStorage()
result = ''
countries = ''
menu_choice = ''
if len(form_data) != 0:
    try:
        connection = db.connect('cs1.ucc.ie', 'ls9', 'raeti', 'cs6503_cs1106_ls9')
        cursor = connection.cursor(db.cursors.DictCursor)
        cursor.execute("""SELECT DISTINCT country FROM winners""")
        menu_choice = """<select name="countries">"""
        for row in cursor.fetchall():
            menu_choice += '<option>%s</options>' % (row['country'])
        menu_choice += '</select>'
        cursor.close()
        connection.close()
        countries = escape(form_data.getfirst('countries', '').strip())
        connection = db.connect('cs1.ucc.ie', 'ls9', 'raeti', 'cs6503_cs1106_ls9')
        cursor = connection.cursor(db.cursors.DictCursor)
        cursor.execute("""SELECT year, song, performer, points FROM winners
                          WHERE country = %s""", (countries))
        result = """<table>
                    <tr><th colspan="2">Eurovision Winners from %s</th></tr>
                    <tr><th>Year</th><th>Song</th><th>Performer</th><th>Points</th></tr>""" % (countries)
        if cursor.rowcount == 0:
            result = '<p>Sorry! Please try again with a valid country.</p>'
        for row in cursor.fetchall():
            result += '<tr><td>%s</td><td>%s</td><td>%s</td><td>%s</td></tr>' % (
                row['year'], row['song'], row['performer'], row['points'])
        result += '</table>'
        cursor.close()
        connection.close()
    except db.Error:
        result = '<p>Sorry! We are experiencing problems at the moment. Please call back later.</p>'
print("""
    <!DOCTYPE html>
    <html lang="en">
        <head>
            <meta charset="utf-8" />
            <title>Eurovision Winners</title>
            <link rel="stylesheet" href="styles.css">
        </head>
        <body>
           <form action="eurovision.py" method="post">
                <label for="country">Countries: </label>
                    %s
                <input type="submit" value="Submit Query" />
            </form>
            %s
        </body>
    </html>""" % (menu_choice, result))
