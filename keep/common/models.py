from collections import namedtuple
from django.db import models
from eulxml import xmlmap
from eulxml.xmlmap.fields import DateField

class Permissions(models.Model):
    class Meta:
        permissions = (
            ("arrangement_allowed", "Access to Arrangement material is allowed."),
            ("marbl_allowed", "Access to MARBL material is allowed."),
        )

_access_term = namedtuple('_access_term', 'code abbreviation access text') # wraps terms below

class _BaseRights(xmlmap.XmlObject):
    'Base class for Rights metadata objects'
    ROOT_NS = 'http://pid.emory.edu/ns/2010/rights'
    ROOT_NAMESPACES = { 'rt': ROOT_NS }

class AccessStatus(_BaseRights):
    ':class:`~eulxml.xmlmap.XmlObject` for :class:`Rights` access status'
    ROOT_NAME = 'accessStatus'
    code = xmlmap.StringField('@code', required=True)
    'access code'
    text = xmlmap.StringField('text()')
    'text description of rights access code'


##
## Rights
##
class Rights(_BaseRights):
    'Rights metadata'
    ROOT_NAME = 'rights'

    access_terms = (
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

    access_terms_dict = dict((term[0], _access_term(*term))
                             for term in access_terms)
    '''dictionary mapping access_terms codes to access term objects. Each
    access term object has three properties: code, abbreviation, access, and text, which
    map to elements of access_terms.'''
    # e.g., access_terms_dict['11'].access == True

    access_status = xmlmap.NodeField('rt:accessStatus', AccessStatus,
        required=True,
        help_text='File access status, as determined by analysis of copyright, donor agreements, permissions, etc.')
    ':class:`AccessStatus`'
    copyright_holder_name = xmlmap.StringField('rt:copyrightholderName',
        required=False,
        help_text='Name of a copyright holder in last, first order')
    'name of the copyright holder'
    copyright_date = xmlmap.StringField('rt:copyrightDate[@encoding="w3cdtf"]',
        required=False,
        help_text='Date of copyright')
    'copyright date (string)'
    access_restriction_expiration = xmlmap.StringField('rt:accessRestrictionExperation[@encoding="w3cdtf"]',
        required=False,
        help_text='Date of when restrictions on an item might expire')
    'access restriction expiration date (string)'

    block_external_access = xmlmap.SimpleBooleanField('rt:externalAccess',
        'deny', None,
        help_text='''DENY ACCESS to library patrons irrespective of Access Status.''')
    '''block external access. If this is True then refuse patron access to this
    item irrespective of :attr:access_status.'''
    # NOTE: users have also requested a <rt:externalAccess>allow</rt:externalAccess>
    # to allow access irrespective of access_status. when we implement
    # that, we'll probably want to incorporate it into this property and
    # rename

    ip_note = xmlmap.StringField('rt:ipNotes', required=False, verbose_name='IP Note',
        help_text='Additional information about the intellectual property rights of the associated work.')
    # NOTE: eventually should be repeatable/StringListField

    @property
    def researcher_access(self):
        '''Does this rights XML indicate that researchers should be
        allowed access to this document?'''
        if self.block_external_access:
            return False

        if not self.access_status:
            return None
        access_code = self.access_status.code
        access_term = self.access_terms_dict.get(access_code, None)
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


class FileMasterTech_Base(xmlmap.XmlObject):
    ROOT_NS = 'http://pid.emory.edu/ns/2011/filemastertech'
    ROOT_NAMESPACES = {'fs': ROOT_NS }
    ROOT_NAME = 'file'

    BROWSABLE_COMPUTERS = ('Performa 5400','Performa 5300c')

    local_id = xmlmap.StringField('fs:localId')
    md5 = xmlmap.StringField('fs:md5')
    computer = xmlmap.StringField('fs:computer')
    path = xmlmap.StringField('fs:path')
    rawpath = xmlmap.StringField('fs:rawpath')
    attributes = xmlmap.StringField('fs:attributes')
    #created = DateField('fs:created')
    #modified = DateField('fs:modified')
    created = xmlmap.StringField('fs:created')
    modified = xmlmap.StringField('fs:modified')
    type = xmlmap.StringField('fs:type')
    creator = xmlmap.StringField('fs:creator')

    def browsable(self):
        return self.computer in self.BROWSABLE_COMPUTERS

    def dir_parts(self):
        raw_parts = self.path.split('/')

        base = '/'
        # path is absolute, so raw_parts[0] is empty. skip it. also skip
        # raw_parts[-1] for special handling later
        for part in raw_parts[1:-1]:
            yield _DirPart(self.computer, base, part)
            base = base + part + '/'

    def name(self):
       return self.path.split('/')[-1]

class FileMasterTech(xmlmap.XmlObject):
    ROOT_NS = 'http://pid.emory.edu/ns/2011/filemastertech'
    ROOT_NAMESPACES = {'fs': ROOT_NS }
    ROOT_NAME = 'document'
    file = xmlmap.NodeListField("fs:file", FileMasterTech_Base,
    required=False)