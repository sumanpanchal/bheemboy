from django.core.management.base import BaseCommand, CommandError
from coursereg.models import Faq
import json

class Command(BaseCommand):
    help = 'Load FAQs to the database from a JSON file. If an identical question is already in the database, it is left untouched.'

    def add_arguments(self, parser):
        parser.add_argument('--datafile',
            default='coursereg/data/faqs.json',
            help='File to load data from (default: coursereg/data/faqs.json)')

    def handle(self, *args, **options):
        with open(options['datafile']) as f:
            faqs = json.loads(f.read())
            counter = 0
            for faq in faqs:
                faq_for = int(faq['faq_for'])
                question = str(faq['question'])
                answer = str(faq['answer'])
                if not Faq.objects.filter(question=question, faq_for=faq_for):
                    Faq.objects.create(faq_for=faq_for, question=question, answer=answer)
                    counter += 1
            self.stdout.write(self.style.SUCCESS(
                'Successfully added %s FAQs to the databse.' % (counter, )
            ))                                                                                
