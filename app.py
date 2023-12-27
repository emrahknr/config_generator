from flask import Flask,render_template,request
from config_generator_upe1 import config_generator_from_excel_upe1
from config_generator_upe2 import config_generator_from_excel_upe2
import os
from werkzeug.utils import secure_filename
from send_mail import HTMLmail



app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = "/"



@app.route("/", methods=["GET","POST"])
def index():

    if request.method == "GET":
        if os.path.isfile('/var/www/html/ne80_config_generator/templates.csv'):
            os.remove('/var/www/html/ne80_config_generator/templates.csv')

        if os.listdir('/var/www/html/ne80_config_generator/konfigs/'):
            for file in os.listdir('/var/www/html/ne80_config_generator/konfigs/'):
                os.remove("/var/www/html/ne80_config_generator/konfigs/"+file)

    if request.method == "POST":
        f = request.files['file']
        #f = request.form.get('file')
        dosya = f.filename
        if f:
            #f.filename = 'templates.csv'
            #f.save(secure_filename(f.filename))
            f.save(os.path.join("/var/www/html/ne80_config_generator/", 'templates.csv'))
            return render_template("index.html", dosya=dosya + " Basariyla Yuklendi. Konfigurasyonlari Olusturup Mail Atabilirsiniz.")
        else:
            return render_template("index.html", hata="Dosya Yukleme Basarisiz.Tekrar deneyin.")

    return render_template("index.html")

@app.route('/upe1')
def upe1():

    konfig1 = config_generator_from_excel_upe1("/var/www/html/ne80_config_generator/templates.csv")
    return render_template("upe1.html", konfig1=konfig1)


@app.route('/upe2')
def upe2():

    konfig2 = config_generator_from_excel_upe2("/var/www/html/ne80_config_generator/templates.csv")
    return render_template("upe2.html", konfig2=konfig2)

@app.route('/send_mail',methods = ["GET","POST"])
def send_mail():

    if request.method == "POST":

        if request.form.get("e-mail"):

            eFRM = "ConfigGenerator@smtp.turkcell.com.tr"
            eCC = 'emrah.konur@turkcell.com.tr'
            eTO = request.form.get("e-mail")
            eSBJ = "NE80 Konfigurasyon"
            bodyf = "/var/www/html/ne80_config_generator/mbody.txt"
            takipFile = "/var/www/html/ne80_config_generator/konfigs/"

            HTMLmail(eFRM, eTO, eCC, eSBJ, bodyf, takipFile)

        else:
            comment = "e-mail bos olamaz!!"
            return render_template("send_mail.html", comment=comment)

    return render_template("send_mail.html")



if __name__ == "__main__":
    app.run(debug=False)
