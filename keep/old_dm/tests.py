from django.conf import settings

from keep.collection.fixtures import FedoraFixtures
from keep import mods
from keep.collection.models import CollectionObject
from keep.old_dm import models
from keep.testutil import KeepTestCase

class LocationTest(KeepTestCase):
    marbl = models.Location(name='MARBL, Robert W. Woodruff Library, Emory University')
    eua_woodruff = models.Location(name='Emory Archives: Robert W. Woodruff Library')
    eua_healthsci = models.Location(name='Emory Archives: Woodruff Health Sciences Library')
    pitts = models.Location(name='Pitts Theology Library')
    business = models.Location(name='Goizueta Business Library')
    oxford = models.Location(name="Hoke O'Kelley Memorial Library, Oxford College")

    def setUp(self):
        # convert fixture objects into short-hand versions so we an easily identify them
        for obj in CollectionObject.top_level():
            if obj.label == 'Manuscript, Archives, and Rare Book Library':
                self.marbl_obj = obj
            elif obj.label == 'Emory University Archives':
                self.eua_obj = obj
            elif obj.label == 'Pitts Theology Library':
                self.pitts_obj = obj
            elif obj.label == "Hoke O'Kelley Memorial Library, Oxford College":
                self.oxford_obj = obj

    def test_corresponding_repository(self):
        self.assertEqual(self.marbl_obj.uri, self.marbl.corresponding_repository,
                         'MARBL location should correspond to MARBL Repository object')
        self.assertEqual(self.eua_obj.uri, self.eua_woodruff.corresponding_repository,
                         'EUA Woodruff location should correspond to EUA Repository Object')
        self.assertEqual(self.eua_obj.uri, self.eua_healthsci.corresponding_repository,
                         'EUA Health/Sci location should correspond to EUA Repository Object')
        self.assertEqual(self.pitts_obj.uri, self.pitts.corresponding_repository,
                         'Pitts location should correspond to Pitts Repository Object')
        self.assertEqual(self.oxford_obj.uri, self.oxford.corresponding_repository,
                         'Oxford location should correspond to Oxford Repository Object')
        self.assertEqual(None, self.business.corresponding_repository,
                         'Business library should return `None` for corresponding repository (none defined)')


class HousingTest(KeepTestCase):

    expected_values = {
        'Moving Image/Sound/Still Image: None': 'none',
        'Moving Image/Sound/Still Image: Other': 'other',
        'Moving Image/Sound/Still Image: Mixed': 'other',
        'Moving Image/Sound: Jewel case': 'jewel case',
        'Moving Image/Sound: Extended/Amaray case': 'jewel case',
        'Moving Image/Sound: Slimline case': 'jewel case',
        'Moving Image/Sound: Plastic container': 'plastic container',
        'Moving Image/Sound: Archival box': 'cardboard box',
        'Moving Image/Sound: Non archival box': 'cardboard box',
        'Moving Image/Sound: Core and archival paper boxes': 'cardboard box',
        'Moving Image/Sound: Tyvek sleeve': 'paper sleeve',
        'Moving Image/Sound: Paper sleeve': 'paper sleeve',
        'Moving Image/Sound: Paper jewel case': 'paper sleeve',
    }

    def test_as_sourcetech_housing(self):
        for old_housing, keep_housing in self.expected_values.iteritems():
            housing = models.Housing(description=old_housing)
            result = housing.as_sourcetech_housing()
            self.assertEqual(keep_housing, result,
                "old_dm housing '%s' should be converted to '%s', but got '%s'" \
                %(housing.description, keep_housing, result))

class FormTest(KeepTestCase):
    expected_values = {
        'Sound - acetate vinyl shellac - 45 rpm': '45 RPM',
        'Sound - glass disc': 'glass disc',
        'Sound - audiocassette': 'audio cassette',
        'Sound - DAT': 'DAT',
        'Sound - acetate vinyl shellac - 78 rpm': '78',
        'Sound - flexidisc': 'flexi disc',
        'Sound - cardboard disc': 'cardboard disc',
        'Sound - acetate vinyl shellac - 33.3 rpm': 'LP',
        'Sound - paper roll': 'other',
        'Sound - MP3': 'sound file (MP3)',
        'Sound - other disc': 'other',
        'Sound - CD': 'CD',
        'Sound - colored plastic disc': 'other',
        'Sound - open reel': 'open reel tape',
        'Sound - other': 'other',
        'Sound - aluminum disc': 'aluminum disc',
    }

    def test_as_sourcetech_form(self):
        for old_form, keep_form in self.expected_values.iteritems():
            form = models.Form(form=old_form)
            result = form.as_sourcetech_form()
            self.assertEqual(keep_form, result,
                "old_dm form '%s' should be converted to '%s', but got '%s'" \
                %(old_form, keep_form, result))

class SpeedTest(KeepTestCase):
    speed_alt_unit = {
        '7.5 ips, 19.05 cm/s': 'inches/sec',
        '30 ips, 76.2cm/s': 'inches/sec',
        '15/16 ips, 2.38 cm/s': 'inches/sec',
        '120 rpm': 'rpm',
        '3 3/4 ips, 9.5 cm/s': 'inches/sec',
        '48 Kilohertz': 'Kilohertz',
        '1 7/8 ips, 4.75 cm/s': 'inches/sec',
        '78 rpm': 'rpm',
        '33 1/3 rpm': 'rpm',
        'Multiple': 'multiple',
        '15/32 ips, 1.19 cm/s': 'inches/sec',
        'Other': 'other',
        '15 ips, 38.1 cm/s': 'inches/sec',
        '45 rpm': 'rpm',
        '44.1 Kilohertz': 'Kilohertz',
    }

    # a few test cases for speeds and expected aspect
    speed_aspects = {
        '15/16 inches/sec': 'tape',
        '16 rpm': 'phono disc',
        '120 rpm': 'phono cylinder',
        'O Other': 'other',  # db has O for speed, other for speed_alt
    }

    def test_unit(self):
        for speed_alt, unit in self.speed_alt_unit.iteritems():
            sp = models.Speed(speed_alt=speed_alt)
            self.assertEqual(unit, sp.unit,
                "old_dm speed_alt value '%s' should result in unit of '%s', got '%s'" % \
                (speed_alt, unit, sp.unit))

    def test_aspect(self):
        for speed, aspect in self.speed_aspects.iteritems():
            val, sep, unit = speed.rpartition(' ')
            if unit == 'inches/sec':
                unit = 'ips'
            sp = models.Speed(speed=val, speed_alt=unit)
            self.assertEqual(aspect, sp.aspect,
                'expected aspect of %s, got %s for speed %s' % (aspect, sp.aspect, speed))

class StaffNameTest(KeepTestCase):
    fixtures =  ['ldap_user']

    def test_transfer_engineer(self):
        # user loaded to db from fixture
        testname = 'John Doe'
        staff = models.StaffName(name=testname)
        name, id, idtype = staff.as_transfer_engineer()
        self.assertEqual(testname, name)
        self.assertEqual('jdoe', id)
        self.assertEqual('ldap', idtype)

        testname = 'Nobody Particular'
        testid = 3
        staff = models.StaffName(name=testname, id=testid)
        name, id, idtype = staff.as_transfer_engineer()
        self.assertEqual(testname, name)
        self.assertEqual(testid, id)
        self.assertEqual('dm1', idtype)

class AccessRights(KeepTestCase):

    def test_w3cdft_copyright_date(self):
        access = models.AccessRights(copyright_date='0000-00-00')
        self.assertEqual(None, access.w3cdtf_copyright_date())
        access = models.AccessRights(copyright_date='1984-00-00')
        self.assertEqual('1984', access.w3cdtf_copyright_date())
        access = models.AccessRights(copyright_date='2001-01-00')
        self.assertEqual('2001-01', access.w3cdtf_copyright_date())


class Authority(KeepTestCase):

    def test_unicode(self):
        authority = models.Authority(authority='lcsh')
        self.assertEqual('lcshstring', unicode(authority))

        authority = models.Authority(authority='naf')
        self.assertEqual('nafstring', unicode(authority))

        authority = models.Authority(authority='somethingElse')
        self.assertEqual('somethingElse', unicode(authority))

#Should this be moved somewhere else?
class Mods(KeepTestCase):

    def test_dates(self):
        recInfo = mods.RecordInfo(creation_date='1976-05-11')
        self.assertTrue('encoding="w3cdtf"' in recInfo.serialize())

        recInfo = mods.RecordInfo(change_date='2011-07-20')
        self.assertTrue('encoding="w3cdtf"' in recInfo.serialize())