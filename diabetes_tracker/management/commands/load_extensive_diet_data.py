from django.core.management.base import BaseCommand
from diabetes_tracker.models import DietSuggestion

class Command(BaseCommand):
    help = 'Load extensive diet suggestions with 100+ Tamil Nadu traditional and millet-based meals'

    def handle(self, *args, **kwargs):
        diet_suggestions = [
            # ==================== BREAKFAST (25 options) ====================
            # Traditional Tamil Nadu Breakfast
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
            {
                'name': 'Ragi Idly',
                'meal_type': 'breakfast',
                'description': 'Healthy idly made with ragi and urad dal',
                'ingredients': 'Ragi flour, urad dal, fenugreek seeds, salt',
                'preparation_method': 'Ferment batter overnight, steam in idly plates',
                'calories': 110,
                'is_millet_based': True,
                'replaces': 'White rice idly',
                'tamil_nadu_region': 'All regions'
            },
            {
                'name': 'Kambu Dosa (Pearl Millet Dosa)',
                'meal_type': 'breakfast',
                'description': 'Crispy dosa made with pearl millet flour',
                'ingredients': 'Kambu flour, rice flour, onion, green chili',
                'preparation_method': 'Mix flours, add water, ferment, cook on tawa',
                'calories': 140,
                'is_millet_based': True,
                'replaces': 'Rice dosa',
                'tamil_nadu_region': 'All regions'
            },
            {
                'name': 'Samai Idly (Little Millet Idly)',
                'meal_type': 'breakfast',
                'description': 'Soft idly made with little millet',
                'ingredients': 'Samai, urad dal, fenugreek',
                'preparation_method': 'Soak millet and dal, grind, ferment, steam',
                'calories': 115,
                'is_millet_based': True,
                'replaces': 'Rice idly',
                'tamil_nadu_region': 'All regions'
            },
            {
                'name': 'Thinai Dosa (Foxtail Millet Dosa)',
                'meal_type': 'breakfast',
                'description': 'Healthy dosa with foxtail millet',
                'ingredients': 'Thinai flour, rice flour, onion, curry leaves',
                'preparation_method': 'Mix ingredients, cook on tawa',
                'calories': 135,
                'is_millet_based': True,
                'replaces': 'Rice dosa',
                'tamil_nadu_region': 'All regions'
            },
            {
                'name': 'Varagu Adai (Kodo Millet Lentil Pancake)',
                'meal_type': 'breakfast',
                'description': 'Protein-rich lentil and millet pancake',
                'ingredients': 'Varagu, toor dal, chana dal, red chili, curry leaves',
                'preparation_method': 'Soak millet and dal, grind coarse, cook on tawa',
                'calories': 180,
                'is_millet_based': True,
                'replaces': 'Rice adai',
                'tamil_nadu_region': 'All regions'
            },
            {
                'name': 'Kudumulu (Ragi Steamed Dumplings)',
                'meal_type': 'breakfast',
                'description': 'Steamed ragi dumplings, healthy breakfast option',
                'ingredients': 'Ragi flour, water, salt, coconut',
                'preparation_method': 'Mix ragi flour with water, shape into balls, steam',
                'calories': 125,
                'is_millet_based': True,
                'replaces': 'Rice kudumulu',
                'tamil_nadu_region': 'Kongu region'
            },
            {
                'name': 'Paniyaram with Millets',
                'meal_type': 'breakfast',
                'description': 'Soft and crispy paniyaram made with mixed millets',
                'ingredients': 'Mixed millet flour, urad dal, onion, curry leaves',
                'preparation_method': 'Ferment batter, cook in paniyaram pan',
                'calories': 130,
                'is_millet_based': True,
                'replaces': 'Rice paniyaram',
                'tamil_nadu_region': 'All regions'
            },
            {
                'name': 'Oats Ragi Porridge',
                'meal_type': 'breakfast',
                'description': 'Nutritious porridge with oats and ragi',
                'ingredients': 'Oats, ragi flour, milk, nuts',
                'preparation_method': 'Cook oats and ragi in milk, add nuts',
                'calories': 160,
                'is_millet_based': True,
                'replaces': 'Sugar cereal',
                'tamil_nadu_region': 'All regions'
            },
            {
                'name': 'Multi-Millet Upma',
                'meal_type': 'breakfast',
                'description': 'Healthy upma with mixed millets and vegetables',
                'ingredients': 'Mixed millets, vegetables, mustard seeds, curry leaves',
                'preparation_method': 'Roast millets, cook with vegetables',
                'calories': 170,
                'is_millet_based': True,
                'replaces': 'Semolina upma',
                'tamil_nadu_region': 'All regions'
            },
            {
                'name': 'Ragi Semiya (Ragi Vermicelli)',
                'meal_type': 'breakfast',
                'description': 'Vermicelli made with ragi flour',
                'ingredients': 'Ragi semiya, vegetables, mustard seeds',
                'preparation_method': 'Cook semiya, temper with spices and vegetables',
                'calories': 145,
                'is_millet_based': True,
                'replaces': 'Wheat semiya',
                'tamil_nadu_region': 'All regions'
            },
            {
                'name': 'Sprouted Millet Porridge',
                'meal_type': 'breakfast',
                'description': 'Highly nutritious porridge with sprouted millets',
                'ingredients': 'Sprouted kambu/samai, jaggery, cardamom',
                'preparation_method': 'Grind sprouted millets, cook with jaggery',
                'calories': 140,
                'is_millet_based': True,
                'replaces': 'Processed cereal',
                'tamil_nadu_region': 'All regions'
            },
            {
                'name': 'Kambu Puttu (Pearl Millet Puttu)',
                'meal_type': 'breakfast',
                'description': 'Steamed millet and coconut layered dish',
                'ingredients': 'Kambu flour, coconut, salt',
                'preparation_method': 'Layer millet flour and coconut, steam',
                'calories': 155,
                'is_millet_based': True,
                'replaces': 'Rice puttu',
                'tamil_nadu_region': 'Kongu region'
            },
            {
                'name': 'Thinai Puttu (Foxtail Millet Puttu)',
                'meal_type': 'breakfast',
                'description': 'Healthy puttu made with foxtail millet',
                'ingredients': 'Thinai flour, coconut, salt',
                'preparation_method': 'Layer and steam millet flour with coconut',
                'calories': 150,
                'is_millet_based': True,
                'replaces': 'Rice puttu',
                'tamil_nadu_region': 'All regions'
            },
            {
                'name': 'Egg White Ragi Dosa',
                'meal_type': 'breakfast',
                'description': 'Protein-rich ragi dosa with egg whites',
                'ingredients': 'Ragi flour, egg whites, onion, green chili',
                'preparation_method': 'Mix ingredients, cook like regular dosa',
                'calories': 165,
                'is_millet_based': True,
                'replaces': 'Plain dosa',
                'tamil_nadu_region': 'All regions'
            },
            {
                'name': 'Millet Chilla (Savory Pancake)',
                'meal_type': 'breakfast',
                'description': 'Quick savory pancake with millet flour',
                'ingredients': 'Millet flour, vegetables, spices',
                'preparation_method': 'Mix flour with vegetables, cook on tawa',
                'calories': 125,
                'is_millet_based': True,
                'replaces': 'Wheat chilla',
                'tamil_nadu_region': 'All regions'
            },
            {
                'name': 'Ragi Malt',
                'meal_type': 'breakfast',
                'description': 'Nutritious ragi malt drink',
                'ingredients': 'Ragi flour, milk, jaggery, cardamom',
                'preparation_method': 'Cook ragi with milk, add jaggery',
                'calories': 135,
                'is_millet_based': True,
                'replaces': 'Sweetened beverages',
                'tamil_nadu_region': 'All regions'
            },
            {
                'name': 'Kambu Sadam (Pearl Millet Rice)',
                'meal_type': 'breakfast',
                'description': 'Simple pearl millet rice with tempering',
                'ingredients': 'Kambu, mustard seeds, curry leaves, coconut',
                'preparation_method': 'Cook millet, temper with spices',
                'calories': 145,
                'is_millet_based': True,
                'replaces': 'White rice',
                'tamil_nadu_region': 'Kongu region'
            },
            {
                'name': 'Samai Pongal',
                'meal_type': 'breakfast',
                'description': 'Traditional pongal made with little millet',
                'ingredients': 'Samai, moong dal, pepper, ginger, ghee',
                'preparation_method': 'Cook millet and dal, temper with spices',
                'calories': 185,
                'is_millet_based': True,
                'replaces': 'Rice pongal',
                'tamil_nadu_region': 'All regions'
            },
            {
                'name': 'Varagu Aval (Kodo Millet Flattened Rice)',
                'meal_type': 'breakfast',
                'description': 'Healthy flattened rice made from kodo millet',
                'ingredients': 'Varagu aval, coconut, jaggery',
                'preparation_method': 'Soak aval, mix with coconut and jaggery',
                'calories': 140,
                'is_millet_based': True,
                'replaces': 'Rice aval',
                'tamil_nadu_region': 'All regions'
            },
            {
                'name': 'Vegetable Ragi Dosa',
                'meal_type': 'breakfast',
                'description': 'Ragi dosa loaded with vegetables',
                'ingredients': 'Ragi flour, carrot, beans, cabbage, spices',
                'preparation_method': 'Mix vegetables with batter, cook on tawa',
                'calories': 155,
                'is_millet_based': True,
                'replaces': 'Plain dosa',
                'tamil_nadu_region': 'All regions'
            },
            {
                'name': 'Sprouts Salad with Millets',
                'meal_type': 'breakfast',
                'description': 'Fresh sprouts salad with cooked millets',
                'ingredients': 'Sprouted moong, cooked millet, lemon, vegetables',
                'preparation_method': 'Mix all ingredients with lemon juice',
                'calories': 130,
                'is_millet_based': True,
                'replaces': 'Heavy breakfast',
                'tamil_nadu_region': 'All regions'
            },
            {
                'name': 'Millet Idiyappam',
                'meal_type': 'breakfast',
                'description': 'String hoppers made with millet flour',
                'ingredients': 'Millet flour, water, salt, coconut',
                'preparation_method': 'Make dough, press into strings, steam',
                'calories': 135,
                'is_millet_based': True,
                'replaces': 'Rice idiyappam',
                'tamil_nadu_region': 'All regions'
            },
            {
                'name': 'Sweet Ragi Porridge',
                'meal_type': 'breakfast',
                'description': 'Sweet porridge with ragi and palm jaggery',
                'ingredients': 'Ragi flour, palm jaggery, milk, cardamom',
                'preparation_method': 'Cook ragi with milk, add jaggery',
                'calories': 150,
                'is_millet_based': True,
                'replaces': 'Sugar cereal',
                'tamil_nadu_region': 'All regions'
            },
            
            # ==================== LUNCH (30 options) ====================
            {
                'name': 'Samai Rice (Little Millet) with Sambar',
                'meal_type': 'lunch',
                'description': 'Little millet served with vegetable sambar',
                'ingredients': 'Samai, toor dal, mixed vegetables, tamarind',
                'preparation_method': 'Cook millet like rice, prepare sambar',
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
            {
                'name': 'Varagu (Kodo Millet) Puliyodharai',
                'meal_type': 'lunch',
                'description': 'Tangy tamarind rice made with kodo millet',
                'ingredients': 'Varagu, tamarind, peanuts, curry leaves, spices',
                'preparation_method': 'Cook millet, mix with tamarind paste',
                'calories': 320,
                'is_millet_based': True,
                'replaces': 'Tamarind rice',
                'tamil_nadu_region': 'All regions'
            },
            {
                'name': 'Thinai (Foxtail Millet) Lemon Rice',
                'meal_type': 'lunch',
                'description': 'Refreshing lemon rice with foxtail millet',
                'ingredients': 'Thinai, lemon, peanuts, curry leaves, turmeric',
                'preparation_method': 'Cook millet, temper with spices, add lemon juice',
                'calories': 290,
                'is_millet_based': True,
                'replaces': 'Lemon rice with white rice',
                'tamil_nadu_region': 'All regions'
            },
            {
                'name': 'Kambu (Pearl Millet) Biryani',
                'meal_type': 'lunch',
                'description': 'Flavorful biryani made with pearl millet',
                'ingredients': 'Kambu, vegetables, biryani spices, mint, coriander',
                'preparation_method': 'Cook millet with spices and vegetables',
                'calories': 340,
                'is_millet_based': True,
                'replaces': 'Rice biryani',
                'tamil_nadu_region': 'All regions'
            },
            {
                'name': 'Samai Biryani (Little Millet Biryani)',
                'meal_type': 'lunch',
                'description': 'Aromatic biryani with little millet',
                'ingredients': 'Samai, mixed vegetables, spices, mint',
                'preparation_method': 'Layer and cook millet with vegetables',
                'calories': 330,
                'is_millet_based': True,
                'replaces': 'Rice biryani',
                'tamil_nadu_region': 'All regions'
            },
            {
                'name': 'Ragi Sangati with Natukozhi Kuzhambu',
                'meal_type': 'lunch',
                'description': 'Traditional ragi balls with country chicken curry',
                'ingredients': 'Ragi flour, country chicken, spices, coconut',
                'preparation_method': 'Make ragi balls, prepare chicken curry',
                'calories': 420,
                'is_millet_based': True,
                'replaces': 'Rice with chicken curry',
                'tamil_nadu_region': 'Rural Tamil Nadu'
            },
            {
                'name': 'Multi-Millet Rice',
                'meal_type': 'lunch',
                'description': 'Mixed millet rice with vegetables',
                'ingredients': 'Mixed millets, vegetables, mustard seeds',
                'preparation_method': 'Cook mixed millets, temper with vegetables',
                'calories': 310,
                'is_millet_based': True,
                'replaces': 'Plain white rice',
                'tamil_nadu_region': 'All regions'
            },
            {
                'name': 'Varagu Coconut Rice',
                'meal_type': 'lunch',
                'description': 'Fragrant coconut rice with kodo millet',
                'ingredients': 'Varagu, coconut, cashews, curry leaves',
                'preparation_method': 'Cook millet, mix with coconut and tempering',
                'calories': 325,
                'is_millet_based': True,
                'replaces': 'Coconut rice with white rice',
                'tamil_nadu_region': 'All regions'
            },
            {
                'name': 'Thinai Curd Rice',
                'meal_type': 'lunch',
                'description': 'Cooling curd rice with foxtail millet',
                'ingredients': 'Thinai, curd, carrot, ginger, pomegranate',
                'preparation_method': 'Cook millet, mix with curd and vegetables',
                'calories': 280,
                'is_millet_based': True,
                'replaces': 'Curd rice with white rice',
                'tamil_nadu_region': 'All regions'
            },
            {
                'name': 'Kambu Tomato Rice',
                'meal_type': 'lunch',
                'description': 'Tangy tomato rice with pearl millet',
                'ingredients': 'Kambu, tomatoes, onions, spices',
                'preparation_method': 'Cook millet, mix with tomato masala',
                'calories': 295,
                'is_millet_based': True,
                'replaces': 'Tomato rice with white rice',
                'tamil_nadu_region': 'All regions'
            },
            {
                'name': 'Samai Vegetable Pulao',
                'meal_type': 'lunch',
                'description': 'Healthy pulao with little millet and vegetables',
                'ingredients': 'Samai, mixed vegetables, pulao spices',
                'preparation_method': 'Cook millet with vegetables and spices',
                'calories': 315,
                'is_millet_based': True,
                'replaces': 'Rice pulao',
                'tamil_nadu_region': 'All regions'
            },
            {
                'name': 'Ragi Noodles with Vegetables',
                'meal_type': 'lunch',
                'description': 'Healthy ragi noodles stir-fried with vegetables',
                'ingredients': 'Ragi noodles, mixed vegetables, soy sauce',
                'preparation_method': 'Boil noodles, stir-fry with vegetables',
                'calories': 290,
                'is_millet_based': True,
                'replaces': 'Wheat noodles',
                'tamil_nadu_region': 'All regions'
            },
            {
                'name': 'Kambu Pongal',
                'meal_type': 'lunch',
                'description': 'Savory pongal with pearl millet',
                'ingredients': 'Kambu, moong dal, pepper, ginger, ghee',
                'preparation_method': 'Cook millet and dal, temper with spices',
                'calories': 325,
                'is_millet_based': True,
                'replaces': 'Rice pongal',
                'tamil_nadu_region': 'All regions'
            },
            {
                'name': 'Varagu Bisibele Bath',
                'meal_type': 'lunch',
                'description': 'Spicy lentil and vegetable rice with kodo millet',
                'ingredients': 'Varagu, toor dal, vegetables, bisibele bath masala',
                'preparation_method': 'Cook millet and dal with vegetables and spices',
                'calories': 360,
                'is_millet_based': True,
                'replaces': 'Rice bisibele bath',
                'tamil_nadu_region': 'All regions'
            },
            {
                'name': 'Samai Khichdi',
                'meal_type': 'lunch',
                'description': 'Comforting khichdi with little millet and moong dal',
                'ingredients': 'Samai, moong dal, vegetables, ghee',
                'preparation_method': 'Cook millet and dal together with vegetables',
                'calories': 305,
                'is_millet_based': True,
                'replaces': 'Rice khichdi',
                'tamil_nadu_region': 'All regions'
            },
            {
                'name': 'Thinai Vegetable Fried Rice',
                'meal_type': 'lunch',
                'description': 'Healthy fried rice with foxtail millet',
                'ingredients': 'Thinai, mixed vegetables, spring onions, soy sauce',
                'preparation_method': 'Cook millet, stir-fry with vegetables',
                'calories': 295,
                'is_millet_based': True,
                'replaces': 'Rice fried rice',
                'tamil_nadu_region': 'All regions'
            },
            {
                'name': 'Kambu Puliyodharai',
                'meal_type': 'lunch',
                'description': 'Tamarind rice with pearl millet',
                'ingredients': 'Kambu, tamarind, peanuts, spices',
                'preparation_method': 'Cook millet, mix with tamarind paste',
                'calories': 310,
                'is_millet_based': True,
                'replaces': 'Rice puliyodharai',
                'tamil_nadu_region': 'All regions'
            },
            {
                'name': 'Ragi Dosa with Vegetable Kurma',
                'meal_type': 'lunch',
                'description': 'Ragi dosa served with creamy vegetable kurma',
                'ingredients': 'Ragi flour, vegetables, coconut, spices',
                'preparation_method': 'Make dosa, prepare kurma separately',
                'calories': 345,
                'is_millet_based': True,
                'replaces': 'Wheat dosa with kurma',
                'tamil_nadu_region': 'All regions'
            },
            {
                'name': 'Millet Chapati with Vegetable Curry',
                'meal_type': 'lunch',
                'description': 'Soft chapatis made with mixed millet flour',
                'ingredients': 'Mixed millet flour, wheat flour, vegetables for curry',
                'preparation_method': 'Make dough, roll chapatis, cook on tawa',
                'calories': 350,
                'is_millet_based': True,
                'replaces': 'Wheat chapati',
                'tamil_nadu_region': 'All regions'
            },
            {
                'name': 'Varagu Parotta',
                'meal_type': 'lunch',
                'description': 'Layered parotta made with kodo millet',
                'ingredients': 'Varagu flour, wheat flour, oil, salt',
                'preparation_method': 'Make dough, layer and roll, cook on tawa',
                'calories': 340,
                'is_millet_based': True,
                'replaces': 'Maida parotta',
                'tamil_nadu_region': 'All regions'
            },
            {
                'name': 'Samai Puttu with Kadala Curry',
                'meal_type': 'lunch',
                'description': 'Steamed millet puttu with chickpea curry',
                'ingredients': 'Samai flour, coconut, chickpeas, spices',
                'preparation_method': 'Make puttu, prepare kadala curry',
                'calories': 355,
                'is_millet_based': True,
                'replaces': 'Rice puttu',
                'tamil_nadu_region': 'All regions'
            },
            {
                'name': 'Thinai Idiyappam with Vegetable Stew',
                'meal_type': 'lunch',
                'description': 'String hoppers with coconut vegetable stew',
                'ingredients': 'Thinai flour, vegetables, coconut milk, spices',
                'preparation_method': 'Make idiyappam, prepare stew',
                'calories': 330,
                'is_millet_based': True,
                'replaces': 'Rice idiyappam',
                'tamil_nadu_region': 'All regions'
            },
            {
                'name': 'Kambu Appam with Vegetable Stew',
                'meal_type': 'lunch',
                'description': 'Soft appam with pearl millet',
                'ingredients': 'Kambu flour, rice flour, coconut, vegetable stew',
                'preparation_method': 'Ferment batter, make appam, serve with stew',
                'calories': 320,
                'is_millet_based': True,
                'replaces': 'Rice appam',
                'tamil_nadu_region': 'All regions'
            },
            {
                'name': 'Ragi Wheat Noodles',
                'meal_type': 'lunch',
                'description': 'Healthy noodles made with ragi and wheat',
                'ingredients': 'Ragi flour, wheat flour, vegetables',
                'preparation_method': 'Make noodles, boil, stir-fry with vegetables',
                'calories': 285,
                'is_millet_based': True,
                'replaces': 'Maida noodles',
                'tamil_nadu_region': 'All regions'
            },
            {
                'name': 'Millet Stuffed Paratha',
                'meal_type': 'lunch',
                'description': 'Stuffed paratha with millet dough',
                'ingredients': 'Millet flour, wheat flour, potato or paneer filling',
                'preparation_method': 'Make dough, stuff with filling, roll, cook',
                'calories': 365,
                'is_millet_based': True,
                'replaces': 'Wheat paratha',
                'tamil_nadu_region': 'All regions'
            },
            {
                'name': 'Varagu Dosa with Chutney',
                'meal_type': 'lunch',
                'description': 'Crispy dosa with kodo millet',
                'ingredients': 'Varagu flour, rice flour, coconut chutney',
                'preparation_method': 'Make dosa batter, cook on tawa',
                'calories': 295,
                'is_millet_based': True,
                'replaces': 'Rice dosa',
                'tamil_nadu_region': 'All regions'
            },
            {
                'name': 'Samai Kozhukattai',
                'meal_type': 'lunch',
                'description': 'Steamed dumplings with little millet',
                'ingredients': 'Samai, coconut, jaggery or savory filling',
                'preparation_method': 'Make dough, shape, steam',
                'calories': 275,
                'is_millet_based': True,
                'replaces': 'Rice kozhukattai',
                'tamil_nadu_region': 'All regions'
            },
            {
                'name': 'Thinai Aval Upma',
                'meal_type': 'lunch',
                'description': 'Upma with foxtail millet flattened rice',
                'ingredients': 'Thinai aval, vegetables, mustard seeds',
                'preparation_method': 'Soak aval, temper with vegetables',
                'calories': 260,
                'is_millet_based': True,
                'replaces': 'Rice aval upma',
                'tamil_nadu_region': 'All regions'
            },
            {
                'name': 'Mixed Millet Salad Bowl',
                'meal_type': 'lunch',
                'description': 'Light and nutritious millet salad',
                'ingredients': 'Cooked millets, vegetables, lemon, herbs',
                'preparation_method': 'Mix all ingredients with dressing',
                'calories': 245,
                'is_millet_based': True,
                'replaces': 'Heavy lunch',
                'tamil_nadu_region': 'All regions'
            },
            
            # ==================== DINNER (30 options) ====================
            {
                'name': 'Varagu (Kodo Millet) Upma',
                'meal_type': 'dinner',
                'description': 'Light and nutritious millet upma with vegetables',
                'ingredients': 'Varagu, vegetables, mustard seeds, curry leaves',
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
            {
                'name': 'Thinai (Foxtail Millet) Pongal',
                'meal_type': 'dinner',
                'description': 'Healthy version of traditional pongal with millet',
                'ingredients': 'Thinai, moong dal, pepper, ginger, ghee',
                'preparation_method': 'Cook millet and dal, temper with spices',
                'calories': 280,
                'is_millet_based': True,
                'replaces': 'Rice pongal',
                'tamil_nadu_region': 'All regions'
            },
            {
                'name': 'Ragi Soup',
                'meal_type': 'dinner',
                'description': 'Warm and nutritious ragi soup',
                'ingredients': 'Ragi flour, vegetables, pepper, cumin',
                'preparation_method': 'Mix ragi with water, add vegetables and spices',
                'calories': 135,
                'is_millet_based': True,
                'replaces': 'Cream soup',
                'tamil_nadu_region': 'All regions'
            },
            {
                'name': 'Samai Khichdi',
                'meal_type': 'dinner',
                'description': 'Light khichdi for dinner with little millet',
                'ingredients': 'Samai, moong dal, vegetables, ghee',
                'preparation_method': 'Cook millet and dal together',
                'calories': 240,
                'is_millet_based': True,
                'replaces': 'Rice khichdi',
                'tamil_nadu_region': 'All regions'
            },
            {
                'name': 'Kambu Congee (Pearl Millet Porridge)',
                'meal_type': 'dinner',
                'description': 'Comforting congee with pearl millet',
                'ingredients': 'Kambu, vegetables, ginger, spices',
                'preparation_method': 'Cook millet with vegetables until soft',
                'calories': 165,
                'is_millet_based': True,
                'replaces': 'Rice congee',
                'tamil_nadu_region': 'All regions'
            },
            {
                'name': 'Millet Dosa with Chutney',
                'meal_type': 'dinner',
                'description': 'Light dosa for dinner with mixed millets',
                'ingredients': 'Mixed millet flour, rice flour, coconut chutney',
                'preparation_method': 'Make dosa batter, cook on tawa',
                'calories': 210,
                'is_millet_based': True,
                'replaces': 'Rice dosa',
                'tamil_nadu_region': 'All regions'
            },
            {
                'name': 'Ragi Chapati with Dal',
                'meal_type': 'dinner',
                'description': 'Healthy ragi chapatis with lentil soup',
                'ingredients': 'Ragi flour, wheat flour, toor dal, spices',
                'preparation_method': 'Make chapatis, prepare dal',
                'calories': 265,
                'is_millet_based': True,
                'replaces': 'Wheat chapati',
                'tamil_nadu_region': 'All regions'
            },
            {
                'name': 'Vegetable Millet Stew',
                'meal_type': 'dinner',
                'description': 'Hearty vegetable stew with millets',
                'ingredients': 'Mixed millets, vegetables, coconut milk',
                'preparation_method': 'Cook millets with vegetables in coconut milk',
                'calories': 225,
                'is_millet_based': True,
                'replaces': 'Creamy stew',
                'tamil_nadu_region': 'All regions'
            },
            {
                'name': 'Samai Idly with Sambar',
                'meal_type': 'dinner',
                'description': 'Light idly with little millet for dinner',
                'ingredients': 'Samai, urad dal, sambar',
                'preparation_method': 'Make idly batter, steam, serve with sambar',
                'calories': 200,
                'is_millet_based': True,
                'replaces': 'Rice idly',
                'tamil_nadu_region': 'All regions'
            },
            {
                'name': 'Varagu Aval Upma',
                'meal_type': 'dinner',
                'description': 'Light upma with kodo millet flattened rice',
                'ingredients': 'Varagu aval, vegetables, mustard seeds',
                'preparation_method': 'Soak aval, temper with vegetables',
                'calories': 195,
                'is_millet_based': True,
                'replaces': 'Rice upma',
                'tamil_nadu_region': 'All regions'
            },
            {
                'name': 'Millet Noodles Soup',
                'meal_type': 'dinner',
                'description': 'Comforting noodle soup with millet noodles',
                'ingredients': 'Millet noodles, vegetables, vegetable broth',
                'preparation_method': 'Cook noodles in vegetable broth',
                'calories': 175,
                'is_millet_based': True,
                'replaces': 'Wheat noodles soup',
                'tamil_nadu_region': 'All regions'
            },
            {
                'name': 'Thinai Paniyaram',
                'meal_type': 'dinner',
                'description': 'Soft paniyaram with foxtail millet',
                'ingredients': 'Thinai, urad dal, onion, curry leaves',
                'preparation_method': 'Ferment batter, cook in paniyaram pan',
                'calories': 185,
                'is_millet_based': True,
                'replaces': 'Rice paniyaram',
                'tamil_nadu_region': 'All regions'
            },
            {
                'name': 'Kambu Adai',
                'meal_type': 'dinner',
                'description': 'Protein-rich lentil and millet pancake',
                'ingredients': 'Kambu, toor dal, chana dal, spices',
                'preparation_method': 'Soak millet and dal, grind, cook on tawa',
                'calories': 230,
                'is_millet_based': True,
                'replaces': 'Rice adai',
                'tamil_nadu_region': 'All regions'
            },
            {
                'name': 'Ragi Roti with Vegetable Curry',
                'meal_type': 'dinner',
                'description': 'Ragi rotis with light vegetable curry',
                'ingredients': 'Ragi flour, vegetables, spices',
                'preparation_method': 'Make rotis, prepare vegetable curry',
                'calories': 245,
                'is_millet_based': True,
                'replaces': 'Wheat roti',
                'tamil_nadu_region': 'All regions'
            },
            {
                'name': 'Samai Puttu with Banana',
                'meal_type': 'dinner',
                'description': 'Light puttu with little millet and banana',
                'ingredients': 'Samai flour, coconut, banana',
                'preparation_method': 'Make puttu, serve with banana',
                'calories': 210,
                'is_millet_based': True,
                'replaces': 'Rice puttu',
                'tamil_nadu_region': 'All regions'
            },
            {
                'name': 'Millet Salad Bowl',
                'meal_type': 'dinner',
                'description': 'Light and refreshing millet salad',
                'ingredients': 'Cooked millets, greens, vegetables, lemon',
                'preparation_method': 'Mix all ingredients with dressing',
                'calories': 160,
                'is_millet_based': True,
                'replaces': 'Heavy dinner',
                'tamil_nadu_region': 'All regions'
            },
            {
                'name': 'Varagu Lemon Rice',
                'meal_type': 'dinner',
                'description': 'Light lemon rice with kodo millet',
                'ingredients': 'Varagu, lemon, peanuts, turmeric',
                'preparation_method': 'Cook millet, mix with lemon and tempering',
                'calories': 205,
                'is_millet_based': True,
                'replaces': 'Rice lemon rice',
                'tamil_nadu_region': 'All regions'
            },
            {
                'name': 'Thinai Curd Rice',
                'meal_type': 'dinner',
                'description': 'Cooling curd rice with foxtail millet',
                'ingredients': 'Thinai, curd, ginger, pomegranate',
                'preparation_method': 'Cook millet, mix with curd and tempering',
                'calories': 185,
                'is_millet_based': True,
                'replaces': 'Curd rice',
                'tamil_nadu_region': 'All regions'
            },
            {
                'name': 'Kambu Dosa with Chutney',
                'meal_type': 'dinner',
                'description': 'Crispy pearl millet dosa for dinner',
                'ingredients': 'Kambu flour, rice flour, chutney',
                'preparation_method': 'Make dosa batter, cook on tawa',
                'calories': 190,
                'is_millet_based': True,
                'replaces': 'Rice dosa',
                'tamil_nadu_region': 'All regions'
            },
            {
                'name': 'Millet Veggie Wrap',
                'meal_type': 'dinner',
                'description': 'Healthy wrap with millet roti and vegetables',
                'ingredients': 'Millet roti, grilled vegetables, hummus',
                'preparation_method': 'Make roti, fill with vegetables',
                'calories': 240,
                'is_millet_based': True,
                'replaces': 'Wheat wrap',
                'tamil_nadu_region': 'All regions'
            },
            {
                'name': 'Samai Tomato Bath',
                'meal_type': 'dinner',
                'description': 'Light tomato rice with little millet',
                'ingredients': 'Samai, tomatoes, onions, spices',
                'preparation_method': 'Cook millet, mix with tomato masala',
                'calories': 215,
                'is_millet_based': True,
                'replaces': 'Tomato rice',
                'tamil_nadu_region': 'All regions'
            },
            {
                'name': 'Ragi Vermicelli Kheer',
                'meal_type': 'dinner',
                'description': 'Sweet kheer for light dessert dinner',
                'ingredients': 'Ragi semiya, milk, jaggery, cardamom',
                'preparation_method': 'Cook semiya in milk, add jaggery',
                'calories': 195,
                'is_millet_based': True,
                'replaces': 'Rice kheer',
                'tamil_nadu_region': 'All regions'
            },
            {
                'name': 'Vegetable Millet Porridge',
                'meal_type': 'dinner',
                'description': 'Comforting vegetable porridge with millets',
                'ingredients': 'Mixed millets, vegetables, vegetable stock',
                'preparation_method': 'Cook millets with vegetables until soft',
                'calories': 170,
                'is_millet_based': True,
                'replaces': 'Cream porridge',
                'tamil_nadu_region': 'All regions'
            },
            {
                'name': 'Kambu Idiyappam',
                'meal_type': 'dinner',
                'description': 'String hoppers with pearl millet',
                'ingredients': 'Kambu flour, water, coconut',
                'preparation_method': 'Make dough, press into strings, steam',
                'calories': 165,
                'is_millet_based': True,
                'replaces': 'Rice idiyappam',
                'tamil_nadu_region': 'All regions'
            },
            {
                'name': 'Thinai Kozhukattai',
                'meal_type': 'dinner',
                'description': 'Steamed dumplings with foxtail millet',
                'ingredients': 'Thinai, coconut, jaggery',
                'preparation_method': 'Make dough, shape, steam',
                'calories': 175,
                'is_millet_based': True,
                'replaces': 'Rice kozhukattai',
                'tamil_nadu_region': 'All regions'
            },
            {
                'name': 'Millet Dalia',
                'meal_type': 'dinner',
                'description': 'Healthy cracked millet porridge',
                'ingredients': 'Cracked millets, moong dal, vegetables',
                'preparation_method': 'Cook millet and dal with vegetables',
                'calories': 200,
                'is_millet_based': True,
                'replaces': 'Wheat dalia',
                'tamil_nadu_region': 'All regions'
            },
            {
                'name': 'Varagu Puttu with Kadala Curry',
                'meal_type': 'dinner',
                'description': 'Light puttu with kodo millet and chickpea curry',
                'ingredients': 'Varagu flour, coconut, chickpeas',
                'preparation_method': 'Make puttu, prepare kadala curry',
                'calories': 260,
                'is_millet_based': True,
                'replaces': 'Rice puttu',
                'tamil_nadu_region': 'All regions'
            },
            {
                'name': 'Ragi Pongal',
                'meal_type': 'dinner',
                'description': 'Light pongal with ragi for dinner',
                'ingredients': 'Ragi, moong dal, pepper, ginger',
                'preparation_method': 'Cook ragi and dal, temper with spices',
                'calories': 215,
                'is_millet_based': True,
                'replaces': 'Rice pongal',
                'tamil_nadu_region': 'All regions'
            },
            {
                'name': 'Millet Stuffed Capsicum',
                'meal_type': 'dinner',
                'description': 'Baked capsicum stuffed with millet and vegetables',
                'ingredients': 'Cooked millets, capsicum, vegetables, cheese',
                'preparation_method': 'Stuff capsicum with millet mixture, bake',
                'calories': 235,
                'is_millet_based': True,
                'replaces': 'Rice stuffed capsicum',
                'tamil_nadu_region': 'All regions'
            },
            
            # ==================== SNACKS (25 options) ====================
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
            {
                'name': 'Ragi Halwa',
                'meal_type': 'snacks',
                'description': 'Healthy sweet made with ragi and jaggery',
                'ingredients': 'Ragi flour, jaggery, ghee, nuts',
                'preparation_method': 'Roast ragi flour, cook with jaggery and ghee',
                'calories': 150,
                'is_millet_based': True,
                'replaces': 'Wheat halwa',
                'tamil_nadu_region': 'All regions'
            },
            {
                'name': 'Millet Ladoo',
                'meal_type': 'snacks',
                'description': 'Nutritious ladoos with millet flour',
                'ingredients': 'Millet flour, jaggery, ghee, nuts',
                'preparation_method': 'Roast millet flour, shape into balls',
                'calories': 135,
                'is_millet_based': True,
                'replaces': 'Wheat ladoo',
                'tamil_nadu_region': 'All regions'
            },
            {
                'name': 'Kambu Murukku',
                'meal_type': 'snacks',
                'description': 'Crispy murukku with pearl millet',
                'ingredients': 'Kambu flour, rice flour, butter, spices',
                'preparation_method': 'Mix flours, shape, fry',
                'calories': 115,
                'is_millet_based': True,
                'replaces': 'Rice murukku',
                'tamil_nadu_region': 'All regions'
            },
            {
                'name': 'Sprouted Moong Salad',
                'meal_type': 'snacks',
                'description': 'Fresh sprouts salad with lemon',
                'ingredients': 'Sprouted moong, onion, tomato, lemon',
                'preparation_method': 'Mix all ingredients with lemon juice',
                'calories': 70,
                'is_millet_based': False,
                'replaces': 'Fried snacks',
                'tamil_nadu_region': 'All regions'
            },
            {
                'name': 'Millet Chivda (Puffed Millet Mix)',
                'meal_type': 'snacks',
                'description': 'Healthy snack mix with puffed millets',
                'ingredients': 'Puffed millets, peanuts, curry leaves, spices',
                'preparation_method': 'Roast puffed millets with nuts and spices',
                'calories': 110,
                'is_millet_based': True,
                'replaces': 'Puffed rice chivda',
                'tamil_nadu_region': 'All regions'
            },
            {
                'name': 'Ragi Banana Smoothie',
                'meal_type': 'snacks',
                'description': 'Nutritious smoothie with ragi and banana',
                'ingredients': 'Ragi flour, banana, milk, honey',
                'preparation_method': 'Blend all ingredients until smooth',
                'calories': 145,
                'is_millet_based': True,
                'replaces': 'Sugar smoothie',
                'tamil_nadu_region': 'All regions'
            },
            {
                'name': 'Millet Cutlets',
                'meal_type': 'snacks',
                'description': 'Baked cutlets with millet and vegetables',
                'ingredients': 'Cooked millets, mashed potatoes, vegetables, spices',
                'preparation_method': 'Mix ingredients, shape into patties, bake',
                'calories': 125,
                'is_millet_based': True,
                'replaces': 'Fried cutlets',
                'tamil_nadu_region': 'All regions'
            },
            {
                'name': 'Kambu Koozh (Fermented Drink)',
                'meal_type': 'snacks',
                'description': 'Traditional fermented millet drink',
                'ingredients': 'Kambu, buttermilk, onion, salt',
                'preparation_method': 'Ferment millet, mix with buttermilk',
                'calories': 90,
                'is_millet_based': True,
                'replaces': 'Sugary drinks',
                'tamil_nadu_region': 'Kongu region'
            },
            {
                'name': 'Thinai Puffed Rice Balls',
                'meal_type': 'snacks',
                'description': 'Healthy energy balls with puffed millet',
                'ingredients': 'Puffed thinai, jaggery, ghee',
                'preparation_method': 'Mix puffed millet with jaggery syrup, shape',
                'calories': 105,
                'is_millet_based': True,
                'replaces': 'Sugar candies',
                'tamil_nadu_region': 'All regions'
            },
            {
                'name': 'Ragi Crackers',
                'meal_type': 'snacks',
                'description': 'Crispy baked crackers with ragi',
                'ingredients': 'Ragi flour, wheat flour, herbs, oil',
                'preparation_method': 'Make dough, roll, cut, bake',
                'calories': 95,
                'is_millet_based': True,
                'replaces': 'Maida crackers',
                'tamil_nadu_region': 'All regions'
            },
            {
                'name': 'Millet Dosa Bites',
                'meal_type': 'snacks',
                'description': 'Mini dosa bites for snacking',
                'ingredients': 'Millet dosa batter, vegetables',
                'preparation_method': 'Make small dosas on tawa',
                'calories': 85,
                'is_millet_based': True,
                'replaces': 'Fried snacks',
                'tamil_nadu_region': 'All regions'
            },
            {
                'name': 'Samai Puffed Rice',
                'meal_type': 'snacks',
                'description': 'Light puffed little millet snack',
                'ingredients': 'Puffed samai, peanuts, spices',
                'preparation_method': 'Roast puffed samai with spices',
                'calories': 75,
                'is_millet_based': True,
                'replaces': 'Puffed rice',
                'tamil_nadu_region': 'All regions'
            },
            {
                'name': 'Varagu Popcorn',
                'meal_type': 'snacks',
                'description': 'Healthy popcorn with kodo millet',
                'ingredients': 'Varagu grains, oil, salt',
                'preparation_method': 'Pop varagu grains like popcorn',
                'calories': 70,
                'is_millet_based': True,
                'replaces': 'Corn popcorn',
                'tamil_nadu_region': 'All regions'
            },
            {
                'name': 'Millet Energy Bar',
                'meal_type': 'snacks',
                'description': 'Homemade energy bar with millets and nuts',
                'ingredients': 'Millet flour, oats, nuts, dates, honey',
                'preparation_method': 'Mix ingredients, bake until firm',
                'calories': 160,
                'is_millet_based': True,
                'replaces': 'Commercial energy bars',
                'tamil_nadu_region': 'All regions'
            },
            {
                'name': 'Ragi Date Balls',
                'meal_type': 'snacks',
                'description': 'No-sugar energy balls with ragi and dates',
                'ingredients': 'Ragi flour, dates, nuts, coconut',
                'preparation_method': 'Mix ingredients, roll into balls',
                'calories': 130,
                'is_millet_based': True,
                'replaces': 'Sugar sweets',
                'tamil_nadu_region': 'All regions'
            },
            {
                'name': 'Thinai Upma Cutlets',
                'meal_type': 'snacks',
                'description': 'Leftover upma shaped into cutlets',
                'ingredients': 'Thinai upma, breadcrumbs',
                'preparation_method': 'Shape upma into patties, shallow fry',
                'calories': 115,
                'is_millet_based': True,
                'replaces': 'Fried snacks',
                'tamil_nadu_region': 'All regions'
            },
            {
                'name': 'Kambu Biscuits',
                'meal_type': 'snacks',
                'description': 'Savory biscuits with pearl millet',
                'ingredients': 'Kambu flour, wheat flour, butter, herbs',
                'preparation_method': 'Make dough, cut shapes, bake',
                'calories': 100,
                'is_millet_based': True,
                'replaces': 'Maida biscuits',
                'tamil_nadu_region': 'All regions'
            },
            {
                'name': 'Millet Veggie Puffs',
                'meal_type': 'snacks',
                'description': 'Baked puffs with millet and vegetables',
                'ingredients': 'Millet flour, vegetables, cheese',
                'preparation_method': 'Make dough, fill with vegetables, bake',
                'calories': 140,
                'is_millet_based': True,
                'replaces': 'Puff pastry',
                'tamil_nadu_region': 'All regions'
            },
            {
                'name': 'Samai Kozhukattai',
                'meal_type': 'snacks',
                'description': 'Steamed dumplings with little millet',
                'ingredients': 'Samai, coconut, jaggery',
                'preparation_method': 'Make dough, shape, steam',
                'calories': 110,
                'is_millet_based': True,
                'replaces': 'Rice kozhukattai',
                'tamil_nadu_region': 'All regions'
            },
            {
                'name': 'Ragi Masala Vada',
                'meal_type': 'snacks',
                'description': 'Healthy vada with ragi and lentils',
                'ingredients': 'Ragi flour, chana dal, spices, curry leaves',
                'preparation_method': 'Mix ingredients, shape, deep fry in healthy oil',
                'calories': 145,
                'is_millet_based': True,
                'replaces': 'Rice vada',
                'tamil_nadu_region': 'All regions'
            },
            {
                'name': 'Millet Thepla',
                'meal_type': 'snacks',
                'description': 'Gujarati style millet flatbread for snacking',
                'ingredients': 'Millet flour, wheat flour, fenugreek, spices',
                'preparation_method': 'Make dough, roll, cook on tawa',
                'calories': 125,
                'is_millet_based': True,
                'replaces': 'Wheat thepla',
                'tamil_nadu_region': 'All regions'
            },
            {
                'name': 'Varagu Aval Mixture',
                'meal_type': 'snacks',
                'description': 'Crispy snack mix with kodo millet flakes',
                'ingredients': 'Varagu aval, peanuts, curry leaves, spices',
                'preparation_method': 'Roast all ingredients together',
                'calories': 105,
                'is_millet_based': True,
                'replaces': 'Rice mixture',
                'tamil_nadu_region': 'All regions'
            },
            {
                'name': 'Thinai Popcorn Balls',
                'meal_type': 'snacks',
                'description': 'Fun snack balls with puffed foxtail millet',
                'ingredients': 'Puffed thinai, honey, nuts',
                'preparation_method': 'Mix puffed millet with honey, shape into balls',
                'calories': 95,
                'is_millet_based': True,
                'replaces': 'Sugar popcorn balls',
                'tamil_nadu_region': 'All regions'
            },
        ]
        
        count = 0
        existing = 0
        for suggestion in diet_suggestions:
            obj, created = DietSuggestion.objects.get_or_create(
                name=suggestion['name'],
                defaults=suggestion
            )
            if created:
                count += 1
                self.stdout.write(self.style.SUCCESS(f'✓ Created: {suggestion["name"]}'))
            else:
                existing += 1
        
        self.stdout.write(self.style.SUCCESS(f'\n✅ Successfully added {count} new diet suggestions!'))
        self.stdout.write(self.style.SUCCESS(f'📊 Total existing: {existing}'))
        self.stdout.write(self.style.SUCCESS(f'🎯 Grand total: {DietSuggestion.objects.count()} diet suggestions'))