from django.core.management.base import BaseCommand
from service.chat import chatbot  # Chatbot obyektini import qilamiz

class Command(BaseCommand):
    help = 'Chatbot bilan muloqot qilish'

    def add_arguments(self, parser):
        parser.add_argument('question', type=str, help='Chatbotga yuboriladigan savol')

    def handle(self, *args, **options):
        question = options['question']
        response= chatbot.get_response(question)
        self.stdout.write(self.style.SUCCESS(f"Chatbot javobi: {response}"))
