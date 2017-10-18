from django.db import models
from django.core.urlresolvers import reverse
from django.utils.text import slugify
import itertools

# Create your models here.

class Evenement(models.Model):
    naam = models.CharField(max_length=200)
    intro = models.CharField(max_length=2000, blank=True)
    omschrijving = models.TextField()
    start_datum = models.DateField()
    einde_datum = models.DateField(blank=True, null=True)
    slug = models.SlugField(unique=True)
    def __str__(self):
        return self.naam
    def get_absolute_url(self):
        return reverse('evenementen:evenement_overzicht', args=(self.slug,))
    def save(self, *args, **kwargs):
        if not self.pk:
            max_length = Evenement._meta.get_field('slug').max_length
            self.slug = orig = slugify(self.naam)[:max_length]
            for x in itertools.count(1):
                if not Evenement.objects.filter(slug=self.slug).exists():
                    break
                self.slug = "%s-%d" % (orig[:max_length - len(str(x)) - 1], x)
        super(Evenement, self).save(*args, **kwargs) # Call the "real" save() method.

class Aanmelding(models.Model):
    evenement = models.ForeignKey(Evenement, on_delete=models.CASCADE)
    voornaam = models.CharField(max_length=200)
    achternaam = models.CharField(max_length=200)