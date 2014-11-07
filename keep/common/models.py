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

##
## Source technical metadata
##
class _BaseSourceTech(xmlmap.XmlObject):
    'Base class for Source Technical Metadata objects'
    ROOT_NS = 'http://pid.emory.edu/ns/2010/sourcetech'
    ROOT_NAMESPACES = {'st': ROOT_NS}


class SourceTechMeasure(_BaseSourceTech):
    ''':class:`~eulxml.xmlmap.XmlObject` for :class:`SourceTech` measurement
    information'''
    ROOT_NAME = 'measure'
    unit = xmlmap.StringField('@unit')
    'unit of measurement'
    aspect = xmlmap.StringField('@aspect')
    'aspect of measurement'
    value = xmlmap.StringField('text()')
    'value (actual measurement)'

    def is_empty(self):
        '''Returns False if no measurement value is set; returns True if any
        measurement value is set.  Attributes are ignored for determining whether
        or not the field should be considered empty, since aspect & unit
        are only meaningful in reference to an actual measurement value.'''
        return not self.node.text



##
## Digital technical metadata
##
class TransferEngineer(_BaseDigitalTech):
    ''':class:`~eulxml.xmlmap.XmlObject` for :class:`DigitalTech` transfer engineer'''
    ROOT_NAME = 'transferEngineer'
    id = xmlmap.StringField('@id')
    'unique id to identify the transfer engineer'
    id_type = xmlmap.StringField('@idType')
    'type of id used'
    name = xmlmap.StringField('text()')
    'full display name for the transfer engineer'

    LDAP_ID_TYPE = 'ldap'
    DM_ID_TYPE = 'dm1'
    LOCAL_ID_TYPE = 'local'

    local_engineers = {
        'vendor1': 'Vendor',
        'other1': 'Other',
    }


class CodecCreator(_BaseDigitalTech):
    ''':class:`~eulxml.xmlmap.XmlObject` for :class:`DigitalTech` codec creator'''
    ROOT_NAME = 'codecCreator'
    configurations = {
        # current format is     id :  hardware, software, software version
        '1': (('Mac G4',), 'DigiDesign ProTools LE', '5.2'),
        '2': (('Mac G5',), 'DigiDesign ProTools LE', '6.7'),
        '3': (('Dell Optiplex 755', 'Apogee Rosetta 200'), 'Sound Forge', '9.0'),
        '4': (('Dell Optiplex 755',), 'iTunes', None),
        '5': (('Unknown',), 'Unknown',  None),
        '6': (('iMac', 'Benchmark ADC1'), 'Adobe Audition CS6', '5.0'),
        '7': (('iMac', 'Benchmark ADC1'), 'Sound Forge Pro', '1.0'),
        '8': (('iMac',), 'iTunes', None),
    }
    'controlled vocabulary for codec creator configurations'
    options = [(id, '%s, %s %s' % (', '.join(c[0]), c[1], c[2] if c[2] is not None else ''))
                    for id, c in configurations.iteritems()]
    options.insert(0, ('', ''))  # empty value at beginning of list (initial default)

    id = xmlmap.StringField('dt:codecCreatorID')
    'codec creator id - `dt:codecCreatorId`'
    hardware = xmlmap.StringField('dt:hardware')
    'hardware  - `dt:hardware` (first hardware only, even if there are multiple)'
    hardware_list = xmlmap.StringListField('dt:hardware')
    'list of all hardware'
    software = xmlmap.StringField('dt:software')
    'software  - `dt:software` (first software only, even if there are multiple)'
    software_version = xmlmap.StringField('dt:softwareVersion')
    'list of all software'