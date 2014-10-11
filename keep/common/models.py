from collections import namedtuple
from django.db import models
from eulxml import xmlmap
from eulxml.xmlmap import premis


class Permissions(models.Model):
    class Meta:
        permissions = (
            ("arrangement_allowed", "Access to Arrangement material is allowed."),
            ("marbl_allowed", "Access to MARBL material is allowed."),
        )

_access_term = namedtuple('_access_term', 'code abbreviation access text') # wraps terms below

rights_access_terms =  (
    # code  abbreviation                     file access allowed?        (full description next line)
    ('1', 'C108-a donor request',              False,     # metadata ok
     'Material under copyright; digital copy made under Section 108a, per donor/ copyright holder request'),
    ('2', 'C108-b or c',                       True,
     'Material under copyright; digital copy made under Section 108b or c; no explicit contract restrictions in the donor agreement'),
    ('3', 'C108-b or c + MARBL use',           True,
     'Material under copyright; digital copy made under Section 108b or c; permission received from copyright holder for Emory University Libraries to use digitized copy in public display, exhibition, etc.'),
    ('4', 'C108-b or c + donor restriction',   False,
     'Material under copyright; digital copy made under Section 108b or c; restriction on item per donor agreement'),
    ('5', 'C108-b or c + Emory Restriction',   False,
     'Material under copyright; digital copy made under Section 108b or c; restriction on item per Emory University Libraries'),
    ('6', 'C held Emory U',                    True,
     'Material under copyright; Emory University holds copyright'),
    ('7', 'C trans to Emory U',                True,
     'Material under copyright; copyright transferred to Emory University'),
    ('8', 'Public Domain',                     True,
     'Material is in public domain'),
    ('9', 'PD - Restricted by Donor or MARBL', False,
     'Material is in public domain; restriction on item per a non-copyright reason in the donor agreement or by Emory University Libraries'),
    ('10', 'Undetermined',                     False,     # metadata ok
     'Access status undetermined'),
    ('11', 'Unknown from Old DM',              True,
     'Material from previous Digital Masters database that cannot be mapped to other codes'),
    ('12', 'Redacted file only',              False,
     'Object must undergo select redaction then modified version of object available to researchers'),
    ('13', 'Metadata only',              False,
     'Only meta data is available'),
    )
'''controlled vocabulary for access condition, ordered the way they should
appear on the form widget'''

rights_access_terms_dict = dict((term[0], _access_term(*term))
                                for term in rights_access_terms)
'''dictionary mapping access_terms codes to access term objects. Each
access term object has three properties: code, abbreviation, access, and text, which
map to elements of access_terms.'''
# e.g., access_terms_dict['11'].access == True

def allow_researcher_access(rts):
    '''
    Check if rights XML indicate that researchers should be
    allowed access to this document.'''
    if rts.block_external_access:
            return False

    if not rts.access_status:
        return None
    access_code = rts.access_status.code
    access_term = rights_access_terms_dict.get(access_code, None)
    if not access_term:
        return None
        
    return access_term.access

class _DirPart(object):
    # a _DirPart wraps around a single path component in a file path so that
    # we can treat that component as an object in its own right.
    def __init__(self, computer, base, name):
        self.computer = computer
        self.base = base
        self.name = name

    def __unicode__(self):
        return self.name

    def path(self):
        return '/' + self.computer + self.base + self.name + '/'


class _BaseDigitalTech(xmlmap.XmlObject):
    'Base class for Digital Technical Metadata objects'
    ROOT_NS = 'http://pid.emory.edu/ns/2010/digitaltech'
    ROOT_NAMESPACES = {'dt': ROOT_NS}


class PremisFixity(premis.BasePremis):
    ROOT_NAME = 'fixity'
    algorithm = xmlmap.StringField('p:messageDigestAlgorithm')
    digest = xmlmap.StringField('p:messageDigest')


class PremisObjectFormat(premis.BasePremis):
    ROOT_NAME = 'format'
    name = xmlmap.StringField('p:formatDesignation/p:formatName')
    version = xmlmap.StringField('p:formatDesignation/p:formatVersion')


class PremisCreatingApplication(premis.BasePremis):
    ROOT_NAME = 'creatingApplication'
    name = xmlmap.StringField('p:creatingApplicationName')
    version = xmlmap.StringField('p:creatingApplicationVersion')
    date = xmlmap.DateField('p:dateCreatedByApplication')


class PremisSoftwareEnvironment(premis.BasePremis):
    ROOT_NAME = 'software'
    name = xmlmap.StringField('p:swName',
        help_text='Name of the software in original environment')
    version = xmlmap.StringField('p:swVersion',
        help_text='Software version')
    type = xmlmap.StringField('p:swType', help_text='Type of software')

hardware_types = ('personal computer', 'personal computer/laptop',
    'external drive', 'removable media', 'word processor')


class PremisHardwareEnvironment(premis.BasePremis):
    ROOT_NAME = 'hardware'
    name = xmlmap.StringField('p:hwName', help_text='Name of original hardware')
    type = xmlmap.StringField('p:hwType', choices=hardware_types,
        help_text='Type of hardware')
    other_information = xmlmap.StringField('p:hwOtherInformation',
        help_text='Other information about the original environment (e.g. original disk label)')


class PremisEnvironment(premis.BasePremis):
    ROOT_NAME = 'environment'
    note = xmlmap.StringField('p:environmentNote')
    # NOTE: both hardware and software could be repeated;
    # for simplicity, onyl mapping one for disk images, for now
    software = xmlmap.NodeField('p:software', PremisSoftwareEnvironment)
    hardware = xmlmap.NodeField('p:hardware', PremisHardwareEnvironment)


class PremisObject(premis.Object):
    composition_level = xmlmap.IntegerField('p:objectCharacteristics/p:compositionLevel')
    checksums = xmlmap.NodeListField('p:objectCharacteristics/p:fixity',
                                     PremisFixity)
    format = xmlmap.NodeField('p:objectCharacteristics/p:format',
                              PremisObjectFormat)
    creating_application = xmlmap.NodeField('p:objectCharacteristics/p:creatingApplication',
                                            PremisCreatingApplication)
    original_environment = xmlmap.NodeField('p:environment[p:environmentNote="Original environment"]',
                                            PremisEnvironment)