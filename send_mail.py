from email.mime.base import MIMEBase
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import email
import os
import smtplib


def HTMLmail(frm, mto, mcc, sobje, mbody, mtxt):

    TOTO = [ ]; COCO = [ ]

    if len(mto) > 0:
       emokatar = mto.split(',')
       for Z1 in emokatar:
           ZZ9 = Z1; TOTO.append(ZZ9)

    if len(mcc) > 0:
       emokatar = mcc.split(',')
       for Z1 in emokatar:
           ZZ9 = Z1; COCO.append(ZZ9)

# Create the root message and fill in the from, to, and subject headers
    msg = MIMEMultipart('alternative')
    msg['Subject'] = sobje
    msg['From'] = frm
    msg['To'] = ', '.join( TOTO )
    msg['Cc'] = ', '.join( COCO )

    text = ""
    html = " <html> <head></head> <body> <p> <pre>"

    fp = open(mbody,'r')
    for i in fp:
        html = html+i
        text = text+i

    fp.close()

    html = html + '</pre> </p> </body> </html>'

    part1 = MIMEText(text, 'plain')
    part2 = MIMEText(html, 'html')

    msg.attach(part1); msg.attach(part2)


    files = []
    for file in os.listdir(mtxt):
        files.append(file)
    for i in files:
        part = MIMEBase('application', "octet-stream")
        part.set_payload(open("/var/www/html/ne80_config_generator/konfigs/"+i,"rb").read())
        email.encoders.encode_base64(part)
        part.add_header('Content-Disposition', 'attachment; filename="%s"' % os.path.basename("/var/www/html/ne80_config_generator/konfigs/"+i))
        msg.attach(part)

    if len(mcc) > 0:
        TOTO = TOTO + COCO

    s = smtplib.SMTP("10.218.130.60")
    s.sendmail(frm, TOTO, msg.as_string())
    s.quit()

    return
