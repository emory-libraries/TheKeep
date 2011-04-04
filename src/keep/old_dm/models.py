# This is an auto-generated Django model module.
# You'll have to do the following manually to clean this up:
#     * Rearrange models' order
#     * Make sure each model has one field with primary_key=True
# Feel free to rename the models, but don't rename db_table values or field names.
#
# Also note: You'll have to insert the output of 'django-admin.py sqlcustom [appname]'
# into your database.

from django.db import models

from keep.collection.models import CollectionObject

# referenced collections that are not available in Fedora
MISSING_COLLECTIONS = {}
# items with no collection or series specified
ITEMS_WITHOUT_COLLECTION = []

class ResourceType(models.Model):
    id = models.IntegerField(primary_key=True)
    type = models.CharField(max_length=100, db_column='resource_type')
    class Meta:
        db_table = u'resource_types'
        managed = False

    def __unicode__(self):
        return self.type

class StaffName(models.Model):
    id = models.IntegerField(primary_key=True)
    name = models.CharField(max_length=100)
    class Meta:
        db_table = u'staff_names'
        managed = False

    def __unicode__(self):
        return self.name


class Authority(models.Model):
    id = models.IntegerField(primary_key=True)
    authority = models.CharField(max_length=255)
    class Meta:
        db_table = u'authorities'
        managed = False

    def __unicode__(self):
        return self.authority

class Genre(models.Model):
    id = models.IntegerField(primary_key=True)
    genre = models.CharField(max_length=255)
    authority = models.ForeignKey(Authority)
    fieldnames = models.IntegerField()
    class Meta:
        db_table = u'genres'
        managed = False

    def __unicode__(self):
        return '%s [authority = %s, field = %d]' % (self.genre, self.authority.authority, self.fieldnames)

class Name(models.Model):
    id = models.IntegerField(primary_key=True)
    name = models.CharField(unique=True, max_length=255)
    authority = models.ForeignKey(Authority)
    name_type = models.CharField(max_length=50)
    class Meta:
        db_table = u'names'
        managed = False

    def __unicode__(self):
        return '%s [%s, authority=%s]' % (self.name, self.name_type, self.authority.authority)

class Role(models.Model):
    id = models.IntegerField(primary_key=True)
    title = models.CharField(max_length=255)
    code = models.CharField(max_length=255)
    class Meta:
        db_table = u'roles'
        managed = False

    def __unicode__(self):
        return '%s [%s]' % (self.title, self.code)

class Language(models.Model):
    id = models.IntegerField(primary_key=True)
    language = models.CharField(max_length=255)
    code = models.CharField(max_length=255)
    class Meta:
        db_table = u'languages'
        managed = False

    def __unicode__(self):
        return '%s [%s]' % (self.language, self.code)

# map old DM locations to Keep top-level collection/owning repository objects
REPOSITORY_LOCATION = {}

class Location(models.Model):
    id = models.IntegerField(primary_key=True)
    name = models.CharField(max_length=100)
    address = models.CharField(max_length=255)
    phone = models.CharField(max_length=50)
    fax = models.CharField(max_length=50)
    email = models.CharField(max_length=50)
    url = models.URLField()
    city = models.CharField(max_length=100)
    state = models.CharField(max_length=2)
    zip = models.CharField(max_length=10)
    class Meta:
        db_table = u'locations'
        managed = False

    @property
    def corresponding_repository(self):
        global REPOSITORY_LOCATION
        # if this location has not yet been mapped to a repository object, look it up
        if self.name not in REPOSITORY_LOCATION:
            repos = CollectionObject.top_level()
            for repo in repos:
                # translate DM location labels to Keep repository object labels
                if (self.name.startswith('Emory Archives') and repo.label == 'Emory University Archives') or \
                   (self.name.startswith('MARBL') and repo.label == 'Manuscript, Archives, and Rare Book Library'):
                    REPOSITORY_LOCATION[self.name] = repo.uri
                    break

        return REPOSITORY_LOCATION[self.name]

class Subject(models.Model):
    subject = models.CharField(max_length=255)
    id = models.IntegerField(primary_key=True)
    authority = models.ForeignKey(Authority)
    fieldnames = models.IntegerField()

    # fieldname codes for type of subject
    geographic = 651
    name_personal = 600
    name_corporate = 610
    name_conference = 611
    topic = 650
    title = 630

    class Meta:
        db_table = u'subjects'
        managed = False

    def __unicode__(self):
        return '%s [authority = %s, field %s]' % (self.subject, self.authority.authority, self.fieldnames)

class AudioContentManager(models.Manager):
    # custom manager to find audio items only, using resource type
    def get_query_set(self):
        # filter on resource type: starting with sound recording, will also match musical & nonmusical variant types
        return super(AudioContentManager, self).get_query_set().filter(resource_type__type__startswith='sound recording')

class Content(models.Model):   # individual item
    id = models.IntegerField(primary_key=True)
    record_id_type = models.CharField(max_length=50)
    other_id = models.CharField(max_length=255)
    created_at = models.DateTimeField()
    modified_at = models.DateTimeField()
    collection_number = models.IntegerField()
    title = models.CharField(max_length=255)
    subtitle = models.CharField(max_length=255)
    resource_type = models.ForeignKey(ResourceType)
    location = models.ForeignKey(Location)
    abstract = models.TextField()
    toc = models.TextField()
    note = models.TextField(db_column='content_notes')
    completed_by = models.IntegerField()
    completed_date = models.DateTimeField()
    data_entered_by = models.ForeignKey(StaffName, db_column='data_entered_by',
                                        related_name='entered_data', null=True)
    data_entered_date = models.DateTimeField()
    authority_work_by = models.ForeignKey(StaffName, db_column='authority_work_by',
                                          related_name='authority_work', null=True)
    authority_work_date = models.DateTimeField()
    initial_qc_by = models.ForeignKey(StaffName, db_column='initial_qc_by',
                                      related_name='quality_control', null=True)
    initial_qc_date = models.DateTimeField()

    # source_sounds (one to many; most items seem to have 0 or 1)
    genres = models.ManyToManyField(Genre)
    names = models.ManyToManyField(Name, through='NameRole')
    languages = models.ManyToManyField(Language)
    subjects = models.ManyToManyField(Subject)

    # eua_series reverse relation is available, defined on EuarchivesSeries class
    @property
    def series_number(self):
        # there should only ever be one series; not defining as one-to-one because not all contents will have a series
        if self.eua_series.count():
            return self.eua_series.all()[0].series

    @property
    def collection(self):
        'Manuscript or Series number in printable/displayable format, with MARBL/EUA designation'
        if self.collection_number:
            return 'MARBL %d' % self.collection_number
        elif self.series_number:
            return 'EUA %d' % self.series_number

    @property
    def collection_object(self):
        'Fedora Collection object corresponding to the collection or series number and location for this item'
        num = None
        if self.collection_number:
            num = self.collection_number
        elif self.series_number:
            num = self.series_number

        if num and self.location:
            coll = list(CollectionObject.find_by_collection_number(num, self.location.corresponding_repository))
            # if we have one and only one match, we have found the correct object
            if len(coll) == 1:
                return coll[0]

        return None

    # default manager & custom audio-only manager
    objects = models.Manager()
    audio_objects = AudioContentManager()

    class Meta:
        db_table = u'contents'
        managed = False

    def __unicode__(self):
        return '%s' % self.id

    # list of fields that will be returned by descriptive_metadata method 
    descriptive_fields = ['Collection', 'ID', 'Other ID', 'Title', 'Note', 'Type of Resource', 'Record Origin',
                          'Genre', 'Name', 'Language', 'Location', 'Subjects - Geographic',
                          'Subject - Name (personal)', 'Subject - Name (corporate)', 'Subject - Name (conference)',
                          'Subject Topic', 'Subject Title', 'Record Changed', 'Record Created']

    def descriptive_metadata(self):
        global MISSING_COLLECTIONS

        # print out descriptive fields and return a list of values
        print '--- Descriptive Metadata ---'
        print 'Collection: %s' % self.collection

        # warn if no collection number could be found (either EUA or MARBL)
        if self.collection is None:
            ITEMS_WITHOUT_COLLECTION.append(self.id)

        # if there is a collection number, warn if the corresponding collection object could not be found
        elif self.collection_object is None:
            if self.collection not in MISSING_COLLECTIONS:
                MISSING_COLLECTIONS[self.collection] = 1
            else:
                MISSING_COLLECTIONS[self.collection] += 1

        print 'Identifier: %s' % self.id
        print 'Other ID: %s' % self.other_id
        data = [self.collection, self.id, self.other_id]
        # source_sound could be multiple; which one do we use?
        for source_sound in self.source_sounds.all():
            print 'Item Date Created: %s' % source_sound.source_date
            print 'Item Date Issued: %s' % source_sound.publication_date
        print 'Item Title: %s' % unicode(self.title)
        print 'Item Note: %s' % self.note
        print 'Item Type of Resource: %s' % self.resource_type.type
        data.extend([unicode(self.title), self.note, self.resource_type.type])

        if self.data_entered_by:
            print 'Item recordOrigin: %s' % self.data_entered_by.name
            data.append(self.data_entered_by.name)
        else:
            data.append(None)

        for genre in self.genres.all():
            print 'Item Genre: %s' % unicode(genre)
        data.append('\n'.join(unicode(genre) for genre in self.genres.all()))

        for namerole in self.namerole_set.all():
            print 'Item Name (Creator): %s' % unicode(namerole.name)
            print "Item Name Role: %s" % namerole.role
        data.append('\n'.join('%s (%s)' % (unicode(namerole.name), namerole.role)  
                        for namerole in self.namerole_set.all()))

        for lang in self.languages.all():
            print 'Item Language: %s' % unicode(lang)
        data.append('\n'.join(unicode(lang) for lang in self.languages.all()))

        print 'Item Physical Location: %s' % self.location.name
        data.append(self.location.name)
        # NOTE: documentation has locations:location as db field, which does not exist

        # subjects are filtered into type of subject by field name codes
        geographic_subjects = self.subjects.filter(fieldnames=Subject.geographic)
        for subject in geographic_subjects:
            print 'Item Subject Geographic: %s' % unicode(subject)
        person_name_subjects = self.subjects.filter(fieldnames=Subject.name_personal)
        for subject in person_name_subjects:
            print 'Item Subject Name (personal): %s' % unicode(subject)
        corp_name_subjects = self.subjects.filter(fieldnames=Subject.name_corporate)
        for subject in corp_name_subjects:
            print 'Item Subject Name (corporate): %s' % unicode(subject)
        conf_name_subjects = self.subjects.filter(fieldnames=Subject.name_conference)
        for subject in conf_name_subjects:
            print 'Item Subject Name (conference): %s' % unicode(subject)
        topic_subjects = self.subjects.filter(fieldnames=Subject.topic)
        for subject in topic_subjects:
            print 'Item Subject Topic: %s' % unicode(subject)
        title_subjects = self.subjects.filter(fieldnames=Subject.title)
        for subject in title_subjects:
            print 'Item Subject Title: %s' % unicode(subject)
        for subject_group in [geographic_subjects, person_name_subjects, corp_name_subjects, conf_name_subjects,
                              topic_subjects, title_subjects]:
            data.append('\n'.join(unicode(subj) for subj in subject_group))

        data.extend([self.modified_at, self.created_at])
        print 'Item recordChangeDate: %s' % self.modified_at
        print 'Item recordCreationDate: %s' % self.created_at

        return data
        
    # fields returned by source_tech_metadata_method
    source_tech_fields = ['Note - General', 'Note - Related Files',
                          'Note - Conservation History', 'Speed',
                          'Item Sub-Location', 'Item Form',
                          'Sound Characteristics', 'Tape - Brand/Stock',
                          'Tape - Housing', 'Tape - Reel Size']

    def source_tech_metadata(self):
        print '--- Source Technical Metadata ---'
        data = []

        # XXX since source_sound is repeatable, check all fields'
        # repeatability in tech metadata spec

        # we'll be using this a lot below
        sounds = list(self.source_sounds.all())

        notes = [ s.source_note for s in sounds
                  if s.source_note ] + \
                [ s.sound_field for s in sounds
                  if s.sound_field ]
        for note in notes:
            print 'Note - General: %s' % note
        data.append('\n'.join(notes))

        relfiles = [ s.related_item for s in sounds
                     if s.related_item ]
        for rel in relfiles:
            print 'Note - Related Files: %s' % rel
        if len(relfiles) > 1:
            print 'ERROR: item %d has %d Note - Related Files fields (not repeatable)' % \
                (self.id, len(relfiles))
        data.append('\n'.join(relfiles))

        cons = [ s.conservation_history for s in sounds
                 if s.conservation_history ]
        for con in cons:
            print 'Note - Conservation History: %s' % con
        data.append('\n'.join(cons))

        speeds = [ (s.speed.speed, s.speed.unit) for s in sounds
                   if s.speed ]
        for speed in speeds:
            print 'Speed: %s (unit: %s)' % speed
        if len(speeds) > 1:
            print 'ERROR: item %d has %d Speed fields (not repeatable)' % \
                (self.id, len(speeds))
        data.append('\n'.join('%s %s' % speed for speed in speeds))

        locs = [ s.item_location for s in sounds
                 if s.item_location ]
        for loc in locs:
            print 'Item Sub-Location: %s' % loc
        if len(locs) > 1:
            print 'ERROR: item %d has %d Item Sub-Location fields (not repeatable)' % \
                (self.id, len(locs))
        data.append('\n'.join(locs))
            
        forms = [ s.form.short_form for s in sounds
                  if s.form ]
        for form in forms:
            print 'Item Form: %s' % form
        data.append('\n'.join(forms))

        chars = [ s.sound_field for s in sounds
                  if s.sound_field ]
        for char in chars:
            print 'Sound Characteristics: %s' % char
        if len(chars) > 1:
            print 'ERROR: item %d has %d Sound Characteristics fields (not repeatable)' % \
                (self.id, len(chars))
        data.append('\n'.join(chars))
            
        stocks = [ s.stock for s in sounds
                   if s.stock ]
        for stock in stocks:
            print 'Tape - Brand/Stock: %s' % stock
        data.append('\n'.join(stocks))
        
        housings = [ s.housing.description for s in sounds
                     if s.housing ]
        for housing in housings:
            print 'Tape - Housing: %s' % housing
        if len(housings) > 1:
            print 'ERROR: item %d has %d Tape - Housing fields (not repeatable)' % \
                (self.id, len(housings))
        data.append('\n'.join(housings))

        sizes = [ s.numeric_reel_size for s in sounds
                  if s.numeric_reel_size ]
        for size in sizes:
            print 'Tape - Reel Size: %d (unit: inches)' % size
        if len(sizes) > 1:
            print 'ERROR: item %d has %d Tape - Reel Size fields (not repeatable)' % \
                (self.id, len(sizes))
        data.append('\n'.join('%d (unit: inches)' % size for size in sizes))
        
        return data

    # all fields stored for a content
    all_fields = descriptive_fields + source_tech_fields


class NameRole(models.Model):
    content = models.ForeignKey(Content)
    name = models.ForeignKey(Name)
    role = models.ForeignKey(Role)
    class Meta:
        db_table = u'contents_names'
        managed = False


class AccessRights(models.Model):
    id = models.IntegerField(primary_key=True)
    restriction_id = models.IntegerField()
    restriction_other = models.CharField(max_length=255)
    content_id = models.IntegerField()
    name_id = models.IntegerField()
    copyright_date = models.CharField(max_length=50)
    class Meta:
        db_table = u'access_rights'
        managed = False

class CodecCreatorSounds(models.Model):
    id = models.IntegerField(primary_key=True)
    hardware = models.CharField(max_length=100)
    software = models.CharField(max_length=100)
    software_version = models.CharField(max_length=100)
    class Meta:
        db_table = u'codec_creator_sounds'
        managed = False

class ColorSpaces(models.Model):
    id = models.IntegerField(primary_key=True)
    color_space = models.CharField(max_length=50)
    class Meta:
        db_table = u'color_spaces'
        managed = False

class Conditions(models.Model):
    id = models.IntegerField(primary_key=True)
    condition = models.CharField(unique=True, max_length=150)
    class Meta:
        db_table = u'conditions'
        managed = False

class ContentsConditions(models.Model):
    content_id = models.IntegerField()
    condition_id = models.IntegerField()
    class Meta:
        db_table = u'contents_conditions'
        managed = False


class Form(models.Model):
    id = models.IntegerField(primary_key=True)
    form = models.CharField(max_length=150)
    support_material = models.CharField(max_length=50)
    dates = models.CharField(max_length=50)
    identifying_features = models.TextField()
    source = models.CharField(max_length=255)
    class Meta:
        db_table = u'forms'
        managed = False

    def __unicode__(self):
        return '%s' % self.id

    @property
    def short_form(self):
        form = self.form
        if form.startswith('Sound - '):
            form = form[len('Sound - '):]
        return form

class Speed(models.Model):
    id = models.IntegerField(primary_key=True)
    speed = models.CharField(max_length=255)
    speed_alt = models.CharField(max_length=255)
    format_type = models.CharField(max_length=255)
    class Meta:
        db_table = u'speeds'
        managed = False

    def __unicode__(self):
        return '%s' % self.id

    @property
    def unit(self):
        if self.speed_alt == 'Multiple':
            return 'multiple'
        elif self.speed_alt == 'Other':
            return 'other'
        elif self.speed_alt.endswith('rpm'):
            return 'rpm'
        elif self.speed_alt.endswith('Kilohertz'):
            return 'Kilohertz'
        elif 'ips' in self.speed_alt:
            return 'inches/sec'


class SrcMovingImages(models.Model):
    id = models.IntegerField(primary_key=True)
    form_id = models.IntegerField()
    disposition = models.CharField(max_length=50)
    generation = models.CharField(max_length=50)
    length = models.IntegerField()
    source_note = models.TextField()
    sound_field = models.CharField(max_length=50)
    stock = models.CharField(max_length=255)
    related_item = models.TextField()
    item_location = models.CharField(max_length=255)
    duration = models.DateTimeField()
    content_id = models.IntegerField()
    housing_id = models.IntegerField()
    color = models.CharField(max_length=50)
    polarity = models.CharField(max_length=50)
    base = models.CharField(max_length=50)
    viewable = models.BooleanField()
    dirty = models.BooleanField()
    scratched = models.BooleanField()
    warped = models.BooleanField()
    sticky = models.BooleanField()
    faded = models.BooleanField()
    vinegar_syndrome = models.BooleanField()
    ad_strip = models.CharField(max_length=50)
    ad_strip_date = models.DateTimeField()
    ad_strip_replace_date = models.DateTimeField()
    conservation_history = models.TextField()
    source_date = models.CharField(max_length=50)
    publication_date = models.CharField(max_length=50)
    class Meta:
        db_table = u'src_moving_images'
        managed = False



class DigitalProvenances(models.Model):
    id = models.IntegerField(primary_key=True)
    date = models.DateTimeField()
    staff_name_id = models.IntegerField()
    action = models.CharField(max_length=255)
    class Meta:
        db_table = u'digital_provenances'
        managed = False

class EuarchivesSeries(models.Model):
    content = models.ForeignKey(Content, related_name='eua_series', primary_key=True)
    series = models.IntegerField()
    class Meta:
        db_table = u'euarchives_contents_series'
        managed = False

class FeedCollections(models.Model):
    mss_number = models.IntegerField(unique=True)
    class Meta:
        db_table = u'feed_collections'
        managed = False



class Housing(models.Model):
    id = models.IntegerField(primary_key=True)
    description = models.CharField(max_length=50)
    class Meta:
        db_table = u'housings'
        managed = False

    def __unicode__(self):
        return '%s' % self.id


class Restrictions(models.Model):
    id = models.IntegerField(primary_key=True)
    description = models.CharField(max_length=255)
    class Meta:
        db_table = u'restrictions'
        managed = False

class ScannerCameras(models.Model):
    id = models.IntegerField(primary_key=True)
    model_name = models.CharField(max_length=100)
    model_number = models.CharField(max_length=100)
    manufacturer = models.CharField(max_length=100)
    software = models.CharField(max_length=100)
    class Meta:
        db_table = u'scanner_cameras'
        managed = False

class SrcStillImages(models.Model):
    id = models.IntegerField(primary_key=True)
    form_id = models.IntegerField()
    dimension_height = models.FloatField()
    dimension_height_unit = models.CharField(max_length=50)
    dimension_width = models.FloatField()
    dimension_width_unit = models.CharField(max_length=50)
    dimension_note = models.CharField(max_length=255)
    disposition = models.CharField(max_length=50)
    generation = models.CharField(max_length=50)
    source_note = models.TextField()
    related_item = models.TextField()
    item_location = models.CharField(max_length=255)
    content_id = models.IntegerField()
    housing_id = models.IntegerField()
    conservation_history = models.TextField()
    source_date = models.CharField(max_length=50)
    publication_date = models.CharField(max_length=50)
    class Meta:
        db_table = u'src_still_images'
        managed = False

class TargetUrls(models.Model):
    id = models.IntegerField(primary_key=True)
    content_id = models.IntegerField()
    url = models.CharField(max_length=2000)
    class Meta:
        db_table = u'target_urls'
        managed = False

class Targets(models.Model):
    id = models.IntegerField(primary_key=True)
    name = models.CharField(max_length=255)
    pub = models.CharField(max_length=255)
    external_location = models.TextField()
    class Meta:
        db_table = u'targets'
        managed = False

class TechImages(models.Model):
    id = models.IntegerField(primary_key=True)
    content_id = models.IntegerField()
    format_name_version = models.CharField(max_length=50)
    byte_order = models.CharField(max_length=50)
    compression_scheme = models.CharField(max_length=100)
    color_space_id = models.IntegerField()
    icc_profile = models.CharField(max_length=150)
    y_cb_cr_subsample = models.CharField(max_length=100)
    y_cb_cr_positioning = models.IntegerField()
    y_cb_cr_coefficients = models.CharField(max_length=100)
    ref_bw = models.CharField(max_length=100)
    jpeg2000_profile = models.CharField(max_length=50)
    jpeg2000_class = models.CharField(max_length=50)
    jpeg2000_layers = models.CharField(max_length=50)
    jpeg2000_level = models.CharField(max_length=50)
    mr_sid = models.BooleanField()
    mr_sid_zoom_levels = models.IntegerField()
    file_size = models.IntegerField()
    scanner_camera_id = models.IntegerField()
    methodology = models.CharField(max_length=50)
    image_width = models.FloatField()
    image_length = models.FloatField()
    ppixel_res = models.IntegerField(db_column='pPixel_res') # Field name made lowercase.
    bits_per_sample = models.CharField(max_length=50)
    bits_per_sample_unit = models.CharField(max_length=50)
    samples_per_pixel = models.CharField(max_length=50)
    extra_samples = models.IntegerField()
    target_id = models.IntegerField()
    image_processing = models.CharField(max_length=255)
    gamma = models.CharField(max_length=50)
    scale = models.IntegerField()
    image_note = models.TextField()
    date_captured = models.DateTimeField()
    djvu = models.BooleanField()
    djvu_format = models.CharField(max_length=50)
    deriv_filename = models.CharField(max_length=255)
    file_location = models.CharField(max_length=50)
    digital_provence_id = models.IntegerField()
    url = models.CharField(max_length=1024)
    src_still_image_id = models.IntegerField()
    class Meta:
        db_table = u'tech_images'
        managed = False

class TechMovingImages(models.Model):
    id = models.IntegerField(primary_key=True)
    date_captured = models.DateTimeField()
    format_name = models.CharField(max_length=50)
    resolution = models.IntegerField()
    bits_per_sample = models.IntegerField()
    sampling = models.CharField(max_length=50)
    aspect_ratio = models.IntegerField()
    calibration_ext_int = models.CharField(max_length=50)
    calibrationlocation = models.TextField(db_column='CalibrationLocation') # Field name made lowercase.
    calibration_type = models.CharField(max_length=255)
    data_rate = models.CharField(max_length=50)
    data_rate_mode = models.CharField(max_length=50)
    duration = models.CharField(max_length=50)
    frame_rate = models.IntegerField()
    note = models.TextField()
    pixels_horizontial = models.IntegerField()
    pixels_vertical = models.IntegerField()
    scan = models.CharField(max_length=50)
    sound = models.BooleanField()
    file_location = models.CharField(max_length=50)
    content_id = models.IntegerField()
    class Meta:
        db_table = u'tech_moving_images'
        managed = False

class TechSounds(models.Model):
    id = models.IntegerField(primary_key=True)
    content_id = models.IntegerField()
    format_name = models.CharField(max_length=50)
    byte_order = models.CharField(max_length=50)
    compression_scheme = models.CharField(max_length=100)
    file_size = models.IntegerField()
    codec_creator = models.IntegerField()
    codec_quality = models.CharField(max_length=50)
    methodology = models.CharField(max_length=50)
    bits_per_sample = models.CharField(max_length=50)
    sampling_frequency = models.CharField(max_length=50)
    sound_note = models.TextField()
    duration = models.CharField(max_length=50)
    date_captured = models.DateTimeField()
    file_location = models.CharField(max_length=50)
    sound_clip = models.TextField()
    digital_provenance_id = models.IntegerField()
    src_sound_id = models.IntegerField()
    class Meta:
        db_table = u'tech_sounds'
        managed = False

class TmpExport(models.Model):
    image = models.IntegerField(db_column='Image') # Field name made lowercase.
    title = models.CharField(max_length=255)
    abstract = models.TextField()
    subject = models.CharField(max_length=255)
    fieldnames = models.IntegerField()
    sa_authority = models.CharField(max_length=255)
    name = models.CharField(max_length=255)
    na_authority = models.CharField(max_length=255)
    genre = models.CharField(max_length=255)
    ga_authority = models.CharField(max_length=255)
    class Meta:
        db_table = u'tmp_export'
        managed = False

class SourceSound(models.Model):
    id = models.IntegerField(primary_key=True)
    reel_size = models.CharField(max_length=50)
    dimension_note = models.CharField(max_length=255)
    disposition = models.CharField(max_length=50)
    gauge = models.CharField(max_length=50)
    generation = models.CharField(max_length=50)
    length = models.CharField(max_length=50)
    source_note = models.TextField()
    sound_field = models.CharField(max_length=50)
    stock = models.CharField(max_length=255)
    tape_thick = models.CharField(max_length=50)
    track_format = models.CharField(max_length=50)
    related_item = models.TextField()
    item_location = models.CharField(max_length=255)
    content = models.ForeignKey(Content, related_name='source_sounds')
    conservation_history = models.TextField()
    source_date = models.CharField(max_length=50)
    publication_date = models.CharField(max_length=50)
    transfer_engineer_staff_id = models.IntegerField()

    # XXX clean up code for these 0-as-null fields:

    # speed_id == 0 means no speed.
    speed_id = models.IntegerField()
    @property
    def speed(self):
        if self.speed_id:
            return Speed.objects.get(pk=self.speed_id)

    # form_id == 0 means no form.
    form_id = models.IntegerField()
    @property
    def form(self):
        if self.form_id:
            return Form.objects.get(pk=self.form_id)

    # housing_id == 0 means no form.
    housing_id = models.IntegerField()
    @property
    def housing(self):
        if self.housing_id:
            return Housing.objects.get(pk=self.housing_id)

    @property
    def numeric_reel_size(self):
        reel_size = self.reel_size
        if reel_size:
            if reel_size.endswith('"'): # all the production items do
                reel_size = reel_size[:-1]
            return int(reel_size)

    class Meta:
        db_table = u'src_sounds'
        managed = False

