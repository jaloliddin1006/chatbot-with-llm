from django.core.management.base import BaseCommand
from service.chat import chatbot  

class Command(BaseCommand):
    help = 'Chatbot bilan muloqot qilish'

    def add_arguments(self, parser):
        parser.add_argument('question', type=str, help='Chatbotga yuboriladigan savol')

    def handle(self, *args, **options):
        question = options['question']
        response= chatbot.get_response(question)
        self.stdout.write(self.style.SUCCESS(f"Chatbot javobi: {response}"))
        while True:
            user_input = input("User: ")
            if user_input == "exit":
                break
            
            response= chatbot.get_response(user_input)
            
            self.stdout.write(self.style.SUCCESS(f"Chatbot: {response}"))
            
