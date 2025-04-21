from rest_framework.test import APITestCase
from rest_framework import status
from registry.models import Animal
from django.urls import reverse
from datetime import date

class SetParentsTestCase(APITestCase):
    def setUp(self):
        self.father = Animal.objects.create(
            name="Rex", species="dog", breed="Labrador", birth_date=date(2015, 6, 1)
        )
        self.mother = Animal.objects.create(
            name="Luna", species="dog", breed="Poodle", birth_date=date(2016, 8, 15)
        )
        self.child = Animal.objects.create(
            name="Max", species="dog", breed="Mixed", birth_date=date(2022, 1, 10)
        )

    def test_set_parents_successfully(self):
        url = reverse('animal-set-parents', kwargs={'pk': self.child.id})
        response = self.client.patch(url, {
            'father': self.father.id,
            'mother': self.mother.id
        }, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['father']['id'], self.father.id)
        self.assertEqual(response.data['mother']['id'], self.mother.id)

    def test_set_parents_invalid_father(self):
        url = reverse('animal-set-parents', kwargs={'pk': self.child.id})
        response = self.client.patch(url, {
            'father': 9999
        }, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('error', response.data)

    def test_set_parents_only_mother(self):
        url = reverse('animal-set-parents', kwargs={'pk': self.child.id})
        response = self.client.patch(url, {
            'mother': self.mother.id
        }, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIsNotNone(response.data['mother'])
        self.assertIsNone(response.data['father'])

    def test_clear_parents(self):
        self.child.father = self.father
        self.child.mother = self.mother
        self.child.save()
        url = reverse('animal-set-parents', kwargs={'pk': self.child.id})
        response = self.client.patch(url, {
            'father': None,
            'mother': None
        }, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIsNone(response.data['father'])
        self.assertIsNone(response.data['mother'])

class AnimalTreeTestCase(APITestCase):
    def setUp(self):
        self.grandfather = Animal.objects.create(
            name="Maximus", species="dog", breed="Bulldog", birth_date=date(2010, 5, 5)
        )
        self.grandmother = Animal.objects.create(
            name="Bella", species="dog", breed="Beagle", birth_date=date(2012, 7, 15)
        )
        self.father = Animal.objects.create(
            name="Rex", species="dog", breed="Labrador", birth_date=date(2015, 6, 1),
            father=self.grandfather, mother=self.grandmother
        )
        self.mother = Animal.objects.create(
            name="Luna", species="dog", breed="Poodle", birth_date=date(2016, 8, 15)
        )
        self.child = Animal.objects.create(
            name="Max", species="dog", breed="Mixed", birth_date=date(2022, 1, 10),
            father=self.father, mother=self.mother
        )

    def test_ancestors(self):
        url = reverse('animal-tree', kwargs={'pk': self.child.id})
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('ancestors', response.data)
        ancestor_names = [a['name'] for a in response.data['ancestors']]
        self.assertIn('Rex', ancestor_names)
        self.assertIn('Luna', ancestor_names)
        self.assertIn('Maximus', ancestor_names)
        self.assertIn('Bella', ancestor_names)

    def test_descendants(self):
        url = reverse('animal-descendants', kwargs={'pk': self.grandfather.id})
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('descendants', response.data)
        descendant_names = [d['name'] for d in response.data['descendants']]
        self.assertIn('Rex', descendant_names)
        self.assertIn('Max', descendant_names)

class AnimalSearchTestCase(APITestCase):
    def setUp(self):
        self.animal1 = Animal.objects.create(
            name="Rex", species="dog", breed="Labrador", birth_date=date(2020, 5, 1)
        )
        self.animal2 = Animal.objects.create(
            name="Luna", species="cat", breed="Persian", birth_date=date(2021, 3, 15)
        )

    def test_search_by_species(self):
        url = reverse('animal-search-list')
        response = self.client.get(url, {'species': 'dog'})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data['results']), 1)
        self.assertEqual(response.data['results'][0]['name'], 'Rex')

    def test_pagination(self):
        url = reverse('animal-search-list')
        response = self.client.get(url)
        self.assertIn('results', response.data)
        self.assertIn('count', response.data)
        self.assertIn('next', response.data)
        self.assertIn('previous', response.data)