import scrapy
import difflib
import smtplib
from email.MIMEMultipart import MIMEMultipart
from email.MIMEText import MIMEText

#add_from,add_to actual emails changed
add_from = "abc@gmail.com" 
add_to = "def@gmail.com","def2@gmail.com"
add_cc = ""
msg = MIMEMultipart()
msg['From'] = add_from
msg['To'] = add_to
msg['Cc'] = add_cc
msg['Subject'] = "New Website\s with Datasets"
global body 
body = "The new websites containing medical image datasets have been discovered:-\n"

class DmozSpider(scrapy.Spider):
	name = "GC"
	with open('starturl.txt') as f:
		start_urls = f.read().splitlines()
	
	def parse(self, response):
		if "grand-challenge.org" in response.url:
			get = response.xpath("//div[starts-with(@class, 'projectlink open datadownload')]")
			urls = get.xpath("./div[@class='top']/a/@href").extract()
			des = get.xpath(".//div[@class='description']/text()").extract()
			new_urls = response.xpath("//a[contains(., 'Data download')]/@href").extract()
			file_old = 'grandchallenge.txt'
			
			k = zip(urls, des)
			l = list(k)
			f = open('file.txt', 'w')
			with open(file_old) as f:
				old_urls = f.read().splitlines()

			if len(old_urls) == len(new_urls):
				print "No new websites discovered"

			else:
				diff_list = list(set(new_urls) -set(old_urls))		
				diff_str = "\n".join(str(x) for x in diff_list)		
				with open(file_old, 'wb') as f:
					f.writelines(["%s\n" % item  for item in new_urls])
				
				body1 = body + diff_str				
				msg.attach(MIMEText(body1, 'plain'))	
				server = smtplib.SMTP("students.iiit.ac.in", 25)
				server.starttls()
				server.login(add_from, "password") #actual password changed
				text = msg.as_string()
				add_recv = add_cc.split(",") + add_to.split(",")
				server.sendmail(add_from,add_recv,text)
				server.quit()   

		if "http://www.imageclef.org/2016/medical" in response.url:

			list_of_testsets = response.xpath("//ul/li/b[contains(.,'test set')]").extract()
			file_old = 'testsets_2016_medical.txt'
			
			with open(file_old) as f:
				list_of_testsets_old = f.read().splitlines()


			if len(list_of_testsets_old) == len(list_of_testsets):
				print "No Updates"

			else:
				diff_list = list(set(new_urls) -set(old_urls))		
				diff_str = "\n".join(str(x) for x in diff_list)	
				with open(file_old,'a') as f:
					f.write(diff_str)
				
				body2 = body + diff_str				
				msg.attach(MIMEText(body2, 'plain'))
				server = smtplib.SMTP("gmail.com", 25)
				server.starttls()
				server.login(add_from, "password") #actual password removed
				text = msg.as_string()
				add_recv = add_cc.split(",") + add_to.split(",")
				server.sendmail(add_from,add_recv,text)
				server.quit() 




