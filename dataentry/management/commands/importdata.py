from django.core.management.base import BaseCommand, CommandError
from dataentry.models import Student
from django.apps import apps
import csv

#Proposed Command - python manage.py importdata file_path model_name
class Command(BaseCommand):
    help = 'Import data from CSV file'

    def add_arguments(self, parser):
        parser.add_argument('file_path',type=str,help="Path to the CSV file")
        parser.add_argument('model_name',type=str, help="Name of the model")

    def handle(self, *args, **kwargs):
        #logic goes here
        file_path = kwargs['file_path']
        model_name = kwargs['model_name'].capitalize()
        model = None
        # search for the model across all installed apps
        for app_config in apps.get_app_configs():
            # Try to search for the model
            try:
                model = apps.get_model(app_label=app_config.label,model_name=model_name)
                break #stop searching
            except LookupError:
                continue #model not found this app, continue searching in next app
        if not model:
            raise CommandError(f"Model {model_name} not found in any app")
        
        with open(file_path, 'r') as file:
            reader = csv.DictReader(file)
            for row in reader:
                roll_no = row['roll_no']
                existing_record = model.objects.filter(roll_no=roll_no).exists()

                if not existing_record:
                    model.objects.create(**row)
                else:
                    self.stdout.write(self.style.WARNING(f"Student with roll no {roll_no} already exist!"))
            
        self.stdout.write(self.style.SUCCESS('Data inserted sucessfully!'))
