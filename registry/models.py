from django.db import models
from django.core.exceptions import ValidationError
from datetime import date

class Owner(models.Model):
    name = models.CharField(max_length=100)
    phone = models.CharField(max_length=20, blank=True)
    email = models.EmailField(blank=True)

    def __str__(self):
        return self.name

class Animal(models.Model):
    SPECIES_CHOICES = [
        ('dog', 'Cão'),
        ('cat', 'Gato'),
        ('bird', 'Pássaro'),
    ]

    name = models.CharField(max_length=100)
    species = models.CharField(max_length=20, choices=SPECIES_CHOICES)
    breed = models.CharField(max_length=100, blank=True, null=True)
    birth_date = models.DateField(null=False)
    registration_date = models.DateField(auto_now_add=True, null=False)
    owners = models.ManyToManyField(Owner, related_name='animals')
    father = models.ForeignKey('self', null=True, blank=True, related_name='offspring_father', on_delete=models.SET_NULL)
    mother = models.ForeignKey('self', null=True, blank=True, related_name='offspring_mother', on_delete=models.SET_NULL)

    class Meta:
        indexes = [
            models.Index(fields=['species']),
            models.Index(fields=['breed']),
            models.Index(fields=['registration_date']),
            models.Index(fields=['father']),
            models.Index(fields=['mother']),
        ]

    def __str__(self):
        return self.name

    def clean(self):
        # Valida espécie dos pais
        if self.father and self.father.species != self.species:
            raise ValidationError("O pai deve ser da mesma espécie.")
        if self.mother and self.mother.species != self.species:
            raise ValidationError("A mãe deve ser da mesma espécie.")
        # Valida idade dos pais
        if self.father and self.father.birth_date > self.birth_date:
            raise ValidationError("O pai não pode ser mais jovem que o filho.")
        if self.mother and self.mother.birth_date > self.birth_date:
            raise ValidationError("A mãe não pode ser mais jovem que o filho.")
        # Evita ciclos
        def check_cycle(animal, parent):
            if not parent:
                return
            if parent == animal:
                raise ValidationError("Ciclo detectado: um animal não pode ser seu próprio ancestral.")
            check_cycle(animal, parent.father)
            check_cycle(animal, parent.mother)
        check_cycle(self, self.father)
        check_cycle(self, self.mother)

    def save(self, *args, **kwargs):
        self.clean()
        super().save(*args, **kwargs)

    def calculate_age(self):
        today = date.today()
        if self.birth_date > today:
            raise ValueError("Data de nascimento não pode ser no futuro.")
        return today.year - self.birth_date.year - (
            (today.month, today.day) < (self.birth_date.month, self.birth_date.day)
        )

    def get_ancestors(self):
        ancestors = []
        to_process = [self]
        seen = set()

        while to_process:
            current = to_process.pop()
            if current.id in seen:
                continue
            seen.add(current.id)
            if current.father:
                ancestors.append(current.father)
                to_process.append(current.father)
            if current.mother:
                ancestors.append(current.mother)
                to_process.append(current.mother)

        return Animal.objects.filter(id__in=[a.id for a in ancestors]).select_related('father', 'mother')

    def get_descendants(self):
        descendants = []
        to_process = [self]
        seen = set()

        while to_process:
            current = to_process.pop()
            if current.id in seen:
                continue
            seen.add(current.id)
            children = list(current.offspring_father.all()) + list(current.offspring_mother.all())
            descendants.extend(children)
            to_process.extend(children)

        return Animal.objects.filter(id__in=[d.id for d in descendants]).select_related('father', 'mother')

    def get_tree_depth(self):
        def max_depth(animal, seen=None):
            if seen is None:
                seen = set()
            if not animal or animal.id in seen:
                return 0
            seen.add(animal.id)
            father_depth = max_depth(animal.father, seen) if animal.father else 0
            mother_depth = max_depth(animal.mother, seen) if animal.mother else 0
            return max(father_depth, mother_depth) + 1
        return max_depth(self) - 1