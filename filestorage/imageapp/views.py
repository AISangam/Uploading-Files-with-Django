# libraries are imported
# rendering the template using render
from django.shortcuts import render
# this will be used to get the path of the media folder from settings
from django.conf import settings
# for storing the file in the desired folder, FileSystemStorage is used  
from django.core.files.storage import FileSystemStorage
# this will handle MultiValueDictKeyError using try and except
from django.utils.datastructures import MultiValueDictKeyError
# using class from models.py
from . models import file_storage

# Create your views here.
def file_storage_to_db(request):
	# Media path
	file_path = settings.MEDIA_ROOT
	# if request is post
	if request.method == 'POST':
	# handling MultiValueDictKeyError	
		try:
			myFile = request.FILES['myFile']
		except MultiValueDictKeyError:
			print("Error.......")
			myFile = "None"
		# creating the object to store the file
		fs = FileSystemStorage(location=file_path)	
		# saving the file in the media folder
		filename = fs.save(myFile.name, myFile)
		# getting the url of the file being saved
		file_url = fs.url(filename)
		# Creating the instance of database
		file_information = file_storage()
		file_information.file_name = myFile.name
		file_information.file_url = file_url 
		# All the information is saved in the database
		file_information.save()
		
		# One can also display the infomation to the user in the frontend
		context = {
					'filename': myFile.name, 
					'file_url': file_url
				  }

		return render(request, 'information_display.html', {'context': context})
	else:
		return render(request, 'upload_file.html')		
