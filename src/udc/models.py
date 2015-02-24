from lxml import etree

from django.db import models
from django.conf import settings
from django.utils.translation import ugettext_lazy as _


class Concept(models.Model):
    lang = models.CharField(max_length=2, choices=settings.LANGUAGES, verbose_name=_(u'Language'), db_index=True)
    about = models.URLField()
    notation = models.CharField(max_length=32)
    broader = models.URLField()
    related = models.TextField(default='')

    label = models.TextField()
    notes = models.TextField(default='')

    class Meta:
        unique_together = [('lang', 'about'), ('lang', 'notation')]
        ordering = ['notation']

    def __unicode__(self):
        return u'%s %s' % (self.notation, self.label)

    @classmethod
    def load(cls, source_file):
        f = open(source_file, 'r')
        doc = etree.parse(f)
        f.close()
        r = doc.getroot()
        nsmap = dict(r.nsmap)
        nsmap['xml'] = 'http://www.w3.org/XML/1998/namespace'

        for concept in doc.iterfind('skos:Concept', namespaces=nsmap):
            about = concept.attrib['{%(rdf)s}about' % nsmap]
            broader_node = concept.find('skos:broader', namespaces=nsmap)
            if broader_node:
                broader = broader_node.attrib['{%(rdf)s}resource' % nsmap]
            else:
                broader = ''
            notation = concept.find('skos:notation', namespaces=nsmap).text

            related = []
            for rel in concept.iterfind('skos:related', namespaces=nsmap):
                related.append(rel.attrib['{%(rdf)s}resource' % nsmap])

            for lang, lang_name in settings.LANGUAGES:
                kwargs = {
                    'broader': broader,
                    'notation': notation,
                    'related': u'\n'.join(related),
                    'label': '',
                }

                for label_node in concept.iterfind('skos:prefLabel', namespaces=nsmap):
                    if lang == label_node.attrib['{%(xml)s}lang' % nsmap]:
                        kwargs['label'] = label_node.text

                notes = []
                for tagname in ('scopeNote', 'appicationNote', 'includingNote'):
                    for node in concept.iterfind('skos:' + tagname, namespaces=nsmap):
                        if lang == node.attrib['{%(xml)s}lang' % nsmap]:
                            notes.append(node.text)
                kwargs['notes'] = u'\n'.join(notes)

                try:
                    obj = Concept.objects.get(lang=lang, about=about)
                except Concept.DoesNotExist:
                    Concept.objects.create(lang=lang, about=about, **kwargs)
                else:
                    Concept.objects.filter(id=obj.id).update(**kwargs)
