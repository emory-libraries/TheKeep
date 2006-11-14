BEGIN;

/* Copy data from DigitalProvence into TechImages */

SELECT "TechImages"."*", "DigitalProvence"."ID" as "digital_provence_id" INTO "TechImagesTmp"
FROM "TechImages" 
LEFT JOIN "DigitalProvence" ON "DigitalProvence"."TechImageID" = "TechImages"."ID";


/* Change column and tables names to work with Rails */
ALTER TABLE "Authority" RENAME TO "authorities";
GRANT SELECT, INSERT, UPDATE, DELETE ON "authorities" TO digmast_user;

ALTER TABLE "CodecCreatorSound" RENAME COLUMN "ID" TO "id";
ALTER TABLE "CodecCreatorSound" RENAME COLUMN "Hardware" TO "hardware";
ALTER TABLE "CodecCreatorSound" RENAME COLUMN "Software" TO "software";
ALTER TABLE "CodecCreatorSound" RENAME COLUMN "SoftwareVersion" TO "software_version";
ALTER TABLE "CodecCreatorSound" RENAME TO "codec_creator_sounds";
GRANT SELECT, INSERT, UPDATE, DELETE ON "codec_creator_sounds" TO digmast_user;

ALTER TABLE "ColorSpace" RENAME COLUMN "ID" TO "id";
ALTER TABLE "ColorSpace" RENAME COLUMN "ColorSpace" TO "color_space";
ALTER TABLE "ColorSpace" RENAME TO "color_spaces";
GRANT SELECT, INSERT, UPDATE, DELETE ON "color_spaces" TO digmast_user;

ALTER TABLE "Condition" RENAME COLUMN "ID" TO "id";
ALTER TABLE "Condition" RENAME COLUMN "Condition" TO "condition";
ALTER TABLE "Condition" RENAME TO "conditions";
GRANT SELECT, INSERT, UPDATE, DELETE ON "conditions" TO digmast_user;

ALTER TABLE "ConditionDetail" RENAME COLUMN "ContentID" TO "content_id";
ALTER TABLE "ConditionDetail" RENAME COLUMN "ConditionID" TO "condition_id";
ALTER TABLE "ConditionDetail" RENAME TO "contents_conditions";
GRANT SELECT, INSERT, UPDATE, DELETE ON "contents_conditions" TO digmast_user;

CREATE TABLE "contents_languages" (content_id integer, language_id integer);
INSERT INTO contents_languages (SELECT "ID", "Language1" FROM "Content" WHERE "Language1" IS NOT NULL);
INSERT INTO contents_languages (SELECT "ID", "Language2" FROM "Content" WHERE "Language2" IS NOT NULL);

ALTER TABLE "contents_languages" ADD COLUMN "id" serial;
ALTER TABLE "contents_languages" ALTER COLUMN content_id SET NOT NULL;
ALTER TABLE "contents_languages" ALTER COLUMN language_id SET NOT NULL;
GRANT SELECT, INSERT, UPDATE, DELETE ON "contents_languages" TO digmast_user;

ALTER TABLE "Content" RENAME COLUMN "ID" TO "id";
ALTER TABLE "Content" RENAME COLUMN "RecordIDType" TO "record_id_type";
ALTER TABLE "Content" RENAME COLUMN "OtherID" TO "other_id";
ALTER TABLE "Content" RENAME COLUMN "DateCreated" TO "created_on";
ALTER TABLE "Content" ALTER  COLUMN "created_at" SET DEFAULT CURRENT_TIMESTAMP;
ALTER TABLE "Content" RENAME COLUMN "DateModified" TO "modified_at";
ALTER TABLE "Content" RENAME COLUMN "Collection Number" TO "collection_number";
ALTER TABLE "Content" ALTER  COLUMN "collection_number" SET NULL;
ALTER TABLE "Content" RENAME COLUMN "Title" TO "title";
ALTER TABLE "Content" RENAME COLUMN "Subtitle" TO "subtitle";
ALTER TABLE "Content" RENAME COLUMN "ResourceType" TO "resource_type_id";
ALTER TABLE "Content" ALTER  COLUMN "resource_type_id" SET DEFAULT NULL;
ALTER TABLE "Content" RENAME COLUMN "Location" TO "location_id";
ALTER TABLE "Content" RENAME COLUMN "Abstract" TO "abstract";
ALTER TABLE "Content" RENAME COLUMN "TOC" TO "toc";
ALTER TABLE "Content" RENAME COLUMN "ContentNotes" TO "content_notes";
ALTER TABLE "Content" RENAME COLUMN "CompletedBy" TO "completed_by";
ALTER TABLE "Content" RENAME COLUMN "CompletedDate" TO "completed_date";
ALTER TABLE "Content" DROP COLUMN "Complete" CASCADE; 
ALTER TABLE "Content" RENAME TO "contents";

ALTER TABLE "Content" ADD COLUMN "data_entered_by" integer;
ALTER TABLE "Content" ADD COLUMN "data_entered_date" timestamp without time zone;

ALTER TABLE "Content" ADD COLUMN "authority_work_by" integer;
ALTER TABLE "Content" ADD COLUMN "authority_work_date" timestamp without time zone;

GRANT SELECT, INSERT, UPDATE, DELETE ON "contents" TO digmast_user;

ALTER TABLE "ContentGenre" RENAME COLUMN "Content_id" TO "content_id";
ALTER TABLE "ContentGenre" RENAME COLUMN "FieldNames" TO "fieldnames";
ALTER TABLE "ContentGenre" RENAME COLUMN "Genre_id" TO "genre_id";
ALTER TABLE "ContentGenre" RENAME TO "contents_genres";
GRANT SELECT, INSERT, UPDATE, DELETE ON "contents_genres" TO digmast_user;

ALTER TABLE "DigitalProvence" RENAME COLUMN "ID" TO "id";
ALTER TABLE "DigitalProvence" RENAME COLUMN "Date" TO "date";
ALTER TABLE "DigitalProvence" RENAME COLUMN "StaffName" TO "staff_name_id";
ALTER TABLE "DigitalProvence" RENAME COLUMN "Action" TO "action";

ALTER TABLE "DigitalProvence" DROP COLUMN "TechImageID" CASCADE;

ALTER TABLE "DigitalProvence" RENAME TO "digital_provenances";
GRANT SELECT, INSERT, UPDATE, DELETE ON "digital_provenances" TO digmast_user;

ALTER TABLE "Form" RENAME COLUMN "ID" TO "id";
ALTER TABLE "Form" RENAME COLUMN "Form" TO "form";
ALTER TABLE "Form" RENAME COLUMN "SupportMaterial" TO "support_material";
ALTER TABLE "Form" RENAME COLUMN "Dates" TO "dates";
ALTER TABLE "Form" RENAME COLUMN "IdentifyingFeatures" TO "identifying_features";
ALTER TABLE "Form" RENAME COLUMN "Source" TO "source";
ALTER TABLE "Form" RENAME TO "forms";
GRANT SELECT, INSERT, UPDATE, DELETE ON "forms" TO digmast_user;

ALTER TABLE "Genres" RENAME COLUMN "Authority_id" TO "authority_id";
ALTER TABLE "Genres" RENAME TO "genres";
GRANT SELECT, INSERT, UPDATE, DELETE ON "genres" TO digmast_user;

ALTER TABLE "Housing" RENAME COLUMN "ID" TO "id";
ALTER TABLE "Housing" RENAME COLUMN "Housing description Film" TO "description";
ALTER TABLE "Housing" RENAME TO "housings";
GRANT SELECT, INSERT, UPDATE, DELETE ON "housings" TO digmast_user;

ALTER TABLE "Language" RENAME COLUMN "ID" TO "id";
ALTER TABLE "Language" RENAME COLUMN "LangName" TO "language";
ALTER TABLE "Language" RENAME COLUMN "LangCode" TO "code";
ALTER TABLE "Language" RENAME TO "languages";
GRANT SELECT, INSERT, UPDATE, DELETE ON "languages" TO digmast_user;

ALTER TABLE "Location" RENAME COLUMN "ID" TO "id";
ALTER TABLE "Location" RENAME COLUMN "LocationName" TO "name";
ALTER TABLE "Location" RENAME COLUMN "LocationStreet" TO "address";
ALTER TABLE "Location" DROP COLUMN "LocationCityStateZip";
ALTER TABLE "Location" ADD COLUMN "city" character varying (100); 
ALTER TABLE "Location" ADD COLUMN "state" character (2);
ALTER TABLE "Location" ADD COLUMN "zip" character (10);
ALTER TABLE "Location" RENAME COLUMN "LocationPhone" TO "phone";
ALTER TABLE "Location" RENAME COLUMN "LocationFax" TO "fax";
ALTER TABLE "Location" RENAME COLUMN "LocationEmail" TO "email";
ALTER TABLE "Location" RENAME COLUMN "LocationWebSite" TO "url";
ALTER TABLE "Location" RENAME TO "locations";
GRANT SELECT, INSERT, UPDATE, DELETE ON "locations" TO digmast_user;

ALTER TABLE "Name" RENAME COLUMN "ID" TO "id";
ALTER TABLE "Name" RENAME COLUMN "Name" TO "name";
ALTER TABLE "Name" RENAME COLUMN "Authority_id" TO "authority_id";
ALTER TABLE "Name" RENAME TO "names";
GRANT SELECT, INSERT, UPDATE, DELETE ON "names" TO digmast_user;

ALTER TABLE "NameDetail" RENAME COLUMN "ContentID" TO "content_id";
ALTER TABLE "NameDetail" RENAME COLUMN "Name" TO "name_id";
ALTER TABLE "NameDetail" RENAME COLUMN "Role" TO "role_id";
ALTER TABLE "NameDetail" RENAME COLUMN "RoleTerm" TO "role_term";
ALTER TABLE "NameDetail" RENAME TO "contents_names";
ALTER TABLE "contents_names" ADD COLUMN "id" serial;
GRANT SELECT, INSERT, UPDATE, DELETE ON "contents_names" TO digmast_user;
GRANT SELECT, INSERT, UPDATE, DELETE ON "contents_names_id_seq" TO digmast_user;

ALTER TABLE "ResourceType" RENAME COLUMN "ID" TO "id";
ALTER TABLE "ResourceType" RENAME COLUMN "ResourceType" TO "resource_type";
ALTER TABLE "ResourceType" RENAME TO "resource_types";
GRANT SELECT, INSERT, UPDATE, DELETE ON "resource_types" TO digmast_user;

ALTER TABLE "Restrictions" RENAME COLUMN "ID" TO "id";
ALTER TABLE "Restrictions" RENAME COLUMN "RestrictionList" TO "description";
ALTER TABLE "Restrictions" RENAME TO "restrictions";
GRANT SELECT, INSERT, UPDATE, DELETE ON "restrictions" TO digmast_user;

ALTER TABLE "RightsAccess" RENAME COLUMN "ID" TO "id";
ALTER TABLE "RightsAccess" RENAME COLUMN "Restriction" TO "restriction_id";
ALTER TABLE "RightsAccess" RENAME COLUMN "RestrictionOther" TO "restriction_other";
ALTER TABLE "RightsAccess" RENAME COLUMN "Content#" TO "content_id";
ALTER TABLE "RightsAccess" RENAME COLUMN "Name" TO "name_id";
ALTER TABLE "RightsAccess" RENAME COLUMN "CopyrightDate" TO "copyright_date";
ALTER TABLE "RightsAccess" RENAME TO "access_rights";
GRANT SELECT, INSERT, UPDATE, DELETE ON "access_rights" TO digmast_user;

ALTER TABLE "Role" RENAME COLUMN "ID" TO "id";
ALTER TABLE "Role" RENAME COLUMN "RoleName" TO "title";
ALTER TABLE "Role" RENAME COLUMN "RoleCode" TO "code";
ALTER TABLE "Role" RENAME TO "roles";
GRANT SELECT, INSERT, UPDATE, DELETE ON "roles" TO digmast_user;

ALTER TABLE "ScannerCamera" RENAME COLUMN "ID" TO "id";
ALTER TABLE "ScannerCamera" RENAME COLUMN "ScannerCameraModelName" TO "model_name";
ALTER TABLE "ScannerCamera" RENAME COLUMN "ScannerCameraModelNnumber" TO "model_number";
ALTER TABLE "ScannerCamera" RENAME COLUMN "ScannerCameraManufacturer" TO "manufacturer";
ALTER TABLE "ScannerCamera" RENAME COLUMN "ScannerCameraSoftware" TO "software";
ALTER TABLE "ScannerCamera" RENAME TO "scanner_cameras";
GRANT SELECT, INSERT, UPDATE, DELETE ON "scanner_cameras" TO digmast_user;

ALTER TABLE "SourceMovingImage" RENAME COLUMN "ID" TO "id";
ALTER TABLE "SourceMovingImage" RENAME COLUMN "Form" TO "form_id";
ALTER TABLE "SourceMovingImage" RENAME COLUMN "Disposition" TO "disposition";
ALTER TABLE "SourceMovingImage" RENAME COLUMN "Generation" TO "generation";
ALTER TABLE "SourceMovingImage" RENAME COLUMN "Length" TO "length";
ALTER TABLE "SourceMovingImage" RENAME COLUMN "SourceNote" TO "source_note";
ALTER TABLE "SourceMovingImage" RENAME COLUMN "SoundField" TO "sound_field";
ALTER TABLE "SourceMovingImage" RENAME COLUMN "Stock" TO "stock";
ALTER TABLE "SourceMovingImage" RENAME COLUMN "RelatedItem" TO "related_item";
ALTER TABLE "SourceMovingImage" RENAME COLUMN "ItemLocation" TO "item_location";
ALTER TABLE "SourceMovingImage" RENAME COLUMN "Duration" TO "duration";
ALTER TABLE "SourceMovingImage" RENAME COLUMN "Content#" TO "content_id";
ALTER TABLE "SourceMovingImage" RENAME COLUMN "HousingDescriptionFilm" TO "housing_id";
ALTER TABLE "SourceMovingImage" RENAME COLUMN "Color" TO "color";
ALTER TABLE "SourceMovingImage" RENAME COLUMN "Polarity" TO "polarity";
ALTER TABLE "SourceMovingImage" RENAME COLUMN "Base" TO "base";
ALTER TABLE "SourceMovingImage" RENAME COLUMN "Viewable" TO "viewable";
ALTER TABLE "SourceMovingImage" RENAME COLUMN "Dirty" TO "dirty";
ALTER TABLE "SourceMovingImage" RENAME COLUMN "Scratched" TO "scratched";
ALTER TABLE "SourceMovingImage" RENAME COLUMN "Warped" TO "warped";
ALTER TABLE "SourceMovingImage" RENAME COLUMN "Sticky" TO "sticky";
ALTER TABLE "SourceMovingImage" RENAME COLUMN "Faded" TO "faded";
ALTER TABLE "SourceMovingImage" RENAME COLUMN "VinegarSyndrome" TO "vinegar_syndrome";
ALTER TABLE "SourceMovingImage" RENAME COLUMN "ADStrip" TO "ad_strip";
ALTER TABLE "SourceMovingImage" RENAME COLUMN "ADStripDate" TO "ad_strip_date";
ALTER TABLE "SourceMovingImage" RENAME COLUMN "ADStripReplaceDate" TO "ad_strip_replace_date";
ALTER TABLE "SourceMovingImage" RENAME COLUMN "ConservationHistory" TO "conservation_history";
ALTER TABLE "SourceMovingImage" RENAME COLUMN "SourceDate" TO "source_date";
ALTER TABLE "SourceMovingImage" RENAME COLUMN "PublicationDate" TO "publication_date";
ALTER TABLE "SourceMovingImage" RENAME TO "src_moving_images";
GRANT SELECT, INSERT, UPDATE, DELETE ON "src_moving_images" TO digmast_user;

ALTER TABLE "SourceSound" RENAME COLUMN "ID" TO "id";
ALTER TABLE "SourceSound" RENAME COLUMN "Form" TO "form_id";
ALTER TABLE "SourceSound" RENAME COLUMN "ReelSize" TO "reel_size";
ALTER TABLE "SourceSound" RENAME COLUMN "DimensionNote" TO "dimension_note";
ALTER TABLE "SourceSound" RENAME COLUMN "Disposition" TO "disposition";
ALTER TABLE "SourceSound" RENAME COLUMN "Gauge" TO "gauge";
ALTER TABLE "SourceSound" RENAME COLUMN "Generation" TO "generation";
ALTER TABLE "SourceSound" RENAME COLUMN "Length" TO "length";
ALTER TABLE "SourceSound" RENAME COLUMN "SourceNote" TO "source_note";
ALTER TABLE "SourceSound" RENAME COLUMN "SoundField" TO "sound_field";
ALTER TABLE "SourceSound" RENAME COLUMN "Speed" TO "speed_id";
ALTER TABLE "SourceSound" RENAME COLUMN "Stock" TO "stock";
ALTER TABLE "SourceSound" RENAME COLUMN "TapeThick" TO "tape_thick";
ALTER TABLE "SourceSound" RENAME COLUMN "TrackFormat" TO "track_format";
ALTER TABLE "SourceSound" RENAME COLUMN "RelatedItem" TO "related_item";
ALTER TABLE "SourceSound" RENAME COLUMN "ItemLocation" TO "item_location";
ALTER TABLE "SourceSound" RENAME COLUMN "Content#" TO "content_id";
ALTER TABLE "SourceSound" RENAME COLUMN "Housing" TO "housing_id";
ALTER TABLE "SourceSound" RENAME COLUMN "ConservationHistory" TO "conservation_history";
ALTER TABLE "SourceSound" RENAME COLUMN "SourceDate" TO "source_date";
ALTER TABLE "SourceSound" RENAME COLUMN "PublicationDate" TO "publication_date";
ALTER TABLE "SourceSound" RENAME COLUMN "TransferEngineer" TO "transfer_engineer_staff_id";
ALTER TABLE "SourceSound" RENAME TO "src_sounds";
GRANT SELECT, INSERT, UPDATE, DELETE ON "src_sounds" TO digmast_user;

ALTER TABLE "SourceStillImage" RENAME COLUMN "ID" TO "id";
ALTER TABLE "SourceStillImage" RENAME COLUMN "Form" TO "form_id";
ALTER TABLE "SourceStillImage" RENAME COLUMN "DimensionHeight" TO "dimension_height";
ALTER TABLE "SourceStillImage" RENAME COLUMN "DimensionHeightUnit" TO "dimension_height_unit";
ALTER TABLE "SourceStillImage" RENAME COLUMN "DimensionWidth" TO "dimension_width";
ALTER TABLE "SourceStillImage" RENAME COLUMN "DimensionWidthUnit" TO "dimension_width_unit";
ALTER TABLE "SourceStillImage" RENAME COLUMN "DimensionNote" TO "dimension_note";
ALTER TABLE "SourceStillImage" RENAME COLUMN "Disposition" TO "disposition";
ALTER TABLE "SourceStillImage" RENAME COLUMN "Generation" TO "generation";
ALTER TABLE "SourceStillImage" RENAME COLUMN "SourceNote" TO "source_note";
ALTER TABLE "SourceStillImage" RENAME COLUMN "RelatedItem" TO "related_item";
ALTER TABLE "SourceStillImage" RENAME COLUMN "ItemLocation" TO "item_location";
ALTER TABLE "SourceStillImage" RENAME COLUMN "Content#" TO "content_id";
ALTER TABLE "SourceStillImage" RENAME COLUMN "HousingDescriptionPhoto" TO "housing_id";
ALTER TABLE "SourceStillImage" RENAME COLUMN "ConservationHistory" TO "conservation_history";
ALTER TABLE "SourceStillImage" RENAME COLUMN "SourceDate" TO "source_date";
ALTER TABLE "SourceStillImage" RENAME COLUMN "PublicationDate" TO "publication_date";
ALTER TABLE "SourceStillImage" RENAME TO "src_still_images";
GRANT SELECT, INSERT, UPDATE, DELETE ON "src_still_images" TO digmast_user;

ALTER TABLE "Speed" RENAME COLUMN "ID" TO "id";
ALTER TABLE "Speed" RENAME COLUMN "Speed" TO "speed";
ALTER TABLE "Speed" RENAME COLUMN "SpeedAlt" TO "speed_alt";
ALTER TABLE "Speed" RENAME COLUMN "FormatType" TO "format_type";
ALTER TABLE "Speed" RENAME TO "speeds";
GRANT SELECT, INSERT, UPDATE, DELETE ON "speeds" TO digmast_user;

ALTER TABLE "StaffName" RENAME COLUMN "ID" TO "id";
ALTER TABLE "StaffName" RENAME COLUMN "StaffName" TO "name";
ALTER TABLE "StaffName" RENAME TO "staff_names";
GRANT SELECT, INSERT, UPDATE, DELETE ON "staff_names" TO digmast_user;

ALTER TABLE "Subjects" RENAME COLUMN "ID" TO "id";
ALTER TABLE "Subjects" RENAME COLUMN "Headings" TO "subject";
ALTER TABLE "Subjects" RENAME COLUMN "Authority_id" TO "authority_id";
ALTER TABLE "Subjects" RENAME TO "subjects";
GRANT SELECT, INSERT, UPDATE, DELETE ON "subjects" TO digmast_user;

CREATE TABLE contents_subjects 
(
id integer,
content_id integer NOT NULL,
subject_id integer,
fieldnames integer 
);

DELETE FROM "Subjects Detail" WHERE "ContentID" IS NULL;
INSERT INTO contents_subjects
(id, content_id, subject_id, fieldnames)
SELECT "ID", "ContentID", "Headings", "FieldNames" FROM "Subjects Detail";

CREATE SEQUENCE "contents_subjects_id_seq";
ALTER TABLE "contents_subjects" ALTER COLUMN "id" SET DEFAULT nextval('contents_subjects_id_seq'::regclass);
SELECT setval('contents_subjects_id_seq', (SELECT max(id) FROM "contents_subjects"));
GRANT SELECT, INSERT, UPDATE, DELETE ON "contents_subjects_id_seq" TO digmast_user;
GRANT SELECT, INSERT, UPDATE, DELETE ON "contents_subjects" TO digmast_user;

DROP TABLE "Subjects Detail" CASCADE;

ALTER TABLE "Target" RENAME COLUMN "ID" TO "id";
ALTER TABLE "Target" RENAME COLUMN "TargetName" TO "name";
ALTER TABLE "Target" RENAME COLUMN "TargetPub" TO "pub";
ALTER TABLE "Target" RENAME COLUMN "TargetExtLocation" TO "external_location";
ALTER TABLE "Target" RENAME TO "targets";
GRANT SELECT, INSERT, UPDATE, DELETE ON "targets" TO digmast_user;

ALTER TABLE "TechMovingImage" RENAME COLUMN "ID" TO "id";
ALTER TABLE "TechMovingImage" ADD COLUMN "content_id" integer;
ALTER TABLE "TechMovingImage" RENAME COLUMN "DateCaptured" TO "date_captured";
ALTER TABLE "TechMovingImage" RENAME COLUMN "FormatName" TO "format_name";
ALTER TABLE "TechMovingImage" RENAME COLUMN "Resolution" TO "resolution";
ALTER TABLE "TechMovingImage" RENAME COLUMN "BitsPerSample" TO "bits_per_sample";
ALTER TABLE "TechMovingImage" RENAME COLUMN "Sampling" TO "sampling";
ALTER TABLE "TechMovingImage" RENAME COLUMN "AspectRatio" TO "aspect_ratio";
ALTER TABLE "TechMovingImage" RENAME COLUMN "CalibrationExtInt" TO "calibration_ext_int";
ALTER TABLE "TechMovingImage" RENAME COLUMN "CalibrationType" TO "calibration_type";
ALTER TABLE "TechMovingImage" RENAME COLUMN "DataRate" TO "data_rate";
ALTER TABLE "TechMovingImage" RENAME COLUMN "DataRateMode" TO "data_rate_mode";
ALTER TABLE "TechMovingImage" RENAME COLUMN "Duration" TO "duration";
ALTER TABLE "TechMovingImage" RENAME COLUMN "FrameRate" TO "frame_rate";
ALTER TABLE "TechMovingImage" RENAME COLUMN "Note" TO "note";
ALTER TABLE "TechMovingImage" RENAME COLUMN "PixelsHorizontal" TO "pixels_horizontial";
ALTER TABLE "TechMovingImage" RENAME COLUMN "PixelsVertical" TO "pixels_vertical";
ALTER TABLE "TechMovingImage" RENAME COLUMN "Scan" TO "scan";
ALTER TABLE "TechMovingImage" RENAME COLUMN "Sound" TO "sound";
ALTER TABLE "TechMovingImage" RENAME COLUMN "FileLoc" TO "file_location";
ALTER TABLE "TechMovingImage" RENAME TO "tech_moving_images";
GRANT SELECT, INSERT, UPDATE, DELETE ON "tech_moving_images" TO digmast_user;

ALTER TABLE "TechImagesTmp" RENAME COLUMN "ID" TO "id";
ALTER TABLE "TechImagesTmp" RENAME COLUMN "Content#" TO "content_id";
ALTER TABLE "TechImagesTmp" RENAME COLUMN "FormatNameVersion" TO "format_name_version";
ALTER TABLE "TechImagesTmp" RENAME COLUMN "ByteOrder" TO "byte_order";
ALTER TABLE "TechImagesTmp" RENAME COLUMN "CompressionScheme" TO "compression_scheme";
ALTER TABLE "TechImagesTmp" RENAME COLUMN "ColorSpace" TO "color_space_id";
ALTER TABLE "TechImagesTmp" RENAME COLUMN "ICCProfile" TO "icc_profile";
ALTER TABLE "TechImagesTmp" RENAME COLUMN "YCbCrSubSample" TO "y_cb_cr_subsample";
ALTER TABLE "TechImagesTmp" RENAME COLUMN "YCbCrPositioning" TO "y_cb_cr_positioning";
ALTER TABLE "TechImagesTmp" RENAME COLUMN "YCbCrCoefficients" TO "y_cb_cr_coefficients";
ALTER TABLE "TechImagesTmp" RENAME COLUMN "RefBW" TO "ref_bw";
ALTER TABLE "TechImagesTmp" RENAME COLUMN "JPEG2000Profile" TO "jpeg2000_profile";
ALTER TABLE "TechImagesTmp" RENAME COLUMN "JPEG2000Class" TO "jpeg2000_class";
ALTER TABLE "TechImagesTmp" RENAME COLUMN "JPEG2000Layers" TO "jpeg2000_layers";
ALTER TABLE "TechImagesTmp" RENAME COLUMN "JPEG2000Level" TO "jpeg2000_level";
ALTER TABLE "TechImagesTmp" RENAME COLUMN "MrSid" TO "mr_sid";
ALTER TABLE "TechImagesTmp" RENAME COLUMN "MrSidZoomLevels" TO "mr_sid_zoom_levels";
ALTER TABLE "TechImagesTmp" RENAME COLUMN "FileSize" TO "file_size";
ALTER TABLE "TechImagesTmp" RENAME COLUMN "ScannerCameraModelName" TO "scanner_camera_id";
ALTER TABLE "TechImagesTmp" RENAME COLUMN "Methodology" TO "methodology";
ALTER TABLE "TechImagesTmp" RENAME COLUMN "ImageWidth" TO "image_width";
ALTER TABLE "TechImagesTmp" RENAME COLUMN "ImageLength" TO "image_length";
ALTER TABLE "TechImagesTmp" RENAME COLUMN "PixelRes" TO "pPixel_res";
ALTER TABLE "TechImagesTmp" RENAME COLUMN "BitsPerSample" TO "bits_per_sample";
ALTER TABLE "TechImagesTmp" RENAME COLUMN "BitsPerSampleUnit" TO "bits_per_sample_unit";
ALTER TABLE "TechImagesTmp" RENAME COLUMN "SamplesPerPixel" TO "samples_per_pixel";
ALTER TABLE "TechImagesTmp" RENAME COLUMN "ExtraSamples" TO "extra_samples";
ALTER TABLE "TechImagesTmp" RENAME COLUMN "TargetLookup" TO "target_id";
ALTER TABLE "TechImagesTmp" RENAME COLUMN "ImageProcessing" TO "image_processing";
ALTER TABLE "TechImagesTmp" RENAME COLUMN "Gamma" TO "gamma";
ALTER TABLE "TechImagesTmp" RENAME COLUMN "Scale" TO "scale";
ALTER TABLE "TechImagesTmp" RENAME COLUMN "ImageNote" TO "image_note";
ALTER TABLE "TechImagesTmp" RENAME COLUMN "DateCaptured" TO "date_captured";
ALTER TABLE "TechImagesTmp" RENAME COLUMN "DjVu" TO "djvu";
ALTER TABLE "TechImagesTmp" RENAME COLUMN "DjVuFormat" TO "djvu_format";
ALTER TABLE "TechImagesTmp" RENAME COLUMN "DerivFileName" TO "deriv_filename";
ALTER TABLE "TechImagesTmp" RENAME COLUMN "FileLoc" TO "file_location";
ALTER TABLE "TechImagesTmp" RENAME COLUMN "Thumbnail" TO "thumbnail";
ALTER TABLE "TechImagesTmp" RENAME TO "tech_images";
GRANT SELECT, INSERT, UPDATE, DELETE ON "tech_images" TO digmast_user;

CREATE SEQUENCE "tech_images_id_seq";
ALTER TABLE tech_images ALTER COLUMN id SET DEFAULT nextval('"tech_images_id_seq"'::regclass);
GRANT SELECT, INSERT, UPDATE, DELETE ON "tech_images_id_seq" TO digmast_user;
SELECT setval('tech_images_id_seq', (SELECT max(id) FROM "tech_images"));

ALTER TABLE "TechSound" RENAME COLUMN "ID" TO "id";
ALTER TABLE "TechSound" RENAME COLUMN "Content#" TO "content_id";
ALTER TABLE "TechSound" RENAME COLUMN "FormatName" TO "format_name";
ALTER TABLE "TechSound" RENAME COLUMN "ByteOrder" TO "byte_order";
ALTER TABLE "TechSound" RENAME COLUMN "CompressionScheme" TO "compression_scheme";
ALTER TABLE "TechSound" RENAME COLUMN "FileSize" TO "file_size";
ALTER TABLE "TechSound" RENAME COLUMN "CodecCreator" TO "codec_creator";
ALTER TABLE "TechSound" RENAME COLUMN "CodecQuality" TO "codec_quality";
ALTER TABLE "TechSound" RENAME COLUMN "Methodology" TO "methodology";
ALTER TABLE "TechSound" RENAME COLUMN "BitsPerSample" TO "bits_per_sample";
ALTER TABLE "TechSound" RENAME COLUMN "SamplingFrequency" TO "sampling_frequency";
ALTER TABLE "TechSound" RENAME COLUMN "SoundNote" TO "sound_note";
ALTER TABLE "TechSound" RENAME COLUMN "Duration" TO "duration";
ALTER TABLE "TechSound" RENAME COLUMN "DateCaptured" TO "date_captured";
ALTER TABLE "TechSound" RENAME COLUMN "FileLoc" TO "file_location";
ALTER TABLE "TechSound" RENAME COLUMN "SoundClip" TO "sound_clip";
ALTER TABLE "TechSound" ADD COLUMN "digital_provence_id" integer;
ALTER TABLE "TechSound" RENAME TO "tech_sounds";
GRANT SELECT, INSERT, UPDATE, DELETE ON "tech_sounds" TO digmast_user;

DROP TABLE "DigitalProvenenceSound" CASCADE;
DROP TABLE "Paste Errors" CASCADE;
DROP TABLE "TechImages" CASCADE;

ALTER TABLE "contents" DROP COLUMN "Language1" CASCADE;
ALTER TABLE "contents" DROP COLUMN "Language2" CASCADE;

UPDATE pg_class SET relname = 'subjects_id_seq' WHERE relname = 'Subjects_ID_seq';

UPDATE pg_class SET relname = 'names_id_seq' WHERE relname = 'Name_ID_seq';

UPDATE pg_class SET relname = 'access_rights_id_seq' WHERE relname = 'RightsAccess_ID_seq';
ALTER TABLE access_rights ALTER COLUMN id SET DEFAULT nextval('"access_rights_id_seq"'::regclass);
GRANT SELECT, INSERT, UPDATE, DELETE ON "access_rights_id_seq" TO digmast_user;

UPDATE pg_class SET relname = 'restrictions_id_seq' WHERE relname = 'Restrictions_ID_seq';
ALTER TABLE restrictions ALTER COLUMN id SET DEFAULT nextval('"restrictions_id_seq"'::regclass);
GRANT SELECT, INSERT, UPDATE, DELETE ON "restrictions_id_seq" TO digmast_user;

UPDATE pg_class SET relname = 'src_still_images_id_seq' WHERE relname = 'SourceStillImage_ID_seq';
UPDATE pg_class SET relname = 'src_still_images_id' WHERE relname = 'SourceStillImage_ID';
UPDATE pg_class SET relname = 'src_still_images_pkey' WHERE relname = 'SourceStillImage_pkey';

ALTER TABLE src_still_images ALTER COLUMN id SET DEFAULT nextval('"src_still_images_id_seq"'::regclass);

CREATE SEQUENCE "content_id_seq";
ALTER TABLE contents ALTER COLUMN id SET DEFAULT nextval('"content_id_seq"'::regclass);
GRANT SELECT, INSERT, UPDATE, DELETE ON "content_id_seq" TO digmast_user;
SELECT setval('content_id_seq', (SELECT max(id) FROM "contents"));


CREATE SEQUENCE "language_id_seq";
/*
UPDATE pg_class SET relname = 'language_id_seq' WHERE relname = 'Language_ID_seq';
*/
ALTER TABLE languages ALTER COLUMN id SET DEFAULT nextval('"language_id_seq"'::regclass);
GRANT SELECT, INSERT, UPDATE, DELETE ON "language_id_seq" TO digmast_user;

CREATE VIEW description_datas AS
 	SELECT t1.main_entry, t1.title_statement, t1.mss_number, t1.description_y_n, t1.record_type, t1.msword_filename, t1.rlin_id_number, t1.xml, t1.notes, t1.id
	FROM dblink('dbname=manuscript_accessions'::text, 'select * from "Description Data"'::text) t1(main_entry character varying(150), title_statement character varying(200), mss_number integer, description_y_n character varying(5), record_type character varying(100), msword_filename character varying(100), rlin_id_number character varying(50), xml character varying(50), notes character varying(100), id integer);

GRANT SELECT ON "description_datas" TO digmast_user;

GRANT SELECT, INSERT, UPDATE, DELETE ON "contents_languages_id_seq" TO digmast_user;
COMMIT;
