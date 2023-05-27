import smtplib

from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.image import MIMEImage



from_addr="pythonfabhost2021@gmail.com"
SMTP_PASSWORD = 'frqrvtpbohkqfoxk'
to_addr="pythonfabhost2022@gmail.com"

msg = MIMEMultipart('alternative')
msg['Subject'] = "Your attendence barcode"
# msg['From'] = from_addr
# msg['To'] = to_addr

text = MIMEText('<img src="cid:image1">', 'html')
msg.attach(text)

image = MIMEImage(open('284029201780.345.png', 'rb').read())

# Define the image's ID as referenced in the HTML body above
image.add_header('Content-ID', '<image1>')
msg.attach(image)

# s = smtplib.SMTP('localhost')
# s = smtplib.SMTP('smtp.gmail.com', 587)
server = smtplib.SMTP('smtp.gmail.com', 25)
server.connect("smtp.gmail.com",587)
server.ehlo()
server.starttls()
server.login(from_addr, SMTP_PASSWORD)
server.sendmail(from_addr, to_addr, msg.as_string())
server.quit()