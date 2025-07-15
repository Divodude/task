# management/commands/create_blog_categories.py
from django.core.management.base import BaseCommand
from accounts.models import BlogCategory

class Command(BaseCommand):
    help = 'Create default blog categories'
    
    def handle(self, *args, **options):
        categories = [
            {
                'name': 'Mental Health',
                'description': 'Articles about mental health, wellness, and psychological well-being.'
            },
            {
                'name': 'Heart Disease',
                'description': 'Information about cardiovascular health, heart disease prevention, and treatment.'
            },
            {
                'name': 'Covid19',
                'description': 'Updates and information about COVID-19, prevention, and recovery.'
            },
            {
                'name': 'Immunization',
                'description': 'Articles about vaccines, immunization schedules, and vaccine safety.'
            }
        ]
        
        for category_data in categories:
            category, created = BlogCategory.objects.get_or_create(
                name=category_data['name'],
                defaults={'description': category_data['description']}
            )
            
            if created:
                self.stdout.write(
                    self.style.SUCCESS(f'Successfully created category: {category.name}')
                )
            else:
                self.stdout.write(
                    self.style.WARNING(f'Category already exists: {category.name}')
                )
        
        self.stdout.write(
            self.style.SUCCESS('Blog categories setup completed!')
        )