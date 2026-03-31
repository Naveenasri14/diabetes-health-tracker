from django.core.management.base import BaseCommand
from diabetes_tracker.models import DietSuggestion

class Command(BaseCommand):
    help = 'Load sample diet suggestions for Tamil Nadu cuisine'

    def handle(self, *args, **kwargs):
        diet_suggestions = [
            # Breakfast
            {
                'name': 'Ragi Dosa (Finger Millet Dosa)',
                'meal_type': 'breakfast',
                'description': 'Healthy dosa made from ragi flour, perfect for diabetes management',
                'ingredients': 'Ragi flour, rice flour, onion, green chili, curry leaves',
                'preparation_method': 'Mix flours with water, add vegetables, cook on tawa',
                'calories': 150,
                'is_millet_based': True,
                'replaces': 'White rice dosa',
                'tamil_nadu_region': 'All regions'
            },
            {
                'name': 'Kambu Koozh (Pearl Millet Porridge)',
                'meal_type': 'breakfast',
                'description': 'Traditional fermented millet porridge, excellent for blood sugar control',
                'ingredients': 'Kambu (pearl millet), water, salt, buttermilk',
                'preparation_method': 'Soak millet overnight, grind, ferment, serve with onion',
                'calories': 120,
                'is_millet_based': True,
                'replaces': 'Rice-based breakfast',
                'tamil_nadu_region': 'Kongu region'
            },
            # Lunch
            {
                'name': 'Samai Rice (Little Millet) with Sambar',
                'meal_type': 'lunch',
                'description': 'Little millet served with vegetable sambar - a perfect diabetic-friendly meal',
                'ingredients': 'Samai (little millet), toor dal, mixed vegetables, tamarind',
                'preparation_method': 'Cook millet like rice, prepare sambar with vegetables',
                'calories': 350,
                'is_millet_based': True,
                'replaces': 'White rice with sambar',
                'tamil_nadu_region': 'All regions'
            },
            {
                'name': 'Kezhvaragu (Ragi) Mudde with Kuzhambu',
                'meal_type': 'lunch',
                'description': 'Traditional ragi balls served with spicy vegetable curry',
                'ingredients': 'Ragi flour, water, vegetables for kuzhambu',
                'preparation_method': 'Boil water, add ragi flour, stir until firm, shape into balls',
                'calories': 380,
                'is_millet_based': True,
                'replaces': 'White rice',
                'tamil_nadu_region': 'Rural Tamil Nadu'
            },
            # Dinner
            {
                'name': 'Varagu (Kodo Millet) Upma',
                'meal_type': 'dinner',
                'description': 'Light and nutritious millet upma with vegetables',
                'ingredients': 'Varagu (kodo millet), vegetables, mustard seeds, curry leaves',
                'preparation_method': 'Cook millet, temper with spices, mix with vegetables',
                'calories': 220,
                'is_millet_based': True,
                'replaces': 'Semolina upma',
                'tamil_nadu_region': 'All regions'
            },
            {
                'name': 'Vegetable Soup with Millets',
                'meal_type': 'dinner',
                'description': 'Light vegetable soup with added millet for fiber',
                'ingredients': 'Mixed vegetables, millet flour, herbs',
                'preparation_method': 'Boil vegetables, thicken with millet flour',
                'calories': 150,
                'is_millet_based': True,
                'replaces': 'Heavy dinner',
                'tamil_nadu_region': 'All regions'
            },
            # Snacks
            {
                'name': 'Roasted Chana (Pottukadalai)',
                'meal_type': 'snacks',
                'description': 'Healthy roasted gram, rich in protein and fiber',
                'ingredients': 'Chana dal, salt',
                'preparation_method': 'Roast chana dal until crisp',
                'calories': 80,
                'is_millet_based': False,
                'replaces': 'Fried snacks',
                'tamil_nadu_region': 'All regions'
            },
            {
                'name': 'Millet Murukku',
                'meal_type': 'snacks',
                'description': 'Traditional murukku made with millet flour',
                'ingredients': 'Millet flour, gram flour, spices',
                'preparation_method': 'Mix flours, shape, deep fry in cold-pressed oil',
                'calories': 120,
                'is_millet_based': True,
                'replaces': 'Rice flour murukku',
                'tamil_nadu_region': 'All regions'
            },
        ]
        
        for suggestion in diet_suggestions:
            obj, created = DietSuggestion.objects.get_or_create(
                name=suggestion['name'],
                defaults=suggestion
            )
            if created:
                self.stdout.write(self.style.SUCCESS(f'Created: {suggestion["name"]}'))
            else:
                self.stdout.write(self.style.WARNING(f'Exists: {suggestion["name"]}'))
        
        self.stdout.write(self.style.SUCCESS('Diet data loaded successfully!'))