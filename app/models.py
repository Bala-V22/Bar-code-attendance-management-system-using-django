from django.db import models
from datetime import datetime
import os


class staff(models.Model):
	id = models.CharField(primary_key=True, max_length=10)
	name = models.CharField(max_length=50)
	email = models.CharField(max_length=50)

	def __str__(self):
		return self.name

class studends(models.Model):
	id = models.CharField(primary_key=True, max_length=10)
	name = models.CharField(max_length=50)
	email = models.CharField(max_length=50)


	def __str__(self):
		return self.name

	def num_photos(self):
		try:
			DIR = f"bag/{self.name}_{self.id}"
			img_count = len(os.listdir(DIR))
			return img_count
		except:
			return 0 

from datetime import date
class Detected(models.Model):
	emp_id = models.ForeignKey(studends, on_delete=models.CASCADE, null=True)
	time_stamp = models.DateTimeField(default=date.today)
	photo = models.ImageField(upload_to='detected/', default='app/facerec/detected/noimg.png')

	def __str__(self):
		emp = studends.objects.get(name=self.emp_id)
		return f"{emp.name} {self.time_stamp}"

