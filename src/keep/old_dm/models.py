# This is an auto-generated Django model module.
# You'll have to do the following manually to clean this up:
#     * Rearrange models' order
#     * Make sure each model has one field with primary_key=True
# Feel free to rename the models, but don't rename db_table values or field names.
#
# Also note: You'll have to insert the output of 'django-admin.py sqlcustom [appname]'
# into your database.

from django.db import models

class Contents(models.Model):
    id = models.IntegerField(primary_key=True)
    record_id_type = models.CharField(max_length=50)
    other_id = models.CharField(max_length=255)
    created_at = models.DateTimeField()
    modified_at = models.DateTimeField()
    collection_number = models.IntegerField()
    title = models.CharField(max_length=255)
    subtitle = models.CharField(max_length=255)
    resource_type_id = models.IntegerField()
    location_id = models.IntegerField()
    abstract = models.TextField()
    toc = models.TextField()
    content_notes = models.TextField()
    completed_by = models.IntegerField()
    completed_date = models.DateTimeField()
    data_entered_by = models.IntegerField()
    data_entered_date = models.DateTimeField()
    authority_work_by = models.IntegerField()
    authority_work_date = models.DateTimeField()
    initial_qc_by = models.IntegerField()
    initial_qc_date = models.DateTimeField()
    class Meta:
        db_table = u'contents'
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

class Authorities(models.Model):
    id = models.IntegerField(primary_key=True)
    authority = models.CharField(max_length=255)
    class Meta:
        db_table = u'authorities'
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

class ContentsGenres(models.Model):
    id = models.IntegerField(primary_key=True)
    content_id = models.IntegerField()
    genre_id = models.IntegerField()
    class Meta:
        db_table = u'contents_genres'
        managed = False

class ContentsLanguages(models.Model):
    content_id = models.IntegerField()
    language_id = models.IntegerField()
    id = models.IntegerField(primary_key=True)
    class Meta:
        db_table = u'contents_languages'
        managed = False

class Locations(models.Model):
    id = models.IntegerField(primary_key=True)
    name = models.CharField(max_length=100)
    address = models.CharField(max_length=255)
    phone = models.CharField(max_length=50)
    fax = models.CharField(max_length=50)
    email = models.CharField(max_length=50)
    url = models.TextField()
    city = models.CharField(max_length=100)
    state = models.TextField() # This field type is a guess.
    zip = models.TextField() # This field type is a guess.
    class Meta:
        db_table = u'locations'
        managed = False

class Forms(models.Model):
    id = models.IntegerField(primary_key=True)
    form = models.CharField(max_length=150)
    support_material = models.CharField(max_length=50)
    dates = models.CharField(max_length=50)
    identifying_features = models.TextField()
    source = models.CharField(max_length=255)
    class Meta:
        db_table = u'forms'
        managed = False

class Languages(models.Model):
    id = models.IntegerField(primary_key=True)
    language = models.CharField(max_length=255)
    code = models.CharField(max_length=255)
    class Meta:
        db_table = u'languages'
        managed = False

class Roles(models.Model):
    id = models.IntegerField(primary_key=True)
    title = models.CharField(max_length=255)
    code = models.CharField(max_length=255)
    class Meta:
        db_table = u'roles'
        managed = False

class Speeds(models.Model):
    id = models.IntegerField(primary_key=True)
    speed = models.CharField(max_length=255)
    speed_alt = models.CharField(max_length=255)
    format_type = models.CharField(max_length=255)
    class Meta:
        db_table = u'speeds'
        managed = False

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

class Subjects(models.Model):
    subject = models.CharField(max_length=255)
    id = models.IntegerField(primary_key=True)
    authority_id = models.IntegerField()
    fieldnames = models.IntegerField()
    class Meta:
        db_table = u'subjects'
        managed = False

class ContentsNames(models.Model):
    content_id = models.IntegerField()
    name_id = models.IntegerField()
    role_id = models.IntegerField()
    id = models.IntegerField(primary_key=True)
    class Meta:
        db_table = u'contents_names'
        managed = False

class DigitalProvenances(models.Model):
    id = models.IntegerField(primary_key=True)
    date = models.DateTimeField()
    staff_name_id = models.IntegerField()
    action = models.CharField(max_length=255)
    class Meta:
        db_table = u'digital_provenances'
        managed = False

class EuarchivesContentsSeries(models.Model):
    content_id = models.IntegerField(unique=True)
    series = models.IntegerField()
    class Meta:
        db_table = u'euarchives_contents_series'
        managed = False

class FeedCollections(models.Model):
    mss_number = models.IntegerField(unique=True)
    class Meta:
        db_table = u'feed_collections'
        managed = False

class Genres(models.Model):
    id = models.IntegerField(primary_key=True)
    genre = models.CharField(max_length=255)
    authority_id = models.IntegerField()
    fieldnames = models.IntegerField()
    class Meta:
        db_table = u'genres'
        managed = False

class Housings(models.Model):
    id = models.IntegerField(primary_key=True)
    description = models.CharField(max_length=50)
    class Meta:
        db_table = u'housings'
        managed = False

class Names(models.Model):
    id = models.IntegerField(primary_key=True)
    name = models.CharField(unique=True, max_length=255)
    authority_id = models.IntegerField()
    name_type = models.CharField(max_length=50)
    class Meta:
        db_table = u'names'
        managed = False

class ResourceTypes(models.Model):
    id = models.IntegerField(primary_key=True)
    resource_type = models.CharField(max_length=100)
    class Meta:
        db_table = u'resource_types'
        managed = False

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

class StaffNames(models.Model):
    id = models.IntegerField(primary_key=True)
    name = models.CharField(max_length=100)
    class Meta:
        db_table = u'staff_names'
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

class ContentsSubjects(models.Model):
    id = models.IntegerField(primary_key=True)
    content_id = models.IntegerField()
    subject_id = models.IntegerField()
    class Meta:
        db_table = u'contents_subjects'
        managed = False

class SrcSounds(models.Model):
    id = models.IntegerField(primary_key=True)
    form_id = models.IntegerField()
    reel_size = models.CharField(max_length=50)
    dimension_note = models.CharField(max_length=255)
    disposition = models.CharField(max_length=50)
    gauge = models.CharField(max_length=50)
    generation = models.CharField(max_length=50)
    length = models.CharField(max_length=50)
    source_note = models.TextField()
    sound_field = models.CharField(max_length=50)
    speed_id = models.IntegerField()
    stock = models.CharField(max_length=255)
    tape_thick = models.CharField(max_length=50)
    track_format = models.CharField(max_length=50)
    related_item = models.TextField()
    item_location = models.CharField(max_length=255)
    content_id = models.IntegerField()
    housing_id = models.IntegerField()
    conservation_history = models.TextField()
    source_date = models.CharField(max_length=50)
    publication_date = models.CharField(max_length=50)
    transfer_engineer_staff_id = models.IntegerField()
    class Meta:
        db_table = u'src_sounds'
        managed = False

