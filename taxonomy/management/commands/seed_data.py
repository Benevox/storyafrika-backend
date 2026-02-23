"""
Management command to seed initial data for StoryAfrika.
Populates categories, countries, themes, and eras based on PRD.
"""
from django.core.management.base import BaseCommand
from taxonomy.models import Category, Country, Theme, Era


class Command(BaseCommand):
    help = 'Seeds initial data for categories, countries, themes, and eras'

    def handle(self, *args, **kwargs):
        self.stdout.write('Seeding StoryAfrika initial data...\n')

        # Seed Categories (Content Pillars from PRD)
        self.stdout.write('Creating categories...')
        categories = [
            {
                'name': 'Stories of Life',
                'description': 'Personal experiences, memories, and everyday African life',
                'order': 1
            },
            {
                'name': 'Culture and Traditions',
                'description': 'Exploration of rituals, customs, languages, food, and identity',
                'order': 2
            },
            {
                'name': 'History and Memory',
                'description': 'Historical narratives, forgotten figures, and collective memory',
                'order': 3
            },
            {
                'name': 'Journeys and Lessons',
                'description': 'Stories of growth, struggle, learning, and transformation',
                'order': 4
            },
            {
                'name': 'Creative Voices',
                'description': 'Fiction, poetry, and artistic expression grounded in African contexts',
                'order': 5
            },
        ]

        for cat_data in categories:
            category, created = Category.objects.get_or_create(
                name=cat_data['name'],
                defaults={
                    'description': cat_data['description'],
                    'order': cat_data['order']
                }
            )
            if created:
                self.stdout.write(f'  ✓ Created: {category.name}')
            else:
                self.stdout.write(f'  - Exists: {category.name}')

        # Seed Countries (Major African Countries)
        self.stdout.write('\nCreating countries...')
        countries = [
            {'name': 'Nigeria', 'flag_emoji': '🇳🇬'},
            {'name': 'Kenya', 'flag_emoji': '🇰🇪'},
            {'name': 'South Africa', 'flag_emoji': '🇿🇦'},
            {'name': 'Ghana', 'flag_emoji': '🇬🇭'},
            {'name': 'Ethiopia', 'flag_emoji': '🇪🇹'},
            {'name': 'Tanzania', 'flag_emoji': '🇹🇿'},
            {'name': 'Uganda', 'flag_emoji': '🇺🇬'},
            {'name': 'Egypt', 'flag_emoji': '🇪🇬'},
            {'name': 'Morocco', 'flag_emoji': '🇲🇦'},
            {'name': 'Senegal', 'flag_emoji': '🇸🇳'},
            {'name': 'Cameroon', 'flag_emoji': '🇨🇲'},
            {'name': 'Rwanda', 'flag_emoji': '🇷🇼'},
            {'name': 'Zimbabwe', 'flag_emoji': '🇿🇼'},
            {'name': 'Botswana', 'flag_emoji': '🇧🇼'},
            {'name': 'Namibia', 'flag_emoji': '🇳🇦'},
            {'name': 'Zambia', 'flag_emoji': '🇿🇲'},
            {'name': 'Mozambique', 'flag_emoji': '🇲🇿'},
            {'name': 'Malawi', 'flag_emoji': '🇲🇼'},
            {'name': 'Angola', 'flag_emoji': '🇦🇴'},
            {'name': 'Ivory Coast', 'flag_emoji': '🇨🇮'},
            {'name': 'Mali', 'flag_emoji': '🇲🇱'},
            {'name': 'Burkina Faso', 'flag_emoji': '🇧🇫'},
            {'name': 'Niger', 'flag_emoji': '🇳🇪'},
            {'name': 'Chad', 'flag_emoji': '🇹🇩'},
            {'name': 'Sudan', 'flag_emoji': '🇸🇩'},
            {'name': 'Somalia', 'flag_emoji': '🇸🇴'},
            {'name': 'Algeria', 'flag_emoji': '🇩🇿'},
            {'name': 'Tunisia', 'flag_emoji': '🇹🇳'},
            {'name': 'Libya', 'flag_emoji': '🇱🇾'},
            {'name': 'Mauritius', 'flag_emoji': '🇲🇺'},
            {'name': 'Seychelles', 'flag_emoji': '🇸🇨'},
            {'name': 'Madagascar', 'flag_emoji': '🇲🇬'},
            {'name': 'Democratic Republic of Congo', 'flag_emoji': '🇨🇩'},
            {'name': 'Republic of Congo', 'flag_emoji': '🇨🇬'},
            {'name': 'Gabon', 'flag_emoji': '🇬🇦'},
            {'name': 'Benin', 'flag_emoji': '🇧🇯'},
            {'name': 'Togo', 'flag_emoji': '🇹🇬'},
            {'name': 'Sierra Leone', 'flag_emoji': '🇸🇱'},
            {'name': 'Liberia', 'flag_emoji': '🇱🇷'},
            {'name': 'Guinea', 'flag_emoji': '🇬🇳'},
            {'name': 'Gambia', 'flag_emoji': '🇬🇲'},
        ]

        for country_data in countries:
            country, created = Country.objects.get_or_create(
                name=country_data['name'],
                defaults={'flag_emoji': country_data['flag_emoji']}
            )
            if created:
                self.stdout.write(f'  ✓ Created: {country.name}')

        self.stdout.write(f'  Total countries: {Country.objects.count()}')

        # Seed Themes
        self.stdout.write('\nCreating themes...')
        themes = [
            'Family',
            'Identity',
            'Migration',
            'Youth',
            'Elders',
            'Resilience',
            'Loss',
            'Joy',
            'Community',
            'Home',
            'Belonging',
            'Change',
            'Education',
            'Work',
            'Love',
            'Friendship',
            'Conflict',
            'Peace',
            'Faith',
            'Nature',
            'Urban Life',
            'Rural Life',
            'Tradition vs Modernity',
            'Language',
            'Food',
            'Music',
            'Art',
            'Independence',
            'Colonialism',
            'Freedom',
        ]

        for theme_name in themes:
            theme, created = Theme.objects.get_or_create(name=theme_name)
            if created:
                self.stdout.write(f'  ✓ Created: {theme.name}')

        self.stdout.write(f'  Total themes: {Theme.objects.count()}')

        # Seed Eras
        self.stdout.write('\nCreating eras...')
        eras = [
            {
                'name': 'Pre-Colonial',
                'description': 'Before European colonization',
                'start_year': None,
                'end_year': 1800
            },
            {
                'name': 'Colonial Era',
                'description': 'Period of European colonial rule',
                'start_year': 1800,
                'end_year': 1960
            },
            {
                'name': 'Independence Era (1960s-1970s)',
                'description': 'Period of African independence movements',
                'start_year': 1960,
                'end_year': 1979
            },
            {
                'name': '1980s-1990s',
                'description': 'Post-independence challenges and transitions',
                'start_year': 1980,
                'end_year': 1999
            },
            {
                'name': '2000s-2010s',
                'description': 'Turn of the millennium',
                'start_year': 2000,
                'end_year': 2019
            },
            {
                'name': 'Contemporary (2020-Present)',
                'description': 'Present day stories',
                'start_year': 2020,
                'end_year': None
            },
        ]

        for era_data in eras:
            era, created = Era.objects.get_or_create(
                name=era_data['name'],
                defaults={
                    'description': era_data['description'],
                    'start_year': era_data['start_year'],
                    'end_year': era_data['end_year']
                }
            )
            if created:
                self.stdout.write(f'  ✓ Created: {era.name}')
            else:
                self.stdout.write(f'  - Exists: {era.name}')

        self.stdout.write('\n')
        self.stdout.write(self.style.SUCCESS('✓ Seeding complete!'))
        self.stdout.write(f'\nSummary:')
        self.stdout.write(f'  Categories: {Category.objects.count()}')
        self.stdout.write(f'  Countries: {Country.objects.count()}')
        self.stdout.write(f'  Themes: {Theme.objects.count()}')
        self.stdout.write(f'  Eras: {Era.objects.count()}')
