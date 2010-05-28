--
-- PostgreSQL database dump
--

SET SESSION AUTHORIZATION 'pgsql';

--
-- TOC entry 3 (OID 2200)
-- Name: public; Type: ACL; Schema: -; Owner: pgsql
--

REVOKE ALL ON SCHEMA public FROM PUBLIC;
GRANT ALL ON SCHEMA public TO PUBLIC;
GRANT USAGE ON SCHEMA public TO rfsinge;


SET SESSION AUTHORIZATION 'jbwhite';

SET search_path = public, pg_catalog;

--
-- TOC entry 13 (OID 12738943)
-- Name: CodecCreatorSound; Type: TABLE; Schema: public; Owner: jbwhite
--

CREATE TABLE "CodecCreatorSound" (
    "ID" serial NOT NULL,
    "Hardware" character varying(100),
    "Software" character varying(100),
    "SoftwareVersion" character varying(100)
);


--
-- TOC entry 14 (OID 12738943)
-- Name: CodecCreatorSound; Type: ACL; Schema: public; Owner: jbwhite
--

REVOKE ALL ON TABLE "CodecCreatorSound" FROM PUBLIC;
GRANT INSERT,SELECT,UPDATE,DELETE ON TABLE "CodecCreatorSound" TO digmast_user;
GRANT SELECT ON TABLE "CodecCreatorSound" TO kskinne;


--
-- TOC entry 88 (OID 12738943)
-- Name: CodecCreatorSound_ID_seq; Type: ACL; Schema: public; Owner: jbwhite
--

REVOKE ALL ON TABLE "CodecCreatorSound_ID_seq" FROM PUBLIC;
GRANT INSERT,SELECT,UPDATE,DELETE ON TABLE "CodecCreatorSound_ID_seq" TO digmast_user;
GRANT SELECT ON TABLE "CodecCreatorSound_ID_seq" TO kskinne;


--
-- TOC entry 15 (OID 12739959)
-- Name: Condition; Type: TABLE; Schema: public; Owner: jbwhite
--

CREATE TABLE "Condition" (
    "ID" serial NOT NULL,
    "Condition" character varying(150)
);


--
-- TOC entry 16 (OID 12739959)
-- Name: Condition; Type: ACL; Schema: public; Owner: jbwhite
--

REVOKE ALL ON TABLE "Condition" FROM PUBLIC;
GRANT INSERT,SELECT,UPDATE,DELETE ON TABLE "Condition" TO digmast_user;
GRANT SELECT ON TABLE "Condition" TO kskinne;


--
-- TOC entry 90 (OID 12739959)
-- Name: Condition_ID_seq; Type: ACL; Schema: public; Owner: jbwhite
--

REVOKE ALL ON TABLE "Condition_ID_seq" FROM PUBLIC;
GRANT INSERT,SELECT,UPDATE,DELETE ON TABLE "Condition_ID_seq" TO digmast_user;
GRANT SELECT ON TABLE "Condition_ID_seq" TO kskinne;


--
-- TOC entry 17 (OID 12739971)
-- Name: ConditionDetail; Type: TABLE; Schema: public; Owner: jbwhite
--

CREATE TABLE "ConditionDetail" (
    "ContentID" integer DEFAULT 0 NOT NULL,
    "ConditionID" integer DEFAULT 0 NOT NULL
);


--
-- TOC entry 18 (OID 12739971)
-- Name: ConditionDetail; Type: ACL; Schema: public; Owner: jbwhite
--

REVOKE ALL ON TABLE "ConditionDetail" FROM PUBLIC;
GRANT INSERT,SELECT,UPDATE,DELETE ON TABLE "ConditionDetail" TO digmast_user;
GRANT SELECT ON TABLE "ConditionDetail" TO kskinne;


--
-- TOC entry 19 (OID 12739985)
-- Name: Content; Type: TABLE; Schema: public; Owner: jbwhite
--

CREATE TABLE "Content" (
    "ID" serial NOT NULL,
    "RecordIDType" character varying(50) DEFAULT 'local'::character varying NOT NULL,
    "OtherID" character varying(255),
    "DateCreated" timestamp without time zone NOT NULL,
    "DateModified" timestamp without time zone,
    "Collection Number" integer DEFAULT 0,
    "Title" character varying(255),
    "Subtitle" character varying(255),
    "ResourceType" integer DEFAULT 6,
    "Language1" integer DEFAULT 25,
    "Language2" integer DEFAULT 140,
    "Location" integer DEFAULT 1,
    "Abstract" text,
    "TOC" text,
    "ContentNotes" text,
    "CompletedBy" integer DEFAULT 0,
    "CompletedDate" timestamp without time zone,
    "Complete" integer DEFAULT 0
);


--
-- TOC entry 21 (OID 12739985)
-- Name: Content; Type: ACL; Schema: public; Owner: jbwhite
--

REVOKE ALL ON TABLE "Content" FROM PUBLIC;
GRANT INSERT,SELECT,UPDATE,DELETE ON TABLE "Content" TO digmast_user;
GRANT SELECT ON TABLE "Content" TO kskinne;


--
-- TOC entry 92 (OID 12739985)
-- Name: Content_ID_seq; Type: ACL; Schema: public; Owner: jbwhite
--

REVOKE ALL ON TABLE "Content_ID_seq" FROM PUBLIC;
GRANT INSERT,SELECT,UPDATE,DELETE ON TABLE "Content_ID_seq" TO digmast_user;
GRANT SELECT ON TABLE "Content_ID_seq" TO kskinne;


--
-- TOC entry 22 (OID 12741787)
-- Name: ScannerCamera; Type: TABLE; Schema: public; Owner: jbwhite
--

CREATE TABLE "ScannerCamera" (
    "ID" serial NOT NULL,
    "ScannerCameraModelName" character varying(100),
    "ScannerCameraModelNnumber" character varying(100),
    "ScannerCameraManufacturer" character varying(100),
    "ScannerCameraSoftware" character varying(100)
);


--
-- TOC entry 23 (OID 12741787)
-- Name: ScannerCamera; Type: ACL; Schema: public; Owner: jbwhite
--

REVOKE ALL ON TABLE "ScannerCamera" FROM PUBLIC;
GRANT INSERT,SELECT,UPDATE,DELETE ON TABLE "ScannerCamera" TO digmast_user;
GRANT SELECT ON TABLE "ScannerCamera" TO kskinne;


--
-- TOC entry 94 (OID 12741787)
-- Name: ScannerCamera_ID_seq; Type: ACL; Schema: public; Owner: jbwhite
--

REVOKE ALL ON TABLE "ScannerCamera_ID_seq" FROM PUBLIC;
GRANT INSERT,SELECT,UPDATE,DELETE ON TABLE "ScannerCamera_ID_seq" TO digmast_user;
GRANT SELECT ON TABLE "ScannerCamera_ID_seq" TO kskinne;


--
-- TOC entry 24 (OID 12741801)
-- Name: Target; Type: TABLE; Schema: public; Owner: jbwhite
--

CREATE TABLE "Target" (
    "ID" serial NOT NULL,
    "TargetName" character varying(255),
    "TargetPub" character varying(255),
    "TargetExtLocation" text
);


--
-- TOC entry 25 (OID 12741801)
-- Name: Target; Type: ACL; Schema: public; Owner: jbwhite
--

REVOKE ALL ON TABLE "Target" FROM PUBLIC;
GRANT INSERT,SELECT,UPDATE,DELETE ON TABLE "Target" TO digmast_user;
GRANT SELECT ON TABLE "Target" TO kskinne;


--
-- TOC entry 96 (OID 12741801)
-- Name: Target_ID_seq; Type: ACL; Schema: public; Owner: jbwhite
--

REVOKE ALL ON TABLE "Target_ID_seq" FROM PUBLIC;
GRANT INSERT,SELECT,UPDATE,DELETE ON TABLE "Target_ID_seq" TO digmast_user;
GRANT SELECT ON TABLE "Target_ID_seq" TO kskinne;


--
-- TOC entry 26 (OID 12741822)
-- Name: TechSound; Type: TABLE; Schema: public; Owner: jbwhite
--

CREATE TABLE "TechSound" (
    "ID" serial NOT NULL,
    "Content#" integer DEFAULT 0,
    "FormatName" character varying(50) DEFAULT 'wav'::character varying,
    "ByteOrder" character varying(50) DEFAULT 'Big Endian (Mac)'::character varying,
    "CompressionScheme" character varying(100),
    "FileSize" integer DEFAULT 0 NOT NULL,
    "CodecCreator" integer DEFAULT 0,
    "CodecQuality" character varying(50) DEFAULT 'lossless'::character varying,
    "Methodology" character varying(50),
    "BitsPerSample" character varying(50) DEFAULT '24'::character varying,
    "SamplingFrequency" character varying(50) DEFAULT '48'::character varying,
    "SoundNote" text,
    "Duration" character varying(50),
    "DateCaptured" timestamp without time zone,
    "FileLoc" character varying(50),
    "SoundClip" text
);


--
-- TOC entry 27 (OID 12741822)
-- Name: TechSound; Type: ACL; Schema: public; Owner: jbwhite
--

REVOKE ALL ON TABLE "TechSound" FROM PUBLIC;
GRANT INSERT,SELECT,UPDATE,DELETE ON TABLE "TechSound" TO digmast_user;
GRANT SELECT ON TABLE "TechSound" TO kskinne;


--
-- TOC entry 98 (OID 12741822)
-- Name: TechSound_ID_seq; Type: ACL; Schema: public; Owner: jbwhite
--

REVOKE ALL ON TABLE "TechSound_ID_seq" FROM PUBLIC;
GRANT INSERT,SELECT,UPDATE,DELETE ON TABLE "TechSound_ID_seq" TO digmast_user;
GRANT SELECT ON TABLE "TechSound_ID_seq" TO kskinne;


--
-- TOC entry 28 (OID 12742681)
-- Name: Housing; Type: TABLE; Schema: public; Owner: jbwhite
--

CREATE TABLE "Housing" (
    "ID" serial NOT NULL,
    "Housing description Film" character varying(50)
);


--
-- TOC entry 29 (OID 12742681)
-- Name: Housing; Type: ACL; Schema: public; Owner: jbwhite
--

REVOKE ALL ON TABLE "Housing" FROM PUBLIC;
GRANT INSERT,SELECT,UPDATE,DELETE ON TABLE "Housing" TO digmast_user;
GRANT SELECT ON TABLE "Housing" TO kskinne;


--
-- TOC entry 100 (OID 12742681)
-- Name: Housing_ID_seq; Type: ACL; Schema: public; Owner: jbwhite
--

REVOKE ALL ON TABLE "Housing_ID_seq" FROM PUBLIC;
GRANT INSERT,SELECT,UPDATE,DELETE ON TABLE "Housing_ID_seq" TO digmast_user;
GRANT SELECT ON TABLE "Housing_ID_seq" TO kskinne;


--
-- TOC entry 30 (OID 12742721)
-- Name: Form; Type: TABLE; Schema: public; Owner: jbwhite
--

CREATE TABLE "Form" (
    "ID" serial NOT NULL,
    "Form" character varying(150),
    "SupportMaterial" character varying(50),
    "Dates" character varying(50),
    "IdentifyingFeatures" text,
    "Source" character varying(255)
);


--
-- TOC entry 31 (OID 12742721)
-- Name: Form; Type: ACL; Schema: public; Owner: jbwhite
--

REVOKE ALL ON TABLE "Form" FROM PUBLIC;
GRANT INSERT,SELECT,UPDATE,DELETE ON TABLE "Form" TO digmast_user;
GRANT SELECT ON TABLE "Form" TO kskinne;


--
-- TOC entry 102 (OID 12742721)
-- Name: Form_ID_seq; Type: ACL; Schema: public; Owner: jbwhite
--

REVOKE ALL ON TABLE "Form_ID_seq" FROM PUBLIC;
GRANT INSERT,SELECT,UPDATE,DELETE ON TABLE "Form_ID_seq" TO digmast_user;
GRANT SELECT ON TABLE "Form_ID_seq" TO kskinne;


--
-- TOC entry 32 (OID 12742801)
-- Name: Language; Type: TABLE; Schema: public; Owner: jbwhite
--

CREATE TABLE "Language" (
    "ID" serial NOT NULL,
    "LangName" character varying(255),
    "LangCode" character varying(255)
);


--
-- TOC entry 33 (OID 12742801)
-- Name: Language; Type: ACL; Schema: public; Owner: jbwhite
--

REVOKE ALL ON TABLE "Language" FROM PUBLIC;
GRANT INSERT,SELECT,UPDATE,DELETE ON TABLE "Language" TO digmast_user;
GRANT SELECT ON TABLE "Language" TO kskinne;


--
-- TOC entry 104 (OID 12742801)
-- Name: Language_ID_seq; Type: ACL; Schema: public; Owner: jbwhite
--

REVOKE ALL ON TABLE "Language_ID_seq" FROM PUBLIC;
GRANT INSERT,SELECT,UPDATE,DELETE ON TABLE "Language_ID_seq" TO digmast_user;
GRANT SELECT ON TABLE "Language_ID_seq" TO kskinne;


--
-- TOC entry 34 (OID 12743214)
-- Name: Location; Type: TABLE; Schema: public; Owner: jbwhite
--

CREATE TABLE "Location" (
    "ID" serial NOT NULL,
    "LocationName" character varying(100) DEFAULT 'MARBL'::character varying,
    "LocationStreet" character varying(255),
    "LocationCityStateZip" character varying(100),
    "LocationPhone" character varying(50),
    "LocationFax" character varying(50),
    "LocationEmail" character varying(50),
    "LocationWebSite" text
);


--
-- TOC entry 35 (OID 12743214)
-- Name: Location; Type: ACL; Schema: public; Owner: jbwhite
--

REVOKE ALL ON TABLE "Location" FROM PUBLIC;
GRANT INSERT,SELECT,UPDATE,DELETE ON TABLE "Location" TO digmast_user;
GRANT SELECT ON TABLE "Location" TO kskinne;


--
-- TOC entry 106 (OID 12743214)
-- Name: Location_ID_seq; Type: ACL; Schema: public; Owner: jbwhite
--

REVOKE ALL ON TABLE "Location_ID_seq" FROM PUBLIC;
GRANT INSERT,SELECT,UPDATE,DELETE ON TABLE "Location_ID_seq" TO digmast_user;
GRANT SELECT ON TABLE "Location_ID_seq" TO kskinne;


--
-- TOC entry 36 (OID 12743236)
-- Name: Name; Type: TABLE; Schema: public; Owner: jbwhite
--

CREATE TABLE "Name" (
    "ID" serial NOT NULL,
    "Name" character varying(255),
    "Authority_id" integer NOT NULL
);


--
-- TOC entry 38 (OID 12743236)
-- Name: Name; Type: ACL; Schema: public; Owner: jbwhite
--

REVOKE ALL ON TABLE "Name" FROM PUBLIC;
GRANT INSERT,SELECT,UPDATE,DELETE ON TABLE "Name" TO digmast_user;
GRANT SELECT ON TABLE "Name" TO kskinne;


--
-- TOC entry 108 (OID 12743236)
-- Name: Name_ID_seq; Type: ACL; Schema: public; Owner: jbwhite
--

REVOKE ALL ON TABLE "Name_ID_seq" FROM PUBLIC;
GRANT INSERT,SELECT,UPDATE,DELETE ON TABLE "Name_ID_seq" TO digmast_user;
GRANT SELECT ON TABLE "Name_ID_seq" TO kskinne;


--
-- TOC entry 39 (OID 12743378)
-- Name: Restrictions; Type: TABLE; Schema: public; Owner: jbwhite
--

CREATE TABLE "Restrictions" (
    "ID" serial NOT NULL,
    "RestrictionList" character varying(255)
);


--
-- TOC entry 40 (OID 12743378)
-- Name: Restrictions; Type: ACL; Schema: public; Owner: jbwhite
--

REVOKE ALL ON TABLE "Restrictions" FROM PUBLIC;
GRANT INSERT,SELECT,UPDATE,DELETE ON TABLE "Restrictions" TO digmast_user;
GRANT SELECT ON TABLE "Restrictions" TO kskinne;


--
-- TOC entry 110 (OID 12743378)
-- Name: Restrictions_ID_seq; Type: ACL; Schema: public; Owner: jbwhite
--

REVOKE ALL ON TABLE "Restrictions_ID_seq" FROM PUBLIC;
GRANT INSERT,SELECT,UPDATE,DELETE ON TABLE "Restrictions_ID_seq" TO digmast_user;
GRANT SELECT ON TABLE "Restrictions_ID_seq" TO kskinne;


--
-- TOC entry 41 (OID 12743395)
-- Name: Paste Errors; Type: TABLE; Schema: public; Owner: jbwhite
--

CREATE TABLE "Paste Errors" (
    "Combo128" text,
    "ID" integer,
    "RecordIDType" character varying(255),
    "OtherID" character varying(255),
    "Combo139" integer,
    "Combo135" character varying(255),
    "Combo137" character varying(255),
    "RecordCreationDate" timestamp without time zone,
    "Text38" timestamp without time zone,
    "Combo40" character varying(255),
    "Combo42" character varying(255),
    "Combo44" character varying(255),
    "Combo46" character varying(255),
    "Title" character varying(255),
    "Subtitle" character varying(255),
    "Text48" text,
    "TOC" text,
    "Text50" text,
    "cmbCompletedBy" integer,
    "txtCompletedOn" timestamp without time zone,
    "chkComplete" boolean
);


--
-- TOC entry 42 (OID 12743403)
-- Name: ResourceType; Type: TABLE; Schema: public; Owner: jbwhite
--

CREATE TABLE "ResourceType" (
    "ID" serial NOT NULL,
    "ResourceType" character varying(100)
);


--
-- TOC entry 43 (OID 12743403)
-- Name: ResourceType; Type: ACL; Schema: public; Owner: jbwhite
--

REVOKE ALL ON TABLE "ResourceType" FROM PUBLIC;
GRANT INSERT,SELECT,UPDATE,DELETE ON TABLE "ResourceType" TO digmast_user;
GRANT SELECT ON TABLE "ResourceType" TO kskinne;


--
-- TOC entry 112 (OID 12743403)
-- Name: ResourceType_ID_seq; Type: ACL; Schema: public; Owner: jbwhite
--

REVOKE ALL ON TABLE "ResourceType_ID_seq" FROM PUBLIC;
GRANT INSERT,SELECT,UPDATE,DELETE ON TABLE "ResourceType_ID_seq" TO digmast_user;
GRANT SELECT ON TABLE "ResourceType_ID_seq" TO kskinne;


--
-- TOC entry 44 (OID 12743424)
-- Name: RightsAccess; Type: TABLE; Schema: public; Owner: jbwhite
--

CREATE TABLE "RightsAccess" (
    "ID" serial NOT NULL,
    "Restriction" integer DEFAULT 10 NOT NULL,
    "RestrictionOther" character varying(255),
    "Content#" integer DEFAULT 0,
    "Name" integer DEFAULT 0,
    "CopyrightDate" character varying(50)
);


--
-- TOC entry 45 (OID 12743424)
-- Name: RightsAccess; Type: ACL; Schema: public; Owner: jbwhite
--

REVOKE ALL ON TABLE "RightsAccess" FROM PUBLIC;
GRANT INSERT,SELECT,UPDATE,DELETE ON TABLE "RightsAccess" TO digmast_user;
GRANT SELECT ON TABLE "RightsAccess" TO kskinne;


--
-- TOC entry 114 (OID 12743424)
-- Name: RightsAccess_ID_seq; Type: ACL; Schema: public; Owner: jbwhite
--

REVOKE ALL ON TABLE "RightsAccess_ID_seq" FROM PUBLIC;
GRANT INSERT,SELECT,UPDATE,DELETE ON TABLE "RightsAccess_ID_seq" TO digmast_user;
GRANT SELECT ON TABLE "RightsAccess_ID_seq" TO kskinne;


--
-- TOC entry 46 (OID 12744361)
-- Name: Role; Type: TABLE; Schema: public; Owner: jbwhite
--

CREATE TABLE "Role" (
    "ID" serial NOT NULL,
    "RoleName" character varying(255),
    "RoleCode" character varying(255)
);


--
-- TOC entry 47 (OID 12744361)
-- Name: Role; Type: ACL; Schema: public; Owner: jbwhite
--

REVOKE ALL ON TABLE "Role" FROM PUBLIC;
GRANT INSERT,SELECT,UPDATE,DELETE ON TABLE "Role" TO digmast_user;
GRANT SELECT ON TABLE "Role" TO kskinne;


--
-- TOC entry 116 (OID 12744361)
-- Name: Role_ID_seq; Type: ACL; Schema: public; Owner: jbwhite
--

REVOKE ALL ON TABLE "Role_ID_seq" FROM PUBLIC;
GRANT INSERT,SELECT,UPDATE,DELETE ON TABLE "Role_ID_seq" TO digmast_user;
GRANT SELECT ON TABLE "Role_ID_seq" TO kskinne;


--
-- TOC entry 48 (OID 12744541)
-- Name: NameDetail; Type: TABLE; Schema: public; Owner: jbwhite
--

CREATE TABLE "NameDetail" (
    "ContentID" integer DEFAULT 0 NOT NULL,
    "Name" integer DEFAULT 0 NOT NULL,
    "Role" integer DEFAULT 0,
    "RoleTerm" character varying(50)
);


--
-- TOC entry 49 (OID 12744541)
-- Name: NameDetail; Type: ACL; Schema: public; Owner: jbwhite
--

REVOKE ALL ON TABLE "NameDetail" FROM PUBLIC;
GRANT INSERT,SELECT,UPDATE,DELETE ON TABLE "NameDetail" TO digmast_user;
GRANT SELECT ON TABLE "NameDetail" TO kskinne;


--
-- TOC entry 50 (OID 12744578)
-- Name: StaffName; Type: TABLE; Schema: public; Owner: jbwhite
--

CREATE TABLE "StaffName" (
    "ID" serial NOT NULL,
    "StaffName" character varying(100)
);


--
-- TOC entry 51 (OID 12744578)
-- Name: StaffName; Type: ACL; Schema: public; Owner: jbwhite
--

REVOKE ALL ON TABLE "StaffName" FROM PUBLIC;
GRANT INSERT,SELECT,UPDATE,DELETE ON TABLE "StaffName" TO digmast_user;
GRANT SELECT ON TABLE "StaffName" TO kskinne;


--
-- TOC entry 118 (OID 12744578)
-- Name: StaffName_ID_seq; Type: ACL; Schema: public; Owner: jbwhite
--

REVOKE ALL ON TABLE "StaffName_ID_seq" FROM PUBLIC;
GRANT INSERT,SELECT,UPDATE,DELETE ON TABLE "StaffName_ID_seq" TO digmast_user;
GRANT SELECT ON TABLE "StaffName_ID_seq" TO kskinne;


--
-- TOC entry 52 (OID 12744593)
-- Name: SourceStillImage; Type: TABLE; Schema: public; Owner: jbwhite
--

CREATE TABLE "SourceStillImage" (
    "ID" serial NOT NULL,
    "Form" integer DEFAULT 0,
    "DimensionHeight" double precision DEFAULT 0,
    "DimensionHeightUnit" character varying(50) DEFAULT 'inches'::character varying,
    "DimensionWidth" double precision DEFAULT 0,
    "DimensionWidthUnit" character varying(50) DEFAULT 'inches'::character varying,
    "DimensionNote" character varying(255),
    "Disposition" character varying(50) DEFAULT 'retained'::character varying NOT NULL,
    "Generation" character varying(50),
    "SourceNote" text,
    "RelatedItem" text,
    "ItemLocation" character varying(255),
    "Content#" integer DEFAULT 0,
    "HousingDescriptionPhoto" integer DEFAULT 0,
    "ConservationHistory" text,
    "SourceDate" character varying(50),
    "PublicationDate" character varying(50)
);


--
-- TOC entry 53 (OID 12744593)
-- Name: SourceStillImage; Type: ACL; Schema: public; Owner: jbwhite
--

REVOKE ALL ON TABLE "SourceStillImage" FROM PUBLIC;
GRANT INSERT,SELECT,UPDATE,DELETE ON TABLE "SourceStillImage" TO digmast_user;
GRANT SELECT ON TABLE "SourceStillImage" TO kskinne;


--
-- TOC entry 120 (OID 12744593)
-- Name: SourceStillImage_ID_seq; Type: ACL; Schema: public; Owner: jbwhite
--

REVOKE ALL ON TABLE "SourceStillImage_ID_seq" FROM PUBLIC;
GRANT INSERT,SELECT,UPDATE,DELETE ON TABLE "SourceStillImage_ID_seq" TO digmast_user;
GRANT SELECT ON TABLE "SourceStillImage_ID_seq" TO kskinne;


--
-- TOC entry 54 (OID 12745562)
-- Name: SourceMovingImage; Type: TABLE; Schema: public; Owner: jbwhite
--

CREATE TABLE "SourceMovingImage" (
    "ID" serial NOT NULL,
    "Form" integer DEFAULT 0,
    "Disposition" character varying(50) DEFAULT 'retained'::character varying NOT NULL,
    "Generation" character varying(50),
    "Length" integer DEFAULT 0,
    "SourceNote" text,
    "SoundField" character varying(50),
    "Stock" character varying(255),
    "RelatedItem" text,
    "ItemLocation" character varying(255),
    "Duration" timestamp without time zone,
    "Content#" integer DEFAULT 0,
    "HousingDescriptionFilm" integer DEFAULT 0,
    "Color" character varying(50),
    "Polarity" character varying(50) DEFAULT 'positive'::character varying,
    "Base" character varying(50) DEFAULT 'acetate'::character varying,
    "Viewable" boolean DEFAULT false,
    "Dirty" boolean,
    "Scratched" boolean,
    "Warped" boolean,
    "Sticky" boolean,
    "Faded" boolean,
    "VinegarSyndrome" boolean,
    "ADStrip" character varying(50),
    "ADStripDate" timestamp without time zone,
    "ADStripReplaceDate" timestamp without time zone,
    "ConservationHistory" text,
    "SourceDate" character varying(50),
    "PublicationDate" character varying(50)
);


--
-- TOC entry 55 (OID 12745562)
-- Name: SourceMovingImage; Type: ACL; Schema: public; Owner: jbwhite
--

REVOKE ALL ON TABLE "SourceMovingImage" FROM PUBLIC;
GRANT INSERT,SELECT,UPDATE,DELETE ON TABLE "SourceMovingImage" TO digmast_user;
GRANT SELECT ON TABLE "SourceMovingImage" TO kskinne;


--
-- TOC entry 122 (OID 12745562)
-- Name: SourceMovingImage_ID_seq; Type: ACL; Schema: public; Owner: jbwhite
--

REVOKE ALL ON TABLE "SourceMovingImage_ID_seq" FROM PUBLIC;
GRANT INSERT,SELECT,UPDATE,DELETE ON TABLE "SourceMovingImage_ID_seq" TO digmast_user;
GRANT SELECT ON TABLE "SourceMovingImage_ID_seq" TO kskinne;


--
-- TOC entry 56 (OID 12745581)
-- Name: Speed; Type: TABLE; Schema: public; Owner: jbwhite
--

CREATE TABLE "Speed" (
    "ID" serial NOT NULL,
    "Speed" character varying(255),
    "SpeedAlt" character varying(255),
    "FormatType" character varying(255)
);


--
-- TOC entry 57 (OID 12745581)
-- Name: Speed; Type: ACL; Schema: public; Owner: jbwhite
--

REVOKE ALL ON TABLE "Speed" FROM PUBLIC;
GRANT INSERT,SELECT,UPDATE,DELETE ON TABLE "Speed" TO digmast_user;
GRANT SELECT ON TABLE "Speed" TO kskinne;


--
-- TOC entry 124 (OID 12745581)
-- Name: Speed_ID_seq; Type: ACL; Schema: public; Owner: jbwhite
--

REVOKE ALL ON TABLE "Speed_ID_seq" FROM PUBLIC;
GRANT INSERT,SELECT,UPDATE,DELETE ON TABLE "Speed_ID_seq" TO digmast_user;
GRANT SELECT ON TABLE "Speed_ID_seq" TO kskinne;


--
-- TOC entry 58 (OID 12745630)
-- Name: SourceSound; Type: TABLE; Schema: public; Owner: jbwhite
--

CREATE TABLE "SourceSound" (
    "ID" serial NOT NULL,
    "Form" integer DEFAULT 0,
    "ReelSize" character varying(50),
    "DimensionNote" character varying(255),
    "Disposition" character varying(50) DEFAULT 'retained'::character varying NOT NULL,
    "Gauge" character varying(50),
    "Generation" character varying(50),
    "Length" character varying(50),
    "SourceNote" text,
    "SoundField" character varying(50),
    "Speed" integer DEFAULT 0,
    "Stock" character varying(255),
    "TapeThick" character varying(50),
    "TrackFormat" character varying(50),
    "RelatedItem" text,
    "ItemLocation" character varying(255),
    "Content#" integer DEFAULT 0,
    "Housing" integer DEFAULT 0,
    "ConservationHistory" text,
    "SourceDate" character varying(50),
    "PublicationDate" character varying(50),
    "TransferEngineer" integer DEFAULT 0
);


--
-- TOC entry 59 (OID 12745630)
-- Name: SourceSound; Type: ACL; Schema: public; Owner: jbwhite
--

REVOKE ALL ON TABLE "SourceSound" FROM PUBLIC;
GRANT INSERT,SELECT,UPDATE,DELETE ON TABLE "SourceSound" TO digmast_user;
GRANT SELECT ON TABLE "SourceSound" TO kskinne;


--
-- TOC entry 126 (OID 12745630)
-- Name: SourceSound_ID_seq; Type: ACL; Schema: public; Owner: jbwhite
--

REVOKE ALL ON TABLE "SourceSound_ID_seq" FROM PUBLIC;
GRANT INSERT,SELECT,UPDATE,DELETE ON TABLE "SourceSound_ID_seq" TO digmast_user;
GRANT SELECT ON TABLE "SourceSound_ID_seq" TO kskinne;


--
-- TOC entry 60 (OID 12746497)
-- Name: ColorSpace; Type: TABLE; Schema: public; Owner: jbwhite
--

CREATE TABLE "ColorSpace" (
    "ID" serial NOT NULL,
    "ColorSpace" character varying(50)
);


--
-- TOC entry 61 (OID 12746497)
-- Name: ColorSpace; Type: ACL; Schema: public; Owner: jbwhite
--

REVOKE ALL ON TABLE "ColorSpace" FROM PUBLIC;
GRANT INSERT,SELECT,UPDATE,DELETE ON TABLE "ColorSpace" TO digmast_user;
GRANT SELECT ON TABLE "ColorSpace" TO kskinne;


--
-- TOC entry 128 (OID 12746497)
-- Name: ColorSpace_ID_seq; Type: ACL; Schema: public; Owner: jbwhite
--

REVOKE ALL ON TABLE "ColorSpace_ID_seq" FROM PUBLIC;
GRANT INSERT,SELECT,UPDATE,DELETE ON TABLE "ColorSpace_ID_seq" TO digmast_user;
GRANT SELECT ON TABLE "ColorSpace_ID_seq" TO kskinne;


--
-- TOC entry 62 (OID 12746523)
-- Name: Subjects; Type: TABLE; Schema: public; Owner: jbwhite
--

CREATE TABLE "Subjects" (
    "Headings" character varying(255),
    "ID" serial NOT NULL,
    "Authority_id" integer DEFAULT 0 NOT NULL
);


--
-- TOC entry 64 (OID 12746523)
-- Name: Subjects; Type: ACL; Schema: public; Owner: jbwhite
--

REVOKE ALL ON TABLE "Subjects" FROM PUBLIC;
GRANT INSERT,SELECT,UPDATE,DELETE ON TABLE "Subjects" TO digmast_user;
GRANT SELECT ON TABLE "Subjects" TO kskinne;


--
-- TOC entry 130 (OID 12746523)
-- Name: Subjects_ID_seq; Type: ACL; Schema: public; Owner: jbwhite
--

REVOKE ALL ON TABLE "Subjects_ID_seq" FROM PUBLIC;
GRANT INSERT,SELECT,UPDATE,DELETE ON TABLE "Subjects_ID_seq" TO digmast_user;
GRANT SELECT ON TABLE "Subjects_ID_seq" TO kskinne;


--
-- TOC entry 65 (OID 12746611)
-- Name: TechImages; Type: TABLE; Schema: public; Owner: jbwhite
--

CREATE TABLE "TechImages" (
    "ID" serial NOT NULL,
    "Content#" integer DEFAULT 0,
    "FormatNameVersion" character varying(50) DEFAULT 'TIFF 6.0'::character varying,
    "ByteOrder" character varying(50) DEFAULT 'Little Endian (PC)'::character varying,
    "CompressionScheme" character varying(100) DEFAULT 'Uncompressed'::character varying,
    "ColorSpace" integer DEFAULT 1,
    "ICCProfile" character varying(150),
    "YCbCrSubSample" character varying(100),
    "YCbCrPositioning" integer DEFAULT 2,
    "YCbCrCoefficients" character varying(100),
    "RefBW" character varying(100),
    "JPEG2000Profile" character varying(50),
    "JPEG2000Class" character varying(50),
    "JPEG2000Layers" character varying(50),
    "JPEG2000Level" character varying(50),
    "MrSid" boolean DEFAULT false,
    "MrSidZoomLevels" integer DEFAULT 0,
    "FileSize" integer DEFAULT 0 NOT NULL,
    "ScannerCameraModelName" integer DEFAULT 0,
    "Methodology" character varying(50) DEFAULT 'library internal use'::character varying NOT NULL,
    "ImageWidth" double precision DEFAULT 0 NOT NULL,
    "ImageLength" double precision DEFAULT 0 NOT NULL,
    "PixelRes" integer DEFAULT 400 NOT NULL,
    "BitsPerSample" character varying(50) DEFAULT '8,8,8'::character varying,
    "BitsPerSampleUnit" character varying(50) DEFAULT 'integer'::character varying,
    "SamplesPerPixel" character varying(50) DEFAULT '3'::character varying,
    "ExtraSamples" integer DEFAULT 0,
    "TargetLookup" integer DEFAULT 0,
    "ImageProcessing" character varying(255),
    "Gamma" character varying(50) DEFAULT '2.2'::character varying,
    "Scale" integer DEFAULT 100,
    "ImageNote" text,
    "DateCaptured" timestamp without time zone,
    "DjVu" boolean DEFAULT false,
    "DjVuFormat" character varying(50),
    "DerivFileName" character varying(255),
    "FileLoc" character varying(50),
    "Thumbnail" text
);


--
-- TOC entry 66 (OID 12746611)
-- Name: TechImages; Type: ACL; Schema: public; Owner: jbwhite
--

REVOKE ALL ON TABLE "TechImages" FROM PUBLIC;
GRANT INSERT,SELECT,UPDATE,DELETE ON TABLE "TechImages" TO digmast_user;
GRANT SELECT ON TABLE "TechImages" TO kskinne;


--
-- TOC entry 132 (OID 12746611)
-- Name: TechImages_ID_seq; Type: ACL; Schema: public; Owner: jbwhite
--

REVOKE ALL ON TABLE "TechImages_ID_seq" FROM PUBLIC;
GRANT INSERT,SELECT,UPDATE,DELETE ON TABLE "TechImages_ID_seq" TO digmast_user;
GRANT SELECT ON TABLE "TechImages_ID_seq" TO kskinne;


--
-- TOC entry 67 (OID 12747599)
-- Name: DigitalProvence; Type: TABLE; Schema: public; Owner: jbwhite
--

CREATE TABLE "DigitalProvence" (
    "ID" serial NOT NULL,
    "Date" timestamp without time zone,
    "StaffName" integer DEFAULT 0,
    "Action" character varying(255),
    "TechImageID" integer DEFAULT 0
);


--
-- TOC entry 68 (OID 12747599)
-- Name: DigitalProvence; Type: ACL; Schema: public; Owner: jbwhite
--

REVOKE ALL ON TABLE "DigitalProvence" FROM PUBLIC;
GRANT INSERT,SELECT,UPDATE,DELETE ON TABLE "DigitalProvence" TO digmast_user;
GRANT SELECT ON TABLE "DigitalProvence" TO kskinne;


--
-- TOC entry 134 (OID 12747599)
-- Name: DigitalProvence_ID_seq; Type: ACL; Schema: public; Owner: jbwhite
--

REVOKE ALL ON TABLE "DigitalProvence_ID_seq" FROM PUBLIC;
GRANT INSERT,SELECT,UPDATE,DELETE ON TABLE "DigitalProvence_ID_seq" TO digmast_user;
GRANT SELECT ON TABLE "DigitalProvence_ID_seq" TO kskinne;


--
-- TOC entry 69 (OID 12747638)
-- Name: TechMovingImage; Type: TABLE; Schema: public; Owner: jbwhite
--

CREATE TABLE "TechMovingImage" (
    "ID" serial NOT NULL,
    "DateCaptured" timestamp without time zone,
    "FormatName" character varying(50),
    "Resolution" integer DEFAULT 400 NOT NULL,
    "BitsPerSample" integer DEFAULT 0,
    "Sampling" character varying(50) DEFAULT '3'::character varying,
    "AspectRatio" integer DEFAULT 0,
    "CalibrationExtInt" character varying(50),
    "CalibrationLocation" text,
    "CalibrationType" character varying(255),
    "DataRate" character varying(50),
    "DataRateMode" character varying(50),
    "Duration" character varying(50),
    "FrameRate" integer DEFAULT 0,
    "Note" text,
    "PixelsHorizontal" integer DEFAULT 0,
    "PixelsVertical" integer DEFAULT 0,
    "Scan" character varying(50),
    "Sound" boolean,
    "FileLoc" character varying(50)
);


--
-- TOC entry 70 (OID 12747638)
-- Name: TechMovingImage; Type: ACL; Schema: public; Owner: jbwhite
--

REVOKE ALL ON TABLE "TechMovingImage" FROM PUBLIC;
GRANT INSERT,SELECT,UPDATE,DELETE ON TABLE "TechMovingImage" TO digmast_user;
GRANT SELECT ON TABLE "TechMovingImage" TO kskinne;


--
-- TOC entry 136 (OID 12747638)
-- Name: TechMovingImage_ID_seq; Type: ACL; Schema: public; Owner: jbwhite
--

REVOKE ALL ON TABLE "TechMovingImage_ID_seq" FROM PUBLIC;
GRANT INSERT,SELECT,UPDATE,DELETE ON TABLE "TechMovingImage_ID_seq" TO digmast_user;
GRANT SELECT ON TABLE "TechMovingImage_ID_seq" TO kskinne;


--
-- TOC entry 71 (OID 12747656)
-- Name: DigitalProvenenceSound; Type: TABLE; Schema: public; Owner: jbwhite
--

CREATE TABLE "DigitalProvenenceSound" (
    "ID" serial NOT NULL,
    "Date" timestamp without time zone,
    "StaffName" integer DEFAULT 0,
    "Action" character varying(255),
    "TechSoundID" integer DEFAULT 0
);


--
-- TOC entry 72 (OID 12747656)
-- Name: DigitalProvenenceSound; Type: ACL; Schema: public; Owner: jbwhite
--

REVOKE ALL ON TABLE "DigitalProvenenceSound" FROM PUBLIC;
GRANT INSERT,SELECT,UPDATE,DELETE ON TABLE "DigitalProvenenceSound" TO digmast_user;
GRANT SELECT ON TABLE "DigitalProvenenceSound" TO kskinne;


--
-- TOC entry 138 (OID 12747656)
-- Name: DigitalProvenenceSound_ID_seq; Type: ACL; Schema: public; Owner: jbwhite
--

REVOKE ALL ON TABLE "DigitalProvenenceSound_ID_seq" FROM PUBLIC;
GRANT INSERT,SELECT,UPDATE,DELETE ON TABLE "DigitalProvenenceSound_ID_seq" TO digmast_user;
GRANT SELECT ON TABLE "DigitalProvenenceSound_ID_seq" TO kskinne;


--
-- TOC entry 73 (OID 12750150)
-- Name: Subjects Detail; Type: TABLE; Schema: public; Owner: jbwhite
--

CREATE TABLE "Subjects Detail" (
    "ID" serial NOT NULL,
    "ContentID" integer DEFAULT 0,
    "FieldNames" integer DEFAULT 0,
    "Headings" integer DEFAULT 0
);


--
-- TOC entry 74 (OID 12750150)
-- Name: Subjects Detail; Type: ACL; Schema: public; Owner: jbwhite
--

REVOKE ALL ON TABLE "Subjects Detail" FROM PUBLIC;
GRANT INSERT,SELECT,UPDATE,DELETE ON TABLE "Subjects Detail" TO digmast_user;
GRANT SELECT ON TABLE "Subjects Detail" TO kskinne;


--
-- TOC entry 140 (OID 12750150)
-- Name: Subjects Detail_ID_seq; Type: ACL; Schema: public; Owner: jbwhite
--

REVOKE ALL ON TABLE "Subjects Detail_ID_seq" FROM PUBLIC;
GRANT INSERT,SELECT,UPDATE,DELETE ON TABLE "Subjects Detail_ID_seq" TO digmast_user;
GRANT SELECT ON TABLE "Subjects Detail_ID_seq" TO kskinne;


--
-- TOC entry 75 (OID 12753220)
-- Name: Authority; Type: TABLE; Schema: public; Owner: jbwhite
--

CREATE TABLE "Authority" (
    id integer DEFAULT nextval('public."Authority_ID_seq"'::text) NOT NULL,
    authority character varying(255)
);


--
-- TOC entry 77 (OID 12753220)
-- Name: Authority; Type: ACL; Schema: public; Owner: jbwhite
--

REVOKE ALL ON TABLE "Authority" FROM PUBLIC;
GRANT INSERT,SELECT,UPDATE,DELETE ON TABLE "Authority" TO digmast_user;


--
-- TOC entry 4 (OID 12753224)
-- Name: Authority_ID_seq; Type: SEQUENCE; Schema: public; Owner: jbwhite
--

CREATE SEQUENCE "Authority_ID_seq"
    INCREMENT BY 1
    NO MAXVALUE
    NO MINVALUE
    CACHE 1;


--
-- TOC entry 6 (OID 12753224)
-- Name: Authority_ID_seq; Type: ACL; Schema: public; Owner: jbwhite
--

REVOKE ALL ON TABLE "Authority_ID_seq" FROM PUBLIC;
GRANT SELECT,UPDATE ON TABLE "Authority_ID_seq" TO digmast_user;


--
-- TOC entry 7 (OID 12753236)
-- Name: Genres_ID_seq; Type: SEQUENCE; Schema: public; Owner: jbwhite
--

CREATE SEQUENCE "Genres_ID_seq"
    INCREMENT BY 1
    NO MAXVALUE
    NO MINVALUE
    CACHE 1;


--
-- TOC entry 9 (OID 12753236)
-- Name: Genres_ID_seq; Type: ACL; Schema: public; Owner: jbwhite
--

REVOKE ALL ON TABLE "Genres_ID_seq" FROM PUBLIC;
GRANT SELECT,UPDATE ON TABLE "Genres_ID_seq" TO digmast_user;


--
-- TOC entry 10 (OID 12753238)
-- Name: ContentGenre_ID_seq; Type: SEQUENCE; Schema: public; Owner: jbwhite
--

CREATE SEQUENCE "ContentGenre_ID_seq"
    START WITH 1
    INCREMENT BY 1
    NO MAXVALUE
    NO MINVALUE
    CACHE 1;


--
-- TOC entry 12 (OID 12753238)
-- Name: ContentGenre_ID_seq; Type: ACL; Schema: public; Owner: jbwhite
--

REVOKE ALL ON TABLE "ContentGenre_ID_seq" FROM PUBLIC;
GRANT SELECT,UPDATE ON TABLE "ContentGenre_ID_seq" TO digmast_user;


--
-- TOC entry 78 (OID 12753242)
-- Name: Genres; Type: TABLE; Schema: public; Owner: jbwhite
--

CREATE TABLE "Genres" (
    id integer DEFAULT nextval('public."Genres_ID_seq"'::text) NOT NULL,
    genre character varying(255),
    "Authority_id" integer DEFAULT 0 NOT NULL
);


--
-- TOC entry 80 (OID 12753242)
-- Name: Genres; Type: ACL; Schema: public; Owner: jbwhite
--

REVOKE ALL ON TABLE "Genres" FROM PUBLIC;
GRANT INSERT,SELECT,UPDATE,DELETE ON TABLE "Genres" TO digmast_user;


--
-- TOC entry 81 (OID 12753248)
-- Name: ContentGenre; Type: TABLE; Schema: public; Owner: jbwhite
--

CREATE TABLE "ContentGenre" (
    id integer DEFAULT nextval('public."ContentGenre_ID_seq"'::text) NOT NULL,
    "Content_id" integer NOT NULL,
    "FieldNames" integer,
    "Genre_id" integer NOT NULL
);


--
-- TOC entry 84 (OID 12753248)
-- Name: ContentGenre; Type: ACL; Schema: public; Owner: jbwhite
--

REVOKE ALL ON TABLE "ContentGenre" FROM PUBLIC;
GRANT INSERT,SELECT,DELETE ON TABLE "ContentGenre" TO digmast_user;


--
-- TOC entry 85 (OID 12753336)
-- Name: Dawson_Grant_Rights ; Type: VIEW; Schema: public; Owner: jbwhite
--

CREATE VIEW "Dawson_Grant_Rights " AS
    SELECT "Content"."ID", "Content"."RecordIDType", "Content"."OtherID", "Content"."DateCreated", "Content"."DateModified", "Content"."Collection Number", "Content"."Title", "Content"."Subtitle", "Content"."ResourceType", "Content"."Language1", "Content"."Language2", "Content"."Location", "Content"."Abstract", "Content"."TOC", "Content"."ContentNotes", "Content"."CompletedBy", "Content"."CompletedDate", "Content"."Complete", "RightsAccess"."RestrictionOther", "Name"."Name", "RightsAccess"."CopyrightDate", "Restrictions"."RestrictionList" FROM (((("TechImages" LEFT JOIN "Content" ON (("TechImages"."Content#" = "Content"."ID"))) LEFT JOIN "RightsAccess" ON (("RightsAccess"."Content#" = "Content"."ID"))) LEFT JOIN "Restrictions" ON (("Restrictions"."ID" = "RightsAccess"."Restriction"))) LEFT JOIN "Name" ON (("Name"."ID" = "RightsAccess"."Name"))) WHERE ("ImageNote" = 'Dawson Grant'::text);


--
-- TOC entry 86 (OID 12753336)
-- Name: Dawson_Grant_Rights ; Type: ACL; Schema: public; Owner: jbwhite
--

REVOKE ALL ON TABLE "Dawson_Grant_Rights " FROM PUBLIC;
GRANT SELECT ON TABLE "Dawson_Grant_Rights " TO kskinne;


--
-- Data for TOC entry 218 (OID 12738943)
-- Name: CodecCreatorSound; Type: TABLE DATA; Schema: public; Owner: jbwhite
--

COPY "CodecCreatorSound" ("ID", "Hardware", "Software", "SoftwareVersion") FROM stdin;
1	Mac G4	DigiDesign ProTools LE	5.2
2	Mac G5	DigiDesign ProTools LE	6.7
3	Unknown	Unknown	Unknown
\.


--
-- Data for TOC entry 219 (OID 12739959)
-- Name: Condition; Type: TABLE DATA; Schema: public; Owner: jbwhite
--

COPY "Condition" ("ID", "Condition") FROM stdin;
14	torn
16	wrinkled
17	staining from water damage
19	creased
\.


--
-- Data for TOC entry 220 (OID 12739971)
-- Name: ConditionDetail; Type: TABLE DATA; Schema: public; Owner: jbwhite
--

COPY "ConditionDetail" ("ContentID", "ConditionID") FROM stdin;
525	17
632	14
637	14
644	14
\.


--
-- Data for TOC entry 221 (OID 12739985)
-- Name: Content; Type: TABLE DATA; Schema: public; Owner: jbwhite
--

COPY "Content" ("ID", "RecordIDType", "OtherID", "DateCreated", "DateModified", "Collection Number", "Title", "Subtitle", "ResourceType", "Language1", "Language2", "Location", "Abstract", "TOC", "ContentNotes", "CompletedBy", "CompletedDate", "Complete") FROM stdin;
9	local	00000029	2006-02-28 00:00:00	2006-02-28 00:00:00	826	Recording of the Wayne State University Men's Glee Club, (Detroit, Michigan,) 9 March 1974	\N	16	25	140	1	William Levi Dawson was the guest conductor of the 90 voice Men's Glee Club during the Wayne State University Department of Music's Winter Festival.	\N	This is side B of the audiocassette.	\N	\N	\N
10	local	00000030	2006-02-28 00:00:00	2006-02-28 00:00:00	826	Recording of the Wayne State University Men's Glee Club, (Detroit, Michigan,) 9 March 1974	\N	16	25	140	1	William Levi Dawson was the guest conductor of the 90 voice Men's Glee Club during the Wayne State University Department of Music's Winter Festival.	\N	\N	\N	\N	\N
11	local	00000031	2006-02-28 00:00:00	2006-02-28 00:00:00	826	Recording of the Wayne State University Men's Glee Club Alumni Concert, (Detroit, Michigan,) 20 March 1976	\N	16	25	140	1	William Levi Dawson was the guest conductor.	\N	\N	\N	\N	\N
12	local	00000032	2006-02-28 00:00:00	2006-02-28 00:00:00	826	Recording of "The Black Composer", WHRO, (Hampton Roads, Virginia), 12 March 1979	\N	16	25	140	1	\N	\N	This is side A of the audiocassette.	\N	\N	\N
13	local	00000033	2006-02-28 00:00:00	2006-02-28 00:00:00	826	Recording of "The Black Composer", WHRO, (Hampton Roads, Virginia), 12 March 1979	\N	16	25	140	1	\N	\N	This is side B of the audiocassette.	\N	\N	\N
14	local	00000034	2006-02-28 00:00:00	2006-02-28 00:00:00	826	Recording of a concert by the Mendelssohn Singers, (Philadelphia, Pennsylvania,) 20 November 1981	\N	16	25	140	1	This concert was a tribute to William Levi Dawson and Dawson conducted the singers.  The concert was related to the Creative Artists' Workshop of Philadelphia.	\N	Mendelssohn Singers and John Russell, Creative Artists' Workshop of Philadelphia, November 20, 1981	\N	\N	\N
15	local	00000035	2006-02-28 00:00:00	2006-02-28 00:00:00	826	Mendelssohn Singers, Philadelphia, Pennsylvania	\N	16	25	140	1	\N	Tribute to WLD, WLD conducting	\N	\N	\N	\N
16	local	00000036	2006-02-28 00:00:00	2006-02-28 00:00:00	826	National Public Radio "The Sunday Show"	\N	16	25	140	1	\N	Interview with WLD recorded and broadcast on NPR about the Negro Folk Symphony	\N	\N	\N	\N
17	local	00000037	2006-02-28 00:00:00	2006-02-28 00:00:00	826	Louisiana All-State Choir	\N	16	25	140	1	\N	WLD conducting	\N	\N	\N	\N
18	local	00000038	2006-02-28 00:00:00	2006-02-28 00:00:00	826	Union Baptist Church Choir, Baltimore, Maryland	\N	16	25	140	1	\N	WLD conducting	\N	\N	\N	\N
19	local	00000039	2006-02-28 00:00:00	2006-02-28 00:00:00	826	Union Baptist Church Choir, Baltimore Maryland	\N	16	25	140	1	\N	WLD conducting	\N	\N	\N	\N
20	local	00000040	2006-02-28 00:00:00	2006-02-28 00:00:00	826	WQXR-FM New York, New York	\N	16	25	140	1	\N	Features WLD and plays 2nd movement of the Negro Folk Symphony, "Hope in the Night"	\N	\N	\N	\N
21	local	00000041	2006-02-28 00:00:00	2006-02-28 00:00:00	676	Roberto Goizueta 1	\N	8	25	140	1	\N	\N	\N	\N	\N	\N
22	local	00000042	2006-02-28 00:00:00	2006-02-28 00:00:00	676	Roberto Goizueta 2	\N	8	25	140	1	\N	\N	\N	\N	\N	\N
23	local	00000043	2006-02-28 00:00:00	2006-02-28 00:00:00	0	Ira Herbert	\N	8	25	140	1	\N	\N	Chief of advertising at Coke, starts late 1960s	\N	\N	\N
24	local	00000044	2006-02-28 00:00:00	2006-02-28 00:00:00	0	Donald Keough 1	\N	8	25	140	1	\N	\N	\N	\N	\N	\N
25	local	00000045	2006-02-28 00:00:00	2006-02-28 00:00:00	0	Donald Keough 2	\N	8	25	140	1	\N	\N	\N	\N	\N	\N
26	local	00000046	2006-02-28 00:00:00	2006-02-28 00:00:00	0	Ralph Cooper 1	\N	8	25	140	1	\N	\N	At Coke 1965 to 2000, president at end	\N	\N	\N
27	local	00000047	2006-02-28 00:00:00	2006-02-28 00:00:00	0	Ralph Cooper 2	\N	8	25	140	1	\N	\N	At Coke 1965 to 2000, president at end	\N	\N	\N
28	local	00000048	2006-02-28 00:00:00	2006-02-28 00:00:00	0	M. Douglas Ivester	\N	8	25	140	1	\N	\N	\N	\N	\N	\N
29	local	00000049	2006-02-28 00:00:00	2006-02-28 00:00:00	0	Carlton Curtis 1	\N	8	25	140	1	\N	\N	Public spokesman for Coke 80s	\N	\N	\N
30	local	00000050	2006-02-28 00:00:00	2006-02-28 00:00:00	0	Carlton Curtis 2	\N	8	25	140	1	\N	\N	Public spokesman for Coke 80s	\N	\N	\N
31	local	00000051	2006-02-28 00:00:00	2006-02-28 00:00:00	0	Carl Ware	\N	8	25	140	1	\N	\N	\N	\N	\N	\N
32	local	00000052	2006-02-28 00:00:00	2006-02-28 00:00:00	0	Garth Hamby 1	\N	8	25	140	1	\N	\N	Coke's corporate secretary circa 1980.	\N	\N	\N
33	local	00000053	2006-02-28 00:00:00	2006-02-28 00:00:00	0	Garth Hamby 2	\N	8	25	140	1	\N	\N	Coke's corporate secretary circa 1980.	\N	\N	\N
34	local	00000054	2006-02-28 00:00:00	2006-02-28 00:00:00	826	Fisk University Choir [1 of 2]	\N	16	25	140	1	\N	Tape blank	\N	\N	\N	\N
35	local	00000055	2006-02-28 00:00:00	2006-02-28 00:00:00	826	Fisk University Choir [2 of 2]	\N	16	25	140	1	\N	Hiawatha's Wedding-Feast Tape blank	\N	\N	\N	\N
36	local	00000056	2006-02-28 00:00:00	2006-02-28 00:00:00	826	Stephen Smith Home for the Aged Benefit, Philadelphia, Pennsylvania [1 of 2]	\N	16	25	140	1	\N	\N	recorded in Philadelphia	\N	\N	\N
37	local	00000057	2006-02-28 00:00:00	2006-02-28 00:00:00	826	Stephen Smith Home for the Aged Benefit, Philadelphia, Pennsylvania [2 of 2]	\N	16	25	140	1	\N	\N	recorded in Philadelphia	\N	\N	\N
38	local	00000058	2006-02-28 00:00:00	2006-02-28 00:00:00	826	William L. Dawson interview, Philadelphia, Pennsylvania	\N	16	25	140	1	\N	\N	Recorded in conjunction with the "Stephen Smith Home for the Aged Benefit"	\N	\N	\N
39	local	00000059	2006-02-28 00:00:00	2006-02-28 00:00:00	826	UNABLE TO TRANSFER Fisk University panel discussion: Martha M. Brown (Tennessee A&I State University), William Dawson, Aaron Douglas (Fisk University), Mrs. Janus C. Lee (mother of WLD)	\N	16	25	140	1	\N	\N	Recorded in conjunction with the "Stephen Smith Home for the Aged Benefit"	\N	\N	\N
40	local	00000060	2006-02-28 00:00:00	2006-02-28 00:00:00	826	Out in the Fields	\N	16	25	140	1	\N	solo soprano with orchestra	\N	\N	\N	\N
41	local	00000061	2006-02-28 00:00:00	2006-02-28 00:00:00	826	George Washington Carver speech at Selma University commencement, Selma, Alabama	\N	16	25	140	1	\N	\N	recording of commercial broadcast [?]	\N	\N	\N
42	local	00000062	2006-02-28 00:00:00	2006-02-28 00:00:00	826	Huntsville Symphony, Negro Folk Symphony	\N	16	25	140	1	\N	\N	\N	\N	\N	\N
43	local	00000063	2006-02-28 00:00:00	2006-02-28 00:00:00	826	Fela Sowande, "Wedding Day" and other unidentified piece	\N	16	25	140	1	\N	\N	Dawson present at performance	\N	\N	\N
44	local	00000064	2006-02-28 00:00:00	2006-02-28 00:00:00	0	George Royal	\N	8	25	140	1	\N	\N	\N	\N	\N	\N
45	local	00000065	2006-02-28 00:00:00	2006-02-28 00:00:00	0	George Royal	\N	8	25	140	1	\N	\N	\N	\N	\N	\N
46	local	00000066	2006-02-28 00:00:00	2006-02-28 00:00:00	0	Morris Redding	\N	8	25	140	1	\N	\N	\N	\N	\N	\N
47	local	00000067	2006-02-28 00:00:00	2006-02-28 00:00:00	0	Morris Redding	\N	8	25	140	1	\N	\N	\N	\N	\N	\N
48	local	00000068	2006-02-28 00:00:00	2006-02-28 00:00:00	0	William Tut Johnson 3	\N	8	25	140	1	\N	\N	First eight minutes of recording extremely distorted-tape creased	\N	\N	\N
49	local	00000070	2006-02-28 00:00:00	2006-02-28 00:00:00	0	H. Burke Nicholson 1	\N	8	25	140	1	\N	\N	\N	\N	\N	\N
50	local	00000071	2006-02-28 00:00:00	2006-02-28 00:00:00	0	H. Burke Nicholson 2	\N	8	25	140	1	\N	\N	\N	\N	\N	\N
51	local	00000072	2006-02-28 00:00:00	2006-02-28 00:00:00	0	H. Burke Nicholson 3	\N	8	25	140	1	\N	\N	\N	\N	\N	\N
52	local	00000073	2006-02-28 00:00:00	2006-02-28 00:00:00	0	H. Burke Nicholson 4	\N	8	25	140	1	\N	\N	\N	\N	\N	\N
53	local	00000074	2006-02-28 00:00:00	2006-02-28 00:00:00	0	H. Burke Nicholson 5	\N	8	25	140	1	\N	\N	\N	\N	\N	\N
54	local	00000075	2006-02-28 00:00:00	2006-02-28 00:00:00	0	H. Burke Nicholson 6	\N	8	25	140	1	\N	\N	\N	\N	\N	\N
55	local	00000076	2006-02-28 00:00:00	2006-02-28 00:00:00	676	H. Burke Nicholson 7	\N	16	25	140	1	\N	\N	\N	\N	\N	\N
56	local	00000077	2006-02-28 00:00:00	2006-02-28 00:00:00	0	Charles Bottoms 3	\N	8	25	140	1	\N	\N	\N	\N	\N	\N
57	local	00000078	2006-02-28 00:00:00	2006-02-28 00:00:00	0	Charles Bottoms 4	\N	8	25	140	1	\N	\N	\N	\N	\N	\N
58	local	00000079	2006-02-28 00:00:00	2006-02-28 00:00:00	0	Charles Bottoms 5	\N	8	25	140	1	\N	\N	\N	\N	\N	\N
59	local	00000080	2006-02-28 00:00:00	2006-02-28 00:00:00	0	Charles Bottoms 6	\N	8	25	140	1	\N	\N	\N	\N	\N	\N
60	local	00000081	2006-02-28 00:00:00	2006-02-28 00:00:00	0	Charles Bottoms 1	\N	8	25	140	1	\N	\N	\N	\N	\N	\N
61	local	00000082	2006-02-28 00:00:00	2006-02-28 00:00:00	0	Charles Bottoms 2	\N	8	25	140	1	\N	\N	\N	\N	\N	\N
62	local	00000083	2006-02-28 00:00:00	2006-02-28 00:00:00	0	Charles Elliott 1	\N	8	25	140	1	\N	\N	\N	\N	\N	\N
63	local	00000084	2006-02-28 00:00:00	2006-02-28 00:00:00	0	Charles Elliott 2	\N	8	25	140	1	\N	\N	\N	\N	\N	\N
64	local	00000085	2006-02-28 00:00:00	2006-02-28 00:00:00	0	Claus Halle 1	\N	8	25	140	1	\N	\N	\N	\N	\N	\N
65	local	00000086	2006-02-28 00:00:00	2006-02-28 00:00:00	0	Claus Halle 2	\N	8	25	140	1	\N	\N	\N	\N	\N	\N
66	local	00000087	2006-02-28 00:00:00	2006-02-28 00:00:00	0	Claus Halle 3	\N	8	25	140	1	\N	\N	\N	\N	\N	\N
67	local	00000088	2006-02-28 00:00:00	2006-02-28 00:00:00	0	Claus Halle 4	\N	8	25	140	1	\N	\N	\N	\N	\N	\N
68	local	00000089	2006-02-28 00:00:00	2006-02-28 00:00:00	0	Claus Halle 5	\N	8	25	140	1	\N	\N	\N	\N	\N	\N
69	local	00000090	2006-02-28 00:00:00	2006-02-28 00:00:00	0	Claus Halle 6	\N	8	25	140	1	\N	\N	\N	\N	\N	\N
70	local	00000091	2006-02-28 00:00:00	2006-02-28 00:00:00	0	Morton Hodgson 1	\N	8	25	140	1	\N	\N	\N	\N	\N	\N
71	local	00000092	2006-02-28 00:00:00	2006-02-28 00:00:00	0	Morton Hodgson 2	\N	8	25	140	1	\N	\N	\N	\N	\N	\N
72	local	00000093	2006-02-28 00:00:00	2006-02-28 00:00:00	0	Joseph W. Jones 1	\N	8	25	140	1	\N	\N	\N	\N	\N	\N
73	local	00000094	2006-02-28 00:00:00	2006-02-28 00:00:00	0	Joseph W. Jones 2	\N	8	25	140	1	\N	\N	\N	\N	\N	\N
74	local	00000095	2006-02-28 00:00:00	2006-02-28 00:00:00	0	Wilbur Kurtz 1	\N	8	25	140	1	\N	\N	\N	\N	\N	\N
75	local	00000096	2006-02-28 00:00:00	2006-02-28 00:00:00	0	Wilbur Kurtz 2	\N	8	25	140	1	\N	\N	\N	\N	\N	\N
76	local	00000097	2006-02-28 00:00:00	2006-02-28 00:00:00	0	Wilbur Kurtz 3	\N	8	25	140	1	\N	\N	\N	\N	\N	\N
77	local	00000098	2006-02-28 00:00:00	2006-02-28 00:00:00	0	Wilbur Kurtz 4	\N	8	25	140	1	\N	\N	\N	\N	\N	\N
78	local	00000099	2006-02-28 00:00:00	2006-02-28 00:00:00	0	Joseph W. Jones 3	\N	8	25	140	1	\N	\N	\N	\N	\N	\N
79	local	00000100	2006-02-28 00:00:00	2006-02-28 00:00:00	0	Joseph W. Jones 4	\N	8	25	140	1	\N	\N	\N	\N	\N	\N
80	local	00000101	2006-02-28 00:00:00	2006-02-28 00:00:00	0	J. Arch Avery 1	\N	8	25	140	1	\N	\N	\N	\N	\N	\N
81	local	00000102	2006-02-28 00:00:00	2006-02-28 00:00:00	0	John Beach 1	\N	8	25	140	1	\N	\N	\N	\N	\N	\N
82	local	00000103	2006-02-28 00:00:00	2006-02-28 00:00:00	0	Sam Ayoub 1	\N	8	25	140	1	\N	\N	\N	\N	\N	\N
83	local	00000104	2006-02-28 00:00:00	2006-02-28 00:00:00	0	Sam Ayoub 2	\N	8	25	140	1	\N	\N	\N	\N	\N	\N
84	local	00000105	2006-02-28 00:00:00	2006-02-28 00:00:00	0	H1 Retirement dinner for Dean Rece, Emory. Proceeding at dinner honoring Mr. Ellis Heber Rece, held in Cox Hall. Dr. Jack Boozer, presiding.	\N	8	25	140	1	\N	3 3/4 2T T1&2	\N	\N	\N	\N
85	local	00000106	2006-02-28 00:00:00	2006-02-28 00:00:00	0	H1 Retirement dinner for Dean Rece, Emory. Proceeding at dinner honoring Mr. Ellis Heber Rece, held in Cox Hall. Dr. Jack Boozer, presiding.	\N	8	25	140	1	\N	3.75 ips  2T	\N	\N	\N	\N
86	local	00000107	2006-02-28 00:00:00	2006-02-28 00:00:00	0	H2 Dean Ellis Heber Rece Panel Discussion Held in Biology 106. On the last half of track 2 is the sermon Mr. Rece preached at the University worship in Durham Chapel.	\N	8	25	140	1	\N	3.75 ips  2T	\N	\N	\N	\N
87	local	00000108	2006-02-28 00:00:00	2006-02-28 00:00:00	0	H2 Dean Ellis Heber Rece Panel Discussion Held in Biology 106. On the last half of Track 2 is the sermon Mr. Rece preached at the University worship in Durham Chapel.	\N	8	25	140	1	\N	3.75 ips  2T	\N	\N	\N	\N
88	local	00000109	2006-02-28 00:00:00	2006-02-28 00:00:00	0	H3 Ellis Hebe Rece Reminiscences	\N	8	25	140	1	\N	3.75ips 1T	\N	\N	\N	\N
89	local	00000110	2006-02-28 00:00:00	2006-02-28 00:00:00	0	H4 William Swoll (Huck) Sawyer. Interview given at Emory in which Mr. Sawyer talks of events and personalities on Emory campuses at Oxford, 1912-24 and at Atlanta, 1920-25.	\N	8	25	140	1	\N	3.75 2T,T1&2	\N	\N	\N	\N
90	local	00000112	2006-02-28 00:00:00	2006-02-28 00:00:00	826	When I was sinking down etc Side 1	\N	16	25	140	1	\N	Recording studio: American Broadcasting Company	\N	\N	\N	\N
91	local	00000113	2006-02-28 00:00:00	2006-02-28 00:00:00	826	Every time I feel the spirit [?] Side 2	\N	16	25	140	1	\N	Recording studio: American Broadcasting Company	\N	\N	\N	\N
92	local	00000114	2006-02-28 00:00:00	2006-02-28 00:00:00	826	Salvation is created Side 3	\N	16	25	140	1	\N	Recording studio: American Broadcasting Company	\N	\N	\N	\N
93	local	00000115	2006-02-28 00:00:00	2006-02-28 00:00:00	826	Every time I feel the spirit [?] Side 4	\N	16	25	140	1	\N	Recording studio: American Broadcasting Company	\N	\N	\N	\N
94	local	00000116	2006-02-28 00:00:00	2006-02-28 00:00:00	826	Side 1	\N	16	25	140	1	\N	Recording studio: American Broadcasting Company	\N	\N	\N	\N
95	local	00000117	2006-02-28 00:00:00	2006-02-28 00:00:00	826	Side 2	\N	16	25	140	1	\N	Recording studio: American Broadcasting Company	\N	\N	\N	\N
96	local	00000118	2006-02-28 00:00:00	2006-02-28 00:00:00	826	Side 3	\N	16	25	140	1	\N	Recording studio: American Broadcasting Company	\N	\N	\N	\N
97	local	00000119	2006-02-28 00:00:00	2006-02-28 00:00:00	826	Side 4	\N	16	25	140	1	\N	Recording studio: American Broadcasting Company	\N	\N	\N	\N
98	local	00000120	2006-02-28 00:00:00	2006-02-28 00:00:00	826	Lit' Boy Chile Side 1	\N	16	25	140	1	\N	Recording studio: American Broadcasting Company	\N	\N	\N	\N
99	local	00000121	2006-02-28 00:00:00	2006-02-28 00:00:00	826	Lit' Boy Chile Side 2	\N	16	25	140	1	\N	Recording studio: American Broadcasting Company	\N	\N	\N	\N
100	local	00000122	2006-02-28 00:00:00	2006-02-28 00:00:00	826	Lit' Boy Chile Side 3	\N	16	25	140	1	\N	Recording studio: American Broadcasting Company	\N	\N	\N	\N
101	local	00000123	2006-02-28 00:00:00	2006-02-28 00:00:00	0	Christmas Side 4	\N	8	25	140	1	\N	Recording studio: American Broadcasting Company	\N	\N	\N	\N
102	local	00000124	2006-02-28 00:00:00	2006-02-28 00:00:00	0	Christian Foreign Service Convocation Program Side 1	\N	8	25	140	1	\N	Recording studio: Champion	\N	\N	\N	\N
103	local	00000125	2006-02-28 00:00:00	2006-02-28 00:00:00	0	Christian Foreign Service Convocation Program Side 2	\N	8	25	140	1	\N	Recording studio: Champion	\N	\N	\N	\N
104	local	00000126	2006-02-28 00:00:00	2006-02-28 00:00:00	0	NBC Program October 10, 1937 1	\N	8	25	140	1	\N	Recording studio: National Broadcasting Company	\N	\N	\N	\N
105	local	00000127	2006-02-28 00:00:00	2006-02-28 00:00:00	0	NBC Program October 10, 1937 2	\N	8	25	140	1	\N	Recording studio: National Broadcasting Company	\N	\N	\N	\N
106	local	00000128	2006-02-28 00:00:00	2006-02-28 00:00:00	0	NBC Program October 10, 1937 3	\N	8	25	140	1	\N	Recording studio: National Broadcasting Company	\N	\N	\N	\N
107	local	00000129	2006-02-28 00:00:00	2006-02-28 00:00:00	0	NBC Program October 10, 1937 4	\N	8	25	140	1	\N	Recording studio: National Broadcasting Company	\N	\N	\N	\N
108	local	00000130	2006-02-28 00:00:00	2006-02-28 00:00:00	0	NBC Program October 10, 1937 5	\N	8	25	140	1	\N	Recording studio: National Broadcasting Company	\N	\N	\N	\N
109	local	00000131	2006-02-28 00:00:00	2006-02-28 00:00:00	0	NBC Program October 10, 1937 6	\N	8	25	140	1	\N	Recording studio: National Broadcasting Company	\N	\N	\N	\N
110	local	00000132	2006-02-28 00:00:00	2006-02-28 00:00:00	0	NBC Program October 10, 1937 7	\N	8	25	140	1	\N	Recording studio: National Broadcasting Company	\N	\N	\N	\N
111	local	00000133	2006-02-28 00:00:00	2006-02-28 00:00:00	0	NBC Program October 10, 1937 8	\N	8	25	140	1	\N	Recording studio: National Broadcasting Company	\N	\N	\N	\N
112	local	00000134	2006-02-28 00:00:00	2006-02-28 00:00:00	0	Negro work song	\N	8	25	140	1	\N	Recording studio: Rockhill	\N	\N	\N	\N
113	local	00000135	2006-02-28 00:00:00	2006-02-28 00:00:00	0	Negro work song	\N	8	25	140	1	\N	Recording studio: Universal	\N	\N	\N	\N
114	local	00000136	2006-02-28 00:00:00	2006-02-28 00:00:00	0	Philadelphia [recorded for WLD] Side 1	\N	8	25	140	1	\N	Recording studio: Crest Recording Studio	\N	\N	\N	\N
115	local	00000137	2006-02-28 00:00:00	2006-02-28 00:00:00	0	Philadelphia [recorded for WLD] Side 2	\N	8	25	140	1	\N	Recording studio: Crest Recording Studio	\N	\N	\N	\N
116	local	00000138	2006-02-28 00:00:00	2006-02-28 00:00:00	0	Philadelphia [recorded for WLD] Side 3	\N	8	25	140	1	\N	Recording studio: Crest Recording Studio	\N	\N	\N	\N
117	local	00000139	2006-02-28 00:00:00	2006-02-28 00:00:00	0	Philadelphia [recorded for WLD] Side 4	\N	8	25	140	1	\N	Recording studio: Crest Recording Studio	\N	\N	\N	\N
118	local	00000140	2006-02-28 00:00:00	2006-02-28 00:00:00	0	Crucifixion Side 1	\N	8	25	140	1	\N	Recording studio: Presto	\N	\N	\N	\N
119	local	00000141	2006-02-28 00:00:00	2006-02-28 00:00:00	0	Crucifixion Side 2	\N	8	25	140	1	\N	Recording studio: Presto	\N	\N	\N	\N
120	local	00000142	2006-02-28 00:00:00	2006-02-28 00:00:00	0	Sicilienne by Von Paradis; Violin and Piano by G. Errington Kerr	\N	8	25	140	1	\N	Recording studio: Presto	\N	\N	\N	\N
121	local	00000143	2006-02-28 00:00:00	2006-02-28 00:00:00	0	Think on me Side 1	\N	8	25	140	1	\N	Recording studio: Unknown	\N	\N	\N	\N
122	local	00000144	2006-02-28 00:00:00	2006-02-28 00:00:00	0	When I have sung my songs for you Side 2	\N	8	25	140	1	\N	Recording studio: Unknown	\N	\N	\N	\N
123	local	00000145	2006-02-28 00:00:00	2006-02-28 00:00:00	0	Onaway! Awake, Beloved! (S. Coleridge-Taylor) Side 1	\N	8	25	140	1	\N	Recording studio: Promotional Recording Star Artists Bureau, N.Y.	\N	\N	\N	\N
124	local	00000146	2006-02-28 00:00:00	2006-02-28 00:00:00	0	Onaway! Awake, Beloved! (S. Coleridge-Taylor) Side 2	\N	8	25	140	1	\N	Recording studio: Promotional Recording Star Artists Bureau, N.Y.	\N	\N	\N	\N
125	local	00000147	2006-02-28 00:00:00	2006-02-28 00:00:00	0	Dahomey and Nigeria #14 and #15, Kokoro etc. Side 1	\N	8	25	140	1	\N	Recording studio: Audio Devices	\N	\N	\N	\N
126	local	00000148	2006-02-28 00:00:00	2006-02-28 00:00:00	0	Dahomey and Nigeria #14 and #15, Kokoro etc. Side 2	\N	8	25	140	1	\N	Recording studio: Audio Devices	\N	\N	\N	\N
127	local	00000149	2006-02-28 00:00:00	2006-02-28 00:00:00	0	Unknown Side 1	\N	8	25	140	1	\N	Recording studio: Musicological Records	\N	\N	\N	\N
128	local	00000150	2006-02-28 00:00:00	2006-02-28 00:00:00	0	Unknown Side 2	\N	8	25	140	1	\N	Recording studio: Musicological Records	\N	\N	\N	\N
129	local	00000151	2006-02-28 00:00:00	2006-02-28 00:00:00	0	Negro Folk Symphony Side 1	\N	8	25	140	1	\N	Recording studio: Sesac Recordings	\N	\N	\N	\N
130	local	00000152	2006-02-28 00:00:00	2006-02-28 00:00:00	0	Negro Folk Symphony Side 2	\N	8	25	140	1	\N	Recording studio: Sesac Recordings	\N	\N	\N	\N
131	local	00000153	2006-02-28 00:00:00	2006-02-28 00:00:00	0	Go Down Moses Side 1	\N	8	25	140	1	\N	Recording studio: Star Artists Bureau, N.Y.	\N	\N	\N	\N
132	local	00000154	2006-02-28 00:00:00	2006-02-28 00:00:00	0	Le Reve	\N	8	25	140	1	\N	Recording studio: Star Artists Bureau, N.Y.	\N	\N	\N	\N
133	local	00000155	2006-02-28 00:00:00	2006-02-28 00:00:00	0	My God is So High	\N	8	25	140	1	\N	Recording studio: Audio Disk (6073)	\N	\N	\N	\N
134	local	00000156	2006-02-28 00:00:00	2006-02-28 00:00:00	0	My God is So High	\N	8	25	140	1	\N	Recording studio: G. Schirmer, Inc.	\N	\N	\N	\N
135	local	00000157	2006-02-28 00:00:00	2006-02-28 00:00:00	0	Ye people, rend your hearts Side 1	\N	8	25	140	1	\N	Recording studio: Star Artists Bureau, N.Y.	\N	\N	\N	\N
136	local	00000158	2006-02-28 00:00:00	2006-02-28 00:00:00	0	La Boheme Side 2	\N	8	25	140	1	\N	Recording studio: Star Artists Bureau, N.Y.	\N	\N	\N	\N
137	local	00000159	2006-02-28 00:00:00	2006-02-28 00:00:00	0	Cecil Boogie	\N	8	25	140	1	\N	Recording studio: Gilt-edge Flexitone Records	\N	\N	\N	\N
138	local	00000160	2006-02-28 00:00:00	2006-02-28 00:00:00	0	I wonder	\N	8	25	140	1	\N	Recording studio: Gilt-edge Flexitone Records	\N	\N	\N	\N
139	local	00000161	2006-02-28 00:00:00	2006-02-28 00:00:00	0	Ain't that Good News	\N	8	25	140	1	\N	Recording studio: Ohio Recording Service	\N	\N	\N	\N
140	local	00000162	2006-02-28 00:00:00	2006-02-28 00:00:00	0	Finlandia	\N	8	25	140	1	\N	Recording studio: Ohio Recording Service	\N	\N	\N	\N
141	local	00000163	2006-02-28 00:00:00	2006-02-28 00:00:00	0	Ain't that Good News	\N	8	25	140	1	\N	Recording studio: Unknown	\N	\N	\N	\N
142	local	00000164	2006-02-28 00:00:00	2006-02-28 00:00:00	0	Deep River 1	\N	8	25	140	1	\N	Recording studio: Champion Recording Corp.	\N	\N	\N	\N
143	local	00000165	2006-02-28 00:00:00	2006-02-28 00:00:00	0	Deep River 2	\N	8	25	140	1	\N	Recording studio: Champion Recording Corp.	\N	\N	\N	\N
144	local	00000166	2006-02-28 00:00:00	2006-02-28 00:00:00	0	Ain't that Good News	\N	8	25	140	1	\N	Recording studio: Unknown	\N	\N	\N	\N
145	local	00000167	2006-02-28 00:00:00	2006-02-28 00:00:00	0	Hiawatha's Wedding Feast (Samuel Coleridge-Taylor) 1	\N	8	25	140	1	\N	Recording studio: Presto	\N	\N	\N	\N
146	local	00000168	2006-02-28 00:00:00	2006-02-28 00:00:00	0	Hiawatha's Wedding Feast (Samuel Coleridge-Taylor) 2	\N	8	25	140	1	\N	Recording studio: Presto	\N	\N	\N	\N
147	local	00000169	2006-02-28 00:00:00	2006-02-28 00:00:00	0	Jean	\N	8	25	140	1	\N	Recording studio: Presto	\N	\N	\N	\N
148	local	00000170	2006-02-28 00:00:00	2006-02-28 00:00:00	0	Old Man River	\N	8	25	140	1	\N	Recording studio: Presto	\N	\N	\N	\N
149	local	00000171	2006-02-28 00:00:00	2006-02-28 00:00:00	0	In the Fields 1	\N	8	25	140	1	\N	Recording studio: Audio Disc	\N	\N	\N	\N
150	local	00000172	2006-02-28 00:00:00	2006-02-28 00:00:00	0	In the Fields 2	\N	8	25	140	1	\N	Recording studio: Audio Disc	\N	\N	\N	\N
151	local	00000173	2006-02-28 00:00:00	2006-02-28 00:00:00	0	Slow thru the dark 1	\N	8	25	140	1	\N	Recording studio: Nola Recording Studio	\N	\N	\N	\N
152	local	00000174	2006-02-28 00:00:00	2006-02-28 00:00:00	0	Slow thru the dark 2	\N	8	25	140	1	\N	Recording studio: Nola Recording Studio	\N	\N	\N	\N
153	local	00000175	2006-02-28 00:00:00	2006-02-28 00:00:00	0	Booker T. Stamp Commemoration (NBC) 1	\N	8	25	140	1	\N	Recording studio: Presto	\N	\N	\N	\N
154	local	00000176	2006-02-28 00:00:00	2006-02-28 00:00:00	0	Booker T. Stamp Commemoration (NBC) 2	\N	8	25	140	1	\N	Recording studio: Presto	\N	\N	\N	\N
155	local	00000177	2006-02-28 00:00:00	2006-02-28 00:00:00	0	Booker T. Stamp Commemoration (NBC) 3	\N	8	25	140	1	\N	Recording studio: Presto	\N	\N	\N	\N
156	local	00000178	2006-02-28 00:00:00	2006-02-28 00:00:00	0	Booker T. Stamp Commemoration (NBC) 4	\N	8	25	140	1	\N	Recording studio: Presto	\N	\N	\N	\N
157	local	00000179	2006-02-28 00:00:00	2006-02-28 00:00:00	0	Unknown (2251) 1	\N	8	25	140	1	\N	Recording studio: Audio Disc	\N	\N	\N	\N
158	local	00000180	2006-02-28 00:00:00	2006-02-28 00:00:00	0	Unknown (2251) 2	\N	8	25	140	1	\N	Recording studio: Audio Disc	\N	\N	\N	\N
159	local	00000181	2006-02-28 00:00:00	2006-02-28 00:00:00	0	Unknown (2251) 3	\N	8	25	140	1	\N	Recording studio: Audio Disc	\N	\N	\N	\N
160	local	00000182	2006-02-28 00:00:00	2006-02-28 00:00:00	0	Unknown (2251) 4	\N	8	25	140	1	\N	Recording studio: Audio Disc	\N	\N	\N	\N
161	local	00000183	2006-02-28 00:00:00	2006-02-28 00:00:00	0	Unknown 1	\N	8	25	140	1	\N	Recording studio: Unknown	\N	\N	\N	\N
162	local	00000184	2006-02-28 00:00:00	2006-02-28 00:00:00	0	Unknown 2	\N	8	25	140	1	\N	Recording studio: Unknown	\N	\N	\N	\N
163	local	00000185	2006-02-28 00:00:00	2006-02-28 00:00:00	0	Unknown 3	\N	8	25	140	1	\N	Recording studio: Unknown	\N	\N	\N	\N
164	local	00000186	2006-02-28 00:00:00	2006-02-28 00:00:00	0	Unknown 4	\N	8	25	140	1	\N	Recording studio: Unknown	\N	\N	\N	\N
165	local	00000187	2006-02-28 00:00:00	2006-02-28 00:00:00	0	Christmas Concert 1	\N	8	25	140	1	\N	Recording studio: Broadcast Recording	\N	\N	\N	\N
166	local	00000188	2006-02-28 00:00:00	2006-02-28 00:00:00	0	Christmas Concert 2	\N	8	25	140	1	\N	Recording studio: Broadcast Recording	\N	\N	\N	\N
167	local	00000189	2006-02-28 00:00:00	2006-02-28 00:00:00	0	Christmas Concert 3	\N	8	25	140	1	\N	Recording studio: Broadcast Recording	\N	\N	\N	\N
168	local	00000190	2006-02-28 00:00:00	2006-02-28 00:00:00	0	Christmas Concert 4	\N	8	25	140	1	\N	Recording studio: Broadcast Recording	\N	\N	\N	\N
169	local	00000191	2006-02-28 00:00:00	2006-02-28 00:00:00	0	Christmas Concert 5	\N	8	25	140	1	\N	Recording studio: Broadcast Recording	\N	\N	\N	\N
170	local	00000192	2006-02-28 00:00:00	2006-02-28 00:00:00	0	Christmas Concert 6	\N	8	25	140	1	\N	Recording studio: Broadcast Recording	\N	\N	\N	\N
171	local	00000193	2006-02-28 00:00:00	2006-02-28 00:00:00	0	Christmas Concert 7	\N	8	25	140	1	\N	Recording studio: Broadcast Recording	\N	\N	\N	\N
172	local	00000194	2006-02-28 00:00:00	2006-02-28 00:00:00	0	Stewball	\N	8	25	140	1	\N	Recording studio: Champion	\N	\N	\N	\N
173	local	00000195	2006-02-28 00:00:00	2006-02-28 00:00:00	0	Stewball First Version 1	\N	8	25	140	1	\N	Recording studio: Champion	\N	\N	\N	\N
174	local	00000196	2006-02-28 00:00:00	2006-02-28 00:00:00	0	Stewball First Version 2	\N	8	25	140	1	\N	Recording studio: Champion	\N	\N	\N	\N
175	local	00000197	2006-02-28 00:00:00	2006-02-28 00:00:00	0	Deep River 1	\N	8	25	140	1	\N	CBS, Recording studio: Rockhill	\N	\N	\N	\N
176	local	00000198	2006-02-28 00:00:00	2006-02-28 00:00:00	0	Let the Heaven fight them on me  2	\N	8	25	140	1	\N	CBS, Recording studio: Rockhill	\N	\N	\N	\N
177	local	00000199	2006-02-28 00:00:00	2006-02-28 00:00:00	0	Song of Mary 3	\N	8	25	140	1	\N	CBS, Recording studio: Rockhill	\N	\N	\N	\N
178	local	00000200	2006-02-28 00:00:00	2006-02-28 00:00:00	0	I know the Lord 4	\N	8	25	140	1	\N	CBS, Recording studio: Rockhill	\N	\N	\N	\N
179	local	00000201	2006-02-28 00:00:00	2006-02-28 00:00:00	0	Bright [?] above 5	\N	8	25	140	1	\N	CBS, Recording studio: Rockhill	\N	\N	\N	\N
180	local	00000202	2006-02-28 00:00:00	2006-02-28 00:00:00	0	Sing o Heaven 6	\N	8	25	140	1	\N	CBS, Recording studio: Rockhill	\N	\N	\N	\N
181	local	00000203	2006-02-28 00:00:00	2006-02-28 00:00:00	0	Sing o Heaven 7	\N	8	25	140	1	\N	CBS, Recording studio: Rockhill	\N	\N	\N	\N
182	local	00000204	2006-02-28 00:00:00	2006-02-28 00:00:00	0	I want to be ready 8	\N	8	25	140	1	\N	CBS, Recording studio: Rockhill	\N	\N	\N	\N
183	local	00000205	2006-02-28 00:00:00	2006-02-28 00:00:00	0	Go down Moses 1	\N	8	25	140	1	\N	CBS, Recording studio: Carnegie Hall Recording	\N	\N	\N	\N
184	local	00000206	2006-02-28 00:00:00	2006-02-28 00:00:00	0	O holy lord 2	\N	8	25	140	1	\N	CBS, Recording studio: Carnegie Hall Recording	\N	\N	\N	\N
185	local	00000207	2006-02-28 00:00:00	2006-02-28 00:00:00	0	Holy Lord 3	\N	8	25	140	1	\N	CBS, Recording studio: Carnegie Hall Recording	\N	\N	\N	\N
186	local	00000208	2006-02-28 00:00:00	2006-02-28 00:00:00	0	O Freedom 4	\N	8	25	140	1	\N	CBS, Recording studio: Carnegie Hall Recording	\N	\N	\N	\N
187	local	00000209	2006-02-28 00:00:00	2006-02-28 00:00:00	0	King Jesus is a listening 5	\N	8	25	140	1	\N	CBS, Recording studio: Carnegie Hall Recording	\N	\N	\N	\N
188	local	00000210	2006-02-28 00:00:00	2006-02-28 00:00:00	0	I want to be ready 6	\N	8	25	140	1	\N	CBS, Recording studio: Carnegie Hall Recording	\N	\N	\N	\N
189	local	00000211	2006-02-28 00:00:00	2006-02-28 00:00:00	0	Lord I want to be a Christian 1	\N	8	25	140	1	\N	CBS, Recording studio: Carnegie Hall Recording	\N	\N	\N	\N
190	local	00000212	2006-02-28 00:00:00	2006-02-28 00:00:00	0	King of kings, Jesus joy 2	\N	8	25	140	1	\N	CBS, Recording studio: Carnegie Hall Recording	\N	\N	\N	\N
191	local	00000213	2006-02-28 00:00:00	2006-02-28 00:00:00	0	Keep me from singing 3	\N	8	25	140	1	\N	CBS, Recording studio: Carnegie Hall Recording	\N	\N	\N	\N
192	local	00000214	2006-02-28 00:00:00	2006-02-28 00:00:00	0	He is coming soon 4	\N	8	25	140	1	\N	CBS, Recording studio: Carnegie Hall Recording	\N	\N	\N	\N
193	local	00000215	2006-02-28 00:00:00	2006-02-28 00:00:00	0	Heavenly union 5	\N	8	25	140	1	\N	CBS, Recording studio: Carnegie Hall Recording	\N	\N	\N	\N
194	local	00000216	2006-02-28 00:00:00	2006-02-28 00:00:00	0	Heavenly union, good Lord 6	\N	8	25	140	1	\N	CBS, Recording studio: Carnegie Hall Recording	\N	\N	\N	\N
195	local	00000217	2006-02-28 00:00:00	2006-02-28 00:00:00	0	In dir ist freude 1	\N	8	25	140	1	\N	Recording studio: Recoton	\N	\N	\N	\N
196	local	00000218	2006-02-28 00:00:00	2006-02-28 00:00:00	0	Jesu, joy of man 2	\N	8	25	140	1	\N	Recording studio: Recoton	\N	\N	\N	\N
197	local	00000219	2006-02-28 00:00:00	2006-02-28 00:00:00	0	Deep river, o my good Lord 1	\N	8	25	140	1	\N	CBS, Recording studio: Carnegie Hall Recording	\N	\N	\N	\N
198	local	00000220	2006-02-28 00:00:00	2006-02-28 00:00:00	0	Balm in Gilead 2	\N	8	25	140	1	\N	CBS, Recording studio: Carnegie Hall Recording	\N	\N	\N	\N
199	local	00000221	2006-02-28 00:00:00	2006-02-28 00:00:00	0	Good news, Deep river 3	\N	8	25	140	1	\N	CBS, Recording studio: Carnegie Hall Recording	\N	\N	\N	\N
200	local	00000222	2006-02-28 00:00:00	2006-02-28 00:00:00	0	Every time I feel the spirit 4	\N	8	25	140	1	\N	CBS, Recording studio: Carnegie Hall Recording	\N	\N	\N	\N
201	local	00000223	2006-02-28 00:00:00	2006-02-28 00:00:00	0	Study war, soon a will be done 5	\N	8	25	140	1	\N	CBS, Recording studio: Carnegie Hall Recording	\N	\N	\N	\N
202	local	00000224	2006-02-28 00:00:00	2006-02-28 00:00:00	0	Beautiful city, study war no more 6	\N	8	25	140	1	\N	CBS, Recording studio: Carnegie Hall Recording	\N	\N	\N	\N
203	local	00000225	2006-02-28 00:00:00	2006-02-28 00:00:00	0	Eddie Fisher's Coke Time Christmas Program: 1	\N	8	25	140	1	\N	WNBC-TV; WLD conducting; Recording studio: Rockhill	\N	\N	\N	\N
204	local	00000226	2006-02-28 00:00:00	2006-02-28 00:00:00	0	Eddie Fisher's Coke Time Christmas Program: 2	\N	8	25	140	1	\N	WNBC-TV; WLD conducting; Recording studio: Rockhill	\N	\N	\N	\N
205	local	00000227	2006-02-28 00:00:00	2006-02-28 00:00:00	0	Eddie Fisher's Coke Time Christmas Program: 3	\N	8	25	140	1	\N	WNBC-TV; WLD conducting; Recording studio: Rockhill	\N	\N	\N	\N
206	local	00000228	2006-02-28 00:00:00	2006-02-28 00:00:00	0	Coca Cola PGM: 1	\N	8	25	140	1	\N	CBS, Recording studio: Mary Howard Recordings	\N	\N	\N	\N
207	local	00000229	2006-02-28 00:00:00	2006-02-28 00:00:00	0	Coca Cola PGM: 2	\N	8	25	140	1	\N	CBS, Recording studio: Mary Howard Recordings	\N	\N	\N	\N
208	local	00000230	2006-02-28 00:00:00	2006-02-28 00:00:00	0	Coca Cola PGM: 3	\N	8	25	140	1	\N	CBS, Recording studio: Mary Howard Recordings	\N	\N	\N	\N
209	local	00000231	2006-02-28 00:00:00	2006-02-28 00:00:00	0	Coca Cola PGM: 4	\N	8	25	140	1	\N	CBS, Recording studio: Mary Howard Recordings	\N	\N	\N	\N
210	local	00000232	2006-02-28 00:00:00	2006-02-28 00:00:00	0	UNCF Convocation: Metropolitan Opera House Meeting: 1	\N	8	25	140	1	\N	Recording studio: Bell Sound Studios	\N	\N	\N	\N
211	local	00000234	2006-02-28 00:00:00	2006-02-28 00:00:00	0	UNCF Convocation: Metropolitan Opera House Meeting: 2	\N	8	25	140	1	\N	Recording studio: Bell Sound Studios	\N	\N	\N	\N
212	local	00000235	2006-02-28 00:00:00	2006-02-28 00:00:00	0	UNCF Convocation: Metropolitan Opera House Meeting: 3	\N	8	25	140	1	\N	Recording studio: Bell Sound Studios	\N	\N	\N	\N
213	local	00000236	2006-02-28 00:00:00	2006-02-28 00:00:00	0	UNCF Convocation: Metropolitan Opera House Meeting: 4	\N	8	25	140	1	\N	Recording studio: Bell Sound Studios	\N	\N	\N	\N
214	local	00000237	2006-02-28 00:00:00	2006-02-28 00:00:00	0	UNCF Convocation: Metropolitan Opera House Meeting: 5	\N	8	25	140	1	\N	Recording studio: Bell Sound Studios	\N	\N	\N	\N
215	local	00000238	2006-02-28 00:00:00	2006-02-28 00:00:00	0	UNCF Convocation: Metropolitan Opera House Meeting: 6	\N	8	25	140	1	\N	Recording studio: Bell Sound Studios	\N	\N	\N	\N
216	local	00000239	2006-02-28 00:00:00	2006-02-28 00:00:00	0	UNCF Convocation: Metropolitan Opera House Meeting: 7	\N	8	25	140	1	\N	Recording studio: Bell Sound Studios	\N	\N	\N	\N
217	local	00000240	2006-02-28 00:00:00	2006-02-28 00:00:00	0	UNCF Convocation: Metropolitan Opera House Meeting: 8	\N	8	25	140	1	\N	Recording studio: Bell Sound Studios	\N	\N	\N	\N
218	local	00000241	2006-02-28 00:00:00	2006-02-28 00:00:00	0	Hiawatha's Wedding Feast (Samuel Coleridge-Taylor) 1	\N	8	25	140	1	\N	12" disk; Recording studio: Presto	\N	\N	\N	\N
219	local	00000242	2006-02-28 00:00:00	2006-02-28 00:00:00	0	Hiawatha's Wedding Feast (Samuel Coleridge-Taylor) 2	\N	8	25	140	1	\N	12" disk; Recording studio: Presto	\N	\N	\N	\N
220	local	00000243	2006-02-28 00:00:00	2006-02-28 00:00:00	0	Da List die Rhu! 1	\N	8	25	140	1	\N	Recording studio: Audio Disc	\N	\N	\N	\N
221	local	00000244	2006-02-28 00:00:00	2006-02-28 00:00:00	0	Da List die Rhu! 2	\N	8	25	140	1	\N	Recording studio: Audio Disc	\N	\N	\N	\N
222	local	00000245	2006-02-28 00:00:00	2006-02-28 00:00:00	0	Atlanta Exposition Address (14605)	\N	8	25	140	1	\N	10" disk; Recording studio: Columbia Graphophone Co.	\N	\N	\N	\N
223	local	00000246	2006-02-28 00:00:00	2006-02-28 00:00:00	0	Atlanta Exposition Address (14605)	\N	8	25	140	1	\N	10" disk; Recording studio: Columbia Graphophone Co.	\N	\N	\N	\N
224	local	00000247	2006-02-28 00:00:00	2006-02-28 00:00:00	0	Eddie Fisher's Coke Time Christmas Program 1	\N	8	25	140	1	\N	WNBC-TV; Recording studio: Rockhill	\N	\N	\N	\N
225	local	00000248	2006-02-28 00:00:00	2006-02-28 00:00:00	0	Eddie Fisher's Coke Time Christmas Program 2	\N	8	25	140	1	\N	WNBC-TV; Recording studio: Rockhill	\N	\N	\N	\N
226	local	00000249	2006-02-28 00:00:00	2006-02-28 00:00:00	0	Eddie Fisher's Coke Time Christmas Program 3	\N	8	25	140	1	\N	WNBC-TV; Recording studio: Rockhill	\N	\N	\N	\N
227	local	00000250	2006-02-28 00:00:00	2006-02-28 00:00:00	0	Eddie Fisher's Coke Time Christmas Program 4	\N	8	25	140	1	\N	WNBC-TV; Recording studio: Rockhill	\N	\N	\N	\N
228	local	00000251	2006-02-28 00:00:00	2006-02-28 00:00:00	0	Every time I Feel The Spirit 1	\N	8	25	140	1	\N	WABC; Recording studio: Champion	\N	\N	\N	\N
229	local	00000252	2006-02-28 00:00:00	2006-02-28 00:00:00	0	Every time I Feel The Spirit 2	\N	8	25	140	1	\N	WABC; Recording studio: Champion	\N	\N	\N	\N
230	local	00000253	2006-02-28 00:00:00	2006-02-28 00:00:00	0	Every time I Feel The Spirit/Deep River 1	\N	8	25	140	1	\N	WJZ NBC; Recording studio: Champion	\N	\N	\N	\N
231	local	00000254	2006-02-28 00:00:00	2006-02-28 00:00:00	0	Booker T. Washington Excerpt 2	\N	8	25	140	1	\N	WJZ NBC; Recording studio: Champion	\N	\N	\N	\N
232	local	00000255	2006-02-28 00:00:00	2006-02-28 00:00:00	0	There is a balm in Gilead	\N	8	25	140	1	\N	WABC  CBS; Recording studio: Unknown	\N	\N	\N	\N
233	local	00000256	2006-02-28 00:00:00	2006-02-28 00:00:00	0	John Beach 2	\N	8	25	140	1	\N	\N	\N	\N	\N	\N
234	local	00000257	2006-02-28 00:00:00	2006-02-28 00:00:00	0	John Knox 1	\N	8	25	140	1	\N	\N	\N	\N	\N	\N
235	local	00000258	2006-02-28 00:00:00	2006-02-28 00:00:00	0	John Knox 2	\N	8	25	140	1	\N	\N	\N	\N	\N	\N
236	local	00000259	2006-02-28 00:00:00	2006-02-28 00:00:00	0	John Knox 3	\N	8	25	140	1	\N	\N	\N	\N	\N	\N
237	local	00000260	2006-02-28 00:00:00	2006-02-28 00:00:00	0	Mae Beach 1	\N	8	25	140	1	\N	\N	\N	\N	\N	\N
238	local	00000261	2006-02-28 00:00:00	2006-02-28 00:00:00	0	Mae Beach 2	\N	8	25	140	1	\N	\N	\N	\N	\N	\N
239	local	00000262	2006-02-28 00:00:00	2006-02-28 00:00:00	0	Mae Beach 3	\N	8	25	140	1	\N	\N	\N	\N	\N	\N
240	local	00000263	2006-02-28 00:00:00	2006-02-28 00:00:00	0	William Tut Johnson 1	\N	8	25	140	1	\N	\N	\N	\N	\N	\N
241	local	00000264	2006-02-28 00:00:00	2006-02-28 00:00:00	0	William Tut Johnson 2	\N	8	25	140	1	\N	\N	\N	\N	\N	\N
242	local	00000265	2006-02-28 00:00:00	2006-02-28 00:00:00	0	John Hunter 1	\N	8	25	140	1	\N	\N	\N	\N	\N	\N
243	local	00000266	2006-02-28 00:00:00	2006-02-28 00:00:00	0	Enrique E. Bledel 1	\N	8	25	140	1	\N	\N	\N	\N	\N	\N
244	local	00000267	2006-02-28 00:00:00	2006-02-28 00:00:00	0	Enrique E. Bledel 2	\N	8	25	140	1	\N	\N	\N	\N	\N	\N
245	local	00000268	2006-02-28 00:00:00	2006-02-28 00:00:00	0	Sean Morton Downey Jr. 1	\N	8	25	140	1	\N	\N	\N	\N	\N	\N
246	local	00000269	2006-02-28 00:00:00	2006-02-28 00:00:00	0	Sean Morton Downey Jr. 2	\N	8	25	140	1	\N	\N	\N	\N	\N	\N
247	local	00000270	2006-02-28 00:00:00	2006-02-28 00:00:00	0	Bill Key 1	\N	8	25	140	1	\N	\N	\N	\N	\N	\N
248	local	00000271	2006-02-28 00:00:00	2006-02-28 00:00:00	0	Bill Key 2	\N	8	25	140	1	\N	\N	\N	\N	\N	\N
249	local	00000272	2006-02-28 00:00:00	2006-02-28 00:00:00	0	Bill Key 3	\N	8	25	140	1	\N	\N	\N	\N	\N	\N
250	local	00000273	2006-02-28 00:00:00	2006-02-28 00:00:00	0	Julius Lunsford 1	\N	8	25	140	1	\N	\N	\N	\N	\N	\N
251	local	00000274	2006-02-28 00:00:00	2006-02-28 00:00:00	0	Julius Lunsford 2	\N	8	25	140	1	\N	\N	\N	\N	\N	\N
252	local	00000275	2006-02-28 00:00:00	2006-02-28 00:00:00	0	Franklin Garrett 2	\N	8	25	140	1	\N	\N	\N	\N	\N	\N
253	local	00000276	2006-02-28 00:00:00	2006-02-28 00:00:00	0	James W. Wimberly 2	\N	8	25	140	1	\N	\N	\N	\N	\N	\N
254	local	00000277	2006-02-28 00:00:00	2006-02-28 00:00:00	0	Franklin Garrett 1	\N	8	25	140	1	\N	\N	\N	\N	\N	\N
255	local	00000278	2006-02-28 00:00:00	2006-02-28 00:00:00	0	Max Schmeling	\N	8	25	140	1	\N	\N	\N	\N	\N	\N
256	local	00000279	2006-02-28 00:00:00	2006-02-28 00:00:00	0	E. Neville Isdell 2	\N	8	25	140	1	\N	\N	\N	\N	\N	\N
257	local	00000280	2006-02-28 00:00:00	2006-02-28 00:00:00	0	E. Neville Isdell 3	\N	8	25	140	1	\N	\N	\N	\N	\N	\N
258	local	00000281	2006-02-28 00:00:00	2006-02-28 00:00:00	0	Edward F.C. Fisk 1	\N	8	25	140	1	\N	\N	\N	\N	\N	\N
259	local	00000282	2006-02-28 00:00:00	2006-02-28 00:00:00	0	Edward F.C. Fisk 2	\N	8	25	140	1	\N	\N	\N	\N	\N	\N
260	local	00000283	2006-02-28 00:00:00	2006-02-28 00:00:00	0	George Downing 1	\N	8	25	140	1	\N	\N	\N	\N	\N	\N
261	local	00000284	2006-02-28 00:00:00	2006-02-28 00:00:00	0	George Downing 2	\N	8	25	140	1	\N	\N	\N	\N	\N	\N
262	local	00000285	2006-02-28 00:00:00	2006-02-28 00:00:00	0	George Downing 3	\N	8	25	140	1	\N	\N	\N	\N	\N	\N
263	local	00000286	2006-02-28 00:00:00	2006-02-28 00:00:00	0	George Downing 4	\N	8	25	140	1	\N	\N	\N	\N	\N	\N
264	local	00000287	2006-02-28 00:00:00	2006-02-28 00:00:00	0	Walter Oppenhoff 1	\N	8	25	140	1	\N	\N	\N	\N	\N	\N
265	local	00000288	2006-02-28 00:00:00	2006-02-28 00:00:00	0	Walter Oppenhoff 2	\N	8	25	140	1	\N	\N	\N	\N	\N	\N
266	local	00000289	2006-02-28 00:00:00	2006-02-28 00:00:00	0	Bert Pelletier 1	\N	8	25	140	1	\N	\N	\N	\N	\N	\N
267	local	00000290	2006-02-28 00:00:00	2006-02-28 00:00:00	0	Bert Pelletier 2	\N	8	25	140	1	\N	\N	\N	\N	\N	\N
268	local	00000291	2006-02-28 00:00:00	2006-02-28 00:00:00	0	William O. Solms 1	\N	8	25	140	1	\N	\N	\N	\N	\N	\N
269	local	00000292	2006-02-28 00:00:00	2006-02-28 00:00:00	0	William O. Solms 2	\N	8	25	140	1	\N	\N	\N	\N	\N	\N
270	local	00000293	2006-02-28 00:00:00	2006-02-28 00:00:00	0	Bill and Jan Schmidt 1	\N	8	25	140	1	\N	\N	\N	\N	\N	\N
271	local	00000294	2006-02-28 00:00:00	2006-02-28 00:00:00	0	Bill and Jan Schmidt 2	\N	8	25	140	1	\N	\N	\N	\N	\N	\N
272	local	00000295	2006-02-28 00:00:00	2006-02-28 00:00:00	0	Bill and Jan Schmidt 3	\N	8	25	140	1	\N	\N	\N	\N	\N	\N
273	local	00000296	2006-02-28 00:00:00	2006-02-28 00:00:00	0	Bill and Jan Schmidt 4	\N	8	25	140	1	\N	\N	\N	\N	\N	\N
274	local	00000297	2006-02-28 00:00:00	2006-02-28 00:00:00	0	Hoe Emma Hoe, unknown spiritual, Go round the boarder Suzie,  Four and twenty, O another man down	\N	8	25	140	1	\N	\N	\N	\N	\N	\N
275	local	00000298	2006-02-28 00:00:00	2006-02-28 00:00:00	0	Pay me my money down, To my love, Young man jump ov'r to me, Every night	\N	8	25	140	1	\N	\N	\N	\N	\N	\N
276	local	00000299	2006-02-28 00:00:00	2006-02-28 00:00:00	826	African field recordings: Reel 1	\N	16	247	140	1	\N	Songs by students at Fourah Bay College, Sierra Leona West Africa. Mr. F.R. [Davis] principal	\N	\N	\N	\N
277	local	00000300	2006-02-28 00:00:00	2006-02-28 00:00:00	826	African field recordings: Reel 1	\N	16	247	140	1	\N	Songs by students at Fourah Bay College, Sierra Leona West Africa. Mr. F.R. [Davis] principal	\N	\N	\N	\N
278	local	00000301	2006-02-28 00:00:00	2006-02-28 00:00:00	826	African field recordings: Reel 1	\N	16	247	140	1	\N	Songs by students at Fourah Bay College, Sierra Leona West Africa. Mr. F.R. [Davis] principal	\N	\N	\N	\N
279	local	00000302	2006-02-28 00:00:00	2006-02-28 00:00:00	826	African field recordings: Reel 1	\N	16	247	140	1	\N	Songs by students at Fourah Bay College, Sierra Leona West Africa. Mr. F.R. [Davis] principal	\N	\N	\N	\N
280	local	00000303	2006-02-28 00:00:00	2006-02-28 00:00:00	826	African field recordings: Reel 1	\N	16	247	140	1	\N	Songs by students at Fourah Bay College, Sierra Leona West Africa. Mr. F.R. [Davis] principal	\N	\N	\N	\N
281	local	00000304	2006-02-28 00:00:00	2006-02-28 00:00:00	826	African field recordings: Reel 1	\N	16	247	140	1	\N	Songs by students at Fourah Bay College, Sierra Leona West Africa. Mr. F.R. [Davis] principal	\N	\N	\N	\N
282	local	00000305	2006-02-28 00:00:00	2006-02-28 00:00:00	826	African field recordings: Reel 1	\N	16	247	140	1	\N	Songs by students at Fourah Bay College, Sierra Leona West Africa. Mr. F.R. [Davis] principal	\N	\N	\N	\N
283	local	00000306	2006-02-28 00:00:00	2006-02-28 00:00:00	826	African field recordings: Reel 1	\N	16	247	140	1	\N	Songs by students at Fourah Bay College, Sierra Leona West Africa. Mr. F.R. [Davis] principal	\N	\N	\N	\N
284	local	00000307	2006-02-28 00:00:00	2006-02-28 00:00:00	826	African field recordings: Reel 1	\N	16	247	140	1	\N	Songs by students at Fourah Bay College, Sierra Leona West Africa. Mr. F.R. [Davis] principal	\N	\N	\N	\N
285	local	00000308	2006-02-28 00:00:00	2006-02-28 00:00:00	0	African field recordings: Reel 1	\N	8	25	140	1	\N	Songs by students at Fourah Bay College, Sierra Leona West Africa. Mr. F.R. [Davis] principal	\N	\N	\N	\N
286	local	00000309	2006-02-28 00:00:00	2006-02-28 00:00:00	0	African field recordings: Reel 1	\N	8	25	140	1	\N	Songs by students at Fourah Bay College, Sierra Leona West Africa. Mr. F.R. [Davis] principal	\N	\N	\N	\N
287	local	00000310	2006-02-28 00:00:00	2006-02-28 00:00:00	0	African field recordings: Reel 1	\N	8	25	140	1	\N	Songs by students at Fourah Bay College, Sierra Leona West Africa. Mr. F.R. [Davis] principal	\N	\N	\N	\N
288	local	00000311	2006-02-28 00:00:00	2006-02-28 00:00:00	0	African field recordings: Reel 1	\N	8	25	140	1	\N	Songs by students at Fourah Bay College, Sierra Leona West Africa. Mr. F.R. [Davis] principal	\N	\N	\N	\N
289	local	00000312	2006-02-28 00:00:00	2006-02-28 00:00:00	0	African field recordings: Reel 1	\N	8	25	140	1	\N	Songs by students at Fourah Bay College, Sierra Leona West Africa. Mr. F.R. [Davis] principal	\N	\N	\N	\N
290	local	00000313	2006-02-28 00:00:00	2006-02-28 00:00:00	0	African field recordings: Reel 1	\N	8	25	140	1	\N	Songs by students at Fourah Bay College, Sierra Leona West Africa. Mr. F.R. [Davis] principal	\N	\N	\N	\N
291	local	00000314	2006-02-28 00:00:00	2006-02-28 00:00:00	0	African field recordings: Reel 1	\N	8	25	140	1	\N	Songs by students at Fourah Bay College, Sierra Leona West Africa. Mr. F.R. [Davis] principal	\N	\N	\N	\N
292	local	00000315	2006-02-28 00:00:00	2006-02-28 00:00:00	0	African field recordings: Reel 1	\N	8	25	140	1	\N	Songs by students at Fourah Bay College, Sierra Leona West Africa. Mr. F.R. [Davis] principal	\N	\N	\N	\N
293	local	00000316	2006-02-28 00:00:00	2006-02-28 00:00:00	0	African field recordings: Reel 1	\N	8	25	140	1	\N	Songs by students at Fourah Bay College, Sierra Leona West Africa. Mr. F.R. [Davis] principal	\N	\N	\N	\N
294	local	00000317	2006-02-28 00:00:00	2006-02-28 00:00:00	0	African field recordings: Reel 1	\N	8	25	140	1	\N	Songs by students at Fourah Bay College, Sierra Leona West Africa. Mr. F.R. [Davis] principal	\N	\N	\N	\N
295	local	00000318	2006-02-28 00:00:00	2006-02-28 00:00:00	0	African field recordings: Reel 1	\N	8	25	140	1	\N	Songs by students at Fourah Bay College, Sierra Leona West Africa. Mr. F.R. [Davis] principal	\N	\N	\N	\N
296	local	00000319	2006-02-28 00:00:00	2006-02-28 00:00:00	0	African field recordings: Reel 1	\N	8	25	140	1	\N	Songs by students at Fourah Bay College, Sierra Leona West Africa. Mr. F.R. [Davis] principal	\N	\N	\N	\N
297	local	00000320	2006-02-28 00:00:00	2006-02-28 00:00:00	0	African field recordings: Reel 1	\N	8	25	140	1	\N	Songs by students at Fourah Bay College, Sierra Leona West Africa. Mr. F.R. [Davis] principal	\N	\N	\N	\N
298	local	00000321	2006-02-28 00:00:00	2006-02-28 00:00:00	0	African field recordings: Reel 1	\N	8	25	140	1	\N	Songs by students at Fourah Bay College, Sierra Leona West Africa. Mr. F.R. [Davis] principal	\N	\N	\N	\N
299	local	00000322	2006-02-28 00:00:00	2006-02-28 00:00:00	0	African field recordings: Reel 1	\N	8	25	140	1	\N	Songs by students at Fourah Bay College, Sierra Leona West Africa. Mr. F.R. [Davis] principal	\N	\N	\N	\N
300	local	00000323	2006-02-28 00:00:00	2006-02-28 00:00:00	0	African field recordings: Reel 1	\N	8	25	140	1	\N	Songs by students at Fourah Bay College, Sierra Leona West Africa. Mr. F.R. [Davis] principal	\N	\N	\N	\N
301	local	00000324	2006-02-28 00:00:00	2006-02-28 00:00:00	0	African field recordings: Reel 1	\N	8	25	140	1	\N	Songs by students at Fourah Bay College, Sierra Leona West Africa. Mr. F.R. [Davis] principal	\N	\N	\N	\N
302	local	00000325	2006-02-28 00:00:00	2006-02-28 00:00:00	0	African field recordings: Reel 1	\N	8	25	140	1	\N	Songs by students at Fourah Bay College, Sierra Leona West Africa. Mr. F.R. [Davis] principal	\N	\N	\N	\N
303	local	00000326	2006-02-28 00:00:00	2006-02-28 00:00:00	0	African field recordings: Reel 2	\N	8	25	140	1	\N	Freetown and Port Loco, Sierra Leone; M. Dain, Tommy Korome playing on his jekete and Ballanji and Bolonji players.	\N	\N	\N	\N
304	local	00000327	2006-02-28 00:00:00	2006-02-28 00:00:00	0	African field recordings: Reel 2	\N	8	25	140	1	\N	Freetown and Port Loco, Sierra Leone; M. Dain, Tommy Korome playing on his jekete and Ballanji and Bolonji players.	\N	\N	\N	\N
305	local	00000328	2006-02-28 00:00:00	2006-02-28 00:00:00	0	African field recordings: Reel 2	\N	8	25	140	1	\N	Freetown and Port Loco, Sierra Leone; M. Dain, Tommy Korome playing on his jekete and Ballanji and Bolonji players.	\N	\N	\N	\N
306	local	00000329	2006-02-28 00:00:00	2006-02-28 00:00:00	0	African field recordings: Reel 2	\N	8	25	140	1	\N	Freetown and Port Loco, Sierra Leone; M. Dain, Tommy Korome playing on his jekete and Ballanji and Bolonji players.	\N	\N	\N	\N
307	local	00000330	2006-02-28 00:00:00	2006-02-28 00:00:00	0	African field recordings: Reel 2	\N	8	25	140	1	\N	Freetown and Port Loco, Sierra Leone; M. Dain, Tommy Korome playing on his jekete and Ballanji and Bolonji players.	\N	\N	\N	\N
308	local	00000331	2006-02-28 00:00:00	2006-02-28 00:00:00	0	African field recordings: Reel 3	\N	8	25	140	1	\N	Solo passages on the ballaryo; Ala Kali Company and drums; [Lunsar] Branch (chief Ala Kali Modu); boys London; part loco branch; Mr. Caulker statement and singing; Mende funeral song; native music and drums; Fourah Bay College; Suehn Mission	\N	\N	\N	\N
309	local	00000332	2006-02-28 00:00:00	2006-02-28 00:00:00	0	African field recordings: Reel 3	\N	8	25	140	1	\N	Solo passages on the ballaryo; Ala Kali Company and drums; [Lunsar] Branch (chief Ala Kali Modu); boys London; part loco branch; Mr. Caulker statement and singing; Mende funeral song; native music and drums; Fourah Bay College; Suehn Mission	\N	\N	\N	\N
310	local	00000333	2006-02-28 00:00:00	2006-02-28 00:00:00	0	African field recordings: Reel 3	\N	8	25	140	1	\N	Solo passages on the ballaryo; Ala Kali Company and drums; [Lunsar] Branch (chief Ala Kali Modu); boys London; part loco branch; Mr. Caulker statement and singing; Mende funeral song; native music and drums; Fourah Bay College; Suehn Mission	\N	\N	\N	\N
311	local	00000334	2006-02-28 00:00:00	2006-02-28 00:00:00	0	African field recordings: Reel 3	\N	8	25	140	1	\N	Solo passages on the ballaryo; Ala Kali Company and drums; [Lunsar] Branch (chief Ala Kali Modu); boys London; part loco branch; Mr. Caulker statement and singing; Mende funeral song; native music and drums; Fourah Bay College; Suehn Mission	\N	\N	\N	\N
312	local	00000335	2006-02-28 00:00:00	2006-02-28 00:00:00	0	African field recordings: Reel 3	\N	8	25	140	1	\N	Solo passages on the ballaryo; Ala Kali Company and drums; [Lunsar] Branch (chief Ala Kali Modu); boys London; part loco branch; Mr. Caulker statement and singing; Mende funeral song; native music and drums; Fourah Bay College; Suehn Mission	\N	\N	\N	\N
313	local	00000336	2006-02-28 00:00:00	2006-02-28 00:00:00	0	African field recordings: Reel 3	\N	8	25	140	1	\N	Solo passages on the ballaryo; Ala Kali Company and drums; [Lunsar] Branch (chief Ala Kali Modu); boys London; part loco branch; Mr. Caulker statement and singing; Mende funeral song; native music and drums; Fourah Bay College; Suehn Mission	\N	\N	\N	\N
314	local	00000337	2006-02-28 00:00:00	2006-02-28 00:00:00	0	African field recordings: Reel 3	\N	8	25	140	1	\N	Solo passages on the ballaryo; Ala Kali Company and drums; [Lunsar] Branch (chief Ala Kali Modu); boys London; part loco branch; Mr. Caulker statement and singing; Mende funeral song; native music and drums; Fourah Bay College; Suehn Mission	\N	\N	\N	\N
315	local	00000338	2006-02-28 00:00:00	2006-02-28 00:00:00	0	African field recordings: Reel 3	\N	8	25	140	1	\N	Solo passages on the ballaryo; Ala Kali Company and drums; [Lunsar] Branch (chief Ala Kali Modu); boys London; part loco branch; Mr. Caulker statement and singing; Mende funeral song; native music and drums; Fourah Bay College; Suehn Mission	\N	\N	\N	\N
316	local	00000339	2006-02-28 00:00:00	2006-02-28 00:00:00	0	African field recordings: Reel 3	\N	8	25	140	1	\N	Solo passages on the ballaryo; Ala Kali Company and drums; [Lunsar] Branch (chief Ala Kali Modu); boys London; part loco branch; Mr. Caulker statement and singing; Mende funeral song; native music and drums; Fourah Bay College; Suehn Mission	\N	\N	\N	\N
317	local	00000340	2006-02-28 00:00:00	2006-02-28 00:00:00	0	African field recordings: Reel 3	\N	8	25	140	1	\N	Solo passages on the ballaryo; Ala Kali Company and drums; [Lunsar] Branch (chief Ala Kali Modu); boys London; part loco branch; Mr. Caulker statement and singing; Mende funeral song; native music and drums; Fourah Bay College; Suehn Mission	\N	\N	\N	\N
318	local	00000341	2006-02-28 00:00:00	2006-02-28 00:00:00	0	African field recordings: Reel 3	\N	8	25	140	1	\N	Solo passages on the ballaryo; Ala Kali Company and drums; [Lunsar] Branch (chief Ala Kali Modu); boys London; part loco branch; Mr. Caulker statement and singing; Mende funeral song; native music and drums; Fourah Bay College; Suehn Mission	\N	\N	\N	\N
319	local	00000342	2006-02-28 00:00:00	2006-02-28 00:00:00	0	African field recordings: Reel 4	\N	8	25	140	1	\N	Suehn Industrial Academy; Ms. M.M. Davis, principal and Miss Winifred Bo[wzous]gha	\N	\N	\N	\N
320	local	00000343	2006-02-28 00:00:00	2006-02-28 00:00:00	0	African field recordings: Reel 4	\N	8	25	140	1	\N	Suehn Industrial Academy; Ms. M.M. Davis, principal and Miss Winifred Bo[wzous]gha	\N	\N	\N	\N
321	local	00000344	2006-02-28 00:00:00	2006-02-28 00:00:00	0	African field recordings: Reel 4	\N	8	25	140	1	\N	Suehn Industrial Academy; Ms. M.M. Davis, principal and Miss Winifred Bo[wzous]gha	\N	\N	\N	\N
322	local	00000345	2006-02-28 00:00:00	2006-02-28 00:00:00	0	African field recordings: Reel 4	\N	8	25	140	1	\N	Suehn Industrial Academy; Ms. M.M. Davis, principal and Miss Winifred Bo[wzous]gha	\N	\N	\N	\N
323	local	00000346	2006-02-28 00:00:00	2006-02-28 00:00:00	0	African field recordings: Reel 4	\N	8	25	140	1	\N	Suehn Industrial Academy; Ms. M.M. Davis, principal and Miss Winifred Bo[wzous]gha	\N	\N	\N	\N
324	local	00000347	2006-02-28 00:00:00	2006-02-28 00:00:00	0	African field recordings: Reel 4	\N	8	25	140	1	\N	Suehn Industrial Academy; Ms. M.M. Davis, principal and Miss Winifred Bo[wzous]gha	\N	\N	\N	\N
325	local	00000348	2006-02-28 00:00:00	2006-02-28 00:00:00	0	African field recordings: Reel 4	\N	8	25	140	1	\N	Suehn Industrial Academy; Ms. M.M. Davis, principal and Miss Winifred Bo[wzous]gha	\N	\N	\N	\N
326	local	00000349	2006-02-28 00:00:00	2006-02-28 00:00:00	0	African field recordings: Reel 4	\N	8	25	140	1	\N	Suehn Industrial Academy; Ms. M.M. Davis, principal and Miss Winifred Bo[wzous]gha	\N	\N	\N	\N
327	local	00000350	2006-02-28 00:00:00	2006-02-28 00:00:00	0	African field recordings: Reel 4	\N	8	25	140	1	\N	Suehn Industrial Academy; Ms. M.M. Davis, principal and Miss Winifred Bo[wzous]gha	\N	\N	\N	\N
328	local	00000351	2006-02-28 00:00:00	2006-02-28 00:00:00	0	African field recordings: Reel 4	\N	8	25	140	1	\N	Suehn Industrial Academy; Ms. M.M. Davis, principal and Miss Winifred Bo[wzous]gha	\N	\N	\N	\N
329	local	00000352	2006-02-28 00:00:00	2006-02-28 00:00:00	0	African field recordings: Reel 4	\N	8	25	140	1	\N	Suehn Industrial Academy; Ms. M.M. Davis, principal and Miss Winifred Bo[wzous]gha	\N	\N	\N	\N
330	local	00000353	2006-02-28 00:00:00	2006-02-28 00:00:00	0	African field recordings: Reel 4	\N	8	25	140	1	\N	Suehn Industrial Academy; Ms. M.M. Davis, principal and Miss Winifred Bo[wzous]gha	\N	\N	\N	\N
331	local	00000354	2006-02-28 00:00:00	2006-02-28 00:00:00	0	African field recordings: Reel 5	\N	8	25	140	1	\N	Suehn town people; Mrs. Venah Johnson, wife of the clan chief also a wonderful dancer	\N	\N	\N	\N
332	local	00000355	2006-02-28 00:00:00	2006-02-28 00:00:00	0	African field recordings: Reel 5	\N	8	25	140	1	\N	Suehn town people; Mrs. Venah Johnson, wife of the clan chief also a wonderful dancer	\N	\N	\N	\N
333	local	00000356	2006-02-28 00:00:00	2006-02-28 00:00:00	0	African field recordings: Reel 5	\N	8	25	140	1	\N	Suehn town people; Mrs. Venah Johnson, wife of the clan chief also a wonderful dancer	\N	\N	\N	\N
334	local	00000357	2006-02-28 00:00:00	2006-02-28 00:00:00	0	African field recordings: Reel 5	\N	8	25	140	1	\N	Suehn town people; Mrs. Venah Johnson, wife of the clan chief also a wonderful dancer	\N	\N	\N	\N
335	local	00000358	2006-02-28 00:00:00	2006-02-28 00:00:00	0	African field recordings: Reel 5	\N	8	25	140	1	\N	Suehn town people; Mrs. Venah Johnson, wife of the clan chief also a wonderful dancer	\N	\N	\N	\N
336	local	00000359	2006-02-28 00:00:00	2006-02-28 00:00:00	0	African field recordings: Reel 6	\N	8	25	140	1	\N	Singers and rattles (women); male singer with accordion; Kpelle drummers and dancers at Gbarnga; two Loma-Fanga drums; drummers and singers women Gala tribe, Sanequelle Liberia; Mano harp etc; Reed drums and singer	\N	\N	\N	\N
337	local	00000360	2006-02-28 00:00:00	2006-02-28 00:00:00	0	African field recordings: Reel 6	\N	8	25	140	1	\N	Singers and rattles (women); male singer with accordion; Kpelle drummers and dancers at Gbarnga; two Loma-Fanga drums; drummers and singers women Gala tribe, Sanequelle Liberia; Mano harp etc; Reed drums and singer	\N	\N	\N	\N
338	local	00000361	2006-02-28 00:00:00	2006-02-28 00:00:00	0	African field recordings: Reel 6	\N	8	25	140	1	\N	Singers and rattles (women); male singer with accordion; Kpelle drummers and dancers at Gbarnga; two Loma-Fanga drums; drummers and singers women Gala tribe, Sanequelle Liberia; Mano harp etc; Reed drums and singer	\N	\N	\N	\N
339	local	00000362	2006-02-28 00:00:00	2006-02-28 00:00:00	0	African field recordings: Reel 6	\N	8	25	140	1	\N	Singers and rattles (women); male singer with accordion; Kpelle drummers and dancers at Gbarnga; two Loma-Fanga drums; drummers and singers women Gala tribe, Sanequelle Liberia; Mano harp etc; Reed drums and singer	\N	\N	\N	\N
340	local	00000363	2006-02-28 00:00:00	2006-02-28 00:00:00	0	African field recordings: Reel 6	\N	8	25	140	1	\N	Singers and rattles (women); male singer with accordion; Kpelle drummers and dancers at Gbarnga; two Loma-Fanga drums; drummers and singers women Gala tribe, Sanequelle Liberia; Mano harp etc; Reed drums and singer	\N	\N	\N	\N
341	local	00000364	2006-02-28 00:00:00	2006-02-28 00:00:00	0	African field recordings: Reel 6	\N	8	25	140	1	\N	Singers and rattles (women); male singer with accordion; Kpelle drummers and dancers at Gbarnga; two Loma-Fanga drums; drummers and singers women Gala tribe, Sanequelle Liberia; Mano harp etc; Reed drums and singer	\N	\N	\N	\N
342	local	00000365	2006-02-28 00:00:00	2006-02-28 00:00:00	0	African field recordings: Reel 6	\N	8	25	140	1	\N	Singers and rattles (women); male singer with accordion; Kpelle drummers and dancers at Gbarnga; two Loma-Fanga drums; drummers and singers women Gala tribe, Sanequelle Liberia; Mano harp etc; Reed drums and singer	\N	\N	\N	\N
343	local	00000366	2006-02-28 00:00:00	2006-02-28 00:00:00	0	African field recordings: Reel 7	\N	8	25	140	1	\N	Gbanga Liberia; Via; Mende; Gala; Statement by the D.C. and Chief Sourequelle Liberia	\N	\N	\N	\N
344	local	00000367	2006-02-28 00:00:00	2006-02-28 00:00:00	0	African field recordings: Reel 7	\N	8	25	140	1	\N	Gbanga Liberia; Via; Mende; Gala; Statement by the D.C. and Chief Sourequelle Liberia	\N	\N	\N	\N
345	local	00000368	2006-02-28 00:00:00	2006-02-28 00:00:00	0	African field recordings: Reel 7	\N	8	25	140	1	\N	Gbanga Liberia; Via; Mende; Gala; Statement by the D.C. and Chief Sourequelle Liberia	\N	\N	\N	\N
346	local	00000369	2006-02-28 00:00:00	2006-02-28 00:00:00	0	African field recordings: Reel 7	\N	8	25	140	1	\N	Gbanga Liberia; Via; Mende; Gala; Statement by the D.C. and Chief Sourequelle Liberia	\N	\N	\N	\N
347	local	00000370	2006-02-28 00:00:00	2006-02-28 00:00:00	0	African field recordings: Reel 7	\N	8	25	140	1	\N	Gbanga Liberia; Via; Mende; Gala; Statement by the D.C. and Chief Sourequelle Liberia	\N	\N	\N	\N
348	local	00000371	2006-02-28 00:00:00	2006-02-28 00:00:00	0	African field recordings: Reel 7	\N	8	25	140	1	\N	Gbanga Liberia; Via; Mende; Gala; Statement by the D.C. and Chief Sourequelle Liberia	\N	\N	\N	\N
349	local	00000372	2006-02-28 00:00:00	2006-02-28 00:00:00	0	African field recordings: Reel 7	\N	8	25	140	1	\N	Gbanga Liberia; Via; Mende; Gala; Statement by the D.C. and Chief Sourequelle Liberia	\N	\N	\N	\N
350	local	00000373	2006-02-28 00:00:00	2006-02-28 00:00:00	0	African field recordings: Reel 7	\N	8	25	140	1	\N	Gbanga Liberia; Via; Mende; Gala; Statement by the D.C. and Chief Sourequelle Liberia	\N	\N	\N	\N
351	local	00000374	2006-02-28 00:00:00	2006-02-28 00:00:00	0	African field recordings: Reel 8	\N	8	25	140	1	\N	Basa tribe Gbangitown; Kakata Liberia: Buzzi tribe; women and the Bande tribe; Fanga drums - two small one: they sang as they beat the drums; four songs by the women and three songs by the men	\N	\N	\N	\N
352	local	00000375	2006-02-28 00:00:00	2006-02-28 00:00:00	0	African field recordings: Reel 8	\N	8	25	140	1	\N	Basa tribe Gbangitown; Kakata Liberia: Buzzi tribe; women and the Bande tribe; Fanga drums - two small one: they sang as they beat the drums; four songs by the women and three songs by the men	\N	\N	\N	\N
353	local	00000376	2006-02-28 00:00:00	2006-02-28 00:00:00	0	African field recordings: Reel 8	\N	8	25	140	1	\N	Basa tribe Gbangitown; Kakata Liberia: Buzzi tribe; women and the Bande tribe; Fanga drums - two small one: they sang as they beat the drums; four songs by the women and three songs by the men	\N	\N	\N	\N
354	local	00000377	2006-02-28 00:00:00	2006-02-28 00:00:00	0	African field recordings: Reel 8	\N	8	25	140	1	\N	Basa tribe Gbangitown; Kakata Liberia: Buzzi tribe; women and the Bande tribe; Fanga drums - two small one: they sang as they beat the drums; four songs by the women and three songs by the men	\N	\N	\N	\N
355	local	00000378	2006-02-28 00:00:00	2006-02-28 00:00:00	0	African field recordings: Reel 8	\N	8	25	140	1	\N	Basa tribe Gbangitown; Kakata Liberia: Buzzi tribe; women and the Bande tribe; Fanga drums - two small one: they sang as they beat the drums; four songs by the women and three songs by the men	\N	\N	\N	\N
356	local	00000379	2006-02-28 00:00:00	2006-02-28 00:00:00	0	African field recordings: Reel 8	\N	8	25	140	1	\N	Basa tribe Gbangitown; Kakata Liberia: Buzzi tribe; women and the Bande tribe; Fanga drums - two small one: they sang as they beat the drums; four songs by the women and three songs by the men	\N	\N	\N	\N
357	local	00000380	2006-02-28 00:00:00	2006-02-28 00:00:00	0	African field recordings: Reel 8	\N	8	25	140	1	\N	Basa tribe Gbangitown; Kakata Liberia: Buzzi tribe; women and the Bande tribe; Fanga drums - two small one: they sang as they beat the drums; four songs by the women and three songs by the men	\N	\N	\N	\N
358	local	00000381	2006-02-28 00:00:00	2006-02-28 00:00:00	0	African field recordings: Reel 8	\N	8	25	140	1	\N	Basa tribe Gbangitown; Kakata Liberia: Buzzi tribe; women and the Bande tribe; Fanga drums - two small one: they sang as they beat the drums; four songs by the women and three songs by the men	\N	\N	\N	\N
359	local	00000382	2006-02-28 00:00:00	2006-02-28 00:00:00	0	African field recordings: Reel 8	\N	8	25	140	1	\N	Basa tribe Gbangitown; Kakata Liberia: Buzzi tribe; women and the Bande tribe; Fanga drums - two small one: they sang as they beat the drums; four songs by the women and three songs by the men	\N	\N	\N	\N
360	local	00000383	2006-02-28 00:00:00	2006-02-28 00:00:00	0	African field recordings: Reel 9	\N	8	25	140	1	\N	Liberia etc; Accra, Achemista; Major Thomas; Twi dance music; Erui Christmas song for the children; Twi song about a baby girl from Ashanta tribe	\N	\N	\N	\N
361	local	00000384	2006-02-28 00:00:00	2006-02-28 00:00:00	0	African field recordings: Reel 9	\N	8	25	140	1	\N	Liberia etc; Accra, Achemista; Major Thomas; Twi dance music; Erui Christmas song for the children; Twi song about a baby girl from Ashanta tribe	\N	\N	\N	\N
362	local	00000385	2006-02-28 00:00:00	2006-02-28 00:00:00	0	African field recordings: Reel 9	\N	8	25	140	1	\N	Liberia etc; Accra, Achemista; Major Thomas; Twi dance music; Erui Christmas song for the children; Twi song about a baby girl from Ashanta tribe	\N	\N	\N	\N
363	local	00000386	2006-02-28 00:00:00	2006-02-28 00:00:00	0	African field recordings: Reel 9	\N	8	25	140	1	\N	Liberia etc; Accra, Achemista; Major Thomas; Twi dance music; Erui Christmas song for the children; Twi song about a baby girl from Ashanta tribe	\N	\N	\N	\N
364	local	00000387	2006-02-28 00:00:00	2006-02-28 00:00:00	0	African field recordings: Reel 9	\N	8	25	140	1	\N	Liberia etc; Accra, Achemista; Major Thomas; Twi dance music; Erui Christmas song for the children; Twi song about a baby girl from Ashanta tribe	\N	\N	\N	\N
365	local	00000388	2006-02-28 00:00:00	2006-02-28 00:00:00	0	African field recordings: Reel 9	\N	8	25	140	1	\N	Liberia etc; Accra, Achemista; Major Thomas; Twi dance music; Erui Christmas song for the children; Twi song about a baby girl from Ashanta tribe	\N	\N	\N	\N
366	local	00000389	2006-02-28 00:00:00	2006-02-28 00:00:00	0	African field recordings: Reel 9	\N	8	25	140	1	\N	Liberia etc; Accra, Achemista; Major Thomas; Twi dance music; Erui Christmas song for the children; Twi song about a baby girl from Ashanta tribe	\N	\N	\N	\N
367	local	00000390	2006-02-28 00:00:00	2006-02-28 00:00:00	0	African field recordings: Reel 10	\N	8	25	140	1	\N	Accra: Erue drummers and dancers; Erue Agbadza chorus; Erue Yeiue Yetish dance; male chorus Damas Choir; Ishmael Adams; While the moon is shining, we play play and play etc.	\N	\N	\N	\N
368	local	00000391	2006-02-28 00:00:00	2006-02-28 00:00:00	0	African field recordings: Reel 10	\N	8	25	140	1	\N	Accra: Erue drummers and dancers; Erue Agbadza chorus; Erue Yeiue Yetish dance; male chorus Damas Choir; Ishmael Adams; While the moon is shining, we play play and play etc.	\N	\N	\N	\N
369	local	00000392	2006-02-28 00:00:00	2006-02-28 00:00:00	0	African field recordings: Reel 10	\N	8	25	140	1	\N	Accra: Erue drummers and dancers; Erue Agbadza chorus; Erue Yeiue Yetish dance; male chorus Damas Choir; Ishmael Adams; While the moon is shining, we play play and play etc.	\N	\N	\N	\N
370	local	00000393	2006-02-28 00:00:00	2006-02-28 00:00:00	0	African field recordings: Reel 10	\N	8	25	140	1	\N	Accra: Erue drummers and dancers; Erue Agbadza chorus; Erue Yeiue Yetish dance; male chorus Damas Choir; Ishmael Adams; While the moon is shining, we play play and play etc.	\N	\N	\N	\N
371	local	00000394	2006-02-28 00:00:00	2006-02-28 00:00:00	0	African field recordings: Reel 10	\N	8	25	140	1	\N	Accra: Erue drummers and dancers; Erue Agbadza chorus; Erue Yeiue Yetish dance; male chorus Damas Choir; Ishmael Adams; While the moon is shining, we play play and play etc.	\N	\N	\N	\N
372	local	00000395	2006-02-28 00:00:00	2006-02-28 00:00:00	0	African field recordings: Reel 11	\N	8	25	140	1	\N	Male voices and drum Kumasi; Shanti singers and drummers Kumasi; Amu's choir in three sections	\N	\N	\N	\N
373	local	00000396	2006-02-28 00:00:00	2006-02-28 00:00:00	0	African field recordings: Reel 11	\N	8	25	140	1	\N	Male voices and drum Kumasi; Shanti singers and drummers Kumasi; Amu's choir in three sections	\N	\N	\N	\N
374	local	00000397	2006-02-28 00:00:00	2006-02-28 00:00:00	0	African field recordings: Reel 11	\N	8	25	140	1	\N	Male voices and drum Kumasi; Shanti singers and drummers Kumasi; Amu's choir in three sections	\N	\N	\N	\N
375	local	00000398	2006-02-28 00:00:00	2006-02-28 00:00:00	0	African field recordings: Reel 11	\N	8	25	140	1	\N	Male voices and drum Kumasi; Shanti singers and drummers Kumasi; Amu's choir in three sections	\N	\N	\N	\N
376	local	00000399	2006-02-28 00:00:00	2006-02-28 00:00:00	0	African field recordings: Reel 11	\N	8	25	140	1	\N	Male voices and drum Kumasi; Shanti singers and drummers Kumasi; Amu's choir in three sections	\N	\N	\N	\N
377	local	00000400	2006-02-28 00:00:00	2006-02-28 00:00:00	0	African field recordings: Reel 11	\N	8	25	140	1	\N	Male voices and drum Kumasi; Shanti singers and drummers Kumasi; Amu's choir in three sections	\N	\N	\N	\N
378	local	00000401	2006-02-28 00:00:00	2006-02-28 00:00:00	0	African field recordings: Reel 11	\N	8	25	140	1	\N	Male voices and drum Kumasi; Shanti singers and drummers Kumasi; Amu's choir in three sections	\N	\N	\N	\N
379	local	00000402	2006-02-28 00:00:00	2006-02-28 00:00:00	0	African field recordings: Reel 11	\N	8	25	140	1	\N	Male voices and drum Kumasi; Shanti singers and drummers Kumasi; Amu's choir in three sections	\N	\N	\N	\N
380	local	00000403	2006-02-28 00:00:00	2006-02-28 00:00:00	0	African field recordings: Reel 11	\N	8	25	140	1	\N	Male voices and drum Kumasi; Shanti singers and drummers Kumasi; Amu's choir in three sections	\N	\N	\N	\N
381	local	00000404	2006-02-28 00:00:00	2006-02-28 00:00:00	0	African field recordings: Reel 11	\N	8	25	140	1	\N	Male voices and drum Kumasi; Shanti singers and drummers Kumasi; Amu's choir in three sections	\N	\N	\N	\N
382	local	00000405	2006-02-28 00:00:00	2006-02-28 00:00:00	0	African field recordings: Reel 11	\N	8	25	140	1	\N	Male voices and drum Kumasi; Shanti singers and drummers Kumasi; Amu's choir in three sections	\N	\N	\N	\N
383	local	00000406	2006-02-28 00:00:00	2006-02-28 00:00:00	0	African field recordings: Reel 12	\N	8	25	140	1	\N	Ale Gheghe; Prampran Planges people talking; songs by Mrs. C.R. Granes, Mr. Granes and Mrs. Addison Cape Coast; Songs by Mrs. Addison; speeches to Amayki from his salt pond aunts also Mr. Amma-Sekyi; songs by three women at saltpond: It's a wonderful	\N	\N	\N	\N
384	local	00000407	2006-02-28 00:00:00	2006-02-28 00:00:00	0	African field recordings: Reel 12	\N	8	25	140	1	\N	Ale Gheghe; Prampran Planges people talking; songs by Mrs. C.R. Granes, Mr. Granes and Mrs. Addison Cape Coast; Songs by Mrs. Addison; speeches to Amayki from his salt pond aunts also Mr. Amma-Sekyi; songs by three women at saltpond: It's a wonderful	\N	\N	\N	\N
385	local	00000408	2006-02-28 00:00:00	2006-02-28 00:00:00	0	African field recordings: Reel 12	\N	8	25	140	1	\N	Ale Gheghe; Prampran Planges people talking; songs by Mrs. C.R. Granes, Mr. Granes and Mrs. Addison Cape Coast; Songs by Mrs. Addison; speeches to Amayki from his salt pond aunts also Mr. Amma-Sekyi; songs by three women at saltpond: It's a wonderful	\N	\N	\N	\N
386	local	00000409	2006-02-28 00:00:00	2006-02-28 00:00:00	0	African field recordings: Reel 12	\N	8	25	140	1	\N	Ale Gheghe; Prampran Planges people talking; songs by Mrs. C.R. Granes, Mr. Granes and Mrs. Addison Cape Coast; Songs by Mrs. Addison; speeches to Amayki from his salt pond aunts also Mr. Amma-Sekyi; songs by three women at saltpond: It's a wonderful	\N	\N	\N	\N
387	local	00000410	2006-02-28 00:00:00	2006-02-28 00:00:00	0	African field recordings: Reel 12	\N	8	25	140	1	\N	Ale Gheghe; Prampran Planges people talking; songs by Mrs. C.R. Granes, Mr. Granes and Mrs. Addison Cape Coast; Songs by Mrs. Addison; speeches to Amayki from his salt pond aunts also Mr. Amma-Sekyi; songs by three women at saltpond: It's a wonderful	\N	\N	\N	\N
388	local	00000411	2006-02-28 00:00:00	2006-02-28 00:00:00	0	African field recordings: Reel 12	\N	8	25	140	1	\N	Ale Gheghe; Prampran Planges people talking; songs by Mrs. C.R. Granes, Mr. Granes and Mrs. Addison Cape Coast; Songs by Mrs. Addison; speeches to Amayki from his salt pond aunts also Mr. Amma-Sekyi; songs by three women at saltpond: It's a wonderful	\N	\N	\N	\N
389	local	00000412	2006-02-28 00:00:00	2006-02-28 00:00:00	0	African field recordings: Reel 12	\N	8	25	140	1	\N	Ale Gheghe; Prampran Planges people talking; songs by Mrs. C.R. Granes, Mr. Granes and Mrs. Addison Cape Coast; Songs by Mrs. Addison; speeches to Amayki from his salt pond aunts also Mr. Amma-Sekyi; songs by three women at saltpond: It's a wonderful	\N	\N	\N	\N
390	local	00000413	2006-02-28 00:00:00	2006-02-28 00:00:00	0	African field recordings: Reel 12	\N	8	25	140	1	\N	Ale Gheghe; Prampran Planges people talking; songs by Mrs. C.R. Granes, Mr. Granes and Mrs. Addison Cape Coast; Songs by Mrs. Addison; speeches to Amayki from his salt pond aunts also Mr. Amma-Sekyi; songs by three women at saltpond: It's a wonderful	\N	\N	\N	\N
391	local	00000414	2006-02-28 00:00:00	2006-02-28 00:00:00	0	African field recordings: Reel 12	\N	8	25	140	1	\N	Ale Gheghe; Prampran Planges people talking; songs by Mrs. C.R. Granes, Mr. Granes and Mrs. Addison Cape Coast; Songs by Mrs. Addison; speeches to Amayki from his salt pond aunts also Mr. Amma-Sekyi; songs by three women at saltpond: It's a wonderful	\N	\N	\N	\N
392	local	00000415	2006-02-28 00:00:00	2006-02-28 00:00:00	0	African field recordings: Reel 12	\N	8	25	140	1	\N	Ale Gheghe; Prampran Planges people talking; songs by Mrs. C.R. Granes, Mr. Granes and Mrs. Addison Cape Coast; Songs by Mrs. Addison; speeches to Amayki from his salt pond aunts also Mr. Amma-Sekyi; songs by three women at saltpond: It's a wonderful	\N	\N	\N	\N
393	local	00000416	2006-02-28 00:00:00	2006-02-28 00:00:00	0	African field recordings: Reel 13	\N	8	25	140	1	\N	Saltpond - three women singers; We all have the same grandpa; Amayki's brother etc; singing and drumming etc at Cotonou Dahemey etc; papo tribe funeral song (solo) about the present chief's father, historical song for the people and the country	\N	\N	\N	\N
394	local	00000417	2006-02-28 00:00:00	2006-02-28 00:00:00	0	African field recordings: Reel 13	\N	8	25	140	1	\N	Saltpond - three women singers; We all have the same grandpa; Amayki's brother etc; singing and drumming etc at Cotonou Dahemey etc; papo tribe funeral song (solo) about the present chief's father, historical song for the people and the country	\N	\N	\N	\N
395	local	00000418	2006-02-28 00:00:00	2006-02-28 00:00:00	0	African field recordings: Reel 13	\N	8	25	140	1	\N	Saltpond - three women singers; We all have the same grandpa; Amayki's brother etc; singing and drumming etc at Cotonou Dahemey etc; papo tribe funeral song (solo) about the present chief's father, historical song for the people and the country	\N	\N	\N	\N
396	local	00000419	2006-02-28 00:00:00	2006-02-28 00:00:00	0	African field recordings: Reel 13	\N	8	25	140	1	\N	Saltpond - three women singers; We all have the same grandpa; Amayki's brother etc; singing and drumming etc at Cotonou Dahemey etc; papo tribe funeral song (solo) about the present chief's father, historical song for the people and the country	\N	\N	\N	\N
397	local	00000420	2006-02-28 00:00:00	2006-02-28 00:00:00	0	African field recordings: Reel 13	\N	8	25	140	1	\N	Saltpond - three women singers; We all have the same grandpa; Amayki's brother etc; singing and drumming etc at Cotonou Dahemey etc; papo tribe funeral song (solo) about the present chief's father, historical song for the people and the country	\N	\N	\N	\N
398	local	00000421	2006-02-28 00:00:00	2006-02-28 00:00:00	0	African field recordings: Reel 13	\N	8	25	140	1	\N	Saltpond - three women singers; We all have the same grandpa; Amayki's brother etc; singing and drumming etc at Cotonou Dahemey etc; papo tribe funeral song (solo) about the present chief's father, historical song for the people and the country	\N	\N	\N	\N
399	local	00000422	2006-02-28 00:00:00	2006-02-28 00:00:00	0	African field recordings: Reel 13	\N	8	25	140	1	\N	Saltpond - three women singers; We all have the same grandpa; Amayki's brother etc; singing and drumming etc at Cotonou Dahemey etc; papo tribe funeral song (solo) about the present chief's father, historical song for the people and the country	\N	\N	\N	\N
400	local	00000423	2006-02-28 00:00:00	2006-02-28 00:00:00	0	African field recordings: Reel 13	\N	8	25	140	1	\N	Saltpond - three women singers; We all have the same grandpa; Amayki's brother etc; singing and drumming etc at Cotonou Dahemey etc; papo tribe funeral song (solo) about the present chief's father, historical song for the people and the country	\N	\N	\N	\N
401	local	00000424	2006-02-28 00:00:00	2006-02-28 00:00:00	0	African field recordings: Reel 13	\N	8	25	140	1	\N	Saltpond - three women singers; We all have the same grandpa; Amayki's brother etc; singing and drumming etc at Cotonou Dahemey etc; papo tribe funeral song (solo) about the present chief's father, historical song for the people and the country	\N	\N	\N	\N
402	local	00000425	2006-02-28 00:00:00	2006-02-28 00:00:00	0	African field recordings: Reel 14	\N	8	25	140	1	\N	Dahomey Yu: funeral song no. 1 (solo); funeral song no.2 (solo); war song (drums, rattles and singers); war song continued; Kokoro	\N	\N	\N	\N
403	local	00000426	2006-02-28 00:00:00	2006-02-28 00:00:00	0	African field recordings: Reel 14	\N	8	25	140	1	\N	Dahomey Yu: funeral song no. 1 (solo); funeral song no.2 (solo); war song (drums, rattles and singers); war song continued; Kokoro	\N	\N	\N	\N
404	local	00000427	2006-02-28 00:00:00	2006-02-28 00:00:00	0	African field recordings: Reel 14	\N	8	25	140	1	\N	Dahomey Yu: funeral song no. 1 (solo); funeral song no.2 (solo); war song (drums, rattles and singers); war song continued; Kokoro	\N	\N	\N	\N
405	local	00000428	2006-02-28 00:00:00	2006-02-28 00:00:00	0	African field recordings: Reel 14	\N	8	25	140	1	\N	Dahomey Yu: funeral song no. 1 (solo); funeral song no.2 (solo); war song (drums, rattles and singers); war song continued; Kokoro	\N	\N	\N	\N
406	local	00000429	2006-02-28 00:00:00	2006-02-28 00:00:00	0	African field recordings: Reel 14	\N	8	25	140	1	\N	Dahomey Yu: funeral song no. 1 (solo); funeral song no.2 (solo); war song (drums, rattles and singers); war song continued; Kokoro	\N	\N	\N	\N
407	local	00000430	2006-02-28 00:00:00	2006-02-28 00:00:00	0	African field recordings: Reel 14	\N	8	25	140	1	\N	Dahomey Yu: funeral song no. 1 (solo); funeral song no.2 (solo); war song (drums, rattles and singers); war song continued; Kokoro	\N	\N	\N	\N
408	local	00000431	2006-02-28 00:00:00	2006-02-28 00:00:00	0	African field recordings: Reel 14	\N	8	25	140	1	\N	Dahomey Yu: funeral song no. 1 (solo); funeral song no.2 (solo); war song (drums, rattles and singers); war song continued; Kokoro	\N	\N	\N	\N
409	local	00000432	2006-02-28 00:00:00	2006-02-28 00:00:00	0	African field recordings: Reel 14	\N	8	25	140	1	\N	Dahomey Yu: funeral song no. 1 (solo); funeral song no.2 (solo); war song (drums, rattles and singers); war song continued; Kokoro	\N	\N	\N	\N
410	local	00000433	2006-02-28 00:00:00	2006-02-28 00:00:00	0	African field recordings: Reel 15	\N	8	25	140	1	\N	Lago Kokaro and his JuJu; Abeokuta singers and drums; recording from N.B.S. discs of African music; Itsikiri (Jecke) tribe and Udje tribe etc.; Woro festival; Youruba music Woro	\N	\N	\N	\N
411	local	00000434	2006-02-28 00:00:00	2006-02-28 00:00:00	0	African field recordings: Reel 15	\N	8	25	140	1	\N	Lago Kokaro and his JuJu; Abeokuta singers and drums; recording from N.B.S. discs of African music; Itsikiri (Jecke) tribe and Udje tribe etc.; Woro festival; Youruba music Woro	\N	\N	\N	\N
412	local	00000435	2006-02-28 00:00:00	2006-02-28 00:00:00	0	African field recordings: Reel 15	\N	8	25	140	1	\N	Lago Kokaro and his JuJu; Abeokuta singers and drums; recording from N.B.S. discs of African music; Itsikiri (Jecke) tribe and Udje tribe etc.; Woro festival; Youruba music Woro	\N	\N	\N	\N
413	local	00000436	2006-02-28 00:00:00	2006-02-28 00:00:00	0	African field recordings: Reel 15	\N	8	25	140	1	\N	Lago Kokaro and his JuJu; Abeokuta singers and drums; recording from N.B.S. discs of African music; Itsikiri (Jecke) tribe and Udje tribe etc.; Woro festival; Youruba music Woro	\N	\N	\N	\N
414	local	00000437	2006-02-28 00:00:00	2006-02-28 00:00:00	0	African field recordings: Reel 15	\N	8	25	140	1	\N	Lago Kokaro and his JuJu; Abeokuta singers and drums; recording from N.B.S. discs of African music; Itsikiri (Jecke) tribe and Udje tribe etc.; Woro festival; Youruba music Woro	\N	\N	\N	\N
415	local	00000438	2006-02-28 00:00:00	2006-02-28 00:00:00	0	African field recordings: Reel 16	\N	8	25	140	1	\N	Lagos N.B.S. from the radio tape etc.; Itsi Kiri tribe and Udje tribe; Kalabaz Choral party 1; Kalabaz Choral party 2;	\N	\N	\N	\N
416	local	00000439	2006-02-28 00:00:00	2006-02-28 00:00:00	0	African field recordings: Reel 16	\N	8	25	140	1	\N	Lagos N.B.S. from the radio tape etc.; Itsi Kiri tribe and Udje tribe; Kalabaz Choral party 1; Kalabaz Choral party 2;	\N	\N	\N	\N
417	local	00000440	2006-02-28 00:00:00	2006-02-28 00:00:00	0	African field recordings: Reel 16	\N	8	25	140	1	\N	Lagos N.B.S. from the radio tape etc.; Itsi Kiri tribe and Udje tribe; Kalabaz Choral party 1; Kalabaz Choral party 2;	\N	\N	\N	\N
418	local	00000441	2006-02-28 00:00:00	2006-02-28 00:00:00	0	African field recordings: Reel 17	\N	8	25	140	1	\N	Lagos Calabar Chorale party; funeral song women; war song men; war song continued	\N	\N	\N	\N
419	local	00000442	2006-02-28 00:00:00	2006-02-28 00:00:00	0	African field recordings: Reel 17	\N	8	25	140	1	\N	Lagos Calabar Chorale party; funeral song women; war song men; war song continued	\N	\N	\N	\N
420	local	00000443	2006-02-28 00:00:00	2006-02-28 00:00:00	0	African field recordings: Reel 17	\N	8	25	140	1	\N	Lagos Calabar Chorale party; funeral song women; war song men; war song continued	\N	\N	\N	\N
421	local	00000445	2006-02-28 00:00:00	2006-02-28 00:00:00	0	WSB9	\N	8	25	140	1	\N	Bob and Homer (edited master)	\N	\N	\N	\N
422	local	00000446	2006-02-28 00:00:00	2006-02-28 00:00:00	0	WSB7	\N	8	25	140	1	\N	Kitchen Klub	\N	\N	\N	\N
423	local	00000447	2006-02-28 00:00:00	2006-02-28 00:00:00	0	WSB11	\N	8	25	140	1	\N	Barn Dance: Intros, closing, applause	\N	\N	\N	\N
424	local	00000448	2006-02-28 00:00:00	2006-02-28 00:00:00	0	WSB17	\N	8	25	140	1	\N	Charade Parade with script	\N	\N	\N	\N
425	local	00000449	2006-02-28 00:00:00	2006-02-28 00:00:00	0	WSB18	\N	8	25	140	1	\N	The Today Show Part IV	\N	\N	\N	\N
426	local	00000450	2006-02-28 00:00:00	2006-02-28 00:00:00	0	WSB19	\N	8	25	140	1	\N	The Today Show Part III	\N	\N	\N	\N
427	local	00000451	2006-02-28 00:00:00	2006-02-28 00:00:00	0	WSB22	\N	8	25	140	1	\N	Car 48. Steve Elmo #5	\N	\N	\N	\N
428	local	00000452	2006-02-28 00:00:00	2006-02-28 00:00:00	0	WSB50	\N	8	25	140	1	\N	American Story - Benjamin Franklin	\N	\N	\N	\N
429	local	00000453	2006-02-28 00:00:00	2006-02-28 00:00:00	0	WSB64	\N	8	25	140	1	\N	Recollections at 30	\N	\N	\N	\N
430	local	00000454	2006-02-28 00:00:00	2006-02-28 00:00:00	0	WSB65	\N	8	25	140	1	\N	Recollections at 30	\N	\N	\N	\N
431	local	00000455	2006-02-28 00:00:00	2006-02-28 00:00:00	0	WSB74	\N	8	25	140	1	\N	The Juvenile Problem	\N	\N	\N	\N
432	local	00000456	2006-02-28 00:00:00	2006-02-28 00:00:00	0	WSB75	\N	8	25	140	1	\N	New shows on WSB Radio. Same as 00000457	\N	\N	\N	\N
433	local	00000457	2006-02-28 00:00:00	2006-02-28 00:00:00	0	WSB76	\N	8	25	140	1	\N	New shows on WSB Radio. Same as 00000456	\N	\N	\N	\N
434	local	00000458	2006-02-28 00:00:00	2006-02-28 00:00:00	0	WSB77	\N	8	25	140	1	\N	The Broadcasting-Telecasting Story	\N	\N	\N	\N
435	local	00000459	2006-02-28 00:00:00	2006-02-28 00:00:00	0	WSB78	\N	8	25	140	1	\N	Bob and Homer Tiger Story	\N	\N	\N	\N
436	local	00000460	2006-02-28 00:00:00	2006-02-28 00:00:00	0	WSB80	\N	8	25	140	1	\N	World news roundup intros with MacDougal	\N	\N	\N	\N
437	local	00000461	2006-02-28 00:00:00	2006-02-28 00:00:00	0	WSB81	\N	8	25	140	1	\N	\N	\N	\N	\N	\N
438	local	00000462	2006-02-28 00:00:00	2006-02-28 00:00:00	0	WSB83	\N	8	25	140	1	\N	Fire downtown	\N	\N	\N	\N
439	local	00000463	2006-02-28 00:00:00	2006-02-28 00:00:00	0	WSB84 1	\N	8	25	140	1	\N	Happy New Year breaks 4	\N	\N	\N	\N
440	local	00000464	2006-02-28 00:00:00	2006-02-28 00:00:00	0	WSB84 2	\N	8	25	140	1	\N	Happy New Year breaks 4	\N	\N	\N	\N
441	local	00000465	2006-02-28 00:00:00	2006-02-28 00:00:00	0	WSB85 1	\N	8	25	140	1	\N	Promotion IDs	\N	\N	\N	\N
442	local	00000466	2006-02-28 00:00:00	2006-02-28 00:00:00	0	WSB85 2	\N	8	25	140	1	\N	Promotion IDs	\N	\N	\N	\N
443	local	00000467	2006-02-28 00:00:00	2006-02-28 00:00:00	0	WSB87 1	\N	8	25	140	1	\N	WSB Radio 35th Anniversary	\N	\N	\N	\N
444	local	00000468	2006-02-28 00:00:00	2006-02-28 00:00:00	0	WSB87 2	\N	8	25	140	1	\N	WSB Radio 35th Anniversary	\N	\N	\N	\N
445	local	00000469	2006-02-28 00:00:00	2006-02-28 00:00:00	0	WSB88	\N	8	25	140	1	\N	The Voice Speaks	\N	\N	\N	\N
446	local	00000470	2006-02-28 00:00:00	2006-02-28 00:00:00	0	WSB89	\N	8	25	140	1	\N	The Voice Speaks WSB Anniversary Program	\N	\N	\N	\N
447	local	00000471	2006-02-28 00:00:00	2006-02-28 00:00:00	0	WSB90	\N	8	25	140	1	\N	Promo	\N	\N	\N	\N
448	local	00000472	2006-02-28 00:00:00	2006-02-28 00:00:00	0	WSB92A	\N	8	25	140	1	\N	Pan American Story: Robert E. Lee	\N	\N	\N	\N
449	local	00000473	2006-02-28 00:00:00	2006-02-28 00:00:00	0	WSB92B	\N	8	25	140	1	\N	Recollections at 30	\N	\N	\N	\N
450	local	00000474	2006-02-28 00:00:00	2006-02-28 00:00:00	0	WSB93	\N	8	25	140	1	\N	Mr. Outler Radio Week Spots	\N	\N	\N	\N
451	local	00000475	2006-02-28 00:00:00	2006-02-28 00:00:00	0	WSB1820	\N	8	25	140	1	\N	BUC at the Fox: Chim Chim Cheree, Sixteen Going on Seventeen	\N	\N	\N	\N
452	local	00000476	2006-02-28 00:00:00	2006-02-28 00:00:00	0	WSB2308B	\N	8	25	140	1	\N	Save the Fox Special Air Check	\N	\N	\N	\N
453	local	00000477	2006-02-28 00:00:00	2006-02-28 00:00:00	0	WSB1816	\N	8	25	140	1	\N	Bob Van Camp at the Fox	\N	\N	\N	\N
454	local	00000478	2006-02-28 00:00:00	2006-02-28 00:00:00	0	WSB94	\N	8	25	140	1	\N	Nat. Radio Spots	\N	\N	\N	\N
455	local	00000479	2006-02-28 00:00:00	2006-02-28 00:00:00	0	WSB99A	\N	8	25	140	1	\N	\N	\N	\N	\N	\N
456	local	00000480	2006-02-28 00:00:00	2006-02-28 00:00:00	0	WSB99B	\N	8	25	140	1	\N	Recollections at 30	\N	\N	\N	\N
457	local	00000481	2006-02-28 00:00:00	2006-02-28 00:00:00	0	WSB100	\N	8	25	140	1	\N	Stone Mountain Wedding	\N	\N	\N	\N
458	local	00000482	2006-02-28 00:00:00	2006-02-28 00:00:00	0	WSB101	\N	8	25	140	1	\N	Somebody goofed	\N	\N	\N	\N
459	local	00000483	2006-02-28 00:00:00	2006-02-28 00:00:00	0	WSB102	\N	8	25	140	1	\N	Deathless Weekend	\N	\N	\N	\N
460	local	00000484	2006-02-28 00:00:00	2006-02-28 00:00:00	0	Charlie Buchanan interview 1	\N	8	25	140	1	\N	Discussing Savoy ballroom; Interviewee VERY faint voice	\N	\N	\N	\N
461	local	00000485	2006-02-28 00:00:00	2006-02-28 00:00:00	0	Charlie Buchanan interview 2	\N	8	25	140	1	\N	Discussing Savoy ballroom; Interviewee VERY faint voice. Recording stops after about 3:50 minutes.	\N	\N	\N	\N
462	local	00000486	2006-02-28 00:00:00	2006-02-28 00:00:00	0	Strange Fruit by Josh White	\N	8	25	140	1	\N	Decca Personality Series Album No. A-447, 23654B	\N	\N	\N	\N
463	local	00000487	2006-02-28 00:00:00	2006-02-28 00:00:00	0	The House I Live in by Josh White	\N	8	25	140	1	\N	Asch Records 348-3B	\N	\N	\N	\N
464	local	00000488	2006-02-28 00:00:00	2006-02-28 00:00:00	0	Trouble by Josh White	\N	8	25	140	1	\N	Columbia Records C22-3, 35560 (CO 27416)	\N	\N	\N	\N
465	local	00000489	2006-02-28 00:00:00	2006-02-28 00:00:00	0	WSB6	\N	8	25	140	1	\N	WSB Promotional techniques - CAN NOT DUP OFF R2R	\N	\N	\N	\N
466	local	00000490	2006-02-28 00:00:00	2006-02-28 00:00:00	0	WSB10	\N	8	25	140	1	\N	Dr. Six Guns	\N	\N	\N	\N
467	local	00000491	2006-02-28 00:00:00	2006-02-28 00:00:00	0	WSB12	\N	8	25	140	1	\N	Barn Dance 10/05	\N	\N	\N	\N
468	local	00000492	2006-02-28 00:00:00	2006-02-28 00:00:00	0	WSB21	\N	8	25	140	1	\N	Today TV show	\N	\N	\N	\N
469	local	00000493	2006-02-28 00:00:00	2006-02-28 00:00:00	0	WSB23	\N	8	25	140	1	\N	Car 48 #1; religious programming	\N	\N	\N	\N
470	local	00000494	2006-02-28 00:00:00	2006-02-28 00:00:00	0	WSB24	\N	8	25	140	1	\N	Car 48: Case of the Wrong Combination	\N	\N	\N	\N
471	local	00000495	2006-02-28 00:00:00	2006-02-28 00:00:00	0	WSB25	\N	8	25	140	1	\N	Car 48 #3: Case of the Poison Pen	\N	\N	\N	\N
472	local	00000496	2006-02-28 00:00:00	2006-02-28 00:00:00	0	WSB26	\N	8	25	140	1	\N	Car 48 #2: Case of the Farewell Note	\N	\N	\N	\N
473	local	00000497	2006-02-28 00:00:00	2006-02-28 00:00:00	0	WSB27	\N	8	25	140	1	\N	Car 48: The Case of the Lure	\N	\N	\N	\N
474	local	00000498	2006-02-28 00:00:00	2006-02-28 00:00:00	0	WSB28	\N	8	25	140	1	\N	Car 48: The Case of the Wild Kid; Sammy Kaye's Sunday Serenade	\N	\N	\N	\N
475	local	00000499	2006-02-28 00:00:00	2006-02-28 00:00:00	0	WSB53	\N	8	25	140	1	\N	Recollections at 30: Judy Garland	\N	\N	\N	\N
476	local	00000500	2006-02-28 00:00:00	2006-02-28 00:00:00	0	WSB54	\N	8	25	140	1	\N	Recollections at 30	\N	\N	\N	\N
477	local	00000501	2006-02-28 00:00:00	2006-02-28 00:00:00	0	WSB55	\N	8	25	140	1	\N	Recollections at 30; part of Right to Happiness	\N	\N	\N	\N
478	local	00000502	2006-02-28 00:00:00	2006-02-28 00:00:00	0	Great Get Together 1	\N	8	25	140	1	\N	\N	\N	\N	\N	\N
479	local	00000503	2006-02-28 00:00:00	2006-02-28 00:00:00	0	Great Get Together 2	\N	8	25	140	1	\N	\N	\N	\N	\N	\N
480	local	00000504	2006-02-28 00:00:00	2006-02-28 00:00:00	0	Coca-Cola Fountain Favorites 1	\N	8	25	140	1	\N	\N	\N	\N	\N	\N
481	local	00000505	2006-02-28 00:00:00	2006-02-28 00:00:00	0	Coca-Cola Fountain Favorites 2	\N	8	25	140	1	\N	\N	\N	\N	\N	\N
482	local	00000506	2006-02-28 00:00:00	2006-02-28 00:00:00	0	Great Get Together 3; Enterprise	\N	8	25	140	1	\N	\N	\N	\N	\N	\N
483	local	00000507	2006-02-28 00:00:00	2006-02-28 00:00:00	0	Centennial; Fountain; BBC show	\N	8	25	140	1	\N	\N	\N	\N	\N	\N
484	local	00000508	2006-02-28 00:00:00	2006-02-28 00:00:00	0	Alfons Hilgers 1	\N	8	25	140	1	\N	\N	\N	\N	\N	\N
485	local	00000509	2006-02-28 00:00:00	2006-02-28 00:00:00	0	Alfons Hilgers 2	\N	8	25	140	1	\N	\N	\N	\N	\N	\N
486	local	00000510	2006-02-28 00:00:00	2006-02-28 00:00:00	0	Ambrose Pendergrast 1	\N	8	25	140	1	\N	\N	\N	\N	\N	\N
487	local	00000511	2006-02-28 00:00:00	2006-02-28 00:00:00	0	Ambrose Pendergrast 2	\N	8	25	140	1	\N	\N	\N	\N	\N	\N
488	local	00000512	2006-02-28 00:00:00	2006-02-28 00:00:00	0	Deke DeLoach 1	\N	8	25	140	1	\N	\N	\N	\N	\N	\N
489	local	00000513	2006-02-28 00:00:00	2006-02-28 00:00:00	0	Deke DeLoach 2	\N	8	25	140	1	\N	\N	\N	\N	\N	\N
490	local	00000514	2006-02-28 00:00:00	2006-02-28 00:00:00	0	Maurice Duttera 1	\N	8	25	140	1	\N	\N	\N	\N	\N	\N
491	local	00000515	2006-02-28 00:00:00	2006-02-28 00:00:00	0	Maurice Duttera 2	\N	8	25	140	1	\N	\N	\N	\N	\N	\N
492	local	00000516	2006-02-28 00:00:00	2006-02-28 00:00:00	0	WSB56	\N	8	25	140	1	\N	Recollections at 30: Composers sing own songs; News	\N	\N	\N	\N
493	local	00000517	2006-02-28 00:00:00	2006-02-28 00:00:00	0	WSB57	\N	8	25	140	1	\N	Recollections at 30: Lady in Red, Vic and Said, Al Jolson, Ben Bernie, Bill Robinson, Nick Morana, Tiger Rand;	\N	\N	\N	\N
494	local	00000518	2006-02-28 00:00:00	2006-02-28 00:00:00	0	WSB58	\N	8	25	140	1	\N	Recollections at 30: Franny Brice, Joe Penner, Ginger Rodgers, Mickey Rooney, Brenda and Cobena, Judy Garland; News	\N	\N	\N	\N
495	local	00000519	2006-02-28 00:00:00	2006-02-28 00:00:00	0	WSB59	\N	8	25	140	1	\N	Recollections at 30: Veteran's Day Special: Tallulah Bankhead, Geo. M. Cohan, bugler, Frank Munn, Mme. Schumann-Heink, FDR declares war, Iwo Jima landing, The Lunts, Kate Smith; News	\N	\N	\N	\N
496	local	00000520	2006-02-28 00:00:00	2006-02-28 00:00:00	0	WSB60	\N	8	25	140	1	\N	Recollections at 30: Al Jolson, Bing Crosby, Ed Wynn, Nelson Eddy, FDR Fireside Chat 1936, children's show, Sisters of the Skillet, Dinah Shore; News; Best of Groucho;	\N	\N	\N	\N
497	local	00000521	2006-02-28 00:00:00	2006-02-28 00:00:00	0	WSB62	\N	8	25	140	1	\N	Recollections at 30: Arthur Tracy, Neighbor Nell, Sigmund Romberg, June Walker, Edwin C. Hill, Jack Benny, Jesse Crawford; News	\N	\N	\N	\N
498	local	00000522	2006-02-28 00:00:00	2006-02-28 00:00:00	0	WSB67	\N	8	25	140	1	\N	Recollections at 30: Harriett Hilliard, Bob Burns, Elsie Janis, Gene Raymond; News; Unnamed mystery - perhaps Nick and Norah Charles	\N	\N	\N	\N
499	local	00000523	2006-02-28 00:00:00	2006-02-28 00:00:00	0	WSB68	\N	8	25	140	1	\N	Recollections at 30: Dinah Shore, Charles Laughton, Wynn Murray, Babe Didrikson Zaharias, John Bowles, Harry Lauder; News; X-1 beginning (The 7th victim)	\N	\N	\N	\N
500	local	00000524	2006-02-28 00:00:00	2006-02-28 00:00:00	0	WSB69	\N	8	25	140	1	\N	Recollections at 30: John McCormick, Beatrice Lillie, The Silver Masked Crooner (Joe White), Capistrano swallows, Paderewsky, Morton Downey; Nightbeat	\N	\N	\N	\N
501	local	00000525	2006-02-28 00:00:00	2006-02-28 00:00:00	0	WSB70	\N	8	25	140	1	\N	Recollections at 30: American album of familiar songs, Ethel Barrymore, Barry Wood and Hit Parade Orchestra, Bing Crosby, Will Rodgers, Fred Waring and Chorus, Duncan Sisters	\N	\N	\N	\N
502	local	00000526	2006-02-28 00:00:00	2006-02-28 00:00:00	0	WSB72	\N	8	25	140	1	\N	Recollections at 30 (final episode): B.A. Rolfe, Gene Austin, Snoring Comedian, Peter DeRose, Don McNeill, Whisperin' Jack Smith, Rudy Vallee; News	\N	\N	\N	\N
503	local	00000527	2006-02-28 00:00:00	2006-02-28 00:00:00	0	WSB73	\N	8	25	140	1	\N	Recollections at 30: H.V. Kaltenborne special; News	\N	\N	\N	\N
504	local	00000528	2006-02-28 00:00:00	2006-02-28 00:00:00	0	Brian Dyson 1	\N	8	25	140	1	\N	\N	\N	\N	\N	\N
505	local	00000529	2006-02-28 00:00:00	2006-02-28 00:00:00	0	Brian Dyson 2	\N	8	25	140	1	\N	\N	\N	\N	\N	\N
506	local	00000530	2006-02-28 00:00:00	2006-02-28 00:00:00	0	Lew Gregg	\N	8	25	140	1	\N	\N	\N	\N	\N	\N
507	local	00000531	2006-02-28 00:00:00	2006-02-28 00:00:00	0	Don Sisler 1	\N	8	25	140	1	\N	\N	\N	\N	\N	\N
508	local	00000532	2006-02-28 00:00:00	2006-02-28 00:00:00	0	Don Sisler 2	\N	8	25	140	1	\N	\N	\N	\N	\N	\N
509	local	00000533	2006-02-28 00:00:00	2006-02-28 00:00:00	0	Don Sisler 3	\N	8	25	140	1	\N	\N	\N	\N	\N	\N
510	local	00000534	2006-02-28 00:00:00	2006-02-28 00:00:00	0	WSB79	\N	8	25	140	1	\N	Farm Report; script of show in tape box	\N	\N	\N	\N
511	local	00000535	2006-02-28 00:00:00	2006-02-28 00:00:00	0	WSB82 - Can not dup off R2R - file does not exist	\N	8	25	140	1	\N	President Eisenhower	\N	\N	\N	\N
512	local	00000536	2006-02-28 00:00:00	2006-02-28 00:00:00	0	WSB91	\N	8	25	140	1	\N	Basketball Crowd Noise; music program - Shawnee on Delaware; Press conference of the air; telegram about basketball game in tape box	\N	\N	\N	\N
513	local	00000537	2006-02-28 00:00:00	2006-02-28 00:00:00	0	WSB95	\N	8	25	140	1	\N	Tribute to Ohio Gov. James M. Cox on his passing; program included in tape box	\N	\N	\N	\N
514	local	00000538	2006-02-28 00:00:00	2006-02-28 00:00:00	0	WSB96	\N	8	25	140	1	\N	John M. Outler Jr. retirement interview; classical music; commercial for Great Music;	\N	\N	\N	\N
515	local	00000539	2006-02-28 00:00:00	2006-02-28 00:00:00	0	WSB98	\N	8	25	140	1	\N	Herman Talmadge speech, Rome, GA; commercials; the woman in the house; poetry; Jane Pickens show	\N	\N	\N	\N
516	local	00000540	2006-02-28 00:00:00	2006-02-28 00:00:00	0	Lew Gregg 1	\N	8	25	140	1	\N	\N	\N	\N	\N	\N
517	local	00000541	2006-02-28 00:00:00	2006-02-28 00:00:00	0	Lew Gregg 2	\N	8	25	140	1	\N	\N	\N	\N	\N	\N
518	local	00000542	2006-02-28 00:00:00	2006-02-28 00:00:00	0	Lew Gregg 3	\N	8	25	140	1	\N	\N	\N	\N	\N	\N
519	local	00000543	2006-02-28 00:00:00	2006-02-28 00:00:00	0	J. H. Smit 1	\N	8	25	140	1	\N	\N	\N	\N	\N	\N
520	local	00000544	2006-02-28 00:00:00	2006-02-28 00:00:00	0	J. H. Smit 2	\N	8	25	140	1	\N	\N	\N	\N	\N	\N
521	local	00000545	2006-02-28 00:00:00	2006-02-28 00:00:00	0	Samuel B. Frank February 6, 1990 1	\N	8	25	140	1	\N	\N	\N	\N	\N	\N
522	local	00000546	2006-02-28 00:00:00	2006-02-28 00:00:00	0	Samuel B. Frank January 27, 1990 1	\N	8	25	140	1	\N	\N	Announced date is 1/27/1990 and inventory date is 1/26/1990	\N	\N	\N
523	local	00000547	2006-02-28 00:00:00	2006-02-28 00:00:00	0	Samuel B. Frank January 27, 1990 2	\N	8	25	140	1	\N	\N	Announced date is 1/27/1990 and inventory date is 1/26/1990	\N	\N	\N
524	local	00000548	2006-02-28 00:00:00	2006-02-28 00:00:00	0	Samuel B. Frank January 28, 1990 1	\N	8	25	140	1	\N	\N	\N	\N	\N	\N
525	local	00000549	2006-02-28 00:00:00	2006-02-28 00:00:00	0	Samuel B. Frank January 28, 1990 2	\N	8	25	140	1	\N	\N	\N	\N	\N	\N
526	local	00000550	2006-02-28 00:00:00	2006-02-28 00:00:00	0	Charles and Lillian Schifilliti 1	\N	8	25	140	1	\N	\N	\N	\N	\N	\N
527	local	00000551	2006-02-28 00:00:00	2006-02-28 00:00:00	0	Charles and Lillian Schifilliti 2	\N	8	25	140	1	\N	\N	\N	\N	\N	\N
528	local	00000552	2006-02-28 00:00:00	2006-02-28 00:00:00	0	Gene Patterson	\N	8	25	140	1	\N	\N	\N	\N	\N	\N
529	local	00000553	2006-02-28 00:00:00	2006-02-28 00:00:00	0	Samuel B. Frank January 28, 1990 3	\N	8	25	140	1	\N	\N	\N	\N	\N	\N
530	local	00000554	2006-02-28 00:00:00	2006-02-28 00:00:00	0	Samuel B. Frank January 28, 1990 4	\N	8	25	140	1	\N	\N	\N	\N	\N	\N
531	local	00000555	2006-02-28 00:00:00	2006-02-28 00:00:00	0	Samuel B. Frank February 3, 1990 1	\N	8	25	140	1	\N	\N	\N	\N	\N	\N
532	local	00000556	2006-02-28 00:00:00	2006-02-28 00:00:00	0	Samuel B. Frank February 3, 1990 2	\N	8	25	140	1	\N	\N	\N	\N	\N	\N
533	local	00000557	2006-02-28 00:00:00	2006-02-28 00:00:00	0	Hyacinth Curtis interview	\N	8	25	140	1	\N	Recording begins with telephone interview in progress; interview stops and starts	\N	\N	\N	\N
534	local	00000558	2006-02-28 00:00:00	2006-02-28 00:00:00	0	Bessie Dudley interview	\N	8	25	140	1	\N	Recording begins with telephone interview in progress; interview stops and starts - names edited out; Recording ends after about 26:00	\N	\N	\N	\N
535	local	00000559	2006-02-28 00:00:00	2006-02-28 00:00:00	0	Samuel B. Frank February 6, 1990 2	\N	8	25	140	1	\N	Interview ended at 5:50	\N	\N	\N	\N
536	local	00000560	2006-02-28 00:00:00	2006-02-28 00:00:00	0	Samuel B. Frank February 26, 1990 1	\N	8	25	140	1	\N	\N	\N	\N	\N	\N
537	local	00000561	2006-02-28 00:00:00	2006-02-28 00:00:00	0	Samuel B. Frank February 26, 1990 2	\N	8	25	140	1	\N	\N	\N	\N	\N	\N
538	local	00000562	2006-02-28 00:00:00	2006-02-28 00:00:00	0	Samuel B. Frank February 26, 1990 and March 20, 1990 1	\N	8	25	140	1	\N	2/26/1990 interview ends at 18:20; 3/20/1990 interview begins at 18:21	\N	\N	\N	\N
539	local	00000563	2006-02-28 00:00:00	2006-02-28 00:00:00	0	Samuel B. Frank February 26, 1990 and March 20, 1990 2	\N	8	25	140	1	\N	\N	\N	\N	\N	\N
540	local	00000564	2006-02-28 00:00:00	2006-02-28 00:00:00	0	Samuel B. Frank  June 2, 1990	\N	8	25	140	1	\N	Interview stops at 29:40	\N	\N	\N	\N
541	local	00000565	2006-02-28 00:00:00	2006-02-28 00:00:00	0	Samuel B. Frank June 10, 1990 1	\N	8	25	140	1	\N	06/10/1990 on inventory, announced date is 06/11/1990	\N	\N	\N	\N
542	local	00000566	2006-02-28 00:00:00	2006-02-28 00:00:00	0	Samuel B. Frank June 10, 1990 2	\N	8	25	140	1	\N	06/10/1990 on inventory, announced date is 06/11/1990	\N	\N	\N	\N
543	local	00000567	2006-02-28 00:00:00	2006-02-28 00:00:00	0	Samuel B. Frank June 10, 1990 3	\N	8	25	140	1	\N	06/10/1990 on inventory, announced date is 06/11/1990; interview ended at 40:50; nothing on side B of tape.	\N	\N	\N	\N
544	local	00000568	2006-02-28 00:00:00	2006-02-28 00:00:00	0	Samuel B. Frank June 15, 1990 1	\N	8	25	140	1	\N	06/14/1990 on inventory, announced date is 06/15/1990	\N	\N	\N	\N
545	local	00000569	2006-02-28 00:00:00	2006-02-28 00:00:00	0	Samuel B. Frank June 15, 1990 2	\N	8	25	140	1	\N	06/14/1990 on inventory, announced date is 06/15/1990	\N	\N	\N	\N
546	local	00000570	2006-02-28 00:00:00	2006-02-28 00:00:00	0	Samuel B. Frank June 20, 1990 1	\N	8	25	140	1	\N	\N	\N	\N	\N	\N
547	local	00000571	2006-02-28 00:00:00	2006-02-28 00:00:00	0	Samuel B. Frank June 20, 1990 2	\N	8	25	140	1	\N	24:20 interview ended	\N	\N	\N	\N
548	local	00000572	2006-02-28 00:00:00	2006-02-28 00:00:00	0	DO NOT USE - DUPLICATE FILE - Samuel B. Frank March 20, 1990 1	\N	8	25	140	1	\N	Duplicate of 00000562-00000563, n.d. on inventory and 3/20/1990 announced	\N	\N	\N	\N
549	local	00000573	2006-02-28 00:00:00	2006-02-28 00:00:00	0	DO NOT USE - DUPLICATE FILE - Samuel B. Frank March 20, 1990 2	\N	8	25	140	1	\N	Duplicate of 00000562-00000563, n.d. on inventory and 3/20/1990 announced	\N	\N	\N	\N
550	local	00000574	2006-02-28 00:00:00	2006-02-28 00:00:00	0	Bouness, Dick 1	\N	8	25	140	1	\N	Nothing on side A of tape.	\N	\N	\N	\N
551	local	00000575	2006-02-28 00:00:00	2006-02-28 00:00:00	0	Bouness, Dick 2	\N	8	25	140	1	\N	\N	\N	\N	\N	\N
552	local	00000576	2006-02-28 00:00:00	2006-02-28 00:00:00	0	Bouness, Dick 3	\N	8	25	140	1	\N	Interview ends at 3:30	\N	\N	\N	\N
553	local	00000577	2006-02-28 00:00:00	2006-02-28 00:00:00	0	Bouness, Bebee and Elva (?)	\N	8	25	140	1	\N	Interview ends at 7:50; Side B blank.	\N	\N	\N	\N
554	local	00000578	2006-02-28 00:00:00	2006-02-28 00:00:00	0	Hill, Alice  1	\N	8	25	140	1	\N	\N	\N	\N	\N	\N
555	local	00000579	2006-02-28 00:00:00	2006-02-28 00:00:00	0	Hill, Alice  2	\N	8	25	140	1	\N	\N	\N	\N	\N	\N
556	local	00000580	2006-02-28 00:00:00	2006-02-28 00:00:00	0	Fleming, N.B. Interview of Rev. J. E. Cline and Roy Etheridge, 1	\N	8	25	140	1	\N	RT 378.758 F59i, loud hum, related file 00000580-000 00581	\N	\N	\N	\N
557	local	00000581	2006-02-28 00:00:00	2006-02-28 00:00:00	0	Oxford Alumni Event, "Welcome back Oxford Alumni to our homecoming",2	\N	8	25	140	1	\N	RT 378.758 F59i, related file 00000580-00000581, loud hum, cuts off for a second at 18:40	\N	\N	\N	\N
558	local	00000582	2006-02-28 00:00:00	2006-02-28 00:00:00	0	Ward, Judson Clements, Jr. Interviews with emeriti professors, Oxford College of Emory University, 1967, 1	\N	8	25	140	1	\N	RT 378.758 W25ie, related file 00000582-00000583, Carlton, W.A.; Strozier, E.W.; Dickey, W.J.; Eady, V.Y.C	\N	\N	\N	\N
559	local	00000583	2006-02-28 00:00:00	2006-02-28 00:00:00	0	Ward, Judson Clements, Jr. Interviews with emeriti professors, Oxford College of Emory University,  2, 1967	\N	8	25	140	1	\N	RT 378.758 W25ie, related file 00000582-00000583, Carlton, W.A.; Strozier, E.W.; Dickey, W.J.; Eady, V.Y.C. Buzz and hum in background.	\N	\N	\N	\N
560	local	00000584	2006-02-28 00:00:00	2006-02-28 00:00:00	0	Dr. White and Dean Ward talking of Old Emory at Oxford 1	\N	8	25	140	1	\N	RT 378.758 W58, related file 00000584-00000585,repeats itself at 1:40, first part stops at 29:00 then starts again.	\N	\N	\N	\N
561	local	00000585	2006-02-28 00:00:00	2006-02-28 00:00:00	0	Dr. White and Dean Ward talking of Old Emory at Oxford 2	\N	8	25	140	1	\N	RT 378.758 W58, related file 00000584-00000585, stops at 2:10	\N	\N	\N	\N
562	local	00000586	2006-02-28 00:00:00	2006-02-28 00:00:00	0	Elizer and Wilbur Harwell	\N	8	25	140	1	\N	RT 378.758 E42, related file 00000586-00000587,very hard to hear,recording of a math class, new speaker at 16:00 that can barely be heard, speaker ends at 50:00.	\N	\N	\N	\N
563	local	00000587	2006-02-28 00:00:00	2006-02-28 00:00:00	0	Elizer and Wilbur Harwell, 1	\N	8	25	140	1	\N	RT 378.758 E42, related file 00000586-00000587, strong static hum	\N	\N	\N	\N
564	local	00000588	2006-02-28 00:00:00	2006-02-28 00:00:00	0	Ward interviews W. A. Strozier and Lee W. Blitch, 1	\N	8	25	140	1	\N	RT 378.758 W25is, related file 00000588-00000589, buzz in background; Ward, Judson Clements, 1912-	\N	\N	\N	\N
565	local	00000589	2006-02-28 00:00:00	2006-02-28 00:00:00	0	Ward interviews W. A. Strozier and Lee W. Blitch, 2	\N	8	25	140	1	\N	RT 378.758 W25is, related file 00000588-00000589, buzz in background; Ward, Judson Clements, 1912-	\N	\N	\N	\N
566	local	00000590	2006-02-28 00:00:00	2006-02-28 00:00:00	0	Ward, Judson C., Jr. Interviews with women of community of Oxford, Georgia 1	\N	8	25	140	1	\N	RT 378.758 W25iw, related file 00000590-00000591	\N	\N	\N	\N
567	local	00000591	2006-02-28 00:00:00	2006-02-28 00:00:00	0	Ward, Judson C., Jr. Interviews with women of community of Oxford, Georgia 2	\N	8	25	140	1	\N	RT 378.758 W25iw, related file 00000590-00000591, interview changes at 12:00 to interviewing 4 emeritus professors	\N	\N	\N	\N
568	local	00000592	2006-02-28 00:00:00	2006-02-28 00:00:00	0	Memorial service for Dr. Charles Lester, side 1	\N	8	25	140	1	\N	 related file 00000592-00000607, hum in background	\N	\N	\N	\N
569	local	00000593	2006-02-28 00:00:00	2006-02-28 00:00:00	0	Dean Ward Interviews David Lester of Emory University 1	\N	8	25	140	1	\N	RT 378.758 W25il, related file 00000593-00000594, static hum in background	\N	\N	\N	\N
570	local	00000594	2006-02-28 00:00:00	2006-02-28 00:00:00	0	Dean Ward Interviews David Lester of Emory University 1	\N	8	25	140	1	\N	RT 378.758 W25il, related file 00000593-00000594, static hum, cuts off abruptly	\N	\N	\N	\N
571	local	00000595	2006-02-28 00:00:00	2006-02-28 00:00:00	0	Dean Fleming at Oxford (1) -1	\N	8	25	140	1	\N	RT 378.758 F59 Fleming (1), related file 00000595-00000596-00000599, Loud hum in background, hard to hear voices	\N	\N	\N	\N
572	local	00000596	2006-02-28 00:00:00	2006-02-28 00:00:00	0	Dean Fleming at Oxford (1) -2	\N	8	25	140	1	\N	RT 378.758 F59 Fleming (1), related file 00000595-00000596-00000599, background hum	\N	\N	\N	\N
573	local	00000597	2006-02-28 00:00:00	2006-02-28 00:00:00	0	Judson C. Ward interviews Lewis Lamar Clegg & Lee W. Blitch -1	\N	8	25	140	1	\N	RT 378.758 W25if, related file 00000597-00000598,  Judson C. Ward, buzz/hum at beginning of tape	\N	\N	\N	\N
574	local	00000598	2006-02-28 00:00:00	2006-02-28 00:00:00	0	Judson C. Ward interviews Lewis Lamar Clegg & Lee W. Blitch -2	\N	8	25	140	1	\N	RT 378.758 W25if, related file 00000597-00000598, static sound when people speak, strong hum at 10:30 & 12:00. Blitch interview starts at 16:00	\N	\N	\N	\N
575	local	00000599	2006-02-28 00:00:00	2006-02-28 00:00:00	0	Dean Fleming at Oxford (2) -1	\N	8	25	140	1	\N	RT 378.758 F59 Fleming  (2), related file 00000595-00000596,00000599, side 2 is blank, buzz/hum in background	\N	\N	\N	\N
576	local	00000600	2006-02-28 00:00:00	2006-02-28 00:00:00	0	Choral Music Concert, Glenn Memorial Auditorium	\N	8	25	140	1	\N	Welcome and Introductions: Linda Matthews 00:20; Delores Crowell 07:30; James Wagner 08:54	\N	\N	\N	\N
577	local	00000601	2006-02-28 00:00:00	2006-02-28 00:00:00	0	Rebel Irishwomen: Helena Molony	\N	8	25	140	1	\N	Related files: 00000601-00000602; transferred on patron request; Claddagh Records Ltd.	\N	\N	\N	\N
578	local	00000602	2006-02-28 00:00:00	2006-02-28 00:00:00	0	Rebel Irishwomen: Helena Molony, Kathleen Behan, Maud Gonne MacBride	\N	8	25	140	1	\N	Related files: 00000601-00000602; transferred on patron request; Claddagh Records Ltd.	\N	\N	\N	\N
579	local	00000603	2006-02-28 00:00:00	2006-02-28 00:00:00	0	Unknown (case label that says Mathew is incorrect)	\N	8	25	140	1	\N	Related files: 00000603-00000604, Martin Luther King's "I have a dream" speech, NPR recording, at 19:00 min the NPR recording becomes opera/Chanuka music	\N	\N	\N	\N
580	local	00000604	2006-02-28 00:00:00	2006-02-28 00:00:00	0	Unknown (case label that says Mathew is incorrect)	\N	8	25	140	1	\N	Related files: 00000603-00000604, Program recording of "Festival of Lights", explanation of Chanuka and Chanuka hymns	\N	\N	\N	\N
581	local	00000605	2006-02-28 00:00:00	2006-02-28 00:00:00	0	Unknown	\N	8	25	140	1	\N	Barcode #16043006, related files 00000605-00000606, hum in background can hardly hear voices, relates to the Civil War	\N	\N	\N	\N
582	local	00000606	2006-02-28 00:00:00	2006-02-28 00:00:00	0	Unknown	\N	8	25	140	1	\N	Barcode #16043006, related files 00000605-00000606, relates to the Civil War	\N	\N	\N	\N
583	local	00000607	2006-02-28 00:00:00	2006-02-28 00:00:00	0	Memorial service for Dr. Charles Lester  2	\N	8	25	140	1	\N	 related file 00000592-00000607, strong hum/buzz in background	\N	\N	\N	\N
584	local	00000608	2006-02-28 00:00:00	2006-02-28 00:00:00	0	Bill Sharpe 1	\N	8	25	140	1	\N	Buzz in background, music in background when Sharp speaks	\N	\N	\N	\N
585	local	00000609	2006-02-28 00:00:00	2006-02-28 00:00:00	0	Bill Sharpe 2	\N	8	25	140	1	\N	Buzz in background, music fades in and out	\N	\N	\N	\N
586	local	00000610	2006-02-28 00:00:00	2006-02-28 00:00:00	0	Jasper Yeomans 1	\N	8	25	140	1	\N	\N	\N	\N	\N	\N
587	local	00000611	2006-02-28 00:00:00	2006-02-28 00:00:00	0	Jasper Yeomans 2	\N	8	25	140	1	\N	\N	\N	\N	\N	\N
588	local	00000612	2006-02-28 00:00:00	2006-02-28 00:00:00	0	E. Neville Isdell  1	\N	8	25	140	1	\N	Buzz in background, Pendergrast's voice faint, background music can be heard	\N	\N	\N	\N
589	local	00000613	2006-02-28 00:00:00	2006-02-28 00:00:00	0	Ika Herbert - DO NOT USE - DUPLICATE - SEE 00000043	\N	8	25	140	1	\N	Buzz in background, interview very hard to hear, loud music in background	\N	\N	\N	\N
590	local	00000614	2006-02-28 00:00:00	2006-02-28 00:00:00	0	Mladin Zarubica 1	\N	8	25	140	1	\N	Telephone interview	\N	\N	\N	\N
591	local	00000615	2006-02-28 00:00:00	2006-02-28 00:00:00	0	Otis, Madeline Zack 1	\N	8	25	140	1	\N	09/04/1990 date on inventory, announced date is 09/03/1990	\N	\N	\N	\N
592	local	00000616	2006-02-28 00:00:00	2006-02-28 00:00:00	0	Otis, Madeline Zack 2	\N	8	25	140	1	\N	09/04/1990 date on inventory, announced date is 09/03/1990	\N	\N	\N	\N
593	local	00000617	2006-02-28 00:00:00	2006-02-28 00:00:00	0	Rita Ann Higgins 1	\N	8	25	140	1	\N	Related files: 00000617-00000618	\N	\N	\N	\N
594	local	00000618	2006-02-28 00:00:00	2006-02-28 00:00:00	0	Rita Ann Higgins 2	\N	8	25	140	1	\N	Related files: 00000617-00000618. Interview ends at 23:00	\N	\N	\N	\N
595	local	00000619	2006-02-28 00:00:00	2006-02-28 00:00:00	0	Paula Meehan at Marion Square 1	\N	8	25	140	1	\N	Related files: 00000619-00000620. Interview ends at 58:00. Background noise.	\N	\N	\N	\N
596	local	00000620	2006-02-28 00:00:00	2006-02-28 00:00:00	0	Paula Meehan at Marion Square 2	\N	8	25	140	1	\N	Related files: 00000619-00000620. Interview starts at 05:00 and ends at 17:15.	\N	\N	\N	\N
597	local	00000621	2006-02-28 00:00:00	2006-02-28 00:00:00	0	Nuala N. Dhomhnaill 1	\N	8	25	140	1	\N	Related files: 00000621-00000622. Background noise.	\N	\N	\N	\N
598	local	00000622	2006-02-28 00:00:00	2006-02-28 00:00:00	0	Nuala N. Dhomhnaill 2	\N	8	25	140	1	\N	Related files: 00000621-00000622. Background noise. Interview begins at 03:00.	\N	\N	\N	\N
599	local	00000623	2006-02-28 00:00:00	2006-02-28 00:00:00	0	Jones, Clay and Rose 1	\N	8	25	140	1	\N	21:11 recording ends	\N	\N	\N	\N
600	local	00000624	2006-02-28 00:00:00	2006-02-28 00:00:00	0	Jones, Clay and Rose 2	\N	8	25	140	1	\N	18:40 recording ends	\N	\N	\N	\N
601	local	00000625	2006-02-28 00:00:00	2006-02-28 00:00:00	0	Otis, Madeline Zack 3	\N	8	25	140	1	\N	\N	\N	\N	\N	\N
602	local	00000626	2006-02-28 00:00:00	2006-02-28 00:00:00	0	Otis, Madeline Zack 4	\N	8	25	140	1	\N	Interview ends at 7:40; inventory says side B is blank - this is incorrect.	\N	\N	\N	\N
603	local	00000627	2006-02-28 00:00:00	2006-02-28 00:00:00	0	WSB236	\N	8	25	140	1	\N	The Man Behind the Legend: A Tribute to Arturo Toscanini, pt. 1	\N	\N	\N	\N
604	local	00000628	2006-02-28 00:00:00	2006-02-28 00:00:00	0	WSB87	\N	8	25	140	1	\N	WSB Radio 35th Anniversary	\N	\N	\N	\N
605	local	00000629	2006-02-28 00:00:00	2006-02-28 00:00:00	0	WSB83	\N	8	25	140	1	\N	Fire Downtown live report; Three Star Extra: weather, news, sports	\N	\N	\N	\N
606	local	00000630	2006-02-28 00:00:00	2006-02-28 00:00:00	0	WSB77	\N	8	25	140	1	\N	Voice of the South: Broadcasting and Telecasting Story	\N	\N	\N	\N
607	local	00000631	2006-02-28 00:00:00	2006-02-28 00:00:00	0	WSB2	\N	8	25	140	1	\N	WSB 34th Anniversary: Radio Looks Ahead, pt. 2	\N	\N	\N	\N
608	local	00000632	2006-02-28 00:00:00	2006-02-28 00:00:00	0	WSB1	\N	8	25	140	1	\N	WSB 34th Anniversary: Radio Looks Ahead, pt. 2	\N	\N	\N	\N
609	local	00000633	2006-02-28 00:00:00	2006-02-28 00:00:00	0	Mrs. Woodruff's Funeral: Ministers Only	\N	8	25	140	1	\N	Recording ends at about 15:32.	\N	\N	\N	\N
610	local	00000634	2006-02-28 00:00:00	2006-02-28 00:00:00	0	Mrs. Woodruff's Funeral Complete Tape: Music and Ministers	\N	8	25	140	1	\N	Very poor sound quality. Recording ends at about 42:00.	\N	\N	\N	\N
611	local	00000635	2006-02-28 00:00:00	2006-02-28 00:00:00	0	Mladin Zarubica 2	\N	8	25	140	1	\N	Telephone interview	\N	\N	\N	\N
612	local	00000636	2006-02-28 00:00:00	2006-02-28 00:00:00	0	Vera Gordon	\N	8	25	140	1	\N	Very loud hum and faint voices - almost inaudible.	\N	\N	\N	\N
613	local	00000637	2006-02-28 00:00:00	2006-02-28 00:00:00	0	Sam Ayoub 3	\N	8	25	140	1	\N	\N	\N	\N	\N	\N
614	local	00000638	2006-02-28 00:00:00	2006-02-28 00:00:00	0	Morton Hodgson 3	\N	8	25	140	1	\N	Slight buzz in background, vacuum cleaner noise in background	\N	\N	\N	\N
615	local	00000639	2006-02-28 00:00:00	2006-02-28 00:00:00	0	Morton Hodgson 4	\N	8	25	140	1	\N	Slight buzz in background. Interview ends abruptly	\N	\N	\N	\N
616	local	00000640	2006-02-28 00:00:00	2006-02-28 00:00:00	0	Ovid Davis 1	\N	8	25	140	1	\N	\N	\N	\N	\N	\N
617	local	00000641	2006-02-28 00:00:00	2006-02-28 00:00:00	0	Memories by Pat Frank Talking with son Mike 1	\N	8	25	140	1	\N	\N	\N	\N	\N	\N
618	local	00000642	2006-02-28 00:00:00	2006-02-28 00:00:00	0	Memories by Pat Frank Talking with son Mike 2	\N	8	25	140	1	\N	\N	\N	\N	\N	\N
619	local	00000643	2006-02-28 00:00:00	2006-02-28 00:00:00	0	Memories by Pat Frank 3	\N	8	25	140	1	\N	\N	\N	\N	\N	\N
620	local	00000644	2006-02-28 00:00:00	2006-02-28 00:00:00	0	Memories by Pat Frank 4	\N	8	25	140	1	\N	\N	\N	\N	\N	\N
621	local	00000645	2006-02-28 00:00:00	2006-02-28 00:00:00	0	Memories by Pat Frank 5	\N	8	25	140	1	\N	\N	\N	\N	\N	\N
622	local	00000646	2006-02-28 00:00:00	2006-02-28 00:00:00	0	Memories by Pat Frank 6	\N	8	25	140	1	\N	\N	\N	\N	\N	\N
623	local	00000647	2006-02-28 00:00:00	2006-02-28 00:00:00	0	Aubrey Morris [WSB News Director] reporting on George Bright trial [for bombing the temple on Peachtree Street]	\N	8	25	140	1	\N	This was transferred from a CD-R recording but when the reel-to-reel is located, a transfer of that should replace this.	\N	\N	\N	\N
624	local	00000648	2006-02-28 00:00:00	2006-02-28 00:00:00	0	Barndance	\N	8	25	140	1	\N	This was transferred from a CD-R recording but when the reel-to-reel is located, a transfer of that should replace this.	\N	\N	\N	\N
625	local	00000649	2006-02-28 00:00:00	2006-02-28 00:00:00	0	Sibley Commission Testimony [Georgia General Assembly Committee on Schools]	\N	8	25	140	1	\N	This was transferred from a CD-R recording but when the reel-to-reel is located, a transfer of that should replace this.	\N	\N	\N	\N
626	local	00000650	2006-02-28 00:00:00	2006-02-28 00:00:00	0	Memories by Pat Frank 7	\N	8	25	140	1	\N	\N	\N	\N	\N	\N
627	local	00000651	2006-02-28 00:00:00	2006-02-28 00:00:00	0	Memories by Pat Frank 8	\N	8	25	140	1	\N	Interview ends at 11:00	\N	\N	\N	\N
628	local	00000652	2006-02-28 00:00:00	2006-02-28 00:00:00	0	Memories by Pat Frank 9	\N	8	25	140	1	\N	\N	\N	\N	\N	\N
629	local	00000653	2006-02-28 00:00:00	2006-02-28 00:00:00	0	Memories by Pat Frank 10	\N	8	25	140	1	\N	\N	\N	\N	\N	\N
630	local	00000654	2006-02-28 00:00:00	2006-02-28 00:00:00	0	Shakespeare and the Goddess of Complete Being Tape 14 Side B	\N	8	25	140	1	\N	Ted Hughes dictating to typist named Judith: chapter 53	\N	\N	\N	\N
631	local	00000655	2006-02-28 00:00:00	2006-02-28 00:00:00	0	Kevin Young reading	\N	8	25	140	1	\N	Inaugural reading of Raymond Danowski Poetry Library Reading Series. Speakers: Steve Ennis, Prof. Walter Kalashia, Kevin Young	\N	\N	\N	\N
632	local	00000656	2006-02-28 00:00:00	2006-02-28 00:00:00	0	Shakespeare and the Goddess of Complete Being Tape 1 Side A	\N	8	25	140	1	\N	Ted Hughes dictating to typist named Judith: chapter 1	\N	\N	\N	\N
633	local	00000657	2006-02-28 00:00:00	2006-02-28 00:00:00	0	Shakespeare and the Goddess of Complete Being Tape 2 Side A	\N	8	25	140	1	\N	Ted Hughes dictating to typist named Judith: chapter 1 continued	\N	\N	\N	\N
634	local	00000658	2006-02-28 00:00:00	2006-02-28 00:00:00	0	Shakespeare and the Goddess of Complete Being Tape 3 Side A	\N	8	25	140	1	\N	Ted Hughes dictating to typist named Judith: chapter 1 continued	\N	\N	\N	\N
635	local	00000659	2006-02-28 00:00:00	2006-02-28 00:00:00	0	Shakespeare and the Goddess of Complete Being Tape 3 Side B	\N	8	25	140	1	\N	Ted Hughes dictating to typist named Judith: chapter 1 continued	\N	\N	\N	\N
636	local	00000660	2006-02-28 00:00:00	2006-02-28 00:00:00	0	Shakespeare and the Goddess of Complete Being Tape 4 Side A	\N	8	25	140	1	\N	Ted Hughes dictating to typist named Judith: Appendix, chapter 2 (starts 24:00), chapter 3	\N	\N	\N	\N
637	local	00000661	2006-02-28 00:00:00	2006-02-28 00:00:00	0	Shakespeare and the Goddess of Complete Being Tape 4 Side B	\N	8	25	140	1	\N	Ted Hughes dictating to typist named Judith: chapter 3 continued, chapter 4 (starts 27:00)	\N	\N	\N	\N
638	local	00000662	2006-02-28 00:00:00	2006-02-28 00:00:00	0	Shakespeare and the Goddess of Complete Being Tape 5 Side A	\N	8	25	140	1	\N	Ted Hughes dictating to typist named Judith: chapter 4 continued, section 3 chapter 5 (starts 11:30), chapter 8 (starts 24:07), chapter 11 (starts 40:00). Note: The chapter numbers may not be correct but are recorded according to Hughes' dictation.	\N	\N	\N	\N
639	local	00000663	2006-02-28 00:00:00	2006-02-28 00:00:00	0	Shakespeare and the Goddess of Complete Being Tape 5 Side B	\N	8	25	140	1	\N	Ted Hughes dictating to typist named Judith: chapter 7 continued, chapter 12 (starts 23:00).	\N	\N	\N	\N
640	local	00000664	2006-02-28 00:00:00	2006-02-28 00:00:00	0	Shakespeare and the Goddess of Complete Being Tape 12 Side A	\N	8	25	140	1	\N	Ted Hughes dictating to typist named Judith: chapters unknown	\N	\N	\N	\N
641	local	00000665	2006-02-28 00:00:00	2006-02-28 00:00:00	0	Shakespeare and the Goddess of Complete Being Tape 12 Side B	\N	8	25	140	1	\N	Ted Hughes dictating to typist named Judith: chapters unknown	\N	\N	\N	\N
642	local	00000666	2006-02-28 00:00:00	2006-02-28 00:00:00	0	Shakespeare and the Goddess of Complete Being Tape 14 Side A	\N	8	25	140	1	\N	Ted Hughes dictating to typist named Judith: chapters unknown	\N	\N	\N	\N
643	local	00000667	2006-02-28 00:00:00	2006-02-28 00:00:00	0	Shakespeare and the Goddess of Complete Being Tape 6 Side A	\N	8	25	140	1	\N	Ted Hughes dictating to typist named Judith: chapter 12 continued, chapter 14 (starts 9:30). Chapter 13 skipped.	\N	\N	\N	\N
644	local	00000668	2006-02-28 00:00:00	2006-02-28 00:00:00	0	Shakespeare and the Goddess of Complete Being Tape 6 Side B	\N	8	25	140	1	\N	Ted Hughes dictating to typist named Judith: chapter 14 continued, chapter 15 (starts 6:00), chapter 16 (starts 32:30), section 4 (starts 45:00).	\N	\N	\N	\N
645	local	00000669	2006-02-28 00:00:00	2006-02-28 00:00:00	0	Shakespeare and the Goddess of Complete Being Tape 8 Side A	\N	8	25	140	1	\N	Ted Hughes dictating to typist named Judith: chapter 25 continued	\N	\N	\N	\N
646	local	00000670	2006-02-28 00:00:00	2006-02-28 00:00:00	0	Shakespeare and the Goddess of Complete Being Tape 8 Side B	\N	8	25	140	1	\N	Ted Hughes dictating to typist named Judith: section 5, chapter 27 (starts 27:30). Chapter 26 skipped.	\N	\N	\N	\N
647	local	00000671	2006-02-28 00:00:00	2006-02-28 00:00:00	0	Shakespeare and the Goddess of Complete Being Tape 7 Side A	\N	8	25	140	1	\N	Ted Hughes dictating to typist named Judith: chapter 22 (TH acknowledges jump in chapters), chapter 23 (starts 13:00), chapter 24 (starts 22:50).	\N	\N	\N	\N
648	local	00000672	2006-02-28 00:00:00	2006-02-28 00:00:00	0	Shakespeare and the Goddess of Complete Being Tape 7 Side B	\N	8	25	140	1	\N	Ted Hughes dictating to typist named Judith: chapter 24 continued, chapter 25 (starts 3:15).	\N	\N	\N	\N
649	local	00000673	2006-02-28 00:00:00	2006-02-28 00:00:00	0	Shakespeare and the Goddess of Complete Being Tape 9 Side A	\N	8	25	140	1	\N	Ted Hughes dictating to typist named Judith: chapter 27 continued, chapter 29 (starts 26:00). Chapter 28 skipped.	\N	\N	\N	\N
650	local	00000674	2006-02-28 00:00:00	2006-02-28 00:00:00	0	Shakespeare and the Goddess of Complete Being Tape 9 Side B	\N	8	25	140	1	\N	Ted Hughes dictating to typist named Judith: chapter 29 continued.	\N	\N	\N	\N
651	local	00000675	2006-02-28 00:00:00	2006-02-28 00:00:00	0	Shakespeare and the Goddess of Complete Being Tape 10 Side A	\N	8	25	140	1	\N	Ted Hughes dictating to typist named Judith: chapter 30, chapter 31 (starts 17:20), chapter 32 (starts 43:40).	\N	\N	\N	\N
652	local	00000676	2006-02-28 00:00:00	2006-02-28 00:00:00	0	Shakespeare and the Goddess of Complete Being Tape 10 Side B	\N	8	25	140	1	\N	Ted Hughes dictating to typist named Judith: chapter 32 continued, chapter 33 (starts 7:15), chapter 34 (starts 19:00), chapter 35 (starts 41:00).	\N	\N	\N	\N
653	local	00000677	2006-02-28 00:00:00	2006-02-28 00:00:00	0	Shakespeare and the Goddess of Complete Being Tape 11 Side A	\N	8	25	140	1	\N	Ted Hughes dictating to typist named Judith: chapter 35 continued, chapter 36 (starts 9:10), chapter 37 (starts 19:30), chapter 38 (starts 29:00), chapter 39 (starts 32:20).	\N	\N	\N	\N
654	local	00000678	2006-02-28 00:00:00	2006-02-28 00:00:00	0	Shakespeare and the Goddess of Complete Being Tape 11 Side B	\N	8	25	140	1	\N	Ted Hughes dictating to typist named Judith: chapter 39 continued, chapter 40 (starts 11:20), chapter 41 (starts 37:50).	\N	\N	\N	\N
655	local	00000679	2006-02-28 00:00:00	2006-02-28 00:00:00	0	Shakespeare and the Goddess of Complete Being Tape 13 Side A	\N	8	25	140	1	\N	Ted Hughes dictating to typist named Judith: chapter 44 continued, chapter 45 (starts 08:30), chapter 46 (starts 15:00), chapter 47 (starts 32:05).	\N	\N	\N	\N
656	local	00000680	2006-02-28 00:00:00	2006-02-28 00:00:00	0	Shakespeare and the Goddess of Complete Being Tape 13 Side B	\N	8	25	140	1	\N	Ted Hughes dictating to typist named Judith: chapter 47 continued, chapter 48 (starts 08:00).	\N	\N	\N	\N
657	local	00000681	2006-02-28 00:00:00	2006-02-28 00:00:00	0	Shakespeare and the Goddess of Complete Being Tape 16 Side A	\N	8	25	140	1	\N	Ted Hughes dictating to typist named Judith: chapter 56 continued, chapter 57 (starts 09:35).	\N	\N	\N	\N
658	local	00000682	2006-02-28 00:00:00	2006-02-28 00:00:00	0	Shakespeare and the Goddess of Complete Being 4 Introduction	\N	8	25	140	1	\N	Ted Hughes dictating to typist named Judith: Introduction	\N	\N	\N	\N
659	local	00000683	2006-02-28 00:00:00	2006-02-28 00:00:00	0	Shakespeare and the Goddess of Complete Being 25D end	\N	8	25	140	1	\N	Ted Hughes dictating to typist named Judith: chapter 25D continued.	\N	\N	\N	\N
660	local	00000684	2006-02-28 00:00:00	2006-02-28 00:00:00	0	Shakespeare and the Goddess of Complete Being	\N	8	25	140	1	\N	Ted Hughes dictating to typist named Judith: dictation begins Years ago in a brief note to an Anthology …	\N	\N	\N	\N
661	local	00000685	2006-02-28 00:00:00	2006-02-28 00:00:00	0	Urgent 1	\N	8	25	140	1	\N	Ted Hughes dictating to typist named Judith: dictation begins This is a piece I'd like you to do …	\N	\N	\N	\N
662	local	00000686	2006-02-28 00:00:00	2006-02-28 00:00:00	0	Urgent 2	\N	8	25	140	1	\N	Ted Hughes dictating to typist named Judith: dictation begins Learned writers simply appropriated foreign words …	\N	\N	\N	\N
663	local	00000687	2006-02-28 00:00:00	2006-02-28 00:00:00	0	The Poet Speaks: Sylvia Plath interviewed by Peter Orr	\N	8	25	140	1	\N	BBC recording.	\N	\N	\N	\N
664	local	00000688	2006-02-28 00:00:00	2006-02-28 00:00:00	0	Shakespeare and the Goddess of Complete Being Tape 15 Side A	\N	8	25	140	1	\N	Ted Hughes dictating to typist named Judith: chapter 53 continued, chapter 54 (starts 32:00).	\N	\N	\N	\N
665	local	00000689	2006-02-28 00:00:00	2006-02-28 00:00:00	0	Shakespeare and the Goddess of Complete Being Tape 15 Side B	\N	8	25	140	1	\N	Ted Hughes dictating to typist named Judith: chapter 54 continued, chapter 55 (starts 15:51), chapter 56 (starts 40:41).	\N	\N	\N	\N
666	local	00000690	2006-02-28 00:00:00	2006-02-28 00:00:00	0	Shakespeare and the Goddess of Complete Being Introduction	\N	8	25	140	1	\N	Ted Hughes dictating to typist named Judith: Introduction	\N	\N	\N	\N
667	local	00000691	2006-02-28 00:00:00	2006-02-28 00:00:00	0	Shakespeare and the Goddess of Complete Being 25A	\N	8	25	140	1	\N	Ted Hughes dictating to typist named Judith: chapter 25B continued, chapter 25C (starts 30:00).	\N	\N	\N	\N
668	local	00000692	2006-02-28 00:00:00	2006-02-28 00:00:00	0	Shakespeare and the Goddess of Complete Being 25B	\N	8	25	140	1	\N	Ted Hughes dictating to typist named Judith: chapter 25C continued, chapter 25D (starts 26:01).	\N	\N	\N	\N
669	local	00000693	2006-02-28 00:00:00	2006-02-28 00:00:00	0	Shakespeare and the Goddess of Complete Being	\N	8	25	140	1	\N	Ted Hughes dictating to typist named Judith: dictation begins Venus and Adonis …	\N	\N	\N	\N
670	local	00000694	2006-02-28 00:00:00	2006-02-28 00:00:00	0	Service of Thanksgiving for the Life and Work of Ted Hughes 1	\N	8	25	140	1	\N	\N	\N	\N	\N	\N
671	local	00000695	2006-02-28 00:00:00	2006-02-28 00:00:00	0	Service of Thanksgiving for the Life and Work of Ted Hughes 2	\N	8	25	140	1	\N	\N	\N	\N	\N	\N
672	local	00000696	2006-02-28 00:00:00	2006-02-28 00:00:00	0	Choral Music Concert, Glenn Memorial Auditorium	\N	8	25	140	1	\N	Emory University Concert Choir. Oh, What a Beautiful City 01:38; Remarks 05:20; Out in the Fields 06:49; Ezekiel Saw de Wheel 10:25	\N	\N	\N	\N
673	local	00000697	2006-02-28 00:00:00	2006-02-28 00:00:00	0	Choral Music Concert, Glenn Memorial Auditorium	\N	8	25	140	1	\N	Glenn Chancel Choir. Remarks  01:35; Hallelujah 02:46; True Religion 07:44; You're Tired Chile 10:49	\N	\N	\N	\N
674	local	00000698	2006-02-28 00:00:00	2006-02-28 00:00:00	0	Choral Music Concert, Glenn Memorial Auditorium	\N	8	25	140	1	\N	Clark Atlanta University Philharmonic Society. Remarks 02:41; There's a Little Wheel a-Turnin in my Heart 03:32; There is a Balm in Gilead 06:51; Behold the Star 11:09	\N	\N	\N	\N
675	local	00000699	2006-02-28 00:00:00	2006-02-28 00:00:00	0	Choral Music Concert, Glenn Memorial Auditorium	\N	8	25	140	1	\N	Atlanta Sacred Chorale. Hail Mary 02:41, Everytime I Feel the Spirit 07:36; In His Care-O 09:40	\N	\N	\N	\N
676	local	00000700	2006-02-28 00:00:00	2006-02-28 00:00:00	0	Choral Music Concert, Glenn Memorial Auditorium	\N	8	25	140	1	\N	Tuskegee University Golden Voices Choir. Ain'a That Good News  03:44; remarks 05:43, Jesus Walked this Lonesome Valley 07:20; I Wan' to be Ready 11:06; Before the Sun Goes Down 15:34	\N	\N	\N	\N
677	local	00000701	2006-02-28 00:00:00	2006-02-28 00:00:00	0	Choral Music Concert, Glenn Memorial Auditorium	\N	8	25	140	1	\N	Combined Choirs. Remarks 03:20; Pilgrim's Chorus for Tannhauser 03:38; Remarks 08:30;  God, I Need Thee 09:30; Soon-Ah Will Be Done 15:50	\N	\N	\N	\N
678	local	00000702	2006-02-28 00:00:00	2006-02-28 00:00:00	0	Chamber Music Concert, Emerson Concert Hall Schwartz Center for Performing Arts	\N	8	25	140	1	\N	Sonata in A Minor: Allego moderato 03:30, Largo 11:40, Moderator 17:48	\N	\N	\N	\N
679	local	00000703	2006-02-28 00:00:00	2006-02-28 00:00:00	0	Chamber Music Concert, Emerson Concert Hall Schwartz Center for Performing Arts	\N	8	25	140	1	\N	Let the Wind Cry …How I Adore Thee 02:18; I am in Doubt 05:20; Romance for Alto Saxophone 11:42	\N	\N	\N	\N
680	local	00000704	2006-02-28 00:00:00	2006-02-28 00:00:00	0	Chamber Music Concert, Emerson Concert Hall Schwartz Center for Performing Arts	\N	8	25	140	1	\N	Goddess Variations 03:23; Poem for Mezzo-soprano and Chamber Ensemble 21:00	\N	\N	\N	\N
681	local	00000705	2006-02-28 00:00:00	2006-02-28 00:00:00	0	Chamber Music Concert, Emerson Concert Hall Schwartz Center for Performing Arts	\N	8	25	140	1	\N	Indigena 04:26; Of Mounts and Mountains 17:36	\N	\N	\N	\N
682	local	00000706	2006-02-28 00:00:00	2006-02-28 00:00:00	0	Chamber Music Concert, Emerson Concert Hall Schwartz Center for Performing Arts	\N	8	25	140	1	\N	France Dance 01:20; Boogie Woogie Concertante for improvised solo piano, wind instruments, and percussion (1991) 14:15	\N	\N	\N	\N
683	local	00000707	2006-02-28 00:00:00	2006-02-28 00:00:00	0	New Horizons Concert MeShell Ndegeocello	\N	8	25	140	1	\N	IK tone; intro music; Fela to 14:10; Love Song 14:35; Come Smoke my Herb 21:16; Red Planetary 29:31; Sky Walker 32:25; Remarks 40:48	\N	\N	\N	\N
684	local	00000708	2006-02-28 00:00:00	2006-02-28 00:00:00	0	New Horizons Concert MeShell Ndegeocello	\N	8	25	140	1	\N	Heavy Spirits; Quentin Mac; Fellowship; Encore	\N	\N	\N	\N
685	local	00000709	2006-02-28 00:00:00	2006-02-28 00:00:00	0	Ovid Davis 3	\N	8	25	140	1	\N	\N	\N	\N	\N	\N
686	local	00000710	2006-02-28 00:00:00	2006-02-28 00:00:00	0	5th International Ted Hughes Conference: Craig Raine	\N	8	25	140	1	\N	\N	\N	\N	\N	\N
687	local	00000711	2006-02-28 00:00:00	2006-02-28 00:00:00	0	Ovid Davis 2	\N	8	25	140	1	\N	\N	\N	\N	\N	\N
688	local	00000712	2006-02-28 00:00:00	2006-02-28 00:00:00	0	Nat Harrison 1	\N	8	25	140	1	\N	\N	\N	\N	\N	\N
689	local	00000713	2006-02-28 00:00:00	2006-02-28 00:00:00	0	Nat Harrison 2	\N	8	25	140	1	\N	\N	\N	\N	\N	\N
690	local	00000714	2006-02-28 00:00:00	2006-02-28 00:00:00	0	Atlanta, Thanksgiving, 1963	\N	8	25	140	1	\N	No second track. Description on inventory list.	\N	\N	\N	\N
691	local	00000715	2006-02-28 00:00:00	2006-02-28 00:00:00	0	Atlanta, early 1965 1	\N	8	25	140	1	\N	Description on inventory list.	\N	\N	\N	\N
692	local	00000716	2006-02-28 00:00:00	2006-02-28 00:00:00	0	Atlanta, early 1965 2	\N	8	25	140	1	\N	Description on inventory list.	\N	\N	\N	\N
693	local	00000717	2006-02-28 00:00:00	2006-02-28 00:00:00	0	Atlanta, early 1964	\N	8	25	140	1	\N	No second track. Description on inventory list.	\N	\N	\N	\N
694	local	00000718	2006-02-28 00:00:00	2006-02-28 00:00:00	0	St. Augustine: MLK reaction to grand jury	\N	8	25	140	1	\N	No second track. Description on inventory list.	\N	\N	\N	\N
695	local	00000719	2006-02-28 00:00:00	2006-02-28 00:00:00	0	St. Augustine: Church singing	\N	8	25	140	1	\N	No second track. Description on inventory list.	\N	\N	\N	\N
696	local	00000720	2006-02-28 00:00:00	2006-02-28 00:00:00	0	St Augustine: "I Love Everybody" singing	\N	8	25	140	1	\N	No second track. Description on inventory list.	\N	\N	\N	\N
697	local	00000721	2006-02-28 00:00:00	2006-02-28 00:00:00	0	St Augustine: Scarey night march 1	\N	8	25	140	1	\N	Description on inventory list.	\N	\N	\N	\N
698	local	00000722	2006-02-28 00:00:00	2006-02-28 00:00:00	0	St Augustine: Scarey night march 2	\N	8	25	140	1	\N	Description on inventory list.	\N	\N	\N	\N
699	local	00000723	2006-02-28 00:00:00	2006-02-28 00:00:00	0	Neshoba, two days after disappearance	\N	8	25	140	1	\N	No second track. Description on inventory list.	\N	\N	\N	\N
700	local	00000724	2006-02-28 00:00:00	2006-02-28 00:00:00	0	Dr. Gayraud S. Wiltmore speech: Emerging Patterns of the Church's Witness Today	\N	8	25	140	1	\N	\N	\N	\N	\N	\N
701	local	00000725	2006-02-28 00:00:00	2006-02-28 00:00:00	0	Hattiesburg, Canton and Greenwood during Freedom Summer	\N	8	25	140	1	\N	No second track. Description on inventory list.	\N	\N	\N	\N
702	local	00000726	2006-02-28 00:00:00	2006-02-28 00:00:00	0	E.B. King and Mrs. Victoria Grey	\N	8	25	140	1	\N	No second track. Listed but not described on inventory list.	\N	\N	\N	\N
703	local	00000727	2006-02-28 00:00:00	2006-02-28 00:00:00	0	Colbert, GA:  Lemuel Penn killing	\N	8	25	140	1	\N	No second track. Description on inventory list.	\N	\N	\N	\N
704	local	00000728	2006-02-28 00:00:00	2006-02-28 00:00:00	0	Interview with Klan Wizard Robert Shelton	\N	8	25	140	1	\N	No second track. Description on inventory list. UHER is on tape	\N	\N	\N	\N
705	local	00000729	2006-02-28 00:00:00	2006-02-28 00:00:00	0	Greenwood, Mississippi	\N	8	25	140	1	\N	No second track. Description on inventory list.	\N	\N	\N	\N
706	local	00000730	2006-02-28 00:00:00	2006-02-28 00:00:00	0	Freedom Democratic Party Convention Jackson, Mississippi. Aug. 6, 1964 1	\N	8	25	140	1	\N	Description on inventory list.	\N	\N	\N	\N
707	local	00000731	2006-02-28 00:00:00	2006-02-28 00:00:00	0	Freedom Democratic Party Convention Jackson, Mississippi. Aug. 6, 1964 2	\N	8	25	140	1	\N	Description on inventory list.	\N	\N	\N	\N
708	local	00000732	2006-02-28 00:00:00	2006-02-28 00:00:00	0	St. Augustine:  King congratulates people for their heroism	\N	8	25	140	1	\N	No second track. Description on inventory list.	\N	\N	\N	\N
709	local	00000733	2006-02-28 00:00:00	2006-02-28 00:00:00	0	No title	\N	8	25	140	1	\N	No second track. Listed but not described on inventory list. MACARTHUR-RUFFNER "59" on back of tape box	\N	\N	\N	\N
710	local	00000734	2006-02-28 00:00:00	2006-02-28 00:00:00	0	No title	\N	8	25	140	1	\N	No second track. Listed but not described on inventory list.	\N	\N	\N	\N
711	local	00000735	2006-02-28 00:00:00	2006-02-28 00:00:00	0	#53 KKK	\N	8	25	140	1	\N	No second track. Not on inventory list.	\N	\N	\N	\N
712	local	00000736	2006-02-28 00:00:00	2006-02-28 00:00:00	0	St. Augustine: Sound & Light	\N	8	25	140	1	\N	No second track. Not on inventory list. History of St. Augustine, FL, tails out.	\N	\N	\N	\N
713	local	00000737	2006-02-28 00:00:00	2006-02-28 00:00:00	0	Haiti Invasion, Santo Domingo 1	\N	8	25	140	1	\N	Not on inventory list.	\N	\N	\N	\N
714	local	00000738	2006-02-28 00:00:00	2006-02-28 00:00:00	0	Haiti Invasion, Santo Domingo 2	\N	8	25	140	1	\N	Not on inventory list.	\N	\N	\N	\N
715	local	00000739	2006-02-28 00:00:00	2006-02-28 00:00:00	0	#51 SEAN 1	\N	8	25	140	1	\N	Not on inventory list.	\N	\N	\N	\N
716	local	00000740	2006-02-28 00:00:00	2006-02-28 00:00:00	0	#51 SEAN 2	\N	8	25	140	1	\N	Not on inventory list. Paul Goode tape #51 CD inside box	\N	\N	\N	\N
717	local	00000741	2006-02-28 00:00:00	2006-02-28 00:00:00	0	Tape #4 Pat Brett	\N	8	25	140	1	\N	No second track. Not on inventory list. Paul Goode tapes #4 CD inside box; tails out	\N	\N	\N	\N
718	local	00000742	2006-02-28 00:00:00	2006-02-28 00:00:00	0	Overseas Assignment 1	\N	8	25	140	1	\N	Not on inventory list.	\N	\N	\N	\N
719	local	00000743	2006-02-28 00:00:00	2006-02-28 00:00:00	0	Overseas Assignment 2	\N	8	25	140	1	\N	Not on inventory list.	\N	\N	\N	\N
720	local	00000744	2006-02-28 00:00:00	2006-02-28 00:00:00	0	Dr. Martin Luther King Jr. speech in Montreat NC: Church on the Final Frontier of Racial Tension	\N	8	25	140	1	\N	\N	\N	\N	\N	\N
721	local	00000745	2006-02-28 00:00:00	2006-02-28 00:00:00	0	Women's Leadership Day	\N	8	25	140	1	\N	Original program in tape box. Access copy split onto 2 CDs	\N	\N	\N	\N
722	local	00000746	2006-02-28 00:00:00	2006-02-28 00:00:00	0	Matthew G. Carter, Montclair N.J. speaker	\N	8	25	140	1	\N	Original program in tape box. Access copy split onto 2 CDs. Poor sound quality.	\N	\N	\N	\N
723	local	00000747	2006-02-28 00:00:00	2006-02-28 00:00:00	0	Men's Day Program	\N	8	25	140	1	\N	Original program in tape box. Access copy split onto 2 CDs	\N	\N	\N	\N
724	local	00000748	2006-02-28 00:00:00	2006-02-28 00:00:00	0	Mardi Gras 2005 1	\N	8	25	140	1	\N	Various interviews and ambiance. Nick Spitzer producer	\N	\N	\N	\N
725	local	00000749	2006-02-28 00:00:00	2006-02-28 00:00:00	0	Mardi Gras 2005 2	\N	8	25	140	1	\N	Flambeau interviews and Hermes Parade. Nick Spitzer producer	\N	\N	\N	\N
726	local	00000752	2006-02-28 00:00:00	2006-02-28 00:00:00	0	Women's Leadership Day	\N	8	25	140	1	\N	Original program in tape box. Access copy split onto 2 CDs	\N	\N	\N	\N
727	local	00000753	2006-02-28 00:00:00	2006-02-28 00:00:00	0	Paster G. M. Branch preaching	\N	8	25	140	1	\N	Original program in tape box.	\N	\N	\N	\N
728	local	00000754	2006-02-28 00:00:00	2006-02-28 00:00:00	0	Adams, Wilhelmia 1	\N	8	25	140	1	\N	Sony CHF60, Related files: 00000754-00000755	\N	\N	\N	\N
729	local	00000755	2006-02-28 00:00:00	2006-02-28 00:00:00	0	Adams, Wilhelmia 2	\N	8	25	140	1	\N	Sony CHF60, Related files: 00000754-00000755	\N	\N	\N	\N
730	local	00000756	2006-02-28 00:00:00	2006-02-28 00:00:00	0	Vacation Bible School	\N	8	25	140	1	\N	Original program in tape box.	\N	\N	\N	\N
731	local	00000757	2006-02-28 00:00:00	2006-02-28 00:00:00	0	Adams,Wilhelmina/Bricktop 1	\N	8	25	140	1	\N	 Related files: 00000757-00000758, interview ends at 26:08	\N	\N	\N	\N
732	local	00000758	2006-02-28 00:00:00	2006-02-28 00:00:00	0	Adams,Wilhelmina/Bricktop 2	\N	8	25	140	1	\N	 Related files: 00000757-00000758, interviewee very soft spoken	\N	\N	\N	\N
733	local	00000759	2006-02-28 00:00:00	2006-02-28 00:00:00	0	Adams,Wilhelmina 1	\N	8	25	140	1	\N	Related files: 00000759-00000760, low Background noise	\N	\N	\N	\N
734	local	00000760	2006-02-28 00:00:00	2006-02-28 00:00:00	0	Adams,Wilhelmina 2	\N	8	25	140	1	\N	Related files: 00000759-00000760, interviewed ended at 2:06	\N	\N	\N	\N
735	local	00000761	2006-02-28 00:00:00	2006-02-28 00:00:00	0	Adams,Wilhelmina 1	\N	8	25	140	1	\N	Interview ended at 18:00	\N	\N	\N	\N
736	local	00000762	2006-02-28 00:00:00	2006-02-28 00:00:00	0	Adams,Wilhelmina/Bruce,Mary 1	\N	8	25	140	1	\N	background street noise on tape, Related files: 00000762-00000763	\N	\N	\N	\N
737	local	00000763	2006-02-28 00:00:00	2006-02-28 00:00:00	0	Adams,Wilhelmina/Bruce,Mary 2	\N	8	25	140	1	\N	Tap dancing heard in the background,Interview ends at 10:00, Related files: 00000762-00000763	\N	\N	\N	\N
738	local	00000764	2006-02-28 00:00:00	2006-02-28 00:00:00	0	Anderson, Gordon 1	\N	8	25	140	1	\N	Related files: 00000764-00000765, interview ends at 28:35, "hicups" between 22:00-26:00	\N	\N	\N	\N
739	local	00000765	2006-02-28 00:00:00	2006-02-28 00:00:00	0	Anderson, Gordon 2	\N	8	25	140	1	\N	Related files: 00000764-00000765, interview ends at 16:41, microphone bumps	\N	\N	\N	\N
740	local	00000766	2006-02-28 00:00:00	2006-02-28 00:00:00	0	Faculty Meeting 1	\N	8	25	140	1	\N	Poor sound quality up to 01:30.	\N	\N	\N	\N
741	local	00000767	2006-02-28 00:00:00	2006-02-28 00:00:00	0	Interview with Emmylou Harris	\N	8	25	140	1	\N	Emmylou Harris discusses her album "Red Dirt Circle," her upbringing and move into country music, and the evolution of her voice.	\N	\N	\N	\N
742	local	00000768	2006-02-28 00:00:00	2006-02-28 00:00:00	0	Interview with Gregory Davis and Roger Lewis of the Dirty Dozen	\N	8	25	140	1	\N	See abstract	\N	\N	\N	\N
743	local	00000769	2006-02-28 00:00:00	2006-02-28 00:00:00	0	\N	\N	8	25	140	1	\N	\N	\N	\N	\N	\N
744	local	00000770	2006-02-28 00:00:00	2006-02-28 00:00:00	0	\N	\N	8	25	140	1	\N	\N	\N	\N	\N	\N
745	local	00000771	2006-02-28 00:00:00	2006-02-28 00:00:00	0	\N	\N	8	25	140	1	\N	\N	\N	\N	\N	\N
746	local	00000772	2006-02-28 00:00:00	2006-02-28 00:00:00	0	Simon Armitage	\N	8	25	140	1	\N	\N	\N	\N	\N	\N
747	local	00000773	2006-02-28 00:00:00	2006-02-28 00:00:00	0	Faculty Meeting 2	\N	8	25	140	1	\N	Recording ends about 24:00	\N	\N	\N	\N
748	local	00000774	2006-02-28 00:00:00	2006-02-28 00:00:00	0	Monday Night Rally 1	\N	8	25	140	1	\N	Poor sound quality	\N	\N	\N	\N
749	local	00000775	2006-02-28 00:00:00	2006-02-28 00:00:00	0	Monday Night Rally 2	\N	8	25	140	1	\N	Poor sound quality	\N	\N	\N	\N
750	local	00000776	2006-02-28 00:00:00	2006-02-28 00:00:00	0	Wednesday Convocation 2	\N	8	25	140	1	\N	\N	\N	\N	\N	\N
751	local	00000777	2006-02-28 00:00:00	2006-02-28 00:00:00	0	Wednesday Convocation 1	\N	8	25	140	1	\N	\N	\N	\N	\N	\N
752	local	00000778	2006-02-28 00:00:00	2006-02-28 00:00:00	0	Wednesday Convocation 3	\N	8	25	140	1	\N	Background noise in parts. Recording ends about 26:00	\N	\N	\N	\N
753	local	00000779	2006-02-28 00:00:00	2006-02-28 00:00:00	0	Anderson, Gordon	\N	8	25	140	1	\N	Interview ends at 15:64	\N	\N	\N	\N
754	local	00000780	2006-02-28 00:00:00	2006-02-28 00:00:00	0	Attles, Joe 1	\N	8	25	140	1	\N	Related files: 00000780-00000781	\N	\N	\N	\N
755	local	00000781	2006-02-28 00:00:00	2006-02-28 00:00:00	0	Attles, Joe 2	\N	8	25	140	1	\N	Interview ends at 9:38, Related files: 00000780-00000781	\N	\N	\N	\N
756	local	00000782	2006-02-28 00:00:00	2006-02-28 00:00:00	0	Attles, Joe/Bricktop 1	\N	8	25	140	1	\N	Interview ends at 18:58,  Related files: 00000782-00000783	\N	\N	\N	\N
757	local	00000783	2006-02-28 00:00:00	2006-02-28 00:00:00	0	Attles, Joe/Bricktop 2	\N	8	25	140	1	\N	Interview ends at 18:43,  Related files: 00000782-00000783	\N	\N	\N	\N
758	local	00000784	2006-02-28 00:00:00	2006-02-28 00:00:00	0	Attlas, Joe	\N	8	25	140	1	\N	Interview ends at 19:35, TV noise in background	\N	\N	\N	\N
759	local	00000785	2006-02-28 00:00:00	2006-02-28 00:00:00	0	\N	\N	8	25	140	1	\N	\N	\N	\N	\N	\N
760	local	00000786	2006-02-28 00:00:00	2006-02-28 00:00:00	0	\N	\N	8	25	140	1	\N	\N	\N	\N	\N	\N
761	local	00000787	2006-02-28 00:00:00	2006-02-28 00:00:00	0	\N	\N	8	25	140	1	\N	\N	\N	\N	\N	\N
762	local	00000788	2006-02-28 00:00:00	2006-02-28 00:00:00	0	\N	\N	8	25	140	1	\N	\N	\N	\N	\N	\N
763	local	00000789	2006-02-28 00:00:00	2006-02-28 00:00:00	0	\N	\N	8	25	140	1	\N	\N	\N	\N	\N	\N
764	local	00000790	2006-02-28 00:00:00	2006-02-28 00:00:00	0	\N	\N	8	25	140	1	\N	\N	\N	\N	\N	\N
765	local	00000791	2006-02-28 00:00:00	2006-02-28 00:00:00	0	\N	\N	8	25	140	1	\N	\N	\N	\N	\N	\N
766	local	00000792	2006-02-28 00:00:00	2006-02-28 00:00:00	0	\N	\N	8	25	140	1	\N	\N	\N	\N	\N	\N
767	local	00000793	2006-02-28 00:00:00	2006-02-28 00:00:00	0	The Waste Land/and Other Poems read by T.S. Eliot: The Waste Land (complete)	\N	8	25	140	1	\N	Caedmon Records Inc. TC 1326	\N	\N	\N	\N
768	local	00000794	2006-02-28 00:00:00	2006-02-28 00:00:00	0	The Waste Land/and Other Poems read by T.S. Eliot: The Hollow Men	\N	8	25	140	1	\N	Caedmon Records Inc. TC 1326	\N	\N	\N	\N
769	local	00000795	2006-02-28 00:00:00	2006-02-28 00:00:00	0	The Waste Land/and Other Poems read by T.S. Eliot: Journey of the Magi from the Ariel Poems	\N	8	25	140	1	\N	Caedmon Records Inc. TC 1326	\N	\N	\N	\N
770	local	00000796	2006-02-28 00:00:00	2006-02-28 00:00:00	0	The Waste Land/and Other Poems read by T.S. Eliot: La Figlia che Piange	\N	8	25	140	1	\N	Caedmon Records Inc. TC 1326	\N	\N	\N	\N
771	local	00000797	2006-02-28 00:00:00	2006-02-28 00:00:00	0	The Waste Land/and Other Poems read by T.S. Eliot: Landscapes: New Hampshire, Virginia, Usk, Rannoch by Glencoe, Cape Ann	\N	8	25	140	1	\N	Caedmon Records Inc. TC 1326	\N	\N	\N	\N
772	local	00000798	2006-02-28 00:00:00	2006-02-28 00:00:00	0	The Waste Land/and Other Poems read by T.S. Eliot: Morning at the Window	\N	8	25	140	1	\N	Caedmon Records Inc. TC 1326	\N	\N	\N	\N
773	local	00000799	2006-02-28 00:00:00	2006-02-28 00:00:00	0	The Waste Land/and Other Poems read by T.S. Eliot: Difficulties of a Statesman from Coriolan	\N	8	25	140	1	\N	Caedmon Records Inc. TC 1326	\N	\N	\N	\N
774	local	00000800	2006-02-28 00:00:00	2006-02-28 00:00:00	0	The Waste Land/and Other Poems read by T.S. Eliot: Sweeney Among Nightingales	\N	8	25	140	1	\N	Caedmon Records Inc. TC 1326	\N	\N	\N	\N
775	local	00000801	2006-02-28 00:00:00	2006-02-28 00:00:00	0	The Waste Land/and Other Poems read by T.S. Eliot: Whispers of Immortality	\N	8	25	140	1	\N	Caedmon Records Inc. TC 1326. Live recording courtesy of radio station WFMT, Chicago.	\N	\N	\N	\N
776	local	00000802	2006-02-28 00:00:00	2006-02-28 00:00:00	0	The Waste Land/and Other Poems read by T.S. Eliot: Macavity the Mystery Cat	\N	8	25	140	1	\N	Caedmon Records Inc. TC 1326. Live recording courtesy of radio station WFMT, Chicago.	\N	\N	\N	\N
777	local	00000803	2006-02-28 00:00:00	2006-02-28 00:00:00	0	T.S. Eliot reads his Four Quartets: Burnt Norton	\N	8	25	140	1	\N	Angel Records 45012. Recorded under the Auspices of the British Council	\N	\N	\N	\N
778	local	00000804	2006-02-28 00:00:00	2006-02-28 00:00:00	0	T.S. Eliot reads his Four Quartets: East Coker	\N	8	25	140	1	\N	Angel Records 45012. Recorded under the Auspices of the British Council	\N	\N	\N	\N
779	local	00000805	2006-02-28 00:00:00	2006-02-28 00:00:00	0	T.S. Eliot reads his Four Quartets: The Dry Salvages	\N	8	25	140	1	\N	Angel Records 45012. Recorded under the Auspices of the British Council	\N	\N	\N	\N
780	local	00000806	2006-02-28 00:00:00	2006-02-28 00:00:00	0	T.S. Eliot reads his Four Quartets: Little Gidding	\N	8	25	140	1	\N	Angel Records 45012. Recorded under the Auspices of the British Council	\N	\N	\N	\N
781	local	00000807	2006-02-28 00:00:00	2006-02-28 00:00:00	0	William Carlos Williams Reading His Poems: The Decent	\N	8	25	140	1	\N	Caedmon Records Inc. TC 1047. Recorded at the Poet's home.	\N	\N	\N	\N
782	local	00000808	2006-02-28 00:00:00	2006-02-28 00:00:00	0	William Carlos Williams Reading His Poems: To Daphne and Virginia	\N	8	25	140	1	\N	Caedmon Records Inc. TC 1047. Recorded at the Poet's home.	\N	\N	\N	\N
783	local	00000809	2006-02-28 00:00:00	2006-02-28 00:00:00	0	William Carlos Williams Reading His Poems: The Orchestra	\N	8	25	140	1	\N	Caedmon Records Inc. TC 1047. Recorded at the Poet's home.	\N	\N	\N	\N
784	local	00000810	2006-02-28 00:00:00	2006-02-28 00:00:00	0	William Carlos Williams Reading His Poems: For Eleanor and Bill Monahan	\N	8	25	140	1	\N	Caedmon Records Inc. TC 1047. Recorded at the Poet's home.	\N	\N	\N	\N
785	local	00000811	2006-02-28 00:00:00	2006-02-28 00:00:00	0	William Carlos Williams Reading His Poems: The Yellow Flower	\N	8	25	140	1	\N	Caedmon Records Inc. TC 1047. Recorded at the Poet's home.	\N	\N	\N	\N
786	local	00000812	2006-02-28 00:00:00	2006-02-28 00:00:00	0	William Carlos Williams Reading His Poems: The Host	\N	8	25	140	1	\N	Caedmon Records Inc. TC 1047. Recorded at the Poet's home.	\N	\N	\N	\N
787	local	00000813	2006-02-28 00:00:00	2006-02-28 00:00:00	0	William Carlos Williams Reading His Poems: Work in Progress, section	\N	8	25	140	1	\N	Caedmon Records Inc. TC 1047. Recorded at the Poet's home.	\N	\N	\N	\N
788	local	00000814	2006-02-28 00:00:00	2006-02-28 00:00:00	0	William Carlos Williams Reading His Poems: The Botticellian Trees	\N	8	25	140	1	\N	Caedmon Records Inc. TC 1047. Recorded at the Poet's home.	\N	\N	\N	\N
789	local	00000815	2006-02-28 00:00:00	2006-02-28 00:00:00	0	William Carlos Williams Reading His Poems: Flowers by the Sea	\N	8	25	140	1	\N	Caedmon Records Inc. TC 1047. Recorded at the Poet's home.	\N	\N	\N	\N
790	local	00000816	2006-02-28 00:00:00	2006-02-28 00:00:00	0	William Carlos Williams Reading His Poems: The Yatchts	\N	8	25	140	1	\N	Caedmon Records Inc. TC 1047. Recorded at the Poet's home.	\N	\N	\N	\N
791	local	00000817	2006-02-28 00:00:00	2006-02-28 00:00:00	0	William Carlos Williams Reading His Poems: The Catholic Bells	\N	8	25	140	1	\N	Caedmon Records Inc. TC 1047. Recorded at the Poet's home.	\N	\N	\N	\N
792	local	00000818	2006-02-28 00:00:00	2006-02-28 00:00:00	0	William Carlos Williams Reading His Poems: Smell!	\N	8	25	140	1	\N	Caedmon Records Inc. TC 1047. Recorded at the Poet's home.	\N	\N	\N	\N
793	local	00000819	2006-02-28 00:00:00	2006-02-28 00:00:00	0	William Carlos Williams Reading His Poems: Fish	\N	8	25	140	1	\N	Caedmon Records Inc. TC 1047. Recorded at the Poet's home.	\N	\N	\N	\N
794	local	00000820	2006-02-28 00:00:00	2006-02-28 00:00:00	0	William Carlos Williams Reading His Poems: Primrose	\N	8	25	140	1	\N	Caedmon Records Inc. TC 1047. Recorded at the Poet's home.	\N	\N	\N	\N
795	local	00000821	2006-02-28 00:00:00	2006-02-28 00:00:00	0	William Carlos Williams Reading His Poems: To Elsie	\N	8	25	140	1	\N	Caedmon Records Inc. TC 1047. Recorded at the Poet's home.	\N	\N	\N	\N
796	local	00000822	2006-02-28 00:00:00	2006-02-28 00:00:00	0	William Carlos Williams Reading His Poems: Between Walls	\N	8	25	140	1	\N	Caedmon Records Inc. TC 1047. Recorded at the Poet's home.	\N	\N	\N	\N
797	local	00000823	2006-02-28 00:00:00	2006-02-28 00:00:00	0	William Carlos Williams Reading His Poems: On Gay Wallpaper	\N	8	25	140	1	\N	Caedmon Records Inc. TC 1047. Recorded at the Poet's home.	\N	\N	\N	\N
798	local	00000824	2006-02-28 00:00:00	2006-02-28 00:00:00	0	William Carlos Williams Reading His Poems: The Red Lily	\N	8	25	140	1	\N	Caedmon Records Inc. TC 1047. Recorded at the Poet's home.	\N	\N	\N	\N
799	local	00000825	2006-02-28 00:00:00	2006-02-28 00:00:00	0	\N	\N	8	25	140	1	\N	\N	\N	\N	\N	\N
800	local	00000826	2006-02-28 00:00:00	2006-02-28 00:00:00	0	\N	\N	8	25	140	1	\N	\N	\N	\N	\N	\N
801	local	00000827	2006-02-28 00:00:00	2006-02-28 00:00:00	0	\N	\N	8	25	140	1	\N	\N	\N	\N	\N	\N
802	local	00000828	2006-02-28 00:00:00	2006-02-28 00:00:00	0	\N	\N	8	25	140	1	\N	\N	\N	\N	\N	\N
803	local	00000829	2006-02-28 00:00:00	2006-02-28 00:00:00	0	\N	\N	8	25	140	1	\N	\N	\N	\N	\N	\N
804	local	00000830	2006-02-28 00:00:00	2006-02-28 00:00:00	0	\N	\N	8	25	140	1	\N	\N	\N	\N	\N	\N
805	local	00000831	2006-02-28 00:00:00	2006-02-28 00:00:00	0	\N	\N	8	25	140	1	\N	\N	\N	\N	\N	\N
806	local	00000832	2006-02-28 00:00:00	2006-02-28 00:00:00	0	\N	\N	8	25	140	1	\N	\N	\N	\N	\N	\N
807	local	00000833	2006-02-28 00:00:00	2006-02-28 00:00:00	0	\N	\N	8	25	140	1	\N	\N	\N	\N	\N	\N
808	local	00000834	2006-02-28 00:00:00	2006-02-28 00:00:00	0	\N	\N	8	25	140	1	\N	\N	\N	\N	\N	\N
809	local	00000835	2006-02-28 00:00:00	2006-02-28 00:00:00	0	Pleasure Dome An Audible Anthology of Modern Poetry Read by Its Creators and Edited by Lloyd Frankenberg: T.S. Eliot	\N	8	25	140	1	\N	Poem Titles: A Game of Chess. Columbia Masterworks ML 4259.	\N	\N	\N	\N
810	local	00000836	2006-02-28 00:00:00	2006-02-28 00:00:00	0	Pleasure Dome An Audible Anthology of Modern Poetry Read by Its Creators and Edited by Lloyd Frankenberg: Marianne Moore	\N	8	25	140	1	\N	Poem Titles: In Distrust of Merits. Columbia Masterworks ML 4259.	\N	\N	\N	\N
811	local	00000837	2006-02-28 00:00:00	2006-02-28 00:00:00	0	Pleasure Dome An Audible Anthology of Modern Poetry Read by Its Creators and Edited by Lloyd Frankenberg: E.E. Cummings	\N	8	25	140	1	\N	Poem Titles: Spring is Like a Perhaps Hand, This Bride and Groom, Pity This Busy Monster, Manunkind, Rain or Hail. Columbia Masterworks ML 4259.	\N	\N	\N	\N
812	local	00000838	2006-02-28 00:00:00	2006-02-28 00:00:00	0	Pleasure Dome An Audible Anthology of Modern Poetry Read by Its Creators and Edited by Lloyd Frankenberg: William Carlos Williams	\N	8	25	140	1	\N	Poem Titles: The Young Housewife, The Bull, Poem, Lear, The Dance, El Hombre. Columbia Masterworks ML 4259.	\N	\N	\N	\N
813	local	00000839	2006-02-28 00:00:00	2006-02-28 00:00:00	0	Pleasure Dome An Audible Anthology of Modern Poetry Read by Its Creators and Edited by Lloyd Frankenberg:  Ogden Nash	\N	8	25	140	1	\N	Poem Titles: Allow Me Madam but It Won't Help, The Hunter, The Perfect Husband, The Outcome of Mr. McLeod's Gratitude, Introspective Reflection, So Penseroso. Columbia Masterworks ML 4259.	\N	\N	\N	\N
814	local	00000840	2006-02-28 00:00:00	2006-02-28 00:00:00	0	Pleasure Dome An Audible Anthology of Modern Poetry Read by Its Creators and Edited by Lloyd Frankenberg: W.H. Auden	\N	8	25	140	1	\N	Poem Titles: Ballad, Prime. Columbia Masterworks ML 4259.	\N	\N	\N	\N
815	local	00000841	2006-02-28 00:00:00	2006-02-28 00:00:00	0	Pleasure Dome An Audible Anthology of Modern Poetry Read by Its Creators and Edited by Lloyd Frankenberg: Dylan Thomas	\N	8	25	140	1	\N	Poem Titles: Poem in October, In My Craft or Sullen Art . Columbia Masterworks ML 4259.	\N	\N	\N	\N
816	local	00000842	2006-02-28 00:00:00	2006-02-28 00:00:00	0	Pleasure Dome An Audible Anthology of Modern Poetry Read by Its Creators and Edited by Lloyd Frankenberg: Elizabeth Bishop	\N	8	25	140	1	\N	Poem Titles: Anaphora, Late Air, The Fish. Columbia Masterworks ML 4259.	\N	\N	\N	\N
817	local	00000843	2006-02-28 00:00:00	2006-02-28 00:00:00	0	\N	\N	8	25	140	1	\N	\N	\N	\N	\N	\N
818	local	00000844	2006-02-28 00:00:00	2006-02-28 00:00:00	0	\N	\N	8	25	140	1	\N	\N	\N	\N	\N	\N
819	local	00000845	2006-02-28 00:00:00	2006-02-28 00:00:00	0	\N	\N	8	25	140	1	\N	\N	\N	\N	\N	\N
820	local	\N	2006-05-12 00:00:00	2006-05-12 00:00:00	6	test	\N	6	25	140	1	\N	\N	\N	\N	\N	\N
821	local	00000021	2006-02-28 00:00:00	2006-02-28 00:00:00	830	North Carolina Festival Chorus, Greenboro, North Carolina	\N	8	247	\N	1	\N	WLD Conducting	\N	\N	\N	\N
822	local	\N	2006-05-14 00:00:00	\N	954	Crowell Gardens. [postcard]	One of many beautiful gardens in Augusta, Georgia.	1	247	140	1	The postcard is a drawing or painting of a fountain and series of topiary arch in the gardens.	\N	The postcard was mailed to Dr. and Mrs. Ross H. McLeau (Department of History, Emory University) on April 16, 1942.	\N	\N	\N
823	local	Fragile Pictures	2006-05-14 00:00:00	2006-05-16 00:00:00	\N	African American Fireman, Savannah, Georgia	\N	9	25	140	1	Daguerrotype of an African American fireman in uniform.	\N	Hand-tinted daguerrotype of an African American firefighter.	\N	\N	\N
1020	local	1020	2006-05-18 00:00:00	2006-05-18 00:00:00	2	\N	\N	6	247	140	1	\N	\N	\N	\N	\N	\N
1021	local	\N	2006-05-19 00:00:00	2006-05-19 00:00:00	0	\N	\N	6	247	140	1	\N	\N	\N	\N	\N	\N
1022	local	\N	2006-05-19 00:00:00	2006-05-19 00:00:00	0	\N	\N	6	247	140	1	\N	\N	\N	\N	\N	\N
1023	local	\N	2006-05-19 00:00:00	2006-05-19 00:00:00	89	\N	\N	6	247	140	1	\N	\N	\N	\N	\N	\N
1024	local	\N	2006-05-23 00:00:00	2006-05-23 00:00:00	0	test	\N	6	247	140	1	\N	\N	\N	\N	\N	\N
1026	local	\N	2006-05-24 00:00:00	2006-05-24 00:00:00	0	\N	\N	6	247	140	1	\N	\N	\N	\N	\N	\N
1027	local	0644-001	2006-06-06 00:00:00	\N	584	Sylvia Plath, Frieda, and Nicholas among the daffodils at Court Green, April 1962	\N	9	25	140	1	This color photograph was taken by the Swedish photographer Siv Arb when she visited Court Green in April 1962 to interview Hughes for a piece she was writing for a Swedish magazine, Rondo.	\N	\N	\N	\N	\N
1028	local	0644-002	2006-06-06 00:00:00	\N	584	Ted Hughes at Court Green (indoors), ca. 1970s	\N	9	25	140	1	Ted Hughes seated by a window in his home at Court Green.  The photograph was taken by his wife, Carol Hughes.	\N	\N	\N	\N	\N
1029	local	0644-003	2006-06-06 00:00:00	\N	584	Ted Hughes on board an ocean liner, ca. August 1959	\N	6	25	140	1	Ted Hughes stands with his arms crossed on the deck of an ocean liner ca. August 1959.  The photograph was taken by his wife, Sylvia Plath.	\N	\N	\N	\N	\N
1030	local	0644-004	2006-06-06 00:00:00	\N	584	Sylvia Plath on board an ocean liner	\N	6	25	140	1	Sylvia Plath stands with her hand on her hip on the deck of an ocean liner ca. August 1959.  The photograph was taken by her husband, Ted Hughes.	\N	\N	\N	\N	\N
1031	local	0644-005	2006-06-06 00:00:00	\N	584	Ted Hughes and Sylvia Plath seated with two unidentified men aboard the SS United States, 1959	\N	9	25	140	1	Ted Hughes and Sylvia Plath are seated side-by-side at a table in the dining area.  Two unidentified men are seated across from them.  Other The room is decorated for a party.	\N	\N	\N	\N	\N
1032	local	0854-001.tif	2006-06-06 00:00:00	\N	789	Ted Hughes Cambridge University ca. 1950-1954	\N	9	25	140	1	school (graduation) photo	\N	\N	\N	\N	\N
1033	local	0644-006	2006-06-07 00:00:00	\N	584	Page 16 of a notebook of poem drafts by Ted Hughes, [ca. 1949-1966]	\N	1	25	140	1	The page contains handwritten poem drafts, including "Against Larks."	\N	\N	\N	\N	\N
1038	local	0644-005.tif	2006-06-08 00:00:00	\N	584	Sylvia Plath and Ted Hughes seated with unidentified men on the SS United States, December 1959	\N	9	25	140	1	Sylvia's caption reads: "The Gala Banquet on the ungallant SS United States: December '59 Return to Europe, a pooker on the way after autumn at Yaddo."	\N	\N	\N	\N	\N
1039	local	0644-010.tif	2006-06-08 00:00:00	\N	584	Poem Draft by Ted Hughes, Notebook 8, p. 55.	\N	1	25	140	1	From Notebook 8, Challenge Duplicate Book, n.d., [ca. 1965-1966], ca. 200 pp.  Multiple titled and untitled drafts of published and unpublished poems	\N	\N	\N	\N	\N
1040	local	0644-007.tif	2006-06-09 00:00:00	\N	584	Poem Draft by Ted Hughes, Notebook 1, p. 32.	\N	1	247	140	1	From Notebook 1: Notebook (torn in half), n.d., [ca. 1949-1966], 62 pp.  Multiple untitled manuscript drafts including an untitled short story ("The address to the public...,") followed by "A dreamed story: August 19th."  Verso of notebook pages contain multiple poem drafts including "Against Larks," "The Black Oak," "Ode to Indolence," "The Fallen Violin," and A Wind Flashes the Grass."	\N	\N	\N	\N	\N
1041	local	0644-008.tif	2006-06-09 00:00:00	\N	584	Poem Draft by Ted Hughes, Notebook 8, p. 52.	\N	1	25	140	1	From Notebook 8, Challenge Duplicate Book, n.d., [ca. 1965-1966], ca. 200 pp.  Multiple titled and untitled drafts of published and unpublished poems	\N	\N	\N	\N	\N
1042	local	0644-009.tif	2006-06-09 00:00:00	\N	584	Poem Draft by Ted Hughes, Notebook 8, p. 53.	\N	1	25	140	1	From Notebook 8, Challenge Duplicate Book, n.d., [ca. 1965-1966], ca. 200 pp.  Multiple titled and untitled drafts of published and unpublished poems	\N	\N	\N	\N	\N
1043	local	0644-011.tif	2006-06-09 00:00:00	\N	584	Poem Draft by Ted Hughes, Notebook 8, p. 64.	\N	1	25	140	1	From Notebook 8, Challenge Duplicate Book, n.d., [ca. 1965-1966], ca. 200 pp.  Multiple titled and untitled drafts of published and unpublished poems.	\N	\N	\N	\N	\N
1044	local	0644#############002001.TIF	2006-06-09 00:00:00	\N	584	Ted Hughes and Sylvia Plath in their Boston Apartment, 1958.	\N	9	25	140	1	Photo points to the period when Hughes and Plath lived in Boston, studying and working in the same small apartment.	\N	\N	\N	\N	\N
1045	local	0644#############003001.TIF	2006-06-09 00:00:00	\N	584	"A Pride of Poets"	Stephen Spender, W.H. Auden, Ted Hughes, T.S. Eliot, and Louis MacNeice at Faber and Faber cocktail party honoring W. H. Auden, 23 June 1960.	9	25	140	1	Taken four months before the publication of Plath's first book of poetry.	\N	\N	\N	\N	\N
1046	local	0644#############004001.TIF	2006-06-09 00:00:00	\N	584	Sylvia Plath, at the Grand Canyon?, 1959	\N	9	25	140	1	Ted and Sylvia spent time camping across the United States in the summer of 1959.	\N	\N	\N	\N	\N
1034	local	\N	2006-06-07 00:00:00	\N	826	Speech by William Levi Dawson to the American Choral Directors convention, undated	\N	1	247	140	1	\N	\N	This is page 1 of 4.	\N	\N	\N
1073	local	\N	2006-06-09 00:00:00	\N	826	Program for the Alabama Music Hall of Fame Induction Banquet and Awards Show, 26 January 1989	\N	1	247	140	1	William Levi Dawson was one of the inductees.	\N	Only the cover and page 20 were scanned.  This is the cover.	\N	\N	\N
1074	local	\N	2006-06-09 00:00:00	\N	826	Program for the Alabama Music Hall of Fame Induction Banquet and Awards Show, 26 January 1989	\N	1	247	\N	1	William Levi Dawson was one of the inductees.  This page includes Dawson's biography.	\N	Only the cover and page 20 were scanned.  This is page 20.	\N	\N	\N
1082	local	\N	2006-06-09 00:00:00	\N	826	Letter from William Levi Dawson to Robert Shaw, 20 April 1985	\N	1	247	\N	1	The letter concerns a planned performance of the Negro Folk Symphony by the Atlanta Symphony Orchestra in 1985.	\N	\N	\N	\N	\N
1087	local	0644#############005001.TIF	2006-06-12 00:00:00	\N	584	Ted Hughes and Craig Raine, ca. 1980s	\N	9	25	140	1	Ted Hughes with English poet and critic Craig Raine. Raine worked as poetry editor at Faber and Faber beginning in 1981.	\N	\N	\N	\N	\N
1088	local	0644#############006001.TIF	2006-06-12 00:00:00	\N	584	Ted & Carol Hughes, ca. 1970s.	\N	9	25	140	1	\N	\N	\N	\N	\N	\N
1089	local	0644#############007001.TIF	2006-06-12 00:00:00	\N	584	Plath, Sylvia, U.S. Passport, 1959.	\N	9	25	140	1	During this period Hughes lived with Sylvia Plath in the United States  where he taught at the University of Massachusetts and she at Smith College.	\N	\N	\N	\N	\N
1090	local	0644#############008001.TIF	2006-06-12 00:00:00	\N	584	Hughes, Ted, Permit to exit and re-enter U.S., 1959	\N	13	25	140	1	During this period Hughes lived with Sylvia Plath in the United States  where he taught at the University of Massachusetts and she at Smith College.	\N	\N	\N	\N	\N
1091	local	0644#############009001.TIF	2006-06-12 00:00:00	\N	584	Ted Hughes, Sylvia Plath & Ted Hughes's Parents, 1956.	\N	9	25	140	1	Photograph was taken the year of Ted and Sylvia's marriage, June 16th, 1956. They were married in a small service at the church of St. George the Martyr in London.	\N	\N	\N	\N	\N
1092	local	0644#############010001.TIF	2006-06-12 00:00:00	\N	584	Ted Hughes and Sylvia Plath, ca. 1961-1962.	\N	9	25	140	1	Photograph likely taken in England following Plath and Hughes's departure from the United States around the time of the birth of their first child.	\N	\N	\N	\N	\N
1093	local	0644#############011001.TIF	2006-06-12 00:00:00	\N	584	Ted Hughes, Sylvia Plath & Ted Hughes's Parents, 1956.	\N	9	25	140	1	Photograph was taken the year of Ted and Sylvia's marriage, June 16th, 1956. They were married in a small service at the church of St. George the Martyr in London.	\N	\N	\N	\N	\N
1094	local	0644#############012001.TIF	2006-06-12 00:00:00	\N	584	Ted Hughes, ca. 1960s	\N	9	25	140	1	\N	\N	\N	\N	\N	\N
1095	local	0644#############014001.TIF	2006-06-12 00:00:00	\N	584	\N	\N	1	25	140	1	\N	\N	\N	\N	\N	\N
1096	local	0644#############015001.TIF	2006-06-12 00:00:00	\N	584	Ted Hughes, Derek Walcott & Seamus Heaney, 1993.	\N	9	25	140	1	Hughes with Nobel prize winners Derek Walcott & Seamus Heaney.	\N	\N	\N	\N	\N
1097	local	0644#############016001.TIF	2006-06-12 00:00:00	\N	584	Ted Hughes, by Jane Bown (Faber & Faber), ca. 1990's.	\N	9	25	140	1	\N	\N	\N	\N	\N	\N
1098	local	0644#############017001.TIF	2006-06-12 00:00:00	\N	584	Ted Hughes with Fish, ca. 1980's.	\N	9	25	140	1	Hughes was an avid fisherman for most of his life.	\N	\N	\N	\N	\N
1099	local	AssiaWevillBox176F40-2.tif	2006-06-12 00:00:00	\N	584	Wevill, Assia, William Trevor, Jane Donaldson, Sean Gallagher on the Serpentine, ca. 1960	\N	9	25	140	1	Hughes began seeing the artist Assia Wevill during the fall of 1962 while he and Sylvia Plath were still married.	\N	\N	\N	\N	\N
1100	local	AssiaWevillBox176F40.tif	2006-06-12 00:00:00	\N	584	Assia Wevill and others, ca. 1960.	\N	9	25	140	1	Hughes began seeing the artist Assia Wevill during the fall of 1962 while he and Sylvia Plath were still married.	\N	\N	\N	\N	\N
1101	local	GeraldOlwynTed1946.tif	2006-06-12 00:00:00	\N	584	Gerald, Olwyn, and Ted Hughes, 1946.	\N	9	25	140	1	Ted with brother Gerald and sister Olwyn.	\N	\N	\N	\N	\N
1102	local	HeaneyHughesFence.tif	2006-06-13 00:00:00	\N	584	Ted Hughes and Seamus Heaney with roll of fencing, ca. 1980s.	\N	9	25	140	1	Hughes collaborated with Heaney on various projects during the 1980s.	\N	\N	\N	\N	\N
1103	local	hughes-01.tif	2006-06-13 00:00:00	\N	584	"Fighting for Jerusalem," 1970.	\N	1	25	140	1	Graphics, ron brown; MidNAG poetry poster No. 7.	\N	\N	\N	\N	\N
1104	local	hughes-02.tif	2006-06-13 00:00:00	\N	584	"King of Carrion," 1978.	\N	1	25	140	1	Edition 4/20. Poem taken from Crow: From the Life and Songs of the Crow (1970) and printed in 1978.	\N	\N	\N	\N	\N
1105	local	hughes-03.tif	2006-06-13 00:00:00	\N	584	"That Moment," 1970.	\N	1	25	140	1	Edition 18/20.  Poem taken from Crow: From the Life and Songs of the Crow (1970).	\N	\N	\N	\N	\N
1106	local	\N	2006-06-13 00:00:00	\N	\N	Image of Courthouse and YMCA	From "Recent Architecture in Atlanta," Harper's Weekly vol XXXIII no. 1702.	1	25	140	1	\N	\N	\N	\N	\N	\N
1107	local	hughes-04.tif	2006-06-13 00:00:00	\N	584	"Crow and the Birds," 1979.	\N	1	25	140	1	Edition 18/20.  Poem taken from Crow: From the Life and Songs of the Crow (1970).	\N	\N	\N	\N	\N
1108	local	hughes-06.tif	2006-06-13 00:00:00	\N	584	"Crow's Last Stand," 1970.	\N	1	25	140	1	Edition 17/20.  Poem taken from Crow: From the Life and Songs of the Crow (1970).	\N	\N	\N	\N	\N
1109	local	hughes-08.tif	2006-06-13 00:00:00	\N	584	"In the black chapel," 1979.	\N	1	25	140	1	Published on the occasion of the exhibition "Illustrations to Ted Hughes Poems" at the Victoria andd Albert Museum.	\N	\N	\N	\N	\N
1110	local	hughes-10.tif	2006-06-13 00:00:00	\N	584	"Enfolds you" (?)	\N	1	25	140	1	\N	\N	\N	\N	\N	\N
1113	local	\N	2006-06-13 00:00:00	\N	826	Program from Lincoln University's Commencement Exercises, 7 May  1978	\N	1	247	\N	1	William Levi Dawson received an Honorary Doctorate at this ceremony.	\N	The cover and four pages were scanned.  This is the cover.	\N	\N	\N
1083	local	\N	2006-06-09 00:00:00	\N	826	Draft program (typescript) for the Robert W. Woodruff Memorial Concert, Atlanta Symphony Orchestra and Chorus, 9 May 1985	\N	1	247	\N	1	Robert Shaw is listed as the conductor.	\N	\N	\N	\N	\N
1116	local	\N	2006-06-13 00:00:00	\N	826	Biography of William Levi Dawson written for the commencement ceremony at Lincoln University, 7 May 1978	\N	1	247	\N	1	Dawson received an honorary doctorate from Lincoln University that year.  The biography is typed on stationary from the Office of the President.	\N	This is page 1 of 2.	\N	\N	\N
1117	local	\N	2006-06-13 00:00:00	\N	826	Biography of William Levi Dawson written for the commencement ceremony at Lincoln University, 7 May 1978	\N	1	247	\N	1	Dawson received an honorary doctorate from Lincoln University that year.  The biography is typed on stationary from the Office of the President.	\N	This is page 2 of 2.	\N	\N	\N
1119	local	\N	2006-06-13 00:00:00	\N	826	Lincoln University Bulletin (Summer 1978)	Alumni publication of Lincoln University	1	247	\N	1	This issue covered commencement.  Photographs of the honorary degree recipients are printed on the cover, including William Levi Dawson.	\N	Only the cover was scanned.	\N	\N	\N
1121	local	\N	2006-06-13 00:00:00	\N	826	Program for the Louisiana Music Educators Association's 1984 Louisiana All-State Concerts, (Northwestern State University, Natchitoches, Louisiana,) 19-20 November 1984	\N	1	247	\N	1	\N	\N	The entire program was scanned.  These are pages [1-2].	\N	\N	\N
1122	local	\N	2006-06-13 00:00:00	\N	826	Program for the Louisiana Music Educators Association's 1984 Louisiana All-State Concerts, (Northwestern State University, Natchitoches, Louisiana,) 19-20 November 1984	\N	1	247	\N	1	\N	\N	The entire program was scanned.  These are pages [3-4].	\N	\N	\N
1123	local	\N	2006-06-13 00:00:00	\N	826	Program for the Louisiana Music Educators Association's 1984 Louisiana All-State Concerts, (Northwestern State University, Natchitoches, Louisiana,) 19-20 November 1984	\N	1	247	\N	1	\N	\N	The entire program was scanned.  These are pages [5-6].	\N	\N	\N
1124	local	\N	2006-06-13 00:00:00	\N	826	Program for the Louisiana Music Educators Association's 1984 Louisiana All-State Concerts, (Northwestern State University, Natchitoches, Louisiana,) 19-20 November 1984	\N	1	247	\N	1	\N	\N	The entire program was scanned.  These are pages [7-8].	\N	\N	\N
1125	local	\N	2006-06-13 00:00:00	\N	826	Program for the Louisiana Music Educators Association's 1984 Louisiana All-State Concerts, (Northwestern State University, Natchitoches, Louisiana,) 19-20 November 1984	\N	1	247	\N	1	\N	\N	The entire program was scanned.  These are pages [9-10].	\N	\N	\N
1126	local	\N	2006-06-13 00:00:00	\N	826	Program for the Louisiana Music Educators Association's 1984 Louisiana All-State Concerts, (Northwestern State University, Natchitoches, Louisiana,) 19-20 November 1984	\N	1	247	\N	1	\N	\N	The entire program was scanned.  This is the back cover.	\N	\N	\N
1127	local	\N	2006-06-13 00:00:00	\N	826	List of music for the 1984 Louisiana All-State Choir submitted to  Tom Nix by William Levi Dawson	\N	1	247	\N	1	\N	\N	\N	\N	\N	\N
1136	local	\N	2006-06-13 00:00:00	\N	826	Letter from the Music Educators National Conference, Eastern Division, to William Levi Dawson, 7 May 1960	\N	1	247	\N	1	The letter was written by Maurice C. Whitney, President, MENC Eastern Division.  It invites Dawson to serve as conductor for the All-Eastern Chorus, Band and Orchestra at the 1961 Eastern Conference of the MENC in Washington, DC.	\N	\N	\N	\N	\N
1144	local	\N	2006-06-14 00:00:00	\N	857	Joe Attles 2	\N	14	25	140	1	\N	\N	\N	\N	\N	\N
1145	local	000000939	2006-06-14 00:00:00	2006-06-14 00:00:00	857	Joe Attles 2	\N	14	247	140	1	\N	Interview ends at 18:47. Related files 00000938-00000939	\N	\N	\N	\N
1146	local	00000938	2006-06-14 00:00:00	2006-06-14 00:00:00	857	Attles, Joe 1	\N	6	247	140	1	\N	\N	\N	\N	\N	\N
1147	local	1147	2006-06-14 00:00:00	2006-06-14 00:00:00	857	\N	\N	6	247	140	1	\N	\N	\N	\N	\N	\N
1148	local	1148	2006-06-14 00:00:00	2006-06-14 00:00:00	857	\N	\N	6	247	140	1	\N	\N	\N	\N	\N	\N
1149	local	1149	2006-06-14 00:00:00	2006-06-14 00:00:00	857	\N	\N	6	247	140	1	\N	\N	\N	\N	\N	\N
1150	local	\N	2006-06-14 00:00:00	\N	481	Dorothy Tilly with President Truman's Civil Rights Committee, Press Association, Inc.	\N	9	25	140	1	Dorothy Tilly, a civil rights activist from Georgia, stands to the right of President Harry S. Truman (center) and his Committee on Civil Rights, to which she was appointed in 1946. Three years later Tilly founded the Fellowship of the Concerned, a biracial group dedicated to educating white southerners as a means of overcoming prejudice.	\N	\N	\N	\N	\N
1151	local	hughes-09.tif	2006-06-14 00:00:00	\N	584	"Has conquered. He has surrendered everything." (?)	\N	1	25	140	1	\N	\N	\N	\N	\N	\N
1152	local	hughes-11.tif	2006-06-14 00:00:00	\N	584	"Darkness has all come together, making an egg." (?)	\N	1	25	140	1	\N	\N	\N	\N	\N	\N
1153	local	hughes-12.tif	2006-06-14 00:00:00	\N	584	"A sphynx" (?).	\N	1	25	140	1	\N	\N	\N	\N	\N	\N
1154	local	hughes-13.tif	2006-06-14 00:00:00	\N	584	"Why are you afraid?" (?)	\N	1	25	140	1	\N	\N	\N	\N	\N	\N
1155	local	hughes-14.tif	2006-06-14 00:00:00	\N	584	"I meet you." (?)	\N	1	25	140	1	\N	\N	\N	\N	\N	\N
1156	local	hughes-15.tif	2006-06-14 00:00:00	\N	584	"The beautiful thing beckoned, big-haunched he loped." (?)	\N	1	25	140	1	\N	\N	\N	\N	\N	\N
1157	local	hughes-16.tif	2006-06-14 00:00:00	\N	584	"When everything that can fall has fallen." (?)	\N	1	25	140	1	\N	\N	\N	\N	\N	\N
1158	local	hughes-17.tif	2006-06-14 00:00:00	\N	584	"What is left is just what my life bought me:" (?)	\N	1	25	140	1	\N	\N	\N	\N	\N	\N
1159	local	hughes-18.tif	2006-06-14 00:00:00	\N	584	"Big terror decends." (?)	\N	1	25	140	1	\N	\N	\N	\N	\N	\N
1160	local	hughes-19.tif	2006-06-14 00:00:00	\N	584	"Bowled Over," 1967.	\N	1	25	140	1	From Wodwo (1967).	\N	\N	\N	\N	\N
1161	local	\N	2006-06-14 00:00:00	2006-06-14 00:00:00	857	Joe Attles	\N	6	247	140	1	\N	\N	\N	\N	\N	\N
1162	local	\N	2006-06-14 00:00:00	2006-06-14 00:00:00	857	Joe Attles	\N	6	247	140	1	\N	\N	\N	\N	\N	\N
1163	local	\N	2006-06-14 00:00:00	2006-06-14 00:00:00	857	Joe Attles	\N	6	247	140	1	\N	\N	\N	\N	\N	\N
1166	local	\N	2006-06-14 00:00:00	\N	826	Letter from William Lathon to William Levi Dawson, 2 March 1983	\N	1	247	\N	1	Lathon was Assistant to the Dean at the University of Louisville's School of Music.  The letter comments on Dawson's appearance at the Southern Division Music Educators National Conference.	\N	\N	\N	\N	\N
1178	local	\N	2006-06-14 00:00:00	\N	826	Letter from William Levi Dawson to Robert Small, 25 February 1946	\N	1	247	\N	1	From a subject file on Romilio Manduley O'Larson (Cuba), 1943-1946.  Only page 1 is present in the file.	\N	\N	\N	\N	\N
1190	local	\N	2006-06-14 00:00:00	\N	826	Letter from William Levi Dawson to the Program in Black American Culture, National Museum of American History, 12 November 1983	\N	1	247	\N	1	The letter is addressed to Bernice Johnson Reagon, Director, Program in Black American Culture.  It concerns Dawson's participation in the museum's Black History Month program "Spirituals: Black American Choral Song," in February 1984.	\N	\N	\N	\N	\N
1219	local	hughes-20.tif	2006-06-15 00:00:00	\N	584	"As Woman's Weeping," 1966.	\N	1	25	140	1	Poem From Recklings (1966).	\N	\N	\N	\N	\N
1220	local	hughes-21.tif	2006-06-15 00:00:00	\N	584	"Thistles," 1967.	\N	1	25	140	1	Poem from Wodwo (1967).	\N	\N	\N	\N	\N
1221	local	hughes-22.tif	2006-06-15 00:00:00	\N	584	"Still Life," 1967.	\N	1	25	140	1	Poem from Wodwo (1967).	\N	\N	\N	\N	\N
1222	local	hughes-23.tif	2006-06-15 00:00:00	\N	584	"Fern," 1967.	\N	1	25	140	1	Poem from Wodwo (1967).	\N	\N	\N	\N	\N
1223	local	hughes-24.tif	2006-06-15 00:00:00	\N	584	"Theology," 1967.	\N	1	25	140	1	from Wodwo (1967) and part of "Dully Gumption's College Courses" which includes "Semantics," "Political Science," "Theology," and "Humanities"	\N	\N	\N	\N	\N
1224	local	hughes-25.tif	2006-06-15 00:00:00	\N	584	"I said goodbye to earth,"	\N	1	25	140	1	From Gaudete, 1977. Edition 31/75	\N	\N	\N	\N	\N
1225	local	hughes laureate.tif	2006-06-15 00:00:00	\N	584	Ted and Carol Hughes with cask of Laureate's sherry, 1986	\N	9	25	140	1	In 1984 Ted Hughes was named Poet Laureate to the Queen, succeeding Sir John Betjeman	\N	\N	\N	\N	\N
1226	local	hughes portrait.tif	2006-06-15 00:00:00	\N	584	Ted Hughes, Beside Window, ca. 1970s	\N	1	25	140	1	\N	\N	\N	\N	\N	\N
1227	local	hughes-poem.tif	2006-06-15 00:00:00	\N	584	"Song of the Honeybee."	\N	1	25	140	1	from Rain-Charm for the Duchy (1992).	\N	\N	\N	\N	\N
1228	local	mother-covers-eyes.tif	2006-06-15 00:00:00	\N	584	"His mother covers her eyes," MS	\N	1	25	140	1	From Prometheus on the Crag (1973).	\N	\N	\N	\N	\N
1229	local	Notebook23pp32-33.tif	2006-06-15 00:00:00	\N	584	From Notebook 23	\N	1	25	140	1	[Notebook 23], Loose pages [from small black notebook], n.d., [ca. 1978-80], 26 leaves.  Includes titled and untitled drafts and mind-maps bird poems, most published in A Primer of Birds.	\N	\N	\N	\N	\N
1230	local	OP104-1.tif	2006-06-15 00:00:00	\N	584	"A Poet's Epitach," 1963.	\N	13	25	140	1	Newspaper clipping announcing the death of Sylvia Plath. From the Observer Weekend Review, February 17, 1963. Item housed in a spiral bound scrap book containing items from 1963-1968.	\N	\N	\N	\N	\N
1231	local	prometheus-crag.tif	2006-06-15 00:00:00	\N	584	"Prometheus…Relaxes," MS	\N	1	25	140	1	From Prometheus on the Crag (1973).	\N	\N	\N	\N	\N
1232	local	prometheus-cry.tif	2006-06-15 00:00:00	\N	584	"Prometheus…Heard the cry of the wombs," MS	\N	1	25	140	1	From Prometheus on the Crag (1973).	\N	\N	\N	\N	\N
1233	local	prometheus-dream-1.tif	2006-06-19 00:00:00	\N	584	"Prometheus…Tried to recall his night's dream," MS	\N	1	25	140	1	From Prometheus on the Crag (1973).	\N	\N	\N	\N	\N
1234	local	prometheus-dream-2.tif	2006-06-19 00:00:00	\N	584	"Prometheus…Tried to recall his night's dream," MS	\N	1	25	140	1	From Prometheus on the Crag (1973).	\N	\N	\N	\N	\N
1235	local	prometheus-relaxes.tif	2006-06-19 00:00:00	\N	584	"Prometheus…Relaxes,"	\N	1	25	140	1	From Prometheus on the Crag (1973).	\N	\N	\N	\N	\N
1236	local	\N	2006-06-19 00:00:00	2006-06-19 00:00:00	0	\N	\N	14	247	140	1	\N	\N	\N	\N	\N	\N
1237	local	prometheus-vulture-1.tif	2006-06-19 00:00:00	\N	584	"Prometheus…Pondered the vulture," MS	\N	1	25	140	1	From Prometheus on the Crag (1973).	\N	\N	\N	\N	\N
1242	local	prometheus-vulture-2.tif	2006-06-19 00:00:00	\N	584	"Prometheus…Pondered the vulture," MS	\N	1	25	140	1	From Prometheus on the Crag (1973).	\N	\N	\N	\N	\N
1243	local	SpenderLetterBack.tif	2006-06-19 00:00:00	\N	584	Reverse of letter from Stephen Spender to Mrs. Hughes, May 10th 1960.	\N	1	25	140	1	\N	\N	\N	\N	\N	\N
1244	local	SpenderLetterFront.tif	2006-06-19 00:00:00	\N	584	Front of letter from Stephen Spender to Mrs. Hughes, May 10th 1960.	\N	1	25	140	1	\N	\N	\N	\N	\N	\N
1245	local	Talesfrom OvidTereus.tif	2006-06-19 00:00:00	\N	584	"Tereus," MS	\N	1	25	140	1	From Tales from Ovid (1997)	\N	\N	\N	\N	\N
1246	local	Ted1960.tif	2006-06-19 00:00:00	\N	584	Ted Hughes, July 25, 1960, photographed by Hans Beacham.	\N	9	25	140	1	\N	\N	\N	\N	\N	\N
1247	local	TedSchPhoto1940.tif	2006-06-19 00:00:00	\N	584	Ted Hughes, "school-days" photograph, 1940	\N	9	25	140	1	Hughes' school portrait from Mexborough Grammar School.	\N	\N	\N	\N	\N
1248	local	\N	2006-06-19 00:00:00	\N	1	Atlanta Automobile Association Stock Certificate	\N	13	25	140	1	\N	\N	\N	\N	\N	\N
1249	local	\N	2006-06-19 00:00:00	2006-06-19 00:00:00	857	\N	\N	6	247	140	1	\N	\N	\N	\N	\N	\N
1250	local	\N	2006-06-19 00:00:00	2006-06-19 00:00:00	857	\N	\N	14	247	140	1	\N	\N	\N	\N	\N	\N
1251	local	\N	2006-06-19 00:00:00	2006-06-19 00:00:00	857	\N	\N	14	247	140	1	\N	\N	\N	\N	\N	\N
1252	local	\N	2006-06-19 00:00:00	2006-06-19 00:00:00	857	\N	\N	14	247	140	1	\N	\N	\N	\N	\N	\N
1253	local	\N	2006-06-19 00:00:00	2006-06-19 00:00:00	857	\N	\N	14	247	140	1	\N	\N	\N	\N	\N	\N
1254	local	\N	2006-06-19 00:00:00	2006-06-19 00:00:00	857	\N	\N	14	247	140	1	\N	\N	\N	\N	\N	\N
1255	local	\N	2006-06-19 00:00:00	2006-06-19 00:00:00	857	\N	\N	14	247	140	1	\N	\N	\N	\N	\N	\N
1256	local	\N	2006-06-19 00:00:00	2006-06-19 00:00:00	857	\N	\N	14	247	140	1	\N	\N	\N	\N	\N	\N
1257	local	\N	2006-06-19 00:00:00	2006-06-19 00:00:00	857	\N	\N	14	247	140	1	\N	\N	\N	\N	\N	\N
1258	local	\N	2006-06-19 00:00:00	2006-06-19 00:00:00	857	\N	\N	14	247	140	1	\N	\N	\N	\N	\N	\N
1259	local	\N	2006-06-19 00:00:00	2006-06-19 00:00:00	857	\N	\N	14	247	140	1	\N	\N	\N	\N	\N	\N
1260	local	\N	2006-06-19 00:00:00	2006-06-19 00:00:00	857	\N	\N	14	247	140	1	\N	\N	\N	\N	\N	\N
1261	local	\N	2006-06-19 00:00:00	2006-06-19 00:00:00	857	\N	\N	14	247	140	1	\N	\N	\N	\N	\N	\N
1262	local	\N	2006-06-19 00:00:00	2006-06-19 00:00:00	857	\N	\N	14	247	140	1	\N	\N	\N	\N	\N	\N
1263	local	\N	2006-06-22 00:00:00	2006-06-22 00:00:00	\N	\N	\N	6	247	140	1	\N	\N	\N	\N	\N	\N
1264	local	Contactsheet-1.tif	2006-06-22 00:00:00	\N	584	Ted at Faber [& Faber] party with Mr. and Mrs. [T.S.] Eliot, April 21, 1960.	\N	9	25	140	1	Ted Hughes with Faber and Faber editor and Nobel Prize winner T.S. Eliot. Hughes published several books with Faber and Faber including the 1333-page Collected Poems in 2003.	\N	\N	\N	\N	\N
1265	local	Exhibit1.tif	2006-06-22 00:00:00	\N	789	Ted in his library, Court Green, 1990.	\N	9	25	140	1	Written on back, "Sorting out a few flies for the next days fishing." Photograph by Gerald Hughes.	\N	\N	\N	\N	\N
1266	local	Exhibit2.tif	2006-06-22 00:00:00	\N	789	Ted, Gerald, Nicholas (holding gun), and Jack Orchard.	Devon, 1978.	9	25	140	1	Ted with Brother Gerald and son Nicholas.	\N	\N	\N	\N	\N
1267	local	Exhibit3.tif	2006-06-22 00:00:00	\N	584	Ted Hughes with Fish, 1980s.	\N	9	25	140	1	Hughes was an avid fisherman for most of his life.	\N	\N	\N	\N	\N
1268	local	\N	2006-06-23 00:00:00	\N	697	Celestine Sibley Childhood photo, ca. 1920s.	\N	9	25	140	1	\N	\N	\N	\N	\N	\N
1269	local	Exhibit4.tif	2006-06-23 00:00:00	\N	584	Ted Hughes at home with packed Ted Hughes Papers, ca. 1997.	\N	9	25	140	1	\N	\N	\N	\N	\N	\N
1270	local	Exhibit5.tif	2006-06-23 00:00:00	\N	789	Ted Fishing in Canada, ca. 1980s.	\N	9	25	140	1	\N	\N	\N	\N	\N	\N
1271	local	Exhibit7.tif	2006-06-23 00:00:00	\N	789	Gerald Hughes and Assia Wevill, ca. 1966.	Photograph taken by Ted Hughes.	9	25	140	1	Ted Hughes's brother Gerald with the artist Assia Wevill. Hughes began seeing Assia  during the fall of 1962 while he and Sylvia Plath were still married.	\N	\N	\N	\N	\N
1272	local	Exhibit8.tif	2006-06-23 00:00:00	\N	584	Ted and Carol Hughes, 1977? Buckingham Palace?	\N	9	25	140	1	\N	\N	\N	\N	\N	\N
1273	local	Exhibit9.tif	2006-06-23 00:00:00	\N	584	Ted Hughes with Stephen Spender and others, ca. 1980s.	\N	9	25	140	1	\N	\N	\N	\N	\N	\N
1274	local	Exhibit10.tif	2006-06-23 00:00:00	\N	584	Ted Hughes, Frieda, Nicholas, Carol and two unidentified others, ca. 1970s.	\N	9	25	140	1	\N	\N	\N	\N	\N	\N
1275	local	Exhibit11.tif	2006-06-23 00:00:00	\N	584	Ted Hughes at Simon Frasier University, ca. 1990s.	\N	9	25	140	1	\N	\N	\N	\N	\N	\N
1276	local	Exhibit12.tif	2006-06-23 00:00:00	\N	584	Ted Hughes and Roy Davids, ca. 1970s.	\N	9	25	140	1	"At one of the two trees at 'Wuthering Heights.'"	\N	\N	\N	\N	\N
1279	local	\N	2006-06-23 00:00:00	\N	826	Schedule for the Tuskegee Institute Choir during the United Negro Fund Concerts in New York City, 18-22 March [1955]	(As of March 16)	1	247	\N	1	\N	\N	This is page 1 of 2.	\N	\N	\N
1286	local	\N	2006-06-23 00:00:00	\N	826	Letter from Management Corporation of America Artists, Ltd.,  to William Levi Dawson, 27 November 1953	\N	1	247	\N	1	The letter is from Danny Welkes and discusses plans for the Tuskegee Institute Choir to appear on the Coca Cola show in December.	\N	\N	\N	\N	\N
1289	local	\N	2006-06-23 00:00:00	\N	826	Letter from William Levi Dawson to the Broadcasting and Film Division, United Council of Churches, 22 February 1955	\N	1	247	\N	1	The letter is addressed to Frank Nichols.  It concerns the appearance by the Tuskegee Institute Choir on the television show "Frontiers of Faith" in March 1955.	\N	\N	\N	\N	\N
1292	local	\N	2006-06-23 00:00:00	\N	826	Photograph of William Levi Dawson receiving an Honorary Doctorate of Music from Ithaca College, 16 May 1982	\N	9	247	\N	1	President James Walen hands Dawson the honorary degree.	\N	\N	\N	\N	\N
1293	local	\N	2006-06-23 00:00:00	\N	826	William Levi Dawson's travel diary for 1918	\N	1	247	\N	1	These pages contain entries for April 7-20.	\N	Entries for April 7 - September 21 have been scanned.	\N	\N	\N
1294	local	\N	2006-06-23 00:00:00	\N	826	William Levi Dawson's travel diary for 1918	\N	1	247	\N	1	These pages contain entries for April 21 - May 4.	\N	Entries for April 7 - September 21 have been scanned.	\N	\N	\N
1295	local	\N	2006-06-23 00:00:00	\N	826	William Levi Dawson's travel diary for 1918	\N	1	247	\N	1	These pages contain entries for May 5-18.	\N	Entries for April 7 - September 21 have been scanned.	\N	\N	\N
1296	local	\N	2006-06-23 00:00:00	\N	826	William Levi Dawson's travel diary for 1918	\N	1	247	\N	1	These pages contain entries for May 19 - June 1.	\N	Entries for April 7 - September 21 have been scanned.	\N	\N	\N
1297	local	\N	2006-06-23 00:00:00	\N	826	William Levi Dawson's travel diary for 1918	\N	1	247	\N	1	These pages contain entries for June 2-8.	\N	Entries for April 7 - September 21 have been scanned.	\N	\N	\N
1298	local	\N	2006-06-23 00:00:00	\N	826	William Levi Dawson's travel diary for 1918	\N	1	247	\N	1	These pages contain entries for June 9-15.	\N	Entries for April 7 - September 21 have been scanned.	\N	\N	\N
1299	local	\N	2006-06-23 00:00:00	\N	826	William Levi Dawson's travel diary for 1918	\N	1	247	\N	1	These pages contain entries for June 16-29.	\N	Entries for April 7 - September 21 have been scanned.	\N	\N	\N
1300	local	\N	2006-06-23 00:00:00	\N	826	William Levi Dawson's travel diary for 1918	\N	1	247	\N	1	These pages contain entries for June 30 - July 13.	\N	Entries for April 7 - September 21 have been scanned.	\N	\N	\N
1301	local	\N	2006-06-23 00:00:00	\N	826	William Levi Dawson's travel diary for 1918	\N	1	247	\N	1	These pages contain entries for July 14-27.	\N	Entries for April 7 - September 21 have been scanned.	\N	\N	\N
1302	local	\N	2006-06-23 00:00:00	\N	826	William Levi Dawson's travel diary for 1918	\N	1	247	\N	1	These pages contain entries for July 28 - August 10.	\N	Entries for April 7 - September 21 have been scanned.	\N	\N	\N
1303	local	\N	2006-06-23 00:00:00	\N	826	William Levi Dawson's travel diary for 1918	\N	1	247	\N	1	These pages contain entries for August 11-24.	\N	Entries for April 7 - September 21 have been scanned.	\N	\N	\N
1304	local	\N	2006-06-23 00:00:00	\N	826	William Levi Dawson's travel diary for 1918	\N	1	247	\N	1	These pages contain entries for August 25 - September 7.	\N	Entries for April 7 - September 21 have been scanned.	\N	\N	\N
1305	local	\N	2006-06-23 00:00:00	\N	826	William Levi Dawson's travel diary for 1918	\N	1	247	\N	1	These pages contain entries for September 8-21.	\N	Entries for April 7 - September 21 have been scanned.	\N	\N	\N
1306	local	\N	2006-06-23 00:00:00	\N	826	William Levi Dawson's travel diary from Africa, 1952-1953	\N	1	247	\N	1	This entry is for 14 November 1952 (page 1).	\N	Selected entries were digitized.	\N	\N	\N
1307	local	\N	2006-06-23 00:00:00	\N	826	William Levi Dawson's travel diary from Africa, 1952-1953	\N	1	247	\N	1	This entry is for 4 December 1952 (page 21).	\N	Selected entries were digitized.	\N	\N	\N
1308	local	\N	2006-06-23 00:00:00	\N	826	William Levi Dawson's travel diary from Africa, 1952-1953	\N	1	247	\N	1	This entry is for 8 December 1952 (page 25).	\N	Selected entries were digitized.	\N	\N	\N
1309	local	\N	2006-06-23 00:00:00	\N	826	William Levi Dawson's travel diary from Africa, 1952-1953	\N	1	247	\N	1	This entry is for 11 December 1952 (page 28).	\N	Selected entries were digitized.	\N	\N	\N
1310	local	\N	2006-06-23 00:00:00	\N	826	William Levi Dawson's travel journal from Spain, 1956	\N	1	247	\N	1	This entry is for 16 July 1956.	\N	Selected entries were digitized.	\N	\N	\N
1311	local	\N	2006-06-23 00:00:00	\N	826	William Levi Dawson's travel journal from Spain, 1956	\N	1	247	\N	1	This entry is for 19 July 1956.	\N	Selected entries were digitized.	\N	\N	\N
1312	local	\N	2006-06-23 00:00:00	\N	826	William Levi Dawson's travel journal from Spain, 1956	\N	1	247	\N	1	This entry is for 24 July 1956.	\N	Selected entries were digitized.	\N	\N	\N
1313	local	\N	2006-06-23 00:00:00	\N	826	William Levi Dawson's travel journal from Spain, 1956	\N	1	247	\N	1	This entry is for 8 August 1956.	\N	Selected entries were digitized.	\N	\N	\N
1314	local	Exhibit14.tif	2006-06-26 00:00:00	\N	584	Ted Hughes, David Ross, Daniel Weissbort, and Luca Myers, ca. 1990s.	\N	9	25	140	1	\N	\N	\N	\N	\N	\N
1315	local	Exhibit15.tif	2006-06-26 00:00:00	\N	789	Ted with William & Edith Hughes, Mexborough, 1950.	\N	9	25	140	1	Written on reverse: "Ted in the RAF": Mom and Dad with Brother Ted - at Mexborough, Yorkshire.	\N	\N	\N	\N	\N
1316	local	Exhibit16.tif	2006-06-26 00:00:00	\N	789	Ted and Edith Hughes, Mexborough, Yorkshire, 1950	\N	9	25	140	1	\N	\N	\N	\N	\N	\N
1317	local	Heaney1.tif	2006-06-26 00:00:00	\N	584	Letter dated 12th August 1990 from Seamus Heaney to Ted Hughes.	\N	1	25	140	1	Seamus discusses dedicating a poem to Ted.	\N	\N	\N	\N	\N
1318	local	Heaney2.tif	2006-06-26 00:00:00	\N	584	Casting and Gathering, For Ted Hughes, 1990.	\N	1	25	140	1	Dedication reads: "For Ted, with love and gratitude for helping me hear … . Happy birthday. Seamus, August - 1990.	\N	\N	\N	\N	\N
1319	local	HughesTSEliot1.tif	2006-06-26 00:00:00	\N	584	Envelope dated 30 October 1958 containing letter from T.S. Eliot to Ted Hughes.	\N	1	25	140	1	This envelope and letter were sent from Faber & Faber, LTD, where Eliot was serving as editor. The letter congrates Ted for winning first prize in the Guinness Poetry Award.	\N	\N	\N	\N	\N
1320	local	HughesTSEliot2.tif	2006-06-26 00:00:00	\N	584	Letter dated 30th October, 1958 from T.S. Eliot to Ted Hughes.	\N	1	25	140	1	Letter was sent from Faber & Faber, LTD, where Eliot was serving as editor. The letter congrates Ted for winning first prize in the Guinness Poetry Award.	\N	\N	\N	\N	\N
1321	local	Rushdie.tif	2006-06-26 00:00:00	\N	584	Letter dated 22nd December 1984 from Ted Hughes to Salman Rushdie.	\N	1	25	140	1	In the letter Rushdie congradulates Ted on his Laureatship.	\N	\N	\N	\N	\N
1322	local	\N	2006-06-27 00:00:00	\N	826	Highlights in the Career of William L. Dawson, ca. 1981	\N	1	247	140	1	Written by William Levi Dawson.	\N	This is page 1 of 21.	\N	\N	\N
1323	local	\N	2006-06-27 00:00:00	\N	826	Highlights in the Career of William L. Dawson, ca. 1981	\N	1	247	\N	1	Written by William Levi Dawson.	\N	This is page 2 of 21.	\N	\N	\N
1324	local	\N	2006-06-27 00:00:00	\N	826	Highlights in the Career of William L. Dawson, ca. 1981	\N	1	247	\N	1	Written by William Levi Dawson.	\N	This is page 3 of 21.	\N	\N	\N
1325	local	\N	2006-06-27 00:00:00	\N	826	Highlights in the Career of William L. Dawson, ca. 1981	\N	1	247	\N	1	Written by William Levi Dawson.	\N	This is page 4 of 21.	\N	\N	\N
1326	local	\N	2006-06-27 00:00:00	\N	826	Highlights in the Career of William L. Dawson, ca. 1981	\N	1	247	\N	1	Written by William Levi Dawson.	\N	This is page 5 of 21.	\N	\N	\N
1327	local	\N	2006-06-27 00:00:00	\N	826	Highlights in the Career of William L. Dawson, ca. 1981	\N	1	247	\N	1	Written by William Levi Dawson.	\N	This is page 6 of 21.	\N	\N	\N
1328	local	\N	2006-06-27 00:00:00	\N	826	Highlights in the Career of William L. Dawson, ca. 1981	\N	1	247	\N	1	Written by William Levi Dawson.	\N	This is page 7 of 21.	\N	\N	\N
1329	local	\N	2006-06-27 00:00:00	\N	826	Highlights in the Career of William L. Dawson, ca. 1981	\N	1	247	\N	1	Written by William Levi Dawson.	\N	This is page 8 of 21.	\N	\N	\N
1330	local	\N	2006-06-27 00:00:00	\N	826	Highlights in the Career of William L. Dawson, ca. 1981	\N	1	247	\N	1	Written by William Levi Dawson.	\N	This is page 9 of 21.	\N	\N	\N
1331	local	\N	2006-06-27 00:00:00	\N	826	Highlights in the Career of William L. Dawson, ca. 1981	\N	1	247	\N	1	Written by William Levi Dawson.	\N	This is page 10 of 21.	\N	\N	\N
1332	local	\N	2006-06-27 00:00:00	\N	826	Highlights in the Career of William L. Dawson, ca. 1981	\N	1	247	\N	1	Written by William Levi Dawson.	\N	This is page 11 of 21.	\N	\N	\N
1333	local	\N	2006-06-27 00:00:00	\N	826	Highlights in the Career of William L. Dawson, ca. 1981	\N	1	247	\N	1	Written by William Levi Dawson.	\N	This is page 12 of 21.	\N	\N	\N
1334	local	\N	2006-06-27 00:00:00	\N	826	Highlights in the Career of William L. Dawson, ca. 1981	\N	1	247	\N	1	Written by William Levi Dawson.	\N	This is page 13 of 21.	\N	\N	\N
1335	local	\N	2006-06-27 00:00:00	\N	826	Highlights in the Career of William L. Dawson, ca. 1981	\N	1	247	\N	1	Written by William Levi Dawson.	\N	This is page 14 of 21.	\N	\N	\N
1336	local	\N	2006-06-27 00:00:00	\N	826	Highlights in the Career of William L. Dawson, ca. 1981	\N	1	247	\N	1	Written by William Levi Dawson.	\N	This is page 15 of 21.	\N	\N	\N
1337	local	\N	2006-06-27 00:00:00	\N	826	Highlights in the Career of William L. Dawson, ca. 1981	\N	1	247	\N	1	Written by William Levi Dawson.	\N	This is page 16 of 21.	\N	\N	\N
1338	local	\N	2006-06-27 00:00:00	\N	826	Highlights in the Career of William L. Dawson, ca. 1981	\N	1	247	\N	1	Written by William Levi Dawson.	\N	This is page 17 of 21.	\N	\N	\N
1339	local	\N	2006-06-27 00:00:00	\N	826	Highlights in the Career of William L. Dawson, ca. 1981	\N	1	247	\N	1	Written by William Levi Dawson.	\N	This is page 18 of 21.	\N	\N	\N
1340	local	\N	2006-06-27 00:00:00	\N	826	Highlights in the Career of William L. Dawson, ca. 1981	\N	1	247	\N	1	Written by William Levi Dawson.	\N	This is page 19 of 21.	\N	\N	\N
1341	local	\N	2006-06-27 00:00:00	\N	826	Highlights in the Career of William L. Dawson, ca. 1981	\N	1	247	\N	1	Written by William Levi Dawson.	\N	This is page 20 of 21.	\N	\N	\N
1342	local	\N	2006-06-27 00:00:00	\N	826	Highlights in the Career of William L. Dawson, ca. 1981	\N	1	247	\N	1	Written by William Levi Dawson.	\N	This is page 21 of 21.	\N	\N	\N
1343	local	\N	2006-06-27 00:00:00	\N	826	List of awards received by William Levi Dawson, 1930-1978	\N	1	247	\N	1	\N	\N	This is page 1 of 2.	\N	\N	\N
1344	local	\N	2006-06-27 00:00:00	\N	826	List of awards received by William Levi Dawson, 1930-1978	\N	1	247	\N	1	\N	\N	This is page 2 of 2.	\N	\N	\N
1346	local	\N	2006-06-27 00:00:00	\N	826	Receipt for a trombone rented by William Levi Dawson, 16 November 1928	\N	15	247	\N	1	\N	\N	The receipt has two sides; this is side 1.	\N	\N	\N
1347	local	\N	2006-06-27 00:00:00	\N	826	Receipt for a trombone rented by William Levi Dawson, 16 November 1928	\N	15	247	\N	1	\N	\N	The receipt has two sides; this is side 2.	\N	\N	\N
1349	local	\N	2006-06-27 00:00:00	\N	826	Wedding announcement for the marriage of William Levi Dawson to Cecile Demae Nicholson, 21 September 1935	\N	1	247	\N	1	\N	\N	\N	\N	\N	\N
1353	local	\N	2006-06-28 00:00:00	2006-06-28 00:00:00	857	\N	\N	14	247	140	1	\N	\N	\N	\N	\N	\N
1354	local	\N	2006-06-28 00:00:00	2006-06-28 00:00:00	857	\N	\N	14	247	140	1	\N	\N	\N	\N	\N	\N
1355	local	\N	2006-06-28 00:00:00	2006-06-28 00:00:00	857	\N	\N	14	247	140	1	\N	\N	\N	\N	\N	\N
1356	local	\N	2006-06-28 00:00:00	2006-06-28 00:00:00	857	\N	\N	14	247	140	1	\N	\N	\N	\N	\N	\N
1357	local	\N	2006-06-28 00:00:00	2006-06-28 00:00:00	857	\N	\N	14	247	140	1	\N	\N	\N	\N	\N	\N
1358	local	\N	2006-06-28 00:00:00	2006-06-28 00:00:00	857	\N	\N	14	247	140	1	\N	\N	\N	\N	\N	\N
1359	local	\N	2006-06-28 00:00:00	2006-06-28 00:00:00	857	\N	\N	14	247	140	1	\N	\N	\N	\N	\N	\N
1360	local	\N	2006-06-28 00:00:00	2006-06-28 00:00:00	857	\N	\N	14	247	140	1	\N	\N	\N	\N	\N	\N
1361	local	\N	2006-06-28 00:00:00	2006-06-28 00:00:00	857	\N	\N	14	247	140	1	\N	\N	\N	\N	\N	\N
1362	local	\N	2006-06-28 00:00:00	2006-06-28 00:00:00	857	\N	\N	14	247	140	1	\N	\N	\N	\N	\N	\N
1363	local	\N	2006-06-28 00:00:00	2006-06-28 00:00:00	857	\N	\N	14	247	140	1	\N	\N	\N	\N	\N	\N
1364	local	\N	2006-06-28 00:00:00	2006-06-28 00:00:00	857	\N	\N	14	247	140	1	\N	\N	\N	\N	\N	\N
1365	local	\N	2006-06-28 00:00:00	2006-06-28 00:00:00	857	\N	\N	14	247	140	1	\N	\N	\N	\N	\N	\N
1366	local	\N	2006-06-28 00:00:00	2006-06-28 00:00:00	857	\N	\N	14	247	140	1	\N	\N	\N	\N	\N	\N
1367	local	\N	2006-06-28 00:00:00	2006-06-28 00:00:00	857	\N	\N	14	247	140	1	\N	\N	\N	\N	\N	\N
1368	local	TedFrida1.tif	2006-06-28 00:00:00	\N	947	Letter from Ted Hughes to Frida Hughes, 17 May 1978.	\N	1	25	140	1	\N	\N	\N	\N	\N	\N
1369	local	TedFrida2.tif	2006-06-28 00:00:00	\N	947	Letter from Ted Hughes to Frida Hughes, 17 May 1978.	\N	1	25	140	1	Reverse.	\N	\N	\N	\N	\N
1370	local	TitlePanel-1.tif	2006-06-28 00:00:00	\N	584	Ted Hughes, ca. 1960's	\N	9	25	140	1	\N	\N	\N	\N	\N	\N
1371	local	AssiaHat1.tif	2006-06-12 00:00:00	\N	584	Wevill, Assia, William Trevor, Jane Donaldson, Sean Gallagher on the Serpentine, ca. 1960	\N	9	25	140	1	Hughes began seeing the artist Assia Wevill during the fall of 1962 while he and Sylvia Plath were still married.	\N	COPY: WITH COLOR BAR	\N	\N	\N
1373	local	Emory05.tif	2006-06-09 00:00:00	\N	584	Ted Hughes and Sylvia Plath in their Boston Apartment, 1958.	\N	9	25	140	1	Photo dates to the period when Hughes and Plath lived in Boston, studying and working in the same small apartment.	\N	COPY: WITH COLOR BAR	\N	\N	\N
1374	local	Emory06.tif	2006-06-28 00:00:00	\N	584	Sylvia Plath camping at Rock Lake, Algonquin Provinvial Park, Ontario, Canada, July 1959.	\N	9	25	140	1	Photographed by Ted Hughes taken during Ted and Sylvia's camping trip across the US and Canada in 1959.	\N	With COLOR BAR.	\N	\N	\N
1377	local	Emory07.tif	2006-06-30 00:00:00	2006-06-30 00:00:00	584	Ted Hughes camping at Rock Lake, Algonquin Provincial Park, Ontario, Canada, July 1959.	\N	9	25	140	1	Photographed by Sylvia Plath taken during Ted and Sylvia's camping trip across the US and Canada in 1959.	\N	With COLOR BAR.	\N	\N	\N
1378	local	Emory08.tif	2006-06-30 00:00:00	2006-06-30 00:00:00	789	Ted Hughes in the harbor at Cornucopia, Wisconsin, July 1959.	\N	9	25	140	1	Photographed by Sylvia Plath. Taken during Ted and Sylvia's camping trip across the US and Canada in 1959.	\N	With COLOR BAR.	\N	\N	\N
1379	local	Emory10.tif	2006-06-30 00:00:00	\N	789	Ted Hughes at Yellowstone Lake, Yellowstone National Park, Wyoming, July 1959.	\N	9	25	140	1	Photographed by Sylvia Plath. Taken during Ted and Sylvia's camping trip across the US and Canada in 1959.	\N	With COLOR BAR.	\N	\N	\N
1380	local	Emory12.tif	2006-06-30 00:00:00	\N	584	"A Pride of Poets," 23 June 1960	\N	9	25	140	1	Stephen Spender, W.H. Auden, Ted Hughes, T.S. Eliot, and Louis Macneice at Faber and Faber cocktail party honoring W.H. Auden, photographed by Mark Gerson.	\N	With COLOR BAR.	\N	\N	\N
1381	local	Emory13.tif	2006-06-30 00:00:00	\N	789	Sylvia picnicking on Primrose Hill with Frieda in carriage, 1960.	\N	9	25	140	1	Photographed by Ted Hughes.	\N	With COLOR BAR.	\N	\N	\N
1382	local	Emory15.tif	2006-06-30 00:00:00	\N	584	Ted, Carol, Frieda and Nicholas Hughes, Yorkshire, ca. 1973.	\N	9	25	140	1	\N	\N	With COLOR BAR.	\N	\N	\N
1383	local	EmoryColor01.tif	2006-06-06 00:00:00	\N	584	Sylvia Plath, Frieda, and Nicholas among the daffodils at Court Green, April 1962	\N	9	25	140	1	This color photograph was taken by the Swedish photographer Siv Arb when she visited Court Green in April 1962 to interview Hughes for a piece she was writing for a Swedish magazine, Rondo.	\N	With COLOR BAR.	\N	\N	\N
1384	local	EmoryManuscripts01.tif	2006-06-30 00:00:00	\N	584	"The Thought-fox," 1995 MS.	\N	1	25	140	1	\N	\N	With COLOR BAR.	\N	\N	\N
1385	local	EmoryManuscripts02.tif	2006-06-30 00:00:00	\N	584	Cover of Saint Botolph's Review, 1956.	\N	1	25	140	1	In February 1956 Hughes contributed four poems to a new literary magazine called St. Botolph's Review.  It was at a party to mark the launch of the new magazine that he first met the American poet Sylvia Plath who was in Cambridge on a Fulbright Scholarship.	\N	\N	\N	\N	\N
1386	local	EmoryManuscripts04.tif	2006-06-30 00:00:00	\N	584	Sylvia Plath's holograph list of characters in "Falcon Yard," 1958.	\N	1	25	140	1	\N	\N	With COLOR BAR.	\N	\N	\N
1387	local	PrimroseBack.tif	2006-06-30 00:00:00	\N	584	(Reverse) Sylvia on Blanket with Baby Carriage, Primrose, 1961	\N	1	25	140	1	\N	\N	With COLOR BAR.	\N	\N	\N
1388	local	TedSchPhoto1940.tif	2006-06-19 00:00:00	\N	584	Ted Hughes, "school-days" photograph, 1940	\N	9	25	140	1	Hughes' school portrait from Mexborough Grammar School.	\N	With COLOR BAR	\N	\N	\N
1389	local	SpainPoetess.tif	2006-07-05 00:00:00	\N	584	\N	\N	1	25	140	1	\N	\N	WITH COLOR BAR.	\N	\N	\N
1390	local	TedAmerica1.tif	2006-07-05 00:00:00	\N	584	Ted at unknown lake during USA trip, 1959.	\N	9	25	140	1	Ted while traveling through the US with Sylvia. Photograph by Sylvia Plath.	\N	WITH COLOR BAR.	\N	\N	\N
1391	local	TedGraduation.tif	2006-07-05 00:00:00	\N	584	Ted Hughes, Cambridge graduation, 1954.	\N	9	25	140	1	Ted Hughes at his graduation from Pembroke College, Cambridge (Stearn & Sons).	\N	WITH COLOR BAR.	\N	\N	\N
1392	local	TedMirror.tif	2006-07-05 00:00:00	\N	789	Ted and Olwyn Hughes [in mirror reflection], Mexborough, Yorkshire, 1947.	\N	9	25	140	1	Ted photographed with sister Olwyn (reflected in mirror).	\N	With COLOR BAR.	\N	\N	\N
1393	local	TH-signature.tif	2006-07-05 00:00:00	\N	584	Ted Hughes's signature	\N	9	25	140	1	\N	\N	\N	\N	\N	\N
1394	local	FeastLupercal.tif	2006-07-05 00:00:00	\N	584	"The Feast of Lupercal," 1960.	\N	1	25	140	1	Ttypescript list of where poems were submitted, with holograph notes [in Plath's hand], and near complete typescript w/ holograph corrections.	\N	\N	\N	\N	\N
1395	local	ThoughtFox.tif	2006-07-05 00:00:00	\N	584	"The Thought-Fox," MS.	\N	1	25	140	1	\N	\N	\N	\N	\N	\N
1396	local	TedandLeonardBaskin.tif	2006-07-05 00:00:00	\N	584	Ted Hughes and Leonard Baskin in Cumbria, late 1970s	\N	9	25	140	1	Ted with his friend and  frequent collaborator, the artist Leonard Baskin.	\N	\N	\N	\N	\N
1397	local	ChildhoodCrow.tif	2006-07-05 00:00:00	\N	584	Crow, Draft titles for Crow "Childhood of Crow," 1970.	\N	9	25	140	1	From Crow: From the Life and Songs of the Crow (1970)	\N	\N	\N	\N	\N
1398	local	ChildhoodCrow.tif	2006-07-05 00:00:00	\N	584	Crow, Draft titles for Crow "Childhood of Crow," 1970 (BACK).	\N	9	25	140	1	From Crow: From the Life and Songs of the Crow (1970)	\N	\N	\N	\N	\N
1399	local	0500-001.tif	2006-07-06 00:00:00	\N	443	Bobby Jones, age 2, July 1904	\N	9	25	140	1	\N	\N	\N	\N	\N	\N
1400	local	0500-002.tif	2006-07-06 00:00:00	\N	443	Bobby Jones, age 6, earliest golfing photograph, 1908.	East Lake Country Club, Atlanta, GA.	9	25	140	1	This is the earlies known photograph of Bobby Jones playing golf.	\N	\N	\N	\N	\N
1401	local	0500-003.TIF	2006-07-06 00:00:00	\N	443	Bobby Jones and Archer Davison, age 13, 1915.	Druid Hills Golf Club, Atlanta, GA	9	25	140	1	\N	\N	\N	\N	\N	\N
1402	local	0500-004.tif	2006-07-06 00:00:00	\N	443	Bobby Jones, age 14, 1916.	U.S. Amateur Championship, Merion Cricket Club, Ardmore, PA.	9	25	140	1	This was Bobby Jones's first golf tournament outside of the south. He won the match.	\N	\N	\N	\N	\N
1403	local	0500-005.tif	2006-07-06 00:00:00	\N	443	Bobby Jones, age 14, 1916.	U.S. Amateur Championship, Merion Cricket Club, Ardmore, PA.	9	25	140	1	This was Bobby Jones's first golf tournament outside of the south. He won the match.	\N	A different image from 1402	\N	\N	\N
1404	local	0500-006.tif	2006-07-06 00:00:00	\N	443	Bobby Jones, Perry Adair, [?] Standish, [?] Edwards, 4 July 1918	Golf meet, East Lake Country Club, Atlanta, GA.	9	25	140	1	Bobby Jones played his first golf matches at East Lake, the original home of the Atlanta Athletic Club. In 1967 the Atlanta Athletic Club moved to Duluth, Georgia where it still exists today.	\N	\N	\N	\N	\N
1405	local	0500-007.tif	2006-07-06 00:00:00	\N	443	Bobby Jones and Harry Vardon, May 1920.	U.S. Open Championship, Inverness Club, Ohio.	9	25	140	1	Jones with Harry Vardon, a major figure in early golf history. Vardon won the British Open six times, and the U.S. Open once.	\N	\N	\N	\N	\N
1406	local	0500-008.tif	2006-07-06 00:00:00	\N	443	Bobby Jones and Chick Evans, 1920.	Western Amateur Championship, Memphis, TN.	9	25	140	1	Jones with Chick Evans, the first amature golfer to win the U.S Open and U.S Amature championships in one year.	\N	\N	\N	\N	\N
1407	local	0500-009.tif	2006-07-07 00:00:00	\N	443	Bobby Jones and [?], n.d.	\N	9	25	140	1	\N	\N	\N	\N	\N	\N
1408	local	0500-010.tif	2006-07-07 00:00:00	\N	443	Bobby Jones, ca. early 1920s.	\N	9	25	140	1	\N	\N	\N	\N	\N	\N
1409	local	0500-011.tif	2006-07-07 00:00:00	\N	443	Bobby Jones and Frank Godchaux, 1922.	Southern Amateur Champtionship, East Lake Country Club, Atlanta, GA.	9	25	140	1	Jones and Frank Godchaux at East Lake, the original home of the Atlanta Athletic Club. In 1967 the Atlanta Athletic Club moved to Duluth, Georgia where it still exists today.	\N	\N	\N	\N	\N
1410	local	0500-012.tif	2006-07-07 00:00:00	\N	443	Bobby Jones and Roger Wethered, 1922.	Walker Cup Tournament, National Golf Links of America, Southampton, NY.	9	25	140	1	Jones represented the United States in the Walker Cup five times, and winning 9 of 10 matches. The Walker cup is a golf tournament consisting of teams of amateur players from the US, Great Britain, and Ireland. The Walker Cup match is played in alternative years in the US and Europe.	\N	\N	\N	\N	\N
1411	local	0500-013.tif	2006-07-07 00:00:00	\N	443	Bobby Jones and George Duncan, 1922.	U.S. Open Championship, Skokie Country Club, Chicago, IL.	9	25	140	1	Caption reads, "Bobby Jones and George Duncan, the brilliant Scottish professional, who played the last two rounds together at Skokie, Chicago, in the national open championship of 1922, which Bobby finished a single stroke back of Sarazen. (Pietzcker)	\N	\N	\N	\N	\N
1412	local	0500-014.tif	2006-07-07 00:00:00	\N	443	Bobby Jones, 1922.	U.S. Open Championship, Skokie Country Club, Chicago, IL.	9	25	140	1	Jones finished second behind Gene Sarazen, his best U.S. Open performace yet.	\N	\N	\N	\N	\N
1413	local	0500-015.tif	2006-07-07 00:00:00	\N	443	Gene Sarazen, practicing at Jacksonville, FL, ca. 1922.	\N	9	25	140	1	Jones finished second at the U.S. Open Championship behind Gene Sarazen, his best performace yet. Sarazen is one of only a few golfers to with every major championship throughout his career: The U.S. Open twice, the PGA championship three times, and the British open and the Masters once each.	\N	\N	\N	\N	\N
1414	local	0500-016.tif	2006-07-07 00:00:00	\N	443	Bobby Jones putting on the third green during play-off with Bobby Cruickshank, 1923.	U.S. Open Championship, Inwood Country Club, Inwood, NJ.	9	25	140	1	Jones beat Cruickshank for his first U.S. Open victory.	\N	\N	\N	\N	\N
1415	local	0500-017.tif	2006-07-07 00:00:00	\N	443	Bobby Jones putting on the third green during play-off with Bobby Cruickshank, 1923.	U.S. Open Championship, Inwood Country Club, Inwood, NJ.	9	25	140	1	Jones beat Cruickshank for his first U.S. Open victory.	\N	\N	\N	\N	\N
1416	local	0500-018.tif	2006-07-07 00:00:00	\N	443	Bobby Jones playing out of a bunker during the final round, U.S. Open Championship, 1923.	Inwood Country Club, Inwood, NJ.	9	25	140	1	Jones beat Cruickshank for his first U.S. Open victory.	\N	\N	\N	\N	\N
1417	local	0500-019.tif	2006-07-07 00:00:00	\N	443	Bobby Jones playing out of a bunker during the final round, U.S. Open Championship, 1923.	Inwood Country Club, Inwood, NJ.	9	25	140	1	Jones beat Cruickshank for his first U.S. Open victory.	\N	\N	\N	\N	\N
1418	local	0500-020.tif	2006-07-07 00:00:00	\N	443	Jimmy Maiden, Bobby Jones, Bobby Cruickshank, and Stewart Maiden, 1923.	U.S. Open Championship, Inwood Country Club, Inwood, NJ.	9	25	140	1	Jones beat Cruickshank for his first U.S. Open victory.	\N	\N	\N	\N	\N
1419	local	0500-021.tif	2006-07-07 00:00:00	\N	443	Jimmy Maiden, Bobby Jones, Luke Ross, and Steward Maiden, 1923.	U.S. Open Championship, Inwood Country Club, Inwood, NJ.	9	25	140	1	Jones beat Cruickshank for his first U.S. Open victory.	\N	\N	\N	\N	\N
1420	local	0500-022.tif	2006-07-07 00:00:00	\N	443	Bobby Jones and [?], U.S. Open Championship, 1923.	Inwood Country Club, Inwood, NJ.	9	25	140	1	Jones beat Cruickshank for his first U.S. Open victory.	\N	\N	\N	\N	\N
1421	local	0500-023.tif	2006-07-07 00:00:00	\N	443	Bobby Jones and Bobby Cruickshank, 1923.	U.S. Open Championship, Inwood Country Club, Inwood, NJ.	9	25	140	1	Jones beat Cruickshank for his first U.S. Open victory.	\N	\N	\N	\N	\N
1422	local	0500-024.tif	2006-07-07 00:00:00	\N	443	Bobby Jones, Bobby Cruikshank, and others at awards ceremony, 1923.	U.S. Open Championship, Inwood Country Club.	9	25	140	1	Jones beat Cruickshank for his first U.S. Open victory.	\N	\N	\N	\N	\N
1423	local	0500-025.tif	2006-07-07 00:00:00	\N	443	Bobby Jones holding trophy cup, 16 July 1923.	U.S. Open Championship, Inwood Country Club, Inwood, NJ.	9	25	140	1	Jones beat Cruickshank for his first U.S. Open victory.	\N	\N	\N	\N	\N
1424	local	0500-026.tif	2006-07-07 00:00:00	\N	443	Bobby Jones, age 21, 1923.	U.S. Open Championship, Inwood Country Club, Inwood, NJ.	9	25	140	1	Jones beat Cruickshank for his first U.S. Open victory.	\N	\N	\N	\N	\N
1425	local	0500-027.tif	2006-07-07 00:00:00	\N	443	Scene at Brookwood Station, Atlanta, after U.S. Open Championship, 1923.	\N	9	25	140	1	Jones beat Cruickshank for his first U.S. Open victory.	\N	\N	\N	\N	\N
1426	local	0500-028.tif	2006-07-07 00:00:00	\N	443	Scene at Brookwood Station, Atlanta, after U.S. Open Championship, 1923.	\N	9	25	140	1	\N	\N	\N	\N	\N	\N
1427	local	0500-029.tif	2006-07-07 00:00:00	\N	443	O.B. Keeler at typwriter, n.d.	\N	9	25	140	1	Caption reads, "Not that it makes any difference. This is O.B. Keeler, known as the Boswell of Bobby Jones, and co-author with him of these memoirs." --quote: O.B. Keeler	\N	\N	\N	\N	\N
1428	local	0500-030.tif	2006-07-07 00:00:00	\N	443	Max Marston and Bobby Jones, 1923.	U.S. Amateur Championship, Flossmoor Country Club, Chicago, IL.	9	25	140	1	Caption reads, "Max Marston and Bobby Jones. Marston defeated Jones in the second round of the national amateur at Flossmoor, Chicago, in 1923 and went on to with the championship on the 38th green from Jess Sweetser.	\N	\N	\N	\N	\N
1429	local	0500-031.tif	2006-07-07 00:00:00	\N	443	U.S. Walker Cup Team, 1924.	[from left to right] Bobby Jones, Chick Evans, Jess Sweetser, Francis Ouimet, Bob Gardner, W.C. Fownes, Jr., Max Marston, Jesse Guilford, Harrison Johnston, and Dr. O.F. Willing.	9	25	140	1	Jones represented the United States in the Walker Cup five times, and winning 9 of 10 matches. The Walker cup is a golf tournament consisting of teams of amateur players from the US, Great Britain, and Ireland. The Walker Cup match is played in alternative years in the US and Europe.	\N	\N	\N	\N	\N
1430	local	0500-032.tif	2006-07-07 00:00:00	\N	443	Bobby Jones shaking hands with George Von Elm, 1924.	U.S. Amateur Championship, Merion Cricket Club, Ardmore, PA.	9	25	140	1	Jones beat George Von Elm to with the championship.	\N	\N	\N	\N	\N
1431	local	0500-033.tif	2006-07-07 00:00:00	\N	443	Bobby Jones and others at awards ceremony, 1924.	U.S. Amateur Championship, Merion Cricket Club, Ardmore, PA.	9	25	140	1	Jones beat George Von Elm to with the championship.	\N	\N	\N	\N	\N
1432	local	0500-034.tif	2006-07-07 00:00:00	\N	443	Bobby Jones receiving trophy cup, 1924.	U.S. Amateur Championship, Merion Cricket Club, Ardmore, PA.	9	25	140	1	Caption reads: "Bobby gets the big cup at Merion. Mynant D. Vanderpool is making the speech. Alan Wilson is in the background. George Von Elm looks slightly despondent. But his time is coming."	\N	\N	\N	\N	\N
1433	local	0500-035.tif	2006-07-07 00:00:00	\N	443	Bobby Jones and wife, Mary, at Atlanta Athletic Club dinner, [ca. 1924-1925?].	\N	9	25	140	1	Caption reads, "Mrs. Bobby, formerly Miss Mary Malone of Atlanta, and Bobby at one of the numerous dinners given in his honor by his home club, the Atlanta Athletic Club."	\N	\N	\N	\N	\N
1434	local	0500-036.tif	2006-07-07 00:00:00	\N	443	Bobby Jones and W. McFarlane shaking hands, 1925.	U.S. Open Championship, Worcester County Club, Worcester, MA.	9	25	140	1	Bobby Jones finished second.	\N	\N	\N	\N	\N
1435	local	0500-037.tif	2006-07-10 00:00:00	\N	443	Bobby Jones and Jimmy DeHart, 1925.	U.S. Amateur Championship, Oakmont Country Club, Pittsburgh, PA.	9	25	140	1	Jones won each of his matches by an average of eight holes.	\N	\N	\N	\N	\N
1436	local	0500-038.tif	2006-07-10 00:00:00	\N	443	Bobby Jones and Watts Gunn shaking hands, 1925.	U.S. Amateur Championship, Oakmont Country Club, Pittsburgh, PA.	9	25	140	1	Jones beat fellow East Lake golfer Watts Gunn in the only final match in the Amateur's history between two golfers from the same club.	\N	\N	\N	\N	\N
1437	local	0500-039.tif	2006-07-10 00:00:00	\N	443	Bobby Jones and Watts Gunn, 1925.	U.S. Amateur Championship, Oakmont Country Club, Pittsburgh, PA.	9	25	140	1	Jones beat fellow East Lake golfer Watts Gunn in the only final match in the Amateur's history between two golfers from the same club.	\N	\N	\N	\N	\N
1438	local	0500-040.tif	2006-07-10 00:00:00	\N	443	Bobby Jones and Watts Gunn with trophy cup, 1925.	U.S. Amateur Championship, Oakmont Country Club, Pittsburgh, PA.	9	25	140	1	Jones beat fellow East Lake golfer Watts Gunn in the only final match in the Amateur's history between two golfers from the same club.	\N	\N	\N	\N	\N
1439	local	0500-041.tif	2006-07-10 00:00:00	\N	443	Gallery watchers, 1925.	U.S. Open Championship, Oakmont Country Club, Pittsburgh, PA, 1925.	9	25	140	1	Jones beat fellow East Lake golfer Watts Gunn in the only final match in the Amateur's history between two golfers from the same club.	\N	\N	\N	\N	\N
1440	local	0500-042.tif	2006-07-10 00:00:00	\N	443	Bobby Jones with trophy cup, 1925.	U.S. Amateur Championship, Oakmont Country Club, Pittsburgh, PA.	9	25	140	1	Jones beat fellow East Lake golfer Watts Gunn in the only final match in the Amateur's history between two golfers from the same club.	\N	\N	\N	\N	\N
1441	local	0500-043.tif	2006-07-10 00:00:00	\N	443	Watts Gunn, D.P. Davis and Bobby Jones, 1926.	Golf match, St. Augustine, FL.	9	25	140	1	caption reads, "At a Florida match, St. Augustine. Watts Gunn and Bobby Jones with their host, the late D. P. Davis, who was drowned six months later. The Atlanta boys played Archie Compston and Arnaud Massy at St. Augustine early in the season of 1926."	\N	\N	\N	\N	\N
1442	local	0500-044.tif	2006-07-10 00:00:00	\N	443	Bobby Jones and Sam Sweeting, 1926.	Fishing trip to Sarasota Bay, FL.	9	25	140	1	Caption reads, " 'I love to play,' says Bobby in the story. Here he is off with Sam Sweeting for a fishing trip in Sarasota Bay, Florida. Photo by Keeler."	\N	\N	\N	\N	\N
1443	local	0500-045.tif	2006-07-10 00:00:00	\N	443	Bobby Jones and wife, Mary, 1926.	Fishing trip to Sarasota Bay, FL.	9	25	140	1	Caption reads, "Bobby fishing in Sarasota Bay. Mrs. Bobby, well wrapped up, sits behind him."	\N	\N	\N	\N	\N
1444	local	0500-046.tif	2006-07-10 00:00:00	\N	443	Gene Tunney, exhibition match, Miami, FL, 1926.	\N	9	25	140	1	Heavyweight boxing champion from 1926-28.	\N	\N	\N	\N	\N
1445	local	0500-047.tif	2006-07-10 00:00:00	\N	443	Clark Griffith and Bobby Jones, 1925-1926.	Whitfield Estates Country Club. Sarasota, FL.	9	25	140	1	Bobby Jones with MLB pitcher Clark Griffith.	\N	\N	\N	\N	\N
1446	local	0500-048.tif	2006-07-10 00:00:00	\N	443	Bobby Jones and Walter Gagen, 1926.	Whitfield Estates Country Club, Sarasota, FL.	9	25	140	1	Caption reads, "Bobby loves to play against the professionals, especially Walter Hagen, who gave him the most conclusive drubbing of his career early in 1926 in a 72-hole match in Florida. He is here shown with Sir Walter at the start of that match at Sarasota. Between them is the referee, George Morse, well-known golfer and sportsman of Vermont."	\N	\N	\N	\N	\N
1447	local	0500-049.tif	2006-07-10 00:00:00	\N	443	Bobby Jones receiving trophy cup from W.C. Fownes, Jr., 1926.	U.S. Open Championship, Scioto Country Club, Columbus, OH.	9	25	140	1	Bobby Jones won this his second U.S. Open Championship.	\N	\N	\N	\N	\N
1448	local	0500-050.tif	2006-07-10 00:00:00	\N	443	Bobby Jones and Robert Harris, 1926.	British Amateur Championship, Muirfield Golf Club, Scotland.	9	25	140	1	Caption reads, "Bobby Jones, American amateur champion (at the time), and Robert Harris, British amateur champion, as they started their match in the fifth round of the 1926 British amateur championship at Muirfield, Scotland, in which Jones was the victor by the astonishing margin of 8-6 in an 18-hole match."	\N	\N	\N	\N	\N
1449	local	0500-051.tif	2006-07-10 00:00:00	\N	443	Caddies Jack McIntyre and Jamieson Hogg, Scotland, 1926.	\N	9	25	140	1	Caption reads, "Scotland owns two champion caddies. The big one is Jack McIntyre, who carried Bobby Jones' clubs at St. Anne's when he won the British open of 1926. The left one with all the freckles is Jamieson Hogg, who caddied for Jess Sweetser who won the British amateur championship a few weeks earlier."	\N	\N	\N	\N	\N
1451	local	0500-053.tif	2006-07-10 00:00:00	\N	443	Ted Ray, Bobby Jones, James Briad, and Harry Vardon, 1926.	British Open Championship, St. Anne's England.	9	25	140	1	This was Bobby Jones's fist Open Championship victory.	\N	\N	\N	\N	\N
1452	local	0500-054.tif	2006-07-10 00:00:00	\N	443	Bobby Jones with trophy cup, 1926.	British Open Championship, St. Anne's, England.	9	25	140	1	This was Bobby Jones's fist Open Championship victory.	\N	\N	\N	\N	\N
1453	local	0500-055.tif	2006-07-10 00:00:00	\N	443	Bobby Jones and Al Watrous at play, 1926.	British Open Championship, St. Anne's, England.	9	25	140	1	This was Bobby Jones's fist Open Championship victory.	\N	\N	\N	\N	\N
1454	local	0500-056.tif	2006-07-10 00:00:00	\N	443	Gallery shot, 1926.	British Open Championship, St. Anne's, England.	9	25	140	1	This was Bobby Jones's fist Open Championship victory.	\N	\N	\N	\N	\N
1455	local	0500-057.tif	2006-07-10 00:00:00	\N	443	Gallery shot, 1926.	British Open Championship, St. Anne's, England.	9	25	140	1	This was Bobby Jones's fist Open Championship victory.	\N	\N	\N	\N	\N
1456	local	0500-058.tif	2006-07-10 00:00:00	\N	443	Frances Ouimet, swinging, 1926.	George Duncan's course, Wentworth Hall, Surrey, England.	9	25	140	1	\N	\N	\N	\N	\N	\N
1457	local	0500-059.tif	2006-07-11 00:00:00	\N	443	Bobby Jones and Frances Ouimet, 1926.	George Duncan's course, Wentworth Hall, Surrey, England.	9	25	140	1	\N	\N	\N	\N	\N	\N
1458	local	0500-060.tif	2006-07-11 00:00:00	\N	443	Bobby Jones and Frances Ouimet, 1926.	George Duncan's course, Wentworth Hall, Surrey, England.	9	25	140	1	\N	\N	\N	\N	\N	\N
1459	local	0500-061.tif	2006-07-11 00:00:00	\N	443	Bobby Jones and Frances Ouimet, 1926.	George Duncan's course, Wentworth Hall, Surrey, England.	9	25	140	1	\N	\N	\N	\N	\N	\N
1460	local	0500-062.tif	2006-07-11 00:00:00	\N	443	American Walker Cup International Golf Team, 1926.	\N	9	25	140	1	Jones represented the United States in the Walker Cup five times, and winning 9 of 10 matches. The Walker cup is a golf tournament consisting of teams of amateur players from the US, Great Britain, and Ireland. The Walker Cup match is played in alternative years in the US and Europe.	\N	\N	\N	\N	\N
1461	local	0500-063.tif	2006-07-11 00:00:00	\N	443	Gallery scene, 1926.	Walker Cup, St. Andrews, Scotland.	9	25	140	1	Caption reads, "The Stars and Stripes, mingled with the Union Jack, floating over the eighteen green at St. Andrews, the home of golf, as the 1926 Walker Cup international matches are finished with Uncle once on top -- by a scant point."	\N	\N	\N	\N	\N
1462	local	0500-064.tif	2006-07-11 00:00:00	\N	443	Gallery scene, 1926.	Walker Cup, St. Andrews, Scotland.	9	25	140	1	Caption reads, "Evening at St. Andrews, the home of golf, and the finish of the last match of the 1926 international struggle between Great Britain and America, won by America by a single point."	\N	\N	\N	\N	\N
1463	local	0500-065.tif	2006-07-11 00:00:00	\N	443	Bobby Jones and O.B. Keeler with [from left] U.S. Open, Southern Open, Walker Cup, and British Open trophies, 1926.	\N	9	25	140	1	Jones with devoted sportwriter and friend O.B. Keeler and various golf trophies.	\N	\N	\N	\N	\N
1464	local	0500-066.tif	2006-07-11 00:00:00	\N	443	Bobby Jones and O.B. Keeler with [from left] U.S. Open, Southern Open, Walker Ccup, and British Open trophies, 1926.	\N	9	25	140	1	Jones with devoted sportwriter and friend O.B. Keeler and various golf trophies.	\N	\N	\N	\N	\N
1465	local	0500-067.tif	2006-07-11 00:00:00	\N	443	Bobby Jones preparing to swing, n.d.	\N	9	25	140	1	\N	\N	\N	\N	\N	\N
1466	local	0500-068.tif	2006-07-11 00:00:00	\N	443	Bobby Jones, O.B. Keeler, Mrs. Andrews with guns, n.d.	\N	9	25	140	1	Jones with devoted sportwriter and friend O.B. Keeler.	\N	\N	\N	\N	\N
1467	local	0500-069.tif	2006-07-11 00:00:00	\N	443	Bobby Jones, 24 August 1927.	U.S. Amateur Championship, Minikahda Club, Minneapolis, MN.	9	25	140	1	Jones won in Minneapolis for his third U.S. Amateur victory.	\N	\N	\N	\N	\N
1468	local	0500-070.tif	2006-07-11 00:00:00	\N	443	U.S. Amateur Championship, Minikahda Club, Minneapolis, MN, 24 August 1927.	\N	9	25	140	1	Jones won in Minneapolis for his third U.S. Amateur victory.	\N	\N	\N	\N	\N
1469	local	0500-071.tif	2006-07-11 00:00:00	\N	443	Bobby Jones and Harrison Johnston, 25 August 1927.	U.S. Amateur Championship, Minikahda Club, Minneapolis, MN.	9	25	140	1	Jones won in Minneapolis for his third U.S. Amateur victory.	\N	\N	\N	\N	\N
1470	local	0500-072.tif	2006-07-11 00:00:00	\N	443	Bobby Jones and Maurice McCarthy, 25 August 1927.	U.S. Amateur Championship, Minikahda Club, Minneapolis, MN.	9	25	140	1	Jones won in Minneapolis for his third U.S. Amateur victory.	\N	\N	\N	\N	\N
1471	local	0500-073.tif	2006-07-11 00:00:00	\N	443	Bobby Jones at play, 27 August 1927.	U.S. Amateur Championship, Minikahda Club, Minneapolis, MN.	9	25	140	1	Jones won in Minneapolis for his third U.S. Amateur victory.	\N	\N	\N	\N	\N
1472	local	0500-074.tif	2006-07-11 00:00:00	\N	443	Bobby Jones shakes hands with Chick Evans, 27 August 1927.	U.S. Amateur Championship, Minikahda Club, Minneapolis, MN.	9	25	140	1	Jones won in Minneapolis for his third U.S. Amateur victory.	\N	\N	\N	\N	\N
1473	local	0500-075.tif	2006-07-11 00:00:00	\N	443	Trophy Cup, 27 August 1927.	U.S. Amateur Championship, Minikahda Club, Minneapolis, MN.	9	25	140	1	Jones won in Minneapolis for his third U.S. Amateur victory.	\N	\N	\N	\N	\N
1474	local	0500-076.tif	2006-07-11 00:00:00	\N	443	Bobby Jones at play, 27 August 1927.	U.S. Amateur Championship, Minikahda Club, Minneapolis, MN.	9	25	140	1	Jones won in Minneapolis for his third U.S. Amateur victory.	\N	\N	\N	\N	\N
1475	local	0500-077.tif	2006-07-11 00:00:00	\N	443	Bobby Jones receiving trophy from W.C. Fownes, 27 August 1927.	U.S. Amateur Championship, Minikahda Club, Minneapolis, MN.	9	25	140	1	Jones won in Minneapolis for his third U.S. Amateur victory.	\N	\N	\N	\N	\N
1476	local	0500-078.tif	2006-07-11 00:00:00	\N	443	Bobby Jones and Chick Evans at play, 28 August 1927.	U.S. Amateur Championship, Minikahda Club, Minneapolis, MN.	9	25	140	1	Jones won in Minneapolis for his third U.S. Amateur victory.	\N	\N	\N	\N	\N
1477	local	0500-079.tif	2006-07-11 00:00:00	\N	443	Bobby Jones, August 1927.	U.S. Amateur Championship, Minikahda Club, Minneapolis, MN.	9	25	140	1	Jones won in Minneapolis for his third U.S. Amateur victory.	\N	\N	\N	\N	\N
1478	local	0500-080.tif	2006-07-11 00:00:00	\N	443	Bobby Jones and Francis Ouimet, August 1927.	U.S. Amateur Championship, Minikahda Club, Minneapolis, MN.	9	25	140	1	Jones won in Minneapolis for his third U.S. Amateur victory.	\N	\N	\N	\N	\N
1479	local	0500-081.tif	2006-07-11 00:00:00	\N	443	Gallery scene, 1927.	U.S. Amateur Championship, Minikahda Club, Minneapolis, MN.	9	25	140	1	Jones won in Minneapolis for his third U.S. Amateur victory.	\N	\N	\N	\N	\N
1480	local	0500-082.tif	2006-07-11 00:00:00	\N	443	Bobby Jones with puppy, December 1927.	Georgia Field Trial Club, Waynesboro, GA.	9	25	140	1	\N	\N	\N	\N	\N	\N
1481	local	0500-083.tif	2006-07-11 00:00:00	\N	443	Bobby Jones with George Washington Chance, December 1927.	Georgia Field Trial Club, Waynesboro, GA.	9	25	140	1	\N	\N	\N	\N	\N	\N
1482	local	0500-084.tif	2006-07-11 00:00:00	\N	443	Bobby Jones at play, 28 June 1929.	U.S. Open Championship, Winged Food Golf Club, Mamaroneck, NY.	9	25	140	1	This was Bobby Jones's third U.S Open Championship victory.	\N	\N	\N	\N	\N
1483	local	0500-085.tif	2006-07-11 00:00:00	\N	443	Bobby Jones, 27 June 1929.	U.S. Open Championship, Winged Food Golf Club, Mamaroneck, NY.	9	25	140	1	This was Bobby Jones's third U.S Open Championship victory.	\N	\N	\N	\N	\N
1484	local	0500-086.tif	2006-07-11 00:00:00	\N	443	Bobby Jones at play, 29 June 1929.	U.S. Open Championship, Winged Food Golf Club, Mamaroneck, NY.	9	25	140	1	This was Bobby Jones's third U.S Open Championship victory.	\N	\N	\N	\N	\N
1485	local	0500-087.tif	2006-07-11 00:00:00	\N	443	Bobby Jones at play, 29 June 1929.	U.S. Open Championship, Winged Food Golf Club, Mamaroneck, NY.	9	25	140	1	This was Bobby Jones's third U.S Open Championship victory.	\N	\N	\N	\N	\N
1486	local	0500-088.tif	2006-07-11 00:00:00	\N	443	Al Espinosa at play, 29 June 1929.	U.S. Open Championship, Winged Food Golf Club, Mamaroneck, NY.	9	25	140	1	This was Bobby Jones's third U.S Open Championship victory.	\N	\N	\N	\N	\N
1487	local	0500-089.tif	2006-07-11 00:00:00	\N	443	Bobby Jones and Al Watrous at play, June 1929.	U.S. Open Championship, Winged Food Golf Club, Mamaroneck, NY.	9	25	140	1	This was Bobby Jones's third U.S Open Championship victory.	\N	\N	\N	\N	\N
1488	local	0500-090.tif	2006-07-11 00:00:00	\N	443	Bobby Jones at play, 29 June 1929.	U.S. Open Championship, Winged Food Golf Club, Mamaroneck, NY.	9	25	140	1	This was Bobby Jones's third U.S Open Championship victory.	\N	\N	\N	\N	\N
1489	local	0500-091.tif	2006-07-11 00:00:00	\N	443	Bobby Jones and Al Espinosa, 30 June 1929.	U.S. Open Championship, Winged Food Golf Club, Mamaroneck, NY.	9	25	140	1	This was Bobby Jones's third U.S Open Championship victory.	\N	\N	\N	\N	\N
1490	local	0500-092.tif	2006-07-11 00:00:00	\N	443	Bobby Jones and Al Espinosa shaking hands, 30 June 1929.	U.S. Open Championship, Winged Food Golf Club, Mamaroneck, NY.	9	25	140	1	This was Bobby Jones's third U.S Open Championship victory.	\N	\N	\N	\N	\N
1491	local	0500-093.tif	2006-07-11 00:00:00	\N	443	Bobby Jones putting on the 5th green, final round, 30 June 1929.	U.S. Open Championship, Winged Food Golf Club, Mamaroneck, NY.	9	25	140	1	This was Bobby Jones's third U.S Open Championship victory.	\N	\N	\N	\N	\N
1492	local	0500-094.tif	2006-07-11 00:00:00	\N	443	Bobby Jones teeing off, 1929.	U.S. Open Championship, Winged Food Golf Club, Mamaroneck, NY.	9	25	140	1	This was Bobby Jones's third U.S Open Championship victory.	\N	\N	\N	\N	\N
1493	local	0500-095.tif	2006-07-11 00:00:00	\N	443	Bobby Jones at play with gallery watching, 1929.	U.S. Open Championship, Winged Food Golf Club, Mamaroneck, NY.	9	25	140	1	This was Bobby Jones's third U.S Open Championship victory.	\N	\N	\N	\N	\N
1494	local	0500-096.tif	2006-07-11 00:00:00	\N	443	Bobby Jones at play with gallery watching, 1929.	U.S. Open Championship, Winged Food Golf Club, Mamaroneck, NY.	9	25	140	1	This was Bobby Jones's third U.S Open Championship victory.	\N	\N	\N	\N	\N
1495	local	0500-097.tif	2006-07-12 00:00:00	\N	443	Douglas Fairbanks, autographed photograph, n.d.	\N	9	25	140	1	Fairbanks was an early silent movie actor, screenwriter, director and producer active in the 1920s and 30s.	\N	\N	\N	\N	\N
1496	local	0500-098.tif	2006-07-12 00:00:00	\N	443	Bobby Jones, formal pose, n.d,	\N	9	25	140	1	\N	\N	\N	\N	\N	\N
1497	local	0500-099.tif	2006-07-12 00:00:00	\N	443	Bobby Jones and O.B. Keeler, n.d.	\N	9	25	140	1	Jones with devoted sportwriter and friend O.B. Keeler.	\N	\N	\N	\N	\N
1498	local	0500-100.tif	2006-07-12 00:00:00	\N	443	Walker Cup team members Brown and Johnson with Douglas Fairbanks, 5 June 1930.	Paddington Station.	9	25	140	1	Jones represented the United States in the Walker Cup five times, and winning 9 of 10 matches. The Walker cup is a golf tournament consisting of teams of amateur players from the US, Great Britain, and Ireland. The Walker Cup match is played in alternative years in the US and Europe.	\N	\N	\N	\N	\N
1499	local	0500-101.tif	2006-07-12 00:00:00	\N	443	Walker Cup team members Brown and Johnson with Douglas Fairbanks, Paddington Station, 5 June 1930.	\N	9	25	140	1	Jones represented the United States in the Walker Cup five times, and winning 9 of 10 matches. The Walker cup is a golf tournament consisting of teams of amateur players from the US, Great Britain, and Ireland. The Walker Cup match is played in alternative years in the US and Europe.	\N	\N	\N	\N	\N
1500	local	0500-102.tif	2006-07-12 00:00:00	\N	443	U.S. Walker Cup team, Addington, Surrey, 5 July 1930.	\N	9	25	140	1	[from left, back row] Roland Mackenzie, Bobby Jones, Don Moe, George Voigt, [front row] Harrison Johnston, Dr. O.F. Willing, Francis Ouimet, and George Von Elm.	\N	\N	\N	\N	\N
1501	local	0500-103.tif	2006-07-12 00:00:00	\N	443	George Von Elm, Leo Diegel, and other members of U.S. Walker Cup team on the practice green, 5 July 1930.	Addington, Surrey.	9	25	140	1	Jones represented the United States in the Walker Cup five times, and winning 9 of 10 matches. The Walker cup is a golf tournament consisting of teams of amateur players from the US, Great Britain, and Ireland. The Walker Cup match is played in alternative years in the US and Europe.	\N	\N	\N	\N	\N
1502	local	0500-104.tif	2006-07-12 00:00:00	\N	443	U.S. Walker Cup team, Addington, Surrey, 5 July 1930.	\N	9	25	140	1	[from left] Dr. O.F. Willing, George Voigt, Don Moe, and Bobby Jones during a practice round.	\N	\N	\N	\N	\N
1503	local	0500-105.tif	2006-07-12 00:00:00	\N	443	Walker Cup team members Douglas Fairbanks and Leo Diegel, 5 July 1930.	Addington, Surrey.	9	25	140	1	Jones represented the United States in the Walker Cup five times, and winning 9 of 10 matches. The Walker cup is a golf tournament consisting of teams of amateur players from the US, Great Britain, and Ireland. The Walker Cup match is played in alternative years in the US and Europe.	\N	\N	\N	\N	\N
1504	local	0500-106.tif	2006-07-12 00:00:00	\N	443	Walker Cup team member Don Moe, swinging, 5 July 1930.	Addington, Surrey.	9	25	140	1	Jones represented the United States in the Walker Cup five times, and winning 9 of 10 matches. The Walker cup is a golf tournament consisting of teams of amateur players from the US, Great Britain, and Ireland. The Walker Cup match is played in alternative years in the US and Europe.	\N	\N	\N	\N	\N
1505	local	0500-107.tif	2006-07-12 00:00:00	\N	443	Walker Cup team members Douglas Fairbanks and Leo Diegel, practicing, 5 July 1930.	Addington, Surrey.	9	25	140	1	Jones represented the United States in the Walker Cup five times, and winning 9 of 10 matches. The Walker cup is a golf tournament consisting of teams of amateur players from the US, Great Britain, and Ireland. The Walker Cup match is played in alternative years in the US and Europe.	\N	\N	\N	\N	\N
1506	local	0500-108.tif	2006-07-12 00:00:00	\N	443	Walker Cup team members Douglas Fairbanks and Leo Diegel, 5 July 1930.	Addington, Surrey.	9	25	140	1	Jones represented the United States in the Walker Cup five times, and winning 9 of 10 matches. The Walker cup is a golf tournament consisting of teams of amateur players from the US, Great Britain, and Ireland. The Walker Cup match is played in alternative years in the US and Europe.	\N	\N	\N	\N	\N
1507	local	0500-109.tif	2006-07-12 00:00:00	\N	443	Walker Cup team member Roland MacKenzie, swinging, 5 July 1930.	Addington, Surrey.	9	25	140	1	Jones represented the United States in the Walker Cup five times, and winning 9 of 10 matches. The Walker cup is a golf tournament consisting of teams of amateur players from the US, Great Britain, and Ireland. The Walker Cup match is played in alternative years in the US and Europe.	\N	\N	\N	\N	\N
1508	local	0500-110.tif	2006-07-12 00:00:00	\N	443	Walker Cup team member George Von Elm practicing, 5 July 1930.	Addington, Surrey.	9	25	140	1	Jones represented the United States in the Walker Cup five times, and winning 9 of 10 matches. The Walker cup is a golf tournament consisting of teams of amateur players from the US, Great Britain, and Ireland. The Walker Cup match is played in alternative years in the US and Europe.	\N	\N	\N	\N	\N
1509	local	0500-111.tif	2006-07-12 00:00:00	\N	443	Walker Cup team member Dr. O.F. Willing, practicing, 5 July 1930.	Addington, Surrey.	9	25	140	1	Jones represented the United States in the Walker Cup five times, and winning 9 of 10 matches. The Walker cup is a golf tournament consisting of teams of amateur players from the US, Great Britain, and Ireland. The Walker Cup match is played in alternative years in the US and Europe.	\N	\N	\N	\N	\N
1510	local	0500-112.tif	2006-07-12 00:00:00	\N	443	Bobby Jones practicing.	Addington, Surrey.	9	25	140	1	\N	\N	\N	\N	\N	\N
1511	local	0500-113.tif	2006-07-12 00:00:00	\N	443	Bobby Jones taking a break, May 1930.	British Amateur Championship, St. Andrews, Scotland.	9	25	140	1	In 1930 Bobby Jones completed the "Grand Slam" of golf: winning the British Open, the US Open, the US Amateur, and the British Amateur in one year.	\N	\N	\N	\N	\N
1512	local	0500-114.tif	2006-07-12 00:00:00	\N	443	Bobby Jones and Roger H. Wethered, 18th green, 31 May 1930.	British Amateur Championship, St. Andrews, Scotland.	9	25	140	1	In 1930 Bobby Jones completed the "Grand Slam" of golf: winning the British Open, the US Open, the US Amateur, and the British Amateur in one year.	\N	\N	\N	\N	\N
1513	local	0500-115.tif	2006-07-12 00:00:00	\N	443	Bobby Jones being escorted to Club House after winning, 31 May 1930.	British Amateur Championship, St. Andrews, Scotland.	9	25	140	1	In 1930 Bobby Jones completed the "Grand Slam" of golf: winning the British Open, the US Open, the US Amateur, and the British Amateur in one year.	\N	\N	\N	\N	\N
1514	local	0500-116.tif	2006-07-12 00:00:00	\N	443	Bobby Jones lifted above crowd, 31 May 1930.	British Amateur Championship, St. Andrews, Scotland.	9	25	140	1	In 1930 Bobby Jones completed the "Grand Slam" of golf: winning the British Open, the US Open, the US Amateur, and the British Amateur in one year.	\N	\N	\N	\N	\N
1515	local	0500-117.tif	2006-07-12 00:00:00	\N	443	Bobby Jones receiving trophy cup from Col. Skene, 31 May 1930.	British Amateur Championship, St. Andrews, Scotland.	9	25	140	1	In 1930 Bobby Jones completed the "Grand Slam" of golf: winning the British Open, the US Open, the US Amateur, and the British Amateur in one year.	\N	\N	\N	\N	\N
1516	local	0500-118.tif	2006-07-12 00:00:00	\N	443	Bobby Jones speaking at award ceremony, 31 May 1930.	British Amateur Championship, St. Andrews, Scotland.	9	25	140	1	In 1930 Bobby Jones completed the "Grand Slam" of golf: winning the British Open, the US Open, the US Amateur, and the British Amateur in one year.	\N	\N	\N	\N	\N
1517	local	0500-119.tif	2006-07-12 00:00:00	\N	443	Bobby Jones and Roger H. Wthered shaking hands, 31 May 1930.	British Amateur Championship, St. Andrews, Scotland.	9	25	140	1	In 1930 Bobby Jones completed the "Grand Slam" of golf: winning the British Open, the US Open, the US Amateur, and the British Amateur in one year.	\N	\N	\N	\N	\N
1518	local	0500-120.tif	2006-07-12 00:00:00	\N	443	Bobby Jones, putting on the 10th green, 18 June 1930.	British Open Championship, Royal Liverpool Golf Club, Hoylake, England.	9	25	140	1	In 1930 Bobby Jones completed the "Grand Slam" of golf: winning the British Open, the US Open, the US Amateur, and the British Amateur in one year.	\N	\N	\N	\N	\N
1519	local	0500-121.tif	2006-07-12 00:00:00	\N	443	Bobby Jones, 18 June 1930.	British Open Championship, Royal Liverpool Golf Club, Hoylake, England.	9	25	140	1	In 1930 Bobby Jones completed the "Grand Slam" of golf: winning the British Open, the US Open, the US Amateur, and the British Amateur in one year.	\N	\N	\N	\N	\N
1520	local	0500-122.tif	2006-07-13 00:00:00	\N	443	Bobby Jones, teeing off, 20 June 1930.	British Open Championship, Royal Liverpool Golf Club, Hoylake, England.	9	25	140	1	In 1930 Bobby Jones completed the "Grand Slam" of golf: winning the British Open, the US Open, the US Amateur, and the British Amateur in one year.	\N	\N	\N	\N	\N
1521	local	0500-123.tif	2006-07-13 00:00:00	\N	443	Leo Diegel, teeing off, 18 June 1930.	British Open Championship, Royal Liverpool Golf Club, Hoylake, England.	9	25	140	1	In 1930 Bobby Jones completed the "Grand Slam" of golf: winning the British Open, the US Open, the US Amateur, and the British Amateur in one year.	\N	\N	\N	\N	\N
1522	local	0500-124.tif	2006-07-13 00:00:00	\N	443	Leo Diegel, walking in the rain, 18 June 1930.	British Open Championship, Royal Liverpool Golf Club, Hoylake, England.	9	25	140	1	In 1930 Bobby Jones completed the "Grand Slam" of golf: winning the British Open, the US Open, the US Amateur, and the British Amateur in one year.	\N	\N	\N	\N	\N
1523	local	0500-125.tif	2006-07-13 00:00:00	\N	443	Horton Smith, 20 June 1930.	British Open Championship, Royal Liverpool Golf Club, Hoylake, England.	9	25	140	1	In 1930 Bobby Jones completed the "Grand Slam" of golf: winning the British Open, the US Open, the US Amateur, and the British Amateur in one year.	\N	\N	\N	\N	\N
1524	local	0500-126.tif	2006-07-13 00:00:00	\N	443	Bobby Jones and Cyril Tolley, leaving Waterloo, 27 June 1930.	\N	9	25	140	1	\N	\N	\N	\N	\N	\N
1525	local	0500-127.tif	2006-07-13 00:00:00	\N	443	Mr. and Mrs. Bobby Jones, [June 1930?]	\N	9	25	140	1	Bobby Jones with wife, Mary.	\N	\N	\N	\N	\N
1526	local	0500-128.tif	2006-07-13 00:00:00	\N	443	Walker Cup team, Atlanta terminal station, n.d.	\N	9	25	140	1	Jones represented the United States in the Walker Cup five times, and winning 9 of 10 matches. The Walker cup is a golf tournament consisting of teams of amateur players from the US, Great Britain, and Ireland. The Walker Cup match is played in alternative years in the US and Europe.	\N	\N	\N	\N	\N
1527	local	0500-129.tif	2006-07-13 00:00:00	\N	443	O.B. Keeler, Bobby Jones, and [?] standing next to Grand Canyon Sante Fe Limited train, n.d.	\N	9	25	140	1	Jones with devoted sportwriter and friend O.B. Keeler.	\N	\N	\N	\N	\N
1528	local	0500-130.tif	2006-07-13 00:00:00	\N	443	Mr. and Mrs. Bobby Jones, O.B. Keeler, and others next to Grand Canyon Sante Fr Limited train, n.d.	\N	9	25	140	1	Jones with devoted sportwriter and friend O.B. Keeler and wife, Mary.	\N	\N	\N	\N	\N
1529	local	0500-131.tif	2006-07-13 00:00:00	\N	443	Dinner party, Los Angeles, CA, ca. early 1930s.	\N	9	25	140	1	\N	\N	\N	\N	\N	\N
1530	local	0500-132.tif	2006-07-13 00:00:00	\N	443	Bobby Jones and Walter Huston, inscribed to Jones from Huston, ca. early 1930s.	\N	9	25	140	1	Inscription reads, "Dead Bob, the only excuse for these expressions is good acting. It was a pleasure to have been a associated with you, Walter Huston."	\N	\N	\N	\N	\N
1531	local	0500-133.tif	2006-07-13 00:00:00	\N	443	Bobby Jones and Robert W. Woodruff examining camera, ca. early 1930s.	\N	9	25	140	1	Jones with Robert W. Woodruff, chariman of the Coca-Cola company.	\N	\N	\N	\N	\N
1532	local	\N	2006-07-13 00:00:00	\N	826	Photograph of the Tuskegee School of Music faculty, 1934-1935	Alberta Lillian Sims; Frank L. Drye; Portia Washington Pittman; Catherine Moton Patterson; Orrin Suthern; Florence Cole Talbert; William Levi Dawson; Hazel Harrison; Emily C. Neely; George D. Rankin; Dorothy Sulton Chenault; Andrew F.  Rosemond	9	247	140	1	The faculty stands in a line on the steps of a building.	\N	\N	\N	\N	\N
1533	local	\N	2006-07-13 00:00:00	\N	826	Photograph of the Tuskegee Choir with Portia Washington Pittman, ca. 1934	\N	9	25	140	1	A formal portrait with the choir standing on a stage on risers.  William L. Dawson stands in the center.  Pittman stands on the far right.  Caption on reverse reads "Made December 16, 1932 in Logan Hall."	\N	\N	\N	\N	\N
1534	local	\N	2006-07-13 00:00:00	\N	826	Photograph of the Tuskegee Choir with Alberta Lillian Simms, 1935	\N	9	25	140	1	A formal portrait of the choir standing next to the Chapel at Tuskegee Institute.  Simms stands at the center.  The photograph was taken by P. H. Polk of Tuskegee's Photographic Division.	\N	\N	\N	\N	\N
1535	local	\N	2006-07-13 00:00:00	\N	826	Photograph of the Tuskegee Institute Orchestra, 23 Apri 1935	\N	9	25	140	1	Photograph of the orchestra rehearsing with Dawson.  Inscribed: "To Mr. William L. Dawson from Tuskegee Institute Orchestra 4/23/1935."  The photograph was taken by P. H. Polk of Tuskegee's Photographic Division.	\N	\N	\N	\N	\N
1536	local	\N	2006-07-13 00:00:00	\N	826	Photograph of the Tuskegee Choir, ca. 1935	\N	9	25	140	1	The choir stands on the steps of a building.  William L. Dawson stands at center.	\N	\N	\N	\N	\N
1538	local	\N	2006-07-13 00:00:00	\N	826	Photograph of the Tuskegee Choir and Orchestra at a performance of Hiawatha's Wedding Feast by Samuel Taylor Coleridge, 4 April 1936	Otis D. Wright, soloist; William L. Dawson conducting; Tuskegee Institute Chapel	9	25	140	1	The choir and orchestra are in place to perform.  Dawson stands at center and is facing the camera.  The photograph was taken by P. H. Polk of Tuskegee's Photographic Division.	\N	\N	\N	\N	\N
1539	local	\N	2006-07-13 00:00:00	\N	826	Photograph of the Tuskegee Choir performing on the NBC television show "Coke Time," December 1950	All smiles and refreshing	9	25	140	1	The choir traveled to New York City as guests of Coca Cola to appear in the "Coke Time" Christmas show on NBC.  The accompanying caption reads: "ALL SMILES AND 'REFRESHING'--The members of the Tuskegee Choir and right to left, Mr. Kendrix, Mr. Coste, Mr. Sussan and Mr. Dawson, were all smiles as the above more or less formal picture was made.  Fred Robbins, MC for 'Coke Time' and Perry Watkins, scenery designer for 'Coke Time' productions, were not available at the time the picture was made.  Mr. Watkins is a negro, with outstanding ability as a designer of television locations."	\N	\N	\N	\N	\N
1540	local	\N	2006-07-13 00:00:00	\N	826	Photograph of a Tuskegee Choir recording session at CBS, ca. 1955	\N	9	25	140	1	William Levi Dawson conducts the standing choir (wearing robes) in front of a live audience (seen only in a reflection).  The microphone and recording equipment is set up in front of them.  Photograph by Maury Garber.	\N	\N	\N	\N	\N
1542	local	\N	2006-07-13 00:00:00	\N	826	Photograph of the Tuskegee Choir performing Dvorak's "Stabat Mater" with the Atlanta Symphony Orchestra at the Tuskegee Institute, 9 April 1950	\N	9	25	140	1	The Choir was joined by 41 members of the Atlanta Symphany Orchestra.  William L. Dawson conducted.  This photograph was taken from the side of the stage.	\N	\N	\N	\N	\N
1543	local	\N	2006-07-13 00:00:00	\N	826	Photograph of the Chapel at Tuskegee Institute	\N	9	25	140	1	A photograph of the front of the chapel.  This image is part of a series of images of buildings on the Tuskegee campus.	\N	\N	\N	\N	\N
1544	local	\N	2006-07-13 00:00:00	\N	826	Photograph of the Tuskegee Choir, ca. 1955	\N	9	25	140	1	A formal portrait of the choir standing in Chapel at Tuskegee.  William L. Dawson stands in the center.  The choir is wearing robes.	\N	\N	\N	\N	\N
1545	local	\N	2006-07-13 00:00:00	\N	826	Photograph of the Tuskegee Singers during their tour of Philadelphia and New York, ca. 1920	\N	9	25	140	1	William L. Dawson was a member of the Tuskegee Singers.  The photograph was taken by C. M. Battey of Tuskegee's Photographic Division.	\N	\N	\N	\N	\N
1546	local	\N	2006-07-13 00:00:00	\N	826	Photograph of William Levi Dawson and Eliza Dawson [?]	\N	9	25	140	1	Formal portrait taken by the Quarles Studio in Tuskegee, Alabama.	\N	\N	\N	\N	\N
1547	local	\N	2006-07-13 00:00:00	\N	826	Photograph of William Levi Dawson and Ed Sullivan on the set of the Ed Sullivan Show, 6 April 1952	\N	9	25	140	1	Dawson and Sullivan shake hands on stage.	\N	\N	\N	\N	\N
1548	local	\N	2006-07-13 00:00:00	\N	826	Photograph of William Levi Dawson in student cadet uniform, ca. 1918	\N	9	25	140	1	Dawson stands casually with one hand in his pocket.  He is outdoors in front of a tree and near a building.	\N	\N	\N	\N	\N
1549	local	\N	2006-07-13 00:00:00	\N	826	Portrait of William Levi Dawson holding a trombone, ca. 1920	\N	9	25	140	1	In this formal portrait, Dawson stands facing left and holding his trombone with his right hand.  He is wearing a suit and tie.	\N	\N	\N	\N	\N
1550	local	\N	2006-07-13 00:00:00	\N	826	Portrait of William Levi Dawson, ca. 1920	\N	9	25	140	1	This photograph was taken by C. M. Battey of Tuskegee's Photographic Institute.	\N	\N	\N	\N	\N
1551	local	\N	2006-07-13 00:00:00	\N	826	Photograph of William Levi Dawson in marching band uniform with a trombone, ca. 1920	\N	9	25	140	1	Dawson is standing outside near some trees facing the camera.  He hold his trombone vertically in front of him with his right hand.	\N	\N	\N	\N	\N
1552	local	\N	2006-07-13 00:00:00	\N	826	Portrait of William Levi Dawson, ca. 1926	\N	9	25	140	1	Dawson sits in a chair in front of a neutral background.  The photograph was taken by P. H. Polk of Tuskegee's Photographic Division.	\N	\N	\N	\N	\N
1553	local	\N	2006-07-13 00:00:00	\N	826	Photograph of William Levi Dawson with two dogs, ca. 1931	\N	9	25	140	1	Dawson is outside in winter coat.  He is kneeling and looks down at two puppies he is holding in front of him.  The photograph was taken by P. H. Polk  of Tuskegee's Photographic Division.	\N	\N	\N	\N	\N
1554	local	\N	2006-07-13 00:00:00	\N	826	Portrait of William Levi Dawson, 21 November 1934	\N	9	25	140	1	This photograph was taken by Carl Van Vechten.  It is his negative number XVIgi9.	\N	\N	\N	\N	\N
1555	local	\N	2006-07-13 00:00:00	\N	826	Photograph of William Levi Dawson at a piano, ca. 1936	\N	9	25	140	1	Dawson is seated at a piano with a score open in front of him.  He has one hand on top of the piano and the other is on the keys.  He is turned toward the camera and smiling.  The photograph was taken by Springfield Acme Newspictures.	\N	\N	\N	\N	\N
1556	local	\N	2006-07-13 00:00:00	\N	826	Portrait of William Levi Dawson, ca. 1945	\N	9	25	140	1	\N	\N	\N	\N	\N	\N
1557	local	\N	2006-07-13 00:00:00	\N	826	Portrait of William Levi Dawson, ca. 1945	\N	9	25	140	1	\N	\N	\N	\N	\N	\N
1558	local	\N	2006-07-13 00:00:00	\N	826	Photograph of William Levi Dawson learning against a tree, ca. 1920	\N	9	25	140	1	In this informal snapshot, Dawson stands outside leaning against a small tree.  He is wearing a suit and tie and holds a hat in his left hand.  A gazebo is visible in the background.	\N	\N	\N	\N	\N
1559	local	\N	2006-07-13 00:00:00	\N	826	Photograph of William Levi Dawson rehearsing with unidentified voices, ca. 1950	\N	9	25	140	1	The performers are seated while Dawson stands in front of them conducting.	\N	\N	\N	\N	\N
1560	local	\N	2006-07-13 00:00:00	\N	826	Photograph of the Tuskegee Choir and Orchestra at a performance of "The Death of Minnehaha" at the Tuskegee Institute Chapel, 1 Apri 1939	Frank B. Harrison and Cleota Collins, soloists; William L. Dawson conducting	9	25	140	1	The choir and orchestra are in place to perform.  Dawson stands at center and is facing the camera.	\N	\N	\N	\N	\N
1561	local	\N	2006-07-13 00:00:00	\N	826	Announcement of 50th Anniversary Celebration of Tuskegee Normal and Industrial Institute, April 13, 1931	\N	1	25	140	1	A Festival of Negro Music, directed by Dawson	\N	\N	\N	\N	\N
1562	local	\N	2006-07-13 00:00:00	\N	826	Program of Tuskegee Institute Choir and Male Chorus at Carnegie Hall, February 8	\N	1	25	140	1	\N	\N	\N	\N	\N	\N
1563	local	\N	2006-07-13 00:00:00	\N	826	Inaugural Program of the Radio City Music Hall-opening December 27, 1932	\N	1	25	140	1	\N	\N	\N	\N	\N	\N
1564	local	\N	2006-07-13 00:00:00	\N	826	Program of Philadelphia Orchestra at Carnegie Hall, November 20, 1934	\N	1	25	140	1	Leopold Stokowski as conductor	\N	\N	\N	\N	\N
1565	local	\N	2006-07-13 00:00:00	\N	826	Program of Tuskegee Choir at the Tuskegee Institute from 1930s	\N	1	25	140	1	\N	\N	\N	\N	\N	\N
1566	local	\N	2006-07-13 00:00:00	\N	826	WAPI-The Voice of Alabama, Birmingham, from 1930s	\N	1	25	140	1	\N	\N	\N	\N	\N	\N
1567	local	0500-134.tif	2006-07-14 00:00:00	\N	443	Bobby Jones posing next to automobile, n.d.	\N	9	25	140	1	\N	\N	\N	\N	\N	\N
1568	local	0500-135.tif	2006-07-14 00:00:00	\N	443	Bobby Jones at play, n.d	\N	9	25	140	1	Inscribed from Frank E. [Bereshow?], "To Bobby Jones. With Best Wishes, Frank E. Bereshow [?]"	\N	\N	\N	\N	\N
1569	local	0500-136.tif	2006-07-14 00:00:00	\N	443	Bobby Jones, n.d.	\N	9	25	140	1	\N	\N	\N	\N	\N	\N
1570	local	0500-137.tif	2006-07-14 00:00:00	\N	443	Bobby Jones, Joseph E. Brown, and others on the green, during filming of "How I Play Golf", n.d.,	\N	9	25	140	1	Jones produced a series of short instructional golf films entitled, "How I Play Golf." O.B. Keeler wrote the narrations. In each ten-minute film, Jones comes across a struggling golf player and shows proper techniques.	\N	\N	\N	\N	\N
1571	local	0500-138.tif	2006-07-14 00:00:00	\N	443	Joseph E. Brown and Bobby Jones on the green, during filming of "How I Play Golf", n.d.	\N	9	25	140	1	Jones produced a series of short instructional golf films entitled, "How I Play Golf." O.B. Keeler wrote the narrations. In each ten-minute film, Jones comes across a struggling golf player and shows proper techniques.	\N	\N	\N	\N	\N
1572	local	0500-139.tif	2006-07-14 00:00:00	\N	443	Bobby Jones, World War II, n.d.	\N	9	25	140	1	\N	\N	\N	\N	\N	\N
1573	local	0500-140.tif	2006-07-14 00:00:00	\N	443	Bobby Jones, World War II, newspaper clipping photo, n.d.	\N	9	25	140	1	\N	\N	\N	\N	\N	\N
1574	local	0500-141.tif	2006-07-14 00:00:00	\N	443	Bobby Jones, cigarette photo card issued by Who's Who in Sport, Lambert and Butler, England, 1926.	\N	9	25	140	1	\N	\N	\N	\N	\N	\N
1575	local	0500-142.tif	2006-07-14 00:00:00	\N	443	Bobby Jones with Charles J. Wilkey, dean of Emory University Law School.	\N	9	25	140	1	Jones spent one year at Emory Law school before passing the bar exam.	\N	\N	\N	\N	\N
1576	local	0500-143.tif	2006-07-14 00:00:00	\N	443	Bobby Jones with Charles J. Hilkey, dean of Emory University Law School.	Emory Alumnus, March 1927, p. 11.	9	25	140	1	Jones spent one year at Emory Law school before passing the bar exam.	\N	\N	\N	\N	\N
1577	local	0500-144.tif	2006-07-14 00:00:00	\N	443	Bobby Jones, autographed photo, 21 Aug 1930.	\N	9	25	140	1	\N	\N	\N	\N	\N	\N
1578	local	0500-145.tif	2006-07-14 00:00:00	\N	443	Bobby Jones, Great Britain, 1930.	\N	9	25	140	1	In 1930 Bobby Jones completed the "Grand Slam" of golf: winning the British Open, the US Open, the US Amateur, and the British Amateur in one year.	\N	\N	\N	\N	\N
1579	local	0500-146.tif	2006-07-14 00:00:00	\N	443	Bobby Jones and Eric Fiddian, 1930.	British Amateur Championship, St. Andrews, Scotland.	9	25	140	1	In 1930 Bobby Jones completed the "Grand Slam" of golf: winning the British Open, the US Open, the US Amateur, and the British Amateur in one year.	\N	\N	\N	\N	\N
1580	local	0500-147.tif	2006-07-14 00:00:00	\N	443	Bobby Jones with Roger Wethered, 1930.	Walker Cup matches, Royal St. George's Golf Club, Sandwich, England.	9	25	140	1	Jones represented the United States in the Walker Cup five times, and winning 9 of 10 matches. The Walker cup is a golf tournament consisting of teams of amateur players from the US, Great Britain, and Ireland. The Walker Cup match is played in alternative years in the US and Europe.	\N	\N	\N	\N	\N
1581	local	0500-148.tif	2006-07-14 00:00:00	\N	443	Bobby Jones with wife and father, New York, 1930.	\N	9	25	140	1	In 1930 Bobby Jones completed the "Grand Slam" of golf: winning the British Open, the US Open, the US Amateur, and the British Amateur in one year.	\N	\N	\N	\N	\N
1582	local	0500-149.tif	2006-07-14 00:00:00	\N	443	Bobby Jones practicing iron shots, n.d.	\N	9	25	140	1	\N	\N	\N	\N	\N	\N
1583	local	0500-150.tif	2006-07-14 00:00:00	\N	443	Bobby Jones with unidentified, others.	\N	9	25	140	1	\N	\N	\N	\N	\N	\N
1584	local	0500-151.tif	2006-07-14 00:00:00	\N	443	Bobby Jones teeing off, n.d.	\N	9	25	140	1	\N	\N	\N	\N	\N	\N
1585	local	0500-152.tif	2006-07-14 00:00:00	\N	443	Bobby Jones playing out of the sand, 1923.	U.S. Open Championship, Inwood Country Club, Inwood, NJ.	9	25	140	1	In 1930 Bobby Jones completed the "Grand Slam" of golf: winning the British Open, the US Open, the US Amateur, and the British Amateur in one year.	\N	\N	\N	\N	\N
1586	local	0500-153.tif	2006-07-14 00:00:00	\N	443	Bobby Jones chipping, n.d.	\N	9	25	140	1	\N	\N	\N	\N	\N	\N
1587	local	0500-154.tif	2006-07-14 00:00:00	\N	443	Bobby Jones at the finish of his swing, n.d.	\N	9	25	140	1	\N	\N	\N	\N	\N	\N
1588	local	0500-155.tif	2006-07-14 00:00:00	\N	443	Bobby Jones laughing, n.d.	\N	9	25	140	1	\N	\N	\N	\N	\N	\N
1589	local	0500-156.tif	2006-07-14 00:00:00	\N	443	Bobby Jones and [?], n.d.	\N	9	25	140	1	\N	\N	\N	\N	\N	\N
1590	local	0500-157.tif	2006-07-14 00:00:00	\N	443	Bobby Jones and [?], n.d.	\N	9	25	140	1	\N	\N	\N	\N	\N	\N
1591	local	0500-158.tif	2006-07-14 00:00:00	\N	443	Bobby Jones teaching a young boy how to swing, n.d.	\N	9	25	140	1	\N	\N	\N	\N	\N	\N
1593	local	\N	2006-07-17 00:00:00	\N	0	The African Trader, By W.H.G Kingston	Illustration pg. 4	1	25	140	1	Caption reads, "meantime the shark, as if still eager to make us its prey, was swimming round and round the boat."	\N	Image for Carter G. Woodson exhibit	\N	\N	\N
1594	local	55	2006-07-17 00:00:00	\N	0	The Ivory Porter, the Cloth Porter, and Woman, in Usagara, p. 461	from The Lake Regions of Central Africa by Richard F. Burton	1	25	140	1	\N	\N	Image for Carter G. Woodson exhibit	\N	\N	\N
1595	local	68	2006-07-17 00:00:00	\N	0	Bantu Heritage, by H.P. Junod	\N	1	25	140	1	\N	\N	Image for Carter G. Woodson exhibit	\N	\N	\N
1596	local	67	2006-07-17 00:00:00	\N	0	Zimbabwe Ruins	Bantu Heritage, by H.P. Junod	1	25	140	1	\N	\N	Image for Carter G. Woodson exhibit	\N	\N	\N
1597	local	63	2006-07-17 00:00:00	\N	0	Gold Coast Native Institutions by Casely Hayford	Dedication page	1	25	140	1	\N	\N	Image for Carter G. Woodson exhibit	\N	\N	\N
1598	local	65a	2006-07-17 00:00:00	\N	0	J. Dahomey: An Ancient West African Kingdom Volume II.	Title plate	1	25	140	1	\N	\N	Image for Carter G. Woodson exhibit	\N	\N	\N
1599	local	65b	2006-07-17 00:00:00	2006-07-17 00:00:00	0	J. Dahomey: An Ancient West African Kingdom Volume II.	Title page illustration	1	25	140	1	\N	\N	Image for Carter G. Woodson exhibit	\N	\N	\N
1600	local	54a	2006-07-17 00:00:00	\N	0	West Africa before Europe by E.W. Blyden	Portrait of E.W. Blyden	1	25	140	1	\N	\N	Image for Carter G. Woodson exhibit	\N	\N	\N
1601	local	54b	2006-07-17 00:00:00	\N	0	West Africa before Europe by E.W. Blyden	Title page	1	25	140	1	\N	\N	Image for Carter G. Woodson exhibit	\N	\N	\N
1602	local	0500-159.tif	2006-07-17 00:00:00	\N	443	Bobby Jones and unidentified others, n.d.	\N	9	25	140	1	\N	\N	\N	\N	\N	\N
1603	local	0500-160.tif	2006-07-17 00:00:00	\N	443	Gallery shot, n.d.	\N	9	25	140	1	\N	\N	\N	\N	\N	\N
1604	local	0500-161.tif	2006-07-17 00:00:00	\N	443	Bobby Jones with Douglas Fairbanks, Jr.	\N	9	25	140	1	\N	\N	\N	\N	\N	\N
1605	local	0500-162.tif	2006-07-17 00:00:00	\N	443	Bobby Jones and unidentified cameramen, "How I Play Golf." 1931	\N	9	25	140	1	Jones produced a series of short instructional golf films entitled, "How I Play Golf." O.B. Keeler wrote the narrations. In each ten-minute film, Jones comes across a struggling golf player and shows proper techniques.	\N	\N	\N	\N	\N
1606	local	0500-163.tif	2006-07-17 00:00:00	\N	443	Cast and crew of "How I Play Golf," 1931	\N	9	25	140	1	Jones produced a series of short instructional golf films entitled, "How I Play Golf." O.B. Keeler wrote the narrations. In each ten-minute film, Jones comes across a struggling golf player and shows proper techniques.	\N	\N	\N	\N	\N
1607	local	0500-164.tif	2006-07-17 00:00:00	\N	443	Bobby Jones demonstrating his technique while O.B. Keeler works on the script, "How I Play Golf," 1931.	\N	9	25	140	1	Jones produced a series of short instructional golf films entitled, "How I Play Golf." O.B. Keeler wrote the narrations. In each ten-minute film, Jones comes across a struggling golf player and shows proper techniques.	\N	\N	\N	\N	\N
1608	local	0500-165.tif	2006-07-17 00:00:00	\N	443	Bobby Jones and unidentfiied others, "How I Play Golf"	\N	9	25	140	1	Jones produced a series of short instructional golf films entitled, "How I Play Golf." O.B. Keeler wrote the narrations. In each ten-minute film, Jones comes across a struggling golf player and shows proper techniques.	\N	\N	\N	\N	\N
1609	local	0500-166.tif	2006-07-17 00:00:00	\N	443	Bobby Jones and unidentified others, "How I Play Golf," 1931.	\N	9	25	140	1	Jones produced a series of short instructional golf films entitled, "How I Play Golf." O.B. Keeler wrote the narrations. In each ten-minute film, Jones comes across a struggling golf player and shows proper techniques.	\N	\N	\N	\N	\N
1610	local	0500-167.tif	2006-07-17 00:00:00	\N	443	Bobby Jones and [?] take a look at the script, "How I Play Golf," 1931.	\N	9	25	140	1	Jones produced a series of short instructional golf films entitled, "How I Play Golf." O.B. Keeler wrote the narrations. In each ten-minute film, Jones comes across a struggling golf player and shows proper techniques.	\N	\N	\N	\N	\N
1613	local	AssiaHat1.tif	2006-07-18 00:00:00	2006-07-18 00:00:00	0	\N	\N	6	25	140	1	\N	\N	\N	\N	\N	\N
1614	local	\N	2006-07-18 00:00:00	\N	584	Wevill, Assia, William Trevor, Jane Donaldson, Sean Gallagher on the Serpentine, ca. 1960	\N	9	25	140	1	Hughes began seeing the artist Assia Wevill during the fall of 1962 while he and Sylvia Plath were still married.	\N	\N	\N	\N	\N
1615	local	\N	2006-07-18 00:00:00	\N	584	Wevill, Assia, William Trevor, Jane Donaldson, Sean Gallagher on the Serpentine, ca. 1960	\N	9	\N	\N	1	Hughes began seeing the artist Assia Wevill during the fall of 1962 while he and Sylvia Plath were still married.	\N	\N	\N	\N	\N
1616	local	\N	2006-07-18 00:00:00	\N	584	Wevill, Assia, William Trevor, Jane Donaldson, Sean Gallagher on the Serpentine, ca. 1960	\N	9	\N	\N	1	Hughes began seeing the artist Assia Wevill during the fall of 1962 while he and Sylvia Plath were still married.	\N	\N	\N	\N	\N
1617	local	0500-168.tif	2006-07-20 00:00:00	\N	443	Bobby Jones standing by as the camera is being set up, "How I Play Golf," 1931.	\N	9	25	140	1	Jones produced a series of short instructional golf films entitled, "How I Play Golf." O.B. Keeler wrote the narrations. In each ten-minute film, Jones comes across a struggling golf player and shows proper techniques.	\N	\N	\N	\N	\N
1618	local	0500-169.tif	2006-07-20 00:00:00	\N	443	Bobby Jones receiving the Gorham bronze statue, California, 1931.	includes director George C. Marshall.	9	25	140	1	\N	\N	\N	\N	\N	\N
1619	local	0500-170.tif	2006-07-20 00:00:00	\N	443	Clipping of bobby Jones receiving the Gorham broze statue, 1931.	\N	9	25	140	1	\N	\N	\N	\N	\N	\N
1620	local	0500-171.tif	2006-07-20 00:00:00	\N	443	Bobby Jones posing with helmet and pipe, World War II, [1940s].	\N	9	25	140	1	\N	\N	\N	\N	\N	\N
1621	local	0500-172.tif	2006-07-20 00:00:00	\N	443	Bobby Jones and [?] in uniform, World War II, [1940s].	\N	9	25	140	1	\N	\N	\N	\N	\N	\N
1622	local	0500-173.tif	2006-07-20 00:00:00	\N	443	Bobby Jones and other officers at a USO show, montage of four photos, July 1944.	World War II, Cretteville (Normandy), France, July 1944.	9	25	140	1	\N	\N	\N	\N	\N	\N
1623	local	0500-174.tif	2006-07-20 00:00:00	\N	443	Bobby Jones and other officers at a USO show, July 1944.	World War II, Cretteville (Normandy), France.	9	25	140	1	\N	\N	\N	\N	\N	\N
1624	local	0500-175.tif	2006-07-20 00:00:00	\N	443	Bobby Jones and Robert Snodgrass, opening of campaign headquarters for President Dwight D. Eisenhower, n.d.	\N	9	25	140	1	\N	\N	\N	\N	\N	\N
1625	local	0500-176.tif	2006-07-20 00:00:00	\N	443	Bobby Jones and Robert Snodgrass, opening of campaign headquarters for President Dwight D. Eisenhower, n.d.	\N	9	25	140	1	\N	\N	\N	\N	\N	\N
1626	local	0500-177.tif	2006-07-20 00:00:00	\N	443	Bobby Jones, President Dwight D. Eisenhower, and unidentified others, 2 Sept. 1952	\N	9	25	140	1	\N	\N	\N	\N	\N	\N
1627	local	0500-178.tif	2006-07-20 00:00:00	\N	443	President Dwight D. Eisenhower and unidentified others, n.d.	\N	9	25	140	1	\N	\N	\N	\N	\N	\N
1628	local	0500-179.tif	2006-07-20 00:00:00	\N	443	Deer running out of the water, Lake Sinclair, GA, 1955.	From a fishing trip by Bobby Jones and Charlie Elliott.	9	25	140	1	\N	\N	\N	\N	\N	\N
1629	local	0500-180.tif	2006-07-20 00:00:00	\N	443	Deer swimming across the lake, Lake Sinclair, GA, 1955.	\N	9	25	140	1	From a fishing trip by Bobby Jones and Charlie Elliott.	\N	\N	\N	\N	\N
1630	local	0500-181.tif	2006-07-20 00:00:00	\N	443	Fish jumping out of the water, Lake Sinclair, GA, 1955.	\N	9	25	140	1	From a fishing trip by Bobby Jones and Charlie Elliott.	\N	\N	\N	\N	\N
1631	local	0500-182.tif	2006-07-20 00:00:00	\N	443	Bobby Jones releasing a fish, Lake Sinclair, GA, 1955.	\N	9	25	140	1	From a fishing trip by Bobby Jones and Charlie Elliott.	\N	\N	\N	\N	\N
1632	local	0500-183.tif	2006-07-20 00:00:00	\N	443	Bobby Jones, O.B. Keeler, and unidentified others, n.d.	Hunting trip, Leary, GA.	9	25	140	1	Jones with devoted sportwriter and friend O.B. Keeler.	\N	\N	\N	\N	\N
1633	local	0500-184.tif	2006-07-20 00:00:00	\N	443	Bobby Jones and [?], n.d.	Hunting trip, Leary, GA.	9	25	140	1	\N	\N	\N	\N	\N	\N
1634	local	0500-185.tif	2006-07-20 00:00:00	\N	443	Bobby Jones and [?], n.d.	Hunting trip, Leary, GA.	9	25	140	1	\N	\N	\N	\N	\N	\N
1635	local	0500-186.tif	2006-07-20 00:00:00	\N	443	Bobby Jones on horseback, n.d.	Hunting trip, Leary, GA.	9	25	140	1	\N	\N	\N	\N	\N	\N
1636	local	0500-187.tif	2006-07-20 00:00:00	\N	443	Bobby Jones signing roll of Burgesses, St. Andrews Freedom Ceremony, 1958.	\N	9	25	140	1	\N	\N	\N	\N	\N	\N
1637	local	0500-188.tif	2006-07-20 00:00:00	\N	443	Bobby Jones being interviewd by Leonard Mumford, Scottish Television.	Eisenhower Cup, 1958.	9	25	140	1	\N	\N	\N	\N	\N	\N
1638	local	0500-189.tif	2006-07-20 00:00:00	\N	443	Bobby Jones in golf cart with Cliff Roberts, watching play at the Masters, Augusta, GA, 1959.	\N	9	25	140	1	\N	\N	\N	\N	\N	\N
1639	local	0500-190.tif	2006-07-20 00:00:00	\N	443	Bobby Jones seated at desk with papers, 1959.	\N	9	25	140	1	\N	\N	\N	\N	\N	\N
1640	local	0500-191.tif	2006-07-20 00:00:00	\N	443	Charles R. Yates and others, posing with paintings of Bobby Jones by Thomas Stephens and President Dwight D. Eisenhower, [1950s?]	\N	9	25	140	1	\N	\N	\N	\N	\N	\N
1641	local	0500-192.tif	2006-07-20 00:00:00	\N	443	Bobby Jones and Vice President Richard M. Nixon, 1960, Bill Mark, photographer, Bobby Jones papers	\N	9	25	140	1	\N	\N	\N	\N	\N	\N
1642	local	0500-193.tif	2006-07-20 00:00:00	\N	443	Bobby Jones posing with book The American Golfer by Charles Price, 1964.	\N	9	25	140	1	\N	\N	\N	\N	\N	\N
1643	local	0500-194.tif	2006-07-20 00:00:00	\N	443	Bobby Jones in golf cart with Gene Sarazen, May 1966.	\N	9	25	140	1	Color snapshot	\N	\N	\N	\N	\N
1644	local	0500-195.tif	2006-07-20 00:00:00	\N	443	Joe Dey and other officials at memorial service for Bobby Jones, May 1972.	Parish Church of the Holy Trinity Church, St. Andrews.	9	25	140	1	Joe Dey is The former executive director of the USGA.	\N	\N	\N	\N	\N
1645	local	0500-196.tif	2006-07-20 00:00:00	\N	443	Bobby Jones with David Estes, head of Special Collections, Robert W. Woodruff Library.	Color snapshot, n.d.	9	25	140	1	Emory University.	\N	\N	\N	\N	\N
1646	local	0500-197.tif	2006-07-20 00:00:00	\N	443	Bobby Jones and O.B. Keeler posing with Grand Slam trophies, 1930.	\N	9	25	140	1	[from left] British Amateur, British Open, Walker Cup, U.S. Open, U.S. Amateur.	\N	\N	\N	\N	\N
1647	local	\N	2006-07-20 00:00:00	\N	826	Tuskegee Alumni News Briefs 2, No. 1 (August 1946), pg. 1	\N	1	247	140	1	The articles on this page are "Choir sings at the unveiling of Booker T. Washington Bust" and "Tiger Club Dinner big success."	\N	Only the first page was digitized.	\N	\N	\N
1648	local	\N	2006-07-20 00:00:00	\N	826	Program for The Death of Minnehaha from the Song of Hiawatha by Samuel Coleridge-Taylor, rendered by the Tuskegee Institute Choir and Orchestra, 1 April 1939	William L. Dawson, conducting; auspices Tuskegee Institute Entertainment Course	1	247	140	1	\N	\N	Only the cover was scanned.	\N	\N	\N
1649	local	\N	2006-07-20 00:00:00	\N	826	Portrait of H.T. Burleigh, 1933	\N	9	25	140	1	Burleigh inscribed this formal portrait as follows:  "Given to W. L. Dawson as an evidence of the regard and esteem of his friend.  N.Y. Jan. 1933  H.T. Burleigh."  This photograph was taken by Apeda Studios.	\N	\N	\N	\N	\N
1650	local	\N	2006-07-20 00:00:00	\N	826	Photograph of H.T. Burleigh playing the piano	\N	9	25	140	1	Burleigh is playing the piano and singing in what appears to be his home.  The photograph was taken from the side of the piano.	\N	\N	\N	\N	\N
1651	local	\N	2006-07-20 00:00:00	\N	826	Ticket stub for the National Colored All-Star baseball game, Comiskey Park, 13 August 1944	\N	15	247	140	1	\N	\N	\N	\N	\N	\N
1652	local	\N	2006-07-20 00:00:00	\N	826	Laundry receipt, Tuskegee Institute, 16 November 1942	\N	15	247	140	1	\N	\N	\N	\N	\N	\N
1653	local	\N	2006-07-20 00:00:00	\N	826	Photograph of William Levi Dawson with a copy of a recording of "Leopold Stokowski Conducts Negro Folk Symphony," ca. 1964	\N	9	25	140	1	In this snapshot, Dawson holds the record up for the camera so the title is visible.	\N	\N	\N	\N	\N
1655	local	0892-045	2006-07-20 00:00:00	\N	826	Portrait of Paul Lawrence Dunbar	\N	9	25	140	1	In this formal portrait, Dunbar rests his chin on his right hand.  His head and shoulders are visible, and he is looking down and to his right.  He is wearing a tuxedo.  The photograph was taken by C. M. Battey of Tuskegee's Photographic Division.	\N	\N	\N	\N	\N
1656	local	\N	2006-07-20 00:00:00	\N	826	Portrait of Carl Busch, June 1927	\N	9	25	140	1	Busch stands among some flowers.  A hat shades his face.  The print is inscribed as follows: "Wm L. Dawson with greetings from his old teacher Carl Busch.  Provo, Utah, June 1927."	\N	\N	\N	\N	\N
1657	local	\N	2006-07-20 00:00:00	\N	826	Photograph of a recording session of Negro Folk Symphony for Decca Records, 29 October 1963	\N	9	25	140	1	William L. Dawson and Leopold Stokowski stand next to each other reviewing the score.  The caption reads as follows:  "William Dawson (left), composer of the 'Negro Folk Symphony', discussing the score with Leopold Stokowski, whose recording of the work will be released by Decca Records next week."  The photograph was taken for Decca Records, Inc.	\N	\N	\N	\N	\N
1658	local	\N	2006-07-20 00:00:00	\N	826	Telegraph from Leopold Stokowski to William Levi Dawson, 1 November 1934	\N	1	247	140	1	Stokowski wrote after rehearsing the symphony that will later be titled the Negro Folk Symphony.  He asks Dawson for the title of the symphony and its three movements, noting "wish to give it title that will explain itself to listener."	\N	\N	\N	\N	\N
1659	local	\N	2006-07-20 00:00:00	\N	826	Reproduction of the opening night program for Radio City Music Hall, n.d.	\N	1	247	140	1	\N	\N	Only one page was scanned.	\N	\N	\N
1660	local	\N	2006-07-20 00:00:00	\N	826	News article about Choir's performance in Philadelphia	\N	1	247	140	1	"Applause Halts Symhony, Old Custom Broken"\r\n"Noted director forced to hold up performance of Dawson's work."	\N	NEED TO FIND THE ORIGINAL AND RESCAN IT.	\N	\N	\N
1661	local	\N	2006-07-20 00:00:00	\N	826	Photograph of William Levi Dawson and Aaron Douglass	\N	9	25	140	1	A snapshot of Dawson and Douglas standing together in front of a house. Both are dressed in suits.  Douglass holds a hat.	\N	\N	\N	\N	\N
1662	local	\N	2006-07-20 00:00:00	\N	826	Photograph of the Tuskegee Choir, ca. 1955	\N	9	25	140	1	William Levi Dawson conducts the choir on stage.  The choir is wearing robes and is standing on risers.	\N	\N	\N	\N	\N
1663	local	\N	2006-07-20 00:00:00	\N	826	Dunbar News 4, No. 19 (11 January 1933), pg. 1	\N	1	247	140	1	The headline reads, "The Tuskegee Choir at International Music Hall, Radio City, Rockefeller Center"	\N	CHECK TO SEE IF THIS IS THE ENTIRE ARTICLE.	\N	\N	\N
1664	local	\N	2006-07-20 00:00:00	\N	826	Photograph of William Levi Dawson at a piano, ca. 1936	\N	9	25	140	1	Dawson is seated at a piano with a score open in front of him.  He has one hand on top of the piano as he edits the score with a pen.  The photograph was taken by Springfield Acme Newspictures.	\N	\N	\N	\N	\N
1665	local	\N	2006-07-20 00:00:00	\N	826	Portrait of William Grant Still	\N	9	25	140	1	The photograph is inscribed as follows:  "To my friend Dawson, with best wishes.  William Grant Still."  Still sent the image on December 22, 1950, in response to a request from Dawson.	\N	\N	\N	\N	\N
1666	local	\N	2006-07-20 00:00:00	\N	826	Portrait of W. C. Handy	\N	9	25	140	1	Handy is seated and reading a book.  He has his head resting on his right hand while his left holds the book open.  He is wearing a suit and tie.  The image is inscribed to Dawson, and the inscription is dated July 19, 1955.  The photograph was copyrighted by George Maillard Kesslere, B. I.	\N	\N	\N	\N	\N
1667	local	\N	2006-07-20 00:00:00	\N	826	Portrait of Nathaniel Dett	\N	9	25	140	1	An inscription in white reads as follows:  "To my friend and colleague Mr. William L. Dawson with the compliments and best wishes of Nathaniel Dett July 24, 1936."	\N	\N	\N	\N	\N
1668	local	\N	2006-07-20 00:00:00	\N	826	Photograph of the Wayne State Glee Club, Detroit, Michigan, 14 March, 1970	\N	9	25	140	1	The photograph was taken during a performance or rehearsal.  William Levi Dawson was the guest conductor.	\N	\N	\N	\N	\N
1669	local	\N	2006-07-20 00:00:00	\N	826	Photograph of William Levi Dawson conducting an unknown chorus, 1979	\N	9	25	140	1	The photograph was taken during a performance or rehearsal.  Dawson seems to stand above the chorus.  The photograph was taken by Leandre Jackson.	\N	\N	\N	\N	\N
1670	local	\N	2006-07-20 00:00:00	\N	826	Photograph of William Levi Dawson receiving a Doctor of Laws from Lincoln University, 7 May 1978	\N	9	25	140	1	Dawson shakes the hand of Lincoln President Dr. Herman Branson as Dawson receives his hood.	\N	\N	\N	\N	\N
1671	local	\N	2006-07-20 00:00:00	\N	826	Letter from H.T. Burleigh to William Levi Dawson, 7 March 1921	\N	1	247	140	1	In the letter, Burleigh critiques on of Dawson's compositions.	\N	This image contains pages 1 and 2 of 3.	\N	\N	\N
1672	local	\N	2006-07-20 00:00:00	\N	826	Letter from H.T. Burleigh to William Levi Dawson, 7 March 1921	\N	1	247	140	1	In the letter, Burleigh critiques on of Dawson's compositions.	\N	This image contains page 3 of 3.	\N	\N	\N
1673	local	\N	2006-07-20 00:00:00	\N	826	Photograph of William Levi Dawson in New York City, ca. 1934	\N	9	25	140	1	Dawson stands on a busy street carrying a suitcase.  A hotel bell hop appears to be holding his suitcase.  Many other men stand behind Dawson and the bell hop, also holding coats and suitcases.  Behind the men is a bus.  The photograph was taken by Cecil Layne.	\N	\N	\N	\N	\N
1674	local	\N	2006-07-20 00:00:00	\N	826	Photograph of William Levi Dawson and others, Sancta Ignatia Basilicus, Loyola, Spain, [1956]	\N	9	25	140	1	Dawson and a large group stand on the steps of the basilica.  Dawson stands at center.  The photograph was taken by a photography studio in Madrid.  The name of the studio is stamped on the reverse of the photo but is not legible.	\N	\N	\N	\N	\N
1675	local	\N	2006-07-20 00:00:00	\N	826	Photograph of William Levi Dawson, Ambassador Lodge and others, Loyola, Spain, [1956]	\N	9	25	140	1	The group stands in front of an archway.  The photograph was taken by a photography studio in Madrid.  The name of the studio is stamped on the reverse of the photo but is not legible.	\N	\N	\N	\N	\N
1676	local	\N	2006-07-20 00:00:00	\N	826	Photograph of William Levi Dawson and Cecile N. Dawson at the Silver Rail Bar and Grill, New York City, August 1951	\N	9	25	140	1	This souvenir photograph shows the Dawsons seated at a table.  The caption on the verso reads: "Souvenir Photograph.  August 1951.  Silver Rail Bar & Grill Between 116 & 117 Streets on 8th Ave."	\N	\N	\N	\N	\N
1680	local	\N	2006-07-20 00:00:00	\N	826	Photograph of a recording session of the Negro Folk Symphony, [1963?]	\N	9	25	140	1	A shot from above of Leopold Stokowski directing a symphony, probably in 1963.  Dawson sits in the background, following along in the score.  The caption on the reverse reads: "Stokowski recording the Negro Folk Symphony."	\N	\N	\N	\N	\N
1681	local	\N	2006-07-20 00:00:00	\N	826	Photograph of a recording session of Negro Folk Symphony for Decca Records, 29 October 1963	\N	9	25	140	1	Leopold Stokowski, William Levi Dawson and George Jellinek together at the session.  Stokowski sits on the left behind a stand with the score on it.  He is raising a glass to his lips.  Dawson stands at center with a briefcase under his arm, holding his glasses in his hand.  He is looking at Jellinek.  Jellinek stands on the right with his hands on his hips.  The caption on the reverse of one copy of this image reads: "Leopold Stokowski, William Dawson, and George Jellinek at recording session of the Negro Folk Symphony."  The photograph was probably taken for Decca Records, Inc.	\N	\N	\N	\N	\N
1682	local	\N	2006-07-20 00:00:00	\N	826	Photograph of William Levi Dawson with tape recorder in Nigeria, West Africa, 1952	\N	9	25	140	1	Dawson stands outside with bags containing his recording equipment hanging over his shoulders.  He is wearing a pith helmet and his tie is loosened. The caption on the reverse reads:  "William Dawson with his tape recorder in Nigeria, West Africa, 1952."	\N	\N	\N	\N	\N
1683	local	\N	2006-07-20 00:00:00	\N	826	Panorama of the Tuskegee Institute campus	\N	9	25	140	1	\N	\N	\N	\N	\N	\N
1685	local	84	2006-07-21 00:00:00	\N	0	Moussa et Gi-gla, by L. Sonolet	Cover	1	25	140	1	\N	\N	\N	\N	\N	\N
1686	local	85	2006-07-21 00:00:00	\N	0	Moussa et Gi-gla, by L. Sonolet	Title page	1	25	140	1	\N	\N	\N	\N	\N	\N
1687	local	0500-198.tif	2006-07-21 00:00:00	\N	443	Bobby Jones and O.B. Keeler posing with Grand Slam trophies, 1930.	\N	9	25	140	1	[from left] British Open, British Amateur, U.S. Open.	\N	\N	\N	\N	\N
1688	local	0500-199.tif	2006-07-21 00:00:00	\N	443	O.B. Keeler, n.d.	\N	9	25	140	1	Jones's devoted sportwriter and friend O.B. Keeler.	\N	\N	\N	\N	\N
1689	local	0500-200.tif	2006-07-21 00:00:00	\N	443	Bobby Jones and Robert W. Woodruff shaking hands, n.d.	\N	9	25	140	1	Jones with Robert W. Woodruff, chairman of the Coca-Cola company.	\N	\N	\N	\N	\N
1690	local	0500-201.tif	2006-07-21 00:00:00	\N	443	Bobby Jones, Robert W. Woodruff, and Eddie Rickenbacker, n.d.	\N	9	25	140	1	Jones with Robert W. Woodruff, chairman of the Coca-Cola company.	\N	\N	\N	\N	\N
1691	local	0500-202.tif	2006-07-21 00:00:00	\N	443	Bobby Jones, Robert W. Woodruff, and [?], n.d.	\N	9	25	140	1	Jones with Robert W. Woodruff, chairman of the Coca-Cola company.	\N	\N	\N	\N	\N
1692	local	0500-203.tif	2006-07-21 00:00:00	\N	443	Coca-Cola executives at dinner party, n.d.	\N	9	25	140	1	\N	\N	\N	\N	\N	\N
1693	local	0500-204.tif	2006-07-21 00:00:00	\N	443	Coca-Cola executives at dinner party, n.d.	\N	9	25	140	1	\N	\N	\N	\N	\N	\N
1694	local	0500-205.tif	2006-07-21 00:00:00	\N	443	Bobby Jones with Princes Edward and Albert, and unidentified others, n.d.	\N	9	25	140	1	\N	\N	\N	\N	\N	\N
1695	local	0500-206.tif	2006-07-21 00:00:00	\N	443	Unidentified female, photo inscribed to Bobby Jones, n.d.	\N	9	25	140	1	\N	\N	\N	\N	\N	\N
1696	local	0500-207.tif	2006-07-21 00:00:00	\N	443	[?] Bowman, photo inscribed to Bobby Jones, n.d.	\N	9	25	140	1	\N	\N	\N	\N	\N	\N
1697	local	0500-208.tif	2006-07-21 00:00:00	\N	443	Bobby Jones and [?], n.d.	\N	9	25	140	1	\N	\N	\N	\N	\N	\N
1698	local	0500-209.tif	2006-07-21 00:00:00	\N	443	Bobby Jones addressing the ball for a mashie pitch, stereocard, n.d.	\N	9	25	140	1	\N	\N	\N	\N	\N	\N
1699	local	0500-210.tif	2006-07-21 00:00:00	\N	443	Bobby Jones wearing golf club jacket of the Augusta National Golf Club, n.d.	\N	9	25	140	1	\N	\N	\N	\N	\N	\N
1700	local	0500-211.tif	2006-07-21 00:00:00	\N	443	Bobby Jones wearing golf club jacket of the Augusta National Golf Club, n.d.	\N	9	25	140	1	\N	\N	\N	\N	\N	\N
1701	local	0500-212.tif	2006-07-21 00:00:00	\N	443	Bobby Jones standing in front of home on Northside Drive, Atlanta, n.d.	\N	9	25	140	1	\N	\N	\N	\N	\N	\N
1702	local	0500-213.tif	2006-07-21 00:00:00	\N	443	Golf clubs on exhibit, driver and one-iron, n.d.	\N	9	25	140	1	\N	\N	\N	\N	\N	\N
1703	local	0500-214.tif	2006-07-21 00:00:00	\N	443	Golf clubs on exhibit, one-iron, n.d.	\N	9	25	140	1	\N	\N	\N	\N	\N	\N
1704	local	0500-215.tif	2006-07-21 00:00:00	\N	443	British Amateur Championship, St. Andrews, Scotland, May 1930.	\N	9	25	140	1	In 1930 Bobby Jones completed the "Grand Slam" of golf: winning the British Open, the US Open, the US Amateur, and the British Amateur in one year.	\N	\N	\N	\N	\N
1705	local	0500-216.tif	2006-07-21 00:00:00	\N	443	St. Andrews, Scotland, n.d.	\N	9	25	140	1	Location of the British Open (The Open) golf tournament.	\N	\N	\N	\N	\N
1706	local	\N	2006-07-24 00:00:00	\N	\N	\N	\N	6	25	140	1	\N	\N	\N	\N	\N	\N
1707	local	\N	2006-07-24 00:00:00	\N	11	Arthur Houston Allen (cabinet photo),[ca. 1900s-1920s?]	\N	9	25	140	1	Reverse of photo: "Portrait Group & Architectural Photography. Ying Cheong. Canton Road. Shanghai. Views for sale. Extra Copies of this Picture can be had at any time by sending."	\N	\N	\N	\N	\N
1708	local	\N	2006-07-24 00:00:00	\N	11	Arthur Allen class picture (cabinet photo), Oxford College, 1886.	\N	9	25	140	1	\N	\N	\N	\N	\N	\N
1709	local	\N	2006-07-24 00:00:00	\N	11	Mary Louise (Turner) Allen with the Philomathean Society.	June 10, 1892	9	25	140	1	Albumin print, 7 x 8 1/2	\N	\N	\N	\N	\N
1710	local	\N	2006-07-24 00:00:00	\N	11	Ethel Margaret Allen (black and white, 5 x 6 3/4), Philadelphia, [ca. 1895-1910s?]	\N	9	25	140	1	\N	\N	\N	\N	\N	\N
1711	local	\N	2006-07-24 00:00:00	\N	11	Allen, Ethel Margaret (Turner) and Allen Richard Turner at YJA grave.	Shanghai, May 25, 1924	9	25	140	1	\N	\N	\N	\N	\N	\N
1712	local	\N	2006-07-24 00:00:00	\N	11	Allen, Ethel Margaret (Turner) and Allen Richard Turner at YJA grave.	Shanghai, May 25, 1924	9	25	140	1	\N	\N	\N	\N	\N	\N
1713	local	\N	2006-07-24 00:00:00	\N	11	Allen, Alice E. [possibly Wesleyan Class] (black and white, 13 x 10 1/8) [ca. 1885-1900s?]	\N	9	25	140	1	\N	\N	\N	\N	\N	\N
1714	local	\N	2006-07-25 00:00:00	\N	0	Poems of Cabin and Field by Paul Lawrence Dunbar, pg. 109	Man with crossed legs looking at banjo.	1	25	140	1	\N	\N	\N	\N	\N	\N
1715	local	\N	2006-07-25 00:00:00	\N	\N	Poems of Cabin and Field by Paul Lawrence Dunbar, pg. 110	Man standing with finger on banjo	1	25	140	1	\N	\N	\N	\N	\N	\N
1716	local	\N	2006-07-25 00:00:00	\N	0	Poems of Cabin and Field by Paul Lawrence Dunbar, pg. 112	Landscape scene	1	25	140	1	\N	\N	\N	\N	\N	\N
1717	local	\N	2006-07-25 00:00:00	\N	\N	Poems of Cabin and Field by Paul Lawrence Dunbar, pg. 114	Group shot with musicians	1	25	140	1	\N	\N	\N	\N	\N	\N
1718	local	\N	2006-07-25 00:00:00	\N	\N	Poems of Cabin and Field by Paul Lawrence Dunbar, pg. 116	Group of children	1	25	140	1	\N	\N	\N	\N	\N	\N
1719	local	\N	2006-07-25 00:00:00	\N	\N	Poems of Cabin and Field by Paul Lawrence Dunbar, pg. 118	Women sitting by door.	1	25	140	1	\N	\N	\N	\N	\N	\N
1720	local	\N	2006-07-25 00:00:00	\N	\N	Poems of Cabin and Field by Paul Lawrence Dunbar, pg. 120	Group outside next to house.	1	25	140	1	\N	\N	\N	\N	\N	\N
1721	local	\N	2006-07-25 00:00:00	\N	\N	Poems of Cabin and Field by Paul Lawrence Dunbar, pg. 122	Man sitting outside with banjo	1	25	140	1	\N	\N	\N	\N	\N	\N
1722	local	\N	2006-07-25 00:00:00	\N	0	Poems of Cabin and Field by Paul Lawrence Dunbar, pg. 124	Banjo	1	25	140	1	\N	\N	\N	\N	\N	\N
1723	local	\N	2006-07-25 00:00:00	\N	0	Rock Mountain (north side), from Georgia illustrated by William Carey Richards	\N	1	25	140	1	Drawn by J. Smilie from a sketch by T. Addison Richards. Engraved by Rawdon, Wright, Hatch & Smillie.	\N	\N	\N	\N	\N
1724	local	\N	2006-07-25 00:00:00	\N	0	Rock Mountain from Georgia illustrated by William Carey Richards	\N	1	25	140	1	Drawn by J. Smilie from a sketch by T. Addison Richards. Engraved by Rawdon, Wright, Hatch & Smillie.	\N	\N	\N	\N	\N
1725	local	\N	2006-07-24 00:00:00	\N	11	Allen, Mary Houston, ca. 1880, “45 years old”	\N	9	25	140	1	\N	\N	\N	\N	\N	\N
1726	local	\N	2006-07-24 00:00:00	\N	11	Allen, Mary Houston and children, ca. 1870s, Savannah, Ga.	\N	9	25	140	1	\N	\N	\N	\N	\N	\N
1727	local	\N	2006-07-25 00:00:00	\N	11	Allen, Mary Houston (black and white, 3 3/4 x 5 1/2), [1910s?]	\N	9	25	140	1	\N	\N	\N	\N	\N	\N
1728	local	\N	2006-07-26 00:00:00	\N	21	Photo of 38 GA regement in reunion Clarkston Sept 26, 1895.	\N	9	25	140	1	\N	\N	\N	\N	\N	\N
1729	local	\N	2006-07-26 00:00:00	\N	21	Group of Confederate officers of 38th GA	\N	9	25	140	1	\N	\N	\N	\N	\N	\N
1730	local	\N	2006-07-26 00:00:00	\N	11	Allen, Mary Houston (black and white, 5 x 8), Shanghai, [February 14, 1920]	\N	9	25	140	1	\N	\N	\N	\N	\N	\N
1731	local	\N	2006-07-26 00:00:00	\N	11	Allen, Mary Houston (black and white, 7 1/2 x 5 1/4), Shanghai, [ca. 1920s?]	\N	9	25	140	1	\N	\N	\N	\N	\N	\N
1732	local	\N	2006-07-26 00:00:00	\N	11	Allen, Mary Houston, possibly at dedication of Young John Allen church in Shanghai (black and white, 11 3/4 x 5, 11 3/4 x 8), [1900-1920s?]	\N	9	25	140	1	\N	\N	\N	\N	\N	\N
1733	local	\N	2006-07-26 00:00:00	\N	11	Allen, Mary Houston, possibly at dedication of Young John Allen church in Shanghai (black and white, 11 3/4 x 5, 11 3/4 x 8), [1900-1920s?]	\N	9	25	140	1	\N	\N	\N	\N	\N	\N
1734	local	\N	2006-07-26 00:00:00	\N	11	Allen, Young John, 1854	\N	9	25	140	1	\N	\N	\N	\N	\N	\N
1735	local	\N	2006-07-26 00:00:00	\N	11	Allen, Young John, 1854	\N	9	25	140	1	\N	\N	\N	\N	\N	\N
1736	local	\N	2006-07-26 00:00:00	\N	11	Allen, Young John, ca. 1870s, Savannah, Ga.	\N	9	25	140	1	\N	\N	\N	\N	\N	\N
1737	local	\N	2006-07-26 00:00:00	\N	11	Allen, Young John and his Chinese writers, Tsai and Yin, ca. 1900s [copy of original]	\N	9	25	140	1	\N	\N	\N	\N	\N	\N
1738	local	\N	2006-07-26 00:00:00	\N	11	Allen, Young John, Girl’s School, group of teachers and managers, ca. 1900s [copy of original]	\N	9	25	140	1	\N	\N	\N	\N	\N	\N
1739	local	\N	2006-07-26 00:00:00	\N	11	Allen, Young John in front of Prospect Church (Lone Oak, Georgia) with unidentified individual, 1900 February 7	\N	9	25	140	1	Inscription on reverse: "with love and kind wishes to Dr. Allen, from Marie Sewell"	\N	\N	\N	\N	\N
1740	local	\N	2006-07-26 00:00:00	\N	11	Allen, Young John, ca. 1906 [copy of original]	\N	9	25	140	1	\N	\N	\N	\N	\N	\N
1741	local	\N	2006-07-26 00:00:00	\N	11	Allen, Young John, ca. 1920s?	\N	9	25	140	1	\N	\N	includes negative	\N	\N	\N
1742	local	\N	2006-07-26 00:00:00	\N	11	Allen-Lee Memorial Church, Meriweather County, Georgia, 1938	\N	9	25	140	1	Written on reverse: "the new memorial Lee Allen church at Lone Oak GA, Merriweather County. On the same spot where old prospect church stood."	\N	\N	\N	\N	\N
1743	local	\N	2006-07-26 00:00:00	\N	11	Memorial marker of childhood home of YJA, Meriweather County, Georgia	\N	9	25	140	1	Written on reverse: "A boulder erected in memory of Dr. Young J. Allen on the same spot of ground where the house stood in which he was reared. The Howtchens farm in Merriweather GA, just -- miles from the Allen Lee memorial church."	\N	\N	\N	\N	\N
1744	local	\N	2006-07-26 00:00:00	\N	11	Young John Allen Home, Grantville, GA.	\N	9	25	140	1	Written on reverse: "this house was built by Dr. Young John Allen just after he gradualid (SIC) at Emory Univversity - Oxford GA. It was his intention to teach school at Grantville GA, and this house was to be a boys dormitory. In all these years there has not been a change made about it except the verandda columns. By the time the house was finished, Dr. Allen was called to China.	\N	\N	\N	\N	\N
1745	local	\N	2006-07-26 00:00:00	\N	11	Young John Allen Home, Grantville, GA.	\N	9	25	140	1	Written on reverse: "another view of the house Dr. Young J Allen built."	\N	\N	\N	\N	\N
1746	local	\N	2006-07-26 00:00:00	\N	11	YJ Allen Tree, Oxford, GA, 1915.	\N	9	25	140	1	\N	\N	\N	\N	\N	\N
1747	local	\N	2006-07-26 00:00:00	\N	11	Loehr, George R. with his class of the Huchow Middle School, Huchow, 1917	\N	9	25	140	1	\N	\N	\N	\N	\N	\N
1748	local	\N	2006-07-26 00:00:00	\N	11	Loehr, George R. in cemetary at Lone Oak, Georgia, n.d.	\N	9	25	140	1	\N	\N	\N	\N	\N	\N
1749	local	\N	2006-07-26 00:00:00	\N	11	Wan Kwoh Kung Pao (The Globe Magazine), various title pages	\N	9	25	140	1	1 of 5	\N	\N	\N	\N	\N
1750	local	\N	2006-07-26 00:00:00	\N	11	Wan Kwoh Kung Pao (The Globe Magazine), various title pages	\N	9	25	140	1	2 of 5	\N	\N	\N	\N	\N
1751	local	\N	2006-07-26 00:00:00	\N	11	Wan Kwoh Kung Pao (The Globe Magazine), various title pages	\N	9	25	140	1	3 of 5	\N	\N	\N	\N	\N
1752	local	\N	2006-07-26 00:00:00	\N	11	Wan Kwoh Kung Pao (The Globe Magazine), various title pages	\N	9	25	140	1	4 of 5	\N	\N	\N	\N	\N
1753	local	\N	2006-07-26 00:00:00	\N	11	Wan Kwoh Kung Pao (The Globe Magazine), various title pages	\N	9	25	140	1	5 of 5	\N	\N	\N	\N	\N
1754	local	\N	2006-07-26 00:00:00	\N	826	Photograph of William Levi Dawson, Governor George Wallace and others at the Alabama Music Hall of Fame reception, 6 December 1984	\N	9	25	140	1	Dawson, Wallace and others stand together near a Christmas tree.  The photo was inscribed by Wallace to Dawson as follows:  "To my friend Dr. Dawson--may God bless you.  Lisa T. Wallace."	\N	\N	\N	\N	\N
1755	local	\N	2006-07-26 00:00:00	\N	826	Photograph of Booker T. Washington speaking before a large audience	\N	9	25	140	1	Washington is on a podium.  He has his back to the camera, but he has turned so that his face is in profile.	\N	\N	\N	\N	\N
1756	local	\N	2006-07-26 00:00:00	\N	826	Photograph of a recording session of the Negro Folk Symphony, [1963?]	\N	9	25	140	1	An image of Leopold Stokowski directing during a recording session.  The shot is from above.	\N	\N	\N	\N	\N
1758	local	\N	2006-07-26 00:00:00	\N	826	Photograph of White Memo Hall at Tuskegee Institute	\N	9	25	140	1	A photograph of the front of the building.  The image is printed in reverse.  This image is part of a series of images of buildings on the Tuskegee campus.	\N	\N	\N	\N	\N
1759	local	\N	2006-07-26 00:00:00	\N	826	Photograph of the home of Dr. Booker T. Washington at Tuskegee Institute	\N	9	25	140	1	A photograph of the front of the building.  This image is part of a series of images of buildings on the Tuskegee campus.	\N	\N	\N	\N	\N
1760	local	\N	2006-07-26 00:00:00	\N	826	Photograph of Rockefeller Hall at Tuskegee Institute	\N	9	25	140	1	A photograph of the front of the building.  This image is part of a series of images of buildings on the Tuskegee campus.	\N	\N	\N	\N	\N
1764	local	\N	2006-07-26 00:00:00	\N	826	"Team work: Dr. Booker T. Washington's last Sunday evening talk to the teachers and students" [at Tuskegee Institute], 17 October 1915	Delivered in the Institute Chapel	1	247	140	1	\N	\N	Only selected pages were scanned.  This is the cover.	\N	\N	\N
1765	local	\N	2006-07-26 00:00:00	\N	826	"Team work: Dr. Booker T. Washington's last Sunday evening talk to the teachers and students" [at Tuskegee Institute], 17 October 1915	Delivered in the Institute Chapel	1	247	140	1	\N	\N	Only selected pages were scanned.  This is page 3.	\N	\N	\N
1766	local	\N	2006-07-26 00:00:00	\N	826	Program for the Officers of the Tuskegee Institute Cadet Corps' 29th Annual Entertainment, 10 May 1919	\N	1	247	140	1	\N	\N	Only selected pages were scanned.  This is the cover.	\N	\N	\N
1767	local	\N	2006-07-26 00:00:00	\N	826	Program for the Officers of the Tuskegee Institute Cadet Corps' 29th Annual Entertainment, 10 May 1919	\N	1	247	140	1	These pages list the Second Lieutenants; Non-Commissioned Staff; Band Organization; and Graduate Officers, Resident.	\N	Only selected pages were scanned.	\N	\N	\N
1769	local	\N	2006-07-26 00:00:00	\N	826	Photograph of Doc Cook and His Doctors of Syncopation at White City, Chicago, Illinois, 1927	\N	9	25	140	1	The band is in place on a stage in front of an ornate mosaic backdrop.  The band includes (left to right) Billy Butler, Don Pasquall, Joe Poston, Stanley Wilson, Wyatt Huston, Sterling Todd, Andrew Hillaire, Doc Cook, William Newton, William Levi Dawson, Charlie Allen, and Elwood Graham. They were performing at White City (63rd and South Parkway in Chicago.)  The photograph was taken by H.A. Atwell Studio.	\N	\N	\N	\N	\N
1770	local	\N	2006-07-26 00:00:00	\N	826	Program for the Annual Festival of the Civic Music Association of Chicago, 6 May 1928	\N	1	247	140	1	The Festival was held at Orchestra Hall and featured performances by the Civic Orchestra of Chicago and the Combined Children's Choruses of the Association.  This page lists the members of the Civic Orchestra of Chicago.	\N	Only page 12 was scanned.	\N	\N	\N
1771	local	\N	2006-07-26 00:00:00	\N	826	Program for Orfeo Lleidata La Violeta, Audicion de Las Obras de Tomas Luis de Victoria y Espirituales Negros, Viernes 3-11 Noche, [1956]	\N	1	482	140	1	\N	\N	Only the cover was scanned.	\N	\N	\N
1772	local	\N	2006-07-26 00:00:00	\N	826	Bulletin concerning the School of Music of the Tuskegee Normal and Industrial Institute, 1931-1932	November 1931	1	247	140	1	\N	\N	Only the cover was scanned.	\N	\N	\N
1773	local	\N	2006-07-26 00:00:00	\N	826	Cecil N. Dawson's notes concerning European travels, [1965?]	\N	1	247	140	1	Dawson wrote her notes on index cards.	\N	Only one side of one card was scanned.	\N	\N	\N
1774	local	\N	2006-07-26 00:00:00	\N	826	Photograph of the Tuskegee Choir performing on the NBC television show "Coke Time," December 1950	Eddie Fisher obliges with autographs following Christmas show	9	25	140	1	The accompanying caption reads: "EDDIE FISHER OBLIGES WITH AUTOGRAPHS FOLLOWING CHRISTMAS SHOW--The Tuskegee Choir and 'Coke Time's' Eddie Fisher were mutually attracted to each other during Choir's appearance as guests of Mr. Fisher on NBC-TV last December 25 and January 1.  Mr. Dawson and Moss H. Kendrix, Public Relations Counselor for the Coca-Cola Company, assist youthful star in filling his requests for autographs.  Choir travelled to New York City for the holiday appearance as guests of the Coca Cola Company, sponsor of 'Coke Time.'"	\N	\N	\N	\N	\N
1775	local	\N	2006-07-26 00:00:00	\N	826	Photograph of the Tuskegee Choir performing with [Leontyne Price], [20 March 1955]	\N	9	25	140	1	The choir is directed by William Levi Dawson. The choir and soloists are on a stage.	\N	\N	\N	\N	\N
1776	local	\N	2006-07-26 00:00:00	\N	826	Photograph of the ROTC and Commandant's Staff, Military Department, Tuskegee Institute, 1921	\N	9	25	140	1	Panoramic view of the ROTC and Commandant's staff seated in a semi-circle on the Tuskegee campus.  William Levi Dawson was a member of the ROTC.  The photograph was taken by C.M. Battey of Tuskegee's Photographic Division.	\N	\N	\N	\N	\N
1777	local	\N	2006-07-26 00:00:00	\N	826	Detroit Symphony Orchestra, Negro Folk Sympony CD	\N	16	25	140	1	\N	\N	\N	\N	\N	\N
1778	local	\N	2006-07-26 00:00:00	\N	826	St. Olaf Choir CD, Spirituals of William L Dawson	\N	16	25	140	1	\N	\N	\N	\N	\N	\N
1779	local	\N	2006-07-26 00:00:00	\N	826	Sheet music  for "Jesus Walked This Lonesome Valley," Warner Bros. Music, 1927	Spiritual by William L. Dawson	1	247	140	1	\N	\N	Only the cover was scanned.	\N	\N	\N
1780	local	56b	2006-07-27 00:00:00	\N	0	Barth's Exploration and Travels in Central Africa Illustrated, 1870	Musgu Chief	1	25	140	1	\N	\N	Image for Carter G. Woodson exhibit	\N	\N	\N
1781	local	56a	2006-07-27 00:00:00	\N	\N	Barth's Exploration and Travels in Central Africa Illustrated, 1870	Title page	1	25	140	1	\N	\N	Image for Carter G. Woodson exhibit	\N	\N	\N
1782	local	62	2006-07-27 00:00:00	\N	0	Expedition in Southern Africa by Captain W.C. Harris.	Title page	1	25	140	1	\N	\N	Image for Carter G. Woodson exhibit	\N	\N	\N
1783	local	\N	2006-07-27 00:00:00	\N	11	Chinese dignataries [including Marquis Ito, General Oyama, Admiral Ting & Viceroy Li Hung Chang]	\N	9	25	140	1	\N	\N	\N	\N	\N	\N
1784	local	\N	2006-07-27 00:00:00	\N	11	Chinese dignataries [including Marquis Ito, General Oyama, Admiral Ting & Viceroy Li Hung Chang]	Photo of a young woman	9	25	140	1	\N	\N	\N	\N	\N	\N
1785	local	\N	2006-07-27 00:00:00	\N	11	Chinese dignataries [including Marquis Ito, General Oyama, Admiral Ting & Viceroy Li Hung Chang]	unidentified man	9	25	140	1	\N	\N	\N	\N	\N	\N
1786	local	\N	2006-07-27 00:00:00	\N	11	Chinese dignataries [including Marquis Ito, General Oyama, Admiral Ting & Viceroy Li Hung Chang]	unidentified man	9	25	140	1	\N	\N	\N	\N	\N	\N
1787	local	\N	2006-07-27 00:00:00	\N	11	Chinese dignataries [including Marquis Ito, General Oyama, Admiral Ting & Viceroy Li Hung Chang]	unidentified man	9	25	140	1	\N	\N	\N	\N	\N	\N
1788	local	\N	2006-07-27 00:00:00	\N	11	Chinese dignataries [including Marquis Ito, General Oyama, Admiral Ting & Viceroy Li Hung Chang]	unidentified man	9	25	140	1	\N	\N	\N	\N	\N	\N
1789	local	94	2006-07-28 00:00:00	\N	0	Negro History Bulletin Vol 4 pp. 76-77	Hauling sugar cane, Haiti	1	25	140	1	\N	\N	Image for Carter G. Woodson exhibit	\N	\N	\N
1790	local	93	2006-07-28 00:00:00	\N	0	Negro History Bulletin Vol 4 p. 76-77	Carrying straw, Haiti	1	25	140	1	\N	\N	Image for Carter G. Woodson exhibit	\N	\N	\N
1791	local	74	2006-07-28 00:00:00	\N	0	Negro History Bulletin Vol 4 p. 33	Border on bottom	1	25	140	1	\N	\N	Image for Carter G. Woodson exhibit	\N	\N	\N
1792	local	53	2006-07-28 00:00:00	\N	0	Negro History Bulletin Vol 4 p. 28	Border on bottom	1	25	140	1	\N	\N	Image for Carter G. Woodson exhibit	\N	\N	\N
1793	local	91	2006-07-28 00:00:00	\N	0	Negro History Bulletin Vol 4 p. 13	The Blacksmith shop	1	25	140	1	\N	\N	Image for Carter G. Woodson exhibit	\N	\N	\N
1794	local	513	2006-07-28 00:00:00	\N	0	Negro History Bulletin Vol 4 p. 8	At Work in the African Home	1	25	140	1	\N	\N	Image for Carter G. Woodson exhibit	\N	\N	\N
1795	local	90	2006-07-28 00:00:00	\N	0	Negro History Bulletin Vol 4 p. 8	Why Study Africa?	1	25	140	1	\N	\N	Image for Carter G. Woodson exhibit	\N	\N	\N
1796	local	603	2006-07-28 00:00:00	\N	0	Negro History Bulletin Vol 2 p. 22	Annual meeting of the Association for the Study of Negro Life and History	1	25	140	1	\N	\N	Image for Carter G. Woodson exhibit	\N	\N	\N
1797	local	263	2006-07-28 00:00:00	\N	0	Negro History p. 42 Bulletin December 1939	Professions in Africa	1	25	140	1	\N	\N	Image for Carter G. Woodson exhibit	\N	\N	\N
1798	local	627	2006-07-28 00:00:00	\N	0	The Movable School goes to the Negro Farmer by Thomas Monroe Campbell	The Rural Negro Youth an the Home in Which He Lives Still Constitutes a Serious Problem	1	25	140	1	\N	\N	Image for Carter G. Woodson exhibit	\N	\N	\N
1799	local	629	2006-07-28 00:00:00	\N	0	The Rural Negro by Garter Godwin Woodson, p. 25	The Man Behind the Plow	1	25	140	1	\N	\N	Image for Carter G. Woodson exhibit	\N	\N	\N
1800	local	628	2006-07-28 00:00:00	\N	0	Black America by Scott Nearing	A young Alabama cotton picker	1	247	140	1	\N	\N	Image for Carter G. Woodson exhibit	\N	\N	\N
1801	local	\N	2006-07-31 00:00:00	\N	\N	Fuck You/ a magazine of the arts number 5 volume 5	scan of cover image	1	25	140	1	F.Y is a literary magazine founded in 1962 by the poet Ed Sanders. The magazine lasted 13 issues, printing work by such writers and artists as Allen Ginsberg, Gary Snyder, William Burroughs, Leroi Jones, Gregory Corso, Robert Creeley among others.	\N	\N	\N	\N	\N
1802	local	\N	2006-07-31 00:00:00	\N	0	Fine Clothes to the Jew by Langston Huges	Inscription page	1	25	140	1	Inscription reads: "To Nella Larsen - my Negro songs and poems - Langston Hughes; New York April 7, 1930."	\N	\N	\N	\N	\N
1803	local	\N	2006-07-31 00:00:00	\N	0	The Fuck You/ Quote of the Week	Sept 14, 1964	1	25	140	1	F.Y is a literary magazine founded in 1962 by the poet Ed Sanders. The magazine lasted 13 issues, printing work by such writers and artists as Allen Ginsberg, Gary Snyder, William Burroughs, Leroi Jones, Gregory Corso, Robert Creeley among others.	\N	\N	\N	\N	\N
1804	local	89	2006-07-31 00:00:00	\N	0	Froudacity: West India Fables Explained By J.J. Thomas	cover image	1	25	140	1	\N	\N	Image for Carter G. Woodson exhibit	\N	\N	\N
1805	local	264	2006-07-31 00:00:00	\N	0	Image of Toussain't Louverture for coloring by Lois Mailou Jones	\N	1	25	140	1	\N	\N	Image for Carter G. Woodson exhibit	\N	\N	\N
1806	local	231	2006-07-31 00:00:00	\N	0	Photo of Civil War Drummer boy in "A Brave Black Regiment"	Miles Moore p. 32	1	25	140	1	\N	\N	Image for Carter G. Woodson exhibit	\N	\N	\N
1807	local	251	2006-07-31 00:00:00	\N	0	Photo of Joseph T. Wilson in "A Brave Black Regiment," p. 256.	\N	1	25	140	1	\N	\N	Image for Carter G. Woodson exhibit	\N	\N	\N
1808	local	247a	2006-07-31 00:00:00	\N	0	Photo facing cover in "Twenty-Five Years History of the Grand Fountain of the United Order of the True Reformers, 1881-1905"	\N	1	25	140	1	Caption reads: "Rev. William Washington Browne. Founder of Grand Fountain, U.O.T.R. Born in Habersham County, GA. October 20, 1849. Died at Washington, D.C. December 21, 1897."	\N	Image for Carter G. Woodson exhibit	\N	\N	\N
1809	local	247b	2006-07-31 00:00:00	\N	0	"Twenty-Five Years History of the Grand Fountain of the United Order of the True Reformers, 1881-1905"	title page	1	25	140	1	\N	\N	Image for Carter G. Woodson exhibit	\N	\N	\N
1810	local	240	2006-07-31 00:00:00	\N	0	Photo of Paul Robeson in the Negro in Sports p. 99.	\N	9	25	140	1	\N	\N	Image for Carter G. Woodson exhibit	\N	\N	\N
1811	local	209	2006-07-31 00:00:00	\N	0	Image of foldout of 1921 chapter Dreer, Herman. 1940. History of the Omega Psi Phi Fraternity	\N	9	25	140	1	\N	\N	Image for Carter G. Woodson exhibit	\N	\N	\N
1812	local	210	2006-07-31 00:00:00	\N	0	Dreer, Herman. 1940. History of the Omega Psi Phi Fraternity	\N	1	25	140	1	\N	\N	Image for Carter G. Woodson exhibit	\N	\N	\N
1813	local	0892-101	2006-07-31 00:00:00	\N	826	Tuskegee Institue Sheet Music: "There Is a Balm in Gilead," 1967	\N	1	247	140	1	\N	\N	\N	\N	\N	\N
1815	local	0892-103	2006-07-31 00:00:00	\N	826	Sheet music for "Ezekiel Saw De Wheel (Mixed Chorus)," Music Press, Tuskegee Institute, 1962	\N	1	247	140	1	The music was arranged by William Levi Dawson. It was part of the Tuskegee Choir Series by Dawson.  This score is number T110.	\N	Only the cover was scanned.	\N	\N	\N
1816	local	0892-104	2006-07-31 00:00:00	\N	826	William L Dawson, "Talk about a Child that Do Love Jesus"	\N	6	25	140	1	\N	\N	\N	\N	\N	\N
1817	local	0892-105	2006-07-31 00:00:00	\N	826	Sheet music for "The Memphis Blues," Handy Brothers Music, 1954	by W. C. Handy	6	247	140	1	\N	\N	Only the cover was scanned.	\N	\N	\N
1818	local	0892-106	2006-07-31 00:00:00	\N	826	Sheet music for "Golden Brown Blues," W. C. Handy, 1926	Lyric by Langston Hughes; music by W. C. Handy	6	247	140	1	\N	\N	Only the cover was scanned.	\N	\N	\N
1819	local	0892-107	2006-07-31 00:00:00	\N	826	HT Burleigh, "Deep River," 1941	\N	6	247	140	1	\N	\N	\N	\N	\N	\N
1820	local	0892-109	2006-07-31 00:00:00	\N	826	Sheet music for "Ain'-a That Good News!" (Male), Music Press, Tuskegee Institute, 1965	arranged by William Levi Dawson	6	247	140	1	This work was part of the Tuskegee Choir Series.	\N	Only the cover and pages 2-3 were scanned.  This is pages 2-3.	\N	\N	\N
1821	local	0892-110	2006-07-31 00:00:00	\N	826	Sheet music for "Ain'-a That Good News!" (Male), Music Press, Tuskegee Institute, 1965	arranged by William Levi Dawson	6	247	140	1	This work was part of the Tuskegee Choir Series.	\N	Only the cover and pages 2-3 were scanned.  This is pages 2-3.	\N	\N	\N
1822	local	0892-111	2006-07-31 00:00:00	\N	826	Sheet music for "King Jesus Is A-Listening" (arranged for mixed voices,) H. T. FitzSimons Company, 1925	Arranged by William Levi Dawson	6	247	140	1	\N	\N	Only cover and first two pages were scanned.  This image is the cover.	\N	\N	\N
1823	local	0892-112	2006-07-31 00:00:00	\N	826	Sheet music for "King Jesus Is A-Listening" (arranged for mixed voices,) H. T. FitzSimons Company, 1925	Arranged by William Levi Dawson	6	247	140	1	\N	\N	Only cover and first two pages were scanned.  This image is the second two pages.	\N	\N	\N
1824	local	0892-113	2006-07-31 00:00:00	\N	826	Sheet music for "Juba," Clayton F. Summy Co., 1934	composed by R. Nathaniel	6	247	140	1	\N	\N	Only the cover was scanned.	\N	\N	\N
1825	local	0892-114	2006-07-31 00:00:00	\N	826	Sheet music for "The Dett Collection of Negro Spirituals-Fourth Group," Hall and McCreary, 1936	arranged and edited by R. Nathaniel Dett	6	247	140	1	\N	\N	Only the cover was scanned	\N	\N	\N
1827	local	\N	2006-08-01 00:00:00	\N	21	Portion of the flag from Hagood's brigade	\N	15	247	140	1	Hagood, Johnson, 1829 1898; an exchange of letters between Hagood and C. P. A. Brown upon Brown’s giving Hagood a portion of the flag of Hagood’s brigade; Brown to Hagood, Monticello, Fairfield Co., March 7, 1882; Hagood to Brown, Columbia, S. C., March 11, 1882; a portion of the flag is included	\N	\N	\N	\N	\N
1828	local	0892-115	2006-08-01 00:00:00	\N	826	Sheet music for "In Memoriam: The Colored Soldiers Who Died for Democracy," Delkas Music, 1943	By William Grant Still	6	247	140	1	\N	\N	Only the cover was scanned.	\N	\N	\N
1829	local	0892-116	2006-08-01 00:00:00	\N	\N	Folk songs of the American Negro ([John W. Work and Frederick J. Work, 1907])	edited by Frederick J. Work; introduction by John W. Work, Jr.	19	247	140	1	This cover of this copy has an ink stamp reading "copy has stamp: Standard Music Co., Nashville, Tenn."  Only the cover and pages 60-61 were scanned.  This image is pages 60-61.	\N	\N	\N	\N	\N
1830	local	0892-117	2006-08-01 00:00:00	\N	826	Program for the United Negro College Fund's United Negro College Convocation, (New York, New York,) 20 March 1955	\N	1	247	140	1	The Convocation took place in the Metropolitan Opera House.  It included performances by the Tuskegee Institute Concert Choir (William Levi Dawson, director) and Leontyne Price.  Benjamin Mays and John Foster Dulles gave addresses.	\N	Only the cover and pages [1-2] were scanned.  These are pages [1-2].	\N	\N	\N
1831	local	0892-118	2006-08-01 00:00:00	\N	826	Program for the United Negro College Fund's United Negro College Convocation, (New York, New York,) 20 March 1955	\N	1	25	140	1	The Convocation took place in the Metropolitan Opera House.  It included performances by the Tuskegee Institute Concert Choir (William Levi Dawson, director) and Leontyne Price.  Benjamin Mays and John Foster Dulles gave addresses.	\N	Only the cover and pages [1-2] were scanned.  This is the cover.	\N	\N	\N
1832	local	0892-119	2006-08-01 00:00:00	\N	826	Wedding portrait of Cecile Nicholson Dawson, 1 September 1935	\N	9	25	140	1	\N	\N	\N	\N	\N	\N
1833	local	0892-120	2006-08-01 00:00:00	\N	826	Commencement program and year-end bulletin for the Horner Institute of Fine Arts (Kansas City, Missouri,) 4-16 June 1923	Program of final events	1	247	140	1	William Levi Dawson received a certificate from the School of Music in 1923.	\N	Only the cover of the program was scanned.	\N	\N	\N
1834	local	0892-121	2006-08-01 00:00:00	\N	826	Program for "Hiawatha's Wedding Feast by Samuel Coleridge-Taylor," rendered by the Tuskegee Institute Choir and Orchestra, (Tuskegee Institute,)  4 April 1936	\N	1	247	140	1	William Levi Dawson conducted the choir and orchestra.  This image shows the two pages listing the members of the Institute Choir and the Institute Orchestra.	\N	Only selected pages were digitized.	\N	\N	\N
1835	local	0892-122	2006-08-01 00:00:00	\N	826	Program for "Hiawatha's Wedding Feast by Samuel Coleridge-Taylor," rendered by the Tuskegee Institute Choir and Orchestra, 4 April 1936	\N	1	247	140	1	William Levi Dawson conducted the choir and orchestra.	\N	Only selected pages were digitized.  This is the cover.	\N	\N	\N
1836	local	0892-123	2006-08-01 00:00:00	\N	826	Portrait of Cornella Lampton Dawson	\N	9	25	140	1	Dawson is seated in a chair with her hands in her lap.	\N	\N	\N	\N	\N
1837	local	0892-124	2006-08-01 00:00:00	\N	826	Autograph score for "A Negro Work Song for Orchestra" by William Levi Dawson	\N	6	247	140	1	The image includes the score for "Stewball" and Dawson's signature.	\N	The bottom half of page 1 and pages 2 and 3 were scanned.  This is a detail from page 1.	\N	\N	\N
1838	local	0892-125	2006-08-01 00:00:00	\N	826	Autograph score for "A Negro Work Song for Orchestra" by William Levi Dawson	\N	6	247	140	1	\N	\N	The bottom half of page 1 and pages 2 and 3 were scanned.   This is page 2.	\N	\N	\N
1839	local	0892-126	2006-08-01 00:00:00	\N	826	Autograph score for "A Negro Work Song for Orchestra" by William Levi Dawson	\N	6	25	140	1	\N	\N	The bottom half of page 1 and pages 2 and 3 were scanned.    This is page 3.	\N	\N	\N
1840	local	0892-127	2006-08-01 00:00:00	\N	961	Sheet music for "Negro Dance," Holt Publishing Co., 1921	by N. Douglas Holt	6	247	140	1	Only the first page was scanned.	\N	\N	\N	\N	\N
1841	local	0892-128	2006-08-01 00:00:00	\N	961	Sheet music for "Deep River," G. Schirmer Inc., 1913	arranged by H. T. Burleigh	6	247	140	1	Only pages 2-3 were scanned.	\N	\N	\N	\N	\N
1842	local	0892-129	2006-08-01 00:00:00	\N	826	Photograph of the Tuskegee Institute Choir in Carnegie Hall, January 1933	\N	9	25	140	1	The choir stands on risers.  William Levi Dawson, the director, stands at the center, facing the camera.  An inscription in white reads as follows: "New York City, January 1933, Tuskegee Institute Choir in Carnegie Hall.  Hail Radio City! 'Roxy'."  This photograph was taken by Apeda Studios.	\N	\N	\N	\N	\N
1843	local	0892-130	2006-08-01 00:00:00	\N	\N	Folk songs of the American Negro ([John W. Work and Frederick J. Work, 1907])	edited by Frederick J. Work; introduction by John W. Work, Jr.	19	247	140	1	This cover of this copy has an ink stamp reading "copy has stamp: Standard Music Co., Nashville, Tenn."  Only the cover and pages 60-61 were scanned.  This image is the cover.	\N	\N	\N	\N	\N
1844	local	0892-131	2006-08-01 00:00:00	\N	826	Portrait of Leopold Stokowski	\N	9	25	140	1	Stokowski is shown in profile.  The photograph is inscribed in white as follows:  "For William Dawson.  Leopold Stokowski."	\N	\N	\N	\N	\N
1845	local	0892-132	2006-08-01 00:00:00	\N	826	Autograph score for "Oh, My Little Soul Gwine Shine like a Star," arranged by William Levi Dawson	\N	6	247	140	1	This is the second theme of the first movement of the Negro Folk Symphony.  The image shows only a part of a larger page.  The page includes music for "Oh, My Little Soul Gwine Shine like a Star," "Hallalujah!," and "Oh Le'me Shine."	\N	The other two themes were scanned separately.	\N	\N	\N
1846	local	0892-133	2006-08-01 00:00:00	\N	826	Autograph score for "Hallalujah!," arranged by William Levi Dawson	\N	6	247	140	1	This is the first theme of the third movement of the Negro Folk Symphony.  The image shows only a part of a larger page.  The page includes music for "Oh, My Little Soul Gwine Shine like a Star," "Hallalujah!," and "Oh Le'me Shine."	\N	The other two themes were scanned separately.	\N	\N	\N
1847	local	0892-134	2006-08-01 00:00:00	\N	826	Autograph score for "Oh Le'me Shine," arranged by William Levi Dawson	\N	6	247	140	1	This is the second theme of the third movement of the Negro Folk Symphony.  The image shows only a part of a larger page.  The page includes music for "Oh, My Little Soul Gwine Shine like a Star," "Hallalujah!," and "Oh Le'me Shine."	\N	The other two themes were scanned separately.	\N	\N	\N
1848	local	0892-135	2006-08-01 00:00:00	\N	826	Sheet music for "Who is Dat Yonder?" Nephil Music, 1942	Arranged by Edward Boatner	6	247	140	1	\N	\N	Only the cover was scanned.	\N	\N	\N
1850	local	98a	2006-08-02 00:00:00	\N	0	Portrait of Rafael L. Trujillo from Reajuste de La Deuda Externa	\N	1	25	140	1	\N	\N	Image for Carter G. Woodson exhibit	\N	\N	\N
1851	local	98b	2006-08-02 00:00:00	\N	\N	T.P from Reajuste de La Deuda Externa by Rafael L. Trujillo	\N	1	25	140	1	\N	\N	Image for Carter G. Woodson exhibit	\N	\N	\N
1852	local	51	2006-08-02 00:00:00	\N	0	La Colonie du Niger by Maurice Abadie, 1927.	Cover	1	25	140	1	\N	\N	Image for Carter G. Woodson exhibit	\N	\N	\N
1853	local	80a	2006-08-02 00:00:00	\N	0	Senegambie et Guinee by M. Amedee Tardieu	title plate	1	25	140	1	\N	\N	Image for Carter G. Woodson exhibit	\N	\N	\N
1854	local	80b	2006-08-02 00:00:00	\N	0	Senegambie et Guinee by M. Amedee Tardieu	Plate 1: Lemaitre direxit St. Louis du Senegal	1	25	140	1	\N	\N	Image for Carter G. Woodson exhibit	\N	\N	\N
1855	local	80c	2006-08-02 00:00:00	\N	0	Senegambie et Guinee by M. Amedee Tardieu	Plate 4: Image of three men	9	25	140	1	\N	\N	Image for Carter G. Woodson exhibit	\N	\N	\N
1856	local	622	2006-08-02 00:00:00	\N	0	Image of Berea College's Howard Hall	From Berea College, Kentucky: An Interesting History p. 49	1	25	140	1	\N	\N	Image for Carter G. Woodson exhibit	\N	\N	\N
1857	local	201	2006-08-02 00:00:00	\N	0	Image of a Group of Pullman Porters	From Brazeal, Brailsford R. 1946: The Brotherhood of Sleeping Car Porters	1	25	140	1	\N	\N	Image for Carter G. Woodson exhibit	\N	\N	\N
1858	local	79	2006-08-02 00:00:00	\N	0	Archeologie de L'Afrique Noire by D.P. de Pedrals	Cover	1	25	140	1	\N	\N	Image for Carter G. Woodson exhibit	\N	\N	\N
1859	local	79	2006-08-02 00:00:00	\N	0	Archeologie de L'Afrique Noire by D.P. de Pedrals	inscription in French  to woodson from de Pedrals	6	25	140	1	\N	\N	Image for Carter G. Woodson exhibit	\N	\N	\N
1860	local	612	2006-08-02 00:00:00	\N	0	The Negro in Our History by Carter G. Woodson and Charles H. Wesley	Cover	1	25	140	1	\N	\N	Image for Carter G. Woodson exhibit	\N	\N	\N
1861	local	52	2006-08-02 00:00:00	\N	0	Batoula by Rene Maran, 1922.	Scan of paragraph on end of p. 13	1	25	140	1	\N	\N	Image for Carter G. Woodson exhibit	\N	\N	\N
1862	local	52	2006-08-02 00:00:00	\N	0	Batoula by Rene Maran, 1922.	End of paragraph which began on p. 13 onto p. 14	1	25	140	1	\N	\N	Image for Carter G. Woodson exhibit	\N	\N	\N
1863	local	3	2006-08-02 00:00:00	\N	0	Image of Book over on A Tribute for the Negro by Wilson Armistead, 1848.	\N	1	25	140	1	\N	\N	Image for Carter G. Woodson exhibit	\N	\N	\N
1864	local	4	2006-08-02 00:00:00	\N	0	"What the Negro Was Thinking During the Eighteenth Century"	The Journal of Negro History Bulletin Jan 1916, Vol/1. No. 1 pg. 49	1	25	140	1	\N	\N	Image for Carter G. Woodson exhibit	\N	\N	\N
1865	local	99a	2006-08-02 00:00:00	\N	0	Edwards' "West Indies," 1806 p. 257	\N	1	25	140	1	\N	\N	Image for Carter G. Woodson exhibit	\N	\N	\N
1866	local	0892-136	2006-08-02 00:00:00	\N	826	Halftone image of the Lincoln High School Orchestra from the Lincolnian (yearbook), 1926	\N	9	25	140	1	This image was printed in the Lincolnian in the Arts section.  William Levi Dawson directed the Orchestra.	\N	\N	\N	\N	\N
1867	local	0892-137	2006-08-02 00:00:00	\N	826	Lincolnian [yearbook], 1926	\N	1	247	140	1	The Lincolnian was the yearbook for Lincoln High School (Kansas City, Missouri).  William Levi Dawson was the director for both the band and orchestra.	\N	Only the page with entries for the Lincoln High School Band and Lincoln High School Orchestra was scanned.	\N	\N	\N
1868	local	0892-138	2006-08-02 00:00:00	\N	826	Autograph score of "Ain't that Good News," arranged by William Levi Dawson	\N	6	247	140	1	This score is part of a compositional sketchbook.	\N	No other scores from this composition book have been scanned.	\N	\N	\N
1869	local	0892-139	2006-08-02 00:00:00	\N	826	Sheet music for "Jump Back, Honey, Jump Back," Wunderlichs Piano Co., 1923	Words by Paul Lawrence Dunbar, music by William Levi Dawson	6	247	140	1	\N	\N	Only the cover was scanned.	\N	\N	\N
1870	local	0892-140	2006-08-02 00:00:00	\N	826	Sheet music for "Glory to the New Born King," Theodore Presser Co., 1929	arranged by John W. Work	6	247	140	1	Autograph inscription reads "Look this over see how yo [sic] like it.  W. Waley."	\N	Only the first page was scanned (numbered page 3).	\N	\N	\N
1871	local	0892-141	2006-08-02 00:00:00	\N	826	Program for the Redpath Chautauqua, 22-27 August 1921	\N	1	247	140	1	The program included a performance by the Tuskegee Institute Singers.	\N	Only the front cover was scanned.	\N	\N	\N
1872	local	0892-142	2006-08-02 00:00:00	\N	826	Program for "A Program of New Compositions by Mr. Weidig's Class," American Conservatory of Music, (Chicago, Illinois,) 28 May 1927	\N	1	247	140	1	William Levi Dawson was a member of Mr. Weidig's class and one of his compositions was performed.	\N	Only the cover was scanned.	\N	\N	\N
1873	local	0892-143	2006-08-02 00:00:00	\N	826	Autograph score for "Sonata No. I (A Major)" [for violin and piano], by William Levi Dawson	\N	6	247	140	1	\N	\N	Only the first two pages were scanned.  This is page 1.	\N	\N	\N
1874	local	0892-144	2006-08-02 00:00:00	\N	826	Autograph score for "Sonata No. I (A Major)" [for violin and piano], by William Levi Dawson	\N	6	247	140	1	\N	\N	Only the first two pages were scanned.  This is page 2.	\N	\N	\N
1875	local	0892-145	2006-08-02 00:00:00	\N	826	Bulletin concerning the School of Music of the Tuskegee Normal and Industrial Institute, 1931-1932	\N	1	247	140	1	\N	\N	Only pages 6-7 were scanned.	\N	\N	\N
1876	local	0892-146	2006-08-02 00:00:00	\N	826	Program, Inaugural Program of Radio City Music Hall, December 1932	\N	1	247	140	1	\N	\N	\N	\N	\N	\N
1877	local	0892-147	2006-08-02 00:00:00	\N	826	Program, Inaugural Program of Radio City Music Hall, December 1932	\N	1	247	140	1	\N	\N	\N	\N	\N	\N
1878	local	0892-148	2006-08-02 00:00:00	\N	826	Autograph score for "Jump Back, Honey, Jump Back," arranged by William Levi Dawson	\N	6	247	140	1	This score is part of a compositional sketchbook.	\N	No other scores from this composition book have been scanned.  All four pages of "Jump Back, Honey, Jump Back" were scanned.  This is page 1.	\N	\N	\N
1879	local	0892-149	2006-08-02 00:00:00	\N	826	Autograph score for "Jump Back, Honey, Jump Back," arranged by William Levi Dawson	\N	6	247	140	1	This score is part of a compositional sketchbook.	\N	No other scores from this composition book have been scanned.  All four pages of "Jump Back, Honey, Jump Back" were scanned.  This is page 2.	\N	\N	\N
1880	local	0892-150	2006-08-02 00:00:00	\N	826	Autograph score for "Jump Back, Honey, Jump Back," arranged by William Levi Dawson	\N	6	247	140	1	This score is part of a compositional sketchbook.	\N	No other scores from this composition book have been scanned.  All four pages of "Jump Back, Honey, Jump Back" were scanned.  This is page 3.	\N	\N	\N
1881	local	0892-151	2006-08-02 00:00:00	\N	826	Autograph score for "Jump Back, Honey, Jump Back," arranged by William Levi Dawson	\N	6	247	140	1	This score is part of a compositional sketchbook.	\N	No other scores from this composition book have been scanned.  All four pages of "Jump Back, Honey, Jump Back" were scanned.  This is page 4.	\N	\N	\N
1882	local	0892-152	2006-08-02 00:00:00	\N	826	Map of Northwest Africa - ERASE	\N	5	25	140	1	\N	\N	\N	\N	\N	\N
1883	local	0892-153	2006-08-02 00:00:00	\N	\N	Dust cover for The Drugstore Cat, by Ann Petry, 1949	\N	1	25	140	1	Only the front of the dust jacket was scanned.  This book was from the library of William Levi Dawson and includes an inscription to him from Petry.	\N	\N	\N	\N	\N
1884	local	0892-154	2006-08-02 00:00:00	\N	826	William Levi Dawson's bookplate	\N	15	354	140	1	The bookplate has two African drums on it.	\N	\N	\N	\N	\N
1885	local	0892-155	2006-08-02 00:00:00	\N	\N	Dust jacket for The Raven by Chancellor Williams (Dorrance, c1943)	\N	1	25	140	1	The spine and front cover were scanned as one image.  This book is from the library of William Levi Dawson.	\N	Woodruff Special Collections copy has dust jacket; bookplate of William L. Dawson; presentation inscription: For W.L. & Cecile, with best wishes & affectionate regards, Chancellor, Aug. 10th, 1961.	\N	\N	\N
1886	local	615	2006-08-03 00:00:00	\N	0	Image of article from "Birth of a Nation"	Woodson Library The Crisis October, 1916, pp. 295-96	1	25	140	1	\N	\N	Image for Carter G. Woodson exhibit	\N	\N	\N
1887	local	512	2006-08-03 00:00:00	\N	0	Lois Mailou Jones, image on card	Associated Publishers, Inc. 1996	1	25	140	1	\N	\N	Image for Carter G. Woodson exhibit	\N	\N	\N
1888	local	235	2006-08-03 00:00:00	\N	0	Major Charity E. Adams in the Negro History Bulletin June 1944 p. 195	\N	9	25	140	1	\N	\N	Image for Carter G. Woodson exhibit	\N	\N	\N
1889	local	236	2006-08-03 00:00:00	\N	0	Photo of Benjamin O. Davis in the Negro History Bulletin May, 1944 p. 171	\N	9	25	140	1	\N	\N	Image for Carter G. Woodson exhibit	\N	\N	\N
1890	local	237	2006-08-03 00:00:00	\N	0	Image of entire page in The Crisis July, 1911 p. 115	\N	1	25	140	1	\N	\N	Image for Carter G. Woodson exhibit	\N	\N	\N
1891	local	239	2006-08-03 00:00:00	\N	0	Photo of the Young Men's Christian Associatio Basketball Team at Washington D.C	The Crisis July, 1911 p. 119	9	25	140	1	\N	\N	Image for Carter G. Woodson exhibit	\N	\N	\N
1892	local	250	2006-08-03 00:00:00	\N	0	Cover of Aframerican Woman' Journal Summer and Fall 1940	\N	9	25	140	1	\N	\N	Image for Carter G. Woodson exhibit	\N	\N	\N
1893	local	\N	2006-08-03 00:00:00	\N	0	Image of Mary Eliza Church Terrell in 1989 Afro-American History Kit	\N	13	25	140	1	\N	\N	Image for Carter G. Woodson exhibit	\N	\N	\N
1894	local	248	2006-08-03 00:00:00	\N	0	Photo of Lucy Laney in the Journal of Negro History March 1942, p. 123	\N	9	25	140	1	\N	\N	Image for Carter G. Woodson exhibit	\N	\N	\N
1895	local	40	2006-08-03 00:00:00	\N	0	Image of Sojourner Truth in Ebony Images	\N	9	25	140	1	\N	\N	Image for Carter G. Woodson exhibit	\N	\N	\N
1896	local	234	2006-08-03 00:00:00	\N	0	Photo of "Women War Workers" in American Negro in the World War by Emmett J. Scott	\N	1	25	140	1	\N	\N	Image for Carter G. Woodson exhibit	\N	\N	\N
1897	local	616	2006-08-03 00:00:00	\N	0	Photograph of Woodrow in American Negro in the World War by Emmett J. Scott	\N	9	25	140	1	\N	\N	Image for Carter G. Woodson exhibit	\N	\N	\N
1898	local	219	2006-08-03 00:00:00	\N	\N	Photo of "Group of Colored Officers of the 368th Infantry"  in American Negro in the World War by Emmett J. Scott	\N	9	25	140	1	\N	\N	Image for Carter G. Woodson exhibit	\N	\N	\N
1899	local	41	2006-08-03 00:00:00	\N	0	Cover image of Joseph Wilson in the Black Phalanx	\N	9	25	140	1	\N	\N	Image for Carter G. Woodson exhibit	\N	\N	\N
1900	local	19	2006-08-03 00:00:00	\N	\N	Image of Martin Delaney in the Black Phalanx	\N	9	25	140	1	\N	\N	Image for Carter G. Woodson exhibit	\N	\N	\N
1901	local	232	2006-08-03 00:00:00	\N	0	Battle of Bunker Hill Peter Salem shooting the British Major Pitcairn	In The Black Phalanx	9	25	140	1	\N	\N	Image for Carter G. Woodson exhibit	\N	\N	\N
1902	local	409	2006-08-07 00:00:00	\N	0	Image of wooden comb, bowl and drinking cup, p. 3	From Negro Art, Music and Rhyme by Helen Adele Whiting	1	25	140	1	\N	\N	Image for Carter G. Woodson exhibit	\N	\N	\N
1903	local	411	2006-08-07 00:00:00	\N	\N	The African Likes to Make Things with Iron, p. 9	From Negro Art, Music and Rhyme by Helen Adele Whiting	1	25	140	1	\N	\N	Image for Carter G. Woodson exhibit	\N	\N	\N
1904	local	410	2006-08-07 00:00:00	\N	\N	Iron, p. 8	From Negro Art, Music and Rhyme by Helen Adele Whiting	1	25	140	1	\N	\N	Image for Carter G. Woodson exhibit	\N	\N	\N
1905	local	407	2006-08-07 00:00:00	\N	0	Inscription to Dr. Woodson from Rayfod W. Logan	From The Negro and the Post-War world: A Primer by Rayford W. Logan.	1	25	140	1	\N	\N	Image for Carter G. Woodson exhibit	\N	\N	\N
1906	local	401	2006-08-07 00:00:00	\N	0	A History of the Gold Coast by W.E.F. Ward	\N	1	25	140	1	\N	\N	Image for Carter G. Woodson exhibit	\N	\N	\N
1907	local	405	2006-08-07 00:00:00	\N	\N	Photo of Haile Selassie from Ethopia A Pawn in European Diplomacy	\N	1	25	140	1	\N	\N	Image for Carter G. Woodson exhibit	\N	\N	\N
1908	local	402	2006-08-07 00:00:00	\N	0	Bay-Tree Country by A.S. Cripps	\N	1	25	140	1	\N	\N	Image for Carter G. Woodson exhibit	\N	\N	\N
1909	local	404	2006-08-07 00:00:00	\N	0	Image from The Black Man's Burden by E.D. Morel	\N	1	25	140	1	\N	\N	Image for Carter G. Woodson exhibit	\N	\N	\N
1910	local	403	2006-08-07 00:00:00	\N	\N	Title page from The Black Man's Burden by E.D. Morel	\N	1	247	140	1	\N	\N	Image for Carter G. Woodson exhibit	\N	\N	\N
1911	local	204	2006-08-07 00:00:00	\N	0	Scan of First Congress of Negro Women Dec 1985 p. 10	\N	1	247	140	1	\N	\N	Image for Carter G. Woodson exhibit	\N	\N	\N
1912	local	217	2006-08-07 00:00:00	\N	\N	Scan of the founders at the National League of African American women p. 1	\N	1	247	140	1	\N	\N	Image for Carter G. Woodson exhibit	\N	\N	\N
1913	local	0892-156	2006-08-07 00:00:00	\N	\N	Dust jacket for The songs of our years : a study of Negro folk music, by Clyde Owen Jackson (Exposition Press, c1968)	\N	1	247	140	1	Front, spine, and back of dust jacket were scanned as one image.    This book is from the library of William Levi Dawson.	\N	Woodruff Special Collections copy has dust jacket; presentation inscription: To my friend, Mr. William L. Dawson, On behalf of the thousands of youngsters you inspired and guided over the years, may I say, simply, "Thanks".... Sincerely, Clyde Owen Jackson, 2/20/68, Houston, Texas.	\N	\N	\N
1914	local	0892-157front	2006-08-07 00:00:00	\N	826	Christmas Card from George Washington Carver to William Levi Dawson, 1934	\N	1	247	140	1	The illustration on the front cover includes a portrait of Carver.	\N	The front and inscription were scanned.  This is the front cover.	\N	\N	\N
1915	local	0892-157backtif	2006-08-07 00:00:00	\N	826	Christmas Card from George Washington Carver to William Levi Dawson, 1934	\N	1	247	140	1	The illustration on the front cover includes a portrait of Carver.	\N	The front and inscription were scanned.  This is the inscription.	\N	\N	\N
1916	local	DawsonMusic1	2006-08-07 00:00:00	\N	826	Negro Folk Symphony Movement 1, score	\N	6	25	140	1	\N	\N	MISSING - DELETE RECORD??	\N	\N	\N
1917	local	DawsonMusic2	2006-08-07 00:00:00	\N	826	Score for the Negro Folk Symphony, 1st movement [version 10], by Willliam Levi Dawson, [post-1956?]	\N	6	247	140	1	\N	\N	Only selected pages from this score were scanned.  This is page 16.	\N	\N	\N
1918	local	DawsonMusic3	2006-08-07 00:00:00	\N	826	Score for the Negro Folk Symphony, 1st movement [version 10], by Willliam Levi Dawson, [post-1956?]	\N	6	247	140	1	\N	\N	Only selected pages from this score were scanned.  This is page 17.	\N	\N	\N
1919	local	DawsonMusic4	2006-08-07 00:00:00	\N	826	Score for the Negro Folk Symphony, 2nd movement [version 10], by Willliam Levi Dawson, [post-1956?]	\N	6	247	140	1	\N	\N	Only selected pages from this score were scanned.  This is page 1.	\N	\N	\N
1920	local	DawsonMusic5	2006-08-07 00:00:00	\N	826	Score for the Negro Folk Symphony, 3rd movement [version 10], by Willliam Levi Dawson, [post-1956?]	\N	6	247	140	1	\N	\N	Only selected pages from this score were scanned.  This is page 9.	\N	\N	\N
1921	local	DawsonScore1	2006-08-07 00:00:00	\N	826	Score for the Negro Folk Symphony, 1st movement [version 10], by Willliam Levi Dawson, [post-1956?]	\N	6	247	140	1	\N	\N	Only selected pages from this score were scanned.  This is page 1.	\N	\N	\N
1922	local	DawsonScore2	2006-08-07 00:00:00	\N	826	Score for the Negro Folk Symphony, 1st movement [version 10], by Willliam Levi Dawson, [post-1956?]	\N	6	247	140	1	\N	\N	Only selected pages from this score were scanned.  This is page 19.	\N	\N	\N
1923	local	DawsonScore3	2006-08-07 00:00:00	\N	826	Score for the Negro Folk Symphony, 3rd movement [version 10], by Willliam Levi Dawson, [post-1956?]	\N	6	247	140	1	\N	\N	Only selected pages from this score were scanned.  This is page 26.	\N	\N	\N
1924	local	DawsonScore4	2006-08-07 00:00:00	\N	826	Score for the Negro Folk Symphony, 3rd movement [version 10], by Willliam Levi Dawson, [post-1956?]	\N	6	247	140	1	\N	\N	Only selected pages from this score were scanned.  This is page 29.	\N	\N	\N
1925	local	InvisibleMan	2006-08-07 00:00:00	\N	\N	The Invisible Man by Ralph Ellison (Random House, 1952)	\N	1	247	140	1	Only the title page inscribed by Ellison to William Levi Dawson was scanned.  The inscription reads: "For William L. Dawson, who, before I knew him, inspired me, and who after I came to Tuskegee taught me by example the discipline of the writer. With gratitude, Ralph Ellison, June 1953."  This book is from the library of William Levi Dawson.	\N	\N	\N	\N	\N
1926	local	ER-1	2006-08-07 00:00:00	\N	826	Photocopy of an autograph score for "God, I Need Thee" (hymn), words by Howard Thurman, music by William Levi Dawson	\N	6	247	140	1	A note on the score reads as follows: "November 1, 1943 @ Tuskegee Institute, Ala.  From the Chapel Bulletin, Vol. XI, No. 7, Sunday October 31, 1943."	\N	\N	\N	\N	\N
1928	local	ER-3	2006-08-07 00:00:00	\N	826	Photograph of the Tuskegee Choir performing on the NBC television show "Coke Time," December 1950	Tuskegee Choir appears with Eddie Fisher on "Coke Time"	9	25	140	1	The accompanying caption reads: "TUSKEGEE CHOIR APPEARS WITH EDDIE FISHER ON 'COKE TIME'--The Tuskegee Choir, under the direction of William L. Dawson, was guest on the Eddie Fisher 'Coke Time' TV shows, Christmas Day and again on New year's day.  Above, Mr. Dawson leads the Tuskegee Choir, as Eddie Fisher does one of his solos with the group.  Programs originated from NBC's Radio City."	\N	Image was scanned in grayscale.	\N	\N	\N
1929	local	dawson-ellington	2006-08-07 00:00:00	\N	826	Photograph of William Levi Dawson and Duke Ellington	\N	9	25	140	1	Dawson and Ellington stand next to each other in front of a building.  The photograph was taken by P. H. Polk, Photographic Division, Tuskegee Institute.	\N	\N	\N	\N	\N
1930	local	Dawsoninterview	2006-08-07 00:00:00	\N	826	Photograph of William Levi Dawson, ca. 1979	\N	9	25	140	1	Dawson is seated on a sofa.  He is wearing a dark colored turtle neck and a herring bone jacket.  He is speaking and has raised both hands to emphasize a point.  The photograph was taken by The Bulletin (Philadelphia, Pennsylvania.)	\N	\N	\N	\N	\N
1931	local	dawson-portrait	2006-08-07 00:00:00	\N	826	Portrait of William Levi Dawson, ca. 1960	\N	9	25	140	1	The photograph was taken by the Hawkins Studio, Tuskegee Institute.	\N	\N	\N	\N	\N
1934	local	238	2006-08-08 00:00:00	\N	0	Photo of the M Street High School Team	in The Crisis, July 1911 p. 115	1	247	140	1	\N	\N	Image for Carter G. Woodson exhibit	\N	\N	\N
1935	local	224	2006-08-08 00:00:00	2006-08-08 00:00:00	0	Image from Thommpson, John L. 1917 History and Views of Colored Officers.	\N	1	247	140	1	\N	\N	Image for Carter G. Woodson exhibit	\N	\N	\N
1936	local	604	2006-08-08 00:00:00	2006-08-08 00:00:00	0	The Most Romantic of Our History is That of the Negro	\N	1	247	140	1	\N	\N	Image for Carter G. Woodson exhibit	\N	\N	\N
1937	local	614	2006-08-08 00:00:00	2006-08-08 00:00:00	0	"Christmas in Georgia" The Crisis, December 1916, pp. 78-79	\N	1	247	140	1	\N	\N	Image for Carter G. Woodson exhibit	\N	\N	\N
1938	local	214	2006-08-09 00:00:00	2006-08-09 00:00:00	0	Inscription from HC Russell to Dr. Woodson	On Gibson, W.H. Sr. 1897. History of the United Brothers	1	247	140	1	\N	\N	Image for Carter G. Woodson exhibit	\N	\N	\N
1939	local	526	2006-08-09 00:00:00	2006-08-09 00:00:00	0	The New Floyd's Flowers Illustrated Stories	cover	1	247	140	1	\N	\N	Image for Carter G. Woodson exhibit	\N	\N	\N
1940	local	526	2006-08-09 00:00:00	2006-08-09 00:00:00	0	The New Floyd's Flowers Illustrated Stories - Image of Mrs. Alice Howard	p. 290	1	247	140	1	\N	\N	Image for Carter G. Woodson exhibit	\N	\N	\N
1941	local	528	2006-08-09 00:00:00	2006-08-09 00:00:00	0	The New Floyd's Flowers Illustrated Stories - Image of Mrs. Alice Howard	p. 291	1	247	140	1	\N	\N	Image for Carter G. Woodson exhibit	\N	\N	\N
1942	local	412	2006-08-09 00:00:00	2006-08-09 00:00:00	0	"Africa'' from Children of the Sun by Parker	\N	1	247	140	1	\N	\N	Image for Carter G. Woodson exhibit	\N	\N	\N
1943	local	277	2006-08-10 00:00:00	2006-08-10 00:00:00	0	The Negro in Our History by Carter G. Woodson	Scan of cover image	1	247	140	1	\N	\N	Image for Carter G. Woodson exhibit	\N	\N	\N
1944	local	277	2006-08-10 00:00:00	2006-08-10 00:00:00	0	The Negro in Our History by Carter G. Woodson	Scan of design on reverse of book	1	247	140	1	\N	\N	Image for Carter G. Woodson exhibit	\N	\N	\N
1945	local	277	2006-08-10 00:00:00	2006-08-10 00:00:00	0	The Negro in Our History by Carter G. Woodson	pg. 1: "confidential…"	1	247	140	1	\N	\N	Image for Carter G. Woodson exhibit	\N	\N	\N
1946	local	277	2006-08-10 00:00:00	2006-08-10 00:00:00	0	The Negro in Our History by Carter G. Woodson	Order form	1	247	140	1	\N	\N	Image for Carter G. Woodson exhibit	\N	\N	\N
1947	local	174 (Ephemera #4)	2006-08-10 00:00:00	2006-08-10 00:00:00	0	"Valuable books on the negro"	The publications of the ASSOCIATED PUBLISHERS, INC.	1	247	140	1	\N	\N	Image for Carter G. Woodson exhibit	\N	\N	\N
1948	local	172 (Ephemera #2)	2006-08-10 00:00:00	2006-08-10 00:00:00	0	The Negro in Our History - advertisment	\N	1	247	140	1	\N	\N	Image for Carter G. Woodson exhibit	\N	\N	\N
1949	local	173 (Ephemera #3)	2006-08-10 00:00:00	2006-08-10 00:00:00	0	The Negro in our History by Carter G. Woodson - advertisment	\N	1	247	140	1	\N	\N	Image for Carter G. Woodson exhibit	\N	\N	\N
1950	local	171 (Ephemera #1)	2006-08-11 00:00:00	2006-08-11 00:00:00	0	The Negro in Our History - advertisment - front	\N	1	247	140	1	\N	\N	Image for Carter G. Woodson exhibit	\N	\N	\N
1951	local	171 (Ephemera #1)	2006-08-11 00:00:00	2006-08-11 00:00:00	0	The Negro in our history - advertisment - reverse	\N	1	247	140	1	\N	\N	Image for Carter G. Woodson exhibit	\N	\N	\N
1952	local	197	2006-08-11 00:00:00	2006-08-11 00:00:00	0	The Journal of Negro History volume 1 1916 title page	\N	1	247	140	1	\N	\N	Image for Carter G. Woodson exhibit	\N	\N	\N
1953	local	198	2006-08-11 00:00:00	2006-08-11 00:00:00	0	The Journal of Negro History volume 1 January 1916 table of contents	\N	1	247	140	1	\N	\N	Image for Carter G. Woodson exhibit	\N	\N	\N
1954	local	275	2006-08-11 00:00:00	2006-08-11 00:00:00	0	A Statement of the Purpose, Growth and Prospects of the Journal of Negro History	\N	1	247	140	1	\N	\N	Image for Carter G. Woodson exhibit	\N	\N	\N
1955	local	276	2006-08-11 00:00:00	2006-08-11 00:00:00	0	An Appeal for more members for the Association for the study of Negro Life and History	\N	1	247	140	1	\N	\N	Image for Carter G. Woodson exhibit	\N	\N	\N
1956	local	278	2006-08-11 00:00:00	2006-08-11 00:00:00	0	Financial statement of The Association for the Study of Negro Life and History, inc.	\N	1	247	140	1	\N	\N	Image for Carter G. Woodson exhibit	\N	\N	\N
1957	local	279	2006-08-11 00:00:00	2006-08-11 00:00:00	0	A.S.N.L.H (blue)	\N	1	247	140	1	\N	\N	Image for Carter G. Woodson exhibit	\N	\N	\N
1958	local	280	2006-08-11 00:00:00	2006-08-11 00:00:00	0	Why You Should Subscribe to The Journal of Negro History	\N	1	247	140	1	\N	\N	Image for Carter G. Woodson exhibit	\N	\N	\N
1959	local	281	2006-08-11 00:00:00	2006-08-11 00:00:00	0	"Pictures of Distinguished Negroes" reverse	\N	1	247	140	1	\N	\N	Image for Carter G. Woodson exhibit	\N	\N	\N
1960	local	281	2006-08-11 00:00:00	2006-08-11 00:00:00	0	"Pictures of Distinguished Negroes" reverse	\N	1	247	140	1	\N	\N	Image for Carter G. Woodson exhibit	\N	\N	\N
1961	local	281	2006-08-11 00:00:00	2006-08-11 00:00:00	0	"Mary McLeod Bethune," Educator and Public Servant	\N	1	247	140	1	\N	\N	Image for Carter G. Woodson exhibit	\N	\N	\N
1962	local	282	2006-08-11 00:00:00	2006-08-11 00:00:00	0	Gwendolyn Brooks with others	\N	9	247	140	1	\N	\N	Image for Carter G. Woodson exhibit	\N	\N	\N
1963	local	283	2006-08-11 00:00:00	2006-08-11 00:00:00	0	Casely Hayford: An African Native Barrister on the Gold Coast	\N	1	247	140	1	\N	\N	Image for Carter G. Woodson exhibit	\N	\N	\N
1964	local	284	2006-08-11 00:00:00	2006-08-11 00:00:00	0	Program of the Annual Meeting of the Association for the Study of Negro Life and History	\N	1	247	140	1	\N	\N	Image for Carter G. Woodson exhibit	\N	\N	\N
1965	local	285	2006-08-11 00:00:00	2006-08-11 00:00:00	0	"Miseducation," flyer.	\N	1	247	140	1	\N	\N	Image for Carter G. Woodson exhibit	\N	\N	\N
1966	local	286	2006-08-11 00:00:00	2006-08-11 00:00:00	0	"Why don't you join..." flyer	\N	1	25	140	1	\N	\N	Image for Carter G. Woodson exhibit	\N	\N	\N
1967	local	188	2006-08-15 00:00:00	2006-08-15 00:00:00	0	Twelve Negro Spirituals by William Grant Still	Cover	1	247	140	1	\N	\N	Image for Carter G. Woodson exhibit	\N	\N	\N
1968	local	182	2006-08-15 00:00:00	2006-08-15 00:00:00	0	Racial Integrity by Arthur A. Schomburg	Title Page	1	247	140	1	\N	\N	Image for Carter G. Woodson exhibit	\N	\N	\N
1969	local	183	2006-08-15 00:00:00	2006-08-15 00:00:00	0	The Negro Woman by Thomas Nelson	Cover	1	247	140	1	\N	\N	Image for Carter G. Woodson exhibit	\N	\N	\N
1970	local	1970	2006-08-15 00:00:00	2006-08-15 00:00:00	0	As it is by Mamie Jordan Carver	Cover	1	247	140	1	\N	\N	Image for Carter G. Woodson exhibit	\N	\N	\N
1971	local	185	2006-08-15 00:00:00	2006-08-15 00:00:00	0	Simple Formulae For Measuring Atoms, Their Speed, and the Speed of Light By Lucien V. Alexis, Sr.	Cover	1	247	140	1	\N	\N	Image for Carter G. Woodson exhibit	\N	\N	\N
1972	local	185	2006-08-15 00:00:00	2006-08-15 00:00:00	0	Simple Formulae For Measuring Atoms, Their Speed, and the Speed of Light By Lucien V. Alexis, Sr.	Reverse	1	247	140	1	\N	\N	Image for Carter G. Woodson exhibit	\N	\N	\N
1973	local	186	2006-08-15 00:00:00	2006-08-15 00:00:00	0	Papers of the American Negro Academy	cover	1	247	140	1	\N	\N	Image for Carter G. Woodson exhibit	\N	\N	\N
1974	local	187	2006-08-15 00:00:00	2006-08-15 00:00:00	0	Quotations of Booker T. Washingson compiled by E. Davidson Washington	cover	1	247	140	1	\N	\N	Image for Carter G. Woodson exhibit	\N	\N	\N
1975	local	288	2006-08-15 00:00:00	2006-08-15 00:00:00	0	The Crisis April 1911	cover	1	247	140	1	\N	\N	Image for Carter G. Woodson exhibit	\N	\N	\N
1976	local	289	2006-08-15 00:00:00	2006-08-15 00:00:00	0	Aya Bombe! Revue Mensuelle	cover	1	262	140	1	\N	\N	Image for Carter G. Woodson exhibit	\N	\N	\N
1977	local	193	2006-08-15 00:00:00	2006-08-15 00:00:00	0	Pulse November 1947	cover	1	247	140	1	\N	\N	Image for Carter G. Woodson exhibit	\N	\N	\N
1978	local	195	2006-08-15 00:00:00	2006-08-15 00:00:00	0	Minutes of the National Association of Colored Women Incorporated	cover	1	247	140	1	\N	\N	Image for Carter G. Woodson exhibit	\N	\N	\N
1979	local	287	2006-08-15 00:00:00	2006-08-15 00:00:00	0	PIC Right On! Volume 1, No. 2.	cover	1	247	140	1	\N	\N	Image for Carter G. Woodson exhibit	\N	\N	\N
1980	local	194	2006-08-15 00:00:00	2006-08-15 00:00:00	0	The Crisis volume two July 1911	Cover	17	247	140	1	\N	\N	Image for Carter G. Woodson exhibit	\N	\N	\N
1982	local	233	2006-08-15 00:00:00	2006-08-15 00:00:00	0	The Negro History Bulletin October 1942	Cover	17	247	140	1	\N	\N	Image for Carter G. Woodson exhibit	\N	\N	\N
1983	local	43	2006-08-16 00:00:00	2006-08-16 00:00:00	0	The Slave Trade in America - p. 311	"He applied the lash not only to make them eat, but to make them sing"	1	247	140	1	\N	\N	Image for Carter G. Woodson exhibit	\N	\N	\N
1984	local	44	2006-08-16 00:00:00	2006-08-16 00:00:00	0	The Slave Trade in America - p. 309	"She… walked to the ship's side, and … dropped the body into the sea."	1	247	140	1	\N	\N	Image for Carter G. Woodson exhibit	\N	\N	\N
1985	local	280	2006-08-16 00:00:00	2006-08-16 00:00:00	0	Dubois Portrait	\N	9	547	140	1	\N	\N	Image for Carter G. Woodson exhibit	\N	\N	\N
1986	local	\N	2006-08-16 00:00:00	2006-08-16 00:00:00	826	Reprint of "Interpretation of the Religious Folk-Songs of the American Negro," by William L. Dawson, [1955]	\N	1	247	140	1	This article was originally published in the March 1955 issue of Etude.	\N	This is page 1 of 2.	\N	\N	\N
1987	local	\N	2006-08-16 00:00:00	2006-08-16 00:00:00	826	Reprint of "Interpretation of the Religious Folk-Songs of the American Negro," by William L. Dawson, [1955]	\N	1	247	140	1	This article was originally published in the March 1955 issue of Etude.	\N	This is page 2 of 2.	\N	\N	\N
1988	local	\N	2006-08-16 00:00:00	2006-08-16 00:00:00	826	Conference on Afroamerican music and the historically black college: a reappraisal (front)	\N	1	247	140	1	\N	\N	\N	\N	\N	\N
1989	local	\N	2006-08-16 00:00:00	2006-08-16 00:00:00	826	Conference on Afroamerican music and the historically black college: a reappraisal (reverse)	\N	1	247	\N	1	\N	\N	\N	\N	\N	\N
1990	local	\N	2006-08-16 00:00:00	2006-08-16 00:00:00	826	Forever Thine by William L. Dawson	1/5	6	247	140	1	\N	\N	\N	\N	\N	\N
1991	local	\N	2006-08-16 00:00:00	2006-08-16 00:00:00	826	Forever Thine by William L. Dawson	2/5	6	247	140	1	\N	\N	\N	\N	\N	\N
1992	local	\N	2006-08-16 00:00:00	2006-08-16 00:00:00	826	Forever Thine by William L. Dawson	3/5	6	247	140	1	\N	\N	\N	\N	\N	\N
1993	local	\N	2006-08-16 00:00:00	2006-08-16 00:00:00	826	Forever Thine by William L. Dawson	4/5	6	247	140	1	\N	\N	\N	\N	\N	\N
1994	local	\N	2006-08-16 00:00:00	2006-08-16 00:00:00	826	Forever Thine by William L. Dawson	5/5	6	247	140	1	\N	\N	\N	\N	\N	\N
1995	local	\N	2006-08-16 00:00:00	2006-08-16 00:00:00	826	Tuskegee Institute Music Department, 1933-1947 (1933 account of Radio City Music Hall event) pg 1	1/14	1	247	140	1	\N	\N	\N	\N	\N	\N
1996	local	\N	2006-08-16 00:00:00	2006-08-16 00:00:00	826	Tuskegee Institute Music Department, 1933-1947 (1933 account of Radio City Music Hall event) pg 2	2/14	1	247	140	1	\N	\N	\N	\N	\N	\N
1997	local	\N	2006-08-16 00:00:00	2006-08-16 00:00:00	826	Tuskegee Institute Music Department, 1933-1947 (1933 account of Radio City Music Hall event) pg 3	3/14	1	247	140	1	\N	\N	\N	\N	\N	\N
1998	local	\N	2006-08-16 00:00:00	2006-08-16 00:00:00	826	Tuskegee Institute Music Department, 1933-1947 (1933 account of Radio City Music Hall event) pg 4	4/14	1	247	140	1	\N	\N	\N	\N	\N	\N
1999	local	\N	2006-08-16 00:00:00	2006-08-16 00:00:00	826	Tuskegee Institute Music Department, 1933-1947 (1933 account of Radio City Music Hall event) pg 5	5/14	1	247	140	1	\N	\N	\N	\N	\N	\N
2000	local	\N	2006-08-16 00:00:00	2006-08-16 00:00:00	826	Tuskegee Institute Music Department, 1933-1947 (1933 account of Radio City Music Hall event) pg 6	6/14	1	247	140	1	\N	\N	\N	\N	\N	\N
2001	local	\N	2006-08-16 00:00:00	2006-08-16 00:00:00	826	Tuskegee Institute Music Department, 1933-1947 (1933 account of Radio City Music Hall event) pg 7	7/14	1	247	140	1	\N	\N	\N	\N	\N	\N
2002	local	\N	2006-08-16 00:00:00	2006-08-16 00:00:00	826	Tuskegee Institute Music Department, 1933-1947 (1933 account of Radio City Music Hall event) pg 8	8/14	1	247	140	1	\N	\N	\N	\N	\N	\N
2003	local	\N	2006-08-16 00:00:00	2006-08-16 00:00:00	826	Tuskegee Institute Music Department, 1933-1947 (1933 account of Radio City Music Hall event) pg 8	8a/14	1	247	140	1	\N	\N	DUPLICATE	\N	\N	\N
2004	local	\N	2006-08-16 00:00:00	2006-08-16 00:00:00	826	Tuskegee Institute Music Department, 1933-1947 (1933 account of Radio City Music Hall event) pg 9	9/14	1	247	140	1	\N	\N	\N	\N	\N	\N
2005	local	\N	2006-08-16 00:00:00	2006-08-16 00:00:00	826	Tuskegee Institute Music Department, 1933-1947 (1933 account of Radio City Music Hall event) pg 9	9a/14	1	247	140	1	\N	\N	DUPLICATE	\N	\N	\N
2006	local	\N	2006-08-16 00:00:00	2006-08-16 00:00:00	826	Tuskegee Institute Music Department, 1933-1947 (1933 account of Radio City Music Hall event) pg 10	10/14	1	247	140	1	\N	\N	\N	\N	\N	\N
2007	local	\N	2006-08-16 00:00:00	2006-08-16 00:00:00	826	Tuskegee Institute Music Department, 1933-1947 (1933 account of Radio City Music Hall event) pg 10	10a/14	1	247	140	1	\N	\N	\N	\N	\N	\N
2008	local	\N	2006-08-16 00:00:00	2006-08-16 00:00:00	826	Tuskegee Institute Music Department, 1933-1947 (1933 account of Radio City Music Hall event) pg 11	11/14	1	247	140	1	\N	\N	\N	\N	\N	\N
2009	local	\N	2006-08-16 00:00:00	2006-08-16 00:00:00	826	Tuskegee Institute Music Department, 1933-1947 (1933 account of Radio City Music Hall event) pg 11	11a/14	1	247	140	1	\N	\N	\N	\N	\N	\N
2010	local	\N	2006-08-17 00:00:00	2006-08-17 00:00:00	826	Arts Hall of Fame fourth introductory ceremony ambassador's dinner festival of arts. April 26, 1975.	Title page of program	1	247	140	1	\N	\N	\N	\N	\N	\N
2011	local	\N	2006-08-17 00:00:00	2006-08-17 00:00:00	826	Arts Hall of Fame fourth introductory ceremony ambassador's dinner festival of arts. April 26, 1975.	William Levi Dawson bio	1	247	140	1	\N	\N	\N	\N	\N	\N
7	local	00000027	2006-02-28 00:00:00	2006-02-28 00:00:00	826	Recording of an event at Columbus College, (Columbus, Georgia), n.d.	\N	16	25	140	1	The recording includes the speech "Balm in Gilead" delivered by William Levi Dawson and performance by a choir.  Dawson did not conduct the choir.	\N	This is side B of the audiocasette.	\N	\N	0
8	local	00000028	2006-02-28 00:00:00	2006-02-28 00:00:00	826	Recording of the Wayne State University Men's Glee Club, (Detroit, Michigan,) 9 March 1974	\N	16	25	140	1	William Levi Dawson was the guest conductor of the 90 voice Men's Glee Club during the Wayne State University Department of Music's Winter Festival.	\N	This is side A of the audiocassette.	\N	\N	0
1	local	00000021	2006-02-28 00:00:00	2006-02-28 00:00:00	826	Recording of the North Carolina Festival Chorus (Greenboro, North Carolina,) 15-16 April 1971	\N	16	247	140	1	William Levi Dawson was a guest conductor of 500 voices at the North Carolina Music Educators Conference that convened at the University of North Carolina at Greensboro.	\N	\N	2	2006-08-23 00:00:00	-1
4	local	00000024	2006-02-28 00:00:00	2006-02-28 00:00:00	826	Recording of the Tuskegee Alumni, Philadelphia Chapter, Golden Anniversary Dinner, (Philadelphia, Pennsylvania,) 4 December 1971	Honoring William Levi Dawson	16	25	140	1	The dinner included a tribute to conductor William Levi Dawson and speeches by author Ralph Ellison and fashion designer Allie White.	\N	This is side A of the audiocassette.	2	2006-08-23 17:21:35	-1
5	local	00000025	2006-02-28 00:00:00	2006-02-28 00:00:00	826	Recording of the Tuskegee Alumni, Philadelphia Chapter, Golden Anniversary Dinner, (Philadelphia, Pennsylvania,) 4 December 1971	Honoring William Levi Dawson	16	25	140	1	The dinner included a tribute to conductor William Levi Dawson and speeches by author Ralph Ellison and fashion designer Allie White.	\N	This is side B of the audiocassette.	2	2006-08-23 17:36:28	-1
6	local	00000026	2006-02-28 00:00:00	2006-02-28 00:00:00	826	Recording of an event at Columbus College, (Columbus, Georgia), n.d.	\N	16	25	140	1	The recording includes the speech "Balm in Gilead" delivered by William Levi Dawson and performance by a choir.  Dawson did not conduct the choir.	\N	This is side A of the audiocasette.  REDO - RECORDING BLANK	2	2006-08-23 17:39:31	-1
1814	local	0892-102	2006-07-31 00:00:00	\N	826	Published score for "Soon-Ah Will Be Done" (Male,) Music Press, Tuskegee Institute, 1962	\N	1	247	140	1	The music was arranged by William Levi Dawson. It was part of the Tuskegee Choir Series by Dawson.  This score is number T101-A.	\N	Only the cover was scanned.	\N	\N	\N
1111	local	\N	2006-06-13 00:00:00	\N	826	Letter from Rebecca T. Cureau to William Levi Dawson, 13 September 1985	\N	1	247	140	1	Cureau was then the Director of the Willis James Commemorative Project and a Visiting Lecturer in Music at Spelman College.  The letter concerns the Conference on Afro-American Music in Historically Black Colleges.	\N	This is page 1 of 2.	\N	\N	\N
1112	local	\N	2006-06-13 00:00:00	\N	826	Letter from Rebecca T. Cureau to William Levi Dawson, 13 September 1985	\N	1	247	\N	1	Cureau was then the Director of the Willis James Commemorative Project and a Visiting Lecturer in Music at Spelman College.  The letter concerns the Conference on Afro-American Music in Historically Black Colleges.	\N	This is page 2 of 2.	\N	\N	\N
1128	local	\N	2006-06-13 00:00:00	\N	826	Letter from the Louisiana Department of Music Education to William Levi Dawson, 12 April 1984	\N	1	247	\N	1	The letter was written by Tom D. Wafer, State Supervisor, Music Education, State of Louisiana.  It concerns the 1984 Louisiana All-State Choir.	\N	\N	\N	\N	\N
1541	local	\N	2006-07-13 00:00:00	\N	826	Photograph of the Tuskegee Choir performing Dvorak's "Stabat Mater" with the Atlanta Symphony Orchestra at the Tuskegee Institute, 9 April 1950	\N	9	25	140	1	The Choir was joined by 41 members of the Atlanta Symphany Orchestra.  William L. Dawson conducted.  This photograph was taken from the balcony and shows the entire choir and orchestra.	\N	\N	2	\N	\N
3	local	00000023	2006-02-28 00:00:00	2006-02-28 00:00:00	826	Recording of the Choral Festival 71, Houston Independent School District, (Houston, Texas,) 13 May 1971	\N	16	25	140	1	William Levi Dawson was the guest conductor of a mixed chorus of 400 voices and a female ensemble of 700 voices drawn from Houston senior high school choruses.  Both the rehearsal and concert were recorded.	\N	This is side B of the audiocassette.	\N	\N	0
2015	local	3333333	2006-08-25 00:00:00	\N	6	test	test	6	25	140	1	test	test	test	0	\N	0
2016	local	333333	2006-08-25 00:00:00	\N	6	test	test	6	25	140	1	etest	test	estt	0	\N	0
2017	local	\N	2006-08-25 00:00:00	\N	0	test	\N	6	25	140	1	\N	\N	\N	0	\N	0
2018	local	11111111	2006-08-25 00:00:00	\N	0	\N	\N	6	25	140	1	\N	\N	\N	0	\N	0
2019	local	6666666	2006-08-25 00:00:00	\N	6	\N	\N	6	25	140	1	\N	\N	\N	0	\N	0
2020	local	\N	2006-08-25 00:00:00	\N	0	\N	\N	6	25	140	1	\N	\N	\N	0	\N	0
2021	local	333333	2006-08-25 00:00:00	\N	0	\N	\N	6	25	140	1	\N	\N	\N	0	\N	0
1068	local	\N	2006-06-09 00:00:00	\N	826	Letter from the Alabama Arts Hall of Fame to William Levi Dawson, 13 March 1975	\N	1	247	140	1	The letter was written by W. C. Bauer, Chairman.  The letter informs Dawson that he has been nominated to be inducted into the Arts Hall of Fame.	\N	\N	\N	\N	\N
1075	local	\N	2006-06-09 00:00:00	\N	826	Letter from Shawnee Press, Inc., to William Levi Dawson, 2 November 1983	\N	1	247	140	1	The letter was written by Sheila O. Baress, librarian.  It lists the dates on which the Atlanta Symphony Orchestra plans to perform the Negro Folk Symphony in 1984.	\N	\N	\N	\N	\N
1076	local	\N	2006-06-09 00:00:00	\N	826	Letter from the Atlanta Symphony Orchestra to William Levi Dawson, 10 November 1983	\N	1	247	\N	1	The letter was written by Nancy L. Bankoff, Orchestra Manager and Music Administrator.  It informs Dawson of the Symphony's plans to perform the Negro Folk Symphony in February 1984 and invites him to attend the performances.	\N	\N	\N	\N	\N
1179	local	\N	2006-06-14 00:00:00	\N	826	Letter from William Levi Dawson to Jose F. Carneado, 1 March 1946	\N	1	247	\N	1	This document forms part of a subject file on Romilio Manduley O'Larson (Cuba), 1943-1946.	\N	Page 1 of 2.	\N	\N	\N
1079	local	\N	2006-06-09 00:00:00	\N	826	Letter from William Levi Dawson to the Atlanta Symphony Orchestra, 26 December 1983	\N	1	247	\N	1	The letter was addressed to Nancy L. Bankoff, Orchestra Manager and Music Administrator.  It concerns the planned performances of the Negro Folk Symphony in February 1984.	\N	\N	\N	\N	\N
1078	local	\N	2006-06-09 00:00:00	\N	826	Letter from William Levi Dawson to the Atlanta Symphony Orchestra, 28 November 1983	\N	1	247	\N	1	The letter was addressed to Nancy L. Bankoff, Orchestra Manager and Music Administrator.  It concerns the planned performances of the Negro Folk Symphony in February 1984.	\N	\N	\N	\N	\N
1077	local	\N	2006-06-09 00:00:00	\N	826	Letter from William Levi Dawson to Robert Shaw, 28 November 1983	\N	1	247	\N	1	Shaw was the Conductor of the Atlanta Symphony Orchestra.  The letter concerns the planned performances of the Negro Folk Symphony in February 1984.	\N	\N	\N	\N	\N
1080	local	\N	2006-06-09 00:00:00	\N	826	Letter from the Atlanta Symphony Orchestra to William Levi Dawson, 9 January 1984	\N	1	247	\N	1	The letter was written by Nancy L. Bankoff, Orchestra Manager and Music Administrator.  It concerns the planned  performances of the Negro Folk Symphony in February 1984.	\N	\N	\N	\N	\N
1081	local	\N	2006-06-09 00:00:00	\N	826	Letter from Shawnee Press, Inc.,  to William Levi Dawson, 26 March 1985	\N	1	247	\N	1	The letter was written by Kelly Mulvey.  It concerns a planned performance of the Negro Folk Symphony by the Atlanta Symphony Orchestra in 1985.	\N	\N	\N	\N	\N
1084	local	\N	2006-06-09 00:00:00	\N	826	Atlanta arts monthly magazine: the monthly magazine of the Robert W. Woodruff Arts Center, Vol. XVI, No. 19 (February 1984)	\N	1	247	\N	1	This issue included the program for the concerts on February 2, 3 and 4, 1984.  Those concerts included William Levi Dawson's Negro Folk Symphony.	\N	Only the cover was scanned.	\N	\N	\N
1118	local	\N	2006-06-13 00:00:00	\N	826	Citation for the honorary doctorate given to William Levi Dawson by Lincoln University, 7 May 1978	\N	1	247	\N	1	Typescript on Lincoln University letterhead.	\N	\N	\N	\N	\N
1129	local	\N	2006-06-13 00:00:00	\N	826	News release from the Creative Artists Workshop (Philadelphia, Pennsylvania), 1981	\N	1	247	\N	1	The release concerns an evening of compositions by William Levi Dawson sponsored by several Pennsylvania organizations.  The event at the Academy of Music Hall in Philadelphia was to include performances by the Mendelssohn singers, and John R. Russell.	\N	\N	\N	\N	\N
1130	local	\N	2006-06-13 00:00:00	\N	826	Letter from Robert R. Moton Memorial Institute, Inc., to William Levi Dawson, 16 January 1985	\N	1	247	\N	1	The letter was written by F. D. Patterson, Director, College Endowment Funding Program, Robert R. Moton Memorial Institute, Inc.  It thanks Dawson for his talk at the Moton Conference Center on January 13 and 14.	\N	\N	\N	\N	\N
1135	local	\N	2006-06-13 00:00:00	\N	826	Typescript of "Instructions for learning and memorizing the music," written by William Levi Dawson for the Music Educators National Conference All-Eastern Division Chorus, [1960]	\N	1	247	\N	1	Dawson conducted the chorus in January 1961 in Washington, DC.	\N	\N	\N	\N	\N
1141	local	\N	2006-06-13 00:00:00	\N	826	Letter from the National Interscholastic Music Activities Commission, an auxiliary of the Music Educators National Conference, to William Levi Dawson, 20 June 1960	\N	1	247	\N	1	The letter was written by Wayne H. Camp, General Chairman, National Interscholastic Music Activities Commission.  He requests that Dawson send him the proposed compositions for the All-Eastern Chorus, Band and Orchestra for the 1961 Eastern Conference of the MENC in Washington, DC.	\N	\N	\N	\N	\N
1142	local	\N	2006-06-13 00:00:00	\N	826	Letter from William Levi Dawson to the National Interscholastic Music Activities Commission, 27 June 1960	\N	1	247	\N	1	The letter is addressed to Wayne H. Camp, General Chairman, National Interscholastic Music Activities Commission. Dawson requests more information about the All-Eastern Chorus, Band and Orchestra for the 1961 Eastern Conference of the MENC in Washington, DC.	\N	\N	\N	\N	\N
1143	local	\N	2006-06-13 00:00:00	\N	826	Letter from William Levi Dawson to the National Interscholastic Music Activities Commission, 18 July 1960	\N	1	247	\N	1	The letter is addressed to Wayne H. Camp, General Chairman, National Interscholastic Music Activities Commission. The letter accompanied the proposed program for the All-Eastern Chorus, Band and Orchestra for the 1961 Eastern Conference of the MENC in Washington, DC.	\N	Page 1 of 2.  The proposed program (page 2)  has not been scanned.	\N	\N	\N
1167	local	\N	2006-06-14 00:00:00	\N	826	Program for the Ohio Music Education Association's Professional Conference (Dayton, Ohio), 2-4 February 1984	\N	1	247	\N	1	William Levi Dawson presented a clinic entitled "Interpretation of the music of the American Negro--a choral reading session."	\N	Only the cover and page 31 were scanned.  This is the cover.	\N	\N	\N
1169	local	\N	2006-06-14 00:00:00	\N	826	Letter from the Ohio Music Education Association to William Levi Dawson, 26 October 1983	\N	1	247	\N	1	The letter was written by Ernie Flamm, Conference Chairman, Ohio Music Education Association.  It concerns Dawson's participation in the 1984 OMEA Professional Conference.	\N	\N	\N	\N	\N
1191	local	\N	2006-06-14 00:00:00	\N	826	Letter from the Program in Black American Culture, National Museum of American History, to William Levi Dawson, 9 February 1984	\N	1	247	\N	1	The letter was written by Bernice Johnson Reagon, Director, Program in Black American Culture.  It concerns Dawson's participation in the museum's Black History Month program "Spirituals: Black American Choral Song," in February 1984.	\N	\N	\N	\N	\N
1192	local	\N	2006-06-14 00:00:00	\N	826	Letter from William Levi Dawson to the Program in Black American Culture, National Museum of American History, 6 March 1984	\N	1	247	\N	1	The letter is addressed to Bernice Johnson Reagon, Director, Program in Black American Culture.  It concerns Dawson's participation in the museum's Black History Month program "Spirituals: Black American Choral Song," in February 1984.	\N	\N	\N	\N	\N
1287	local	\N	2006-06-23 00:00:00	\N	826	Letter from the United Negro College Fund to William Levi Dawson, 28 January 1955	\N	1	247	\N	1	The letter was written by Dorothy L. Barker, Radio and TV Director, United Negro College Fund.  It concerns the Tuskegee Institute Choir's concerts and appearances in New York City in March 1955 during UNCF Convocation week.	\N	\N	\N	\N	\N
1288	local	\N	2006-06-23 00:00:00	\N	826	Letter from the United Negro College Fund to William Levi Dawson, 8 February 1955	\N	1	247	\N	1	The letter was written by W. J. Trent, Jr., Executive Director, United Negro College Fund.   It concerns the Tuskegee Institute Choir's concerts and appearances in New York City in March 1955 during UNCF Convocation week.	\N	\N	\N	\N	\N
1290	local	\N	2006-06-23 00:00:00	\N	826	Broadside announcing that the Tuskegee Institute School of Music is ready to receive applications, [undated]	\N	1	247	\N	1	The text begins, "An Announcement.  The School of Music of Tuskegee Institute is ready to receive applications for the study of Piano, Voice, Violin, Brass and Woodwind Instruments, Public School Music, History and Appreciation of Music, Theory of Music, and Instrumental Supervisors Course for band and orchestra instructors."  William Levi Dawson was the director of the School of Music.  This item most likely dates from the period 1933-1947.	\N	\N	\N	\N	\N
1291	local	\N	2006-06-23 00:00:00	\N	826	List of the faculty of the Tuskegee Institute School of Music [typescript], 9 January 1934	\N	1	247	\N	1	The list includes each teacher's educational background and course load.  William Levi Dawson was the director of the school.	\N	\N	\N	\N	\N
1345	local	\N	2006-06-27 00:00:00	\N	826	Course book from Crane Junior College (Chicago, Illinois) belonging to William Levi Dawson, 1927	\N	15	247	\N	1	This book records the classes Dawson took and the grades he received.	\N	Only the page for the semester ending January 27 was scanned.	\N	\N	\N
1348	local	\N	2006-06-27 00:00:00	\N	826	Voter registration certificate (Cook County, Illinois) for Willliam L. Dawson, 10 April 1928	\N	1	247	\N	1	\N	\N	\N	\N	\N	\N
1350	local	\N	2006-06-27 00:00:00	\N	826	Program for a pianoforte recital by Cornella D Lampton in Rankin Memorial Hall, 6 April [1914]	\N	1	247	\N	1	Lampton is listed as receiving a Mus. B. degree in the class of 1914.  The name of the school is not included in the program.  Lampton was a graduate of Howard University and Oberlin College.	\N	\N	\N	\N	\N
1351	local	\N	2006-06-27 00:00:00	\N	826	Program for a piano recital by Cornella D. Lampton, 15 February 1927	\N	1	247	\N	1	The location for the recital is not given.	\N	\N	\N	\N	\N
1352	local	\N	2006-06-27 00:00:00	\N	826	Honorary Doctorate of Music degree received by William Levi Dawson from Tuskegee Institute, 25 March 1956	\N	1	247	\N	1	\N	\N	\N	\N	\N	\N
1035	local	\N	2006-06-07 00:00:00	\N	826	Speech by William Levi Dawson to the American Choral Directors convention, undated	\N	1	247	\N	1	\N	\N	This is page 2 of 4.	\N	\N	\N
1036	local	\N	2006-06-07 00:00:00	\N	826	Speech by William Levi Dawson to the American Choral Directors convention, undated	\N	1	247	\N	1	\N	\N	This is page 3 of 4.	\N	\N	\N
1037	local	\N	2006-06-07 00:00:00	\N	826	Speech by William Levi Dawson to the American Choral Directors convention, undated	\N	1	247	\N	1	\N	\N	This is page 4 of 4.	\N	\N	\N
1047	local	\N	2006-06-09 00:00:00	\N	826	Autograph draft of a speech by William Levi Dawson on choral conducting, undated	\N	1	247	140	1	\N	\N	The speech was handwritten in pencil with corrections in red.  This is page 1 of 13 (numbered I).	\N	\N	\N
1048	local	\N	2006-06-09 00:00:00	\N	826	Autograph draft of a speech by William Levi Dawson on choral conducting, undated	\N	1	247	\N	1	\N	\N	The speech was handwritten in pencil with corrections in red.  This is page 2 of 13 (numbered II).	\N	\N	\N
1049	local	\N	2006-06-09 00:00:00	\N	826	Autograph draft of a speech by William Levi Dawson on choral conducting, undated	\N	1	247	\N	1	\N	\N	The speech was handwritten in pencil with corrections in red.  This is page 3 of 13 (numbered III).	\N	\N	\N
1050	local	\N	2006-06-09 00:00:00	\N	826	Autograph draft of a speech by William Levi Dawson on choral conducting, undated	\N	1	247	\N	1	\N	\N	The speech was handwritten in pencil with corrections in red.  This is page 4 of 13 (numbered IV).	\N	\N	\N
1051	local	\N	2006-06-09 00:00:00	\N	826	Autograph draft of a speech by William Levi Dawson on choral conducting, undated	\N	1	247	\N	1	\N	\N	The speech was handwritten in pencil with corrections in red.  This is page 5 of 13 (numbered V).	\N	\N	\N
1052	local	\N	2006-06-09 00:00:00	\N	826	Autograph draft of a speech by William Levi Dawson on choral conducting, undated	\N	1	247	\N	1	\N	\N	The speech was handwritten in pencil with corrections in red.  This is page 6 of 13 (numbered VI).	\N	\N	\N
1053	local	\N	2006-06-09 00:00:00	\N	826	Autograph draft of a speech by William Levi Dawson on choral conducting, undated	\N	1	247	\N	1	\N	\N	The speech was handwritten in pencil with corrections in red.  This is page 7 of 13 (numbered VII).	\N	\N	\N
1054	local	\N	2006-06-09 00:00:00	\N	826	Autograph draft of a speech by William Levi Dawson on choral conducting, undated	\N	1	247	\N	1	\N	\N	The speech was handwritten in pencil with corrections in red.  This is page 8 of 13 (numbered VIII).	\N	\N	\N
1055	local	\N	2006-06-09 00:00:00	\N	826	Autograph draft of a speech by William Levi Dawson on choral conducting, undated	\N	1	247	\N	1	\N	\N	The speech was handwritten in pencil with corrections in red.  This is page 9 of 13 (numbered IX).	\N	\N	\N
1056	local	\N	2006-06-09 00:00:00	\N	826	Autograph draft of a speech by William Levi Dawson on choral conducting, undated	\N	1	247	\N	1	\N	\N	The speech was handwritten in pencil with corrections in red.  This is page 10 of 13 (numbered Xa).	\N	\N	\N
1057	local	\N	2006-06-09 00:00:00	\N	826	Autograph draft of a speech by William Levi Dawson on choral conducting, undated	\N	1	247	\N	1	\N	\N	The speech was handwritten in pencil with corrections in red.  This is page 11 of 13 (numbered Xb).	\N	\N	\N
1058	local	\N	2006-06-09 00:00:00	\N	826	Autograph draft of a speech by William Levi Dawson on choral conducting, undated	\N	1	247	\N	1	\N	\N	The speech was handwritten in pencil with corrections in red.  This is page 12 of 13 (from verso of page Xb).  The final page of notes was not scanned in July 2006.	\N	\N	\N
1059	local	\N	2006-06-09 00:00:00	\N	826	A "Report to Mr. Robert D. Barton, Assistant Cultural Attache, American Embassy, Madrid, Spain, on my trip to Spain during my trip to Spain during the summer, 1956," by William Levi Dawson	\N	1	247	140	1	In 1956 the United States State Department invited Dawson to tour Spain to train local choirs in the African American spiritual tradition.	\N	This is page 1 of 7.	\N	\N	\N
1060	local	\N	2006-06-09 00:00:00	\N	826	A "Report to Mr. Robert D. Barton, Assistant Cultural Attache, American Embassy, Madrid, Spain, on my trip to Spain during my trip to Spain during the summer, 1956," by William Levi Dawson	\N	1	247	\N	1	In 1956 the United States State Department invited Dawson to tour Spain to train local choirs in the African American spiritual tradition.	\N	This is page 2 of 7.	\N	\N	\N
1061	local	\N	2006-06-09 00:00:00	\N	826	A "Report to Mr. Robert D. Barton, Assistant Cultural Attache, American Embassy, Madrid, Spain, on my trip to Spain during my trip to Spain during the summer, 1956," by William Levi Dawson	\N	1	247	\N	1	In 1956 the United States State Department invited Dawson to tour Spain to train local choirs in the African American spiritual tradition.	\N	This is page 3 of 7.	\N	\N	\N
1062	local	\N	2006-06-09 00:00:00	\N	826	A "Report to Mr. Robert D. Barton, Assistant Cultural Attache, American Embassy, Madrid, Spain, on my trip to Spain during my trip to Spain during the summer, 1956," by William Levi Dawson	\N	1	247	\N	1	In 1956 the United States State Department invited Dawson to tour Spain to train local choirs in the African American spiritual tradition.	\N	This is page 4 of 7.	\N	\N	\N
1063	local	\N	2006-06-09 00:00:00	\N	826	A "Report to Mr. Robert D. Barton, Assistant Cultural Attache, American Embassy, Madrid, Spain, on my trip to Spain during my trip to Spain during the summer, 1956," by William Levi Dawson	\N	1	247	\N	1	In 1956 the United States State Department invited Dawson to tour Spain to train local choirs in the African American spiritual tradition.	\N	This is page 5 of 7.	\N	\N	\N
1064	local	\N	2006-06-09 00:00:00	\N	826	A "Report to Mr. Robert D. Barton, Assistant Cultural Attache, American Embassy, Madrid, Spain, on my trip to Spain during my trip to Spain during the summer, 1956," by William Levi Dawson	\N	1	247	\N	1	In 1956 the United States State Department invited Dawson to tour Spain to train local choirs in the African American spiritual tradition.	\N	This is page 6 of 7.	\N	\N	\N
1065	local	\N	2006-06-09 00:00:00	\N	826	A "Report to Mr. Robert D. Barton, Assistant Cultural Attache, American Embassy, Madrid, Spain, on my trip to Spain during my trip to Spain during the summer, 1956," by William Levi Dawson	\N	1	247	\N	1	In 1956 the United States State Department invited Dawson to tour Spain to train local choirs in the African American spiritual tradition.	\N	This is page 7 of 7.	\N	\N	\N
1066	local	\N	2006-06-09 00:00:00	\N	826	Itinerary for Mr. William Levi Dawson's trip to Africa, Sarah Marquis Travel Service, 28 October 1952	\N	1	247	140	1	Carbon copy of the itinerary on Sarah Marquis Travel Service letterhead.	\N	This is page 1 of 2.	\N	\N	\N
1067	local	\N	2006-06-09 00:00:00	\N	826	Itinerary for Mr. William Levi Dawson's trip to Africa, Sarah Marquis Travel Service, 28 October 1952	\N	1	247	\N	1	Carbon copy of the itinerary on Sarah Marquis Travel Service letterhead.	\N	This is page 2 of 2.	\N	\N	\N
1069	local	\N	2006-06-09 00:00:00	\N	826	Letter from the Alabama Arts Music Hall of Fame to William Levi Dawson, 6 October 1984	\N	1	247	140	1	The letter was written by Lola Scobey, Executive Director, Alabama Arts Music Hall of Fame. It informs Dawson that he has been nominated to be inducted into the Arts Hall of Fame.	\N	This is page 1 of 4.	\N	\N	\N
1070	local	\N	2006-06-09 00:00:00	\N	826	Letter from the Alabama Arts Music Hall of Fame to William Levi Dawson, 6 October 1984	\N	1	247	\N	1	The letter was written by Lola Scobey, Executive Director, Alabama Arts Music Hall of Fame. It informs Dawson that he has been nominated to be inducted into the Arts Hall of Fame.	\N	This is page 2 of 4.	\N	\N	\N
1071	local	\N	2006-06-09 00:00:00	\N	826	Letter from the Alabama Arts Music Hall of Fame to William Levi Dawson, 6 October 1984	\N	1	247	\N	1	The letter was written by Lola Scobey, Executive Director, Alabama Arts Music Hall of Fame. It informs Dawson that he has been nominated to be inducted into the Arts Hall of Fame.	\N	This is page 3 of 4.	\N	\N	\N
1072	local	\N	2006-06-09 00:00:00	\N	826	Letter from the Alabama Arts Music Hall of Fame to William Levi Dawson, 6 October 1984	\N	1	247	\N	1	The letter was written by Lola Scobey, Executive Director, Alabama Arts Music Hall of Fame. It informs Dawson that he has been nominated to be inducted into the Arts Hall of Fame.	\N	This is page 4 of 4.	\N	\N	\N
1115	local	\N	2006-06-13 00:00:00	\N	826	Program from Lincoln University's Commencement Exercises, 7 May  1978	\N	1	247	\N	1	William Levi Dawson received an Honorary Doctorate at this ceremony.	\N	The cover and four pages were scanned. These two pages list the honor graduates and the graduating class 1978.	\N	\N	\N
1114	local	\N	2006-06-13 00:00:00	\N	826	Program from Lincoln University's Commencement Exercises, 7 May  1978	\N	1	247	\N	1	William Levi Dawson received an Honorary Doctorate at this ceremony.	\N	The cover and four pages were scanned.  These two pages list the graduation exercises.	\N	\N	\N
1120	local	\N	2006-06-13 00:00:00	\N	826	Program for the Louisiana Music Educators Association's 1984 Louisiana All-State Concerts (Northwestern State University, Natchitoches, Louisiana), 19-20 November 1984	\N	1	247	\N	1	\N	\N	The entire program was scanned.  This is the cover.	\N	\N	\N
1131	local	\N	2006-06-13 00:00:00	\N	826	Program from the ceremony designating the Robert R. Moton House (Capahosic, Virginia) as a national historic landmark, 14  January 1985	\N	1	247	\N	1	The event was sponsored by the Robert R. Moton Memorial Institute and Conference Center.  William Levi Dawson spoke during the ceremony.	\N	The cover and the page listing the program were scanned.  This is the cover.	\N	\N	\N
1132	local	\N	2006-06-13 00:00:00	\N	826	Program from the ceremony designating the Robert R. Moton House (Capahosic, Virginia) as a national historic landmark, 14  January 1985	\N	1	247	\N	1	The event was sponsored by the Robert R. Moton Memorial Institute and Conference Center.  William Levi Dawson spoke during the ceremony.	\N	The cover and the page listing the program were scanned.  This is the page listing the program.	\N	\N	\N
1133	local	\N	2006-06-13 00:00:00	\N	826	Program for the Eastern Music Educators Conference Gala Festival Concert (Washington, DC), 16 January 1961	\N	1	247	\N	1	William Levi Dawson was the conductor for the All-Eastern Division High School Chorus.	\N	The cover and the page listing the program were scanned.  This is the cover.	\N	\N	\N
1134	local	\N	2006-06-13 00:00:00	\N	826	Program for the Eastern Music Educators Conference Gala Festival Concert (Washington, DC), 16 January 1961	\N	1	247	\N	1	William Levi Dawson was the conductor for the All-Eastern Division High School Chorus.	\N	The cover and the page listing the program were scanned.  This is the page listing the program.	\N	\N	\N
1137	local	\N	2006-06-13 00:00:00	\N	826	Letter from William Levi Dawson to the Music Educators National Conference, Eastern Division, 14 May 1960	\N	1	247	\N	1	The letter is addressed to Maurice C. Whitney, President, MENC Eastern Division.  In the letter, Dawson accepts an invitation to serve as conductor for the All-Eastern Chorus, Band and Orchestra at the 1961 Eastern Conference of the MENC in Washington, DC.	\N	\N	\N	\N	\N
1138	local	\N	2006-06-13 00:00:00	\N	826	Letter from the Music Educators National Conference to William Levi Dawson, 25 May 1960	\N	1	247	\N	1	The letter was written by Wayne H. Camp, General Chairman, National Interscholastic Music Activities Commission, an auxiliary of the Music Educators National Conference.  It contains details and a schedule related to the performance of the All-Eastern Chorus, Band and Orchestra at the 1961 Eastern Conference of the MENC in Washington, DC.	\N	This is page 1 of 3.	\N	\N	\N
1139	local	\N	2006-06-13 00:00:00	\N	826	Letter from the Music Educators National Conference to William Levi Dawson, 25 May 1960	\N	1	247	\N	1	The letter was written by Wayne H. Camp, General Chairman, National Interscholastic Music Activities Commission, an auxiliary of the Music Educators National Conference.  It contains details and a schedule related to the performance of the All-Eastern Chorus, Band and Orchestra at the 1961 Eastern Conference of the MENC in Washington, DC.	\N	This is page 2 of 3.	\N	\N	\N
1140	local	\N	2006-06-13 00:00:00	\N	826	Letter from the Music Educators National Conference to William Levi Dawson, 25 May 1960	\N	1	247	\N	1	The letter was written by Wayne H. Camp, General Chairman, National Interscholastic Music Activities Commission, an auxiliary of the Music Educators National Conference.  It contains details and a schedule related to the performance of the All-Eastern Chorus, Band and Orchestra at the 1961 Eastern Conference of the MENC in Washington, DC.	\N	This is page 3 of 3.	\N	\N	\N
1164	local	\N	2006-06-14 00:00:00	\N	826	Program for the In-Service Conference sponsored by the Southern Division of the Music Educators National Conference (Louisville, Kentucky), 2-5 February 1983	\N	1	247	140	1	William Levi Dawson presented a choral reading session on African American spirituals and folk songs.	\N	Only the cover and page 67 were scanned.  This is the cover.	\N	\N	\N
1165	local	\N	2006-06-14 00:00:00	\N	826	Program for the In-Service Conference sponsored by the Southern Division of the Music Educators National Conference (Louisville, Kentucky), 2-5 February 1983	\N	1	247	\N	1	William Levi Dawson presented a choral reading session on African American spirituals and folk songs.  This page includes the description of Dawson's session.	\N	Only the cover and page 67 were scanned.  This is page 67.	\N	\N	\N
1168	local	\N	2006-06-14 00:00:00	\N	826	Program for the Ohio Music Education Association's Professional Conference (Dayton, Ohio), 2-4 February 1984	\N	1	247	\N	1	William Levi Dawson presented a clinic entitled "Interpretation of the music of the American Negro--a choral reading session."  The description of Dawson's clinic is on this page.	\N	Only the cover and page 31 were scanned.  This is page 31.	\N	\N	\N
1170	local	\N	2006-06-14 00:00:00	\N	826	Holograph translation by William Levi Dawson of "Negro Aviators" by Herminio Portell Vila, originally published in El Pais (Madrid, Spain), 20 February 1944	\N	1	247	\N	1	This document forms part of a subject file on Romilio Manduley O'Larson (Cuba), 1943-1946.	\N	Page 1 of 6.	\N	\N	\N
1171	local	\N	2006-06-14 00:00:00	\N	826	Holograph translation by William Levi Dawson of "Negro Aviators" by Herminio Portell Vila, originally published in El Pais (Madrid, Spain), 20 February 1944	\N	1	247	\N	1	This document forms part of a subject file on Romilio Manduley O'Larson (Cuba), 1943-1946.	\N	Page 2 of 6.	\N	\N	\N
1172	local	\N	2006-06-14 00:00:00	\N	826	Holograph translation by William Levi Dawson of "Negro Aviators" by Herminio Portell Vila, originally published in El Pais (Madrid, Spain), 20 February 1944	\N	1	247	\N	1	This document forms part of a subject file on Romilio Manduley O'Larson (Cuba), 1943-1946.	\N	Page 3 of 6.	\N	\N	\N
1173	local	\N	2006-06-14 00:00:00	\N	826	Holograph translation by William Levi Dawson of "Negro Aviators" by Herminio Portell Vila, originally published in El Pais (Madrid, Spain), 20 February 1944	\N	1	247	\N	1	This document forms part of a subject file on Romilio Manduley O'Larson (Cuba), 1943-1946.	\N	Page 4 of 6.	\N	\N	\N
1174	local	\N	2006-06-14 00:00:00	\N	826	Holograph translation by William Levi Dawson of "Negro Aviators" by Herminio Portell Vila, originally published in El Pais (Madrid, Spain), 20 February 1944	\N	1	247	\N	1	This document forms part of a subject file on Romilio Manduley O'Larson (Cuba), 1943-1946.	\N	Page 5 of 6.	\N	\N	\N
1175	local	\N	2006-06-14 00:00:00	\N	826	Holograph translation by William Levi Dawson of "Negro Aviators" by Herminio Portell Vila, originally published in El Pais (Madrid, Spain), 20 February 1944	\N	1	247	\N	1	This document forms part of a subject file on Romilio Manduley O'Larson (Cuba), 1943-1946.	\N	Page 6 of 6.	\N	\N	\N
1176	local	\N	2006-06-14 00:00:00	\N	826	Letter from William Levi Dawson to Rene, 21 February 1946	\N	1	247	\N	1	This document forms part of a subject file on Romilio Manduley O'Larson (Cuba), 1943-1946.	\N	Page 1 of 2.	\N	\N	\N
1177	local	\N	2006-06-14 00:00:00	\N	826	Letter from William Levi Dawson to Rene, 21 February 1946	\N	1	247	\N	1	This document forms part of a subject file on Romilio Manduley O'Larson (Cuba), 1943-1946.	\N	Page 2 of 2.	\N	\N	\N
1180	local	\N	2006-06-14 00:00:00	\N	826	Letter from William Levi Dawson to Jose F. Carneado, 1 March 1 1946	\N	1	247	\N	1	This document forms part of a subject file on Romilio Manduley O'Larson (Cuba), 1943-1946.	\N	Page 2 of 2.	\N	\N	\N
1181	local	\N	2006-06-14 00:00:00	\N	826	Letter from William Levi Dawson to Congressman William L. Dawson, 1 March 1946	\N	1	247	\N	1	In this letter, Dawson requests that the Congressman aid efforts to secure permission for Romilio Manduley O'Larson to live in the U.S.  Attached to the letter is a memorandum in English and in Spanish concerning this request.  From a subject file on Romilio Manduley O'Larson (Cuba), 1943-1946.	\N	Page 1 of 3.	\N	\N	\N
1182	local	\N	2006-06-14 00:00:00	\N	826	Letter from William Levi Dawson to Congressman William L. Dawson, 1 March 1946	\N	1	247	\N	1	In this letter, Dawson requests that the Congressman aid efforts to secure permission for Romilio Manduley O'Larson to live in the U.S.  Attached to the letter is a memorandum in English and in Spanish concerning this request.  From a subject file on Romilio Manduley O'Larson (Cuba), 1943-1946.	\N	Page 2 of 3.	\N	\N	\N
1183	local	\N	2006-06-14 00:00:00	\N	826	Letter from William Levi Dawson to Congressman William L. Dawson, 1 March 1946	\N	1	247	482	1	In this letter, Dawson requests that the Congressman aid efforts to secure permission for Romilio Manduley O'Larson to live in the U.S.  Attached to the letter is a memorandum in English and in Spanish concerning this request.  From a subject file on Romilio Manduley O'Larson (Cuba), 1943-1946.	\N	Page 3 of 3.	\N	\N	\N
1184	local	\N	2006-06-14 00:00:00	\N	826	Program for the tenth annual conference of the Organization of American Kodaly Educators (New Orleans, Louisiana), 5-8 April 1984	\N	1	247	\N	1	\N	\N	Only the cover and page [12] were scanned.  This is the cover.	\N	\N	\N
1185	local	\N	2006-06-14 00:00:00	\N	826	Program for the tenth annual conference of the Organization of American Kodaly Educators (New Orleans, Louisiana), 5-8 April 1984	\N	1	247	\N	1	This page includes the schedule for the afternoon and evening of Saturday, 7 April.  The program that day included a session by William Levi Dawson.	\N	Only the cover and page [12] were scanned.  This is the cover.	\N	\N	\N
1188	local	\N	2006-06-14 00:00:00	\N	826	Letter from Program in Black American Culture, National Museum of American History, to William Levi Dawson, 1 November 1983	\N	1	247	\N	1	The letter was written by Bernice Johnson Reagon, Director, Program in Black American Culture.  It concerns Dawson's participation in the museum's Black History Month program "Spirituals: Black American Choral Song" in February 1984.	\N	Page 1 of 2.	\N	\N	\N
1189	local	\N	2006-06-14 00:00:00	\N	826	Letter from Program in Black American Culture, National Museum of American History, to William Levi Dawson, 1 November 1983	\N	1	247	\N	1	The letter was written by Bernice Johnson Reagon, Director, Program in Black American Culture.  It concerns Dawson's participation in the museum's Black History Month program "Spirituals: Black American Choral Song" in February 1984.	\N	Page 2 of 2.	\N	\N	\N
1186	local	\N	2006-06-14 00:00:00	\N	826	Program for "Black American choral song: the evolution of the spiritual," sponsored by the National Museum of American History Department of Public Programs, 3-4 February 1984	\N	1	247	\N	1	William Levi Dawson and Eva Jesseye led a master class.	\N	Both covers and the program were scanned.  This is the front and back covers.	\N	\N	\N
1187	local	\N	2006-06-14 00:00:00	\N	826	Program for "Black American choral song: the evolution of the spiritual," sponsored by the National Museum of American History Department of Public Programs, 3-4 February 1984	\N	1	247	\N	1	William Levi Dawson and Eva Jesseye led a master class.	\N	Both covers and the program were scanned.  This is the overview and program.	\N	\N	\N
1193	local	\N	2006-06-14 00:00:00	\N	826	Brochure: "How to see Barcelona and its surroundings," undated	\N	1	247	\N	1	William Levi Dawson acquired this brochure during a trip Spain in 1956.	\N	Both sides of the tri-fold brochure were scanned.  This is the first side.	\N	\N	\N
1194	local	\N	2006-06-14 00:00:00	\N	826	Brochure: "How to see Barcelona and its surroundings," undated	\N	1	247	\N	1	William Levi Dawson acquired this brochure during a trip Spain in 1956.	\N	Both sides of the tri-fold brochure were scanned.  This is the first side.	\N	\N	\N
1195	local	\N	2006-06-14 00:00:00	\N	826	Menu from an Iberia Airlines flight between New York and Madrid, 17 July 1956	\N	15	482	247	1	William Levi Dawson acquired this menu during a trip Spain in 1956.	\N	The two inside pages were scanned.  This is the page indicating the flight and date.	\N	\N	\N
1196	local	\N	2006-06-14 00:00:00	\N	826	Menu from an Iberia Airlines flight between New York and Madrid, 17 July 1956	\N	1	247	\N	1	William Levi Dawson acquired this menu during a trip Spain in 1956.	\N	The two inside pages were scanned.  This is the menu.	\N	\N	\N
1197	local	\N	2006-06-14 00:00:00	\N	826	Brochure for the Othon Palace Hotel (Sao Paulo, Brazil), undated	\N	1	247	\N	1	\N	\N	\N	\N	\N	\N
1198	local	\N	2006-06-14 00:00:00	\N	826	Brochure for the Othon Palace Hotel (Sao Paulo, Brazil), undated	\N	1	247	\N	1	\N	\N	\N	\N	\N	\N
1199	local	\N	2006-06-14 00:00:00	\N	826	Report on concerts held in Spain under the direction of PL-402 specialist grantee William Levi Dawson, by Antonio Gonzales de la Pena (American Embassy, Madrid, Spain), [ca. 1956]	\N	1	247	\N	1	This unclassified report discusses Dawson's 1956 cultural trip to Spain.  (In 1956 the United States State Department invited Dawson to tour Spain to train local choirs in the African American spiritual tradition.)	\N	This is page 1 of 4.	\N	\N	\N
1200	local	\N	2006-06-14 00:00:00	\N	826	Report on concerts held in Spain under the direction of PL-402 specialist grantee William Levi Dawson, by Antonio Gonzales de la Pena (American Embassy, Madrid, Spain), [ca. 1956]	\N	1	247	\N	1	This unclassified report discusses Dawson's 1956 cultural trip to Spain.  (In 1956 the United States State Department invited Dawson to tour Spain to train local choirs in the African American spiritual tradition.)	\N	This is page 2 of 4.	\N	\N	\N
1201	local	\N	2006-06-14 00:00:00	\N	826	Report on concerts held in Spain under the direction of PL-402 specialist grantee William Levi Dawson, by Antonio Gonzales de la Pena (American Embassy, Madrid, Spain), [ca. 1956]	by Antonio Gonzales Pena, American Embassy, Madrid	1	247	\N	1	This unclassified report discusses Dawson's 1956 cultural trip to Spain.  (In 1956 the United States State Department invited Dawson to tour Spain to train local choirs in the African American spiritual tradition.)	\N	This is page 3 of 4.	\N	\N	\N
1202	local	\N	2006-06-14 00:00:00	\N	826	Report on concerts held in Spain under the direction of PL-402 specialist grantee William Levi Dawson, by Antonio Gonzales de la Pena (American Embassy, Madrid, Spain), [ca. 1956]	by Antonio Gonzales Pena, American Embassy, Madrid	1	247	\N	1	This unclassified report discusses Dawson's 1956 cultural trip to Spain.  (In 1956 the United States State Department invited Dawson to tour Spain to train local choirs in the African American spiritual tradition.)	\N	This is page 4 of 4.	\N	\N	\N
1203	local	\N	2006-06-14 00:00:00	\N	826	Typed copies of fan mail sent to the Tuskegee Institute Choir, 1937	\N	1	247	\N	1	The title page for this group of letters reads "A sampling of the thousands of fan-mail letters that were received during the series of half-hour broadcasts by the Tuskegee Institute Choir, conducted by William L. Dawson, each Sunday over the NBC Red network 1937-38."\n\nThis page contains transcriptions of letters from Chester Bowles (New York, New York) and Mrs. William Kirkham Taylor (Clarksville, Virginia).	\N	The title page was not scanned.  This is page 1 of 8.	\N	\N	\N
1204	local	\N	2006-06-14 00:00:00	\N	826	Typed copies of fan mail sent to the Tuskegee Institute Choir, 1937	\N	1	247	\N	1	The title page for this group of letters reads "A sampling of the thousands of fan-mail letters that were received during the series of half-hour broadcasts by the Tuskegee Institute Choir, conducted by William L. Dawson, each Sunday over the NBC Red network 1937-38."\n\nThis page contains a transcription of a letter from R. K. Chesterton (Alvaston, Derby, England).	\N	This is page 2 of 8.	\N	\N	\N
1205	local	\N	2006-06-14 00:00:00	\N	826	Typed copies of fan mail sent to the Tuskegee Institute Choir, 1937	\N	1	247	\N	1	The title page for this group of letters reads "A sampling of the thousands of fan-mail letters that were received during the series of half-hour broadcasts by the Tuskegee Institute Choir, conducted by William L. Dawson, each Sunday over the NBC Red network 1937-38."\n\nThis page contains transcriptions of letters from George Weida Spohn (Northfield, Minnesota) and Nick Kenny (New York Daily Mirror).	\N	This is page 3 of 8.	\N	\N	\N
1206	local	\N	2006-06-14 00:00:00	\N	826	Typed copies of fan mail sent to the Tuskegee Institute Choir, 1937	\N	1	247	\N	1	The title page for this group of letters reads "A sampling of the thousands of fan-mail letters that were received during the series of half-hour broadcasts by the Tuskegee Institute Choir, conducted by William L. Dawson, each Sunday over the NBC Red network 1937-38."\n\nThis page contains a transcription of a letter from H. G. Tilghman (Norfolk Virginian-Pilot).	\N	This is page 4 of 8.	\N	\N	\N
1207	local	\N	2006-06-14 00:00:00	\N	826	Typed copies of fan mail sent to the Tuskegee Institute Choir, 1937	\N	1	247	\N	1	The title page for this group of letters reads "A sampling of the thousands of fan-mail letters that were received during the series of half-hour broadcasts by the Tuskegee Institute Choir, conducted by William L. Dawson, each Sunday over the NBC Red network 1937-38."\n\nThis page contains a transcription of a letter from Evelyn Hultin (Arlington, Virginia).	\N	This is page 5 of 8.	\N	\N	\N
1208	local	\N	2006-06-14 00:00:00	\N	826	Typed copies of fan mail sent to the Tuskegee Institute Choir, 1937	\N	1	247	\N	1	The title page for this group of letters reads "A sampling of the thousands of fan-mail letters that were received during the series of half-hour broadcasts by the Tuskegee Institute Choir, conducted by William L. Dawson, each Sunday over the NBC Red network 1937-38."\n\nThis page contains transcriptions of letters from Samuel M. Subers (Norfolk, Virginia) and Charles Perry (Providence, Rhode Island).	\N	This is page 6 of 8.	\N	\N	\N
1209	local	\N	2006-06-14 00:00:00	\N	826	Typed copies of fan mail sent to the Tuskegee Institute Choir, 1937	\N	1	247	\N	1	The title page for this group of letters reads "A sampling of the thousands of fan-mail letters that were received during the series of half-hour broadcasts by the Tuskegee Institute Choir, conducted by William L. Dawson, each Sunday over the NBC Red network 1937-38."\n\nThis page contains a transcription of a letter from D. Sterling Wheelwright, Chapel Director and Organist, the Washington Chapel, Church of Jesus Christ of Latter Day Saints.	\N	This is page 7 of 8.	\N	\N	\N
1210	local	\N	2006-06-14 00:00:00	\N	826	Typed copies of fan mail sent to the Tuskegee Institute Choir, 1937	\N	1	247	\N	1	The title page for this group of letters reads "A sampling of the thousands of fan-mail letters that were received during the series of half-hour broadcasts by the Tuskegee Institute Choir, conducted by William L. Dawson, each Sunday over the NBC Red network 1937-38."\n\nThis page contains transcriptions of letters from Harry S. Hull, Jr. (Auburn, New York), and Harold V. Milligan (New York, New York).	\N	This is page 8 of 8.	\N	\N	\N
1277	local	\N	2006-06-23 00:00:00	\N	826	Schedule of performances for the Tuskegee Institute Choir during the United Negro Fund Concerts in New York City, 19-20 March 1955	\N	1	247	140	1	This schedule was clipped to a telephone memorandum outlining the rehearsals planned during the trip.	\N	Both the schedule and memorandum were scanned.	\N	\N	\N
1278	local	\N	2006-06-23 00:00:00	\N	826	Telephone memorandum outlining a schedule of performances for the Tuskegee Institute Choir during the United Negro Fund Concerts in New York City, 19-20 March 1955	\N	1	247	\N	1	This memorandum was clipped to a schedule of performances planned during the trip.	\N	Both the schedule and memorandum were scanned.	\N	\N	\N
1280	local	\N	2006-06-23 00:00:00	\N	826	Schedule for the Tuskegee Institute Choir during the United Negro Fund Concerts in New York City, 18-22 March [1955]	(As of March 16)	1	247	\N	1	\N	\N	This is page 2 of 2.	\N	\N	\N
1281	local	\N	2006-06-23 00:00:00	\N	826	Transcript of the Tuskegee Institute Choir Christmas Concert, 23 December 1951	\N	1	247	\N	1	The concert was part of a series presented by ABC in cooperation with the United Negro College Fund.  The transcript was done for WAPX, a radio station in Montgomery, Alabama.	\N	Page 1 of 5.	\N	\N	\N
2	local	00000022	2006-02-28 00:00:00	2006-02-28 00:00:00	826	Recording of the Choral Festival 71, Houston Independent School District, (Houston, Texas,) 13 May 1971	\N	16	25	140	1	William Levi Dawson was the guest conductor of a mixed chorus of 400 voices and a female ensemble of 700 voices drawn from Houston senior high school choruses.  Both the rehearsal and concert were recorded.	\N	This is side A of the audiocassette.	\N	\N	0
1537	local	\N	2006-07-13 00:00:00	\N	826	Photograph of the Tuskegee Institute Choir performing on the steps of a building, [ca. 1935]	\N	9	25	140	1	The choir performs on the steps of a building.  Dawson stands in front of them conducting.	\N	\N	\N	\N	\N
1282	local	\N	2006-06-23 00:00:00	\N	826	Transcript of the Tuskegee Institute Choir Christmas Concert, 23 December 1951	\N	1	247	\N	1	The concert was part of a series presented by ABC in cooperation with the United Negro College Fund.  The transcript was done for WAPX, a radio station in Montgomery, Alabama.	\N	Page 2 of 5.	\N	\N	\N
1283	local	\N	2006-06-23 00:00:00	\N	826	Transcript of the Tuskegee Institute Choir Christmas Concert, 23 December 1951	\N	1	247	\N	1	The concert was part of a series presented by ABC in cooperation with the United Negro College Fund.  The transcript was done for WAPX, a radio station in Montgomery, Alabama.	\N	Page 3 of 5.	\N	\N	\N
1284	local	\N	2006-06-23 00:00:00	\N	826	Transcript of the Tuskegee Institute Choir Christmas Concert, 23 December 1951	\N	1	247	\N	1	The concert was part of a series presented by ABC in cooperation with the United Negro College Fund.  The transcript was done for WAPX, a radio station in Montgomery, Alabama.	\N	Page 4 of 5.	\N	\N	\N
1285	local	\N	2006-06-23 00:00:00	\N	826	Transcript of the Tuskegee Institute Choir Christmas Concert, 23 December 1951	\N	1	247	\N	1	The concert was part of a series presented by ABC in cooperation with the United Negro College Fund.  The transcript was done for WAPX, a radio station in Montgomery, Alabama.	\N	Page 5 of 5.	\N	\N	\N
2028	local	\N	2006-09-11 00:00:00	2006-09-11 00:00:00	611	\N	\N	6	247	140	1	\N	\N	\N	0	\N	0
2029	local	\N	2006-09-11 00:00:00	2006-09-11 00:00:00	611	\N	\N	6	247	140	1	\N	\N	\N	0	\N	0
1592	local	70	2006-07-17 00:00:00	\N	0	The African Trader by W.H.C. Kingston (cover)	\N	1	25	140	1	Carter Woodson Library	\N	Image for Carter G. Woodson exhibit	\N	\N	\N
2034	local	0957-009.tif	2006-09-12 00:00:00	\N	891	John Oliver Killens Biographical Sketch, 1964	\N	1	25	140	1	\N	\N	\N	0	\N	0
2037	local	0957-009.tif	2006-09-12 00:00:00	\N	0	\N	\N	6	25	140	1	\N	\N	\N	0	\N	0
2032	local	0957-015.tif	2006-09-12 00:00:00	\N	891	Biographical Sketch of John Oliver Killens, 1964	\N	6	25	140	1	\N	\N	\N	0	\N	0
2038	local	0957-009.tif	2006-09-12 00:00:00	\N	0	\N	\N	6	25	140	1	\N	\N	\N	0	\N	0
2033	local	0957-009.tif	2006-09-12 00:00:00	\N	891	John Oliver Killens: Clipping, [photograph of Killens receiving a plaque from Ossie Davis,] New York, Amsterdam News, 23 August 1980	\N	9	25	140	1	\N	\N	\N	0	\N	0
2039	local	0957-016.tif	2006-09-12 00:00:00	\N	0	\N	\N	6	25	140	1	\N	\N	\N	0	\N	0
2035	local	0957-016.tif	2006-09-12 00:00:00	\N	891	Funeral program for John Oliver Killens, Bethany Baptist Church, Brooklyn, New York, 16 January, 1988	\N	9	25	140	1	\N	\N	\N	0	\N	0
2040	local	0957-014.tif	2006-09-12 00:00:00	\N	0	\N	\N	6	25	140	1	\N	\N	\N	0	\N	0
2041	local	0957-014.tif	2006-09-12 00:00:00	\N	891	\N	\N	6	25	140	1	\N	\N	\N	0	\N	0
2042	local	\N	2006-09-12 00:00:00	\N	891	\N	\N	6	25	140	1	\N	\N	\N	0	\N	0
2043	local	0957-014.tif	2006-09-12 00:00:00	\N	0	Schedule for John Oliver Killens, Macon, Georgia, 4-19 January, 1986	\N	6	25	140	1	\N	\N	\N	0	\N	0
2044	local	0957-014.tif	2006-09-12 00:00:00	\N	0	\N	\N	6	25	140	1	\N	\N	\N	0	\N	0
2045	local	\N	2006-09-12 00:00:00	\N	0	\N	a	6	25	140	1	\N	\N	\N	0	\N	0
2046	local	0957-014.tif	2006-09-12 00:00:00	\N	0	\N	\N	6	25	140	1	\N	\N	\N	0	\N	0
2047	local	0957-014.tif	2006-09-12 00:00:00	\N	891	\N	\N	6	25	140	1	\N	\N	\N	0	\N	0
2030	local	0957-013.tif	2006-09-12 00:00:00	2006-09-12 00:00:00	891	John Oliver Killens: Poster "The American Race Crisis" lecture series, 1964	\N	1	247	140	1	\N	\N	\N	0	\N	0
2048	local	\N	2006-09-12 00:00:00	\N	0	\N	\N	1	25	140	1	\N	\N	\N	0	\N	0
2049	local	\N	2006-09-12 00:00:00	\N	891	\N	\N	6	25	140	1	\N	\N	\N	0	\N	0
2036	local	0957-014.tif	2006-09-12 00:00:00	\N	891	Schedule for John Oliver Killens, Macon, Georgia, 4-19 January, 1986	\N	1	25	140	1	\N	\N	\N	0	\N	0
2050	local	0957-008.tif	2006-09-12 00:00:00	\N	0	\N	\N	6	25	140	1	\N	\N	\N	0	\N	0
2051	local	0957-008.tif	2006-09-12 00:00:00	\N	891	\N	\N	6	25	140	1	\N	\N	\N	0	\N	0
2052	local	0957-008.tif	2006-09-12 00:00:00	\N	891	\N	\N	1	25	140	1	\N	\N	\N	0	\N	0
2053	local	0957-008a.tif	2006-09-12 00:00:00	\N	\N	\N	\N	6	25	140	1	\N	\N	\N	0	\N	0
2054	local	0957-008a.tif	2006-09-12 00:00:00	\N	0	\N	\N	6	25	140	1	\N	\N	\N	0	\N	0
2055	local	0957-008a.tif	2006-09-12 00:00:00	\N	0	\N	\N	6	25	140	1	\N	\N	\N	0	\N	0
2056	local	0957-008a.tif	2006-09-12 00:00:00	\N	0	\N	\N	6	25	140	1	\N	\N	\N	0	\N	0
2057	local	\N	2006-09-12 00:00:00	\N	891	\N	\N	6	25	140	1	\N	\N	\N	0	\N	0
2058	local	0957a.tif	2006-09-12 00:00:00	\N	0	\N	\N	6	25	140	1	\N	\N	\N	0	\N	0
2059	local	\N	2006-09-12 00:00:00	\N	891	\N	\N	6	25	140	1	\N	\N	\N	0	\N	0
2060	local	\N	2006-09-12 00:00:00	\N	891	\N	\N	6	25	140	1	\N	\N	\N	0	\N	0
2061	local	\N	2006-09-12 00:00:00	\N	891	\N	\N	6	25	140	1	\N	\N	\N	0	\N	0
2062	local	0957-008a.tif	2006-09-12 00:00:00	\N	0	\N	\N	6	25	140	1	\N	\N	\N	0	\N	0
2063	local	\N	2006-09-13 00:00:00	\N	1	\N	\N	6	25	140	1	\N	\N	\N	0	\N	0
2064	local	\N	2006-09-13 00:00:00	\N	198	\N	\N	6	25	140	1	\N	\N	\N	0	\N	0
2065	local	\N	2006-09-13 00:00:00	\N	0	\N	\N	10	25	140	1	\N	\N	\N	0	\N	0
2066	local	\N	2006-09-13 00:00:00	\N	0	\N	\N	6	25	140	1	\N	\N	\N	0	\N	0
2067	local	\N	2006-09-13 00:00:00	\N	1	\N	\N	6	25	140	1	\N	\N	\N	0	\N	0
2068	local	\N	2006-09-13 00:00:00	\N	0	\N	\N	6	25	140	1	\N	\N	\N	0	\N	0
2069	local	\N	2006-09-13 00:00:00	\N	0	\N	\N	10	25	140	1	\N	\N	\N	0	\N	0
2070	local	\N	2006-09-13 00:00:00	\N	0	\N	\N	6	25	140	1	\N	\N	\N	0	\N	0
2071	local	\N	2006-09-13 00:00:00	\N	198	\N	\N	6	25	140	1	\N	\N	\N	0	\N	0
2072	local	\N	2006-09-13 00:00:00	\N	456	\N	\N	6	25	140	1	\N	\N	\N	0	\N	0
2073	local	\N	2006-09-15 00:00:00	\N	0	1001 Things Everyone Should Know About African American History by Jeffrey C. Stewart	\N	1	247	140	1	\N	\N	part of the Carter G. Woodson Library	0	\N	0
2074	local	0957-008a.tif	2006-09-15 00:00:00	\N	0	\N	\N	6	25	140	1	\N	\N	\N	0	\N	0
2077	local	\N	2006-09-15 00:00:00	\N	0	\N	\N	1	25	140	1	\N	\N	\N	0	\N	0
2080	local	0957-008b.tif	2006-09-15 00:00:00	\N	891	\N	\N	1	25	140	1	\N	\N	\N	0	\N	0
2081	local	\N	2006-09-15 00:00:00	\N	891	\N	\N	6	25	140	1	\N	\N	\N	0	\N	0
2076	local	0957-008b.tif	2006-09-15 00:00:00	\N	891	John Oliver Killens: Clipping, "Return to Old South stirs old memories for writer Killens," Atlanta Journal Constitution, 9 February, 1986	\N	1	25	140	1	\N	\N	\N	0	\N	0
2082	local	\N	2006-09-15 00:00:00	\N	891	\N	\N	6	25	140	1	\N	\N	\N	0	\N	0
2083	local	\N	2006-09-15 00:00:00	\N	891	\N	\N	6	25	140	1	\N	\N	\N	0	\N	0
2079	local	0957-007.tif	2006-09-15 00:00:00	\N	891	John Oliver Killens: Book jacket for Youngblood (English)	\N	9	25	140	1	\N	\N	\N	0	\N	0
2084	local	\N	2006-09-15 00:00:00	\N	891	\N	\N	6	25	140	1	\N	\N	\N	0	\N	0
2085	local	\N	2006-09-15 00:00:00	\N	891	\N	\N	6	25	140	1	\N	\N	\N	0	\N	0
2086	local	\N	2006-09-15 00:00:00	\N	891	\N	\N	6	25	140	1	\N	\N	\N	0	\N	0
2087	local	\N	2006-09-15 00:00:00	\N	891	\N	\N	6	25	140	1	\N	\N	\N	0	\N	0
2088	local	\N	2006-09-15 00:00:00	\N	891	\N	\N	6	25	140	1	\N	\N	\N	0	\N	0
2089	local	\N	2006-09-15 00:00:00	\N	891	\N	\N	6	25	140	1	\N	\N	\N	0	\N	0
2090	local	\N	2006-09-15 00:00:00	\N	891	\N	\N	6	25	140	1	\N	\N	\N	0	\N	0
2078	local	0957-011.tif	2006-09-15 00:00:00	\N	891	John Oliver Killens: Book jacket for Youngblood (Russian)	\N	9	25	140	1	\N	\N	\N	0	\N	0
2091	local	\N	2006-09-15 00:00:00	\N	891	\N	\N	9	25	140	1	\N	\N	\N	0	\N	0
2092	local	\N	2006-09-15 00:00:00	\N	891	\N	\N	6	25	140	1	\N	\N	\N	0	\N	0
2093	local	0957-001.tif	2006-09-15 00:00:00	\N	0	\N	\N	6	25	140	1	\N	\N	\N	0	\N	0
2094	local	\N	2006-09-15 00:00:00	\N	891	\N	\N	6	25	140	1	\N	\N	\N	0	\N	0
2095	local	\N	2006-09-15 00:00:00	\N	891	\N	\N	6	25	140	1	\N	\N	\N	0	\N	0
2075	local	0957-008a.tif	2006-09-15 00:00:00	\N	891	John Oliver Killens:  Clipping, "Return to Old South stirs old memories for writer Killens," Atlanta Journal Constitution, 9 February, 1986	\N	1	25	140	1	\N	\N	\N	0	\N	0
2096	local	\N	2006-09-15 00:00:00	\N	891	\N	\N	6	25	140	1	\N	\N	\N	0	\N	0
2097	local	\N	2006-09-15 00:00:00	\N	891	\N	\N	6	25	140	1	\N	\N	\N	0	\N	0
2098	local	0957-001.tif	2006-09-15 00:00:00	\N	0	\N	\N	6	25	140	1	\N	\N	\N	0	\N	0
2099	local	0957-001.tif	2006-09-15 00:00:00	\N	891	\N	\N	6	25	140	1	\N	\N	\N	0	\N	0
2100	local	\N	2006-09-15 00:00:00	\N	891	\N	\N	6	25	140	1	\N	\N	\N	0	\N	0
2101	local	\N	2006-09-15 00:00:00	\N	891	\N	\N	6	25	140	1	\N	\N	\N	0	\N	0
2102	local	0957-001.tif	2006-09-18 00:00:00	\N	891	John Oliver Killens: Photograph from Writers Conference at Fisk University, 22-24 April, 1966	\N	9	25	140	1	\N	\N	\N	0	\N	0
2103	local	\N	2006-09-18 00:00:00	\N	891	\N	\N	6	25	140	1	\N	\N	\N	0	\N	0
2104	local	0957-005.tif	2006-09-18 00:00:00	\N	0	\N	\N	6	25	140	1	\N	\N	\N	0	\N	0
2105	local	\N	2006-09-18 00:00:00	\N	891	\N	\N	6	25	140	1	\N	\N	\N	0	\N	0
2106	local	\N	2006-09-18 00:00:00	\N	891	\N	\N	6	25	140	1	\N	\N	\N	0	\N	0
2107	local	\N	2006-09-18 00:00:00	\N	891	\N	\N	6	25	140	1	\N	\N	\N	0	\N	0
2108	local	\N	2006-09-18 00:00:00	\N	0	\N	\N	9	25	140	1	\N	\N	\N	0	\N	0
2109	local	0957-005.tif	2006-09-18 00:00:00	\N	891	John Oliver Killens: Book jacket for The Adventures of John Henry, A Man Ain't Nothin' But a Man (English,  Little, Brown)	\N	9	25	140	1	\N	\N	\N	0	\N	0
2110	local	0957-006.tif	2006-09-18 00:00:00	\N	891	John Oliver Killens: Book jacket for And Then We Heard the Thunder (English, Knopf)	\N	9	25	140	1	\N	\N	\N	0	\N	0
2111	local	0957-012.tif	2006-09-18 00:00:00	\N	891	John Oliver Killens: Book jacket for And Then We Heard the Thunder (Russian)	\N	9	25	140	1	\N	\N	\N	0	\N	0
2113	local	\N	2006-09-19 00:00:00	\N	0	\N	\N	6	25	140	1	\N	\N	\N	0	\N	0
2114	local	\N	2006-09-19 00:00:00	\N	752	\N	\N	6	25	140	1	\N	\N	\N	0	\N	0
2115	local	\N	2006-09-19 00:00:00	\N	752	Old Ordnance Survey Maps [back cover], The Falls, 1931	\N	9	247	140	1	This map of The Falls is the third in a series published for Belfast.  It is the Godfrey Edition and contains an essay by Ciaran Carson.  The map was published by Alan Godfrey in 1989.	\N	\N	0	\N	0
2112	local	\N	2006-09-19 00:00:00	\N	752	Old Ordnance Survey Maps [front cover], The Falls, 1931	\N	9	247	\N	1	This map of The Falls is the third in a series published for Belfast.  It is the Godfrey Edition and contains an essay by Ciaran Carson.  The map was published by Alan Godfrey in 1989.	\N	\N	0	\N	0
2116	local	\N	2006-09-19 00:00:00	\N	752	Old Ordnance Survey Maps [inside: upper right quadrant of LX. 12], The Falls, 1931	\N	9	247	140	1	This map of The Falls is the third in a series published for Belfast.  It is the Godfrey Edition and contains an essay by Ciaran Carson.  The map was published by Alan Godfrey in 1989.	\N	\N	2	\N	0
2117	local	\N	2006-09-19 00:00:00	\N	0	\N	\N	9	25	140	1	\N	\N	\N	0	\N	0
2023	local	\N	2006-09-11 00:00:00	2006-09-11 00:00:00	611	Interview w/ Raymond Andrews, 18 November 1988; WUGA Athens	\N	16	247	140	1	\N	WUGA Special aired 11/18/88, Interview w/Ray Andrews by A. Elam written on cassette.	\N	0	\N	0
2024	local	\N	2006-09-11 00:00:00	2006-09-11 00:00:00	611	Talk at Athens Regional Library, 19 November 1988	\N	16	247	140	1	\N	\N	Raymond Andrews 11-19-88 written on cassette.	0	\N	0
2022	local	\N	2006-09-11 00:00:00	2006-09-11 00:00:00	611	 Interview w/ Raymond Andrews, 12 May 1987; WVOG Athens	\N	16	247	140	1	\N	\N	"The Spoken Word", produced by Rachel Brown/Neil Thompson.	0	\N	0
2025	local	\N	2006-09-11 00:00:00	2006-09-11 00:00:00	611	Review of Baby Sweet's by Joy Tremewan, 17 February 1989, WEVL 1	\N	16	247	140	1	\N	\N	 Title on cassette is Raymond Andrews Papers (Emory U.) "Reading Aloud Here," Feb. 17, 1989.  WEVL, Memphis.	0	\N	0
2026	local	\N	2006-09-11 00:00:00	2006-09-11 00:00:00	611	Review of Baby Sweet's by Joy Tremewan, 17 February 1989, WEVL 2	\N	6	247	140	1	\N	\N	Title on cassette is Raymond Andrews Papers (Emory U.) "Reading Aloud Here," Feb. 17, 1989. WEVL, Memphis.	0	\N	0
2027	local	\N	2006-09-11 00:00:00	2006-09-11 00:00:00	611	Interview w/Raymond Andrews by Joy Tremewan, February 17, 1989	\N	16	247	140	1	\N	\N	Title on cassette: Reading Aloud Here, Raymond Andrews, n.d.	0	\N	0
2118	local	\N	2006-09-19 00:00:00	\N	0	Rationale for restitution : two addresses delivered during the Sunday morning services on June 8, 1969 at 10:30 a.m., followed by a discussion period  [cover: Mr. James Forman at the microphone], St. George's Church, Stuyvesant Square, New York	\N	9	247	140	1	This booklet contains remarks  by The Rev. Edward O. Miller, rector of St. George's Church, and remarks  by Mr. James Forman, chairman of the United Black Appeal.  The addresses are followed by a question and answer period with The Rev. Miller and Mr. Forman  in Olmsted Hall.  The address and staff of St. George's Church is listed on the back of the pamphlet.  Woodruff Special Collections copy is from the library of Vincent Harding.	\N	\N	0	\N	0
2121	local	\N	2006-09-20 00:00:00	\N	0	\N	\N	6	25	140	1	\N	\N	\N	0	\N	0
2120	local	\N	2006-09-20 00:00:00	\N	\N	Rationale for restitution : two addresses delivered during the Sunday morning services on June 8, 1969 at 10:30 a.m., followed by a discussion period  [inside: Mr. James Forman at the microphone], St. George's Church, Stuyvesant Square, New York	\N	9	247	\N	1	This booklet contains remarks  by The Rev. Edward O. Miller, rector of St. George's Church, and remarks  by Mr. James Forman, chairman of the United Black Appeal.  The addresses are followed by a question and answer period with The Rev. Miller and Mr. Forman  in Olmsted Hall.  The address and staff of St. George's Church is listed on the back of the pamphlet.  Woodruff Special Collections copy is from the library of Vincent	\N	\N	0	\N	0
2122	local	\N	2006-09-20 00:00:00	\N	0	Rationale for restitution : two addresses delivered during the Sunday morning services on June 8, 1969 at 10:30 a.m., followed by a discussion period  [photograph: Young American for Freedom picket], St. George's Church, Stuyvesant Square, New York	\N	9	247	140	1	This booklet contains remarks  by The Rev. Edward O. Miller, rector of St. George's Church, and remarks  by Mr. James Forman, chairman of the United Black Appeal.  The addresses are followed by a question and answer period with The Rev. Miller and Mr. Forman  in Olmsted Hall.  The address and staff of St. George's Church is listed on the back of the pamphlet.  Woodruff Special Collections copy is from the library of Vincent Harding.	\N	\N	0	\N	0
2123	local	\N	2006-09-20 00:00:00	\N	0	Rationale for restitution : two addresses delivered during the Sunday morning services on June 8, 1969 at 10:30 a.m., followed by a discussion period  [photograph: Question and Answer period], St. George's Church, Stuyvesant Square, New York	\N	9	247	140	1	This booklet contains remarks  by The Rev. Edward O. Miller, rector of St. George's Church, and remarks  by Mr. James Forman, chairman of the United Black Appeal.  The addresses are followed by a question and answer period with The Rev. Miller and Mr. Forman  in Olmsted Hall.  The address and staff of St. George's Church is listed on the back of the pamphlet.  Woodruff Special Collections copy is from the library of Vincent Harding.	\N	\N	0	\N	0
2124	local	\N	2006-09-20 00:00:00	\N	0	Travels through the interior of Africa [ image: A Man and Woman of Bahaharana in the dress of the Country, page 384]; Christian Frederick Damberger;  translated from German; 1801	\N	9	247	140	1	This book  is an account of a fictitious voyage from the Cape of Good Hope to Morocco between the years 1781-1797 . It was written in collaboration with a certain "Magister Junge", who also assisted the author in compiling two other fictitious voyages. Damberger is an alternate pseudonym for Taurinius (the real name is unknown).	\N	\N	0	\N	0
\.


--
-- Data for TOC entry 222 (OID 12741787)
-- Name: ScannerCamera; Type: TABLE DATA; Schema: public; Owner: jbwhite
--

COPY "ScannerCamera" ("ID", "ScannerCameraModelName", "ScannerCameraModelNnumber", "ScannerCameraManufacturer", "ScannerCameraSoftware") FROM stdin;
1	MARBL scanner	scanner1 model number	scanner1 maker	\N
2	Phase One digital camera	\N	\N	\N
3	ECIT scanner 1	\N	\N	\N
4	ECIT scanner 2	\N	\N	\N
5	MARBL handheld digital camera	\N	\N	\N
6	PRES handheld digital camera	\N	\N	\N
\.


--
-- Data for TOC entry 223 (OID 12741801)
-- Name: Target; Type: TABLE DATA; Schema: public; Owner: jbwhite
--

COPY "Target" ("ID", "TargetName", "TargetPub", "TargetExtLocation") FROM stdin;
1	Kodak color control patches (small)	\N	\N
2	Kodak gray scale (small)	\N	\N
3	Kodak color control patches (large)	\N	\N
4	Kodak gray scale (large)	\N	\N
5	Kodak Professional Q60 Color Input target	\N	\N
6	QP card	\N	\N
7	None	\N	\N
8	Other - record in Image Note field	\N	\N
9	Gretag MacBeth ColorChecker chart	\N	\N
\.


--
-- Data for TOC entry 224 (OID 12741822)
-- Name: TechSound; Type: TABLE DATA; Schema: public; Owner: jbwhite
--

COPY "TechSound" ("ID", "Content#", "FormatName", "ByteOrder", "CompressionScheme", "FileSize", "CodecCreator", "CodecQuality", "Methodology", "BitsPerSample", "SamplingFrequency", "SoundNote", "Duration", "DateCaptured", "FileLoc", "SoundClip") FROM stdin;
282	1	wav	Big Endian (Mac)	\N	526900	1	lossless	\N	24	44.1	\N	004743	\N	\N	\N
283	2	wav	Big Endian (Mac)	\N	456900	1	lossless	\N	24	44.1	\N	003006	\N	\N	\N
284	3	wav	Big Endian (Mac)	\N	635500	1	lossless	\N	24	44.1	\N	004151	\N	\N	\N
285	4	wav	Big Endian (Mac)	\N	410100	1	lossless	\N	16	44.1	\N	004021	\N	\N	\N
286	5	wav	Big Endian (Mac)	\N	146200	1	lossless	\N	16	44.1	\N	001423	\N	\N	\N
287	6	wav	Big Endian (Mac)	\N	0	1	lossless	\N	24	48	\N	004554	\N	\N	\N
288	7	wav	Big Endian (Mac)	\N	653300	1	lossless	\N	16	44.1	\N	004301	\N	\N	\N
289	8	wav	Big Endian (Mac)	\N	320400	1	lossless	\N	16	44.1	\N	003135	\N	\N	\N
290	9	wav	Big Endian (Mac)	\N	480600	1	lossless	\N	16	44.1	\N	004718	\N	\N	\N
291	10	wav	Big Endian (Mac)	\N	261265	1	lossless	\N	16	44.1	\N	002506	\N	\N	\N
292	11	wav	Big Endian (Mac)	\N	153900	1	lossless	\N	16	44.1	\N	001508	\N	\N	\N
293	12	wav	Big Endian (Mac)	\N	484600	1	lossless	\N	16	44.1	\N	004741	\N	\N	\N
294	13	wav	Big Endian (Mac)	\N	167600	1	lossless	\N	24	44.1	\N	001629	\N	\N	\N
295	14	wav	Big Endian (Mac)	\N	439500	1	lossless	\N	16	44.1	\N	004332	\N	\N	\N
296	15	wav	Big Endian (Mac)	\N	623400	1	lossless	\N	24	44.1	\N	004110	\N	\N	\N
297	16	wav	Big Endian (Mac)	\N	343800	1	lossless	\N	24	44.1	\N	002242	\N	\N	\N
298	17	wav	Big Endian (Mac)	\N	403400	1	lossless	\N	24	44.1	\N	002345	\N	\N	\N
299	18	wav	Big Endian (Mac)	\N	651327	1	lossless	\N	24	44.1	\N	004200	\N	\N	\N
300	19	wav	Big Endian (Mac)	\N	165036	1	lossless	\N	24	44.1	\N	004200	\N	\N	\N
301	20	wav	Big Endian (Mac)	\N	293521	1	lossless	\N	24	44.1	\N	001855	\N	\N	\N
302	21	wav	Big Endian (Mac)	\N	716600	1	lossless	\N	24	44.1	\N	004720	\N	\N	\N
303	22	wav	Big Endian (Mac)	\N	478600	1	lossless	\N	24	44.1	\N	003136	\N	\N	\N
304	23	wav	Big Endian (Mac)	\N	694700	1	lossless	\N	24	44.1	\N	004540	\N	\N	\N
305	24	wav	Big Endian (Mac)	\N	720400	1	lossless	\N	24	44.1	\N	004722	\N	\N	\N
306	25	wav	Big Endian (Mac)	\N	43000	1	lossless	\N	24	44.1	\N	000249	\N	\N	\N
307	26	wav	Big Endian (Mac)	\N	721000	1	lossless	\N	24	44.1	\N	004736	\N	\N	\N
308	27	wav	Big Endian (Mac)	\N	191000	1	lossless	\N	24	44.1	\N	001236	\N	\N	\N
309	28	wav	Big Endian (Mac)	\N	703800	1	lossless	\N	24	44.1	\N	004629	\N	\N	\N
310	29	wav	Big Endian (Mac)	\N	475000	1	lossless	\N	24	44.1	\N	003122	\N	\N	\N
311	30	wav	Big Endian (Mac)	\N	720000	1	lossless	\N	24	44.1	\N	004732	\N	\N	\N
312	31	wav	Big Endian (Mac)	\N	638800	1	lossless	\N	24	44.1	\N	004240	\N	\N	\N
313	32	wav	Big Endian (Mac)	\N	85400	1	lossless	\N	24	44.1	\N	000530	\N	\N	\N
314	33	wav	Big Endian (Mac)	\N	390800	1	lossless	\N	24	44.1	\N	002141	\N	\N	\N
315	34	wav	Big Endian (Mac)	\N	0	1	lossless	\N	24	48	\N	000000	\N	\N	\N
316	35	wav	Big Endian (Mac)	\N	0	1	lossless	\N	24	48	\N	000000	\N	\N	\N
317	36	wav	Big Endian (Mac)	\N	893600	1	lossless	\N	24	48	\N	004300	\N	\N	\N
318	37	wav	Big Endian (Mac)	\N	652300	1	lossless	\N	24	48	\N	004000	\N	\N	\N
319	38	wav	Big Endian (Mac)	\N	715600	1	lossless	\N	24	48	\N	004325	\N	\N	\N
320	39	wav	Big Endian (Mac)	\N	0	1	lossless	\N	24	48	\N	\N	\N	\N	\N
321	40	wav	Big Endian (Mac)	\N	46300	1	lossless	\N	24	48	\N	000250	\N	\N	\N
322	41	wav	Big Endian (Mac)	\N	0	1	lossless	\N	24	48	\N	\N	\N	\N	\N
323	42	wav	Big Endian (Mac)	\N	762900	1	lossless	\N	24	48	\N	004520	\N	\N	\N
324	43	wav	Big Endian (Mac)	\N	49300	1	lossless	\N	24	48	\N	000300	\N	\N	\N
325	44	wav	Big Endian (Mac)	\N	777300	1	lossless	\N	24	48	\N	004710	\N	\N	\N
326	45	wav	Big Endian (Mac)	\N	69700	1	lossless	\N	24	48	\N	000413	\N	\N	\N
327	46	wav	Big Endian (Mac)	\N	794000	1	lossless	\N	24	48	\N	004800	\N	\N	\N
328	47	wav	Big Endian (Mac)	\N	79000	1	lossless	\N	24	48	\N	000446	\N	\N	\N
329	48	wav	Big Endian (Mac)	\N	655600	1	lossless	\N	24	48	\N	003947	\N	\N	\N
330	49	wav	Big Endian (Mac)	\N	129400	1	lossless	\N	24	48	\N	000749	\N	\N	\N
331	50	wav	Big Endian (Mac)	\N	779300	1	lossless	\N	24	48	\N	004717	\N	\N	\N
332	51	wav	Big Endian (Mac)	\N	778700	1	lossless	\N	24	48	\N	004715	\N	\N	\N
333	52	wav	Big Endian (Mac)	\N	708300	1	lossless	\N	24	48	\N	004258	\N	\N	\N
334	53	wav	Big Endian (Mac)	\N	782000	1	lossless	\N	24	48	\N	004727	\N	\N	\N
335	54	wav	Big Endian (Mac)	\N	785200	1	lossless	\N	24	48	\N	004738	\N	\N	\N
336	55	wav	Big Endian (Mac)	\N	298200	1	lossless	\N	24	48	\N	001805	\N	\N	\N
337	56	wav	Big Endian (Mac)	\N	487800	1	lossless	\N	24	48	\N	002936	\N	\N	\N
338	57	wav	Big Endian (Mac)	\N	783400	1	lossless	\N	24	48	\N	004732	\N	\N	\N
339	58	wav	Big Endian (Mac)	\N	784300	1	lossless	\N	24	48	\N	004735	\N	\N	\N
340	59	wav	Big Endian (Mac)	\N	784500	1	lossless	\N	24	48	\N	004736	\N	\N	\N
341	60	wav	Big Endian (Mac)	\N	414100	1	lossless	\N	24	48	\N	002507	\N	\N	\N
342	61	wav	Big Endian (Mac)	\N	782600	1	lossless	\N	24	48	\N	004729	\N	\N	\N
343	62	wav	Big Endian (Mac)	\N	779000	1	lossless	\N	24	48	\N	004716	\N	\N	\N
344	63	wav	Big Endian (Mac)	\N	318600	1	lossless	\N	24	48	\N	001920	\N	\N	\N
345	64	wav	Big Endian (Mac)	\N	780800	1	lossless	\N	24	48	\N	004722	\N	\N	\N
346	65	wav	Big Endian (Mac)	\N	805100	1	lossless	\N	24	48	\N	004851	\N	\N	\N
347	66	wav	Big Endian (Mac)	\N	781400	1	lossless	\N	24	48	\N	004725	\N	\N	\N
348	67	wav	Big Endian (Mac)	\N	791000	1	lossless	\N	24	48	\N	004800	\N	\N	\N
349	68	wav	Big Endian (Mac)	\N	782700	1	lossless	\N	24	48	\N	004730	\N	\N	\N
350	69	wav	Big Endian (Mac)	\N	184300	1	lossless	\N	24	48	\N	001111	\N	\N	\N
351	70	wav	Big Endian (Mac)	\N	780600	1	lossless	\N	24	48	\N	004722	\N	\N	\N
352	71	wav	Big Endian (Mac)	\N	781800	1	lossless	\N	24	48	\N	004726	\N	\N	\N
353	72	wav	Big Endian (Mac)	\N	785200	1	lossless	\N	24	48	\N	004738	\N	\N	\N
354	73	wav	Big Endian (Mac)	\N	775900	1	lossless	\N	24	48	\N	004705	\N	\N	\N
355	74	wav	Big Endian (Mac)	\N	782700	1	lossless	\N	24	48	\N	004729	\N	\N	\N
356	75	wav	Big Endian (Mac)	\N	781500	1	lossless	\N	24	48	\N	004725	\N	\N	\N
357	76	wav	Big Endian (Mac)	\N	780300	1	lossless	\N	24	48	\N	004720	\N	\N	\N
358	77	wav	Big Endian (Mac)	\N	234400	1	lossless	\N	24	48	\N	001413	\N	\N	\N
359	78	wav	Big Endian (Mac)	\N	778900	1	lossless	\N	24	48	\N	004715	\N	\N	\N
360	79	wav	Big Endian (Mac)	\N	199900	1	lossless	\N	24	48	\N	001208	\N	\N	\N
361	80	wav	Big Endian (Mac)	\N	555600	1	lossless	\N	24	48	\N	003343	\N	\N	\N
362	81	wav	Big Endian (Mac)	\N	583000	1	lossless	\N	24	48	\N	003522	\N	\N	\N
363	82	wav	Big Endian (Mac)	\N	782600	1	lossless	\N	24	48	\N	004729	\N	\N	\N
364	83	wav	Big Endian (Mac)	\N	784100	1	lossless	\N	24	48	\N	004735	\N	\N	\N
365	84	wav	Big Endian (Mac)	\N	1030000	1	lossless	\N	24	48	\N	010420	\N	\N	\N
366	85	wav	Big Endian (Mac)	\N	547100	1	lossless	\N	24	48	\N	003311	\N	\N	\N
367	86	wav	Big Endian (Mac)	\N	518500	1	lossless	\N	24	48	\N	010255	\N	\N	\N
368	87	wav	Big Endian (Mac)	\N	478000	1	lossless	\N	24	48	\N	005800	\N	\N	\N
369	88	wav	Big Endian (Mac)	\N	274000	1	lossless	\N	24	48	\N	003320	\N	\N	\N
370	89	wav	Big Endian (Mac)	\N	538038	1	lossless	\N	24	48	\N	010346	\N	\N	\N
371	90	wav	Big Endian (Mac)	\N	49600	1	lossless	\N	24	44.1	\N	000630	\N	\N	\N
372	91	wav	Big Endian (Mac)	\N	61300	1	lossless	\N	24	44.1	\N	000802	\N	\N	\N
373	92	wav	Big Endian (Mac)	\N	70600	1	lossless	\N	24	44.1	\N	000915	\N	\N	\N
374	93	wav	Big Endian (Mac)	\N	37600	1	lossless	\N	24	44.1	\N	000456	\N	\N	\N
375	94	wav	Big Endian (Mac)	\N	59000	1	lossless	\N	24	44.1	\N	000744	\N	\N	\N
376	95	wav	Big Endian (Mac)	\N	56900	1	lossless	\N	24	44.1	\N	000728	\N	\N	\N
377	96	wav	Big Endian (Mac)	\N	61000	1	lossless	\N	24	44.1	\N	000800	\N	\N	\N
378	97	wav	Big Endian (Mac)	\N	46399	1	lossless	\N	24	44.1	\N	000556	\N	\N	\N
379	98	wav	Big Endian (Mac)	\N	56500	1	lossless	\N	24	44.1	\N	000724	\N	\N	\N
380	99	wav	Big Endian (Mac)	\N	59700	1	lossless	\N	24	44.1	\N	000749	\N	\N	\N
381	100	wav	Big Endian (Mac)	\N	65800	1	lossless	\N	24	44.1	\N	000837	\N	\N	\N
382	101	wav	Big Endian (Mac)	\N	40500	1	lossless	\N	24	44.1	\N	000519	\N	\N	\N
383	102	wav	Big Endian (Mac)	\N	27200	1	lossless	\N	24	44.1	\N	000334	\N	\N	\N
384	103	wav	Big Endian (Mac)	\N	26500	1	lossless	\N	24	44.1	\N	000329	\N	\N	\N
385	104	wav	Big Endian (Mac)	\N	33600	1	lossless	\N	24	44.1	\N	000424	\N	\N	\N
386	105	wav	Big Endian (Mac)	\N	25413	1	lossless	\N	24	44.1	\N	000315	\N	\N	\N
387	106	wav	Big Endian (Mac)	\N	28000	1	lossless	\N	24	44.1	\N	000340	\N	\N	\N
388	107	wav	Big Endian (Mac)	\N	28200	1	lossless	\N	24	44.1	\N	000342	\N	\N	\N
389	108	wav	Big Endian (Mac)	\N	28600	1	lossless	\N	24	44.1	\N	000345	\N	\N	\N
390	109	wav	Big Endian (Mac)	\N	33600	1	lossless	\N	24	44.1	\N	000425	\N	\N	\N
391	110	wav	Big Endian (Mac)	\N	36200	1	lossless	\N	24	44.1	\N	000445	\N	\N	\N
392	111	wav	Big Endian (Mac)	\N	27300	1	lossless	\N	24	44.1	\N	000335	\N	\N	\N
393	112	wav	Big Endian (Mac)	\N	36400	1	lossless	\N	24	44.1	\N	000446	\N	\N	\N
394	113	wav	Big Endian (Mac)	\N	34418	1	lossless	\N	24	44.1	\N	000424	\N	\N	\N
395	114	wav	Big Endian (Mac)	\N	317000	1	lossless	\N	24	44.1	\N	002052	\N	\N	\N
396	115	wav	Big Endian (Mac)	\N	276000	1	lossless	\N	24	44.1	\N	001812	\N	\N	\N
397	116	wav	Big Endian (Mac)	\N	324000	1	lossless	\N	24	44.1	\N	002121	\N	\N	\N
398	117	wav	Big Endian (Mac)	\N	278000	1	lossless	\N	24	44.1	\N	001817	\N	\N	\N
399	118	wav	Big Endian (Mac)	\N	32300	1	lossless	\N	24	44.1	\N	000414	\N	\N	\N
400	119	wav	Big Endian (Mac)	\N	39300	1	lossless	\N	24	44.1	\N	000509	\N	\N	\N
401	120	wav	Big Endian (Mac)	\N	30900	1	lossless	\N	24	44.1	\N	000403	\N	\N	\N
402	121	wav	Big Endian (Mac)	\N	26800	1	lossless	\N	24	44.1	\N	000331	\N	\N	\N
403	122	wav	Big Endian (Mac)	\N	19600	1	lossless	\N	24	44.1	\N	000234	\N	\N	\N
404	123	wav	Big Endian (Mac)	\N	47600	1	lossless	\N	24	44.1	\N	000614	\N	\N	\N
405	124	wav	Big Endian (Mac)	\N	46200	1	lossless	\N	24	44.1	\N	000603	\N	\N	\N
406	125	wav	Big Endian (Mac)	\N	183000	1	lossless	\N	24	44.1	\N	002403	\N	\N	\N
407	126	wav	Big Endian (Mac)	\N	210000	1	lossless	\N	24	44.1	\N	002738	\N	\N	\N
408	127	wav	Big Endian (Mac)	\N	44900	1	lossless	\N	24	44.1	\N	000553	\N	\N	\N
409	128	wav	Big Endian (Mac)	\N	44900	1	lossless	\N	24	44.1	\N	000553	\N	\N	\N
410	129	wav	Big Endian (Mac)	\N	43800	1	lossless	\N	24	44.1	\N	000545	\N	\N	\N
411	130	wav	Big Endian (Mac)	\N	39000	1	lossless	\N	24	44.1	\N	000507	\N	\N	\N
412	131	wav	Big Endian (Mac)	\N	21000	1	lossless	\N	24	44.1	\N	000245	\N	\N	\N
413	132	wav	Big Endian (Mac)	\N	24900	1	lossless	\N	24	44.1	\N	000316	\N	\N	\N
414	133	wav	Big Endian (Mac)	\N	17800	1	lossless	\N	24	44.1	\N	000220	\N	\N	\N
415	134	wav	Big Endian (Mac)	\N	17300	1	lossless	\N	24	44.1	\N	000216	\N	\N	\N
416	135	wav	Big Endian (Mac)	\N	28900	1	lossless	\N	24	44.1	\N	000347	\N	\N	\N
417	136	wav	Big Endian (Mac)	\N	33300	1	lossless	\N	24	44.1	\N	000422	\N	\N	\N
418	137	wav	Big Endian (Mac)	\N	18200	1	lossless	\N	24	44.1	\N	000223	\N	\N	\N
419	138	wav	Big Endian (Mac)	\N	22400	1	lossless	\N	24	44.1	\N	000256	\N	\N	\N
420	139	wav	Big Endian (Mac)	\N	94900	1	lossless	\N	24	44.1	\N	001227	\N	\N	\N
421	140	wav	Big Endian (Mac)	\N	71900	1	lossless	\N	24	44.1	\N	000926	\N	\N	\N
422	141	wav	Big Endian (Mac)	\N	10100	1	lossless	\N	24	44.1	\N	000119	\N	\N	\N
423	142	wav	Big Endian (Mac)	\N	31700	1	lossless	\N	24	44.1	\N	000409	\N	\N	\N
424	143	wav	Big Endian (Mac)	\N	30700	1	lossless	\N	24	44.1	\N	000401	\N	\N	\N
425	144	wav	Big Endian (Mac)	\N	10100	1	lossless	\N	24	44.1	\N	000119	\N	\N	\N
426	145	wav	Big Endian (Mac)	\N	114200	1	lossless	\N	24	44.1	\N	001459	\N	\N	\N
427	146	wav	Big Endian (Mac)	\N	113800	1	lossless	\N	24	44.1	\N	001455	\N	\N	\N
428	147	wav	Big Endian (Mac)	\N	17900	1	lossless	\N	24	44.1	\N	000221	\N	\N	\N
429	148	wav	Big Endian (Mac)	\N	21800	1	lossless	\N	24	44.1	\N	000251	\N	\N	\N
430	149	wav	Big Endian (Mac)	\N	31300	1	lossless	\N	24	44.1	\N	000406	\N	\N	\N
431	150	wav	Big Endian (Mac)	\N	35600	1	lossless	\N	24	44.1	\N	000440	\N	\N	\N
432	151	wav	Big Endian (Mac)	\N	25400	1	lossless	\N	24	44.1	\N	000320	\N	\N	\N
433	152	wav	Big Endian (Mac)	\N	27300	1	lossless	\N	24	44.1	\N	000334	\N	\N	\N
434	153	wav	Big Endian (Mac)	\N	27300	1	lossless	\N	24	44.1	\N	000238	\N	\N	\N
435	154	wav	Big Endian (Mac)	\N	27300	1	lossless	\N	24	44.1	\N	000335	\N	\N	\N
436	155	wav	Big Endian (Mac)	\N	41200	1	lossless	\N	24	44.1	\N	000524	\N	\N	\N
437	156	wav	Big Endian (Mac)	\N	25400	1	lossless	\N	24	44.1	\N	000320	\N	\N	\N
438	157	wav	Big Endian (Mac)	\N	76600	1	lossless	\N	24	44.1	\N	001002	\N	\N	\N
439	158	wav	Big Endian (Mac)	\N	66500	1	lossless	\N	24	44.1	\N	000843	\N	\N	\N
440	159	wav	Big Endian (Mac)	\N	62700	1	lossless	\N	24	44.1	\N	000813	\N	\N	\N
441	160	wav	Big Endian (Mac)	\N	74900	1	lossless	\N	24	44.1	\N	000949	\N	\N	\N
442	161	wav	Big Endian (Mac)	\N	34200	1	lossless	\N	24	44.1	\N	000429	\N	\N	\N
443	162	wav	Big Endian (Mac)	\N	25200	1	lossless	\N	24	44.1	\N	000318	\N	\N	\N
444	163	wav	Big Endian (Mac)	\N	26000	1	lossless	\N	24	44.1	\N	000325	\N	\N	\N
445	164	wav	Big Endian (Mac)	\N	23000	1	lossless	\N	24	44.1	\N	000301	\N	\N	\N
446	165	wav	Big Endian (Mac)	\N	36200	1	lossless	\N	24	44.1	\N	000445	\N	\N	\N
447	166	wav	Big Endian (Mac)	\N	38800	1	lossless	\N	24	44.1	\N	000505	\N	\N	\N
448	167	wav	Big Endian (Mac)	\N	16100	1	lossless	\N	24	44.1	\N	000206	\N	\N	\N
449	168	wav	Big Endian (Mac)	\N	36100	1	lossless	\N	24	44.1	\N	000444	\N	\N	\N
450	169	wav	Big Endian (Mac)	\N	37800	1	lossless	\N	24	44.1	\N	000458	\N	\N	\N
451	170	wav	Big Endian (Mac)	\N	36800	1	lossless	\N	24	44.1	\N	000449	\N	\N	\N
452	171	wav	Big Endian (Mac)	\N	26300	1	lossless	\N	24	48	\N	000327	\N	\N	\N
453	172	wav	Big Endian (Mac)	\N	41300	1	lossless	\N	24	44.1	\N	000525	\N	\N	\N
454	173	wav	Big Endian (Mac)	\N	37500	1	lossless	\N	24	44.1	\N	000455	\N	\N	\N
455	174	wav	Big Endian (Mac)	\N	37500	1	lossless	\N	24	44.1	\N	000455	\N	\N	\N
456	175	wav	Big Endian (Mac)	\N	34100	1	lossless	\N	24	44.1	\N	000429	\N	\N	\N
457	176	wav	Big Endian (Mac)	\N	29500	1	lossless	\N	24	44.1	\N	000352	\N	\N	\N
458	177	wav	Big Endian (Mac)	\N	41000	1	lossless	\N	24	44.1	\N	000523	\N	\N	\N
459	178	wav	Big Endian (Mac)	\N	22800	1	lossless	\N	24	44.1	\N	000300	\N	\N	\N
460	179	wav	Big Endian (Mac)	\N	20800	\N	lossless	\N	24	44.1	\N	000243	\N	\N	\N
461	180	wav	Big Endian (Mac)	\N	22000	1	lossless	\N	24	44.1	\N	000253	\N	\N	\N
462	181	wav	Big Endian (Mac)	\N	42500	1	lossless	\N	24	44.1	\N	000534	\N	\N	\N
463	182	wav	Big Endian (Mac)	\N	14600	1	lossless	\N	24	44.1	\N	000154	\N	\N	\N
464	183	wav	Big Endian (Mac)	\N	36800	1	lossless	\N	24	44.1	\N	000449	\N	\N	\N
465	184	wav	Big Endian (Mac)	\N	42900	1	lossless	\N	24	44.1	\N	000537	\N	\N	\N
466	185	wav	Big Endian (Mac)	\N	41900	1	lossless	\N	24	44.1	\N	000529	\N	\N	\N
467	186	wav	Big Endian (Mac)	\N	42600	1	lossless	\N	24	44.1	\N	000535	\N	\N	\N
468	187	wav	Big Endian (Mac)	\N	41300	1	lossless	\N	24	44.1	\N	000525	\N	\N	\N
469	188	wav	Big Endian (Mac)	\N	23300	1	lossless	\N	24	44.1	\N	000304	\N	\N	\N
470	189	wav	Big Endian (Mac)	\N	40900	1	lossless	\N	24	44.1	\N	000522	\N	\N	\N
471	190	wav	Big Endian (Mac)	\N	41000	1	lossless	\N	24	44.1	\N	000522	\N	\N	\N
472	191	wav	Big Endian (Mac)	\N	31500	1	lossless	\N	24	44.1	\N	000408	\N	\N	\N
473	192	wav	Big Endian (Mac)	\N	38700	1	lossless	\N	24	44.1	\N	000504	\N	\N	\N
474	193	wav	Big Endian (Mac)	\N	40600	1	lossless	\N	24	44.1	\N	000520	\N	\N	\N
475	194	wav	Big Endian (Mac)	\N	40500	1	lossless	\N	24	44.1	\N	000518	\N	\N	\N
476	195	wav	Big Endian (Mac)	\N	27400	1	lossless	\N	24	44.1	\N	000336	\N	\N	\N
477	196	wav	Big Endian (Mac)	\N	19800	1	lossless	\N	24	44.1	\N	000235	\N	\N	\N
478	197	wav	Big Endian (Mac)	\N	34000	1	lossless	\N	24	44.1	\N	000427	\N	\N	\N
479	198	wav	Big Endian (Mac)	\N	42500	1	lossless	\N	24	44.1	\N	000534	\N	\N	\N
480	199	wav	Big Endian (Mac)	\N	40000	1	lossless	\N	24	44.1	\N	000515	\N	\N	\N
481	200	wav	Big Endian (Mac)	\N	41900	\N	lossless	\N	24	44.1	\N	000530	\N	\N	\N
482	201	wav	Big Endian (Mac)	\N	34700	1	lossless	\N	24	44.1	\N	000433	\N	\N	\N
483	202	wav	Big Endian (Mac)	\N	39000	1	lossless	\N	24	44.1	\N	000507	\N	\N	\N
484	203	wav	Big Endian (Mac)	\N	28400	1	lossless	\N	24	44.1	\N	000343	\N	\N	\N
485	204	wav	Big Endian (Mac)	\N	36000	1	lossless	\N	24	44.1	\N	000443	\N	\N	\N
486	205	wav	Big Endian (Mac)	\N	35300	1	lossless	\N	24	44.1	\N	000438	\N	\N	\N
487	206	wav	Big Endian (Mac)	\N	53900	1	lossless	\N	24	44.1	\N	000704	\N	\N	\N
488	207	wav	Big Endian (Mac)	\N	54800	1	lossless	\N	24	44.1	\N	000733	\N	\N	\N
489	208	wav	Big Endian (Mac)	\N	54800	1	lossless	\N	24	44.1	\N	000711	\N	\N	\N
490	209	wav	Big Endian (Mac)	\N	60100	1	lossless	\N	24	44.1	\N	000752	\N	\N	\N
491	210	wav	Big Endian (Mac)	\N	90500	1	lossless	\N	24	44.1	\N	001152	\N	\N	\N
492	211	wav	Big Endian (Mac)	\N	80100	1	lossless	\N	24	44.1	\N	001030	\N	\N	\N
493	212	wav	Big Endian (Mac)	\N	55100	1	lossless	\N	24	44.1	\N	000714	\N	\N	\N
494	213	wav	Big Endian (Mac)	\N	126900	1	lossless	\N	24	44.1	\N	001638	\N	\N	\N
495	214	wav	Big Endian (Mac)	\N	74600	1	lossless	\N	24	44.1	\N	000947	\N	\N	\N
496	215	wav	Big Endian (Mac)	\N	103300	1	lossless	\N	24	44.1	\N	001332	\N	\N	\N
497	216	wav	Big Endian (Mac)	\N	96600	1	lossless	\N	24	44.1	\N	001240	\N	\N	\N
498	217	wav	Big Endian (Mac)	\N	91300	1	lossless	\N	24	44.1	\N	001159	\N	\N	\N
499	218	wav	Big Endian (Mac)	\N	131100	1	lossless	\N	24	44.1	\N	001712	\N	\N	\N
500	219	wav	Big Endian (Mac)	\N	101900	1	lossless	\N	24	44.1	\N	001322	\N	\N	\N
501	220	wav	Big Endian (Mac)	\N	31300	1	lossless	\N	24	44.1	\N	000408	\N	\N	\N
502	221	wav	Big Endian (Mac)	\N	23000	1	lossless	\N	24	44.1	\N	000301	\N	\N	\N
503	222	wav	Big Endian (Mac)	\N	26400	1	lossless	\N	24	44.1	\N	000328	\N	\N	\N
504	223	wav	Big Endian (Mac)	\N	26200	1	lossless	\N	24	44.1	\N	000326	\N	\N	\N
505	224	wav	Big Endian (Mac)	\N	39600	1	lossless	\N	24	44.1	\N	000512	\N	\N	\N
506	225	wav	Big Endian (Mac)	\N	22800	1	lossless	\N	24	44.1	\N	000259	\N	\N	\N
507	226	wav	Big Endian (Mac)	\N	25800	1	lossless	\N	24	44.1	\N	000323	\N	\N	\N
508	227	wav	Big Endian (Mac)	\N	25200	1	lossless	\N	24	44.1	\N	000318	\N	\N	\N
509	228	wav	Big Endian (Mac)	\N	27900	1	lossless	\N	24	44.1	\N	000340	\N	\N	\N
510	229	wav	Big Endian (Mac)	\N	32400	1	lossless	\N	24	44.1	\N	000415	\N	\N	\N
511	230	wav	Big Endian (Mac)	\N	42600	1	lossless	\N	24	44.1	\N	000535	\N	\N	\N
512	231	wav	Big Endian (Mac)	\N	23100	1	lossless	\N	24	44.1	\N	000302	\N	\N	\N
513	232	wav	Big Endian (Mac)	\N	24900	1	lossless	\N	24	44.1	\N	000316	\N	\N	\N
514	233	wav	Big Endian (Mac)	\N	442797	1	lossless	\N	24	48	\N	002610	\N	\N	\N
515	234	wav	Big Endian (Mac)	\N	1300	1	lossless	\N	24	48	\N	002658	\N	\N	\N
516	235	wav	Big Endian (Mac)	\N	792874	1	lossless	\N	24	48	\N	004659	\N	\N	\N
517	236	wav	Big Endian (Mac)	\N	681846	1	lossless	\N	24	48	\N	004014	\N	\N	\N
518	237	wav	Big Endian (Mac)	\N	115779	1	lossless	\N	24	48	\N	000649	\N	\N	\N
519	238	wav	Big Endian (Mac)	\N	0	1	lossless	\N	24	48	\N	\N	\N	\N	\N
520	239	wav	Big Endian (Mac)	\N	381794	1	lossless	\N	24	48	\N	002231	\N	\N	\N
521	240	wav	Big Endian (Mac)	\N	414773	1	lossless	\N	24	48	\N	002428	\N	\N	\N
522	241	wav	Big Endian (Mac)	\N	794025	1	lossless	\N	24	48	\N	004710	\N	\N	\N
523	242	wav	Big Endian (Mac)	\N	782026	1	lossless	\N	24	48	\N	004628	\N	\N	\N
524	243	wav	Big Endian (Mac)	\N	813425	1	lossless	\N	24	48	\N	004800	\N	\N	\N
525	244	wav	Big Endian (Mac)	\N	494100	1	lossless	\N	24	48	\N	002909	\N	\N	\N
526	245	wav	Big Endian (Mac)	\N	800828	1	lossless	\N	24	48	\N	004715	\N	\N	\N
527	246	wav	Big Endian (Mac)	\N	147994	1	lossless	\N	24	48	\N	000844	\N	\N	\N
528	247	wav	Big Endian (Mac)	\N	799656	1	lossless	\N	24	48	\N	004711	\N	\N	\N
529	248	wav	Big Endian (Mac)	\N	588416	1	lossless	\N	24	48	\N	003443	\N	\N	\N
530	249	wav	Big Endian (Mac)	\N	43632	1	lossless	\N	24	48	\N	000234	\N	\N	\N
531	250	wav	Big Endian (Mac)	\N	492803	1	lossless	\N	24	48	\N	004721	\N	\N	\N
532	251	wav	Big Endian (Mac)	\N	138763	1	lossless	\N	16	44.1	\N	001320	\N	\N	\N
533	252	wav	Big Endian (Mac)	\N	450838	1	lossless	\N	16	44.1	\N	004319	\N	\N	\N
534	253	wav	Big Endian (Mac)	\N	431461	1	lossless	\N	16	44.1	\N	004127	\N	\N	\N
535	254	wav	Big Endian (Mac)	\N	62095	1	lossless	\N	16	44.1	\N	000558	\N	\N	\N
536	255	wav	Big Endian (Mac)	\N	379475	1	lossless	\N	16	44.1	\N	002421	\N	\N	\N
537	256	wav	Big Endian (Mac)	\N	245983	1	lossless	\N	16	44.1	\N	002338	\N	\N	\N
538	257	wav	Big Endian (Mac)	\N	23973	1	lossless	\N	16	44.1	\N	000218	\N	\N	\N
539	258	wav	Big Endian (Mac)	\N	768411	1	lossless	\N	24	48	\N	004530	\N	\N	\N
540	259	wav	Big Endian (Mac)	\N	774872	1	lossless	\N	24	48	\N	004543	\N	\N	\N
541	260	wav	Big Endian (Mac)	\N	797318	1	lossless	\N	24	48	\N	004705	\N	\N	\N
542	261	wav	Big Endian (Mac)	\N	798758	1	lossless	\N	24	48	\N	004719	\N	\N	\N
543	262	wav	Big Endian (Mac)	\N	796992	1	lossless	\N	24	48	\N	004713	\N	\N	\N
544	263	wav	Big Endian (Mac)	\N	264143	1	lossless	\N	24	48	\N	001538	\N	\N	\N
545	264	wav	Big Endian (Mac)	\N	801649	1	lossless	\N	24	48	\N	004730	\N	\N	\N
546	265	wav	Big Endian (Mac)	\N	796913	1	lossless	\N	24	48	\N	004713	\N	\N	\N
547	266	wav	Big Endian (Mac)	\N	801873	1	lossless	\N	24	48	\N	004713	\N	\N	\N
548	267	wav	Big Endian (Mac)	\N	720819	1	lossless	\N	24	48	\N	004242	\N	\N	\N
549	268	wav	Big Endian (Mac)	\N	797120	1	lossless	\N	24	48	\N	004714	\N	\N	\N
550	269	wav	Big Endian (Mac)	\N	799671	1	lossless	\N	24	48	\N	004723	\N	\N	\N
551	270	wav	Big Endian (Mac)	\N	800320	1	lossless	\N	24	48	\N	004725	\N	\N	\N
552	271	wav	Big Endian (Mac)	\N	803605	1	lossless	\N	24	48	\N	004737	\N	\N	\N
553	272	wav	Big Endian (Mac)	\N	0	1	lossless	\N	24	48	\N	004702	\N	\N	\N
554	273	wav	Big Endian (Mac)	\N	0	1	lossless	\N	24	48	\N	004720	\N	\N	\N
555	274	wav	Big Endian (Mac)	\N	41092	1	lossless	\N	24	44.1	\N	000515	\N	\N	\N
556	275	wav	Big Endian (Mac)	\N	38041	1	lossless	\N	24	44.1	\N	000452	\N	\N	\N
557	276	wav	Big Endian (Mac)	\N	4128	1	lossless	\N	16	44.1	\N	000023	\N	\N	\N
558	277	wav	Big Endian (Mac)	\N	12130	1	lossless	\N	16	44.1	\N	000110	\N	\N	\N
559	278	wav	Big Endian (Mac)	\N	1312	1	lossless	\N	16	44.1	\N	000007	\N	\N	\N
560	279	wav	Big Endian (Mac)	\N	8632	1	lossless	\N	16	44.1	\N	000050	\N	\N	\N
561	280	wav	Big Endian (Mac)	\N	1689	1	lossless	\N	16	44.1	\N	000009	\N	\N	\N
562	281	wav	Big Endian (Mac)	\N	12447	1	lossless	\N	16	44.1	\N	000112	\N	\N	\N
563	282	wav	Big Endian (Mac)	\N	3198	1	lossless	\N	16	44.1	\N	000018	\N	\N	\N
564	283	wav	Big Endian (Mac)	\N	8207	1	lossless	\N	16	44.1	\N	000047	\N	\N	\N
565	284	wav	Big Endian (Mac)	\N	873	1	lossless	\N	16	44.1	\N	000005	\N	\N	\N
566	285	wav	Big Endian (Mac)	\N	7100	1	lossless	\N	16	44.1	\N	000041	\N	\N	\N
567	286	wav	Big Endian (Mac)	\N	1461	1	lossless	\N	16	44.1	\N	000008	\N	\N	\N
568	287	wav	Big Endian (Mac)	\N	6135	1	lossless	\N	16	44.1	\N	000035	\N	\N	\N
569	288	wav	Big Endian (Mac)	\N	710	1	lossless	\N	16	44.1	\N	000004	\N	\N	\N
570	289	wav	Big Endian (Mac)	\N	4776	1	lossless	\N	16	44.1	\N	000027	\N	\N	\N
571	290	wav	Big Endian (Mac)	\N	1686	1	lossless	\N	16	44.1	\N	000009	\N	\N	\N
572	291	wav	Big Endian (Mac)	\N	11715	1	lossless	\N	16	44.1	\N	000108	\N	\N	\N
573	292	wav	Big Endian (Mac)	\N	731	1	lossless	\N	16	44.1	\N	000004	\N	\N	\N
574	293	wav	Big Endian (Mac)	\N	15741	1	lossless	\N	16	44.1	\N	000131	\N	\N	\N
575	294	wav	Big Endian (Mac)	\N	1007	1	lossless	\N	16	44.1	\N	000005	\N	\N	\N
576	295	wav	Big Endian (Mac)	\N	7114	1	lossless	\N	16	44.1	\N	000041	\N	\N	\N
577	296	wav	Big Endian (Mac)	\N	1041	1	lossless	\N	16	44.1	\N	000006	\N	\N	\N
578	297	wav	Big Endian (Mac)	\N	8600	1	lossless	\N	16	44.1	\N	000049	\N	\N	\N
579	298	wav	Big Endian (Mac)	\N	1480	1	lossless	\N	16	44.1	\N	000008	\N	\N	\N
580	299	wav	Big Endian (Mac)	\N	7727	1	lossless	\N	16	44.1	\N	000044	\N	\N	\N
581	300	wav	Big Endian (Mac)	\N	692	1	lossless	\N	16	44.1	\N	000004	\N	\N	\N
582	301	wav	Big Endian (Mac)	\N	9898	1	lossless	\N	16	44.1	\N	000057	\N	\N	\N
583	302	wav	Big Endian (Mac)	\N	22177	1	lossless	\N	16	44.1	\N	000208	\N	\N	\N
584	303	wav	Big Endian (Mac)	\N	8347	1	lossless	\N	16	44.1	\N	000048	\N	\N	\N
585	304	wav	Big Endian (Mac)	\N	60925	1	lossless	\N	16	44.1	\N	000553	\N	\N	\N
586	305	wav	Big Endian (Mac)	\N	14165	1	lossless	\N	16	44.1	\N	000122	\N	\N	\N
587	306	wav	Big Endian (Mac)	\N	51561	1	lossless	\N	16	44.1	\N	000459	\N	\N	\N
588	307	wav	Big Endian (Mac)	\N	30312	1	lossless	\N	16	44.1	\N	000255	\N	\N	\N
589	308	wav	Big Endian (Mac)	\N	30103	1	lossless	\N	16	44.1	\N	000254	\N	\N	\N
590	309	wav	Big Endian (Mac)	\N	39323	1	lossless	\N	16	44.1	\N	000348	\N	\N	\N
591	310	wav	Big Endian (Mac)	\N	18438	1	lossless	\N	16	44.1	\N	000147	\N	\N	\N
592	311	wav	Big Endian (Mac)	\N	28137	1	lossless	\N	16	44.1	\N	000243	\N	\N	\N
593	312	wav	Big Endian (Mac)	\N	9755	1	lossless	\N	16	44.1	\N	000056	\N	\N	\N
594	313	wav	Big Endian (Mac)	\N	10957	1	lossless	\N	16	44.1	\N	000103	\N	\N	\N
595	314	wav	Big Endian (Mac)	\N	16483	1	lossless	\N	16	44.1	\N	000135	\N	\N	\N
596	315	wav	Big Endian (Mac)	\N	11905	1	lossless	\N	16	44.1	\N	000109	\N	\N	\N
597	316	wav	Big Endian (Mac)	\N	31061	1	lossless	\N	16	44.1	\N	000300	\N	\N	\N
598	317	wav	Big Endian (Mac)	\N	5722	1	lossless	\N	16	44.1	\N	000033	\N	\N	\N
599	318	wav	Big Endian (Mac)	\N	12932	1	lossless	\N	16	44.1	\N	000115	\N	\N	\N
600	319	wav	Big Endian (Mac)	\N	12151	1	lossless	\N	16	44.1	\N	000110	\N	\N	\N
601	320	wav	Big Endian (Mac)	\N	10849	1	lossless	\N	16	44.1	\N	000102	\N	\N	\N
602	321	wav	Big Endian (Mac)	\N	11894	1	lossless	\N	16	44.1	\N	000109	\N	\N	\N
603	322	wav	Big Endian (Mac)	\N	11177	1	lossless	\N	16	44.1	\N	000104	\N	\N	\N
604	323	wav	Big Endian (Mac)	\N	27981	1	lossless	\N	16	44.1	\N	000242	\N	\N	\N
605	324	wav	Big Endian (Mac)	\N	9705	1	lossless	\N	16	44.1	\N	000056	\N	\N	\N
606	325	wav	Big Endian (Mac)	\N	6073	1	lossless	\N	16	44.1	\N	000035	\N	\N	\N
607	326	wav	Big Endian (Mac)	\N	4597	1	lossless	\N	16	44.1	\N	000026	\N	\N	\N
608	327	wav	Big Endian (Mac)	\N	4238	1	lossless	\N	16	44.1	\N	000024	\N	\N	\N
609	328	wav	Big Endian (Mac)	\N	8786	1	lossless	\N	16	44.1	\N	000051	\N	\N	\N
610	329	wav	Big Endian (Mac)	\N	7341	1	lossless	\N	16	44.1	\N	000042	\N	\N	\N
611	330	wav	Big Endian (Mac)	\N	3163	1	lossless	\N	16	44.1	\N	000018	\N	\N	\N
612	331	wav	Big Endian (Mac)	\N	12411	1	lossless	\N	16	44.1	\N	000112	\N	\N	\N
613	332	wav	Big Endian (Mac)	\N	11071	1	lossless	\N	16	44.1	\N	000104	\N	\N	\N
614	333	wav	Big Endian (Mac)	\N	22255	1	lossless	\N	16	44.1	\N	000209	\N	\N	\N
615	334	wav	Big Endian (Mac)	\N	57801	1	lossless	\N	16	44.1	\N	000535	\N	\N	\N
616	335	wav	Big Endian (Mac)	\N	68192	1	lossless	\N	16	44.1	\N	000635	\N	\N	\N
617	336	wav	Big Endian (Mac)	\N	13568	1	lossless	\N	16	44.1	\N	000118	\N	\N	\N
618	337	wav	Big Endian (Mac)	\N	23488	1	lossless	\N	16	44.1	\N	000216	\N	\N	\N
619	338	wav	Big Endian (Mac)	\N	31677	1	lossless	\N	16	44.1	\N	000303	\N	\N	\N
620	339	wav	Big Endian (Mac)	\N	31732	1	lossless	\N	16	44.1	\N	000304	\N	\N	\N
621	340	wav	Big Endian (Mac)	\N	32198	1	lossless	\N	16	44.1	\N	000306	\N	\N	\N
622	341	wav	Big Endian (Mac)	\N	31431	1	lossless	\N	16	44.1	\N	000302	\N	\N	\N
623	342	wav	Big Endian (Mac)	\N	24161	1	lossless	\N	16	44.1	\N	000220	\N	\N	\N
624	343	wav	Big Endian (Mac)	\N	2770	1	lossless	\N	16	44.1	\N	000241	\N	\N	\N
625	344	wav	Big Endian (Mac)	\N	9794	1	lossless	\N	16	44.1	\N	000056	\N	\N	\N
626	345	wav	Big Endian (Mac)	\N	31328	1	lossless	\N	16	44.1	\N	000301	\N	\N	\N
627	346	wav	Big Endian (Mac)	\N	24258	1	lossless	\N	16	44.1	\N	000220	\N	\N	\N
628	347	wav	Big Endian (Mac)	\N	23709	1	lossless	\N	16	44.1	\N	000217	\N	\N	\N
629	348	wav	Big Endian (Mac)	\N	13881	1	lossless	\N	16	44.1	\N	000120	\N	\N	\N
630	349	wav	Big Endian (Mac)	\N	15422	1	lossless	\N	16	44.1	\N	000129	\N	\N	\N
631	350	wav	Big Endian (Mac)	\N	33930	1	lossless	\N	16	44.1	\N	000316	\N	\N	\N
632	351	wav	Big Endian (Mac)	\N	32253	1	lossless	\N	16	44.1	\N	000307	\N	\N	\N
633	352	wav	Big Endian (Mac)	\N	19926	1	lossless	\N	16	44.1	\N	000155	\N	\N	\N
634	353	wav	Big Endian (Mac)	\N	31484	1	lossless	\N	16	44.1	\N	000302	\N	\N	\N
635	354	wav	Big Endian (Mac)	\N	24754	1	lossless	\N	16	44.1	\N	000223	\N	\N	\N
636	355	wav	Big Endian (Mac)	\N	14269	1	lossless	\N	16	44.1	\N	000122	\N	\N	\N
637	356	wav	Big Endian (Mac)	\N	5322	1	lossless	\N	16	44.1	\N	000030	\N	\N	\N
638	357	wav	Big Endian (Mac)	\N	39640	1	lossless	\N	16	44.1	\N	000350	\N	\N	\N
639	358	wav	Big Endian (Mac)	\N	11382	1	lossless	\N	16	44.1	\N	000106	\N	\N	\N
640	359	wav	Big Endian (Mac)	\N	10465	1	lossless	\N	16	44.1	\N	000100	\N	\N	\N
641	360	wav	Big Endian (Mac)	\N	32244	1	lossless	\N	16	44.1	\N	000307	\N	\N	\N
642	361	wav	Big Endian (Mac)	\N	27689	1	lossless	\N	16	44.1	\N	000240	\N	\N	\N
643	362	wav	Big Endian (Mac)	\N	39959	1	lossless	\N	16	44.1	\N	000351	\N	\N	\N
644	363	wav	Big Endian (Mac)	\N	13977	1	lossless	\N	16	44.1	\N	000121	\N	\N	\N
645	364	wav	Big Endian (Mac)	\N	31043	1	lossless	\N	16	44.1	\N	000300	\N	\N	\N
646	365	wav	Big Endian (Mac)	\N	7385	1	lossless	\N	16	44.1	\N	000042	\N	\N	\N
647	366	wav	Big Endian (Mac)	\N	7472	1	lossless	\N	16	44.1	\N	000043	\N	\N	\N
648	367	wav	Big Endian (Mac)	\N	61141	1	lossless	\N	16	44.1	\N	000554	\N	\N	\N
649	368	wav	Big Endian (Mac)	\N	62352	1	lossless	\N	16	44.1	\N	000601	\N	\N	\N
650	369	wav	Big Endian (Mac)	\N	20020	1	lossless	\N	16	44.1	\N	000156	\N	\N	\N
651	370	wav	Big Endian (Mac)	\N	19976	1	lossless	\N	16	44.1	\N	000155	\N	\N	\N
652	371	wav	Big Endian (Mac)	\N	16138	1	lossless	\N	16	44.1	\N	000133	\N	\N	\N
653	372	wav	Big Endian (Mac)	\N	6829	1	lossless	\N	16	44.1	\N	000039	\N	\N	\N
654	373	wav	Big Endian (Mac)	\N	23796	1	lossless	\N	16	44.1	\N	000218	\N	\N	\N
655	374	wav	Big Endian (Mac)	\N	2392	1	lossless	\N	16	44.1	\N	000013	\N	\N	\N
656	375	wav	Big Endian (Mac)	\N	16047	1	lossless	\N	16	44.1	\N	000133	\N	\N	\N
657	376	wav	Big Endian (Mac)	\N	14361	1	lossless	\N	16	44.1	\N	000123	\N	\N	\N
658	377	wav	Big Endian (Mac)	\N	33760	1	lossless	\N	16	44.1	\N	000315	\N	\N	\N
659	378	wav	Big Endian (Mac)	\N	12610	1	lossless	\N	16	44.1	\N	000113	\N	\N	\N
660	379	wav	Big Endian (Mac)	\N	11705	1	lossless	\N	16	44.1	\N	000107	\N	\N	\N
661	380	wav	Big Endian (Mac)	\N	11333	1	lossless	\N	16	44.1	\N	000105	\N	\N	\N
662	381	wav	Big Endian (Mac)	\N	12466	1	lossless	\N	16	44.1	\N	000112	\N	\N	\N
663	382	wav	Big Endian (Mac)	\N	24811	1	lossless	\N	16	44.1	\N	000224	\N	\N	\N
664	383	wav	Big Endian (Mac)	\N	28519	1	lossless	\N	16	44.1	\N	000245	\N	\N	\N
665	384	wav	Big Endian (Mac)	\N	27009	1	lossless	\N	16	44.1	\N	000236	\N	\N	\N
666	385	wav	Big Endian (Mac)	\N	29906	1	lossless	\N	16	44.1	\N	000253	\N	\N	\N
667	386	wav	Big Endian (Mac)	\N	13952	1	lossless	\N	16	44.1	\N	000120	\N	\N	\N
668	387	wav	Big Endian (Mac)	\N	13405	1	lossless	\N	16	44.1	\N	000117	\N	\N	\N
669	388	wav	Big Endian (Mac)	\N	9489	1	lossless	\N	16	44.1	\N	000055	\N	\N	\N
670	389	wav	Big Endian (Mac)	\N	11554	1	lossless	\N	16	44.1	\N	000107	\N	\N	\N
671	390	wav	Big Endian (Mac)	\N	16301	1	lossless	\N	16	44.1	\N	000134	\N	\N	\N
672	391	wav	Big Endian (Mac)	\N	7929	1	lossless	\N	16	44.1	\N	000046	\N	\N	\N
673	392	wav	Big Endian (Mac)	\N	6434	1	lossless	\N	16	44.1	\N	000037	\N	\N	\N
674	393	wav	Big Endian (Mac)	\N	12045	1	lossless	\N	16	44.1	\N	000109	\N	\N	\N
675	394	wav	Big Endian (Mac)	\N	23500	1	lossless	\N	16	44.1	\N	000216	\N	\N	\N
676	395	wav	Big Endian (Mac)	\N	17360	1	lossless	\N	16	44.1	\N	000140	\N	\N	\N
677	396	wav	Big Endian (Mac)	\N	26180	1	lossless	\N	16	44.1	\N	000231	\N	\N	\N
678	397	wav	Big Endian (Mac)	\N	34382	1	lossless	\N	16	44.1	\N	000319	\N	\N	\N
679	398	wav	Big Endian (Mac)	\N	3385	1	lossless	\N	16	44.1	\N	000019	\N	\N	\N
680	399	wav	Big Endian (Mac)	\N	37807	1	lossless	\N	16	44.1	\N	000339	\N	\N	\N
681	400	wav	Big Endian (Mac)	\N	30266	1	lossless	\N	16	44.1	\N	000255	\N	\N	\N
682	401	wav	Big Endian (Mac)	\N	19262	1	lossless	\N	16	44.1	\N	000151	\N	\N	\N
683	402	wav	Big Endian (Mac)	\N	26217	1	lossless	\N	16	44.1	\N	000232	\N	\N	\N
684	403	wav	Big Endian (Mac)	\N	5150	1	lossless	\N	16	44.1	\N	000029	\N	\N	\N
685	404	wav	Big Endian (Mac)	\N	20032	1	lossless	\N	16	44.1	\N	000156	\N	\N	\N
686	405	wav	Big Endian (Mac)	\N	44983	1	lossless	\N	16	44.1	\N	000421	\N	\N	\N
687	406	wav	Big Endian (Mac)	\N	20647	1	lossless	\N	16	44.1	\N	000159	\N	\N	\N
688	407	wav	Big Endian (Mac)	\N	19400	1	lossless	\N	16	44.1	\N	000152	\N	\N	\N
689	408	wav	Big Endian (Mac)	\N	25372	1	lossless	\N	16	44.1	\N	000227	\N	\N	\N
690	409	wav	Big Endian (Mac)	\N	23589	1	lossless	\N	16	44.1	\N	000216	\N	\N	\N
691	410	wav	Big Endian (Mac)	\N	30322	1	lossless	\N	16	44.1	\N	000256	\N	\N	\N
692	411	wav	Big Endian (Mac)	\N	16612	1	lossless	\N	16	44.1	\N	000136	\N	\N	\N
693	412	wav	Big Endian (Mac)	\N	47420	1	lossless	\N	16	44.1	\N	000435	\N	\N	\N
694	413	wav	Big Endian (Mac)	\N	6446	1	lossless	\N	16	44.1	\N	000037	\N	\N	\N
695	414	wav	Big Endian (Mac)	\N	35115	1	lossless	\N	16	44.1	\N	000323	\N	\N	\N
696	415	wav	Big Endian (Mac)	\N	57461	1	lossless	\N	16	44.1	\N	000533	\N	\N	\N
697	416	wav	Big Endian (Mac)	\N	46409	1	lossless	\N	16	44.1	\N	000429	\N	\N	\N
698	417	wav	Big Endian (Mac)	\N	54912	1	lossless	\N	16	44.1	\N	000518	\N	\N	\N
699	418	wav	Big Endian (Mac)	\N	36944	1	lossless	\N	16	44.1	\N	000334	\N	\N	\N
700	419	wav	Big Endian (Mac)	\N	25333	1	lossless	\N	16	44.1	\N	000227	\N	\N	\N
701	420	wav	Big Endian (Mac)	\N	16908	1	lossless	\N	16	44.1	\N	000138	\N	\N	\N
702	421	wav	Big Endian (Mac)	\N	284300	1	lossless	\N	24	48	\N	001708	\N	\N	\N
703	422	wav	Big Endian (Mac)	\N	524900	1	lossless	\N	24	48	\N	003148	\N	\N	\N
704	423	wav	Big Endian (Mac)	\N	526600	1	lossless	\N	24	48	\N	003157	\N	\N	\N
705	424	wav	Big Endian (Mac)	\N	527900	1	lossless	\N	24	48	\N	003205	\N	\N	\N
706	425	wav	Big Endian (Mac)	\N	521700	1	lossless	\N	24	48	\N	003154	\N	\N	\N
707	426	wav	Big Endian (Mac)	\N	529500	1	lossless	\N	24	48	\N	003233	\N	\N	\N
708	427	wav	Big Endian (Mac)	\N	57300	1	lossless	\N	24	48	\N	003256	\N	\N	\N
709	428	wav	Big Endian (Mac)	\N	527200	1	lossless	\N	24	48	\N	003223	\N	\N	\N
710	429	wav	Big Endian (Mac)	\N	548200	1	lossless	\N	24	48	\N	003311	\N	\N	\N
711	430	wav	Big Endian (Mac)	\N	522900	1	lossless	\N	24	48	\N	003202	\N	\N	\N
712	431	wav	Big Endian (Mac)	\N	565500	1	lossless	\N	24	48	\N	003445	\N	\N	\N
713	432	wav	Big Endian (Mac)	\N	726088	1	lossless	\N	24	48	\N	004301	\N	\N	\N
714	433	wav	Big Endian (Mac)	\N	0	1	lossless	\N	24	48	\N	004301	\N	\N	\N
715	434	wav	Big Endian (Mac)	\N	549413	1	lossless	\N	24	48	\N	003257	\N	\N	\N
716	435	wav	Big Endian (Mac)	\N	570194	1	lossless	\N	24	48	\N	003347	\N	\N	\N
717	436	wav	Big Endian (Mac)	\N	337290	1	lossless	\N	24	48	\N	002007	\N	\N	\N
718	437	wav	Big Endian (Mac)	\N	368497	1	lossless	\N	24	48	\N	002150	\N	\N	\N
719	438	wav	Big Endian (Mac)	\N	298834	1	lossless	\N	24	48	\N	001755	\N	\N	\N
720	439	wav	Big Endian (Mac)	\N	342582	1	lossless	\N	24	48	\N	002031	\N	\N	\N
721	440	wav	Big Endian (Mac)	\N	62066	1	lossless	\N	24	48	\N	000340	\N	\N	\N
722	441	wav	Big Endian (Mac)	\N	479599	1	lossless	\N	24	48	\N	002820	\N	\N	\N
723	442	wav	Big Endian (Mac)	\N	46496	1	lossless	\N	24	48	\N	000245	\N	\N	\N
724	443	wav	Big Endian (Mac)	\N	80882	1	lossless	\N	24	48	\N	000447	\N	\N	\N
725	444	wav	Big Endian (Mac)	\N	15760	1	lossless	\N	24	48	\N	000055	\N	\N	\N
726	445	wav	Big Endian (Mac)	\N	533298	1	lossless	\N	24	48	\N	003135	\N	\N	\N
727	446	wav	Big Endian (Mac)	\N	560007	1	lossless	\N	24	48	\N	003310	\N	\N	\N
728	447	wav	Big Endian (Mac)	\N	528827	1	lossless	\N	24	48	\N	003120	\N	\N	\N
729	448	wav	Big Endian (Mac)	\N	543067	1	lossless	\N	24	48	\N	003218	\N	\N	\N
730	449	wav	Big Endian (Mac)	\N	550020	1	lossless	\N	24	48	\N	003235	\N	\N	\N
731	450	wav	Big Endian (Mac)	\N	398183	1	lossless	\N	24	48	\N	\N	\N	\N	\N
732	451	wav	Big Endian (Mac)	\N	422704	1	lossless	\N	24	48	\N	002526	\N	\N	\N
733	452	wav	Big Endian (Mac)	\N	1139995	1	lossless	\N	24	48	\N	010732	\N	\N	\N
734	453	wav	Big Endian (Mac)	\N	541462	1	lossless	\N	24	48	\N	003223	\N	\N	\N
735	454	wav	Big Endian (Mac)	\N	151007	1	lossless	\N	24	48	\N	000852	\N	\N	\N
736	455	wav	Big Endian (Mac)	\N	539774	1	lossless	\N	24	48	\N	003159	\N	\N	\N
737	456	wav	Big Endian (Mac)	\N	521000	1	lossless	\N	24	48	\N	003152	\N	\N	\N
738	457	wav	Big Endian (Mac)	\N	456100	1	lossless	\N	24	48	\N	002752	\N	\N	\N
739	458	wav	Big Endian (Mac)	\N	482500	1	lossless	\N	24	48	\N	002934	\N	\N	\N
740	459	wav	Big Endian (Mac)	\N	54000	1	lossless	\N	24	48	\N	003301	\N	\N	\N
741	460	wav	Big Endian (Mac)	\N	543200	1	lossless	\N	24	48	\N	003250	\N	\N	\N
742	461	wav	Big Endian (Mac)	\N	69000	1	lossless	\N	24	48	\N	000410	\N	\N	\N
743	462	wav	Big Endian (Mac)	\N	58100	1	lossless	\N	24	48	\N	000330	\N	\N	\N
744	463	wav	Big Endian (Mac)	\N	42600	1	lossless	\N	24	48	\N	000247	\N	\N	\N
745	464	wav	Big Endian (Mac)	\N	59200	1	lossless	\N	24	48	\N	000332	\N	\N	\N
746	465	wav	Big Endian (Mac)	\N	0	1	lossless	\N	24	48	\N	000000	\N	\N	\N
747	466	wav	Big Endian (Mac)	\N	0	1	lossless	\N	24	48	\N	003138	\N	\N	\N
748	467	wav	Big Endian (Mac)	\N	0	1	lossless	\N	24	48	\N	003014	\N	\N	\N
749	468	wav	Big Endian (Mac)	\N	0	1	lossless	\N	24	48	\N	003307	\N	\N	\N
750	469	wav	Big Endian (Mac)	\N	0	1	lossless	\N	24	48	\N	003232	\N	\N	\N
751	470	wav	Big Endian (Mac)	\N	0	1	lossless	\N	24	48	\N	002832	\N	\N	\N
752	471	wav	Big Endian (Mac)	\N	0	1	lossless	\N	24	48	\N	003121	\N	\N	\N
753	472	wav	Big Endian (Mac)	\N	0	1	lossless	\N	24	48	\N	003507	\N	\N	\N
754	473	wav	Big Endian (Mac)	\N	0	1	lossless	\N	24	48	\N	002850	\N	\N	\N
755	474	wav	Big Endian (Mac)	\N	0	1	lossless	\N	24	48	\N	003210	\N	\N	\N
756	475	wav	Big Endian (Mac)	\N	0	1	lossless	\N	24	48	\N	003202	\N	\N	\N
757	476	wav	Big Endian (Mac)	\N	0	1	lossless	\N	24	48	\N	003116	\N	\N	\N
758	477	wav	Big Endian (Mac)	\N	0	1	lossless	\N	24	48	\N	003107	\N	\N	\N
759	478	wav	Big Endian (Mac)	\N	804009	1	lossless	\N	24	48	\N	004738	\N	\N	\N
760	479	wav	Big Endian (Mac)	\N	799622	1	lossless	\N	24	48	\N	004723	\N	\N	\N
761	480	wav	Big Endian (Mac)	\N	0	1	lossless	\N	24	48	\N	004607	\N	\N	\N
762	481	wav	Big Endian (Mac)	\N	0	1	lossless	\N	24	48	\N	004730	\N	\N	\N
763	482	wav	Big Endian (Mac)	\N	0	1	lossless	\N	24	48	\N	004714	\N	\N	\N
764	483	wav	Big Endian (Mac)	\N	0	1	lossless	\N	24	48	\N	004719	\N	\N	\N
765	484	wav	Big Endian (Mac)	\N	0	1	lossless	\N	24	48	\N	004731	\N	\N	\N
766	485	wav	Big Endian (Mac)	\N	0	1	lossless	\N	24	48	\N	004730	\N	\N	\N
767	486	wav	Big Endian (Mac)	\N	0	1	lossless	\N	24	48	\N	003150	\N	\N	\N
768	487	wav	Big Endian (Mac)	\N	0	1	lossless	\N	24	48	\N	003150	\N	\N	\N
769	488	wav	Big Endian (Mac)	\N	0	1	lossless	\N	24	48	\N	004737	\N	\N	\N
770	489	wav	Big Endian (Mac)	\N	0	1	lossless	\N	24	48	\N	004740	\N	\N	\N
771	490	wav	Big Endian (Mac)	\N	0	1	lossless	\N	24	48	\N	004720	\N	\N	\N
772	491	wav	Big Endian (Mac)	\N	0	1	lossless	\N	24	48	\N	004720	\N	\N	\N
773	492	wav	Big Endian (Mac)	\N	0	2	lossless	\N	24	48	\N	003112	\N	\N	\N
774	493	wav	Big Endian (Mac)	\N	0	2	lossless	\N	24	48	\N	003202	\N	\N	\N
775	494	wav	Big Endian (Mac)	\N	0	2	lossless	\N	24	48	\N	003121	\N	\N	\N
776	495	wav	Big Endian (Mac)	\N	0	2	lossless	\N	24	48	\N	003110	\N	\N	\N
777	496	wav	Big Endian (Mac)	\N	0	2	lossless	\N	24	48	\N	003254	\N	\N	\N
778	497	wav	Big Endian (Mac)	\N	0	2	lossless	\N	24	48	\N	003242	\N	\N	\N
779	498	wav	Big Endian (Mac)	\N	0	2	lossless	\N	24	48	\N	003430	\N	\N	\N
780	499	wav	Big Endian (Mac)	\N	0	2	lossless	\N	24	48	\N	003430	\N	\N	\N
781	500	wav	Big Endian (Mac)	\N	0	2	lossless	\N	24	48	\N	002948	\N	\N	\N
782	501	wav	Big Endian (Mac)	\N	0	2	lossless	\N	24	48	\N	003128	\N	\N	\N
783	502	wav	Big Endian (Mac)	\N	0	2	lossless	\N	24	48	\N	003545	\N	\N	\N
784	503	wav	Big Endian (Mac)	\N	0	2	lossless	\N	24	48	\N	003222	\N	\N	\N
785	504	wav	Big Endian (Mac)	\N	0	1	lossless	\N	24	48	\N	004728	\N	\N	\N
786	505	wav	Big Endian (Mac)	\N	0	1	lossless	\N	24	48	\N	004730	\N	\N	\N
787	506	wav	Big Endian (Mac)	\N	0	1	lossless	\N	24	48	\N	004720	\N	\N	\N
788	507	wav	Big Endian (Mac)	\N	0	1	lossless	\N	24	48	\N	004730	\N	\N	\N
789	508	wav	Big Endian (Mac)	\N	0	1	lossless	\N	24	48	\N	004710	\N	\N	\N
790	509	wav	Big Endian (Mac)	\N	0	1	lossless	\N	24	48	\N	002958	\N	\N	\N
791	510	wav	Big Endian (Mac)	\N	0	2	lossless	\N	24	48	\N	003313	\N	\N	\N
792	511	wav	Big Endian (Mac)	\N	0	2	lossless	\N	24	48	\N	\N	\N	\N	\N
793	512	wav	Big Endian (Mac)	\N	0	2	lossless	\N	24	48	\N	002300	\N	\N	\N
794	513	wav	Big Endian (Mac)	\N	0	2	lossless	\N	24	48	\N	001830	\N	\N	\N
795	514	wav	Big Endian (Mac)	\N	0	2	lossless	\N	24	48	\N	001927	\N	\N	\N
796	515	wav	Big Endian (Mac)	\N	0	2	lossless	\N	24	48	\N	002732	\N	\N	\N
797	516	wav	Big Endian (Mac)	\N	0	1	lossless	\N	24	48	\N	001710	\N	\N	\N
798	517	wav	Big Endian (Mac)	\N	0	1	lossless	\N	24	48	\N	004710	\N	\N	\N
799	518	wav	Big Endian (Mac)	\N	0	1	lossless	\N	24	48	\N	004720	\N	\N	\N
800	519	wav	Big Endian (Mac)	\N	0	1	lossless	\N	24	48	\N	004730	\N	\N	\N
801	520	wav	Big Endian (Mac)	\N	0	1	lossless	\N	24	48	\N	004730	\N	\N	\N
802	521	wav	Big Endian (Mac)	\N	0	1	lossless	\N	\N	\N	\N	003284	\N	\N	\N
803	522	wav	Big Endian (Mac)	\N	0	1	lossless	\N	24	48	\N	004800	\N	\N	\N
804	523	wav	Big Endian (Mac)	\N	0	1	lossless	\N	24	48	\N	004750	\N	\N	\N
805	524	wav	Big Endian (Mac)	\N	0	1	lossless	\N	24	48	\N	003140	\N	\N	\N
806	525	wav	Big Endian (Mac)	\N	0	1	lossless	\N	24	48	\N	003150	\N	\N	\N
807	526	wav	Big Endian (Mac)	\N	0	1	lossless	\N	24	48	\N	004720	\N	\N	\N
808	527	wav	Big Endian (Mac)	\N	0	1	lossless	\N	24	48	\N	004720	\N	\N	\N
809	528	wav	Big Endian (Mac)	\N	0	1	lossless	\N	24	48	\N	004720	\N	\N	\N
810	529	wav	Big Endian (Mac)	\N	0	1	lossless	\N	24	48	\N	003148	\N	\N	\N
811	530	wav	Big Endian (Mac)	\N	0	1	lossless	\N	24	48	\N	003140	\N	\N	\N
812	531	wav	Big Endian (Mac)	\N	0	1	lossless	\N	24	48	\N	004750	\N	\N	\N
813	532	wav	Big Endian (Mac)	\N	0	1	lossless	\N	24	48	\N	004760	\N	\N	\N
814	533	wav	Big Endian (Mac)	\N	0	2	lossless	\N	24	48	\N	003404	\N	\N	\N
815	534	wav	Big Endian (Mac)	\N	0	2	lossless	\N	24	48	\N	004510	\N	\N	\N
816	535	wav	Big Endian (Mac)	\N	0	1	lossless	\N	24	48	\N	003200	\N	\N	\N
817	536	wav	Big Endian (Mac)	\N	0	1	lossless	\N	24	48	\N	004800	\N	\N	\N
818	537	wav	Big Endian (Mac)	\N	0	1	lossless	\N	24	48	\N	004802	\N	\N	\N
819	538	wav	Big Endian (Mac)	\N	0	1	lossless	\N	24	48	\N	004740	\N	\N	\N
820	539	wav	Big Endian (Mac)	\N	0	1	lossless	\N	24	48	\N	004745	\N	\N	\N
821	540	wav	Big Endian (Mac)	\N	0	1	lossless	\N	24	48	\N	003210	\N	\N	\N
822	541	wav	Big Endian (Mac)	\N	0	1	lossless	\N	24	48	\N	004730	\N	\N	\N
823	542	wav	Big Endian (Mac)	\N	0	1	lossless	\N	24	48	\N	004730	\N	\N	\N
824	543	wav	Big Endian (Mac)	\N	0	1	lossless	\N	24	48	\N	004730	\N	\N	\N
825	544	wav	Big Endian (Mac)	\N	0	1	lossless	\N	24	48	\N	003121	\N	\N	\N
826	545	wav	Big Endian (Mac)	\N	0	2	lossless	\N	24	48	\N	003142	\N	\N	\N
827	546	wav	Big Endian (Mac)	\N	0	2	lossless	\N	24	48	\N	003144	\N	\N	\N
828	547	wav	Big Endian (Mac)	\N	0	2	lossless	\N	24	48	\N	003143	\N	\N	\N
829	548	wav	Big Endian (Mac)	\N	0	2	lossless	\N	24	48	\N	004712	\N	\N	\N
830	549	wav	Big Endian (Mac)	\N	0	2	lossless	\N	24	48	\N	003144	\N	\N	\N
831	550	wav	Big Endian (Mac)	\N	0	2	lossless	\N	24	48	\N	001500	\N	\N	\N
832	551	wav	Big Endian (Mac)	\N	0	2	lossless	\N	24	48	\N	001600	\N	\N	\N
833	552	wav	Big Endian (Mac)	\N	0	2	lossless	\N	24	48	\N	001550	\N	\N	\N
834	553	wav	Big Endian (Mac)	\N	0	2	lossless	\N	24	48	\N	003000	\N	\N	\N
835	554	wav	Big Endian (Mac)	\N	0	2	lossless	\N	24	48	\N	003133	\N	\N	\N
836	555	wav	Big Endian (Mac)	\N	0	2	lossless	\N	24	48	\N	003134	\N	\N	\N
837	556	wav	Big Endian (Mac)	\N	0	1	lossless	\N	24	48	\N	002100	\N	\N	\N
838	557	wav	Big Endian (Mac)	\N	0	1	lossless	\N	24	48	\N	004500	\N	\N	\N
839	558	wav	Big Endian (Mac)	\N	0	1	lossless	\N	24	48	\N	003010	\N	\N	\N
840	559	wav	Big Endian (Mac)	\N	0	1	lossless	\N	24	48	\N	002310	\N	\N	\N
841	560	wav	Big Endian (Mac)	\N	0	1	lossless	\N	24	48	\N	003010	\N	\N	\N
842	561	wav	Big Endian (Mac)	\N	0	1	lossless	\N	24	48	\N	000210	\N	\N	\N
843	562	wav	Big Endian (Mac)	\N	0	1	lossless	\N	24	48	\N	010000	\N	\N	\N
844	563	wav	Big Endian (Mac)	\N	0	1	lossless	\N	24	48	\N	004800	\N	\N	\N
845	564	wav	Big Endian (Mac)	\N	0	1	lossless	\N	24	48	\N	003010	\N	\N	\N
846	565	wav	Big Endian (Mac)	\N	0	1	lossless	\N	24	48	\N	000310	\N	\N	\N
847	566	wav	Big Endian (Mac)	\N	0	1	lossless	\N	24	48	\N	003010	\N	\N	\N
848	567	wav	Big Endian (Mac)	\N	0	1	lossless	\N	24	48	\N	003010	\N	\N	\N
849	568	wav	Big Endian (Mac)	\N	0	2	lossless	\N	24	48	\N	004700	\N	\N	\N
850	569	wav	Big Endian (Mac)	\N	0	2	lossless	\N	24	48	\N	003010	\N	\N	\N
851	570	wav	Big Endian (Mac)	\N	0	2	lossless	\N	24	48	\N	003010	\N	\N	\N
852	571	wav	Big Endian (Mac)	\N	0	2	lossless	\N	24	48	\N	003000	\N	\N	\N
853	572	wav	Big Endian (Mac)	\N	0	2	lossless	\N	24	48	\N	003100	\N	\N	\N
854	573	wav	Big Endian (Mac)	\N	0	2	lossless	\N	24	48	\N	\N	\N	\N	\N
855	574	wav	Big Endian (Mac)	\N	0	2	lossless	\N	24	48	\N	003010	\N	\N	\N
856	575	wav	Big Endian (Mac)	\N	0	2	lossless	\N	24	48	\N	003114	\N	\N	\N
857	576	wav	Big Endian (Mac)	\N	0	2	lossless	\N	24	48	\N	001135	\N	\N	\N
858	577	wav	Big Endian (Mac)	\N	0	2	lossless	\N	24	48	\N	000630	\N	\N	\N
859	578	wav	Big Endian (Mac)	\N	0	2	lossless	\N	24	48	\N	000652	\N	\N	\N
860	579	wav	Big Endian (Mac)	\N	0	2	lossless	\N	24	48	\N	003900	\N	\N	\N
861	580	wav	Big Endian (Mac)	\N	0	2	lossless	\N	24	48	\N	004700	\N	\N	\N
862	581	wav	Big Endian (Mac)	\N	0	2	lossless	\N	24	48	\N	004000	\N	\N	\N
863	582	wav	Big Endian (Mac)	\N	0	2	lossless	\N	24	48	\N	004800	\N	\N	\N
864	583	wav	Big Endian (Mac)	\N	0	2	lossless	\N	24	48	\N	001800	\N	\N	\N
865	584	wav	Big Endian (Mac)	\N	0	2	lossless	\N	24	48	\N	004809	\N	\N	\N
866	585	wav	Big Endian (Mac)	\N	0	2	lossless	\N	24	48	\N	003200	\N	\N	\N
867	586	wav	Big Endian (Mac)	\N	0	2	lossless	\N	24	48	\N	004730	\N	\N	\N
868	587	wav	Big Endian (Mac)	\N	0	2	lossless	\N	24	48	\N	004730	\N	\N	\N
869	588	wav	Big Endian (Mac)	\N	0	2	lossless	\N	24	48	\N	004730	\N	\N	\N
870	589	wav	Big Endian (Mac)	\N	0	2	lossless	\N	24	48	\N	004730	\N	\N	\N
871	590	wav	Big Endian (Mac)	\N	0	2	lossless	\N	24	48	\N	004730	\N	\N	\N
872	591	wav	Big Endian (Mac)	\N	0	2	lossless	\N	24	48	\N	003135	\N	\N	\N
873	592	wav	Big Endian (Mac)	\N	0	2	lossless	\N	24	48	\N	003138	\N	\N	\N
874	593	wav	Big Endian (Mac)	\N	0	2	lossless	\N	24	48	\N	010233	\N	\N	\N
875	594	wav	Big Endian (Mac)	\N	0	2	lossless	\N	24	48	\N	010235	\N	\N	\N
876	595	wav	Big Endian (Mac)	\N	0	2	lossless	\N	24	48	\N	010318	\N	\N	\N
877	596	wav	Big Endian (Mac)	\N	0	2	lossless	\N	24	48	\N	010333	\N	\N	\N
878	597	wav	Big Endian (Mac)	\N	0	2	lossless	\N	24	48	\N	010313	\N	\N	\N
879	598	wav	Big Endian (Mac)	\N	0	2	lossless	\N	24	48	\N	005339	\N	\N	\N
880	599	wav	Big Endian (Mac)	\N	0	2	lossless	\N	24	48	\N	003100	\N	\N	\N
881	600	wav	Big Endian (Mac)	\N	0	2	lossless	\N	24	48	\N	003100	\N	\N	\N
882	601	wav	Big Endian (Mac)	\N	0	2	lossless	\N	24	48	\N	002932	\N	\N	\N
883	602	wav	Big Endian (Mac)	\N	0	2	lossless	\N	24	48	\N	003047	\N	\N	\N
884	603	wav	Big Endian (Mac)	\N	0	1	lossless	\N	24	48	\N	003126	\N	\N	\N
885	604	wav	Big Endian (Mac)	\N	0	2	lossless	\N	24	48	\N	000553	\N	\N	\N
886	605	wav	Big Endian (Mac)	\N	0	2	lossless	\N	24	48	\N	001740	\N	\N	\N
887	606	wav	Big Endian (Mac)	\N	0	2	lossless	\N	24	48	\N	003145	\N	\N	\N
888	607	wav	Big Endian (Mac)	\N	0	2	lossless	\N	24	48	\N	003230	\N	\N	\N
889	608	wav	Big Endian (Mac)	\N	0	2	lossless	\N	24	48	\N	002708	\N	\N	\N
890	609	wav	Big Endian (Mac)	\N	0	2	lossless	\N	24	48	\N	005745	\N	\N	\N
891	610	wav	Big Endian (Mac)	\N	0	2	lossless	\N	24	48	\N	010312	\N	\N	\N
892	611	wav	Big Endian (Mac)	\N	0	2	lossless	\N	24	48	\N	004730	\N	\N	\N
893	612	wav	Big Endian (Mac)	\N	0	2	lossless	\N	24	48	\N	004730	\N	\N	\N
894	613	wav	Big Endian (Mac)	\N	0	2	lossless	\N	24	48	\N	002241	\N	\N	\N
895	614	wav	Big Endian (Mac)	\N	0	2	lossless	\N	24	48	\N	004730	\N	\N	\N
896	615	wav	Big Endian (Mac)	\N	0	2	lossless	\N	24	48	\N	004000	\N	\N	\N
897	616	wav	Big Endian (Mac)	\N	0	2	lossless	\N	24	48	\N	004730	\N	\N	\N
898	617	wav	Big Endian (Mac)	\N	0	2	lossless	\N	24	48	\N	003246	\N	\N	\N
899	618	wav	Big Endian (Mac)	\N	0	2	lossless	\N	24	48	\N	003246	\N	\N	\N
900	619	wav	Big Endian (Mac)	\N	0	2	lossless	\N	24	48	\N	010103	\N	\N	\N
901	620	wav	Big Endian (Mac)	\N	0	2	lossless	\N	24	48	\N	003247	\N	\N	\N
902	621	wav	Big Endian (Mac)	\N	0	2	lossless	\N	24	48	\N	004739	\N	\N	\N
903	622	wav	Big Endian (Mac)	\N	0	2	lossless	\N	24	48	\N	004723	\N	\N	\N
904	623	wav	Big Endian (Mac)	\N	0	1	lossless	\N	24	48	\N	001231	\N	\N	\N
905	624	wav	Big Endian (Mac)	\N	0	1	lossless	\N	24	48	\N	003031	\N	\N	\N
906	625	wav	Big Endian (Mac)	\N	0	1	lossless	\N	24	48	\N	004407	\N	\N	\N
907	626	wav	Big Endian (Mac)	\N	0	2	lossless	\N	24	48	\N	004813	\N	\N	\N
908	627	wav	Big Endian (Mac)	\N	0	2	lossless	\N	24	48	\N	004811	\N	\N	\N
909	628	wav	Big Endian (Mac)	\N	0	2	lossless	\N	24	48	\N	004622	\N	\N	\N
910	629	wav	Big Endian (Mac)	\N	0	2	lossless	\N	24	48	\N	004629	\N	\N	\N
911	630	wav	Big Endian (Mac)	\N	0	2	lossless	\N	24	48	\N	004745	\N	\N	\N
912	631	wav	Big Endian (Mac)	\N	625762	\N	lossless	\N	24	48	\N	010032	\N	\N	\N
913	632	wav	Big Endian (Mac)	\N	0	2	lossless	\N	24	48	\N	004722	\N	\N	\N
914	633	wav	Big Endian (Mac)	\N	0	2	lossless	\N	24	48	\N	004751	\N	\N	\N
915	634	wav	Big Endian (Mac)	\N	0	2	lossless	\N	24	48	\N	004744	\N	\N	\N
916	635	wav	Big Endian (Mac)	\N	0	2	lossless	\N	24	48	\N	004750	\N	\N	\N
917	636	wav	Big Endian (Mac)	\N	0	2	lossless	\N	24	48	\N	004748	\N	\N	\N
918	637	wav	Big Endian (Mac)	\N	0	2	lossless	\N	24	48	\N	004751	\N	\N	\N
919	638	wav	Big Endian (Mac)	\N	0	2	lossless	\N	24	48	\N	004744	\N	\N	\N
920	639	wav	Big Endian (Mac)	\N	0	2	lossless	\N	24	48	\N	004750	\N	\N	\N
921	640	wav	Big Endian (Mac)	\N	0	2	lossless	\N	24	48	\N	004727	\N	\N	\N
922	641	wav	Big Endian (Mac)	\N	0	2	lossless	\N	24	48	\N	004750	\N	\N	\N
923	642	wav	Big Endian (Mac)	\N	0	2	lossless	\N	24	48	\N	004735	\N	\N	\N
924	643	wav	Big Endian (Mac)	\N	0	\N	lossless	\N	24	48	\N	004740	\N	\N	\N
925	644	wav	Big Endian (Mac)	\N	0	\N	lossless	\N	24	48	\N	004722	\N	\N	\N
926	645	wav	Big Endian (Mac)	\N	0	\N	lossless	\N	24	48	\N	004529	\N	\N	\N
927	646	wav	Big Endian (Mac)	\N	0	\N	lossless	\N	24	48	\N	004726	\N	\N	\N
928	647	wav	Big Endian (Mac)	\N	0	\N	lossless	\N	24	48	\N	004750	\N	\N	\N
929	648	wav	Big Endian (Mac)	\N	0	\N	lossless	\N	24	48	\N	004750	\N	\N	\N
930	649	wav	Big Endian (Mac)	\N	0	\N	lossless	\N	24	48	\N	004747	\N	\N	\N
931	650	wav	Big Endian (Mac)	\N	0	1	lossless	\N	24	48	\N	004300	\N	\N	\N
932	651	wav	Big Endian (Mac)	\N	0	2	lossless	\N	24	48	\N	004745	\N	\N	\N
933	652	wav	Big Endian (Mac)	\N	0	2	lossless	\N	24	48	\N	004750	\N	\N	\N
934	653	wav	Big Endian (Mac)	\N	0	1	lossless	\N	24	48	\N	004730	\N	\N	\N
935	654	wav	Big Endian (Mac)	\N	0	1	lossless	\N	24	48	\N	004733	\N	\N	\N
936	655	wav	Big Endian (Mac)	\N	0	1	lossless	\N	24	48	\N	004725	\N	\N	\N
937	656	wav	Big Endian (Mac)	\N	0	1	lossless	\N	24	48	\N	004725	\N	\N	\N
938	657	wav	Big Endian (Mac)	\N	0	1	lossless	\N	24	48	\N	004430	\N	\N	\N
939	658	wav	Big Endian (Mac)	\N	0	1	lossless	\N	24	48	\N	004726	\N	\N	\N
940	659	wav	Big Endian (Mac)	\N	0	1	lossless	\N	24	48	\N	004727	\N	\N	\N
941	660	wav	Big Endian (Mac)	\N	0	1	lossless	\N	24	48	\N	004726	\N	\N	\N
942	661	wav	Big Endian (Mac)	\N	0	1	lossless	\N	24	48	\N	004725	\N	\N	\N
943	662	wav	Big Endian (Mac)	\N	0	1	lossless	\N	24	48	\N	004725	\N	\N	\N
944	663	wav	Big Endian (Mac)	\N	0	1	lossless	\N	24	48	\N	003228	\N	\N	\N
945	664	wav	Big Endian (Mac)	\N	0	2	lossless	\N	24	48	\N	004745	\N	\N	\N
946	665	wav	Big Endian (Mac)	\N	0	2	lossless	\N	24	48	\N	004747	\N	\N	\N
947	666	wav	Big Endian (Mac)	\N	0	2	lossless	\N	24	48	\N	004747	\N	\N	\N
948	667	wav	Big Endian (Mac)	\N	0	2	lossless	\N	24	48	\N	004735	\N	\N	\N
949	668	wav	Big Endian (Mac)	\N	0	2	lossless	\N	24	48	\N	004744	\N	\N	\N
950	669	wav	Big Endian (Mac)	\N	0	2	lossless	\N	24	48	\N	004751	\N	\N	\N
951	670	wav	Big Endian (Mac)	\N	0	2	lossless	\N	24	48	\N	004734	\N	\N	\N
952	671	wav	Big Endian (Mac)	\N	0	2	lossless	\N	24	48	\N	004735	\N	\N	\N
953	672	wav	Big Endian (Mac)	\N	0	2	lossless	\N	24	48	\N	001348	\N	\N	\N
954	673	wav	Big Endian (Mac)	\N	0	2	lossless	\N	24	48	\N	001353	\N	\N	\N
955	674	wav	Big Endian (Mac)	\N	0	2	lossless	\N	24	48	\N	001505	\N	\N	\N
956	675	wav	Big Endian (Mac)	\N	0	2	lossless	\N	24	48	\N	001316	\N	\N	\N
957	676	wav	Big Endian (Mac)	\N	0	2	lossless	\N	24	48	\N	002006	\N	\N	\N
958	677	wav	Big Endian (Mac)	\N	0	2	lossless	\N	24	48	\N	002119	\N	\N	\N
959	678	wav	Big Endian (Mac)	\N	0	2	lossless	\N	24	48	\N	002320	\N	\N	\N
960	679	wav	Big Endian (Mac)	\N	0	2	lossless	\N	24	48	\N	001711	\N	\N	\N
961	680	wav	Big Endian (Mac)	\N	0	2	lossless	\N	24	48	\N	003720	\N	\N	\N
962	681	wav	Big Endian (Mac)	\N	0	2	lossless	\N	24	48	\N	003734	\N	\N	\N
963	682	wav	Big Endian (Mac)	\N	0	2	lossless	\N	24	48	\N	003812	\N	\N	\N
964	683	wav	Big Endian (Mac)	\N	0	2	lossless	\N	24	48	\N	004137	\N	\N	\N
965	684	wav	Big Endian (Mac)	\N	0	2	lossless	\N	24	48	\N	005607	\N	\N	\N
966	685	wav	Big Endian (Mac)	\N	0	1	lossless	\N	24	48	\N	002230	\N	\N	\N
967	686	wav	Big Endian (Mac)	\N	0	\N	lossless	\N	24	48	\N	\N	\N	\N	\N
968	687	wav	Big Endian (Mac)	\N	0	1	lossless	\N	24	48	\N	004721	\N	\N	\N
969	688	wav	Big Endian (Mac)	\N	0	1	lossless	\N	24	48	\N	001327	\N	\N	\N
970	689	wav	Big Endian (Mac)	\N	0	1	lossless	\N	24	48	\N	004709	\N	\N	\N
971	690	wav	Big Endian (Mac)	\N	0	2	lossless	\N	24	48	\N	004232	\N	\N	\N
972	691	wav	Big Endian (Mac)	\N	0	2	lossless	\N	24	48	\N	002742	\N	\N	\N
973	692	wav	Big Endian (Mac)	\N	0	2	lossless	\N	24	48	\N	002901	\N	\N	\N
974	693	wav	Big Endian (Mac)	\N	0	2	lossless	\N	24	48	\N	005006	\N	\N	\N
975	694	wav	Big Endian (Mac)	\N	0	2	lossless	\N	24	48	\N	002447	\N	\N	\N
976	695	wav	Big Endian (Mac)	\N	0	2	lossless	\N	24	48	\N	003203	\N	\N	\N
977	696	wav	Big Endian (Mac)	\N	0	2	lossless	\N	24	48	\N	003005	\N	\N	\N
978	697	wav	Big Endian (Mac)	\N	0	2	lossless	\N	24	48	\N	003133	\N	\N	\N
979	698	wav	Big Endian (Mac)	\N	0	2	lossless	\N	24	48	\N	003109	\N	\N	\N
980	699	wav	Big Endian (Mac)	\N	0	2	lossless	\N	24	48	\N	003455	\N	\N	\N
981	700	wav	Big Endian (Mac)	\N	0	2	lossless	\N	24	48	\N	010125	\N	\N	\N
982	701	wav	Big Endian (Mac)	\N	0	2	lossless	\N	24	48	\N	003459	\N	\N	\N
983	702	wav	Big Endian (Mac)	\N	0	2	lossless	\N	24	48	\N	003153	\N	\N	\N
984	703	wav	Big Endian (Mac)	\N	0	2	lossless	\N	24	48	\N	002718	\N	\N	\N
985	704	wav	Big Endian (Mac)	\N	0	2	lossless	\N	24	48	\N	002400	\N	\N	\N
986	705	wav	Big Endian (Mac)	\N	0	2	lossless	\N	24	48	\N	000741	\N	\N	\N
987	706	wav	Big Endian (Mac)	\N	0	2	lossless	\N	24	48	\N	003203	\N	\N	\N
988	707	wav	Big Endian (Mac)	\N	0	2	lossless	\N	24	48	\N	003200	\N	\N	\N
989	708	wav	Big Endian (Mac)	\N	0	2	lossless	\N	24	48	\N	002851	\N	\N	\N
990	709	wav	Big Endian (Mac)	\N	0	2	lossless	\N	24	48	\N	003029	\N	\N	\N
991	710	wav	Big Endian (Mac)	\N	0	2	lossless	\N	24	48	\N	003130	\N	\N	\N
992	711	wav	Big Endian (Mac)	\N	0	2	lossless	\N	24	48	\N	003105	\N	\N	\N
993	712	wav	Big Endian (Mac)	\N	0	2	lossless	\N	24	48	\N	004417	\N	\N	\N
994	713	wav	Big Endian (Mac)	\N	0	2	lossless	\N	24	48	\N	000420	\N	\N	\N
995	714	wav	Big Endian (Mac)	\N	0	2	lossless	\N	24	48	\N	000908	\N	\N	\N
996	715	wav	Big Endian (Mac)	\N	0	2	lossless	\N	24	48	\N	003719	\N	\N	\N
997	716	wav	Big Endian (Mac)	\N	0	2	lossless	\N	24	48	\N	003702	\N	\N	\N
998	717	wav	Big Endian (Mac)	\N	0	2	lossless	\N	24	48	\N	004720	\N	\N	\N
999	718	wav	Big Endian (Mac)	\N	0	2	lossless	\N	24	48	\N	004411	\N	\N	\N
1000	719	wav	Big Endian (Mac)	\N	0	2	lossless	\N	24	48	\N	004356	\N	\N	\N
1001	720	wav	Big Endian (Mac)	\N	0	2	lossless	\N	24	48	\N	010113	\N	\N	\N
1002	721	wav	Big Endian (Mac)	\N	0	2	lossless	\N	24	48	\N	020835	\N	\N	\N
1003	722	wav	Big Endian (Mac)	\N	0	2	lossless	\N	24	48	\N	020751	\N	\N	\N
1004	723	wav	Big Endian (Mac)	\N	0	2	lossless	\N	24	48	\N	020441	\N	\N	\N
1005	724	wav	Big Endian (Mac)	\N	0	2	lossless	\N	24	48	\N	010659	\N	\N	\N
1006	725	wav	Big Endian (Mac)	\N	0	2	lossless	\N	24	48	\N	003616	\N	\N	\N
1007	726	wav	Big Endian (Mac)	\N	0	2	lossless	\N	24	48	\N	020501	\N	\N	\N
1008	727	wav	Big Endian (Mac)	\N	0	2	lossless	\N	24	48	\N	010102	\N	\N	\N
1009	728	wav	Big Endian (Mac)	\N	0	1	lossless	\N	24	48	\N	003055	\N	\N	\N
1010	729	wav	Big Endian (Mac)	\N	0	1	lossless	\N	24	48	\N	003052	\N	\N	\N
1011	730	wav	Big Endian (Mac)	\N	0	2	lossless	\N	24	48	\N	010254	\N	\N	\N
1012	731	wav	Big Endian (Mac)	\N	0	1	lossless	\N	24	48	\N	003127	\N	\N	\N
1013	732	wav	Big Endian (Mac)	\N	0	1	lossless	\N	24	48	\N	003123	\N	\N	\N
1014	733	wav	Big Endian (Mac)	\N	0	2	lossless	\N	24	48	\N	003146	\N	\N	\N
1015	734	wav	Big Endian (Mac)	\N	0	2	lossless	\N	24	48	\N	003146	\N	\N	\N
1016	735	wav	Big Endian (Mac)	\N	0	1	lossless	\N	24	48	\N	003148	\N	\N	\N
1017	736	wav	Big Endian (Mac)	\N	0	2	lossless	\N	24	48	\N	003148	\N	\N	\N
1018	737	wav	Big Endian (Mac)	\N	0	1	lossless	\N	24	48	\N	003123	\N	\N	\N
1019	738	wav	Big Endian (Mac)	\N	0	2	lossless	\N	24	48	\N	004249	\N	\N	\N
1020	739	wav	Big Endian (Mac)	\N	0	2	lossless	\N	24	48	\N	004728	\N	\N	\N
1021	740	wav	Big Endian (Mac)	\N	0	2	lossless	\N	24	48	\N	003457	\N	\N	\N
1022	741	wav	Big Endian (Mac)	\N	0	1	lossless	\N	24	48	\N	005536	\N	\N	\N
1023	742	wav	Big Endian (Mac)	\N	0	1	lossless	\N	24	48	\N	005522	\N	\N	\N
1024	743	wav	Big Endian (Mac)	\N	0	\N	lossless	\N	24	48	\N	\N	\N	\N	\N
1025	744	wav	Big Endian (Mac)	\N	0	\N	lossless	\N	24	48	\N	\N	\N	\N	\N
1026	745	wav	Big Endian (Mac)	\N	0	\N	lossless	\N	24	48	\N	\N	\N	\N	\N
1027	746	wav	Big Endian (Mac)	\N	0	\N	lossless	\N	24	44.1	\N	004700	\N	\N	\N
1028	747	wav	Big Endian (Mac)	\N	0	2	lossless	\N	24	48	\N	003107	\N	\N	\N
1029	748	wav	Big Endian (Mac)	\N	0	2	lossless	\N	24	48	\N	002750	\N	\N	\N
1030	749	wav	Big Endian (Mac)	\N	0	2	lossless	\N	24	48	\N	002550	\N	\N	\N
1031	750	wav	Big Endian (Mac)	\N	0	2	lossless	\N	24	48	\N	003625	\N	\N	\N
1032	751	wav	Big Endian (Mac)	\N	0	2	lossless	\N	24	48	\N	002900	\N	\N	\N
1033	752	wav	Big Endian (Mac)	\N	0	2	lossless	\N	24	48	\N	003612	\N	\N	\N
1034	753	wav	Big Endian (Mac)	\N	0	2	lossless	\N	24	48	\N	003206	\N	\N	\N
1035	754	wav	Big Endian (Mac)	\N	0	2	lossless	\N	24	48	\N	003058	\N	\N	\N
1036	755	wav	Big Endian (Mac)	\N	0	2	lossless	\N	24	48	\N	003105	\N	\N	\N
1037	756	wav	Big Endian (Mac)	\N	0	2	lossless	\N	24	48	\N	003156	\N	\N	\N
1038	757	wav	Big Endian (Mac)	\N	0	2	lossless	\N	24	48	\N	003146	\N	\N	\N
1039	758	wav	Big Endian (Mac)	\N	0	2	lossless	\N	24	48	\N	003154	\N	\N	\N
1040	759	wav	Big Endian (Mac)	\N	0	\N	lossless	\N	24	48	\N	\N	\N	\N	\N
1041	760	wav	Big Endian (Mac)	\N	0	\N	lossless	\N	24	48	\N	\N	\N	\N	\N
1042	761	wav	Big Endian (Mac)	\N	0	\N	lossless	\N	24	48	\N	\N	\N	\N	\N
1043	762	wav	Big Endian (Mac)	\N	0	\N	lossless	\N	24	48	\N	\N	\N	\N	\N
1044	763	wav	Big Endian (Mac)	\N	0	\N	lossless	\N	24	48	\N	\N	\N	\N	\N
1045	764	wav	Big Endian (Mac)	\N	0	\N	lossless	\N	24	48	\N	\N	\N	\N	\N
1046	765	wav	Big Endian (Mac)	\N	0	\N	lossless	\N	24	48	\N	\N	\N	\N	\N
1047	766	wav	Big Endian (Mac)	\N	0	\N	lossless	\N	24	48	\N	\N	\N	\N	\N
1048	767	wav	Big Endian (Mac)	\N	0	1	lossless	\N	24	48	\N	002532	\N	\N	\N
1049	768	wav	Big Endian (Mac)	\N	0	1	lossless	\N	24	48	\N	000403	\N	\N	\N
1050	769	wav	Big Endian (Mac)	\N	0	1	lossless	\N	24	48	\N	000220	\N	\N	\N
1051	770	wav	Big Endian (Mac)	\N	0	1	lossless	\N	24	48	\N	000136	\N	\N	\N
1052	771	wav	Big Endian (Mac)	\N	0	1	lossless	\N	24	48	\N	000349	\N	\N	\N
1053	772	wav	Big Endian (Mac)	\N	0	1	lossless	\N	24	48	\N	000049	\N	\N	\N
1054	773	wav	Big Endian (Mac)	\N	0	1	lossless	\N	24	48	\N	000030	\N	\N	\N
1055	774	wav	Big Endian (Mac)	\N	0	1	lossless	\N	24	48	\N	000201	\N	\N	\N
1056	775	wav	Big Endian (Mac)	\N	0	1	lossless	\N	24	48	\N	000142	\N	\N	\N
1057	776	wav	Big Endian (Mac)	\N	0	1	lossless	\N	24	48	\N	000339	\N	\N	\N
1058	777	wav	Big Endian (Mac)	\N	0	1	lossless	\N	24	48	\N	001044	\N	\N	\N
1059	778	wav	Big Endian (Mac)	\N	0	1	lossless	\N	24	48	\N	001328	\N	\N	\N
1060	779	wav	Big Endian (Mac)	\N	0	1	lossless	\N	24	48	\N	001451	\N	\N	\N
1061	780	wav	Big Endian (Mac)	\N	0	1	lossless	\N	24	48	\N	001625	\N	\N	\N
1062	781	wav	Big Endian (Mac)	\N	0	1	lossless	\N	24	48	\N	000155	\N	\N	\N
1063	782	wav	Big Endian (Mac)	\N	0	1	lossless	\N	24	48	\N	000511	\N	\N	\N
1064	783	wav	Big Endian (Mac)	\N	0	1	lossless	\N	24	48	\N	000305	\N	\N	\N
1065	784	wav	Big Endian (Mac)	\N	0	1	lossless	\N	24	48	\N	000404	\N	\N	\N
1066	785	wav	Big Endian (Mac)	\N	0	1	lossless	\N	24	48	\N	000310	\N	\N	\N
1067	786	wav	Big Endian (Mac)	\N	0	1	lossless	\N	24	48	\N	000310	\N	\N	\N
1068	787	wav	Big Endian (Mac)	\N	0	1	lossless	\N	24	48	\N	000059	\N	\N	\N
1069	788	wav	Big Endian (Mac)	\N	0	1	lossless	\N	24	48	\N	000110	\N	\N	\N
1070	789	wav	Big Endian (Mac)	\N	0	1	lossless	\N	24	48	\N	000035	\N	\N	\N
1071	790	wav	Big Endian (Mac)	\N	0	1	lossless	\N	24	48	\N	000316	\N	\N	\N
1072	791	wav	Big Endian (Mac)	\N	0	1	lossless	\N	24	48	\N	000002	\N	\N	\N
1073	792	wav	Big Endian (Mac)	\N	0	1	lossless	\N	24	48	\N	000113	\N	\N	\N
1074	793	wav	Big Endian (Mac)	\N	0	1	lossless	\N	24	48	\N	000507	\N	\N	\N
1075	794	wav	Big Endian (Mac)	\N	0	1	lossless	\N	24	48	\N	000131	\N	\N	\N
1076	795	wav	Big Endian (Mac)	\N	0	1	lossless	\N	24	48	\N	000234	\N	\N	\N
1077	796	wav	Big Endian (Mac)	\N	0	1	lossless	\N	24	48	\N	000019	\N	\N	\N
1078	797	wav	Big Endian (Mac)	\N	0	1	lossless	\N	24	48	\N	000050	\N	\N	\N
1079	798	wav	Big Endian (Mac)	\N	0	1	lossless	\N	24	48	\N	000112	\N	\N	\N
1080	799	wav	Big Endian (Mac)	\N	0	\N	lossless	\N	24	48	\N	\N	\N	\N	\N
1081	800	wav	Big Endian (Mac)	\N	0	\N	lossless	\N	24	48	\N	\N	\N	\N	\N
1082	801	wav	Big Endian (Mac)	\N	0	\N	lossless	\N	24	48	\N	\N	\N	\N	\N
1083	802	wav	Big Endian (Mac)	\N	0	\N	lossless	\N	24	48	\N	\N	\N	\N	\N
1084	803	wav	Big Endian (Mac)	\N	0	\N	lossless	\N	24	48	\N	\N	\N	\N	\N
1085	804	wav	Big Endian (Mac)	\N	0	\N	lossless	\N	24	48	\N	\N	\N	\N	\N
1086	805	wav	Big Endian (Mac)	\N	0	\N	lossless	\N	24	48	\N	\N	\N	\N	\N
1087	806	wav	Big Endian (Mac)	\N	0	\N	lossless	\N	24	48	\N	\N	\N	\N	\N
1088	807	wav	Big Endian (Mac)	\N	0	\N	lossless	\N	24	48	\N	\N	\N	\N	\N
1089	808	wav	Big Endian (Mac)	\N	0	\N	lossless	\N	24	48	\N	\N	\N	\N	\N
1090	809	wav	Big Endian (Mac)	\N	0	1	lossless	\N	24	48	\N	000526	\N	\N	\N
1091	810	wav	Big Endian (Mac)	\N	0	1	lossless	\N	24	48	\N	000414	\N	\N	\N
1092	811	wav	Big Endian (Mac)	\N	0	1	lossless	\N	24	48	\N	000412	\N	\N	\N
1093	812	wav	Big Endian (Mac)	\N	0	1	lossless	\N	24	48	\N	000356	\N	\N	\N
1094	813	wav	Big Endian (Mac)	\N	0	1	lossless	\N	24	48	\N	000458	\N	\N	\N
1095	814	wav	Big Endian (Mac)	\N	0	1	lossless	\N	24	48	\N	000413	\N	\N	\N
1096	815	wav	Big Endian (Mac)	\N	0	1	lossless	\N	24	48	\N	000441	\N	\N	\N
1097	816	wav	Big Endian (Mac)	\N	0	1	lossless	\N	24	48	\N	000426	\N	\N	\N
1098	817	wav	Big Endian (Mac)	\N	0	\N	lossless	\N	24	48	\N	\N	\N	\N	\N
1099	818	wav	Big Endian (Mac)	\N	0	\N	lossless	\N	24	48	\N	\N	\N	\N	\N
1100	819	wav	Big Endian (Mac)	\N	0	\N	lossless	\N	24	48	\N	\N	\N	\N	\N
1101	1025	wav	Big Endian (Mac)	\N	0	0	lossless	patron request	24	48	\N	\N	\N	\N	\N
1102	1026	wav	Big Endian (Mac)	\N	0	0	lossless	patron request	24	48	\N	\N	\N	\N	\N
1103	1146	wav	Big Endian	\N	0	1	lossless	patron request	24	48	\N	003204	2006-05-08 00:00:00	\N	\N
1104	1249	wav	Big Endian	\N	0	2	lossless	patron request	24	48	\N	\N	\N	\N	\N
1105	1250	wav	Big Endian	\N	0	2	lossless	patron request	24	48	\N	\N	\N	\N	\N
1106	1251	wav	Big Endian	\N	0	2	lossless	patron request	24	48	\N	\N	\N	\N	\N
1107	1252	wav	Big Endian	\N	0	2	lossless	patron request	24	48	\N	\N	\N	\N	\N
1108	1253	wav	Big Endian	\N	0	2	lossless	patron request	24	48	\N	\N	\N	\N	\N
1109	1254	wav	Big Endian	\N	0	2	lossless	patron request	24	48	\N	\N	\N	\N	\N
1110	1255	wav	Big Endian	\N	0	2	lossless	patron request	24	48	\N	\N	\N	\N	\N
1111	1256	wav	Big Endian	\N	0	2	lossless	patron request	24	48	\N	\N	\N	\N	\N
1112	1257	wav	Big Endian	\N	0	2	lossless	patron request	24	48	\N	\N	\N	\N	\N
1113	1258	wav	Big Endian	\N	0	2	lossless	patron request	24	48	\N	\N	\N	\N	\N
1114	1259	wav	Big Endian	\N	0	2	lossless	patron request	24	48	\N	\N	\N	\N	\N
1115	1260	wav	Big Endian	\N	0	2	lossless	patron request	24	48	\N	\N	\N	\N	\N
1116	1261	wav	Big Endian	\N	0	2	lossless	patron request	24	48	\N	\N	\N	\N	\N
1117	1262	wav	Big Endian	\N	0	2	lossless	patron request	24	48	\N	\N	\N	\N	\N
1118	1145	wav	Big Endian	\N	0	2	lossless	patron request	24	48	\N	003204	\N	\N	\N
2012	0	wav	Big Endian (Mac)		0	0	lossless		24	48			\N		
2014	2028	wav	Big Endian (Mac)		0	0	lossless		24	48			\N		
2016	2029	wav	Big Endian (Mac)		0	0	lossless		24	48			\N		
2003	2023	wav	Big Endian	\N	0	2	lossless	preservation	24	48	Interview ends at 00:33:50.  Tape silent until end.	004643	2006-09-12 00:00:00	Farnsworth	\N
2008	2024	wav	Big Endian	\N	0	2	lossless	preservation	24	48	Very loud background noise, very hard to understand.	004657	2006-09-12 00:00:00	Farnsworth	\N
2009	2025	wav	Big Endian		0	2	lossless	preservation	24	48	Review of Baby Sweet's starts at 00:41:56.  Related files 2025-2026.	004706	2006-09-14 00:00:00	Farnsworth	
2010	2026	wav	Big Endian		0	2	lossless	preservation	24	48	Continues from side 1.  00:12:17 tape is silent.  Related files 2025-2026.	004734	2006-09-18 00:00:00	Farnsworth	
2013	2027	wav	Big Endian		0	2	lossless	preservation	24	48	Interview w/Raymond Andrews ends at 00:32:35.		2006-09-18 00:00:00	Farnsworth	
2001	2022	wav	Big Endian	\N	0	2	lossless	preservation	24	48	Interview begins at 00:04:42 and ends at 00:30:09. Talking stops at 00:32:00.	00:47:12	2006-09-11 00:00:00	Farnsworth	\N
\.


--
-- Data for TOC entry 225 (OID 12742681)
-- Name: Housing; Type: TABLE DATA; Schema: public; Owner: jbwhite
--

COPY "Housing" ("ID", "Housing description Film") FROM stdin;
5	Moving Image: Reel and Metal Boxes/Cannisters
7	Moving Image: Reel and Plastic Boxes/Cannisters
8	Moving Image/Sound/Still Image: None
9	Moving Image/Sound/Still Image: Other
11	Moving Image: Core and Metal Boxes/Cannisters
12	Moving Image: Core and Plastic Boxes/Cannisters
13	Moving Image: Core and Archival Paper Boxes
14	Moving Image: Core and Non Archival Paper Boxes
15	Moving Image: Reel and Archival Paper Boxes
16	Moving Image: Reel and Non Archival Paper Boxes
17	Still Image: Bound album with magnetic pages
18	Still Image: Bound album with paper pages
19	Still Image: Bound album with plastic sleeves
20	Still Image: Binder with plastic sleeves
21	Still Image: Archival envelope
22	Still Image: Metal Box
23	Still Image: Archival box
24	Still Image: Non-archival box
25	Still Image: Archival folder
26	Moving Image/Sound/Still Image: Mixed
27	Still Image: Supported roll
28	Still Image: Unsupported roll
29	Still Image: Non-archival envelope
30	Still Image: Non-archival folder
31	Moving Image/Sound: Jewel case
32	Moving Image/Sound: Extended/Amaray case
33	Moving Image/Sound: Slimline case
34	Moving Image/Sound: Plastic container
35	Moving Image/Sound: Archival box
36	Moving Image/Sound: Non archival box
37	Moving Image/Sound: Tyvek sleeve
38	Moving Image/Sound: Paper sleeve
39	Moving Image/Sound: Paper jewel case
\.


--
-- Data for TOC entry 226 (OID 12742721)
-- Name: Form; Type: TABLE DATA; Schema: public; Owner: jbwhite
--

COPY "Form" ("ID", "Form", "SupportMaterial", "Dates", "IdentifyingFeatures", "Source") FROM stdin;
1	Still Image - albumen process	Coated paper	1851 - c. 1900s	POP, semi-glossy surface; usually on heavy mount; a crackle pattern can often be seen in dark highlights; usually yellowed in highlights; paper fibers visible.	NEDCC http://www.nedcc.org/leaflets/photype.htm
2	Still Image - daguerreotype	Copper, silver plated	1839 - c. 1860	Mirror surface; positive-negative nature; usually in a case	NEDCC http://www.nedcc.org/leaflets/photype.htm
3	Still Image - gelatin dry plate negatives (glass plate negatives)	Glass	\N	Use for negatives that have a gelatin layer as a binder on a glass support.	NEDCC http://www.nedcc.org/leaflets/photype.htm
4	Still Image - lantern slides	Glass	\N	Transparent positive images made or mounted on glass for projection, usually but not necessarily photographic, measuring 3 1/4 to 3 1/2 by 4 inches.	NEDCC http://www.nedcc.org/leaflets/photype.htm
5	Still Image - unknown process/other	\N	\N	\N	\N
6	Still Image - silver gelatin prints	Coated paper	\N	The Gelatin-silver process is the photographic process used with currently available black and white films and printing papers. A suspension of silver salts in gelatin is coated onto acetate film or fiber-based or resin coated paper and allowed to dry (hence the term dry plate). These materials remain stable for months and years unlike the 'wet plate' materials that preceded them.\r\n\r\nThe Gelatin-Silver process was introduced by R. L. Maddox in 1871 with subsequent considerable improvements in sensitivity obtained by Charles Harper Bennet in 1878. Intense research in the last 125 years has lead to current materials that exhibit low grain and high sensitivity to light.\r\n\r\nWhen small crystals (called grains) of silver salts such as silver bromide and silver chloride are exposed to light, a few atoms of free metallic silver are liberated. These free silver atoms form the latent image. This latent image is relatively stable and will persist for some months without degradation provided the film is kept dark and cool. Films are developed using solutions that reduce the free silver atoms. An 'amplification' of the latent image occurs as the silver salts near the free silver atom are also reduced to metallic silver. The strength, temperature and time for which the developer is allowed to act allow the photographer to control the contrast of the final image. The development is then stopped by neutralizing the developer in a second bath.\r\n\r\nOnce development is complete, the undeveloped silver salts must be removed by fixing, and then the film (or paper) must be washed in clean water. The final image consists of metallic silver embedded in the gelatin coating.	http://en.wikipedia.org/wiki/Gelatin-silver_process
7	Sound - cardboard disc	\N	\N	Early disc records were originally made of various materials including hard rubber. From 1897 onwards, earlier materials were largely replaced by a rather brittle formula of 25% "shellac" (a material obtained from the excretion of an Indian beetle, a natural plastic), a filler of a cotton compound similar to manila paper, powdered slate and a small amount of a wax lubricant. The mass production of shellac records began in 1898 in Hanover, Germany. Shellac records were the most common until about 1950. Unbreakable records, usually of celluloid (an early form of plastic) on a pasteboard base, were made from 1904 onwards, but they suffered from an exceptionally high level of surface noise.\r\n\r\nIn the 1890s the early recording formats of discs were usually 17.5 cm (~seven inches) in diameter. By 1910 the 25 cm (~10-inch) record was by far the most popular standard, holding about three minutes of music or entertainment on a side. From 1903 onwards, 30 cm 12-inch records were also commercially sold, mostly of classical music or operatic selections, with four to five minutes of music per side. In 1930, RCA Victor launched the first commercially-available vinyl long-playing record, marketed as "Program Transcription" discs. These revolutionary discs were designed for playback at 33⅓ rpm and pressed on a 30 cm diameter flexible plastic disc. However, vinyl's lower playback noise level than shellac was not forgotten. During and after World War II when shellac supplies were extremely limited, some 78 rpm records were pressed in vinyl instead of shellac (wax), particularly the six-minute 12" (30 cm) 78 rpm records produced by V-Disc for distribution to US troops in World War II.\r\n\r\nBeginning in 1939, Columbia Records continued development of this technology. Dr. Peter Goldmark and his staff undertook exhaustive efforts to address problems of recording and playing back narrow grooves and developing an inexpensive, reliable consumer playback system. In 1948, the 12" (30 cm) Long Play (LP) 33⅓ rpm microgroove record was introduced by the Columbia Record at a dramatic New York press conference.	http://en.wikipedia.org/wiki/Gramophone_record#Less_common_formats
8	Sound - colored plastic disc	\N	\N	Early disc records were originally made of various materials including hard rubber. From 1897 onwards, earlier materials were largely replaced by a rather brittle formula of 25% "shellac" (a material obtained from the excretion of an Indian beetle, a natural plastic), a filler of a cotton compound similar to manila paper, powdered slate and a small amount of a wax lubricant. The mass production of shellac records began in 1898 in Hanover, Germany. Shellac records were the most common until about 1950. Unbreakable records, usually of celluloid (an early form of plastic) on a pasteboard base, were made from 1904 onwards, but they suffered from an exceptionally high level of surface noise.\r\n\r\nIn the 1890s the early recording formats of discs were usually 17.5 cm (~seven inches) in diameter. By 1910 the 25 cm (~10-inch) record was by far the most popular standard, holding about three minutes of music or entertainment on a side. From 1903 onwards, 30 cm 12-inch records were also commercially sold, mostly of classical music or operatic selections, with four to five minutes of music per side. In 1930, RCA Victor launched the first commercially-available vinyl long-playing record, marketed as "Program Transcription" discs. These revolutionary discs were designed for playback at 33⅓ rpm and pressed on a 30 cm diameter flexible plastic disc. However, vinyl's lower playback noise level than shellac was not forgotten. During and after World War II when shellac supplies were extremely limited, some 78 rpm records were pressed in vinyl instead of shellac (wax), particularly the six-minute 12" (30 cm) 78 rpm records produced by V-Disc for distribution to US troops in World War II.\r\n\r\nBeginning in 1939, Columbia Records continued development of this technology. Dr. Peter Goldmark and his staff undertook exhaustive efforts to address problems of recording and playing back narrow grooves and developing an inexpensive, reliable consumer playback system. In 1948, the 12" (30 cm) Long Play (LP) 33⅓ rpm microgroove record was introduced by the Columbia Record at a dramatic New York press conference.	http://en.wikipedia.org/wiki/Gramophone_record#Less_common_formats
9	Sound - paper roll	\N	\N	\N	\N
10	Sound - glass disc	\N	\N	\N	\N
11	Sound - acetate vinyl shellac - 33.3 rpm	\N	\N	Early disc records were originally made of various materials including hard rubber. From 1897 onwards, earlier materials were largely replaced by a rather brittle formula of 25% "shellac" (a material obtained from the excretion of an Indian beetle, a natural plastic), a filler of a cotton compound similar to manila paper, powdered slate and a small amount of a wax lubricant. The mass production of shellac records began in 1898 in Hanover, Germany. Shellac records were the most common until about 1950. Unbreakable records, usually of celluloid (an early form of plastic) on a pasteboard base, were made from 1904 onwards, but they suffered from an exceptionally high level of surface noise.\r\n\r\nIn the 1890s the early recording formats of discs were usually 17.5 cm (~seven inches) in diameter. By 1910 the 25 cm (~10-inch) record was by far the most popular standard, holding about three minutes of music or entertainment on a side. From 1903 onwards, 30 cm 12-inch records were also commercially sold, mostly of classical music or operatic selections, with four to five minutes of music per side. In 1930, RCA Victor launched the first commercially-available vinyl long-playing record, marketed as "Program Transcription" discs. These revolutionary discs were designed for playback at 33⅓ rpm and pressed on a 30 cm diameter flexible plastic disc. However, vinyl's lower playback noise level than shellac was not forgotten. During and after World War II when shellac supplies were extremely limited, some 78 rpm records were pressed in vinyl instead of shellac (wax), particularly the six-minute 12" (30 cm) 78 rpm records produced by V-Disc for distribution to US troops in World War II.\r\n\r\nBeginning in 1939, Columbia Records continued development of this technology. Dr. Peter Goldmark and his staff undertook exhaustive efforts to address problems of recording and playing back narrow grooves and developing an inexpensive, reliable consumer playback system. In 1948, the 12" (30 cm) Long Play (LP) 33⅓ rpm microgroove record was introduced by the Columbia Record at a dramatic New York press conference.	http://en.wikipedia.org/wiki/Gramophone_record#Less_common_formats
12	Sound - acetate vinyl shellac - 45 rpm	\N	\N	Early disc records were originally made of various materials including hard rubber. From 1897 onwards, earlier materials were largely replaced by a rather brittle formula of 25% "shellac" (a material obtained from the excretion of an Indian beetle, a natural plastic), a filler of a cotton compound similar to manila paper, powdered slate and a small amount of a wax lubricant. The mass production of shellac records began in 1898 in Hanover, Germany. Shellac records were the most common until about 1950. Unbreakable records, usually of celluloid (an early form of plastic) on a pasteboard base, were made from 1904 onwards, but they suffered from an exceptionally high level of surface noise.\r\n\r\nIn the 1890s the early recording formats of discs were usually 17.5 cm (~seven inches) in diameter. By 1910 the 25 cm (~10-inch) record was by far the most popular standard, holding about three minutes of music or entertainment on a side. From 1903 onwards, 30 cm 12-inch records were also commercially sold, mostly of classical music or operatic selections, with four to five minutes of music per side. In 1930, RCA Victor launched the first commercially-available vinyl long-playing record, marketed as "Program Transcription" discs. These revolutionary discs were designed for playback at 33⅓ rpm and pressed on a 30 cm diameter flexible plastic disc. However, vinyl's lower playback noise level than shellac was not forgotten. During and after World War II when shellac supplies were extremely limited, some 78 rpm records were pressed in vinyl instead of shellac (wax), particularly the six-minute 12" (30 cm) 78 rpm records produced by V-Disc for distribution to US troops in World War II.\r\n\r\nBeginning in 1939, Columbia Records continued development of this technology. Dr. Peter Goldmark and his staff undertook exhaustive efforts to address problems of recording and playing back narrow grooves and developing an inexpensive, reliable consumer playback system. In 1948, the 12" (30 cm) Long Play (LP) 33⅓ rpm microgroove record was introduced by the Columbia Record at a dramatic New York press conference.	http://en.wikipedia.org/wiki/Gramophone_record#Less_common_formats
13	Sound - acetate vinyl shellac - 78 rpm	\N	\N	Early disc records were originally made of various materials including hard rubber. From 1897 onwards, earlier materials were largely replaced by a rather brittle formula of 25% "shellac" (a material obtained from the excretion of an Indian beetle, a natural plastic), a filler of a cotton compound similar to manila paper, powdered slate and a small amount of a wax lubricant. The mass production of shellac records began in 1898 in Hanover, Germany. Shellac records were the most common until about 1950. Unbreakable records, usually of celluloid (an early form of plastic) on a pasteboard base, were made from 1904 onwards, but they suffered from an exceptionally high level of surface noise.\r\n\r\nIn the 1890s the early recording formats of discs were usually 17.5 cm (~seven inches) in diameter. By 1910 the 25 cm (~10-inch) record was by far the most popular standard, holding about three minutes of music or entertainment on a side. From 1903 onwards, 30 cm 12-inch records were also commercially sold, mostly of classical music or operatic selections, with four to five minutes of music per side. In 1930, RCA Victor launched the first commercially-available vinyl long-playing record, marketed as "Program Transcription" discs. These revolutionary discs were designed for playback at 33⅓ rpm and pressed on a 30 cm diameter flexible plastic disc. However, vinyl's lower playback noise level than shellac was not forgotten. During and after World War II when shellac supplies were extremely limited, some 78 rpm records were pressed in vinyl instead of shellac (wax), particularly the six-minute 12" (30 cm) 78 rpm records produced by V-Disc for distribution to US troops in World War II.\r\n\r\nBeginning in 1939, Columbia Records continued development of this technology. Dr. Peter Goldmark and his staff undertook exhaustive efforts to address problems of recording and playing back narrow grooves and developing an inexpensive, reliable consumer playback system. In 1948, the 12" (30 cm) Long Play (LP) 33⅓ rpm microgroove record was introduced by the Columbia Record at a dramatic New York press conference.	http://en.wikipedia.org/wiki/Gramophone_record#Less_common_formats
14	Sound - audiocassette	\N	\N	Sound recordings on magnetic tape.	AAT
15	Sound - open reel	\N	\N	\N	\N
16	Moving Images - VHS	Videotape	1970s - present	Describes videotape one-half inches in length (12.7mm);  VHS (Video Home System) contains 240 lines of horizontal resolution.	AAT
17	Moving Images - 35 mm	Film	\N	\N	\N
18	Moving Images - 16 mm	Film	\N	\N	\N
19	Moving Images - 8 mm	Film	\N	\N	\N
20	Sound - flexidisc	Vinyl	\N	A Flexi disc sound recording is a thin vinyl sheet with a molded-in spiral stylus groove designed to be playable on a normal phonograph turntable. Before the advent of the compact disc, they were sometimes used as a means to include sound with printed material such as magazines and music instruction books. A flexi disc could be molded with speech or music and bound into the text with a perforated seam, at very little cost and without any requirement for a hard binding. One problem with using the thinner vinyl was that the stylus's weight, combined with the flexi disc's lack of weight, would sometimes cause the disc to stop spinning on the turntable and become held in place by the stylus. For this reason, most flexi discs had a spot on the face of the disc for a coin, or other small, flat, weighted object to enforce the circular motion.	Wikipedia
21	Sound - other disc	\N	\N	\N	\N
65	Architectural Plan - Blueprint	\N	\N	Use for reproductive prints of architectural and other technical drawings having white images on blue backgrounds	AAT
66	Architectural Plan - Computer printout	\N	\N	\N	\N
67	Architectural Plan - Diazotypes	\N	\N	Produced by the effect of light on diazonium-sensitized materials, most often architectural or other technical drawings.	AAT
68	Architectural Plan - Graphite/Pencil	\N	\N	\N	\N
69	Architectural Plan - Green print	\N	circa 1900	Copies, usually of technical drawings, made by a light-sensitive process that produced blue lines on a green ground; produced in small numbers.	AAT
70	Architectural Plan - Ink	\N	\N	\N	\N
72	Architectural Plan - Photostat or Xerographics	\N	\N	General term for copies produced by photocopying, and usually at a one-to-one scale.	AAT
73	Architectural Plan - Sepia	\N	\N	\N	\N
74	Architectural Plan - Watercolor	\N	\N	\N	\N
76	Architectural Plan - Other	\N	\N	\N	\N
77	Architectural Plan - Ferrogallic process	\N	\N	An iron process largely used for reproducing technical drawings; produces an image in black.	AAT
78	Architectural Plan - Analine	\N	\N	\N	\N
79	Architectural Plan - Arch Drawing - Stencil	\N	\N	Images produced by using sheets of material in which desired designs have been cut out so that ink or paint applied will reproduce the designs	AAT
82	Architectural Plan - Brownprints (Van Dyke brown)	\N	\N	Use for prints made on light-sensitized surfaces that produce white images on brown backgrounds.	AAT
83	Architectural Plan - Wash-Off	\N	\N	\N	\N
84	Architectural Plan - Gel-Lithographs	\N	\N	\N	\N
85	Architectural Plan - Hectograph process	\N	19th C	Process used for copying letters in which drawing made with aniline dye is transferred to a prepared gelatin surface from which copies can be made.	AAT
86	Sound - aluminum disc	\N	\N	\N	\N
87	Moving Image - BetaCamSP	Videotape	1987 - present	Betacam videotape for professional use, one-half-inch in size, with stronger resolution than standard Betacam. Introduced  by Sony.	AAT
88	Moving Image - Umatic	Videotape	\N	\N	\N
89	Moving Image - Digital Betacam (DigiBeta)	Videotape	1993 - present	Betacam videotape with digital quality resolution. Introduced by Sony in 1993.	AAT
90	Moving Image - Other	Videotape	\N	\N	\N
91	Sound - other	\N	\N	\N	\N
92	Still Image - ambrotype	Clear glass	1851 - c. 1880	Milky gray highlights; various black backings, occasionally use ruby glass; usually in a case.	NEDCC http://www.nedcc.org/leaflets/photype.htm
93	Still Image - other prints on glass	\N	\N	\N	\N
94	Still Image - tintype, ferrotype	iron, japanned black	1854 - c. 1930s	Milky gray highlights.	NEDCC http://www.nedcc.org/leaflets/photype.htm
95	Still Image - other prints on metal	\N	\N	\N	\N
96	Still Image - stereographs	Card	\N	Refers to the common form of stereoscopic photographs, or double photographs of the same image taken from two slightly different perspectives.	AAT
97	Still Image - Polaroid instant photograph	\N	\N	Diffusion transfer print. Photographic prints made by the diffusion transfer process from film packets that contain their own developing chemicals.	AAT
100	Still Image - Salted paper print (calotype)	Uncoated paper	1840 - c. 1860\r\n1890's	POP, matte surface; paper fibers visible; often faded to pale yellow, especially at the edges; sometimes varnished.	NEDCC http://www.nedcc.org/leaflets/photype.htm
101	Still Image - Platinotype\r\nStill Image - Palladiotype	Uncoated paper	1880 - c. 1930	Gray-black color, matte surface; paper fibers visible; rich, velvety texture; popular with art photographers; very stable images, no fading or silvering.	NEDCC http://www.nedcc.org/leaflets/photype.htm
102	Still Image - Cyanotype	Uncoated paper	c. 1880 - c. 1910	Brilliant blue color, matte surface; invented in 1842 but not used until 1880's; paper fibers visible.	NEDCC http://www.nedcc.org/leaflets/photype.htm
103	Still Image - Carbon print	Coated paper	1860 - present	Used extensively for reproductions of works of art. Subtle image relief; paper fibers visible in highlights; no fading or yellowing; may get large cracks in dark areas.	NEDCC http://www.nedcc.org/leaflets/photype.htm
104	Still Image - Woodburytype	Coated paper	1866 - c. 1900	Same characteristics as carbon prints. Woodburytypes are not photographic, but photomechanical. Mainly used for book illustration and large edition publications.	NEDCC http://www.nedcc.org/leaflets/photype.htm
105	Still Image - Collodion print	Coated paper	1888 - c. 1910	POP, glossy surface (sepia, purple color) or matte surface (gold platinum toned, black color), very stable image, rarely faded; easily abraded; usually mounted.	NEDCC http://www.nedcc.org/leaflets/photype.htm
106	Still Image - letterpress copies	Uncoated paper	\N	Documents often on tissue paper, produced by the transfer of ink through direct contact with the original, using moisture and pressure in a copy press.	AAT
107	Still Image - multigraphs	Paper	\N	Documents, such as letters, leaflets, or forms, produced on a small, office-type offset press used for duplicating.	AAT
108	Moving Image - SVHS	Videotape	\N	One-half inch videotape with a higher resolution (400 horizontal lines) than standard VHS tape.	AAT
109	Moving Image - Mini DV	Videotape	\N	Digital videotape format for digital video recording and playback with excellent resolution.\r\n Digital videotape format for digital video recording and playback with excellent resolution.	AAT
110	Moving Image - Compact Discs	\N	\N	Optical disks on which programs, data, or music are digitally encoded for a laser beam to scan, decode, and transmit to a playback system.	AAT
111	Still Image - black and white negatives	film	\N	Refers to negatives whose images are composed of gray tones, black, and white or clear areas; may include one hue as a result of process, toning, or discoloration	AAT
112	Still Image - color negatives	film	\N	Photographic negatives that record on a single base the hue and lightness of a scene in complementary relation to the scene's perceived values; e.g., light blue is recorded as dark yellow.	AAT
113	Still Image - color separation negatives	film	\N	Negatives that record in monochrome the ranges of lightness of one hue per negative, usually in sets of three negatives. Each is used to make a plate or matrix for printing one color, in register with the others, to form a full-color photomechanical print.	AAT
114	Sound - DAT	\N	\N	\N	\N
115	Sound - CD	\N	\N	\N	\N
116	Sound - MP3	\N	\N	\N	\N
\.


--
-- Data for TOC entry 227 (OID 12742801)
-- Name: Language; Type: TABLE DATA; Schema: public; Owner: jbwhite
--

COPY "Language" ("ID", "LangName", "LangCode") FROM stdin;
143	Abkhazian	abk
144	Achinese	ace
145	Acoli	ach
146	Adangme	ada
147	Afar	aar
148	Afrihili	afh
149	Afrikaans	afr
150	Afro-Asiatic (Other)	afa
151	Akan	aka
152	Akkadian	akk
153	Albanian	alb
154	Aleut	ale
155	Algonquian languages	alg
156	Altaic (Other)	tut
157	Amharic	amh
158	Apache languages	apa
159	Arabic	ara
160	Aramaic	arc
161	Arapaho	arp
162	Araucanian	arn
163	Arawak	arw
164	Armenian	arm
165	Artificial (Other)	art
166	Assamese	asm
167	Athapascan languages	ath
168	Austronesian (Other)	map
169	Avaric	ava
170	Avestan	ave
171	Awadhi	awa
172	Aymara	aym
173	Azerbaijani	aze
174	Aztec	nah
175	Balinese	ban
176	Baltic (Other)	bat
177	Baluchi	bal
178	Bambara	bam
179	Bamileke languages	bai
180	Banda	bad
181	Bantu (Other)	bnt
182	Basa	bas
183	Bashkir	bak
184	Basque	baq
185	Beja	bej
186	Bemba	bem
187	Bengali	ben
188	Berber (Other	ber
189	Bhojpuri	bho
190	Bihari	bih
191	Bikol	bik
192	Bini	bin
193	Bislama	bis
194	Braj	bra
195	Breton	bre
196	Buginese	bug
197	Bulgarian	bul
198	Buriat	bua
199	Burmese	bur
200	Byelorussian	bel
201	Caddo	cad
202	Carib	car
203	Catalan	cat
204	Caucasian (Other)	cau
205	Cebuano	ceb
206	Celtic (Other)	cel
207	Central American Indian (Other)	cai
208	Chagatai	chg
209	Chamorro	cha
210	Chechen	che
211	Cherokee	chr
212	Cheyenne	chy
213	Chibcha	chb
214	Chinese	chi
215	Chinook jargon	chn
216	Choctaw	cho
217	Church Slavic	chu
218	Chuvash	chv
219	Coptic	cop
220	Cornish	cor
221	Corsican	cos
222	Cree	cre
223	Creek	mus
224	Creoles and Pidgins (Other)	crp
225	Creoles and Pidgins, English-based (Other)	cpe
226	Creoles and Pidgins, French-based (Other)	cpf
227	Creoles and Pidgins, Portuguese-based (Other)	cpp
228	Cushitic (Other)	cus
229	Croatian	\N
230	Czech	ces
231	Dakota	dak
232	Danish	dan
233	Delaware	del
234	Dinka	din
235	Divehi	div
236	Dogri	doi
237	Dravidian (Other)	dra
238	Duala	dua
239	Dutch	dut
240	Dutch, Middle (ca. 1050-1350)	dum
241	Dyula	dyu
242	Dzongkha	dzo
243	Efik	efi
244	Egyptian (Ancient)	egy
245	Ekajuk	eka
246	Elamite	elx
247	English	eng
248	English, Middle (ca. 1100-1500)	enm
249	English, Old (ca. 450-1100)	ang
250	Eskimo (Other)	esk
251	Esperanto	epo
252	Estonian	est
253	Ewe	ewe
254	Ewondo	ewo
255	Fang	fan
256	Fanti	fat
257	Faroese	fao
258	Fijian	fij
259	Finnish	fin
260	Finno-Ugrian (Other)	fiu
261	Fon	fon
262	French	fra
263	French, Middle (ca. 1400-1600)	frm
264	French, Old (842- ca. 1400)	fro
265	Frisian	fry
266	Fulah	ful
267	Ga	gaa
268	(Scots)	gae
269	Gallegan	glg
270	Ganda	lug
271	Gayo	gay
272	Geez	gez
273	Georgian	geo
274	German	deu
275	German, Middle High (ca. 1050-1500)	gmh
276	German, Old High (ca. 750-1050)	goh
277	Germanic (Other)	gem
278	Gilbertese	gil
279	Gondi	gon
280	Gothic	got
281	Grebo	grb
282	Greek, Ancient (to 1453)	grc
283	Greek, Modern (1453-)	ell
284	Greenlandic	kal
285	Guarani	grn
286	Gujarati	guj
287	Haida	hai
288	Hausa	hau
289	Hawaiian	haw
290	Hebrew	heb
291	Herero	her
292	Hiligaynon	hil
293	Himachali	him
294	Hindi	hin
295	Hiri Motu	hmo
296	Hungarian	hun
297	Hupa	hup
298	Iban	iba
299	Icelandic	ice
300	Igbo	ibo
301	Ijo	ijo
302	Iloko	ilo
303	Indic (Other)	inc
304	Indo-European (Other)	ine
305	Indonesian	ind
306	Interlingua (International Auxiliary language Association)	ina
307	Interlingue	ine
308	Inuktitut	iku
309	Inupiak	ipk
310	Iranian (Other)	ira
311	Irish	gai
312	Irish, Old (to 900)	sga
313	Irish, Middle (900 - 1200)	mga
314	Iroquoian languages	iro
315	Italian	ita
316	Japanese	jpn
317	Javanese	jav
318	Judeo-Arabic	jrb
319	Judeo-Persian	jpr
320	Kabyle	kab
321	Kachin	kac
322	Kamba	kam
323	Kannada	kan
324	Kanuri	kau
325	Kara-Kalpak	kaa
326	Karen	kar
327	Kashmiri	kas
328	Kawi	kaw
329	Kazakh	kaz
330	Khasi	kha
331	Khmer	khm
332	Khoisan (Other)	khi
333	Khotanese	kho
334	Kikuyu	kik
335	Kinyarwanda	kin
336	Kirghiz	kir
337	Komi	kom
338	Kongo	kon
339	Konkani	kok
340	Korean	kor
341	Kpelle	kpe
342	Kru	kro
343	Kuanyama	kua
344	Kumyk	kum
345	Kurdish	kur
346	Kurukh	kru
347	Kusaie	kus
348	Kutenai	kut
349	Ladino	lad
350	Lahnda	lah
351	Lamba	lam
352	Langue d'Oc (post 1500)	oci
353	Lao	lao
354	Latin	lat
355	Latvian	lav
356	Letzeburgesch	ltz
357	Lezghian	lez
358	Lingala	lin
359	Lithuanian	lit
360	Lozi	loz
361	Luba-Katanga	lub
362	Luiseno	lui
363	Lunda	lun
364	Luo (Kenya and Tanzania)	luo
365	Macedonian	mac
366	Madurese	mad
367	Magahi	mag
368	Maithili	mai
369	Makasar	mak
370	Malagasy	mlg
371	Malay	may
372	Malayalam	mal
373	Maltese	mlt
374	Mandingo	man
375	Manipuri	mni
376	Manobo languages	mno
377	Manx	max
378	Maori	mao
379	Marathi	mar
380	Mari	chm
381	Marshall	mah
382	Marwari	mwr
383	Masai	mas
384	Mayan languages	myn
385	Mende	men
386	Micmac	mic
387	Minangkabau	min
388	Miscellaneous (Other)	mis
389	Mohawk	moh
390	Moldavian	mol
391	Mon-Kmer (Other)	mkh
392	Mongo	lol
393	Mongolian	mon
394	Mossi	mos
395	Multiple languages	mul
396	Munda languages	mun
397	Nauru	nau
398	Navajo	nav
399	Ndebele, North	nde
400	Ndebele, South	nbl
401	Ndongo	ndo
402	Nepali	nep
403	Newari	new
404	Niger-Kordofanian (Other)	nic
405	Nilo-Saharan (Other)	ssa
406	Niuean	niu
407	Norse, Old	non
408	North American Indian (Other)	nai
409	Norwegian	nor
410	Norwegian (Nynorsk)	nno
411	Nubian languages	nub
412	Nyamwezi	nym
413	Nyanja	nya
414	Nyankole	nyn
415	Nyoro	nyo
416	Nzima	nzi
417	Ojibwa	oji
418	Oriya	ori
419	Oromo	orm
420	Osage	osa
421	Ossetic	oss
422	Otomian languages	oto
423	Pahlavi	pal
424	Palauan	pau
425	Pali	pli
426	Pampanga	pam
427	Pangasinan	pag
428	Panjabi	pan
429	Papiamento	pap
430	Papuan-Australian (Other)	paa
431	Persian	fas
432	Persian, Old (ca 600 - 400 B.C.)	peo
433	Phoenician	phn
434	Polish	pol
435	Ponape	pon
436	Portuguese	por
437	Prakrit languages	pra
438	Provencal, Old (to 1500)	pro
439	Pushto	pus
440	Quechua	que
441	Rhaeto-Romance	roh
442	Rajasthani	raj
443	Rarotongan	rar
444	Romance (Other)	roa
445	Romanian	ron
446	Romany	rom
447	Rundi	run
448	Russian	rus
449	Salishan languages	sal
450	Samaritan Aramaic	sam
451	Sami languages	smi
452	Samoan	smo
453	Sandawe	sad
454	Sango	sag
455	Sanskrit	san
456	Sardinian	srd
457	Scots	sco
458	Selkup	sel
459	Semitic (Other)	sem
460	Serbian	\N
461	Serbo-Croatian	scr
462	Serer	srr
463	Shan	shn
464	Shona	sna
465	Sidamo	sid
466	Siksika	bla
467	Sindhi	snd
468	Singhalese	sin
469	Sino-Tibetan (Other)	sit
470	Siouan languages	sio
471	Slavic (Other)	sla
472	Siswant	ssw
473	Slovak	slk
474	Slovenian	slv
475	Sogdian	sog
476	Somali	som
477	Songhai	son
478	Sorbian languages	wen
479	Sotho, Northern	nso
480	Sotho, Southern	sot
481	South American Indian (Other)	sai
482	Spanish	esl
483	Sukuma	suk
484	Sumerian	sux
485	Sudanese	sun
486	Susu	sus
487	Swahili	swa
488	Swazi	ssw
489	Swedish	sve
490	Syriac	syr
491	Tagalog	tgl
492	Tahitian	tah
493	Tajik	tgk
494	Tamashek	tmh
495	Tamil	tam
496	Tatar	tat
497	Telugu	tel
498	Tereno	ter
499	Thai	tha
500	Tibetan	bod
501	Tigre	tig
502	Tigrinya	tir
503	Timne	tem
504	Tivi	tiv
505	Tlingit	tli
506	Tonga (Nyasa)	tog
507	Tonga (Tonga Islands)	ton
508	Truk	tru
509	Tsimshian	tsi
510	Tsonga	tso
511	Tswana	tsn
512	Tumbuka	tum
513	Turkish	tur
514	Turkish, Ottoman (1500 - 1928)	ota
515	Turkmen	tuk
516	Tuvinian	tyv
517	Twi	twi
518	Ugaritic	uga
519	Uighur	uig
520	Ukrainian	ukr
521	Umbundu	umb
522	Undetermined	und
523	Urdu	urd
524	Uzbek	uzb
525	Vai	vai
526	Venda	ven
527	Vietnamese	vie
528	Volapük	vol
529	Votic	vot
530	Wakashan languages	wak
531	Walamo	wal
532	Waray	war
533	Washo	was
534	Welsh	cym
535	Wolof	wol
536	Xhosa	xho
537	Yakut	sah
538	Yao	yao
539	Yap	yap
540	Yiddish	yid
541	Yoruba	yor
542	Zapotec	zap
543	Zenaga	zen
544	Zhuang	zha
545	Zulu	zul
546	Zuni	zun
547	No Linguistic Content	zxx
\.


--
-- Data for TOC entry 228 (OID 12743214)
-- Name: Location; Type: TABLE DATA; Schema: public; Owner: jbwhite
--

COPY "Location" ("ID", "LocationName", "LocationStreet", "LocationCityStateZip", "LocationPhone", "LocationFax", "LocationEmail", "LocationWebSite") FROM stdin;
1	MARBL, Robert W. Woodruff Library, Emory University	540 Asbury Circle	Atlanta, GA 30322-2870	(404) 727-6887	(404) 727-0360	speccollref@emory.edu	#http://specialcollections.library.emory.edu/#
2	Emory Archives: Robert W. Woodruff Library	\N	\N	\N	\N	\N	\N
3	Emory Archives: Woodruff Health Sciences Center Library	\N	\N	\N	\N	\N	\N
4	Emory Archives: Hugh F. MacMillan Library Law Library	\N	\N	\N	\N	\N	\N
5	Emory Archives: Oxford College Hoke O'Kelley Memorial Library	\N	\N	\N	\N	\N	\N
6	Marian K. Heilbrun Library Music and Media Library	\N	\N	\N	\N	\N	\N
7	Pitts Theology Library	\N	\N	\N	\N	\N	\N
8	Goizueta Business Library	\N	\N	\N	\N	\N	\N
9	J. S. Guy Chemistry Library	\N	\N	\N	\N	\N	\N
10	Mathematics and Science Center Library	\N	\N	\N	\N	\N	\N
\.


--
-- Data for TOC entry 229 (OID 12743236)
-- Name: Name; Type: TABLE DATA; Schema: public; Owner: jbwhite
--

COPY "Name" ("ID", "Name", "Authority_id") FROM stdin;
37	Pendergrast, Mark	0
38	Goizueta, Roberto	0
42	Augusta News Company	0
44	Colorpicture (Cambridge, Mass.)	0
45	Wilde (firm: Savannah, Ga.)	0
48	Unknown	0
49	Arb, Siv	0
50	Hughes, Carol	0
51	Plath, Sylvia	0
52	Hughes, Ted	0
53	Jackson, Delilah	0
54	Attles, Joe	0
56	Press Association, Inc	0
57	Randolph, Milton L., Jr.	0
58	Brown, Walter	0
59	Pietzcker, George	0
60	Sanders, Tye	0
61	Keeler, O.B.	0
62	Winn	0
63	Underwood	0
64	Pacific and Atlantic	0
65	Hamilton, Paul	0
66	New World Photos	0
67	Associated Press	0
68	Springfield Acme Newspictures	0
69	Sport and General	0
70	London News Agency	0
71	Jones, Mrs. Bobby	0
72	Putnam Studios	0
73	Wide World Photos	0
74	Lambert and Butler	0
75	Daily Mirror	0
76	Kinsella, J. Hixon	0
77	Emory University	0
78	Star Photos	0
79	American Choral Directors Association	0
81	Johnson, Marion	0
82	Wilmer, Cary B. Jr.	0
83	Cowie, G.M.	0
84	Greene, Bill	0
85	Mark, Bill	0
86	Jackson, Charles	0
87	Shell's Wonderful World of Golf	0
88	Pryer, Elmer	0
89	Lane Bros.	0
90	Reeves, Walton	0
91	Tuskegee University	0
92	Keystone View Company	0
93	Garber, Maurey	0
94	Quarles Studio (Tuskegee, Alabama)	0
95	Van Vechten, Carl, 1880-1964.	0
96	Apeda Studios (N.Y.)	0
97	American Society of Composers, Authors and Publishers.	0
98	Decca Records (Firm)	0
99	Cheong, Ying	0
100	Perkins	0
101	Hill, L.S.	0
102	Ran, William H. Ran	0
103	Wilson, J.N.	0
104	Yoshiaska, T.	0
105	Matzene Chung Hwa	0
106	Ming, Sze Yuen	0
107	Kesslere, George Maillard	0
108	Jackson, Leandre	0
109	Layne, Cecil	0
110	Jchimiya, N.	0
111	H.A. Atwell Studio (Chicago, Ill.)	0
115	Baress, Sheila O.	0
116	Shawnee Press (firm)	0
117	Alabama Music Hall of Fame	0
119	Atlanta Symphony Orchestra	0
120	Spelman College	0
121	Lincoln University (Pa.)	0
122	Louisiana.  Department of Education.	0
123	Creative Artists' Workshop (Philadelphia, Pa.)	0
124	Robert R. Moton Memorial Institute, Inc.	0
125	Music Educators National Conference.  Eastern Divison.	0
126	NAACP	0
127	Association for the Study of Negro Life and History	0
128	Lathon, William	0
129	Horner Institute of Fine Arts (Kansas City, Mo.)	0
130	Bradley and Gilbert Company	0
131	Austin Jenkins Co.	0
132	Associated Publishers	0
133	Nephil Music	0
135	T. Y. Crowell Co.	0
136	WAPX (Montgomery, Ala.)	0
137	Management Corporation of America Artists, Ltd.	0
138	United Negro College Fund	0
139	Ohio Music Education Association	0
141	Sims, Alberta Lillian	0
142	\N	0
143	Civic Orchestra of Chicago	0
144	Warner Bros. Music	0
145	United States. Dept. of State.	0
146	Stokowski, Leopold	0
147	Radio City Music Hall	0
148	Dunbar News (firm)	0
149	Burleigh, H. T.	0
150	Handy Brothers Music Co., Inc.	0
151	Handy, W. C.	0
152	H. T. FitzSimons Company	0
153	Clayton F. Summy Co.	0
154	Hall and McCreary	0
155	Delkas Music	0
156	Dorrance	0
157	Exposition Press	0
158	Carver, George Washington	0
159	Ellison, Ralph	0
160	Random House	0
161	Handy Brothers Music Co. Inc.	0
162	August Valentine Bernier	0
164	Christian Reporter	0
165	Murray Bros Inc.	0
166	The Author	0
167	Evansville Printing Company	0
168	People's International Corporation	0
169	John W. Work and Frederick J. Work	0
170	Holt Publishing Co.	0
171	G. Schirmer Inc.	0
172	Theodore Presser Co.	0
173	William L. Dawson	0
174	The Bulletin (Philadelphia, Pa.)	0
175	Lincoln High School (Kansas City, Mo.)	0
176	Louisiana Music Educators Association	0
178	Music Educators National Conference.  Southern Divison.	0
180	American Conservatory of Music (Chicago, Ill.)	0
39	Dawson, William Levi	0
2001	National Interscholastic Music Activities Commission	0
177	ERASE 2	0
134	ERASE 1	0
163	ERASE 3	0
2003	Music Educators National Conference	0
140	National Museum of American History (U.S.)	0
2004	Iberia Lineas Aearas Espanolas	0
2005	Bowles, Chester	0
2006	Taylor, Mrs. William Kirkham	0
2007	Chesterton, R. K.	0
2008	Spohn, George Weida	0
2009	Kenny, Nick	0
2010	Tilghman, H. G.	0
2011	Hultin, Evelyn	0
2012	Subers, Samuel M.	0
2013	Perry, Charles	0
2014	Wheelwright, D. Sterling	0
2015	Hull, Harry S., Jr.	0
2016	Milligan, Harold V.	0
\.


--
-- Data for TOC entry 230 (OID 12743378)
-- Name: Restrictions; Type: TABLE DATA; Schema: public; Owner: jbwhite
--

COPY "Restrictions" ("ID", "RestrictionList") FROM stdin;
1	Restricted - permission not sought
2	Restricted - permission granted
3	Unrestricted - copyright expired
4	Unrestricted - deed of gift or transfer agreement
5	Restricted copyrighted - permission not sought
6	Restricted copyrighted - permission granted
7	Restricted - donor deed of gift or transfer agreement
8	Restricted - classified
9	Restricted - non copyright issue
10	No restriction
11	Unknown
\.


--
-- Data for TOC entry 231 (OID 12743395)
-- Name: Paste Errors; Type: TABLE DATA; Schema: public; Owner: jbwhite
--

COPY "Paste Errors" ("Combo128", "ID", "RecordIDType", "OtherID", "Combo139", "Combo135", "Combo137", "RecordCreationDate", "Text38", "Combo40", "Combo42", "Combo44", "Combo46", "Title", "Subtitle", "Text48", "TOC", "Text50", "cmbCompletedBy", "txtCompletedOn", "chkComplete") FROM stdin;
\N	1164	local	\N	\N	Dawson, William Levi, 1899-1990.	William Levi Dawson papers	2006-06-14 00:00:00	\N	text	English	\N	MARBL, Robert W. Woodruff Library, Emory University	Program for the In-Service Conference sponsored by the Southern Division of the Music Educators National Conference, 2-5 February 1983	\N	William Levi Dawson presented a choral reading session on African American spirituals and folk songs.	\N	Only the cover and page 67 were scanned.  This is the cover.	\N	\N	f
\.


--
-- Data for TOC entry 232 (OID 12743403)
-- Name: ResourceType; Type: TABLE DATA; Schema: public; Owner: jbwhite
--

COPY "ResourceType" ("ID", "ResourceType") FROM stdin;
1	text
5	cartographic
6	notated music
8	sound recording-musical
9	still image
10	moving image
11	video recording
12	software, multimedia
13	mixed material
14	sound recording-nonmusical
15	three dimensional object
16	sound recording
\.


--
-- Data for TOC entry 233 (OID 12743424)
-- Name: RightsAccess; Type: TABLE DATA; Schema: public; Owner: jbwhite
--

COPY "RightsAccess" ("ID", "Restriction", "RestrictionOther", "Content#", "Name", "CopyrightDate") FROM stdin;
22	11	no luna	1	48	1971-04-16
23	9	\N	820	37	\N
24	3	\N	822	42	\N
25	11	\N	2	48	1971-05-13
26	10	\N	1020	\N	\N
27	11	\N	5	48	1971-12-04
28	11	\N	3	48	1971-05-13
29	7	Reproduction and use of the image is restricted without written permission from Carol Hughes.  See WATCH list.	1027	49	1962-04-00
30	7	Reproduction and use of the image is restricted without written permission from Carol Hughes.  See WATCH file.  (Use contact information for Ted Hughes estate.)	1028	50	\N
31	7	Reproduction and use of the image is restricted without written permission from Carol Hughes.  See WATCH file for both Plath and Hughes.	1029	51	1959-08-00
32	7	Reproduction and use of the image is restricted without written permission from Carol Hughes.  See WATCH file.	1030	52	1959-08-00
33	7	\N	1032	50	1950-00-00
34	7	Reproduction and use of the image is restricted without written permission from Carol Hughes.  See WATCH list.	1033	0	\N
35	1	\N	1028	0	\N
36	7	\N	1031	0	\N
37	7	\N	1038	0	\N
38	7	\N	1040	0	\N
39	7	\N	1041	0	\N
40	7	\N	1042	0	\N
41	7	\N	1039	0	\N
42	7	\N	1043	0	\N
43	7	\N	1044	50	\N
44	7	\N	1045	50	\N
45	7	\N	1046	50	\N
46	7	\N	1089	50	\N
47	7	\N	1090	50	\N
48	7	\N	1091	50	1956-00-00
49	7	\N	1092	50	1961-00-00
50	7	\N	1093	50	1956-00-00
51	7	\N	1094	50	1960-00-00
52	7	\N	1095	50	\N
53	7	\N	1096	50	1993-00-00
54	7	\N	1097	50	1990-00-00
55	7	\N	1099	50	1960-00-00
56	7	\N	1100	50	1960-00-00
57	7	\N	1101	50	1946-00-00
58	7	\N	1102	50	1980-00-00
59	7	\N	1103	50	1970-00-00
60	7	\N	1104	50	1978-00-00
61	7	\N	1105	0	\N
62	7	\N	1107	50	1979-00-00
63	7	\N	1108	50	1970-00-00
64	7	\N	1109	0	\N
65	7	\N	1110	0	\N
66	3	\N	1106	0	\N
67	7	\N	1151	0	\N
68	7	\N	1152	0	\N
69	7	\N	1153	0	\N
70	7	\N	1154	0	\N
71	7	\N	1155	0	\N
72	7	\N	1156	0	\N
73	7	\N	1157	0	\N
74	7	\N	1158	0	\N
75	7	\N	1159	0	\N
76	7	\N	1160	50	1967-00-00
77	7	\N	1219	50	1966-00-00
78	7	\N	1221	50	1967-00-00
79	7	\N	1222	50	1967-00-00
80	7	\N	1223	50	1967-00-00
81	7	\N	1224	50	1977-00-00
82	7	\N	1225	50	1986-00-00
83	7	\N	1226	50	1970-00-00
84	7	\N	1227	50	1992-00-00
85	7	\N	1228	50	1973-00-00
86	7	\N	1229	50	1978-00-00
87	7	\N	1230	50	1963-00-00
88	7	\N	1231	50	1973-00-00
89	7	\N	1232	50	1973-00-00
90	7	\N	1234	50	1973-00-00
91	7	\N	1233	50	1973-00-00
92	7	\N	1235	50	1973-00-00
93	7	\N	1237	50	1973-00-00
94	7	\N	1242	50	1973-00-00
95	7	\N	1243	50	1960-05-10
96	7	\N	1244	50	1960-05-10
97	7	\N	1245	50	1997-00-00
98	7	\N	1247	50	1940-00-00
99	7	\N	1098	50	1980-00-00
100	7	\N	1087	50	1980-00-00
101	7	\N	1088	50	1970-00-00
102	7	\N	1246	50	1960-07-25
103	7	\N	1220	50	1967-00-00
104	5	\N	1150	56	1946-00-00
108	7	\N	1264	50	1960-04-21
109	7	\N	1265	50	1990-00-00
110	7	\N	1266	50	1978-00-00
111	7	\N	1267	50	1980-00-00
112	7	\N	1269	50	1997-00-00
113	7	\N	1270	50	1980-00-00
114	7	\N	1271	50	1966-00-00
115	7	\N	1272	50	1977-00-00
116	7	\N	1273	50	1980-00-00
117	7	\N	1274	50	1970-00-00
118	7	\N	1275	50	1990-00-00
119	7	\N	1276	50	1970-00-00
125	5	\N	1281	136	1951-12-23
126	5	\N	1282	136	1951-12-23
127	5	\N	1283	136	1951-12-23
128	5	\N	1284	136	1951-12-23
129	5	\N	1285	136	1951-12-23
130	5	\N	1286	137	1953-11-27
131	5	\N	1287	138	1955-01-28
132	5	\N	1288	138	1955-02-08
133	6	\N	1289	57	1955-02-22
136	11	\N	1292	48	1982-05-16
137	6	\N	1293	57	1918-00-00
138	6	\N	1294	57	1918-00-00
139	6	\N	1295	57	1918-00-00
140	6	\N	1296	57	1918-00-00
141	6	\N	1297	57	1918-00-00
142	6	\N	1298	57	1918-00-00
143	6	\N	1299	57	1918-00-00
144	6	\N	1300	57	1918-00-00
145	6	\N	1301	57	1918-00-00
146	6	\N	1302	57	1918-00-00
147	6	\N	1303	57	1918-00-00
148	6	\N	1304	57	1918-00-00
149	6	\N	1306	57	1952-11-14
150	6	\N	1307	57	1952-12-04
151	6	\N	1308	57	1952-12-08
152	6	\N	1309	57	1952-12-11
153	6	\N	1310	57	1956-07-16
154	6	\N	1311	57	1956-07-19
155	6	\N	1312	57	1956-07-24
156	6	\N	1313	57	1956-08-08
157	7	\N	1314	50	1990-00-00
158	7	\N	1315	50	1950-00-00
159	7	\N	1316	50	1950-00-00
160	7	\N	1317	50	1990-08-12
161	10	\N	1318	50	1990-08-12
162	10	\N	1319	50	1958-10-30
163	7	\N	1320	50	1958-08-30
164	7	\N	1321	50	1984-12-22
165	6	\N	1322	57	1981-00-00
166	6	\N	1323	57	1981-00-00
167	6	\N	1324	57	1981-00-00
168	6	\N	1325	57	1981-00-00
169	6	\N	1326	57	1981-00-00
170	6	\N	1327	57	1981-00-00
171	6	\N	1328	57	1981-00-00
172	6	\N	1329	57	1981-00-00
173	6	\N	1330	57	1981-00-00
174	6	\N	1331	57	1981-00-00
175	6	\N	1332	57	1981-00-00
176	6	\N	1333	57	1981-00-00
177	6	\N	1334	57	1981-00-00
178	6	\N	1335	57	1981-00-00
179	6	\N	1336	57	1981-00-00
180	6	\N	1337	57	1981-00-00
181	6	\N	1338	57	1981-00-00
182	6	\N	1339	57	1981-00-00
183	6	\N	1340	57	1981-00-00
184	6	\N	1341	57	1981-00-00
185	6	\N	1342	57	1981-00-00
186	6	Probably written in 1978 or 1979.	1343	57	1978-00-00
187	6	Probably written in 1978 or 1979.	1344	57	1978-00-00
189	3	\N	1346	\N	1928-11-28
190	10	\N	1347	\N	1928-11-16
196	7	\N	1368	50	1978-05-17
197	7	\N	1369	50	1978-05-17
198	7	\N	1370	50	1960-00-00
199	11	Image acquired from Notley Advertising Agency.  Photographer unknown.  Deed of gift did not specify copyright status.  Not covered by restrictions placed by Carol Hughes.	1371	\N	\N
200	7	\N	1373	50	1958-00-00
201	7	\N	1374	50	1959-07-00
202	7	\N	1377	50	1959-07-00
203	7	\N	1378	50	1958-07-00
204	7	\N	1379	50	1959-07-00
205	7	\N	1380	50	1960-06-23
206	7	\N	1381	50	1960-00-00
207	7	\N	1382	50	1973-00-00
208	7	\N	1383	49	1962-04-00
209	7	\N	1384	50	1995-00-00
210	7	\N	1385	50	1956-00-00
211	7	\N	1386	50	1958-00-00
212	7	\N	1387	50	1961-00-00
213	7	\N	1388	50	1940-00-00
214	7	\N	1389	50	\N
215	7	\N	1390	50	1959-07-00
216	7	\N	1391	50	1954-00-00
217	10	\N	1392	50	1947-00-00
218	7	\N	1393	50	\N
219	7	\N	1394	50	1960-00-00
220	10	\N	1395	50	1957-00-00
221	7	\N	1396	50	1970-00-00
222	7	\N	1397	50	1970-00-00
223	7	\N	1398	50	1970-00-00
224	3	\N	1400	58	1904-00-00
225	3	\N	1399	\N	1904-00-00
226	3	\N	1401	0	1915-00-00
227	3	\N	1402	0	1916-00-00
228	3	\N	1403	59	1916-00-00
229	3	\N	1404	0	1918-07-04
230	3	\N	1405	59	1920-05-00
231	3	\N	1406	59	1920-00-00
232	11	\N	1407	0	\N
233	3	\N	1408	0	1920-00-00
234	3	\N	1409	60	1922-00-00
235	3	\N	1410	48	1922-00-00
236	3	\N	1411	59	1922-00-00
237	3	\N	1412	59	1922-00-00
238	3	\N	1413	61	1922-00-00
239	3	\N	1414	59	1922-00-00
240	3	\N	1415	59	1922-00-00
241	3	\N	1416	59	1923-00-00
242	3	\N	1417	59	1923-00-00
243	3	\N	1418	59	1923-00-00
244	3	\N	1419	59	1923-00-00
245	3	\N	1420	59	1923-00-00
246	3	\N	1421	59	1923-00-00
247	11	\N	1422	48	1923-00-00
248	3	\N	1423	48	1923-07-16
249	3	\N	1424	48	1923-00-00
250	3	\N	1425	60	1923-00-00
251	3	\N	1426	60	1923-00-00
252	11	\N	1427	48	\N
253	3	\N	1428	64	1923-00-00
254	3	\N	1429	61	1942-00-00
255	3	\N	1430	59	1924-00-00
256	11	\N	1431	48	1924-00-00
257	3	\N	1432	61	1924-00-00
258	3	\N	1433	62	1924-00-00
259	3	\N	1434	48	1925-00-00
260	3	\N	1435	48	1925-00-00
261	3	\N	1436	48	1925-00-00
262	3	\N	1437	48	1925-00-00
263	3	\N	1439	61	1925-00-00
264	3	\N	1440	48	1925-00-00
265	3	\N	1441	48	1926-00-00
266	3	\N	1442	61	1926-00-00
267	3	\N	1443	61	1926-00-00
268	3	\N	1444	61	1926-00-00
269	3	\N	1445	61	1925-00-00
270	3	\N	1446	61	1926-00-00
271	3	\N	1447	63	1926-00-00
272	3	\N	1448	64	1926-00-00
273	3	\N	1449	61	1926-00-00
274	3	\N	1450	48	1926-00-00
275	3	\N	1451	61	1926-00-00
276	3	\N	1452	64	1926-00-00
277	3	\N	1453	61	1926-00-00
278	3	\N	1454	61	1926-00-00
279	3	\N	1455	61	1926-00-00
280	3	\N	1456	48	1926-00-00
281	3	\N	1457	48	1926-00-00
282	3	\N	1458	48	1926-00-00
283	3	\N	1459	48	1926-00-00
284	3	\N	1460	48	1026-00-00
285	3	\N	1461	61	1926-00-00
286	3	\N	1462	61	1926-00-00
287	10	\N	1463	48	1926-00-00
288	3	\N	1464	48	1926-00-00
289	11	\N	1465	62	\N
290	11	\N	1466	62	\N
291	3	\N	1467	64	1927-08-24
292	3	\N	1468	64	1927-08-24
293	3	\N	1469	64	1927-08-25
294	3	\N	1470	64	1927-08-25
295	10	\N	1471	48	1927-08-27
296	3	\N	1472	64	1927-08-27
297	3	\N	1473	64	1927-08-27
298	3	\N	1474	64	1927-08-27
299	3	\N	1475	64	1927-08-27
300	10	\N	1476	64	\N
301	3	\N	1476	64	1927-08-28
302	3	\N	1477	64	1927-08-00
303	3	\N	1478	64	1927-08-00
304	3	\N	1479	64	1927-00-00
305	3	\N	1480	48	1927-12-00
306	3	\N	1481	48	1927-12-00
307	3	\N	1482	73	1929-06-28
308	3	\N	1483	67	1929-06-27
309	3	\N	1484	67	1929-06-29
310	3	\N	1485	68	1929-06-29
311	3	\N	1486	64	1929-06-29
312	3	\N	1487	64	1929-06-00
313	3	\N	1488	67	1929-06-29
314	10	\N	1489	64	1929-06-30
315	10	\N	1490	64	1929-06-30
316	3	\N	1491	68	1929-06-30
317	3	\N	1492	68	1929-00-00
318	3	\N	1493	64	1929-00-00
319	3	\N	1494	64	1929-00-00
320	11	\N	1495	48	\N
321	11	\N	1496	48	\N
322	11	\N	1497	48	\N
323	3	\N	1498	69	1930-06-05
324	3	\N	1499	69	1930-06-05
325	3	\N	1500	69	1930-07-05
326	3	\N	1501	69	1930-07-05
327	3	\N	1502	69	1930-07-05
328	3	\N	1503	69	1930-07-05
329	3	\N	1504	69	1930-07-05
330	3	\N	1505	69	1930-07-05
331	3	\N	1506	69	1930-07-05
332	3	\N	1507	69	1930-07-05
333	3	\N	1508	69	1930-07-05
334	3	\N	1509	48	\N
335	3	\N	1510	48	1930-07-05
336	3	\N	1511	69	1930-05-00
337	10	\N	1512	69	1931-05-30
338	3	\N	1513	69	1930-05-31
339	10	\N	\N	51	\N
340	3	\N	1514	75	1930-05-31
341	3	\N	1515	69	1930-05-31
342	3	\N	1516	69	1930-05-31
343	3	\N	1517	69	1930-05-31
344	3	\N	1518	69	1930-06-18
345	3	\N	1519	69	1930-06-18
346	10	\N	1520	69	1930-06-20
347	3	\N	1521	69	1930-06-18
348	3	\N	1522	69	1930-06-18
349	3	\N	1523	69	1920-06-20
350	3	\N	1524	70	1930-06-27
351	3	\N	1525	70	1930-06-00
352	11	\N	1526	48	\N
353	5	\N	1527	72	\N
354	5	\N	1528	72	\N
355	5	\N	1529	73	\N
356	10	\N	1530	48	1930-00-00
357	3	\N	1531	48	\N
358	3	\N	1532	91	1935-00-00
359	3	\N	1533	91	1934-00-00
360	3	\N	1534	91	1935-00-00
361	3	\N	1535	91	1935-04-23
362	3	\N	1536	91	1935-00-00
363	3	\N	1537	91	1935-00-00
364	3	\N	1538	91	1936-04-04
365	11	\N	1539	48	1950-12-00
366	5	Maurey Garber, 48 West 48th St., New York, NY; Order No. 90.	1540	93	1955-00-00
367	11	\N	1541	48	1950-04-09
368	11	\N	1542	48	1950-04-09
369	11	\N	1543	48	0000-00-00
370	5	\N	1544	91	1955-00-00
371	3	\N	1545	91	1920-00-00
372	11	\N	1546	94	0000-00-00
373	11	\N	1547	48	1952-04-06
374	3	\N	1548	48	1918-00-00
375	3	\N	1549	48	1920-00-00
376	3	\N	1550	91	1920-00-00
377	3	\N	1551	48	1920-00-00
378	3	\N	1552	91	1926-00-00
379	3	\N	1553	91	1931-00-00
380	3	\N	1554	95	1934-11-21
381	3	\N	1555	68	1936-00-00
382	11	\N	1556	48	1945-00-00
383	11	\N	1557	48	1945-00-00
384	3	\N	1558	48	1920-00-00
385	11	\N	1559	48	1950-00-00
386	5	\N	1560	91	1939-04-01
387	1	\N	1561	57	1931-00-00
388	1	\N	1562	57	0000-02-08
389	1	\N	1563	57	1927-12-27
390	1	\N	1564	57	1934-11-20
391	1	1930s	1565	57	0000-00-00
392	1	1930s	1566	57	0000-00-00
393	5	\N	1567	48	\N
394	5	\N	1569	48	\N
395	5	\N	1570	48	\N
396	5	\N	1571	48	\N
397	1	\N	1572	48	\N
398	5	\N	1573	76	\N
399	5	\N	1574	74	1926-00-00
400	5	\N	1575	48	\N
401	10	\N	1576	48	\N
402	3	\N	1577	48	1930-08-21
403	10	\N	1578	70	1930-00-00
404	3	\N	1579	48	1930-00-00
405	3	\N	1580	70	1930-00-00
406	3	\N	1581	48	1930-00-00
407	11	\N	1582	48	\N
408	11	\N	1583	48	\N
409	11	\N	1584	48	\N
410	3	\N	1585	48	1923-00-00
411	11	\N	1586	48	\N
412	11	\N	1587	48	\N
413	11	\N	1588	48	\N
414	11	\N	1589	48	\N
415	11	\N	1590	78	\N
416	11	\N	1591	48	\N
417	3	\N	1592	48	1875-00-00
418	3	\N	1593	48	1875-00-00
419	3	\N	1594	48	1860-00-00
420	3	\N	1595	48	1938-00-00
421	3	\N	1596	48	1938-00-00
422	3	\N	1597	48	1903-00-00
423	11	\N	1602	48	\N
424	11	\N	1603	64	\N
425	3	\N	1604	48	1931-00-00
426	3	\N	1605	48	1931-00-00
427	11	\N	1606	48	1931-00-00
428	3	\N	1607	48	1931-00-00
429	3	\N	1608	48	1931-00-00
430	3	\N	1609	48	1931-00-00
431	3	\N	1610	48	1931-00-00
432	7	See WATCH list for copyright contact information.  Written permission from Carol Hughes required before reproductions can be shared with researchers.	1611	52	\N
433	11	Image acquired from Notley Advertising Agency.  Photographer unknown.  Deed of gift did not specify copyright status.  Not covered by restrictions placed by Carol Hughes.	1614	0	\N
434	11	Image acquired from Notley Advertising Agency.  Photographer unknown.  Deed of gift did not specify copyright status.  Not covered by restrictions placed by Carol Hughes.	1615	0	\N
435	11	Image acquired from Notley Advertising Agency.  Photographer unknown.  Deed of gift did not specify copyright status.  Not covered by restrictions placed by Carol Hughes.	1616	0	\N
436	3	\N	1617	48	1931-00-00
437	3	\N	1618	48	1931-00-00
438	3	\N	1619	48	1931-00-00
439	5	\N	1620	48	\N
440	5	\N	1621	48	\N
441	5	\N	1622	48	\N
442	5	\N	1623	48	\N
443	5	\N	1624	81	\N
444	5	\N	1625	81	\N
445	5	\N	1626	82	1952-09-02
446	5	\N	1627	48	\N
447	5	\N	1628	48	1955-00-00
448	5	\N	1629	48	1955-00-00
449	5	\N	1630	48	1955-00-00
450	5	\N	1631	48	1955-00-00
451	11	\N	1632	48	\N
452	5	\N	1633	48	\N
453	5	\N	1634	48	\N
454	5	\N	1635	48	\N
455	5	\N	1636	83	1958-00-00
456	5	\N	1637	48	1958-00-00
457	5	\N	1638	81	1959-00-00
458	5	\N	1639	84	1959-00-00
459	5	\N	1640	48	1958-00-00
460	5	\N	1641	85	1960-00-00
461	5	\N	1642	86	1964-00-00
462	10	\N	1643	87	1966-05-00
463	5	\N	1644	63	1972-05-00
464	5	\N	1645	48	\N
465	3	\N	1646	0	1930-00-00
466	5	\N	1647	91	1946-08-00
467	5	\N	1648	91	1939-04-01
468	3	\N	1649	96	1933-00-00
469	11	American Society of Composers, Authors and Publishers (ASCAP), New York, NY.	1650	97	0000-00-00
470	10	\N	1651	48	1944-08-13
471	10	\N	1652	48	0000-00-00
472	11	\N	1653	48	1964-00-00
473	6	\N	1654	57	0000-00-00
474	11	\N	1655	91	0000-00-00
475	11	\N	1656	48	1937-06-00
476	5	\N	1657	98	1963-10-29
477	3	\N	1658	146	1934-11-01
478	11	\N	1659	147	0000-00-00
479	1	\N	1660	57	0000-00-00
480	11	\N	1661	48	0000-00-00
481	5	Rights holder is probably Tuskegee University.	1662	91	1955-00-00
482	3	\N	1663	148	1933-01-11
483	3	\N	1664	68	1936-00-00
484	11	\N	1665	48	0000-00-00
485	5	\N	1666	107	0000-00-00
486	11	\N	1667	48	0000-00-00
487	11	\N	1668	48	1970-03-14
488	5	\N	1669	108	1979-00-00
489	11	\N	1670	48	1978-05-07
490	3	\N	1671	149	1921-03-17
491	3	\N	1672	149	1921-03-17
492	11	\N	1673	109	0000-00-00
493	11	\N	1674	48	1956-00-00
494	11	\N	1675	48	1956-00-00
495	11	\N	1676	48	1951-08-00
496	1	\N	1677	57	0000-00-00
497	1	1934-1935	1678	57	0000-00-00
498	1	\N	1679	57	1952-04-06
499	11	\N	1680	48	0000-00-00
500	5	\N	1681	98	1963-29-10
501	11	\N	1682	48	1952-00-00
502	11	\N	1683	48	0000-00-00
503	3	\N	1685	48	1931-00-00
504	3	\N	1686	48	1931-00-00
505	3	\N	1687	48	1930-00-00
506	11	\N	1688	88	\N
507	11	\N	1689	89	\N
508	3	\N	1690	90	1930-00-00
509	11	\N	1691	48	\N
510	3	\N	1692	90	1930-00-00
511	10	\N	1532	\N	\N
512	11	\N	1693	90	\N
513	11	\N	1694	48	\N
514	11	\N	1695	48	\N
515	11	\N	1696	48	\N
516	11	\N	1697	48	\N
517	3	\N	1698	92	\N
518	11	\N	1699	48	\N
519	11	\N	1700	48	\N
520	11	\N	1701	48	\N
521	11	\N	1702	48	\N
522	11	\N	1703	48	\N
523	3	\N	1704	48	1930-05-00
524	11	\N	1705	48	\N
525	3	\N	1707	99	\N
526	3	\N	1708	100	1886-00-00
527	10	\N	1709	101	1892-06-10
528	3	\N	1710	102	\N
529	3	\N	1714	48	1895-00-00
530	3	\N	1715	48	1895-00-00
531	3	\N	1716	48	1895-00-00
532	3	\N	1717	48	1895-00-00
533	3	\N	1718	48	1895-00-00
534	3	\N	1719	48	1895-00-00
535	3	\N	1720	48	1895-00-00
536	3	\N	1721	48	1895-00-00
537	3	\N	1722	48	1895-00-00
538	3	\N	1723	48	1895-00-00
539	3	\N	1711	48	1924-05-25
540	3	\N	1712	102	1924-05-25
541	3	\N	1713	102	\N
542	3	\N	1725	48	\N
543	3	\N	1726	103	\N
544	3	\N	1727	104	\N
545	3	\N	1728	48	1895-00-00
546	3	\N	1729	48	1895-00-00
547	3	\N	1730	104	1920-02-14
548	3	\N	1731	104	\N
549	3	\N	1732	48	\N
550	3	\N	1733	48	\N
551	3	\N	1734	48	1854-00-00
552	3	\N	1735	48	1854-00-00
553	3	\N	1736	103	\N
554	3	\N	1737	48	\N
555	3	\N	1738	48	\N
556	3	\N	1739	48	1900-02-07
557	3	\N	1740	48	1906-00-00
558	3	\N	1741	48	\N
559	3	\N	1742	48	1938-00-00
560	3	\N	1743	48	\N
561	3	\N	1744	48	\N
562	3	\N	1745	48	\N
563	3	\N	1746	48	1915-00-00
564	3	\N	1747	48	1917-00-00
565	3	\N	1748	48	\N
566	3	\N	1749	48	1875-00-00
567	3	\N	1750	48	1875-00-00
568	3	\N	1751	48	1875-00-00
569	3	\N	1752	48	1875-00-00
570	3	\N	1753	48	1875-00-00
571	11	\N	1754	48	1984-12-06
572	11	\N	1755	48	0000-00-00
573	11	\N	1756	48	0000-00-00
574	1	\N	1757	57	1963-10-29
575	11	\N	1758	48	0000-00-00
576	11	\N	1759	48	0000-00-00
577	11	\N	1760	48	0000-00-00
578	1	\N	1761	57	0000-00-00
579	1	\N	1762	57	0000-00-00
580	1	\N	1763	57	0000-00-00
581	3	\N	1764	48	1915-10-17
582	3	\N	1765	48	1915-10-17
583	3	\N	1766	91	1919-05-10
584	3	\N	1767	91	1919-05-10
585	1	\N	1768	57	1927-01-00
586	3	H.A. Atwell Studio, 81 W. Randolph St., Chicago, Illinois.	1769	111	1927-00-00
587	3	\N	1770	143	1927-05-06
588	11	\N	1771	48	1956-00-00
589	3	\N	1772	91	1931-11-00
590	6	\N	1773	57	0000-00-00
591	11	\N	1774	48	1950-12-00
592	11	\N	1775	48	1950-03-20
593	3	\N	1776	91	1921-00-00
594	1	\N	1777	57	0000-00-00
595	1	\N	1778	57	0000-00-00
596	11	\N	1779	144	1927-00-00
597	3	\N	1780	48	1870-00-00
598	3	\N	1781	48	1870-00-00
599	3	\N	1782	48	1838-00-00
600	3	\N	1783	110	1906-04-10
601	3	\N	1784	48	\N
602	3	\N	1785	48	\N
603	3	\N	1786	48	\N
604	3	\N	1787	48	\N
605	3	\N	1788	48	\N
606	5	\N	1789	48	1941-01-00
607	5	\N	1790	48	1941-01-00
608	5	\N	1791	48	1941-01-00
609	5	\N	1792	48	1941-01-00
610	5	\N	1793	48	1941-01-00
611	5	\N	1794	48	1941-01-00
612	5	\N	1795	48	1941-01-00
623	5	\N	1796	48	1938-00-00
624	5	\N	1797	48	1939-12-00
625	6	\N	1065	57	1956-00-00
626	5	\N	1798	48	1936-00-00
627	6	\N	1064	57	1956-00-00
628	6	\N	1063	57	1956-00-00
629	6	\N	1062	57	1956-00-00
630	6	\N	1061	57	1956-00-00
631	6	\N	1060	57	1956-00-00
632	3	\N	1799	48	1930-00-00
634	6	\N	1059	57	1956-00-00
635	5	\N	1800	48	1930-00-00
641	5	\N	1801	48	1963-12-00
642	5	\N	1802	48	1930-04-07
643	5	\N	1803	48	1964-09-14
644	5	\N	1804	48	1890-00-00
645	5	\N	1805	48	1941-01-00
646	3	\N	1806	48	1894-00-00
647	3	\N	1807	48	1894-00-00
648	3	\N	1808	48	1909-00-00
649	3	\N	1809	48	1909-00-00
650	3	\N	1810	48	1939-00-00
651	3	\N	1811	48	1921-00-00
652	3	\N	1812	48	1921-00-00
654	5	\N	1068	117	1975-03-13
655	5	\N	1072	117	1984-10-06
656	5	\N	1071	117	1984-10-06
657	5	\N	1070	117	1984-10-06
658	5	\N	1069	117	1984-10-06
659	5	\N	1075	116	1983-11-02
660	5	\N	1076	119	1983-11-10
661	6	\N	1077	57	1983-11-28
662	6	\N	1078	57	1983-11-28
663	6	\N	1079	57	1983-12-26
664	5	\N	1080	119	1984-01-09
665	1	\N	1813	0	1967-00-00
666	5	\N	1814	57	1962-00-00
667	5	\N	1815	57	1942-00-00
668	1	\N	1816	0	0000-00-00
669	5	\N	1817	150	1954-00-00
670	11	\N	1818	151	1926-00-00
671	1	\N	1819	0	1941-00-00
672	5	\N	1820	57	1965-00-00
673	5	\N	1821	57	1965-00-00
674	11	\N	1822	152	1925-00-00
675	11	\N	1823	152	1925-00-00
676	11	\N	1824	153	1934-00-00
677	11	\N	1825	154	1936-00-00
678	5	\N	1081	116	1985-03-26
679	6	\N	1082	57	1985-04-20
681	5	\N	1116	121	1978-05-07
682	5	\N	1117	121	1978-05-07
683	5	\N	1118	121	1978-05-07
684	6	\N	1127	57	1984-00-00
685	11	\N	1128	122	1984-04-12
686	5	\N	1129	123	1981-00-00
687	5	\N	1130	124	1985-01-16
688	6	\N	1135	57	1960-00-00
689	5	\N	1136	125	1960-05-07
690	6	\N	1137	57	1960-05-14
694	5	\N	1828	155	1943-00-00
695	11	\N	1829	169	1907-00-00
696	5	\N	1830	138	1953-03-20
697	5	\N	1831	138	1953-03-20
698	11	\N	1832	48	0000-00-00
699	5	\N	1833	129	1923-06-04
700	3	\N	1834	91	1936-04-04
701	3	\N	1835	91	1936-04-04
702	11	\N	1836	48	0000-00-00
703	11	\N	1837	57	0000-00-00
704	11	\N	1838	57	0000-00-00
705	11	\N	1839	57	0000-00-00
706	11	\N	1840	170	1921-00-00
707	11	\N	1841	171	1913-00-00
708	3	\N	1842	96	1933-01-00
709	11	\N	1843	169	1907-00-00
710	11	\N	1844	48	0000-00-00
711	5	\N	1845	57	0000-00-00
712	5	\N	1846	57	0000-00-00
713	5	\N	1847	57	0000-00-00
714	5	\N	1848	133	1942-00-00
715	3	\N	1850	48	1837-00-00
716	3	\N	1851	48	1837-00-00
717	3	\N	1852	48	1927-00-00
718	3	\N	1853	48	1847-00-00
719	3	\N	1854	48	1847-00-00
720	3	\N	1855	48	1847-00-00
721	3	\N	1856	48	1892-00-00
722	11	\N	1857	48	\N
723	5	\N	1858	48	1950-00-00
724	5	\N	1859	48	1950-00-00
725	5	\N	1860	48	1962-00-00
726	3	\N	1861	48	1922-00-00
727	3	\N	1862	48	1922-00-00
728	3	\N	1863	48	1848-00-00
729	5	\N	1864	48	1916-01-00
730	3	\N	1865	48	1806-00-00
731	3	\N	1866	134	1926-00-00
732	3	\N	1867	175	1926-00-00
733	11	\N	1868	57	0000-00-00
734	11	\N	1869	48	1923-00-00
735	11	Copyrighted in Great Britain.	1870	172	1929-00-00
736	1	\N	1871	0	1921-08-00
737	3	\N	1872	180	1927-05-28
738	5	\N	1873	57	0000-00-00
739	5	\N	1874	57	0000-00-00
740	3	\N	1875	91	1931-00-00
741	1	\N	1876	0	1932-12-00
742	1	\N	1877	0	1932-12-00
743	11	\N	1878	57	0000-00-00
744	11	\N	1879	57	0000-00-00
745	11	\N	1880	57	0000-00-00
746	11	\N	1881	57	0000-00-00
747	1	\N	1882	0	0000-00-00
748	5	\N	1883	135	1949-00-00
749	6	\N	1884	57	0000-00-00
750	5	\N	1885	156	1943-00-00
751	3	\N	1886	48	1916-00-00
752	3	\N	1887	48	1996-00-00
753	3	\N	1888	48	1944-06-00
754	3	\N	1889	48	1944-05-00
755	3	\N	1890	48	1911-00-00
756	3	\N	1891	48	1911-07-00
757	3	\N	1892	48	1940-00-00
758	5	\N	1893	48	1989-00-00
759	5	\N	1894	48	1942-03-00
760	5	\N	1895	48	\N
761	3	\N	1896	48	1919-00-00
762	3	\N	1897	48	1919-00-00
763	3	\N	1898	48	1919-00-00
764	3	\N	1899	48	1888-00-00
765	3	\N	1900	48	1888-00-00
766	3	\N	1901	48	1888-00-00
767	3	\N	1902	48	1938-00-00
768	3	\N	1903	48	1938-00-00
769	3	\N	1904	48	1938-00-00
770	5	\N	1905	48	1945-01-13
771	11	\N	1906	48	\N
772	5	\N	1907	48	1935-00-00
773	5	\N	1908	48	1935-00-00
774	3	\N	1909	48	1920-00-00
775	3	\N	1910	48	1920-00-00
776	3	\N	1911	48	1933-00-00
777	3	\N	1912	48	1895-00-00
778	5	\N	1913	157	1968-00-00
779	3	\N	1914	158	1934-00-00
780	3	\N	1915	158	1934-00-00
781	1	\N	1916	0	0000-00-00
782	5	\N	1917	57	0000-00-00
783	5	\N	1918	57	0000-00-00
784	1	\N	1919	0	0000-00-00
785	1	\N	1920	0	0000-00-00
786	1	\N	1921	0	0000-00-00
787	1	\N	1922	0	0000-00-00
788	1	\N	1923	0	0000-00-00
789	1	\N	1924	0	0000-00-00
790	5	\N	1925	159	1953-06-00
791	5	\N	1926	57	1943-00-00
792	1	\N	1927	0	0000-00-00
793	11	\N	1928	48	1960-12-00
794	11	\N	1929	91	0000-00-00
795	5	Date may be 1979.	1930	174	0000-00-00
796	5	\N	1931	91	1960-00-00
797	1	\N	1932	0	0000-00-00
798	1	\N	1933	0	0000-00-00
799	3	\N	1934	126	1916-12-00
800	3	\N	1935	48	1917-00-00
801	3	\N	1936	127	1917-00-00
803	6	\N	1142	57	1960-06-27
804	3	\N	1937	48	1916-00-00
805	6	\N	1143	57	1960-07-18
806	5	\N	1166	128	1983-03-02
807	3	\N	1938	130	1897-00-00
808	3	\N	1939	131	1922-00-00
809	3	\N	1940	131	1922-00-00
810	3	\N	1941	131	1922-00-00
811	11	\N	1942	48	\N
812	3	\N	1943	127	1927-00-00
813	3	\N	1944	127	1927-00-00
814	3	\N	1945	127	1927-00-00
815	3	\N	1946	127	1927-00-00
816	11	\N	1947	132	\N
817	11	\N	1948	132	\N
818	11	\N	1949	132	\N
819	6	\N	1279	57	0000-00-00
820	5	\N	1169	139	1983-10-26
830	6	\N	1179	57	1946-03-01
831	6	\N	1180	57	1946-03-01
832	6	\N	1181	57	1946-03-01
833	6	\N	1182	57	1946-03-01
834	6	\N	1183	57	1946-03-01
835	10	\N	1188	140	1983-11-01
836	10	\N	1188	\N	\N
837	10	\N	1189	140	1983-11-01
838	6	\N	1190	57	1983-11-12
839	10	\N	1191	140	1984-02-09
840	6	\N	1305	57	1918-00-00
841	11	\N	1950	132	\N
842	11	\N	1951	132	\N
843	3	\N	1952	127	1916-00-00
844	11	\N	1953	127	1991-10-31
845	3	\N	1954	127	1916-00-00
846	11	\N	1955	127	\N
847	5	\N	1956	127	1929-00-00
848	11	\N	1957	127	\N
849	11	\N	1958	127	\N
850	11	\N	1959	132	\N
851	11	\N	1960	132	\N
852	5	\N	1961	67	1942-00-00
853	11	\N	1962	48	\N
854	11	\N	1963	132	1927-00-00
855	5	\N	1964	127	1941-11-01
856	11	\N	1965	127	\N
857	11	\N	1966	127	\N
859	6	\N	1192	57	1984-03-06
860	10	\N	1199	145	\N
861	10	\N	1200	145	\N
862	10	\N	1201	145	\N
863	10	\N	1202	145	\N
873	5	\N	1925	160	1952-00-00
874	5	\N	1967	150	1937-00-00
875	3	\N	1968	162	1913-00-00
876	11	\N	1969	164	\N
877	3	\N	1970	165	1919-00-00
878	5	\N	1971	166	1937-00-00
879	5	\N	1972	166	1937-00-00
880	3	\N	1973	48	1915-00-00
881	5	\N	1974	48	1938-00-00
882	3	\N	1975	126	1911-04-00
883	5	\N	1976	48	1947-01-00
884	10	\N	1977	48	1947-11-00
885	5	\N	1978	167	1937-00-00
886	5	\N	1979	168	1970-00-00
887	3	\N	1980	48	1911-07-00
888	5	\N	1982	67	1942-10-00
889	3	\N	1983	48	1900-00-00
890	3	\N	1984	48	1900-00-00
891	11	\N	1985	48	\N
892	11	\N	1986	48	1955-03-00
893	11	\N	1987	48	1955-03-00
894	11	\N	1988	48	\N
895	11	\N	1989	48	\N
896	11	\N	1990	173	\N
897	11	\N	1991	48	\N
898	11	\N	1992	173	\N
899	11	\N	1993	173	\N
900	11	\N	1994	173	\N
901	11	\N	1995	48	1933-04-04
902	11	\N	1996	173	1933-04-04
903	11	\N	1997	173	1933-04-04
904	11	\N	1998	173	1933-04-04
905	11	\N	1999	173	1933-04-04
906	11	\N	2000	173	1933-04-04
907	11	\N	2001	173	1933-04-04
908	11	\N	2002	173	1933-04-04
909	11	\N	2003	173	1933-04-04
910	11	\N	2004	173	1933-04-04
911	11	\N	2005	173	1933-04-04
912	11	\N	2006	173	1933-04-04
913	11	\N	2007	173	1933-04-04
914	11	\N	2008	173	1933-04-04
915	11	\N	2009	173	1933-04-04
916	5	\N	2010	48	1975-04-26
917	5	\N	2011	48	1975-04-26
918	11	\N	4	48	1971-12-04
919	11	\N	6	48	0000-00-00
920	11	\N	7	48	0000-00-00
921	11	\N	8	48	1974-03-09
922	11	\N	9	48	1974-03-09
923	11	\N	10	48	1974-03-09
924	11	\N	11	48	1976-03-20
925	11	\N	12	48	1979-03-12
926	11	\N	13	48	1979-03-12
927	5	\N	1073	117	1989-01-26
928	5	\N	1074	117	1989-01-26
929	5	\N	1083	119	1989-00-00
930	5	\N	1084	119	1984-02-00
931	5	\N	1113	121	1978-05-07
932	5	\N	1114	121	1978-05-07
933	5	\N	1115	121	1978-05-07
934	5	\N	1119	121	1978-00-00
935	5	\N	1120	176	1984-11-00
936	5	\N	1121	176	1984-11-00
937	5	\N	1122	176	1984-11-00
938	5	\N	1123	176	1984-11-00
939	5	\N	1124	176	1984-11-00
940	5	\N	1125	176	1984-11-00
941	5	\N	1126	176	1984-11-00
942	5	\N	1131	124	1985-01-14
943	5	\N	1132	124	1985-01-14
946	5	\N	1164	178	1983-02-00
947	5	\N	1165	178	1983-02-00
948	5	\N	1167	139	1984-02-02
949	5	\N	1168	139	1984-02-02
135	5	\N	1291	91	1934-01-09
802	5	Rights holder should be the National Interscholastic Music Activities Commission.	1141	\N	1960-06-20
134	5	This item most likely dates from the period 1933-1947.	1290	91	0000-00-00
188	10	\N	1345	\N	1927-00-00
192	3	\N	1349	48	1935-09-21
195	10	\N	1352	142	\N
194	10	\N	1351	\N	\N
193	10	\N	1350	\N	\N
191	10	\N	1348	\N	\N
638	2	\N	1034	57	\N
637	2	\N	1035	57	\N
636	2	\N	1036	57	\N
120	2	\N	1037	57	\N
105	2	\N	1047	57	\N
106	2	\N	1048	57	\N
613	2	\N	1049	57	\N
614	2	\N	1050	57	\N
615	2	\N	1051	57	\N
616	2	\N	1052	57	\N
617	2	\N	1053	57	\N
618	2	\N	1054	57	\N
619	2	\N	1055	57	\N
620	2	\N	1056	57	\N
621	2	\N	1057	57	\N
622	2	\N	1058	57	\N
640	10	\N	1066	\N	\N
639	10	Statement of facts without creative presentation.	1066	\N	\N
653	10	Statement of facts without creative presentation.	1067	\N	\N
107	5	Copyright holder should be Rebecca T. Cureau	1111	\N	1985-09-13
680	5	Copyright holder should be Rebecca T. Cureau	1112	\N	1985-09-13
945	5	\N	1134	125	1961-01-16
944	5	\N	1133	125	1961-01-16
691	5	Rights holder should be the Music Educators National Conference	1138	\N	1960-05-25
692	5	Rights holder should be the Music Educators National Conference	1139	\N	1960-05-25
693	5	Rights holder should be the Music Educators National Conference	1140	\N	1960-05-25
826	5	\N	1175	48	1944-00-00
829	6	\N	1178	57	1946-02-25
828	6	\N	1177	57	1946-02-21
827	6	\N	1176	57	1946-02-21
821	5	\N	1170	48	1944-00-00
822	5	\N	1171	48	1944-00-00
823	5	\N	1172	48	1944-00-00
824	5	\N	1173	48	1944-00-00
825	5	\N	1174	48	1944-00-00
2001	5	rights holder is Organization of American Kodaly Educators	1184	0	1984-04-00
2002	5	rights holder is Organization of American Kodaly Educators	1185	0	1984-04-00
2003	10	\N	1186	140	1984-02-00
2004	10	\N	1187	140	1984-02-00
2005	11	\N	1193	48	0000-00-00
2006	11	\N	1194	48	0000-00-00
2007	10	\N	1195	\N	\N
2008	10	\N	1196	0	\N
2009	10	\N	1197	\N	\N
864	5	\N	1203	2005	1937-00-00
2010	5	\N	1203	2006	1937-00-00
865	5	\N	1204	2007	1937-00-00
866	5	\N	1205	2008	1937-00-00
2011	5	\N	1205	2009	1937-00-00
867	5	\N	1206	2010	1937-00-00
868	5	\N	1207	2011	1937-00-00
869	5	\N	1208	2012	1937-00-00
2012	5	\N	1208	2013	1937-00-00
870	5	\N	1209	2014	1937-00-00
871	5	\N	1210	2015	1937-00-00
872	5	\N	1210	2016	1937-00-00
121	10	\N	1277	\N	\N
122	5	\N	1278	91	1955-03-19
123	5	\N	1279	48	1955-03-16
124	5	\N	1280	48	1955-03-16
\.


--
-- Data for TOC entry 234 (OID 12744361)
-- Name: Role; Type: TABLE DATA; Schema: public; Owner: jbwhite
--

COPY "Role" ("ID", "RoleName", "RoleCode") FROM stdin;
1	Actor	Act
2	Adapter	Adp
3	Author of afterword, colophon, etc.	Aft
4	Annotator	Ann
5	Bibliographic antecedent	Ant
6	Applicant	App
7	Author in quotations or text abstracts	Aqt
8	Architect	Arc
9	Arranger	Arr
10	Artist	Art
11	Assignee	Asg
12	Associated name	Asn
13	Attributed name	Att
14	Auctioneer	Auc
15	Author of dialog	Aud
16	Author of introduction	Aui
17	Author of screenplay	Aus
18	Author	Aut
19	Binding designer	Bdd
20	Bookjacket designer	Bjd
21	Book designer	Bkd
22	Book producer	Bkp
23	Binder	Bnd
24	Bookplate designer	Bpd
25	Bookseller	Bsl
26	Conceptor	Ccp
27	Choreographer	Chr
28	Collaborator	Clb
29	Client	Cli
30	Calligrapher	Cll
31	Collotyper	Clt
32	Commentator	Cmm
33	Composer	Cmp
34	Compositor	Cmt
35	Conductor	Cnd
36	Censor	Cns
37	Contestant-appellee	Coe
38	Collector	Col
39	Compiler	Com
40	Contestant	Cos
41	Contestant-appellant	Cot
42	Copyright claimant	Cpc
43	Complainant-appellee	Cpe
44	Copyright holder	Cph
45	Complainant	Cpl
46	Complainant-appellant	Cpt
47	Creator	Cre
48	Correspondent	Crp
49	Corrector	Crr
50	Consultant	Csl
51	Consultant to a project	Csp
52	Costume designer	Cst
53	Contributor	Ctb
54	Contestee-appellee	Cte
55	Cartographer	Ctg
56	Contractor	ctr
57	Contestee	cts
58	Contestee-appellant	ctt
59	Curator	cur
60	Commentator for written text	cwt
61	Defendant	dfd
62	Defendant-appellee	dfe
63	Defendant-appellant	dft
64	Degree grantor	dgg
65	Dissertant	dis
66	Delineator	dln
67	Dancer	dnc
68	Donor	dnr
69	Depositor	dpt
70	Draftsman	drm
71	Director	drt
72	Designer	dsr
73	Distributor	dst
74	Dedicatee	dte
75	Dedicator	dto
76	Dubious author	dub
77	Editor	edt
78	Engraver	egr
79	Electrotyper	elt
80	Engineer	eng
81	Etcher	etr
82	Expert	exp
83	Facsimilist	fac
84	Film editor	flm
85	Former owner	fmo
86	Funder	fnd
87	Forger	frg
88	Graphic technician	grt
89	Honoree	hnr
90	Host	hst
91	Illustrator	ill
92	Illuminator	ilu
93	Inscriber	ins
94	Inventor	inv
95	Instrumentalist	itr
96	Interviewee	ive
97	Interviewer	ivr
98	Librettist	lbt
99	Libelee-appellee	lee
100	Libelee	lel
101	Lender	len
102	Libelee-appellant	let
103	Libelant-appellee	lie
104	Libelant	lil
105	Libelant-appellant	lit
106	Landscape architect	lsa
107	Licensee	lse
108	Licensor	lso
109	Lithographer	ltg
110	Lyricist	lyr
111	Metadata contact	mdc
112	Moderator	mod
113	Monitor	mon
114	Metal-engraver	mte
115	Musician	mus
116	Narrator	nrt
117	Opponent	opn
118	Originator	org
119	Organizer of meeting	orm
120	Other	oth
121	Owner	own
122	Patron	pat
123	Publishing director	pbd
124	Publisher	pbl
125	Proofreader	pfr
126	Photographer	pht
127	Platemaker	plt
128	Printer of plates	pop
129	Papermaker	ppm
130	Process contact	prc
131	Production personnel	prd
132	Performer	prf
133	Programmer	prg
134	Producer	pro
135	Printer	prt
136	Patent applicant	pta
137	Plaintiff-appellee	pte
138	Plaintiff	ptf
139	Patent holder	pth
140	Plaintiff-appellant	ptt
141	Rubricator	rbr
142	Recording engineer	rce
143	Recipient	rcp
144	Redactor	red
145	Renderer	ren
146	Researcher	res
147	Reviewer	rev
148	Respondent-appellee	rse
149	Respondent	rsp
150	Respondent-appellant	rst
151	Research team head	rth
152	Research team member	rtm
153	Scientific advisor	sad
154	Scenarist	sce
155	Scribe	scr
156	Sculptor	scl
157	Secretary	sec
158	Signer	sgn
159	Singer	sng
160	Speaker	spk
161	Sponsor	spn
162	Surveyor	srv
163	Standards body	stn
164	Stereotyper	str
165	Thesis advisor	ths
166	Transcriber	trc
167	Translator	trl
168	Type designer	tyd
169	Typographer	tyg
170	Vocalist	voc
171	Writer of accompanying material	wam
172	Woodcutter	wdc
173	Wood-engraver	wde
174	Witness	wit
\.


--
-- Data for TOC entry 235 (OID 12744541)
-- Name: NameDetail; Type: TABLE DATA; Schema: public; Owner: jbwhite
--

COPY "NameDetail" ("ContentID", "Name", "Role", "RoleTerm") FROM stdin;
2	41	0	\N
276	39	134	personal
277	39	134	personal
278	39	134	personal
279	39	134	personal
280	39	134	personal
281	39	134	personal
282	39	134	personal
283	39	134	personal
284	39	134	personal
284	40	10	corporate
820	39	124	corporate
820	41	0	\N
822	41	0	\N
822	42	124	corporate
822	44	135	corporate
823	46	126	personal
999	37	97	\N
999	38	96	\N
1020	42	0	\N
1020	44	0	\N
1145	53	97	personal
1146	53	97	personal
1146	54	96	personal
0	162	0	\N
0	173	0	\N
1280	0	\N	\N
2013	161	6	personal
2024	142	0	\N
\.


--
-- Data for TOC entry 236 (OID 12744578)
-- Name: StaffName; Type: TABLE DATA; Schema: public; Owner: jbwhite
--

COPY "StaffName" ("ID", "StaffName") FROM stdin;
1	Teresa Burk
2	Naomi Nelson
3	Kate Murray
4	Brandy Scott
5	Susan Potts McDonald
6	Elizabeth Russy
8	Laura Akerman
\.


--
-- Data for TOC entry 237 (OID 12744593)
-- Name: SourceStillImage; Type: TABLE DATA; Schema: public; Owner: jbwhite
--

COPY "SourceStillImage" ("ID", "Form", "DimensionHeight", "DimensionHeightUnit", "DimensionWidth", "DimensionWidthUnit", "DimensionNote", "Disposition", "Generation", "SourceNote", "RelatedItem", "ItemLocation", "Content#", "HousingDescriptionPhoto", "ConservationHistory", "SourceDate", "PublicationDate") FROM stdin;
45	111	12	inches	12	inches	\N	retained	original	\N	\N	\N	820	23	\N	2006-00-00	\N
46	5	6	inches	4	inches	\N	retained	original	\N	There are other postcards printed for the Augusta News by Colorpicture in EUPIX.	EUPIX - unprocessed postcards	822	24	\N	\N	\N
47	2	4	inches	5	inches	\N	retained	original	Hinge is broken.	\N	Box 1	823	21	\N	1856-99-99	\N
48	79	0	inches	0	inches	\N	retained	\N	\N	\N	\N	\N	0	\N	\N	\N
49	5	0	inches	0	inches	\N	retained	\N	\N	see box 179 4-21 for other family pictures from this time period; 1383	Series 7 (Photographs), Box 179, folder 11	1027	0	\N	1962-04-00	\N
50	6	0	inches	0	inches	\N	retained	\N	\N	see box 177 folders 1-47 for other portraits of Hughes.	Series 7 (Photographs), Box 177, Folder 16?	1028	0	\N	1970-00-00	\N
51	6	0	inches	0	inches	\N	retained	\N	\N	There is a similar photograph of Plath in the same folder.	Series 7 (Photographs), Box 177, Folder 56	1029	0	\N	1959-08-00	\N
52	6	0	inches	0	inches	\N	retained	\N	\N	There is a similar photograph of Hughes in the same folder.	Series 7 (Photographs), Box 177, Folder 56	1030	0	\N	1959-08-00	\N
53	6	0	inches	0	inches	\N	retained	\N	\N	see box 177 folders 1-47 for other portraits of Hughes.	SERIES 7 PHOTOGRAPHS, ca. 1910-1995 box 1 folder  59	1032	0	\N	1950-00-00	\N
54	0	0	inches	0	inches	\N	retained	\N	\N	Other pages from this notebook have been scanned.	Subseries 2.1 (notebooks), box 57, folder 1	1033	0	\N	\N	\N
56	0	11	inches	8	inches	\N	retained	original	\N	1034, 1036, 1037	Series 4 Writings by Dawson, Box 29, Folder 3	1035	0	\N	0000-00-00	\N
57	0	11	inches	8	inches	\N	retained	original	\N	1034, 1035, 1037	Series 4 Writings by Dawson, Box 29, Folder 3	1036	0	\N	0000-00-00	\N
58	0	11	inches	8	inches	\N	retained	original	\N	1034, 1035, 1036	Series 4 Writings by Dawson, Box 29, Folder 3	1037	0	\N	0000-00-00	\N
59	6	0	inches	0	inches	\N	retained	\N	\N	5 photos on ship (1029, 1030)	SERIES 7 PHOTOGRAPHS, ca. 1910-1995, box 177 folder 57	1038	0	\N	1959-12-00	\N
60	5	0	inches	0	inches	\N	retained	\N	\N	6 images from same series	SERIES 2 WRITINGS BY TED HUGHES, ca. 1949-1990, box 57 folder 1.	1040	0	\N	1949-00-00	\N
61	5	0	inches	0	inches	\N	retained	\N	\N	6 images from same series	SERIES 2 WRITINGS BY TED HUGHES, ca. 1949-1990, box 57 folder 8.	1041	0	\N	1965-00-00	\N
62	5	0	inches	0	inches	\N	retained	\N	\N	6 images from same series	SERIES 2 WRITINGS BY TED HUGHES, ca. 1949-1990, box 57 folder 8.	1042	0	\N	1965-00-00	\N
63	5	0	inches	0	inches	\N	retained	\N	\N	6 images from same series	SERIES 2 WRITINGS BY TED HUGHES, ca. 1949-1990, box 57 folder 8.	1039	0	\N	1965-00-00	\N
64	5	0	inches	0	inches	\N	retained	\N	\N	6 items from same series	SERIES 2 WRITINGS BY TED HUGHES, ca. 1949-1990, box 57 folder 8.	1043	0	\N	1965-00-00	\N
65	6	0	inches	0	inches	\N	retained	\N	\N	Displayed in the 2006 exhibition, "No Other Appetite" at the Grolier Club in New York.	SERIES 7 PHOTOGRAPHS, ca. 1910-1995 box 177 folder 52	1044	0	\N	1958-00-00	\N
66	6	0	inches	0	inches	\N	retained	\N	Displayed in the 2006 exhibition, "No Other Appetite" at the Grolier Club in New York.	1380.	SERIES 7 PHOTOGRAPHS, ca. 1910-1995 box 178 folder 14.	1045	0	\N	1960-06-23	\N
67	6	0	inches	0	inches	\N	retained	\N	\N	1374,77,78.	SERIES 7 PHOTOGRAPHS, ca. 1910-1995 box 179 folder 6.	1046	0	\N	1959-00-00	\N
89	0	11	inches	8	inches	\N	retained	original	\N	\N	Series 5 Subject Files, Box 30, Folder 2	1068	0	\N	1975-03-13	\N
94	0	11	inches	8	inches	\N	retained	original	\N	1074	Series 5: Box 30, Folder 3	1073	0	\N	1989-01-26	\N
95	0	11	inches	8	inches	\N	retained	original	\N	1073	Series 5: Box 30, Folder 3	1074	0	\N	1984-01-26	\N
96	0	11	inches	8	inches	\N	retained	original	\N	\N	Series 5 Subject Files, Box 30, Folder 10	1075	0	\N	1983-11-02	\N
97	0	11	inches	8	inches	\N	retained	original	\N	\N	Series 5 Subject Files, Box 30, Folder 10	1076	0	\N	1983-11-10	\N
98	0	11	inches	8	inches	\N	retained	original	\N	\N	Series 5 Subject Files, Box 30, Folder 10	1077	0	\N	1983-11-28	\N
99	0	11	inches	8	inches	\N	retained	original	\N	\N	Series 5 Subject Files, Box 30, Folder 10	1078	0	\N	1983-11-28	\N
101	0	11	inches	8	inches	\N	retained	original	\N	\N	Series 5 Subject Files, Box 30, Folder 10	1080	0	\N	1984-01-09	\N
102	0	11	inches	8	inches	\N	retained	original	\N	\N	Series 5 Subject Files, Box 30, Folder 10	1081	0	\N	1985-03-26	\N
103	0	11	inches	8	inches	\N	retained	original	\N	\N	Series 5 Subject Files, Box 30, Folder 10	1082	0	\N	1985-04-20	\N
105	0	8.5	inches	5.25	inches	\N	retained	original	\N	\N	Series 5: Box 30, Folder 10	1084	0	\N	1984-02-00	\N
106	0	8	inches	5	inches	\N	retained	original	\N	2 of 3, page 4	Box 30, Folder 10, Series 5 Subject Files	1085	0	\N	1984-02-00	\N
107	0	8	inches	5	inches	\N	retained	original	\N	3 of 3, page 6	Box 30, Folder 10, Series 5 Subject Files	1086	0	\N	1984-02-00	\N
108	5	0	inches	0	inches	\N	retained	\N	\N	\N	SERIES 8 PERSONAL EFFECTS AND MEMORABILIA box 180 folder 21	1089	0	\N	1959-00-00	\N
109	5	0	inches	0	inches	\N	retained	\N	\N	\N	SERIES 8 PERSONAL EFFECTS AND MEMORABILIA box 180 folder 10	1090	0	\N	1959-12-04	\N
110	5	0	inches	0	inches	\N	retained	\N	\N	\N	\N	1095	0	\N	\N	\N
111	6	0	inches	0	inches	\N	retained	\N	\N	1371, 1100	SERIES 7 PHOTOGRAPHS, ca. 1910-1995	1099	0	\N	1960-00-00	\N
112	6	0	inches	0	inches	\N	retained	\N	\N	1371, 1099	SERIES 7 PHOTOGRAPHS, ca. 1910-1995 box 176 folder 40.	1100	0	\N	1960-00-00	\N
113	6	0	inches	0	inches	\N	retained	\N	\N	\N	SERIES 7 PHOTOGRAPHS, ca. 1910-1995 box 177 item 48	1101	0	\N	1946-00-00	\N
114	5	0	inches	0	inches	\N	retained	\N	\N	2 images, one in color	SERIES 7 PHOTOGRAPHS, ca. 1910-1995 box 178 folder 42.	1102	0	\N	1980-00-00	\N
115	5	0	inches	0	inches	\N	retained	\N	\N	\N	Hughes, Ted Literary Broadside Folder	1103	0	\N	1970-00-00	\N
116	5	0	inches	0	inches	\N	retained	\N	\N	From the series "Four Crow Poems"	Hughes, Ted Literary Broadside Folder	1104	0	\N	1978-00-00	\N
117	5	0	inches	0	inches	\N	retained	\N	\N	From the series "Four Crow Poems"	Hughes, Ted Literary Broadside Folder	1105	0	\N	1970-00-00	\N
118	5	0	inches	0	inches	\N	retained	\N	\N	\N	Folio AP2 H32 v. 33 [pt. 3] July-Sept 1889	1106	0	\N	1889-08-03	\N
119	5	0	inches	0	inches	\N	retained	\N	\N	From the series "Four Crow Poems"	Hughes, Ted Literary Broadside Folder	1107	0	\N	1979-00-00	\N
120	5	0	inches	0	inches	\N	retained	\N	\N	From the series "Four Crow Poems."	Hughes, Ted Literary Broadside Folder	1108	0	\N	1970-00-00	\N
121	5	0	inches	0	inches	\N	retained	\N	\N	\N	Hughes, Ted Literary Broadside Folder	1109	0	\N	1979-10-28	\N
124	0	8.75	inches	6	inches	\N	retained	original	\N	1114, 1115	Series 5: Box 30, Folder 16	1113	0	\N	1978-05-07	\N
125	0	8.5	inches	11.75	inches	\N	retained	original	\N	1113, 1115	Series 5: Box 30, Folder 16	1114	0	\N	1978-05-07	1978-05-07
126	0	8.5	inches	11.75	inches	\N	retained	original	\N	1113, 1114	Series 5: Box 30, Folder 16	1115	0	\N	1978-05-07	1978-05-07
129	0	11	inches	8	inches	\N	retained	original	\N	\N	Series 5 Subject Files, Box 30, Folder 16	1118	0	\N	1978-05-07	\N
130	0	11	inches	8	inches	\N	retained	original	\N	\N	Series 5: Box 30, Folder 16	1119	0	\N	1978-00-00	\N
131	0	10.5	inches	4.25	inches	\N	retained	original	\N	1121, 1122, 1123, 1124, 1125, 1126	Series 5: Box 30, Folder 17	1120	0	\N	1984-11-20	\N
132	0	10.5	inches	8.5	inches	\N	retained	original	\N	1120, 1122, 1123, 1124, 1125, 1126	Series 5: Box 30, Folder 17	1121	0	\N	1984-11-20	\N
133	0	10.5	inches	8.5	inches	\N	retained	original	\N	1120, 1121, 1123, 1124, 1125, 1126	Series 5: Box 30, Folder 17	1122	0	\N	1984-11-20	1984-11-20
134	0	10.5	inches	8.5	inches	\N	retained	original	\N	1120, 1121, 1122, 1124, 1125, 1126	Series 5: Box 30, Folder 17	1123	0	\N	1984-11-20	1984-11-20
135	0	10.5	inches	8.5	inches	\N	retained	original	\N	1120, 1121, 1122, 1123, 1125, 1126	Series 5: Box 30, Folder 17	1124	0	\N	1984-11-20	1984-11-20
136	0	10.5	inches	8.5	inches	\N	retained	original	\N	1120, 1121, 1122, 1123, 1124, 1126	Series 5: Box 30, Folder 17	1125	0	\N	1984-11-20	\N
137	0	10.5	inches	4.25	inches	\N	retained	original	\N	1120, 1121, 1122, 1123, 1124, 1125	Series 5: Box 30, Folder 17	1126	0	\N	1984-11-20	1984-11-20
138	0	11	inches	8	inches	\N	retained	original	\N	\N	Series 5 Subject Files, Box 30, Folder 17	1127	0	\N	1984-00-00	\N
139	0	11	inches	8	inches	\N	retained	original	\N	\N	Series 5 Subject Files, Box 30, Folder 17	1128	0	\N	1984-04-12	\N
140	0	11	inches	8	inches	\N	retained	original	\N	\N	Series 5 Subject Files, Box 31, Folder 2	1129	0	\N	1981-00-00	\N
141	0	11	inches	8	inches	\N	retained	original	\N	\N	Series 5 Subject Files, Box 31, Folder 3	1130	0	\N	1985-01-16	\N
142	0	11	inches	8	inches	\N	retained	original	\N	1132	Series 5: Box 31, Folder 3	1131	0	\N	1985-01-14	\N
143	0	11	inches	8	inches	\N	retained	original	\N	1131	Series 5: Box 31, Folder 3	1132	0	\N	1985-01-14	\N
144	0	9	inches	6	inches	\N	retained	original	\N	1134	Series 5: Box 31, Folder 4	1133	0	\N	1961-01-16	\N
145	0	9	inches	6	inches	\N	retained	original	\N	2 of 2, page 2	Box 31, Folder 4, Series 5 Subject Files	1134	0	\N	1961-01-16	1961-01-16
146	0	11	inches	8	inches	\N	retained	original	\N	\N	Series 5 Subject Files, Box 31, Folder 4	1135	0	\N	1960-00-00	\N
147	0	11	inches	8	inches	\N	retained	original	\N	1137	Series 5 Subject Files, Box 31, Folder 5	1136	0	\N	1960-05-07	\N
148	0	11	inches	8	inches	\N	retained	original	\N	1136	Series 5 Subject Files, Box 31, Folder 5	1137	0	\N	1960-05-14	\N
152	0	11	inches	8	inches	\N	retained	original	\N	\N	Series 5 Subject Files, Box 31, Folder 5	1141	0	\N	1960-06-20	\N
153	0	11	inches	8	inches	\N	retained	original	\N	\N	Box 31, Folder 5, Series 5 Subject Files	1142	0	\N	1960-06-27	\N
154	0	11	inches	8	inches	\N	retained	original	\N	\N	Box 31, Folder 5, Series 5 Subject Files	1143	0	\N	1960-07-18	\N
155	6	8	inches	10	inches	\N	retained	original	\N	see box 3 for other materials from Tilly's involment with Truman's Committee on Civil Rights.	box 2 folder 6	1150	0	\N	1946-00-00	\N
156	5	0	inches	0	inches	\N	retained	\N	\N	\N	\N	1153	0	\N	\N	\N
157	5	0	inches	0	inches	\N	retained	\N	\N	\N	\N	1152	0	\N	\N	\N
158	5	0	inches	0	inches	\N	retained	\N	\N	\N	\N	1154	0	\N	\N	\N
159	5	0	inches	0	inches	\N	retained	\N	\N	\N	\N	1155	0	\N	\N	\N
160	5	0	inches	0	inches	\N	retained	\N	\N	\N	\N	1156	0	\N	\N	\N
161	6	0	inches	0	inches	\N	retained	\N	\N	\N	\N	1157	0	\N	\N	\N
162	5	0	inches	0	inches	\N	retained	\N	\N	\N	\N	1158	0	\N	\N	\N
163	5	0	inches	0	inches	\N	retained	\N	\N	\N	\N	1159	0	\N	\N	\N
164	5	0	inches	0	inches	\N	retained	\N	\N	\N	Hughes, Ted Hughes Literary Broadside Folder	1160	0	\N	1967-00-00	\N
165	0	4.25	inches	8.5	inches	\N	retained	original	\N	1165	Series 5: Box 31, Folder 7	1164	0	\N	1983-02-00	\N
166	0	4.25	inches	8.5	inches	\N	retained	original	\N	1164	Series 5: Box 31, Folder 7	1165	0	\N	1985-02-00	\N
167	0	11	inches	8	inches	\N	retained	original	\N	\N	Series 5 Subject Files, Box 31, Folder 7	1166	0	\N	1983-03-02	\N
168	0	3.75	inches	8.25	inches	\N	retained	original	\N	1168	Series 5: Box 31, Folder 11	1167	0	\N	1984-02-02	\N
169	0	3.75	inches	8.25	inches	\N	retained	original	\N	1167	Series 5: Box 31, Folder 11	1168	0	\N	1985-02-02	\N
170	0	11	inches	8	inches	\N	retained	original	\N	\N	Series 5 Subject Files, Box 31, Folder 11	1169	0	\N	1983-10-26	\N
178	0	11	inches	8	inches	\N	retained	original	\N	1175	Series 5 Subject Files, Box 31, Folder 12	1177	0	\N	1946-02-21	\N
179	0	11	inches	8	inches	\N	retained	original	\N	\N	Series 5 Subject Files, Box 31, Folder 12	1178	0	\N	1946-02-25	\N
190	0	11	inches	8	inches	\N	retained	original	\N	1188	Series 5 Subject Files, Box 31, Folder 14	1189	0	\N	1983-11-01	\N
191	0	11	inches	8	inches	\N	retained	original	\N	\N	Series 5 Subject Files, Box 31, Folder 14	1190	0	\N	1983-11-12	\N
192	0	11	inches	8	inches	\N	retained	original	\N	\N	Series 5 Subject Files, Box 31, Folder 14	1191	0	\N	1984-02-09	\N
193	0	11	inches	8	inches	\N	retained	original	\N	\N	Series 5 Subject Files, Box 31, Folder 14	1192	0	\N	1984-03-06	\N
171	0	8	inches	11	inches	\N	retained	original	\N	1171, 1172, 1173, 1174, 1175	Series 5 Subject Files: Box 31, Folder 12	1170	0	\N	1944-02-20	\N
212	0	11	inches	8	inches	\N	retained	original	\N	9 of 16	Box 32, Folder 4, Series 5 Subject Files	1211	0	\N	1937-00-00	\N
213	0	11	inches	8	inches	\N	retained	original	\N	10 of 16	Box 32, Folder 4, Series 5 Subject Files	1212	0	\N	1937-00-00	\N
214	0	11	inches	8	inches	\N	retained	original	\N	11 of 16	Box 32, Folder 4, Series 5 Subject Files	1213	0	\N	1937-00-00	\N
215	0	11	inches	8	inches	\N	retained	original	\N	12 of 16	Box 32, Folder 4, Series 5 Subject Files	1214	0	\N	1937-00-00	\N
216	0	11	inches	8	inches	\N	retained	original	\N	13 of 16	Box 32, Folder 4, Series 5 Subject Files	1215	0	\N	1937-00-00	\N
217	0	11	inches	8	inches	\N	retained	original	\N	14 of 16	Box 32, Folder 4, Series 5 Subject Files	1216	0	\N	1937-00-00	\N
218	0	11	inches	8	inches	\N	retained	original	\N	15 of 16	Box 32, Folder 4, Series 5 Subject Files	1217	0	\N	1937-00-00	\N
219	0	11	inches	8	inches	\N	retained	original	\N	16 of 16	Box 32, Folder 4, Series 5 Subject Files	1218	0	\N	1937-00-00	\N
220	5	0	inches	0	inches	\N	retained	\N	\N	\N	Hughes, Ted Literary Broadside Folder	1219	0	\N	1966-00-00	\N
221	5	0	inches	0	inches	\N	retained	\N	\N	From the series "Gravestones."	Hughes, Ted Literary Broadside Folder	1220	0	\N	1967-00-00	\N
222	0	0	inches	0	inches	\N	retained	\N	\N	See also Subseries 2.2: Wodwo, "Pibroch"	60 15	\N	0	\N	\N	\N
223	5	0	inches	0	inches	\N	retained	\N	\N	From the series "Gravestones."	Hughes, Ted Literary Broadside Folder	1221	0	\N	1967-00-00	\N
224	0	0	inches	0	inches	\N	retained	\N	\N	See also Subseries 2.3: Crow poems, "Bedtime Story VI," MS and TS	\N	\N	0	\N	\N	\N
225	5	0	inches	0	inches	\N	retained	\N	\N	From the series "Gravestones."	Hughes, Ted Literary Broadside Folder	1222	0	\N	1967-00-00	\N
226	5	0	inches	0	inches	\N	retained	\N	\N	From the series "Gravestones."	Hughes, Ted Literary Broadside Folder	1223	0	\N	1967-00-00	\N
227	5	0	inches	0	inches	\N	retained	\N	\N	\N	Hughes, Ted Literary Broadside Folder	1224	0	\N	1977-00-00	\N
228	6	0	inches	0	inches	\N	retained	\N	\N	See box 177 folders 64 to 72 and box 178 1-10 for other photos from the same time period.	SERIES 7 PHOTOGRAPHS, ca. 1910-1995 box 178 folder 10	1225	0	\N	1986-10-09	\N
229	5	0	inches	0	inches	\N	retained	\N	\N	\N	SERIES 7 PHOTOGRAPHS, ca. 1910-1995 box 178 folder 10	1225	0	\N	1986-10-09	\N
230	5	0	inches	0	inches	\N	retained	\N	\N	See also Subseries 2.2: Wolfwatching, "On the Reservation, MS"; Subseries 2.4c: Selected Poems by Keith Douglas; and Subseries 2.6: Tales of the Early World, "The Guardian"	Subseries 2.2 Collected poems, 1957-1995 box 78 folder 7	1227	0	\N	1992-00-00	\N
231	5	0	inches	0	inches	\N	retained	\N	\N	see box 62 folders 32a - 56	Subseries 2.2 Collected poems, 1957-1995 box 62 folder 38.	1228	0	\N	1973-00-00	\N
232	5	0	inches	0	inches	\N	retained	\N	\N	\N	Subseries 2.1 Notebooks, ca. 1949-ca. 1995 box 58 folder 6	1229	0	\N	0000-00-00	\N
233	5	0	inches	0	inches	\N	retained	\N	\N	See also Subseries 2.5: The Dogs, MS for prints of Art Kane photoessay contained in this scrapbook	Subseries 6.4 Scrapbooks, 1956-1968 OP 104	1230	0	\N	1963-02-17	\N
234	5	0	inches	0	inches	\N	retained	\N	\N	see box 62 folders 32a - 56	Subseries 2.2 Collected poems, 1957-1995 box 62 folder 47	1231	0	\N	1973-00-00	\N
235	5	0	inches	0	inches	\N	retained	\N	\N	see box 62 folders 32a - 56	Subseries 2.2 Collected poems, 1957-1995 box 62 folder 41	1232	0	\N	1973-00-00	\N
236	5	0	inches	0	inches	\N	retained	\N	\N	see box 62 folders 32a - 56	Subseries 2.2 Collected poems, 1957-1995 box 62 folder 51	1233	0	\N	1973-00-00	\N
237	5	0	inches	0	inches	\N	retained	\N	\N	see box 62 folders 32a - 56	Subseries 2.2 Collected poems, 1957-1995 box 62 folder 47	1235	0	\N	1973-00-00	\N
238	5	0	inches	0	inches	\N	retained	\N	\N	see box 62 folders 32a - 56	Subseries 2.2 Collected poems, 1957-1995 box 62 folder 45	1237	0	\N	1973-00-00	\N
239	5	0	inches	0	inches	\N	retained	\N	\N	see box 62 folders 32a - 56	Subseries 2.2 Collected poems, 1957-1995 box 62 folder 45	1242	0	\N	1973-00-00	\N
240	5	0	inches	0	inches	\N	retained	\N	\N	1244	SERIES 1 CORRESPONDENCE, 1959-1997 box 8 folder 2	1243	0	\N	1960-05-10	\N
241	5	0	inches	0	inches	\N	retained	\N	\N	1243	SERIES 1 CORRESPONDENCE, 1959-1997 box 8 folder 2	1244	0	\N	1960-05-10	\N
242	5	0	inches	0	inches	\N	retained	\N	\N	boxes 135-137.	Subseries 2.7 Translations, ca. 1968-1999 box 137 folder 4	1245	0	\N	1997-00-00	\N
243	5	0	inches	0	inches	\N	retained	\N	\N	see box 177 folders 1-47 for other portraits of Hughes.	SERIES 7 PHOTOGRAPHS, ca. 1910-1995 box 177 folder 7	1246	0	\N	1960-07-25	\N
244	5	0	inches	0	inches	\N	retained	\N	\N	1388	SERIES 7 PHOTOGRAPHS, ca. 1910-1995 box 177 folder 1	1247	0	\N	1940-00-00	\N
245	6	0	inches	0	inches	\N	retained	\N	\N	This black and white image is housed with its color counterpart.	SERIES 7 PHOTOGRAPHS, ca. 1910-1995 box 177 folder 34	1098	0	\N	1980-00-00	\N
246	5	0	inches	0	inches	\N	retained	\N	\N	\N	Washington Street Block - Washington, Fair, Crew, and Trinity Streets box 11 folder 12	1248	0	\N	1909-08-04	\N
247	6	0	inches	0	inches	\N	retained	\N	\N	one 8x10 image and one contact sheet with six images	SERIES 7 PHOTOGRAPHS, ca. 1910-1995 box 178 folder 38	1087	0	\N	1980-00-00	\N
248	6	0	inches	0	inches	\N	retained	\N	\N	See box 177 folders 64 to 72 and box 178 1-10 for other photos from the same time period.	SERIES 7 PHOTOGRAPHS, ca. 1910-1995 box 177 folder 68	1088	0	\N	1970-00-00	\N
249	6	0	inches	0	inches	\N	retained	\N	\N	5 photos on ship (1029, 1030)	SERIES 7 PHOTOGRAPHS, ca. 1910-1995 box 177 folder 57	1031	0	\N	1959-00-00	\N
250	6	0	inches	0	inches	\N	retained	\N	\N	\N	SERIES 7 PHOTOGRAPHS, ca. 1910-1995 box 177 folder 50	1091	0	\N	1956-00-00	\N
251	6	0	inches	0	inches	\N	retained	\N	\N	\N	SERIES 7 PHOTOGRAPHS, ca. 1910-1995 box 177 folder 60	1092	0	\N	1961-00-00	\N
252	6	0	inches	0	inches	\N	retained	\N	\N	\N	SERIES 7 PHOTOGRAPHS, ca. 1910-1995 box 177 folder 50.	1093	0	\N	1956-00-00	\N
253	6	0	inches	0	inches	\N	retained	\N	\N	see box 177 folders 1-47 for other portraits of Hughes.	SERIES 7 PHOTOGRAPHS, ca. 1910-1995 box 177 folder12.	1094	0	\N	1960-00-00	\N
254	5	0	inches	0	inches	\N	retained	\N	\N	\N	SERIES 7 PHOTOGRAPHS, ca. 1910-1995 box 178 folder 59.	1096	0	\N	1993-00-00	\N
255	6	0	inches	0	inches	\N	retained	\N	\N	see box 177 folders 1-47 for other portraits of Hughes.	SERIES 7 PHOTOGRAPHS, ca. 1910-1995 box 177 folder 40.	1097	0	\N	1990-00-00	\N
256	6	0	inches	0	inches	\N	retained	\N	\N	see box 177 folders 1-47 for other portraits of Hughes.	SERIES 7 PHOTOGRAPHS, ca. 1910-1995 box 177 folder 25	1226	0	\N	1970-00-00	\N
257	5	0	inches	0	inches	\N	retained	\N	\N	see box 62 folders 32a - 56	Subseries 2.2 Collected poems, 1957-1995 box 62 folder 51	1234	0	\N	1973-00-00	\N
258	5	0	inches	0	inches	\N	retained	\N	\N	From the series "Gravestones."	Hughes, Ted Literary Broadside Folder	1160	0	\N	1967-00-00	\N
259	6	0	inches	0	inches	\N	retained	\N	\N	\N	SERIES 7 PHOTOGRAPHS, ca. 1910-1995 box 178 folder 15.	1264	0	\N	1960-04-21	\N
260	5	0	inches	0	inches	\N	retained	\N	\N	1269	Letters to Gerald Hughes box 2 folder 28.	1265	0	\N	1990-00-00	\N
261	5	0	inches	0	inches	\N	retained	\N	\N	\N	Letters to Gerald Hughes box 2 folder 14	1266	0	\N	1978-00-00	\N
262	5	0	inches	0	inches	\N	retained	\N	\N	See also the black and white version of this image. Record ID 1098.	SERIES 7 PHOTOGRAPHS, ca. 1910-1995 box 177 folder 34	1267	0	\N	1980-00-00	\N
263	6	0	inches	0	inches	\N	retained	\N	\N	See box 20 for other portraits and individual photographs of Sibley from 1918 through the 1990s.	SERIES 4 PHOTOGRAPHS, CA. 1900-1993 box 20 folder 2	1268	0	\N	1920-00-00	\N
264	5	0	inches	0	inches	\N	retained	\N	\N	1265	SERIES 7 PHOTOGRAPHS, ca. 1910-1995 box 177 folder 47.	1269	0	\N	1997-00-00	\N
265	5	0	inches	0	inches	\N	retained	\N	\N	for more fishing pictures see 177 folders 3 and 33.	Letters to Gerald Hughes box 2 folder 26.	1270	0	\N	1980-00-00	\N
266	5	0	inches	0	inches	\N	retained	\N	\N	1099, 1100	Letters to Gerald Hughes box 2 folder 11	1271	0	\N	1966-00-00	\N
267	6	0	inches	0	inches	\N	retained	\N	\N	See box 177 folders 64 to 72 and box 178 1-10 for other photos from the same time period.	SERIES 7 PHOTOGRAPHS, ca. 1910-1995 box 178 folder 4.	1272	0	\N	1977-00-00	\N
268	6	0	inches	0	inches	\N	retained	\N	\N	box 179 folder 24; box 179 folder 27	SERIES 7 PHOTOGRAPHS, ca. 1910-1995 box 178 folder 37	1273	0	\N	1980-00-00	\N
269	6	0	inches	0	inches	\N	retained	\N	\N	See box 177 folders 64 to 72 and box 178 1-10 for other photos from the same time period.	SERIES 7 PHOTOGRAPHS, ca. 1910-1995	1274	0	\N	1970-00-00	\N
270	6	0	inches	0	inches	\N	retained	\N	\N	\N	SERIES 7 PHOTOGRAPHS, ca. 1910-1995 box 177 folder 42	1275	0	\N	1990-00-00	\N
271	6	0	inches	0	inches	\N	retained	\N	\N	box 178 folder 34	SERIES 7 PHOTOGRAPHS, ca. 1910-1995 box 178 folder 22	1276	0	\N	1970-00-00	\N
272	0	0	inches	0	inches	\N	retained	\N	\N	\N	\N	1276	0	\N	1970-00-00	\N
282	0	11	inches	8	inches	\N	retained	original	\N	\N	Series Subject Files, Box 32, Folder 6	1286	0	\N	1953-11-27	\N
283	0	11	inches	8	inches	\N	retained	original	\N	\N	Series Subject Files, Box 32, Folder 6	1287	0	\N	1955-01-28	\N
284	0	11	inches	8	inches	\N	retained	original	\N	\N	Series Subject Files, Box 32, Folder 6	1288	0	\N	1955-02-08	\N
285	0	11	inches	8	inches	\N	retained	original	\N	\N	Series Subject Files, Box 32, Folder 6	1289	0	\N	1955-02-22	\N
301	0	5	inches	0	inches	\N	retained	original	\N	1293, 1294, 1295, 1296, 1297, 1298, 1299, 1300, 1301, 1302, 1303, 1304	Series 6, Box 41, Folder 1	1305	0	\N	1918-00-00	\N
302	0	6	inches	4	inches	\N	retained	original	\N	1307, 1308, 1309	Series 6, Box 41, Folder 12	1306	0	\N	1952-11-14	\N
303	0	6	inches	4	inches	\N	retained	original	\N	1306, 1308, 1309	Series 6, Box 41, Folder 12	1307	0	\N	1952-00-00	\N
304	0	6	inches	4	inches	\N	retained	original	\N	1306, 1307, 1309	Series 6, Box 41, Folder 12	1308	0	\N	1952-12-08	\N
305	0	6	inches	4	inches	\N	retained	original	\N	1306, 1307, 1308	Series 6, Box 41, Folder 12	1309	0	\N	1952-12-11	\N
306	0	6	inches	4	inches	\N	retained	original	\N	1311, 1312, 1313	Series 6, Box 41, Folder 13	1310	0	\N	1956-07-16	\N
307	0	6	inches	4	inches	\N	retained	original	\N	1310, 1312, 1313	Series 6, Box 41, Folder 13	1311	0	\N	1956-07-19	\N
308	0	6	inches	4	inches	\N	retained	original	\N	1310, 1311, 1313	Series 6, Box 41, Folder 13	1312	0	\N	1956-07-24	\N
309	0	6	inches	4	inches	\N	retained	original	\N	1310, 1311, 1312	Series 6, Box 41, Folder 13	1313	0	\N	1956-08-08	\N
310	6	0	inches	0	inches	\N	retained	\N	\N	box 177 folder 63;	SERIES 7 PHOTOGRAPHS, ca. 1910-1995 box 178 folder 60	1314	0	\N	1990-00-00	\N
311	6	0	inches	0	inches	\N	retained	\N	\N	box 1 folder 69;	Letters to Gerald Hughes box 1 folder 61	1315	0	\N	1950-00-00	\N
312	6	0	inches	0	inches	\N	retained	\N	\N	box 1 folder 61	Letters to Gerald Hughes box 1 folder 60	1316	0	\N	1950-00-00	\N
313	5	0	inches	0	inches	\N	retained	\N	RESTRICTED.	See image 1318 for a manuscript of the poem discussed in this letter.	Subseries 1.1 Alphabetical correspondence files, 1959-1996 Restricted Corresponse box 9 folder 17	1317	0	\N	1990-08-12	\N
314	5	0	inches	0	inches	\N	retained	\N	Restricted.	See item 1317 for a letter discussing the creation of this poem.	Subseries 1.1 Alphabetical correspondence files, 1959-1996 Restricted Corresponse box 9 folder 17	1318	0	\N	1990-08-12	\N
315	5	0	inches	0	inches	\N	retained	\N	RESTRICTED.	See image 1320 for a copy of the letter contained in this envelope.	Subseries 6.4 Scrapbooks, 1956-1968 OP103a	1319	0	\N	1958-10-30	\N
316	5	0	inches	0	inches	\N	retained	\N	RESTRICTED.	see image 1319 for a scan of the envelope in which this letter was delivered.	Subseries 6.4 Scrapbooks, 1956-1968 OP103a	1320	0	\N	1958-10-30	\N
317	5	0	inches	0	inches	\N	retained	\N	\N	Four other items in box 6 folder 5	Subseries 1.1 Alphabetical correspondence files, 1959-1996 box 6 folder 5	1321	0	\N	1984-12-22	\N
318	0	11	inches	8	inches	\N	retained	original	\N	1323, 1324, 1325, 1326, 1327, 1328, 1329, 1330, 1331, 1332, 1333, 1334, 1335, 1336, 1337, 1338, 1339, 1340, 1341, 1342	Series 7, Box 42, Folder 2	1322	0	\N	1981-00-00	\N
319	0	11	inches	8	inches	\N	retained	original	\N	1322, 1324, 1325, 1326, 1327, 1328, 1329, 1330, 1331, 1332, 1333, 1334, 1335, 1336, 1337, 1338, 1339, 1340, 1341, 1342	Series 7, Box 42, Folder 2	1323	0	\N	1981-00-00	\N
320	0	11	inches	8	inches	\N	retained	original	\N	1322, 1323, 1325, 1326, 1327, 1328, 1329, 1330, 1331, 1332, 1333, 1334, 1335, 1336, 1337, 1338, 1339, 1340, 1341, 1342	Series 7, Box 42, Folder 2	1324	0	\N	1981-00-00	\N
321	0	11	inches	8	inches	\N	retained	original	\N	1322, 1323, 1324, 1326, 1327, 1328, 1329, 1330, 1331, 1332, 1333, 1334, 1335, 1336, 1337, 1338, 1339, 1340, 1341, 1342	Series 7, Box 42, Folder 2	1325	0	\N	1981-00-00	\N
322	0	11	inches	8	inches	\N	retained	original	\N	1322, 1323, 1324, 1325, 1327, 1328, 1329, 1330, 1331, 1332, 1333, 1334, 1335, 1336, 1337, 1338, 1339, 1340, 1341, 1342	Series 7, Box 42, Folder 2	1326	0	\N	1981-00-00	\N
323	0	11	inches	8	inches	\N	retained	original	\N	1322, 1323, 1324, 1325, 1326, 1328, 1329, 1330, 1331, 1332, 1333, 1334, 1335, 1336, 1337, 1338, 1339, 1340, 1341, 1342	Series 7, Box 42, Folder 2	1327	0	\N	1981-00-00	\N
324	0	11	inches	8	inches	\N	retained	original	\N	1322, 1323, 1324, 1325, 1326, 1327, 1329, 1330, 1331, 1332, 1333, 1334, 1335, 1336, 1337, 1338, 1339, 1340, 1341, 1342	Series 7, Box 42, Folder 2	1328	0	\N	1981-00-00	\N
325	0	11	inches	8	inches	\N	retained	original	\N	1322, 1323, 1324, 1325, 1326, 1327, 1328, 1330, 1331, 1332, 1333, 1334, 1335, 1336, 1337, 1338, 1339, 1340, 1341, 1342	Series 7, Box 42, Folder 2	1329	0	\N	1981-00-00	\N
326	0	11	inches	8	inches	\N	retained	original	\N	1322, 1323, 1324, 1325, 1326, 1327, 1328, 1329, 1331, 1332, 1333, 1334, 1335, 1336, 1337, 1338, 1339, 1340, 1341, 1342	Series 7, Box 42, Folder 2	1330	0	\N	1981-00-00	\N
327	0	11	inches	8	inches	\N	retained	original	\N	1322, 1323, 1324, 1325, 1326, 1327, 1328, 1329, 1330, 1332, 1333, 1334, 1335, 1336, 1337, 1338, 1339, 1340, 1341, 1342	Series 7, Box 42, Folder 2	1331	0	\N	1981-00-00	\N
328	0	11	inches	8	inches	\N	retained	original	\N	1322, 1323, 1324, 1325, 1326, 1327, 1328, 1329, 1330, 1331, 1333, 1334, 1335, 1336, 1337, 1338, 1339, 1340, 1341, 1342	Series 7, Box 42, Folder 2	1332	0	\N	1981-00-00	\N
329	0	11	inches	8	inches	\N	retained	original	\N	1322, 1323, 1324, 1325, 1326, 1327, 1328, 1329, 1330, 1331, 1332, 1334, 1335, 1336, 1337, 1338, 1339, 1340, 1341, 1342	Series 7, Box 42, Folder 2	1333	0	\N	1981-00-00	\N
330	0	11	inches	8	inches	\N	retained	original	\N	1322, 1323, 1324, 1325, 1326, 1327, 1328, 1329, 1330, 1331, 1332, 1333, 1335, 1336, 1337, 1338, 1339, 1340, 1341, 1342	Series 7, Box 42, Folder 2	1334	0	\N	1981-00-00	\N
331	0	11	inches	8	inches	\N	retained	original	\N	1322, 1323, 1324, 1325, 1326, 1327, 1328, 1329, 1330, 1331, 1332, 1333, 1334, 1336, 1337, 1338, 1339, 1340, 1341, 1342	Series 7, Box 42, Folder 2	1335	0	\N	1981-00-00	\N
332	0	11	inches	8	inches	\N	retained	original	\N	1322, 1323, 1324, 1325, 1326, 1327, 1328, 1329, 1330, 1331, 1332, 1333, 1334, 1335, 1337, 1338, 1339, 1340, 1341, 1342	Series 7, Box 42, Folder 2	1336	0	\N	1981-00-00	\N
333	0	11	inches	8	inches	\N	retained	original	\N	1322, 1323, 1324, 1325, 1326, 1327, 1328, 1329, 1330, 1331, 1332, 1333, 1334, 1335, 1336, 1338, 1339, 1340, 1341, 1342	Series 7, Box 42, Folder 2	1337	0	\N	1981-00-00	\N
334	0	11	inches	8	inches	\N	retained	original	\N	1322, 1323, 1324, 1325, 1326, 1327, 1328, 1329, 1330, 1331, 1332, 1333, 1334, 1335, 1336, 1337, 1339, 1340, 1341, 1342	Series 7, Box 42, Folder 2	1338	0	\N	1981-00-00	\N
335	0	11	inches	8	inches	\N	retained	original	\N	1322, 1323, 1324, 1325, 1326, 1327, 1328, 1329, 1330, 1331, 1332, 1333, 1334, 1335, 1336, 1337, 1338, 1340, 1341, 1342	Series 7, Box 42, Folder 2	1339	0	\N	1981-00-00	\N
336	0	11	inches	8	inches	\N	retained	original	\N	1322, 1323, 1324, 1325, 1326, 1327, 1328, 1329, 1330, 1331, 1332, 1333, 1334, 1335, 1336, 1337, 1338, 1339, 1341, 1342	Series 7, Box 42, Folder 2	1340	0	\N	1981-00-00	\N
337	0	11	inches	8	inches	\N	retained	original	\N	1322, 1323, 1324, 1325, 1326, 1327, 1328, 1329, 1330, 1331, 1332, 1333, 1334, 1335, 1336, 1337, 1338, 1339, 1340, 1342	Series 7, Box 42, Folder 2	1341	0	\N	1981-00-00	\N
338	0	11	inches	8	inches	\N	retained	original	\N	1322, 1323, 1324, 1325, 1326, 1327, 1328, 1329, 1330, 1331, 1332, 1333, 1334, 1335, 1336, 1337, 1338, 1339, 1340, 1341	Series 7, Box 42, Folder 2	1342	0	\N	1981-00-00	\N
339	0	11	inches	8	inches	\N	retained	original	\N	1344	Series 7, Box 42, Folder 2	1343	0	\N	1978-00-00	\N
340	0	11	inches	8	inches	\N	retained	original	\N	2 of 2	Box 42, Folder 2, Series 7 Other Personal and Family Papers, 1914-1990	1344	0	\N	1978-00-00	\N
342	0	7	inches	8	inches	\N	retained	original	\N	\N	Series 7, Box 42, Folder 10	1346	0	\N	1928-11-16	\N
343	0	7	inches	8	inches	\N	retained	original	\N	2 of 2	Box 42, Folder 10, Series 7 Other Personal and Family Papers, 1914-1990	1347	0	\N	1928-11-16	\N
349	5	0	inches	0	inches	\N	retained	\N	\N	1369	Letters to Frieda Hughes box 1 folder 64	1368	0	\N	1978-05-17	\N
350	5	0	inches	0	inches	\N	retained	\N	\N	1368.	Letters to Frieda Hughes box 1 folder 64	1369	0	\N	1978-05-17	\N
351	6	0	inches	0	inches	\N	retained	\N	\N	box 177 folders 7-12	SERIES 7 PHOTOGRAPHS, ca. 1910-1995 box 177 folder 11	1370	0	\N	1960-00-00	\N
352	6	0	inches	0	inches	\N	retained	\N	\N	1099, 1100	SERIES 7 PHOTOGRAPHS, ca. 1910-1995	1371	0	\N	1960-00-00	\N
353	6	0	inches	0	inches	\N	retained	\N	\N	1044	SERIES 7 PHOTOGRAPHS, ca. 1910-1995 box 177 folder 52	1373	0	\N	1958-00-00	\N
354	6	0	inches	0	inches	\N	retained	\N	\N	1375 Letters to Geral Hughes box 1 folder 70, box 2 folder 1 contain additional photographs from the USA trip. See also MSS 644 box 179 folder 7.	SERIES 7 PHOTOGRAPHS, ca. 1910-1995 box 177 folder 54	1374	0	\N	1959-07-00	\N
355	6	0	inches	0	inches	\N	retained	\N	\N	Letters to Gerald Hughes box 1 folder 70, box 2 folder 1 contain additional photographs from the USA trip. See also MSS 644 box 179 folder 7.	\N	1377	0	\N	1959-07-00	\N
341	0	4	inches	5	inches	\N	retained	original	\N	\N	Series 7: Box 42, Folder 4	1345	0	\N	1927-00-00	\N
356	6	0	inches	0	inches	\N	retained	\N	\N	Letters to Gerald Hughes box 1 folder 70, box 2 folder 1 contain additional photographs from the USA trip. See also MSS 644 box 179 folder 7.	Letters to Gerald Hughes box 2 folder 1	1378	0	\N	1959-07-00	\N
357	6	0	inches	0	inches	\N	retained	\N	\N	box 1 folder 70, box 2 folder 1 contain additional photographs from the USA trip. See also MSS 644 box 179 folder 7.	Letters to Gerald Hughes box 1 folder 70	1379	0	\N	1959-07-00	\N
358	6	0	inches	0	inches	\N	retained	\N	With COLOR BAR.	1045	SERIES 7 PHOTOGRAPHS, ca. 1910-1995 box 174 folder 14	1380	0	\N	1960-06-23	\N
359	6	0	inches	0	inches	\N	retained	\N	\N	see MSS 644 box 179 4-21 for other family pictures from this time period.	Letters to Gerald Hughes box 2 folder 7	1381	0	\N	1960-00-00	\N
360	6	0	inches	0	inches	\N	retained	\N	\N	see box 179 4-21 for other family pictures from this time period.	SERIES 7 PHOTOGRAPHS, ca. 1910-1995 box 177 folder 72	1382	0	\N	1973-00-00	\N
361	5	0	inches	0	inches	\N	retained	\N	\N	see box 179 4-21 for other family pictures from this time period.	Series 7 (Photographs), Box 179, folder 11	1383	0	\N	1962-04-00	\N
362	5	0	inches	0	inches	\N	retained	\N	\N	1395.	Subseries 2.5 Scripts and librettos box 130 folder 12	1384	0	\N	1995-00-00	\N
363	5	0	inches	0	inches	\N	retained	\N	\N	\N	AP4 .S22 1956	1385	0	\N	1956-00-00	\N
364	0	0	inches	0	inches	\N	retained	\N	\N	Ted Hughes papers box 139 folder 19.	\N	1386	0	\N	1958-00-00	\N
365	0	0	inches	0	inches	\N	retained	\N	\N	\N	\N	1386	0	\N	1958-00-00	\N
366	6	0	inches	0	inches	\N	retained	\N	\N	1381	Letters to Gerald Hughes box 2 folder 7	1387	0	\N	1961-00-00	\N
367	6	0	inches	0	inches	\N	retained	\N	\N	See box 178 folder 11 for others school age photographs.	SERIES 7 PHOTOGRAPHS, ca. 1910-1995 box 177 folder 1	1388	0	\N	1940-00-00	\N
368	6	0	inches	0	inches	\N	retained	\N	\N	\N	\N	1389	0	\N	\N	\N
369	6	0	inches	0	inches	\N	retained	\N	\N	box 1 folder 70, box 2 folder 1 contain additional photographs from the USA trip. See also MSS 644 box 179 folder 7.	Letters to Gerald Hughes box 2 folder 2	1390	0	\N	1959-07-00	\N
370	6	0	inches	0	inches	\N	retained	\N	\N	\N	SERIES 7 PHOTOGRAPHS, ca. 1910-1995 box 177 folder 4	1391	0	\N	1954-00-00	\N
371	6	0	inches	0	inches	\N	retained	\N	\N	Ted with sister Olwyn: Letters to Gerald Hughes box 1 folders 46 & 51; box 2 folder 61.	Letters to Gerald Hughes box 1 folder 51	1392	0	\N	1947-00-00	\N
372	5	0	inches	0	inches	\N	retained	\N	\N	\N	\N	1393	0	\N	\N	\N
373	5	0	inches	0	inches	\N	retained	\N	\N	Subseries 2.2 Collected poems, 1957-1995 box 59 folders 5-17.	Subseries 2.2 Collected poems, 1957-1995 box 59 folder 5	1394	0	\N	1960-00-00	\N
374	5	0	inches	0	inches	\N	retained	\N	\N	See also Subseries 2.2: Moortown, "A Knock at the Door"	Subseries 2.2 Collected poems, 1957-1995 box 59 folder 4.	1395	0	\N	1957-00-00	\N
375	6	0	inches	0	inches	\N	retained	\N	\N	Hughes and Baskin: box 178 folders 24, 31, 43, 49, 54, 55; box 179 folder 15.	SERIES 7 PHOTOGRAPHS, ca. 1910-1995 box 178 folder 31	1396	0	\N	1997-00-00	\N
376	6	0	inches	0	inches	\N	retained	\N	\N	box 60 folders 35-56, box 61 folders 1-48	Subseries 2.2 Collected poems, 1957-1995 box 61 folder 40	1397	0	\N	1970-00-00	\N
377	6	0	inches	0	inches	\N	retained	\N	\N	1397	Subseries 2.2 Collected poems, 1957-1995 box 61 folder 40	1398	0	\N	1970-00-00	\N
378	6	0	inches	0	inches	\N	retained	\N	\N	1400.	Bobby Jones collection box 3 folder 1	1399	0	\N	1904-07-00	\N
379	6	0	inches	0	inches	\N	retained	\N	\N	1399.	Bobby Jones collection box 3 folder 2	1400	0	\N	1908-00-00	\N
380	6	0	inches	0	inches	\N	retained	\N	\N	\N	Bobby Jones collection box 3 folder 3	1401	0	\N	1915-00-00	\N
381	6	0	inches	0	inches	\N	retained	\N	\N	\N	Bobby Jones collection box 3 folder 3	1402	0	\N	1916-00-00	\N
382	6	0	inches	0	inches	\N	retained	\N	\N	\N	Bobby Jones collection box 3 folder 5	1403	0	\N	1916-00-00	\N
383	6	0	inches	0	inches	\N	retained	\N	\N	\N	Bobby Jones collection box 3 folder 5	1404	0	\N	1918-07-04	\N
384	6	0	inches	0	inches	\N	retained	\N	\N	\N	Bobby Jones collection box 3 folder 7	1405	0	\N	1920-05-00	\N
385	5	0	inches	0	inches	\N	retained	\N	\N	\N	Bobby Jones collection box 3 folder 8	1406	0	\N	1920-00-00	\N
386	6	0	inches	0	inches	\N	retained	\N	\N	\N	Bobby Jones collection box 3 folder 9	1407	0	\N	\N	\N
387	6	0	inches	0	inches	\N	retained	\N	\N	\N	Bobby Jones collection box 3 folder 10	1408	0	\N	1920-00-00	\N
388	6	0	inches	0	inches	\N	retained	\N	\N	\N	Bobby Jones collection box 3 folder 11	1409	0	\N	1922-00-00	\N
389	6	0	inches	0	inches	\N	retained	\N	\N	\N	Bobby Jones collection box 3 folder 12	1410	0	\N	1922-00-00	\N
390	6	0	inches	0	inches	\N	retained	\N	\N	1412	Bobby Jones collection box 3 folder 13	1411	0	\N	1922-00-00	\N
391	6	0	inches	0	inches	\N	retained	\N	\N	1411.	Bobby Jones collection box 3 folder 14	1412	0	\N	1922-00-00	\N
392	6	0	inches	0	inches	\N	retained	\N	\N	1643.	Bobby Jones collection box 3 folder 15	1413	0	\N	1922-00-00	\N
393	6	0	inches	0	inches	\N	retained	\N	\N	1414-24.	Bobby Jones collection box 3 folder 16	1414	0	\N	1923-00-00	\N
394	6	0	inches	0	inches	\N	retained	\N	\N	1414-24.	Bobby Jones collection box 3 folder 16	1415	0	\N	1923-00-00	\N
395	6	0	inches	0	inches	\N	retained	\N	\N	1414-24.	Bobby Jones collection box 3 folder 17	1416	0	\N	1923-00-00	\N
396	6	0	inches	0	inches	\N	retained	\N	\N	1414-24.	Bobby Jones collection box 3 folder 17	1417	0	\N	1923-00-00	\N
397	6	0	inches	0	inches	\N	retained	\N	\N	1414-24.	Bobby Jones collection box 3 folder 18	1418	0	\N	1923-00-00	\N
398	0	0	inches	0	inches	\N	retained	\N	\N	1418.	\N	\N	0	\N	\N	\N
399	6	0	inches	0	inches	\N	retained	\N	\N	1414-24.	Bobby Jones collection box 3 folder 19	1419	0	\N	1923-00-00	\N
400	6	0	inches	0	inches	\N	retained	\N	\N	1414-24.	Bobby Jones collection box 3 folder 20	1420	0	\N	1923-00-00	\N
401	6	0	inches	0	inches	\N	retained	\N	\N	1414-24.	Bobby Jones collection box 3 folder 21	1421	0	\N	1923-00-00	\N
402	6	0	inches	0	inches	\N	retained	\N	\N	1414-24.	Bobby Jones collection box 3 folder 22	1422	0	\N	1923-00-00	\N
403	6	0	inches	0	inches	\N	retained	\N	\N	1414-24.	Bobby Jones collection box 3 folder 23	1423	0	\N	1923-07-16	\N
404	6	0	inches	0	inches	\N	retained	\N	\N	1414-24.	Bobby Jones collection box 3 folder 24	1424	0	\N	1923-00-00	\N
405	6	0	inches	0	inches	\N	retained	\N	\N	1426.	Bobby Jones collection box 3 folder 25	1425	0	\N	1923-00-00	\N
406	6	0	inches	0	inches	\N	retained	\N	\N	1425.	Bobby Jones collection box 3 folder 25	1426	0	\N	1923-00-00	\N
407	6	0	inches	0	inches	\N	retained	\N	\N	1427, 1463-4, 1466, 1497, 1527-8, 1605-10, 1617, 1628-35; 1646, 1687-8, 1688.	Bobby Jones collection box 3 folder 26	1427	0	\N	\N	\N
408	6	0	inches	0	inches	\N	retained	\N	\N	\N	Bobby Jones collection box 3 folder 27	1428	0	\N	1923-00-00	\N
409	6	0	inches	0	inches	\N	retained	\N	\N	\N	Bobby Jones collection box 3 folder 28	1429	0	\N	1924-00-00	\N
410	6	0	inches	0	inches	\N	retained	\N	\N	1430-32.	Bobby Jones collection box 3 folder 29.	1430	0	\N	1924-00-00	\N
411	6	0	inches	0	inches	\N	retained	\N	\N	1430-32.	Bobby Jones collection box 3 folder 30	1431	0	\N	1924-00-00	\N
412	6	0	inches	0	inches	\N	retained	\N	\N	1430-32.	Bobby Jones collection box 3 folder 31	1432	0	\N	1924-00-00	\N
413	6	0	inches	0	inches	\N	retained	\N	\N	\N	Bobby Jones collection box 3 folder 32	1433	0	\N	1924-00-00	\N
414	6	0	inches	0	inches	\N	retained	\N	\N	\N	Bobby Jones collection box 3 folder 33	1434	0	\N	1925-00-00	\N
415	6	0	inches	0	inches	\N	retained	\N	\N	\N	Bobby Jones collection box 3 folder 34	1435	0	\N	1925-00-00	\N
416	6	0	inches	0	inches	\N	retained	\N	\N	1437, 1438	Bobby Jones collection box 3 folder 35	1436	0	\N	1925-00-00	\N
417	6	0	inches	0	inches	\N	retained	\N	\N	1436, 1438	Bobby Jones collection box 3 folder 35	1437	0	\N	1925-00-00	\N
418	6	0	inches	0	inches	\N	retained	\N	\N	1436, 1437.	Bobby Jones collection box 3 folder 35	1438	0	\N	1925-00-00	\N
419	6	0	inches	0	inches	\N	retained	\N	\N	\N	Bobby Jones collection box 3 folder 36	1439	0	\N	1925-00-00	\N
420	6	0	inches	0	inches	\N	retained	\N	\N	1436-38.	Bobby Jones collection box 3 folder 37	1440	0	\N	1925-00-00	\N
421	6	0	inches	0	inches	\N	retained	\N	\N	\N	Bobby Jones collection box 3 folder 38	1441	0	\N	1926-00-00	\N
422	6	0	inches	0	inches	\N	retained	\N	\N	1443.	Bobby Jones collection box 3 folder 39	1442	0	\N	1926-00-00	\N
423	6	0	inches	0	inches	\N	retained	\N	\N	1442.	Bobby Jones collection box 3 folder 40	1443	0	\N	1926-00-00	\N
424	6	0	inches	0	inches	\N	retained	\N	\N	\N	Bobby Jones collection box 3 folder 41	1444	0	\N	1926-00-00	\N
425	6	0	inches	0	inches	\N	retained	\N	\N	1446.	Bobby Jones collection box 3 folder 42	1445	0	\N	1925-00-00	\N
426	6	0	inches	0	inches	\N	retained	\N	\N	1445	Bobby Jones collection box 3 folder 43	1446	0	\N	1926-00-00	\N
427	6	0	inches	0	inches	\N	retained	\N	\N	1475.	Bobby Jones collection box 3 folder 44	1447	0	\N	1926-00-00	\N
428	6	0	inches	0	inches	\N	retained	\N	\N	\N	Bobby Jones collection box 3 folder 45	1448	0	\N	1926-00-00	\N
429	6	0	inches	0	inches	\N	retained	\N	\N	\N	Bobby Jones collection box 3 folder 46	1449	0	\N	1926-00-00	\N
430	6	0	inches	0	inches	\N	retained	\N	\N	1450-55.	Bobby Jones collection box 3 folder 47	1450	0	\N	1926-00-00	\N
431	6	0	inches	0	inches	\N	retained	\N	\N	1450-55.	Bobby Jones collection box 3 folder 48	1451	0	\N	1926-00-00	\N
432	6	0	inches	0	inches	\N	retained	\N	\N	1450-55.	Bobby Jones collection box 3 folder 49	1452	0	\N	1926-00-00	\N
433	6	0	inches	0	inches	\N	retained	\N	\N	1450-55.	Bobby Jones collection box 3 folder 50	1453	0	\N	1926-00-00	\N
434	6	0	inches	0	inches	\N	retained	\N	\N	1450-55.	Bobby Jones collection box 3 folder 51	1454	0	\N	1926-00-00	\N
435	6	0	inches	0	inches	\N	retained	\N	\N	1450-55.	Bobby Jones collection box 3 folder 51	1455	0	\N	1926-00-00	\N
436	6	0	inches	0	inches	\N	retained	\N	\N	1456-59.	Bobby Jones collection box 3 folder 52	1456	0	\N	1926-00-00	\N
437	6	0	inches	0	inches	\N	retained	\N	\N	1456-59.	Bobby Jones collection box 3 folder 53	1457	0	\N	1926-00-00	\N
438	6	0	inches	0	inches	\N	retained	\N	\N	1456-59.	Bobby Jones collection box 3 folder 53	1458	0	\N	1926-00-00	\N
439	6	0	inches	0	inches	\N	retained	\N	\N	1456-59.	Bobby Jones collection box 3 folder 53	1459	0	\N	1926-00-00	\N
440	6	0	inches	0	inches	\N	retained	\N	\N	1460-62.	Bobby Jones collection box 3 folder 54	1460	0	\N	1926-00-00	\N
441	6	0	inches	0	inches	\N	retained	\N	\N	1460-62.	Bobby Jones collection box 3 folder 55	1461	0	\N	1926-00-00	\N
442	6	0	inches	0	inches	\N	retained	\N	\N	1460-62.	Bobby Jones collection box 3 folder 55	1462	0	\N	1926-00-00	\N
443	6	0	inches	0	inches	\N	retained	\N	\N	1427, 1463-4, 1466, 1497, 1527-8, 1605-10, 1617, 1628-35; 1646, 1687-8, 1688.	Bobby Jones collection box 3 folder 56	1463	0	\N	1926-00-00	\N
444	6	0	inches	0	inches	\N	retained	\N	\N	1427, 1463-4, 1466, 1497, 1527-8, 1605-10, 1617, 1628-35; 1646, 1687-8, 1688.	Bobby Jones collection box 3 folder 57	1464	0	\N	1926-00-00	\N
445	6	0	inches	0	inches	\N	retained	\N	\N	\N	Bobby Jones collection box 3 folder 58	1465	0	\N	\N	\N
446	6	0	inches	0	inches	\N	retained	\N	\N	1427, 1463-4, 1466, 1497, 1527-8, 1605-10, 1617, 1628-35; 1646, 1687-8, 1688.	Bobby Jones collection box 3 folder 59	1466	0	\N	\N	\N
447	6	0	inches	0	inches	\N	retained	\N	\N	1467-1479.	Bobby Jones collection box 4 folder 1	1467	0	\N	1927-08-24	\N
448	6	0	inches	0	inches	\N	retained	\N	\N	1467-1479.	Bobby Jones collection box 4 folder 2	1468	0	\N	1927-08-24	\N
449	6	0	inches	0	inches	\N	retained	\N	\N	1467-1479.	Bobby Jones collection box 4 folder 3	1469	0	\N	1927-08-25	\N
450	6	0	inches	0	inches	\N	retained	\N	\N	1467-1479.	Bobby Jones collection box 4 folder 4	1470	0	\N	1927-08-25	\N
451	6	0	inches	0	inches	\N	retained	\N	\N	1467-1479.	Bobby Jones collection box 4 folder 5	1471	0	\N	1927-08-27	\N
452	6	0	inches	0	inches	\N	retained	\N	\N	1467-1479.	Bobby Jones collection box 4 folder 6	1472	0	\N	1927-08-27	\N
453	6	0	inches	0	inches	\N	retained	\N	\N	1467-1479.	Bobby Jones collection box 4 folder 7	1473	0	\N	1927-08-27	\N
454	6	0	inches	0	inches	\N	retained	\N	\N	1467-1479.	Bobby Jones collection box 4 folder 8	1474	0	\N	1927-08-27	\N
455	6	0	inches	0	inches	\N	retained	\N	\N	1467-1479.	Bobby Jones collection box 4 folder 9	1475	0	\N	1927-08-27	\N
456	6	0	inches	0	inches	\N	retained	\N	\N	1467-1479.	Bobby Jones collection box 4 folder 10	1476	0	\N	1927-08-28	\N
457	6	0	inches	0	inches	\N	retained	\N	\N	1467-1479.	Bobby Jones collection box 4 folder 11	1477	0	\N	1927-08-00	\N
458	6	0	inches	0	inches	\N	retained	\N	\N	1467-1479.	Bobby Jones collection box 4 folder 12	1478	0	\N	1927-08-00	\N
459	6	0	inches	0	inches	\N	retained	\N	\N	1467-1479.	Bobby Jones collection box 4 folder 13	1479	0	\N	1927-08-00	\N
460	6	0	inches	0	inches	\N	retained	\N	\N	1481.	Bobby Jones collection box 4 folder 14	1480	0	\N	1927-12-00	\N
461	6	0	inches	0	inches	\N	retained	\N	\N	1480.	Bobby Jones collection box 4 folder 15	1481	0	\N	1927-12-00	\N
462	6	0	inches	0	inches	\N	retained	\N	\N	1482-94.	Bobby Jones collection box 4 folder 16	1482	0	\N	1929-06-28	\N
463	6	0	inches	0	inches	\N	retained	\N	\N	1482-94.	Bobby Jones collection box 4 folder 17	1483	0	\N	1929-06-27	\N
464	6	0	inches	0	inches	\N	retained	\N	\N	1482-94.	Bobby Jones collection box 4 folder 18	1484	0	\N	1929-06-29	\N
465	6	0	inches	0	inches	\N	retained	\N	\N	1482-94.	Bobby Jones collection box 4 folder 19	1485	0	\N	1929-06-29	\N
466	6	0	inches	0	inches	\N	retained	\N	\N	1482-94.	Bobby Jones collection box 4 folder 20	1486	0	\N	1929-06-29	\N
467	6	0	inches	0	inches	\N	retained	\N	\N	1482-94.	Bobby Jones collection box 4 folder 21	1487	0	\N	1926-06-00	\N
468	6	0	inches	0	inches	\N	retained	\N	\N	1482-94.	Bobby Jones collection box 4 folder 22	1488	0	\N	1929-06-29	\N
469	6	0	inches	0	inches	\N	retained	\N	\N	1482-94.	Bobby Jones collection box 4 folder 23	1489	0	\N	1929-06-30	\N
470	6	0	inches	0	inches	\N	retained	\N	\N	1482-94.	Bobby Jones collection box 4 folder 23	1490	0	\N	1929-06-30	\N
471	6	0	inches	0	inches	\N	retained	\N	\N	1482-94.	Bobby Jones collection box 4 folder 24	1491	0	\N	1929-06-30	\N
472	6	0	inches	0	inches	\N	retained	\N	\N	1482-94.	Bobby Jones collection box 4 folder 24	1492	0	\N	1929-00-00	\N
473	6	0	inches	0	inches	\N	retained	\N	\N	1482-94.	Bobby Jones collection box 4 folder 25	1493	0	\N	1929-00-00	\N
474	6	0	inches	0	inches	\N	retained	\N	\N	1482-94.	Bobby Jones collection box 4 folder 25a	1494	0	\N	1929-00-00	\N
475	5	0	inches	0	inches	\N	retained	\N	\N	1498-1510; 1526.	Bobby Jones collection box 4 folder 26	1495	0	\N	\N	\N
476	6	0	inches	0	inches	\N	retained	\N	\N	\N	Bobby Jones collection box 4 folder 27	1496	0	\N	\N	\N
477	6	0	inches	0	inches	\N	retained	\N	\N	1427, 1463-4, 1466, 1497, 1527-8, 1605-10, 1617, 1628-35; 1646, 1687-8, 1688.	Bobby Jones collection box 4 folder 28	1497	0	\N	\N	\N
478	6	0	inches	0	inches	\N	retained	\N	\N	1498-1510; 1526.	Bobby Jones collection box 4 folder 29	1498	0	\N	1930-06-05	\N
479	6	0	inches	0	inches	\N	retained	\N	\N	1498-1510; 1526.	Bobby Jones collection box 4 folder 29	1499	0	\N	1930-06-05	\N
480	6	0	inches	0	inches	\N	retained	\N	\N	1498-1510; 1526.	Bobby Jones collection box 4 folder 30	1500	0	\N	1930-07-05	\N
481	6	0	inches	0	inches	\N	retained	\N	\N	1498-1510; 1526.	Bobby Jones collection box 4 folder 30	1501	0	\N	1930-07-05	\N
482	6	0	inches	0	inches	\N	retained	\N	\N	1498-1510; 1526.	Bobby Jones collection box 4 folder 30	1502	0	\N	1930-07-05	\N
483	6	0	inches	0	inches	\N	retained	\N	\N	1498-1510; 1526.	Bobby Jones collection box 4 folder 30	1503	0	\N	1930-07-05	\N
484	6	0	inches	0	inches	\N	retained	\N	\N	1498-1510; 1526.	Bobby Jones collection box 4 folder 31	1504	0	\N	1930-07-05	\N
485	6	0	inches	0	inches	\N	retained	\N	\N	1498-1510; 1526.	Bobby Jones collection box 4 folder 32	1505	0	\N	1930-07-05	\N
486	6	0	inches	0	inches	\N	retained	\N	\N	1498-1510; 1526.	Bobby Jones collection box 4 folder 32	1506	0	\N	1930-07-05	\N
487	6	0	inches	0	inches	\N	retained	\N	\N	1498-1510; 1526.	Bobby Jones collection box 4 folder 33	1507	0	\N	1930-07-05	\N
488	6	0	inches	0	inches	\N	retained	\N	\N	1498-1510; 1526.	Bobby Jones collection box 4 folder 34	1508	0	\N	1930-07-05	\N
489	6	0	inches	0	inches	\N	retained	\N	\N	1498-1510; 1526.	Bobby Jones collection box 4 folder 35	1509	0	\N	1930-07-05	\N
490	6	0	inches	0	inches	\N	retained	\N	\N	1498-1510.	Bobby Jones collection box 4 folder 35	1510	0	\N	1930-07-05	\N
491	6	0	inches	0	inches	\N	retained	\N	\N	1511-17	Bobby Jones collection box 4 folder 38	1511	0	\N	1930-05-00	\N
492	6	0	inches	0	inches	\N	retained	\N	\N	1511-17	Bobby Jones collection box 4 folder 37	1512	0	\N	1930-05-30	\N
493	6	0	inches	0	inches	\N	retained	\N	\N	1511-17	Bobby Jones collection box 4 folder 38	1513	0	\N	1930-05-31	\N
494	6	0	inches	0	inches	\N	retained	\N	\N	1511-17	Bobby Jones collection box 4 folder 39	1514	0	\N	1930-05-31	\N
495	0	0	inches	0	inches	\N	retained	\N	\N	\N	4 40	\N	0	\N	\N	\N
496	6	0	inches	0	inches	\N	retained	\N	\N	1511-17	Bobby Jones collection box 4 folder 40	1515	0	\N	1930-05-31	\N
497	6	0	inches	0	inches	\N	retained	\N	\N	1511-17	Bobby Jones collection box 4 folder 41	1516	0	\N	1930-05-31	\N
498	6	0	inches	0	inches	\N	retained	\N	\N	1511-17	Bobby Jones collection box 4 folder 42	1517	0	\N	1930-05-31	\N
499	6	0	inches	0	inches	\N	retained	\N	\N	1518-23.	Bobby Jones collection box 4 folder 43	1518	0	\N	1930-06-18	\N
500	6	0	inches	0	inches	\N	retained	\N	\N	1518-23.	Bobby Jones collection box 4 folder 43	1519	0	\N	1930-06-18	\N
501	6	0	inches	0	inches	\N	retained	\N	\N	1518-23.	Bobby Jones collection box 4 folder 43	1520	0	\N	1930-06-20	\N
502	6	0	inches	0	inches	\N	retained	\N	\N	1518-23.	Bobby Jones collection box 4 folder 44	1521	0	\N	1930-06-18	\N
503	6	0	inches	0	inches	\N	retained	\N	\N	1518-23.	Bobby Jones collection box 4 folder 44	1522	0	\N	1930-06-18	\N
504	6	0	inches	0	inches	\N	retained	\N	\N	1518-23.	Bobby Jones collection box 4 folder 44	1523	0	\N	1920-06-20	\N
505	6	0	inches	0	inches	\N	retained	\N	\N	\N	Bobby Jones collection box 4 folder 46	1524	0	\N	1930-06-27	\N
506	6	0	inches	0	inches	\N	retained	\N	\N	1433, 1443	Bobby Jones collection box 4 folder 47	1525	0	\N	1930-06-00	\N
507	6	0	inches	0	inches	\N	retained	\N	\N	1498-1510; 1526.	Bobby Jones collection box 4 folder 48	1526	0	\N	\N	\N
508	6	0	inches	0	inches	\N	retained	\N	\N	1427, 1463-4, 1466, 1497, 1527-8, 1605-10, 1617, 1628-35; 1646, 1687-8, 1688.	Bobby Jones collection box 4 folder 49	1527	0	\N	\N	\N
509	0	0	inches	0	inches	\N	retained	\N	\N	1498-1510; 1526.	\N	1505	0	\N	\N	\N
510	0	0	inches	0	inches	\N	retained	\N	\N	1427, 1463-4, 1466, 1497, 1527-8, 1605-10, 1617, 1628-35; 1646, 1687-8, 1688.	Bobby Jones collection box 4 folder 50	1528	0	\N	\N	\N
511	6	0	inches	0	inches	\N	retained	\N	\N	1692-3	Bobby Jones collection box 4 folder 51	1529	0	\N	\N	\N
512	6	0	inches	0	inches	\N	retained	\N	\N	\N	Bobby Jones collection box 4 folder 52	1530	0	\N	1930-00-00	\N
513	6	0	inches	0	inches	\N	retained	\N	\N	1605-10; 1617	Bobby Jones collection box 4 folder 53	1531	0	\N	1930-00-00	\N
514	\N	10	inches	6	inches	\N	retained	original	The image is a reproduction of a photograph and caption.	\N	Box 60, Folder 4	1532	0	\N	1935-00-00	\N
515	\N	4	inches	9	inches	\N	retained	original	\N	\N	Box 60, folder7	1533	0	\N	1934-00-00	\N
516	\N	8	inches	10	inches	\N	retained	original	\N	\N	Box 60, Folder 8	1534	0	\N	1935-00-00	\N
517	\N	5	inches	7	inches	\N	retained	original	\N	\N	Box 60, Folder 9	1535	0	\N	1935-04-23	\N
518	\N	8	inches	10	inches	\N	retained	original	\N	\N	Box 60, Folder 10	1536	0	\N	1936-00-00	\N
519	\N	8	inches	10	inches	\N	retained	original	\N	\N	Box 60, Folder 12	1537	0	\N	1935-00-00	\N
520	\N	8	inches	10	inches	\N	retained	original	\N	\N	Box 60, Folder 15	1538	0	\N	1936-04-04	\N
521	\N	8	inches	10	inches	\N	retained	original	\N	1774	Box 60, Folder 18	1539	0	\N	1950-12-00	\N
522	\N	8	inches	10	inches	\N	retained	original	\N	\N	Box 60, Folder 26	1540	0	\N	1955-00-00	\N
523	\N	8	inches	10	inches	\N	retained	original	\N	1542	Box 60, Folder 20	1541	0	\N	1950-04-09	\N
524	\N	8	inches	10	inches	\N	retained	original	\N	1541	Box 60, Folder 20	1542	0	\N	1950-04-09	\N
525	\N	3	inches	6	inches	\N	retained	original	\N	1758, 1759, 1760	Box 60, Folder 39	1543	0	\N	0000-00-00	\N
526	\N	8	inches	10	inches	\N	retained	original	\N	\N	Box 60, Folder 25	1544	0	\N	1955-00-00	\N
527	\N	8	inches	5	inches	\N	retained	original	\N	\N	Box 52, Folder 45	1545	0	\N	1920-00-00	\N
528	\N	10	inches	7	inches	\N	retained	original	\N	\N	Box 53, Folder 7	1546	0	\N	0000-00-00	\N
529	\N	9	inches	7	inches	\N	retained	original	\N	\N	Box 53, Folder 24	1547	0	\N	1952-04-06	\N
530	\N	5	inches	3	inches	\N	retained	original	\N	\N	Box 51, Folder 1	1548	0	\N	1918-00-00	\N
531	\N	0	inches	0	inches	\N	retained	original	\N	\N	Box 51, Folder 2	1549	0	\N	1920-00-00	\N
532	\N	11	inches	6	inches	\N	retained	original	\N	\N	Box 51, Folder 5	1550	0	\N	1920-00-00	\N
533	\N	7	inches	5	inches	\N	retained	use copy	This print is a copy of an original image not held by Emory.	\N	Box 51, Folder 3	1551	0	\N	1920-00-00	\N
534	\N	10	inches	8	inches	\N	retained	original	\N	\N	Box 51, Folder 8	1552	0	\N	1926-00-00	\N
535	\N	4	inches	4	inches	\N	retained	original	\N	\N	Box 51, Folder 9	1553	0	\N	1931-00-00	\N
536	\N	9	inches	7	inches	\N	retained	original	\N	\N	Box 51, Folder 13	1554	0	\N	1934-11-21	\N
537	\N	10	inches	8	inches	\N	retained	original	\N	1664	Box 51, Folder 20	1555	0	\N	1936-00-00	\N
538	\N	10	inches	8	inches	\N	retained	original	\N	\N	Box 51, Folder 24	1556	0	\N	1945-00-00	\N
539	\N	10	inches	8	inches	\N	retained	original	\N	\N	Box 51, Folder 26	1557	0	\N	1945-00-00	\N
540	\N	4	inches	3	inches	\N	retained	original	\N	\N	Box 51, Folder 4	1558	0	\N	1920-00-00	\N
541	\N	10	inches	8	inches	\N	retained	original	\N	\N	Box 52, Folder 11	1559	0	\N	1950-00-00	\N
542	\N	8	inches	10	inches	\N	retained	original	\N	\N	Box 60, Folder 17	1560	0	\N	1939-04-01	\N
543	0	0	inches	0	inches	\N	retained	\N	\N	\N	\N	1561	0	\N	1931-00-00	\N
544	0	0	inches	0	inches	\N	retained	\N	\N	\N	\N	1562	0	\N	0000-02-08	\N
545	0	0	inches	0	inches	\N	retained	\N	\N	\N	\N	1563	0	\N	1932-12-27	\N
546	0	0	inches	0	inches	\N	retained	\N	\N	\N	\N	1564	0	\N	1934-11-20	\N
547	0	0	inches	0	inches	\N	retained	\N	\N	\N	\N	1565	0	\N	0000-00-00	\N
548	0	0	inches	0	inches	\N	retained	\N	\N	\N	\N	1566	0	\N	0000-00-00	\N
549	6	0	inches	0	inches	\N	retained	\N	\N	1567-70	Bobby Jones collection box 4 folder 54	1567	0	\N	\N	\N
550	6	0	inches	0	inches	\N	retained	\N	\N	1567-70	Bobby Jones collection box 4 folder 55	1568	0	\N	\N	\N
551	6	0	inches	0	inches	\N	retained	\N	\N	1567-70	Bobby Jones collection box 4 folder 56	1569	0	\N	\N	\N
552	6	0	inches	0	inches	\N	retained	\N	\N	1567-70	Bobby Jones collection box 4 folder 57	1570	0	\N	\N	\N
553	6	0	inches	0	inches	\N	retained	\N	\N	1605-10; 1617	Bobby Jones collection box 4 folder 57	1571	0	\N	\N	\N
554	6	0	inches	0	inches	\N	retained	\N	\N	1573	Bobby Jones collection box 4 folder 58	1572	0	\N	\N	\N
555	6	0	inches	0	inches	\N	retained	\N	\N	1572	Bobby Jones collection box 4 folder 59	1573	0	\N	\N	\N
556	6	0	inches	0	inches	\N	retained	\N	\N	\N	Bobby Jones collection box 5 folder 1	1574	0	\N	1926-00-00	\N
557	6	0	inches	0	inches	\N	retained	\N	\N	1576	Bobby Jones collection box 5 folder 2	1575	0	\N	\N	\N
558	6	0	inches	0	inches	\N	retained	\N	\N	1575.	Bobby Jones collection box 5 folder 2	1576	0	\N	1927-03-00	\N
559	6	0	inches	0	inches	\N	retained	\N	\N	\N	Bobby Jones collection box 5 folder 3	1577	0	\N	1930-08-21	\N
560	6	0	inches	0	inches	\N	retained	\N	\N	\N	Bobby Jones collection box 5 folder 4	1578	0	\N	1930-00-00	\N
561	6	0	inches	0	inches	\N	retained	\N	\N	\N	Bobby Jones collection box 5 folder 5	1579	0	\N	1930-05-00	\N
562	6	0	inches	0	inches	\N	retained	\N	\N	\N	Bobby Jones collection box 5 folder 6	1580	0	\N	1930-00-00	\N
563	6	0	inches	0	inches	\N	retained	\N	\N	\N	Bobby Jones collection box 5 folder 7	1581	0	\N	1930-00-00	\N
564	6	0	inches	0	inches	\N	retained	\N	\N	\N	Bobby Jones collection box 5 folder 8	1582	0	\N	\N	\N
565	6	0	inches	0	inches	\N	retained	\N	\N	\N	Bobby Jones collection box 5 folder 8	1583	0	\N	\N	\N
566	6	0	inches	0	inches	\N	retained	\N	\N	\N	Bobby Jones collection box 5 folder 8	1584	0	\N	\N	\N
567	6	0	inches	0	inches	\N	retained	\N	\N	\N	Bobby Jones collection box 5 folder 8	1585	0	\N	1923-00-00	\N
568	6	0	inches	0	inches	\N	retained	\N	\N	\N	Bobby Jones collection box 5 folder 8	1586	0	\N	\N	\N
569	6	0	inches	0	inches	\N	retained	\N	\N	\N	Bobby Jones collection box 5 folder 8	1587	0	\N	\N	\N
570	6	0	inches	0	inches	\N	retained	\N	\N	\N	Bobby Jones collection box 5 folder 8	1588	0	\N	\N	\N
571	6	0	inches	0	inches	\N	retained	\N	\N	\N	Bobby Jones collection box 5 folder 8	1589	0	\N	\N	\N
572	6	0	inches	0	inches	\N	retained	\N	\N	\N	Bobby Jones collection box 5 folder 8	1590	0	\N	\N	\N
573	0	0	inches	0	inches	\N	retained	\N	\N	\N	Bobby Jones collection box 5 folder 8	1591	0	\N	\N	\N
575	0	12	inches	7	inches	\N	retained	\N	\N	\N	Woodson PR4845 K54 .A37 1875	1593	0	\N	1875-00-00	\N
576	0	14	inches	27	inches	\N	retained	\N	\N	\N	Woodson DT 361 .B67 1869	1594	0	\N	1860-00-00	\N
577	0	6	inches	6	inches	\N	retained	\N	\N	\N	Woodson DT764 B2 J8 1938	1595	0	\N	1938-00-00	\N
578	0	10	inches	14	inches	\N	retained	\N	\N	\N	Woodson DT764 B2 J8 1938	1596	0	\N	1938-00-00	\N
579	0	12	inches	11	inches	\N	retained	\N	\N	\N	Woodson DT511 H41 1903	1597	0	\N	1903-00-00	\N
580	0	14	inches	10	inches	\N	retained	\N	\N	\N	Woodson DT 541 H4 v.2	1598	0	\N	1938-00-00	\N
581	0	14	inches	10	inches	\N	retained	\N	\N	\N	Woodson DT 541 H4 v.2	1599	0	\N	1938-00-00	\N
582	0	12	inches	7	inches	\N	retained	\N	\N	\N	Woodson DT471 B5 1905	1600	0	\N	1905-00-00	\N
584	0	12	inches	8	inches	\N	retained	\N	\N	\N	Woodson DT471 B5 1905	1601	0	\N	1905-00-00	\N
585	6	0	inches	0	inches	\N	retained	\N	\N	\N	Bobby Jones collection box 5 folder 8	1602	0	\N	\N	\N
586	6	0	inches	0	inches	\N	retained	\N	\N	\N	Bobby Jones collection box 5 folder 8	1603	0	\N	\N	\N
587	6	0	inches	0	inches	\N	retained	\N	\N	1498-1510; 1526.	Bobby Jones collection box 5 folder 9	1604	0	\N	1931-00-00	\N
588	6	0	inches	0	inches	\N	retained	\N	\N	1605-10; 1617	Bobby Jones collection box 5 folder 9	1605	0	\N	1931-00-00	\N
589	6	0	inches	0	inches	\N	retained	\N	\N	1605-10; 1617	Bobby Jones collection box 5 folder 10	1606	0	\N	1931-00-00	\N
590	6	0	inches	0	inches	\N	retained	\N	\N	1427, 1463-4, 1466, 1497, 1527-8, 1605-10, 1617, 1628-35; 1646, 1687-8, 1688.	Bobby Jones collection box 5 folder 10	1607	0	\N	1931-00-00	\N
591	6	0	inches	0	inches	\N	retained	\N	\N	1605-10; 1617	Bobby Jones collection box 5 folder 10	1608	0	\N	1931-00-00	\N
592	6	0	inches	0	inches	\N	retained	\N	\N	1605-10; 1617	Bobby Jones collection box 5 folder 10	1609	0	\N	1931-00-00	\N
593	6	0	inches	0	inches	\N	retained	\N	\N	1605-10; 1617	Bobby Jones collection box 5 folder 10	1610	0	\N	1931-00-00	\N
594	5	4	inches	3	inches	\N	retained	original	\N	\N	Photographs, box 2, folder 11	1611	25	\N	1966-00-00	\N
595	6	3	inches	3	inches	\N	retained	original	\N	1099, 1100, 1371, 1615, 1616	SERIES 7 PHOTOGRAPHS, ca. 1910-1995	1614	0	\N	1960-00-00	\N
596	6	3	inches	3	inches	\N	retained	original	\N	1099, 1100, 1371, 1614, 1616	SERIES 7 PHOTOGRAPHS, ca. 1910-1995	1615	0	\N	1960-00-00	\N
597	6	3	inches	3	inches	\N	retained	original	\N	1099, 1100, 1371, 1614, 1615	SERIES 7 PHOTOGRAPHS, ca. 1910-1995	1616	0	\N	1960-00-00	\N
598	6	0	inches	0	inches	\N	retained	\N	\N	1605-10; 1617	Bobby Jones collection box 5 folder 10	1617	0	\N	1931-00-00	\N
599	6	0	inches	0	inches	\N	retained	\N	\N	1619.	Bobby Jones collection box 5 folder 11	1618	0	\N	1931-00-00	\N
600	6	0	inches	0	inches	\N	retained	\N	\N	1618.	Bobby Jones collection box 5 folder 11	1619	0	\N	1931-00-00	\N
601	6	0	inches	0	inches	\N	retained	\N	\N	1620-23.	Bobby Jones collection box 5 folder 12	1620	0	\N	\N	\N
602	6	0	inches	0	inches	\N	retained	\N	\N	1620-23.	Bobby Jones collection box 5 folder 12	1621	0	\N	\N	\N
603	0	0	inches	0	inches	\N	retained	\N	\N	1620-23.	\N	\N	0	\N	\N	\N
604	6	0	inches	0	inches	\N	retained	\N	\N	1620-23.	Bobby Jones collection box 5 folder 12	1622	0	\N	1944-07-00	\N
605	6	0	inches	0	inches	\N	retained	\N	\N	1620-23.	Bobby Jones collection box 5 folder 12	1623	0	\N	1944-07-00	\N
606	6	0	inches	0	inches	\N	retained	\N	\N	1624-27.	Bobby Jones collection box 5 folder 13	1624	0	\N	\N	\N
607	6	0	inches	0	inches	\N	retained	\N	\N	1624-27.	Bobby Jones collection box 5 folder 13	1625	0	\N	\N	\N
608	6	0	inches	0	inches	\N	retained	\N	\N	1624-27.	Bobby Jones collection box 5 folder 13	1626	0	\N	1952-09-02	\N
609	6	0	inches	0	inches	\N	retained	\N	\N	1624-27.	Bobby Jones collection box 5 folder 13	1627	0	\N	\N	\N
610	6	0	inches	0	inches	\N	retained	\N	\N	1628-35.	Bobby Jones collection box 5 folder 14	1628	0	\N	1955-00-00	\N
611	6	0	inches	0	inches	\N	retained	\N	\N	1628-35.	Bobby Jones collection box 5 folder 14	1629	0	\N	1955-00-00	\N
612	6	0	inches	0	inches	\N	retained	\N	\N	1628-35.	Bobby Jones collection box 5 folder 14	1630	0	\N	1955-00-00	\N
613	6	0	inches	0	inches	\N	retained	\N	\N	1628-35.	Bobby Jones collection box 5 folder 14	1631	0	\N	1955-00-00	\N
614	6	0	inches	0	inches	\N	retained	\N	\N	1427, 1463-4, 1466, 1497, 1527-8, 1605-10, 1617, 1628-35; 1646, 1687-8, 1688.	Bobby Jones collection box 5 folder 14	1632	0	\N	\N	\N
615	6	0	inches	0	inches	\N	retained	\N	\N	1628-35.	Bobby Jones collection box 5 folder 14	1633	0	\N	\N	\N
616	6	0	inches	0	inches	\N	retained	\N	\N	1628-35.	Bobby Jones collection box 5 folder 14	1634	0	\N	\N	\N
617	6	0	inches	0	inches	\N	retained	\N	\N	1628-35.	Bobby Jones collection box 5 folder 14	1635	0	\N	\N	\N
618	6	0	inches	0	inches	\N	retained	\N	\N	\N	Bobby Jones collection box 5 folder 15	1636	0	\N	1958-00-00	\N
619	6	0	inches	0	inches	\N	retained	\N	\N	\N	Bobby Jones collection box 5 folder 16	1637	0	\N	1958-00-00	\N
620	6	0	inches	0	inches	\N	retained	\N	\N	\N	Bobby Jones collection box 5 folder 17	1638	0	\N	1959-00-00	\N
621	6	0	inches	0	inches	\N	retained	\N	\N	\N	Bobby Jones collection box 5 folder 18	1639	0	\N	1959-00-00	\N
622	6	0	inches	0	inches	\N	retained	\N	\N	See also Robert W. Woodruff papers, box 41:11 “John M. Budinger correspondence” for more information on Eisenhower portrait.	Bobby Jones collection box 5 folder 19	1640	0	\N	\N	\N
623	6	0	inches	0	inches	\N	retained	\N	\N	\N	Bobby Jones collection box 5 folder 20	1641	0	\N	1960-00-00	\N
624	6	0	inches	0	inches	\N	retained	\N	\N	\N	Bobby Jones collection box 5 folder 21	1642	0	\N	1964-00-00	\N
625	5	0	inches	0	inches	\N	retained	\N	\N	1413	Bobby Jones collection box 5 folder 22	1643	0	\N	1966-05-00	\N
626	5	0	inches	0	inches	\N	retained	\N	\N	\N	Bobby Jones collection box 5 folder 23	1644	0	\N	1972-05-00	\N
627	6	0	inches	0	inches	\N	retained	\N	\N	\N	Bobby Jones collection box 5 folder 24	1645	0	\N	\N	\N
628	6	0	inches	0	inches	\N	retained	\N	\N	1427, 1463-4, 1466, 1497, 1527-8, 1605-10, 1617, 1628-35; 1646, 1687-8, 1688.	Bobby Jones collection box 5 folder 25	1646	0	\N	1930-00-00	\N
629	0	11	inches	8	inches	\N	retained	original	\N	\N	Box 68, Folder 10	1647	0	\N	1946-08-00	\N
630	0	9	inches	6	inches	\N	retained	original	\N	\N	Box 100, Folder 54	1648	0	\N	1939-04-01	\N
631	\N	9	inches	7	inches	\N	retained	original	\N	\N	Box 60, Folder 46	1649	0	\N	1933-00-00	\N
632	\N	8	inches	9	inches	\N	retained	original	Original has a tear on the left hand side.  The tape visible on the corners in the image was removed by Preservation after the digital image was created.	\N	Box 60, Folder 46	1650	0	\N	0000-00-00	\N
633	0	2	inches	2	inches	\N	retained	original	\N	\N	Box 42, Folder 13	1651	0	\N	1944-08-13	\N
634	0	9	inches	3	inches	\N	retained	original	\N	\N	Box 107, Folder 22	1652	0	\N	1942-11-16	\N
635	\N	4	inches	6	inches	\N	retained	original	\N	\N	Box 51, Folder 33	1653	0	\N	1964-00-00	\N
636	0	0	inches	0	inches	\N	retained	original	\N	\N	Box 118	1654	0	\N	0000-00-00	\N
637	\N	9	inches	7	inches	\N	retained	original	One corner is missing and there are some small tears at the edges.	\N	Box 60, Folder 62	1655	0	\N	0000-00-00	\N
638	\N	8	inches	6	inches	\N	retained	original	The board the photo is mounted on is chipped around the edges.	\N	Box 60, Folder 47	1656	0	\N	1927-06-00	\N
639	\N	8	inches	10	inches	\N	retained	original	\N	1681	Box 53, Folder 36	1657	0	\N	1963-10-29	\N
640	0	6	inches	8	inches	\N	retained	original	\N	\N	Box 1, Folder 8 ?	1658	0	\N	1934-11-01	\N
641	0	11	inches	6	inches	\N	retained	original	\N	\N	Box 100, Folder 41	1659	0	\N	0000-00-00	\N
642	0	0	inches	0	inches	\N	retained	\N	\N	\N	\N	1660	0	\N	0000-00-00	\N
643	\N	2	inches	2	inches	\N	retained	original	\N	\N	Box 53, Folder 26	1661	0	\N	0000-00-00	\N
644	\N	7	inches	9	inches	\N	retained	original	Original is creased and has a small tear on the bottom.	\N	Box 60, Folder 28	1662	0	\N	1955-00-00	\N
645	0	6	inches	10	inches	\N	retained	original	\N	\N	OP64	1663	0	\N	1933-01-11	\N
646	\N	10	inches	8	inches	\N	retained	original	\N	1555	Box 51, Folder 20	1664	0	\N	1936-00-00	\N
647	\N	7	inches	5	inches	\N	retained	original	\N	\N	Box 61, Folder 42	1665	0	\N	0000-00-00	\N
648	\N	10	inches	8	inches	\N	retained	original	\N	\N	Box 61, Folder 9	1666	0	\N	0000-00-00	\N
649	\N	10	inches	8	inches	\N	retained	original	\N	\N	Box 60, Folder 57	1667	0	\N	0000-00-00	\N
650	\N	8	inches	10	inches	\N	retained	original	\N	\N	Box 52, Folder 22	1668	0	\N	1970-03-14	\N
651	\N	8	inches	10	inches	\N	retained	original	\N	\N	Box 52, Folder 32	1669	0	\N	1979-00-00	\N
652	\N	8	inches	10	inches	\N	retained	original	\N	\N	Box 52, Folder 31	1670	0	\N	1978-05-07	\N
653	0	8	inches	12	inches	\N	retained	original	\N	1672	Box 1, Folder 5 ?	1671	0	\N	1921-03-17	\N
654	0	0	inches	0	inches	\N	retained	original	\N	1671	Box 1, Folder 5 ?	1672	0	\N	1921-03-17	\N
655	\N	0	inches	0	inches	\N	retained	original	\N	\N	Box 53, Folder 1	1673	0	\N	1934-00-00	\N
656	\N	7	inches	10	inches	\N	retained	original	\N	\N	Box 53, Folder 29	1674	0	\N	1956-00-00	\N
657	\N	0	inches	0	inches	\N	retained	original	\N	\N	Box 3, Folder 28	1675	0	\N	1956-00-00	\N
658	\N	7	inches	5	inches	\N	retained	original	\N	\N	Box 53, Folder 22	1676	0	\N	1951-08-00	\N
659	0	0	inches	0	inches	\N	retained	\N	\N	\N	\N	1677	0	\N	0000-00-00	\N
660	0	0	inches	0	inches	\N	retained	\N	\N	\N	Box 10	1678	0	\N	0000-00-00	\N
661	0	0	inches	0	inches	\N	retained	\N	\N	\N	Box 3	1679	0	\N	1952-04-06	\N
662	\N	7	inches	10	inches	\N	retained	original	\N	1756	Box 61, Folder 44	1680	0	\N	0000-00-00	\N
663	\N	5	inches	5	inches	\N	retained	original	\N	1657	Box 53, Folder 36	1681	0	\N	1963-10-29	\N
664	\N	10	inches	8	inches	\N	retained	original	\N	\N	Box 51, Folder 27	1682	0	\N	1952-00-00	\N
665	\N	4	inches	10	inches	\N	retained	original	\N	\N	Box 60, Folder 35	1683	0	\N	0000-00-00	\N
666	0	0	inches	0	inches	\N	retained	\N	\N	\N	\N	1685	0	\N	1931-00-00	\N
667	0	0	inches	0	inches	\N	retained	\N	\N	\N	\N	1686	0	\N	1931-00-00	\N
668	6	0	inches	0	inches	\N	retained	\N	\N	1427, 1463-4, 1466, 1497, 1527-8, 1605-10, 1617, 1628-35; 1646, 1687-8, 1688.	Bobby Jones collection box 5 folder 25	1687	0	\N	1930-00-00	\N
669	6	0	inches	0	inches	\N	retained	\N	\N	1427, 1463-4, 1466, 1497, 1527-8, 1605-10, 1617, 1628-35; 1646, 1687-8, 1688.	Bobby Jones collection box 5 folder 25	1688	0	\N	\N	\N
670	6	0	inches	0	inches	\N	retained	\N	\N	1689-93.	Bobby Jones collection box 5 folder 26	1689	0	\N	\N	\N
671	6	0	inches	0	inches	\N	retained	\N	\N	1689-93.	Bobby Jones collection box 5 folder 26	1690	0	\N	\N	\N
672	6	0	inches	0	inches	\N	retained	\N	\N	1689-93.	Bobby Jones collection box 5 folder 26	1691	0	\N	\N	\N
673	6	0	inches	0	inches	\N	retained	\N	\N	1689-93.	Bobby Jones collection box 5 folder 26	1692	0	\N	1930-00-00	\N
674	6	0	inches	0	inches	\N	retained	\N	\N	1689-93.	Bobby Jones collection box 5 folder 26	1693	0	\N	1930-00-00	\N
675	6	0	inches	0	inches	\N	retained	\N	\N	\N	Bobby Jones collection box 5 folder 27	1694	0	\N	\N	\N
676	6	0	inches	0	inches	\N	retained	\N	\N	1695-7	Bobby Jones collection box 5 folder 28	1695	0	\N	\N	\N
677	6	0	inches	0	inches	\N	retained	\N	\N	1695-7	Bobby Jones collection box 5 folder 28	1696	0	\N	\N	\N
678	6	0	inches	0	inches	\N	retained	original	\N	1695-7	Bobby Jones collection box 5 folder 28	1697	0	\N	\N	\N
679	96	0	inches	0	inches	\N	retained	original	\N	\N	Bobby Jones collection box 5 folder 29	1698	0	\N	\N	\N
680	6	0	inches	0	inches	\N	retained	original	\N	1700.	Bobby Jones collection box 5 folder 30	1699	0	\N	\N	\N
681	6	0	inches	0	inches	\N	retained	original	\N	1699.	Bobby Jones collection box 5 folder 30	1700	0	\N	\N	\N
682	6	0	inches	0	inches	\N	retained	original	\N	\N	Bobby Jones collection box 5 folder 31	1701	0	\N	\N	\N
683	6	0	inches	0	inches	\N	retained	original	\N	1703	Bobby Jones collection box 5 folder 32	1702	0	\N	\N	\N
684	6	0	inches	0	inches	\N	retained	original	\N	1702	Bobby Jones collection box 5 folder 32	1703	0	\N	\N	\N
685	6	0	inches	0	inches	\N	retained	\N	\N	\N	unknown	1704	0	\N	1930-05-00	\N
686	5	0	inches	0	inches	\N	retained	\N	\N	\N	Unknown	1705	0	\N	\N	\N
687	5	0	inches	0	inches	\N	retained	\N	\N	\N	Young John Allen Papers box 41a folder 1	1707	0	\N	\N	\N
688	5	0	inches	0	inches	\N	retained	\N	\N	\N	Young John Allen Papers box 41a folder 2	1708	0	\N	1886-00-00	\N
689	1	0	inches	0	inches	\N	retained	\N	\N	\N	Young John Allen Papers box 41a folder 3	1709	0	\N	1892-06-10	\N
690	6	0	inches	0	inches	\N	retained	\N	\N	\N	Young John Allen Papers box 41a folder 4	1710	0	\N	\N	\N
691	0	0	inches	0	inches	\N	retained	\N	\N	\N	Young John Allen Papers box 41a folder 4	\N	0	\N	\N	\N
692	5	0	inches	0	inches	\N	retained	\N	\N	\N	PS 1556 P6	1714	0	\N	1895-00-00	\N
693	5	0	inches	0	inches	\N	retained	\N	\N	\N	PS 1556 P6	1715	0	\N	1895-00-00	\N
694	5	0	inches	0	inches	\N	retained	\N	\N	\N	PS 1556 P6	1716	0	\N	1895-00-00	\N
695	5	0	inches	0	inches	\N	retained	\N	\N	\N	PS 1556 P6	1717	0	\N	1895-00-00	\N
696	5	0	inches	0	inches	\N	retained	\N	\N	\N	PS 1556 P6	1718	0	\N	1895-00-00	\N
697	5	0	inches	0	inches	\N	retained	\N	\N	\N	PS 1556 P6	1719	0	\N	1895-00-00	\N
698	5	0	inches	0	inches	\N	retained	\N	\N	\N	PS 1556 P6	1720	0	\N	1895-00-00	\N
699	5	0	inches	0	inches	\N	retained	\N	\N	\N	PS 1556 P6	1721	0	\N	1895-00-00	\N
700	5	0	inches	0	inches	\N	retained	\N	\N	\N	PS 1556 P6	1722	0	\N	1895-00-00	\N
701	96	0	inches	0	inches	\N	retained	\N	\N	\N	F287 R53	1723	0	\N	1842-00-00	\N
702	5	0	inches	0	inches	\N	retained	\N	\N	\N	F287 R52	1724	0	\N	1841-00-00	\N
703	5	0	inches	0	inches	\N	retained	\N	\N	\N	Young John Allen Papers box 41a folder 5	1711	0	\N	1924-05-25	\N
704	5	0	inches	0	inches	\N	retained	\N	\N	\N	Young John Allen Papers box 41a folder 5	1712	0	\N	1924-05-25	\N
705	5	0	inches	0	inches	\N	retained	\N	\N	\N	Young John Allen Papers box 41a folder 6	1713	0	\N	\N	\N
706	6	0	inches	0	inches	\N	retained	\N	\N	\N	Young John Allen Papers box 41a folder 7	1725	0	\N	\N	\N
707	5	0	inches	0	inches	\N	retained	\N	\N	\N	Young John Allen Papers box 41a folder 8	1726	0	\N	\N	\N
708	6	0	inches	0	inches	\N	retained	\N	\N	\N	Young John Allen Papers box 41a folder 9	1727	0	\N	\N	\N
709	5	0	inches	0	inches	\N	retained	\N	\N	1729.	Confederate Misc. II	1728	0	\N	1895-00-00	\N
710	5	0	inches	0	inches	\N	retained	\N	\N	1728.	Confederate Misc. II	1729	0	\N	1895-00-00	\N
711	0	0	inches	0	inches	\N	retained	\N	\N	\N	10	\N	0	\N	\N	\N
712	5	0	inches	0	inches	\N	retained	\N	\N	\N	Young John Allen Papers box 41a folder 10	1730	0	\N	1920-02-14	\N
713	6	0	inches	0	inches	\N	retained	\N	\N	\N	Young John Allen Papers box 41a folder 11	1731	0	\N	\N	\N
714	6	0	inches	0	inches	\N	retained	\N	\N	1 of 2	Young John Allen Papers box 41a folder 12	1732	0	\N	\N	\N
715	6	0	inches	0	inches	\N	retained	\N	\N	2 of 2	Young John Allen Papers box 41a folder 12	1733	0	\N	\N	\N
716	5	0	inches	0	inches	\N	retained	\N	\N	1 of 2	Young John Allen Papers box 41a folder 13	1734	0	\N	\N	\N
717	5	0	inches	0	inches	\N	retained	\N	\N	2 of 2	Young John Allen Papers box 41a folder 13	1735	0	\N	\N	\N
718	5	0	inches	0	inches	\N	retained	\N	\N	\N	Young John Allen Papers box 41a folder 14	1736	0	\N	\N	\N
719	5	0	inches	0	inches	\N	retained	\N	\N	\N	Young John Allen Papers box 41a folder 15	1737	0	\N	\N	\N
720	5	0	inches	0	inches	\N	retained	\N	\N	\N	Young John Allen Papers box 41a folder 16	1738	0	\N	\N	\N
721	5	0	inches	0	inches	\N	retained	\N	\N	\N	Young John Allen Papers box 41a folder 17	1739	0	\N	1900-02-07	\N
722	5	0	inches	0	inches	\N	retained	\N	\N	\N	Young John Allen Papers box 41a folder 18	1740	0	\N	1906-00-00	\N
723	6	0	inches	0	inches	\N	retained	\N	\N	\N	Young John Allen Papers box 41a folder 19	1741	0	\N	\N	\N
724	5	0	inches	0	inches	\N	retained	\N	\N	\N	Young John Allen Papers box 41a folder 20	1742	0	\N	1938-00-00	\N
725	5	0	inches	0	inches	\N	retained	\N	\N	\N	Young John Allen Papers box 41a folder 21	1743	0	\N	\N	\N
726	6	0	inches	0	inches	\N	retained	\N	\N	\N	Young John Allen Papers box 41a folder 22	1744	0	\N	\N	\N
727	6	0	inches	0	inches	\N	retained	\N	\N	\N	Young John Allen Papers box 41a folder 22	1745	0	\N	\N	\N
728	5	0	inches	0	inches	\N	retained	\N	\N	\N	Young John Allen Papers box 41a folder 23	1746	0	\N	1915-00-00	\N
729	6	0	inches	0	inches	\N	retained	\N	\N	\N	Young John Allen Papers box 41a folder 24	1747	0	\N	1917-00-00	\N
730	5	0	inches	0	inches	\N	retained	\N	\N	\N	Young John Allen Papers box 41a folder 25	1748	0	\N	\N	\N
731	5	0	inches	0	inches	\N	retained	\N	\N	1749-53.	Young John Allen Papers box 41a folder 27	1749	0	\N	1875-00-00	\N
732	5	0	inches	0	inches	\N	retained	\N	\N	1749-53.	Young John Allen Papers box 41a folder 27	1750	0	\N	1875-00-00	\N
733	5	0	inches	0	inches	\N	retained	\N	\N	1749-53.	Young John Allen Papers box 41a folder 27	1751	0	\N	1875-00-00	\N
734	5	0	inches	0	inches	\N	retained	\N	\N	1749-53.	Young John Allen Papers box 41a folder 27	1752	0	\N	1875-00-00	\N
735	6	0	inches	0	inches	\N	retained	\N	\N	1749-53.	Young John Allen Papers box 41a folder 27	1753	0	\N	1875-00-00	\N
736	\N	8	inches	10	inches	\N	retained	original	\N	\N	Box 53, Folder 55	1754	0	\N	1984-12-06	\N
737	\N	0	inches	0	inches	\N	retained	original	The source image is a copy print.	\N	Box 61, Folder 49	1755	0	\N	0000-00-00	\N
738	\N	7	inches	10	inches	\N	retained	original	\N	1680	Box 61, Folder 44	1756	0	\N	1963-00-00	\N
739	0	0	inches	0	inches	\N	retained	\N	\N	\N	photographs, Box 3	1757	0	\N	1963-10-29	\N
740	\N	4	inches	6	inches	\N	retained	original	\N	1543, 1759, 1760	Box 60, Folder 39	1758	0	\N	0000-00-00	\N
741	\N	4	inches	6	inches	\N	retained	original	\N	1760, 1543	Box 60, Folder 39	1759	0	\N	0000-00-00	\N
742	\N	4	inches	6	inches	\N	retained	original	\N	1543, 1759	Box 60, Folder 39	1760	0	\N	0000-00-00	\N
743	0	0	inches	0	inches	\N	retained	\N	\N	\N	photographs, Box 10	1761	0	\N	0000-00-00	\N
744	0	0	inches	0	inches	\N	retained	\N	\N	\N	Box 10, Folder 9 ?	1762	0	\N	0000-00-00	\N
745	5	0	inches	0	inches	\N	retained	\N	\N	\N	photographs, Box 11	1763	0	\N	0000-00-00	\N
746	0	9	inches	6	inches	\N	retained	original	\N	1764	Box 108, Folder 21	1764	0	\N	1915-10-17	\N
747	0	9	inches	6	inches	\N	retained	original	\N	1764	Box 108, Folder 21	1765	0	\N	1915-10-17	\N
748	0	6	inches	4	inches	\N	retained	original	\N	1767	Box 100, Folder 5	1766	0	\N	1919-05-10	\N
749	0	6	inches	7	inches	\N	retained	original	\N	1766	Box 100, Folder 5	1767	0	\N	1919-05-10	\N
750	0	0	inches	0	inches	\N	retained	\N	\N	\N	Other Papers	1768	0	\N	1927-01-00	\N
751	\N	8	inches	10	inches	\N	retained	original	\N	\N	Box 52, Folder 52	1769	0	\N	1927-00-00	\N
752	0	9	inches	6	inches	\N	retained	original	\N	\N	Box 100, Folder 27	1770	0	\N	1928-05-06	\N
753	0	8	inches	6	inches	\N	retained	original	\N	\N	Box 101, Folder 5	1771	0	\N	1956-00-00	\N
754	0	9	inches	6	inches	\N	retained	original	\N	\N	Box 107, Folder 2	1772	0	\N	1931-11-00	\N
755	0	5	inches	3	inches	\N	retained	original	\N	\N	Box 42, Folder 33	1773	0	\N	1965-00-00	\N
756	\N	8	inches	10	inches	\N	retained	original	\N	1539, 1928	Box 60, Folder 19	1774	0	\N	1950-12-00	\N
757	\N	8	inches	10	inches	\N	retained	original	\N	\N	Box 60, Folder 27	1775	0	\N	1955-03-20	\N
758	\N	8	inches	21	inches	\N	retained	original	\N	\N	OP61	1776	0	\N	1921-00-00	\N
759	0	0	inches	0	inches	\N	retained	\N	\N	\N	Music library	1777	0	\N	0000-00-00	\N
760	0	0	inches	0	inches	\N	retained	\N	\N	\N	Music Library	1778	0	\N	0000-00-00	\N
761	0	12	inches	9	inches	\N	retained	original	\N	\N	Box 15, Folder 16	1779	0	\N	1927-00-00	\N
762	5	0	inches	0	inches	\N	retained	\N	\N	\N	Woodson DT351 B273 1870	1780	0	\N	1870-00-00	\N
763	5	0	inches	0	inches	\N	retained	\N	\N	\N	Woodson DT351 B273 1870	1781	0	\N	1870-00-00	\N
764	5	0	inches	0	inches	\N	retained	\N	\N	\N	Woodson DT756 H3 1838	1782	0	\N	1838-00-00	\N
765	5	0	inches	0	inches	\N	retained	\N	\N	1 of 7	Young John Allen Papers box 41a folder 26	1783	0	\N	1906-04-10	\N
766	5	0	inches	0	inches	\N	retained	\N	\N	2 of 7	Young John Allen Papers box 41a folder 26	1784	0	\N	\N	\N
767	5	0	inches	0	inches	\N	retained	\N	\N	3 of 7	Young John Allen Papers box 41a folder 26	1785	0	\N	\N	\N
768	5	0	inches	0	inches	\N	retained	\N	\N	4 of 7	Young John Allen Papers box 41a folder 26	1786	0	\N	\N	\N
769	5	0	inches	0	inches	\N	retained	\N	\N	5 of 7	Young John Allen Papers box 41a folder 26	1787	0	\N	\N	\N
770	5	0	inches	0	inches	\N	retained	\N	\N	6 of 7	Young John Allen Papers box 41a folder 26	1788	0	\N	\N	\N
771	5	0	inches	0	inches	\N	retained	\N	\N	1790	\N	1789	0	\N	1941-01-00	\N
772	5	0	inches	0	inches	\N	retained	\N	\N	1789	\N	1790	0	\N	1941-01-00	\N
773	5	0	inches	0	inches	\N	retained	\N	\N	\N	\N	1791	0	\N	1941-01-00	\N
774	5	0	inches	0	inches	\N	retained	\N	\N	\N	\N	1792	0	\N	1941-01-00	\N
775	5	0	inches	0	inches	\N	retained	\N	\N	\N	\N	1793	0	\N	1941-01-00	\N
776	5	0	inches	0	inches	\N	retained	\N	\N	\N	\N	1794	0	\N	1941-01-00	\N
777	5	0	inches	0	inches	\N	retained	\N	\N	\N	\N	1795	0	\N	1941-01-00	\N
778	5	0	inches	0	inches	\N	retained	\N	\N	\N	\N	1796	0	\N	1938-00-00	\N
779	5	0	inches	0	inches	\N	retained	\N	\N	\N	\N	1797	0	\N	1939-12-00	\N
780	5	0	inches	0	inches	\N	retained	\N	\N	\N	Woodson S544.3 A2 C3 1936	1798	0	\N	1936-00-00	\N
781	6	0	inches	0	inches	\N	retained	\N	\N	\N	\N	1799	0	\N	1930-00-00	\N
782	5	0	inches	0	inches	\N	retained	original	\N	\N	Woodson E185.61 N35 1929	1800	0	\N	1929-01-00	1929-01-00
783	5	0	inches	0	inches	\N	retained	\N	\N	1803	\N	1801	0	\N	1963-12-00	\N
784	6	0	inches	0	inches	\N	retained	\N	\N	\N	PS 3515 U34 F55 Copy 1	1802	0	\N	1930-04-07	\N
785	5	0	inches	0	inches	\N	retained	\N	\N	1801	\N	1803	0	\N	1964-09-14	\N
786	6	0	inches	0	inches	\N	retained	\N	\N	\N	Woodson F1231 T44 1890	1804	0	\N	1890-00-00	\N
787	6	0	inches	0	inches	\N	retained	\N	\N	\N	\N	1805	0	\N	1941-01-00	\N
788	5	0	inches	0	inches	\N	retained	\N	\N	\N	Woodson E513.5 54th E45 1894	1806	0	\N	1894-00-00	\N
789	5	0	inches	0	inches	\N	retained	\N	\N	\N	Woodson E513.5 54th E45 1894	1807	0	\N	1894-00-00	\N
790	5	0	inches	0	inches	\N	retained	\N	\N	\N	\N	1808	0	\N	1909-00-00	\N
791	5	0	inches	0	inches	\N	retained	\N	\N	\N	\N	1809	0	\N	1909-00-00	\N
792	6	0	inches	0	inches	\N	retained	\N	\N	\N	Woodson GV697 A1 H45 1939	1810	0	\N	1939-00-00	\N
793	5	0	inches	0	inches	\N	retained	\N	\N	\N	Woodson LJ75 O55 D7 1940	1811	0	\N	1921-00-00	\N
794	5	0	inches	0	inches	\N	retained	\N	\N	\N	Woodson LJ75 O55 D7 1940	1812	0	\N	1940-00-00	\N
795	0	0	inches	0	inches	\N	retained	\N	\N	\N	WLD sheet music, Box 2	1813	0	\N	1967-00-00	\N
796	0	10	inches	7	inches	\N	retained	original	\N	\N	Box 71, Folder 17 or 18	1814	0	\N	1962-00-00	\N
797	0	10	inches	7	inches	\N	retained	original	\N	\N	Box 70, Folder 20	1815	0	\N	1942-00-00	\N
798	0	0	inches	0	inches	\N	retained	\N	\N	\N	WLD sheet music, Box 2	1816	0	\N	0000-00-00	\N
799	0	12	inches	9	inches	\N	retained	original	\N	\N	Box 75, Folder 43	1817	0	\N	1954-00-00	\N
800	0	12	inches	9	inches	\N	retained	original	\N	\N	Box 75, Folder 15	1818	0	\N	1926-00-00	\N
801	0	0	inches	0	inches	\N	retained	\N	\N	\N	\N	1819	0	\N	1941-00-00	\N
802	0	14	inches	10.5	inches	\N	retained	original	\N	1821	Box 70, Folder 4	1820	0	\N	1965-00-00	\N
803	0	14	inches	7.0999999999999996	inches	\N	retained	original	\N	1820	Box 70, Folder 4	1821	0	\N	1965-00-00	\N
804	0	10	inches	7	inches	\N	retained	original	\N	1823	Box 70, Folder 36	1822	0	\N	1925-00-00	\N
805	0	10	inches	14	inches	\N	retained	original	\N	1822	Box 70, Folder 46	1823	0	\N	1925-00-00	\N
806	0	10	inches	7	inches	\N	retained	original	\N	\N	Box 74, Folder 21	1824	0	\N	1934-00-00	\N
807	0	9	inches	6	inches	\N	retained	original	\N	\N	Box 74, Folder 8	1825	0	\N	1936-00-00	\N
808	0	8	inches	36	inches	\N	retained	original	1829-1898 (life of Johnson Hagood)	\N	box 1 folder 12	1827	0	\N	\N	\N
809	0	11	inches	8	inches	\N	retained	original	\N	\N	Box 78, Folder 10	1828	0	\N	1943-00-00	\N
810	0	10	inches	12	inches	\N	retained	original	\N	1843	MARBL ML3356 .W78	1829	0	\N	1907-00-00	\N
811	0	11.300000000000001	inches	16.800000000000001	inches	\N	retained	original	\N	1831	Box 101, Folder 1	1830	0	\N	1953-03-20	\N
812	0	8.8000000000000007	inches	11.300000000000001	inches	\N	retained	original	\N	1830	Box 101, Folder 1	1831	0	\N	1953-03-20	\N
813	\N	12.300000000000001	inches	9.6999999999999993	inches	\N	retained	original	\N	\N	OP53	1832	0	\N	1935-09-01	\N
814	0	5	inches	4	inches	\N	retained	\N	\N	\N	Box 100, Folder 18	1833	0	\N	1923-06-04	\N
815	0	9	inches	12	inches	\N	retained	original	\N	1835	Box 100, Folder 51	1834	0	\N	1936-04-04	\N
816	0	9	inches	6	inches	\N	retained	original	\N	1834	Box 100, folder 51	1835	0	\N	1936-04-04	\N
817	\N	10.1	inches	7.7000000000000002	inches	\N	retained	original	\N	\N	Box 58, Folder 20	1836	0	\N	0000-00-00	\N
818	0	0	inches	0	inches	\N	retained	\N	\N	\N	Scores	\N	0	\N	\N	\N
819	0	7	inches	10	inches	\N	retained	original	\N	1838, 1839	OP10	1837	0	\N	0000-00-00	\N
820	0	15	inches	11	inches	\N	retained	original	\N	1837, 1839	OP10	1838	0	\N	0000-00-00	\N
821	0	15	inches	11	inches	\N	retained	original	\N	1837, 1838	OP10	1839	0	\N	0000-00-00	\N
822	0	12	inches	9	inches	\N	retained	original	\N	\N	\N	1840	0	\N	1921-00-00	\N
823	0	10	inches	14	inches	\N	retained	original	\N	\N	\N	1841	0	\N	1913-00-00	\N
824	\N	7.7999999999999998	inches	14.300000000000001	inches	\N	retained	original	\N	\N	Box 60, Folder 3	1842	0	\N	1933-01-00	\N
825	0	10	inches	6	inches	\N	retained	original	\N	1829	MARBL ML3356 .W78	1843	0	\N	1907-00-00	\N
826	\N	9.6999999999999993	inches	7.7999999999999998	inches	\N	retained	original	\N	\N	Box 61, Folder 43	1844	0	\N	0000-00-00	\N
827	0	3	inches	12	inches	\N	retained	original	\N	1846, 1847	OP11	1845	0	\N	0000-00-00	\N
828	0	3	inches	12	inches	\N	retained	original	\N	1845, 1847	OP11	1846	0	\N	0000-00-00	\N
829	0	2	inches	12	inches	\N	retained	original	\N	1845, 1846	OP11	1847	0	\N	0000-00-00	\N
830	0	11	inches	7	inches	\N	retained	original	\N	\N	Box 72, Folder 29	1848	0	\N	1942-00-00	\N
831	6	0	inches	0	inches	\N	retained	\N	\N	1851	Woodson HJ 8547 T78	1850	0	\N	1937-00-00	\N
832	6	0	inches	0	inches	\N	retained	\N	\N	1851	Woodson HJ 8547 T78	1851	0	\N	1937-00-00	\N
833	5	0	inches	0	inches	\N	retained	\N	\N	\N	not cataloged	1852	0	\N	1927-00-00	\N
834	5	0	inches	0	inches	\N	retained	\N	\N	\N	Woodson	1853	0	\N	1847-00-00	\N
835	0	0	inches	0	inches	\N	retained	\N	\N	\N	Woodson	1854	0	\N	1847-00-00	\N
836	5	0	inches	0	inches	\N	retained	\N	\N	\N	Woodson	1855	0	\N	1847-00-00	\N
837	6	0	inches	0	inches	\N	retained	\N	\N	\N	Woodson LD393 B4 1892	1856	0	\N	1892-00-00	\N
838	6	0	inches	0	inches	\N	retained	\N	\N	\N	Woodson HD6515 R36 B7	1857	0	\N	1946-00-00	\N
839	5	0	inches	0	inches	\N	retained	\N	\N	1859	Woodson GN 861 P4 1950	1858	0	\N	1950-00-00	\N
840	6	0	inches	0	inches	\N	retained	\N	\N	1859	Woodson GN861 P4 1950	1859	0	\N	1950-00-00	\N
841	5	0	inches	0	inches	\N	retained	\N	\N	\N	E185 W89 1962	1860	0	\N	1962-00-00	\N
842	5	0	inches	0	inches	\N	retained	\N	\N	1862	PQ2625 A74 B313 1922	1861	0	\N	1922-00-00	\N
843	5	0	inches	0	inches	\N	retained	\N	\N	1861	PQ2625 A74 B313 1922	1862	0	\N	1922-00-00	\N
844	5	0	inches	0	inches	\N	retained	\N	\N	\N	Woodson HT1581 .A6 1969	1863	0	\N	1848-00-00	\N
845	5	0	inches	0	inches	\N	retained	\N	\N	\N	Woodson	1864	0	\N	1916-01-00	\N
846	5	0	inches	0	inches	\N	retained	\N	\N	\N	Woodson F2131 E48 1806 v.1	1865	0	\N	1806-00-00	\N
847	\N	3.3999999999999999	inches	5.5	inches	\N	retained	original	\N	\N	Box 111, Folder 26	1866	0	\N	1926-00-00	\N
848	0	11	inches	7	inches	\N	retained	original	\N	\N	Box 111, Folder 26	1867	0	\N	1926-00-00	\N
849	0	10	inches	8	inches	\N	retained	original	\N	\N	Box 18, Folder 2 ?	1868	0	\N	0000-00-00	\N
850	0	13	inches	10	inches	\N	retained	original	\N	\N	Box 79, Folder 3	1869	0	\N	1923-00-00	\N
851	0	10	inches	7	inches	\N	retained	original	\N	\N	Box 78, Folder 33	1870	0	\N	1929-00-00	\N
852	0	0	inches	0	inches	\N	retained	\N	\N	\N	Box 100, Folder 17	1871	0	\N	1921-08-00	\N
853	0	0	inches	0	inches	\N	retained	\N	\N	\N	Box 100, Folder 21	1872	0	\N	1927-05-28	\N
854	0	14	inches	11	inches	\N	retained	original	\N	1874	OP17	1873	0	\N	0000-00-00	\N
855	0	14	inches	11	inches	\N	retained	original	\N	1873	OP17 ?	1874	0	\N	0000-00-00	\N
856	0	9.4000000000000004	inches	12.199999999999999	inches	\N	retained	original	\N	\N	Box 107, Folder 2	1875	0	\N	1931-00-00	\N
857	0	0	inches	0	inches	\N	retained	\N	\N	1 of 2, cover	Printed Material, WLD Programs	1876	0	\N	1932-12-00	\N
858	0	0	inches	0	inches	\N	retained	\N	\N	2 of 2, inside pages	Printed Material, WLD Programs	1877	0	\N	1932-12-00	\N
859	0	14	inches	11	inches	\N	retained	original	\N	1879, 1880, 1881	Box 18, Folder 1	1878	0	\N	0000-00-00	\N
860	0	14	inches	11	inches	\N	retained	original	\N	1878, 1880, 1881	Box 18, Folder 1	1879	0	\N	0000-00-00	\N
861	0	14	inches	11	inches	\N	retained	original	\N	1878, 1879, 1881	Box 18, Folder 1	1880	0	\N	0000-00-00	\N
862	0	14	inches	11	inches	\N	retained	original	\N	1878, 1879, 1880	Box 18, Folder 1	1881	0	\N	0000-00-00	\N
863	0	0	inches	0	inches	\N	retained	\N	\N	\N	\N	1882	0	\N	0000-00-00	\N
864	0	10	inches	7	inches	\N	retained	original	\N	\N	PS3531 .E933 D7 1949	1883	0	\N	1949-00-00	\N
865	0	4	inches	3	inches	\N	retained	original	\N	\N	Box 118	1884	0	\N	0000-00-00	\N
866	0	9	inches	8	inches	\N	retained	original	\N	\N	PS3545 .I5332 R3 1943	1885	0	\N	1943-00-00	\N
867	5	0	inches	0	inches	\N	retained	\N	\N	\N	Woodson	1886	0	\N	1916-00-00	\N
868	5	0	inches	0	inches	\N	retained	\N	\N	\N	Woodson	1887	0	\N	1996-00-00	\N
869	5	0	inches	0	inches	\N	retained	\N	\N	\N	Woodson uncataloged	1888	0	\N	1944-06-00	\N
870	5	0	inches	0	inches	\N	retained	\N	\N	\N	Woodson uncataloged	1889	0	\N	1944-05-00	\N
871	5	0	inches	0	inches	\N	retained	\N	\N	\N	Woodson uncataloged	1890	0	\N	1911-00-00	\N
872	5	0	inches	0	inches	\N	retained	\N	\N	\N	Woodson uncataloged	1891	0	\N	1911-07-00	\N
873	5	0	inches	0	inches	\N	retained	\N	\N	\N	Woodson uncataloged	1892	0	\N	1940-00-00	\N
874	5	0	inches	0	inches	\N	retained	\N	\N	\N	Woodson uncataloged	1893	0	\N	1989-00-00	\N
875	5	0	inches	0	inches	\N	retained	\N	\N	\N	Woodson uncataloged	1894	0	\N	1942-03-00	\N
876	5	0	inches	0	inches	\N	retained	\N	\N	\N	Woodson uncataloged	1895	0	\N	\N	\N
877	6	0	inches	0	inches	\N	retained	\N	\N	\N	D639 N4 S3	1896	0	\N	1919-00-00	\N
878	6	0	inches	0	inches	\N	retained	\N	\N	\N	D639 N4 S3	1897	0	\N	1919-00-00	\N
879	6	0	inches	0	inches	\N	retained	\N	\N	\N	D639 N4 S3	1898	0	\N	1919-00-00	\N
880	5	0	inches	0	inches	\N	retained	\N	\N	\N	Woodson E185.63 W815 1888b	1899	0	\N	1888-00-00	\N
881	5	0	inches	0	inches	\N	retained	original	\N	\N	Woodson E185.63 W815 1888b	1900	0	\N	1888-00-00	\N
882	5	0	inches	0	inches	\N	retained	original	\N	\N	Woodson E185.63 W815 1888b	1901	0	\N	1888-00-00	\N
883	5	0	inches	0	inches	\N	retained	\N	\N	\N	Woodson PE1119 .W55 1938	1902	0	\N	1938-00-00	\N
884	5	0	inches	0	inches	\N	retained	\N	\N	\N	Woodson PE1119 .W55 1938	1903	0	\N	1938-00-00	\N
885	5	0	inches	0	inches	\N	retained	\N	\N	\N	Woodson PE1119 .W55 1938	1904	0	\N	1938-00-00	\N
886	5	0	inches	0	inches	\N	retained	\N	\N	\N	Woodson GN645 .L55 1945	1905	0	\N	1946-01-13	\N
887	5	0	inches	0	inches	\N	retained	\N	\N	\N	Woodson DT511 W28	1906	0	\N	\N	\N
888	6	0	inches	0	inches	\N	retained	\N	\N	\N	Woodson DT 386 .W6	1907	0	\N	1935-00-00	\N
889	5	0	inches	0	inches	\N	retained	\N	\N	\N	Woodson PR 9390.9 .C74	1908	0	\N	\N	\N
890	6	0	inches	0	inches	\N	retained	\N	\N	\N	Woodson DT31 M6 1920	1909	0	\N	1920-00-00	\N
891	6	0	inches	0	inches	\N	retained	\N	\N	\N	Woodson DT31 M6 1920	1910	0	\N	1920-00-00	\N
892	6	0	inches	0	inches	\N	retained	\N	\N	\N	Woodson E185.5 N277 .D3 1933	1911	0	\N	1895-12-00	\N
893	6	0	inches	0	inches	\N	retained	\N	\N	\N	Woodson E185.5 N277 .D3 1933	1912	0	\N	1895-12-00	\N
894	0	8	inches	12	inches	\N	retained	original	\N	\N	ML3556 .J39	1913	0	\N	1968-00-00	\N
895	0	6	inches	4	inches	\N	retained	original	\N	1915	Box 2, Folder 7 ?	1914	0	\N	1934-00-00	\N
896	0	6	inches	4	inches	\N	retained	original	\N	1914	Box 2, Folder 7 ?	1915	0	\N	1934-00-00	\N
897	0	0	inches	0	inches	\N	retained	\N	\N	1 of 2	scores	1916	0	\N	0000-00-00	\N
898	0	18	inches	14	inches	\N	retained	original	\N	1918, 1921, 1922	OP4.1	1917	0	\N	0000-00-00	\N
899	0	18	inches	14	inches	\N	retained	original	\N	1917, 1921, 1922	OP4.1	1918	0	\N	0000-00-00	\N
900	0	0	inches	0	inches	\N	retained	\N	\N	\N	OP4.2	1919	0	\N	0000-00-00	\N
901	0	0	inches	0	inches	\N	retained	\N	\N	\N	OP4.3	1920	0	\N	0000-00-00	\N
902	0	0	inches	0	inches	\N	retained	\N	\N	\N	OP4.1	1921	0	\N	0000-00-00	\N
903	0	0	inches	0	inches	\N	retained	\N	\N	\N	Scores	1922	0	\N	0000-00-00	\N
904	0	0	inches	0	inches	\N	retained	\N	\N	\N	Scores	1923	0	\N	0000-00-00	\N
905	0	0	inches	0	inches	\N	retained	\N	\N	\N	Scores	1924	0	\N	0000-00-00	\N
906	0	8	inches	6	inches	\N	retained	original	\N	\N	PS3555 .L625 I6 1952 COPY 2	1925	0	\N	1952-00-00	\N
907	0	9.8000000000000007	inches	7.5	inches	\N	retained	original	\N	\N	Box 15, Folder 7	1926	0	\N	1943-00-00	\N
908	5	0	inches	0	inches	\N	retained	\N	\N	\N	\N	1927	0	\N	0000-00-00	\N
909	\N	8.0999999999999996	inches	9.9000000000000004	inches	\N	retained	original	\N	1539, 1774	Box 60, Folder 19	1928	0	\N	1950-12-00	\N
910	\N	7	inches	5	inches	\N	retained	original	\N	\N	Box 53, Folder 5	1929	0	\N	0000-00-00	\N
911	\N	7.5999999999999996	inches	9.5	inches	\N	retained	original	\N	\N	Box 52, Folder 5	1930	0	\N	1979-00-00	\N
912	\N	10	inches	8	inches	\N	retained	original	\N	\N	Box 51, Folder 30	1931	0	\N	1960-00-00	\N
913	5	0	inches	0	inches	\N	retained	\N	\N	\N	\N	1932	0	\N	0000-00-00	\N
914	0	0	inches	0	inches	\N	retained	\N	\N	\N	Box 10, Folder 9 ?	1933	0	\N	0000-00-00	\N
915	5	10	inches	7	inches	\N	retained	original	\N	\N	Woodson not cataloged	1934	0	\N	1916-12-00	1916-12-00
916	5	9	inches	6	inches	\N	retained	original	\N	\N	Woodson D639 N4 T46 1917	1935	0	\N	1917-00-00	1917-00-00
917	5	13	inches	10	inches	\N	retained	original	\N	\N	Woodson	1936	0	\N	1928-02-00	1928-02-00
918	5	10	inches	7	inches	\N	retained	original	\N	\N	Woodson uncataloged	1937	0	\N	1916-00-00	1916-00-00
919	5	7	inches	5	inches	\N	retained	original	\N	Image for Carter G. Woodson exhibit	Woodson uncataloged	1938	0	\N	1897-00-00	1897-00-00
920	5	8	inches	6	inches	\N	retained	original	\N	1940, 1941	Woodson P27 F644 N48 1922	1939	0	\N	1922-00-00	1922-00-00
921	5	8	inches	6	inches	\N	retained	original	\N	1939, 1941	Woodson P27 F644 N48 1922	1940	\N	\N	1922-00-00	1922-00-00
922	5	8	inches	6	inches	\N	retained	original	\N	1940, 1941	Woodson P27 F644 N48 1922	1941	\N	\N	1922-00-00	1922-00-00
923	5	9	inches	6	inches	\N	retained	original	\N	\N	\N	1942	0	\N	\N	\N
924	6	9	inches	6	inches	\N	retained	original	\N	1943, 1944, 1945, 1946	E185 .W89 1927 c. 1	1943	0	\N	1927-00-00	1927-00-00
925	6	9	inches	6	inches	\N	retained	original	\N	1943, 1944, 1945, 1946	E185 .W89 1927 c. 1	1944	\N	\N	1927-00-00	1927-00-00
926	6	9	inches	6	inches	\N	retained	original	\N	1943, 1944, 1945, 1946	E185 .W89 1927 c. 1	1945	\N	\N	1927-00-00	1927-00-00
927	6	9	inches	6	inches	\N	retained	original	\N	1943, 1944, 1945, 1946	E185 .W89 1927 c. 1	1946	\N	\N	1927-00-00	1927-00-00
928	5	9	inches	6	inches	\N	retained	original	\N	\N	Woodson	1947	0	\N	\N	\N
929	5	8	inches	5	inches	\N	retained	original	\N	\N	Woodson	1948	0	\N	\N	\N
930	5	7	inches	4	inches	\N	retained	original	\N	\N	\N	1949	0	\N	\N	\N
931	5	11	inches	9	inches	\N	retained	original	\N	1951	Woodson	1950	0	\N	\N	\N
933	5	11	inches	9	inches	\N	retained	original	\N	1950	Woodson	1951	0	\N	\N	\N
934	5	10	inches	7	inches	\N	retained	original	\N	\N	Woodson uncataloged	1952	0	\N	1916-00-00	1916-00-00
935	5	10	inches	7	inches	\N	retained	original	\N	\N	Woodson uncataloged	1953	0	\N	1916-01-00	1991-10-31
936	5	8	inches	3	inches	\N	retained	original	\N	\N	Woodson uncataloged	1954	0	\N	1916-00-00	1916-00-00
937	6	9	inches	6	inches	\N	retained	original	\N	\N	Woodson	1955	0	\N	\N	\N
938	5	9	inches	6	inches	\N	retained	original	\N	\N	Woodson	1956	0	\N	1929-00-00	1929-00-00
939	5	9	inches	4	inches	\N	retained	original	\N	\N	Woodson uncataloged	1957	0	\N	\N	\N
940	5	8	inches	4	inches	\N	retained	original	\N	\N	Woodson	1958	0	\N	\N	\N
941	5	12	inches	9	inches	\N	retained	original	\N	\N	Woodson	1959	0	\N	\N	\N
942	5	12	inches	9	inches	\N	retained	original	\N	\N	Woodson	1960	0	\N	\N	\N
943	5	6	inches	5	inches	\N	retained	original	\N	\N	Woodson	1961	0	\N	1942-00-00	1942-00-00
944	0	8	inches	5	inches	\N	retained	original	\N	\N	Woodson	1962	0	\N	\N	\N
945	6	8	inches	6	inches	\N	retained	original	\N	\N	Woodson	1963	0	\N	1927-00-00	1927-00-00
946	5	6	inches	9	inches	\N	retained	original	\N	\N	Woodson	1964	0	\N	1941-11-01	1941-11-01
947	0	7	inches	4	inches	\N	retained	original	\N	\N	Woodson	1965	0	\N	\N	\N
948	0	5	inches	8	inches	\N	retained	original	\N	\N	Woodson	1966	0	\N	\N	\N
949	5	12	inches	9	inches	\N	retained	original	\N	\N	Woodson M1670 S77 1937 v. 2	1967	0	\N	1937-00-00	1937-00-00
950	5	9	inches	6	inches	\N	retained	original	\N	\N	Woodson E185.5 .N4 1913 copy 1	1968	0	\N	1913-00-00	1913-00-00
951	5	10	inches	6	inches	\N	retained	original	\N	\N	Woodson E185.86 .B254	1969	0	\N	\N	\N
952	5	7	inches	5	inches	\N	retained	original	\N	\N	Woodson PS3505 .A94 A8	1970	0	\N	1919-00-00	1919-00-00
953	5	10	inches	7	inches	\N	retained	original	\N	1972	Woodson QC 407 .A44 1939	1971	0	\N	1937-00-00	\N
954	5	10	inches	7	inches	\N	retained	original	\N	1971	Woodson QC 407 .A44 1939	1972	\N	\N	1937-00-00	\N
955	5	9	inches	6	inches	\N	retained	original	\N	\N	Woodson 185.5 A51 No. 18119	1973	0	\N	1915-00-00	\N
956	5	9	inches	7	inches	\N	retained	original	\N	\N	Woodson E185.6 W3185 1938	1974	0	\N	1938-00-00	1938-00-00
957	5	10	inches	7	inches	\N	retained	original	\N	\N	Woodson uncataloged	1975	0	\N	1911-04-00	1911-04-00
958	5	12	inches	9	inches	\N	retained	original	\N	\N	Woodson uncataloged	1976	0	\N	1947-01-00	1947-01-00
959	5	11	inches	9	inches	\N	retained	original	\N	\N	woodson uncataloged	1977	0	\N	1947-11-00	1947-11-00
960	5	9	inches	7	inches	\N	retained	original	\N	\N	Woodson unccataloged	1978	0	\N	1937-00-00	1937-00-00
961	6	6	inches	4	inches	\N	retained	original	\N	\N	Woodson uncataloged	1979	0	\N	1970-00-00	1970-00-00
962	5	10	inches	7	inches	\N	retained	original	\N	\N	\N	1980	0	\N	1911-07-00	1911-07-00
963	5	12	inches	9	inches	\N	retained	original	\N	\N	Woodson uncataloged	1982	0	\N	1942-10-00	1942-10-00
964	5	9	inches	7	inches	\N	retained	original	\N	\N	Woodson uncataloged	1983	0	\N	1900-00-00	1900-00-00
965	5	9	inches	7	inches	\N	retained	original	\N	\N	Woodson uncataloged	1984	\N	\N	1900-00-00	1900-00-00
966	6	14	inches	11	inches	\N	retained	original	\N	\N	Woodson	1985	0	\N	\N	\N
967	\N	14	inches	10	inches	\N	retained	original	\N	\N	Box 30, Folder 2	1986	0	\N	1955-03-00	\N
968	\N	14	inches	10	inches	\N	retained	original	\N	\N	Box 30, Folder 2	1987	\N	\N	1955-03-00	\N
969	5	11	inches	17	inches	\N	retained	original	\N	\N	Dawson box 30 folder 12	1988	0	\N	\N	\N
970	5	11	inches	17	inches	\N	retained	original	\N	\N	Dawson box 30 folder 12	1989	0	\N	\N	\N
971	5	14	inches	10	inches	\N	retained	original	\N	1990-94	Dawson box 79 folder 1	1990	0	\N	\N	\N
972	5	14	inches	10	inches	\N	retained	original	\N	1990-94	Dawson box 79 folder 1	1991	\N	\N	\N	\N
973	5	14	inches	10	inches	\N	retained	original	\N	1990-94	Dawson box 79 folder 1	1992	\N	\N	\N	\N
974	5	14	inches	10	inches	\N	retained	original	\N	1990-94	Dawson box 79 folder 1	1993	\N	\N	\N	\N
975	5	14	inches	10	inches	\N	retained	original	\N	1990-94	Dawson box 79 folder 1	1994	\N	\N	\N	\N
976	5	11	inches	8	inches	\N	retained	original	\N	1995-2009	Woodson box 32 folder 7	1995	0	\N	1933-04-04	1933-04-04
977	5	11	inches	8	inches	\N	retained	original	\N	1995-2009	Woodson box 32 folder 7	1996	\N	\N	1933-04-04	1933-04-04
978	5	11	inches	8	inches	\N	retained	original	\N	1995-2009	Woodson box 32 folder 7	1997	\N	\N	1933-04-04	1933-04-04
979	5	11	inches	8	inches	\N	retained	original	\N	1995-2009	Woodson box 32 folder 7	1998	\N	\N	1933-04-04	1933-04-04
980	5	11	inches	8	inches	\N	retained	original	\N	1995-2009	Woodson box 32 folder 7	1999	\N	\N	1933-04-04	1933-04-04
981	5	11	inches	8	inches	\N	retained	original	\N	1995-2009	Woodson box 32 folder 7	2000	\N	\N	1933-04-04	1933-04-04
982	5	11	inches	8	inches	\N	retained	original	\N	1995-2009	Woodson box 32 folder 7	2001	\N	\N	1933-04-04	1933-04-04
983	5	11	inches	8	inches	\N	retained	original	\N	1995-2009	Woodson box 32 folder 7	2002	\N	\N	1933-04-04	1933-04-04
984	5	11	inches	8	inches	\N	retained	original	\N	1995-2009	Woodson box 32 folder 7	2003	\N	\N	1933-04-04	1933-04-04
985	5	11	inches	8	inches	\N	retained	original	\N	1995-2009	Woodson box 32 folder 7	2004	\N	\N	1933-04-04	1933-04-04
986	5	11	inches	8	inches	\N	retained	original	\N	1995-2009	Woodson box 32 folder 7	2005	\N	\N	1933-04-04	1933-04-04
987	5	11	inches	8	inches	\N	retained	original	\N	1995-2009	Woodson box 32 folder 7	2006	\N	\N	1933-04-04	1933-04-04
988	5	11	inches	8	inches	\N	retained	original	\N	1995-2009	Woodson box 32 folder 7	2007	\N	\N	1933-04-04	1933-04-04
989	5	11	inches	8	inches	\N	retained	original	\N	1995-2009	Woodson box 32 folder 7	2008	\N	\N	1933-04-04	1933-04-04
990	5	11	inches	8	inches	\N	retained	original	\N	1995-2009	Woodson box 32 folder 7	2009	\N	\N	1933-04-04	1933-04-04
991	5	10	inches	7	inches	\N	retained	original	\N	\N	Dawson box 30 folder 2	2010	0	\N	1975-04-26	1975-04-26
992	5	10	inches	7	inches	\N	retained	original	\N	\N	Dawson box 30 folder 2	2011	\N	\N	1975-04-26	1975-04-26
993	0	0	inches	0	inches	\N	retained	\N	\N	\N	\N	14	0	\N	\N	\N
994	79	0	inches	0	inches	\N	retained	\N	\N	\N	\N	\N	0	\N	\N	\N
995	0	0	inches	0	inches	\N	retained	\N	\N	\N	\N	55	0	\N	\N	\N
996	0	0	inches	0	inches	\N		\N	\N	\N	\N	1842	0	\N	\N	\N
100	0	8.5	inches	5.5	inches	\N	retained	original	\N	\N	Series 5 Subject Files, Box 30, Folder 10	1079	0	\N	1983-12-26	\N
104	0	11	inches	8	inches	\N	retained	original	\N	\N	Series 5: Box 30, Folder 10	1083	0	\N	1985-05-09	\N
286	0	5.75	inches	3.5	inches	\N	retained	original	\N	\N	Box 32, Folder 7	1290	0	\N	0000-00-00	\N
287	0	11	inches	8.25	inches	\N	retained	original	\N	\N	Box 32, Folder 7	1291	0	\N	1934-01-09	\N
288	\N	5	inches	7	inches	\N	retained	original	\N	\N	Series 6: Box 40, Folder 4	1292	18	\N	1982-05-16	\N
344	0	6	inches	8	inches	\N	retained	original	\N	\N	Series 7: Box 42, Folder 15	1348	0	\N	1928-04-10	\N
345	0	6	inches	4	inches	\N	retained	original	\N	\N	Series 7: Box 42, Folder 16	1349	0	\N	1935-09-21	\N
346	0	7	inches	3.75	inches	\N	retained	original	\N	\N	Series 7: Box 42, Folder 22	1350	0	\N	1914-04-06	\N
347	0	6	inches	8.5	inches	\N	retained	original	\N	\N	Series 7: Box 42, Folder 23	1351	0	\N	1927-02-15	\N
348	0	8	inches	2	inches	\N	retained	original	\N	\N	Series 7: Box 43, Folder 24	1352	0	\N	1956-03-25	\N
55	0	11	inches	8	inches	\N	retained	original	\N	1035, 1036, 1037	Series 4 Writings by Dawson: Box 29, Folder 3	1034	0	\N	0000-00-00	\N
68	0	11	inches	8	inches	\N	retained	original	\N	1048, 1049, 1050, 1051, 1052, 1053, 1054, 1055, 1056, 1057, 1058	Series 4 Writings by Dawson: Box 29, Folder 4	1047	0	\N	0000-00-00	\N
69	0	11	inches	8	inches	\N	retained	original	\N	1047, 1049, 1050, 1051, 1052, 1053, 1054, 1055, 1056, 1057, 1058	Series 4 Writings by Dawson: Box 29, Folder 4	1048	0	\N	0000-00-00	\N
70	0	11	inches	8	inches	\N	retained	original	\N	1047, 1048, 1050, 1051, 1052, 1053, 1054, 1055, 1056, 1057, 1058	Series 4 Writings by Dawson: Box 29, Folder 4	1049	0	\N	0000-00-00	\N
71	0	11	inches	8	inches	\N	retained	original	\N	1047, 1048, 1049, 1051, 1052, 1053, 1054, 1055, 1056, 1057, 1058	Series 4 Writings by Dawson: Box 29, Folder 4	1050	0	\N	0000-00-00	\N
72	0	11	inches	8	inches	\N	retained	original	\N	1047, 1048, 1049, 1050, 1052, 1053, 1054, 1055, 1056, 1057, 1058	Series 4 Writings by Dawson: Box 29, Folder 4	1051	0	\N	0000-00-00	\N
73	0	11	inches	8	inches	\N	retained	original	\N	1047, 1048, 1049, 1050, 1051, 1053, 1054, 1055, 1056, 1057, 1058	Series 4 Writings by Dawson: Box 29, Folder 4	1052	0	\N	0000-00-00	\N
74	0	11	inches	8	inches	\N	retained	original	\N	1047, 1048, 1049, 1050, 1051, 1052, 1054, 1055, 1056, 1057, 1058	Series 4 Writings by Dawson: Box 29, Folder 4	1053	0	\N	0000-00-00	\N
75	0	11	inches	8	inches	\N	retained	original	\N	1047, 1048, 1049, 1050, 1051, 1052, 1053, 1055, 1056, 1057, 1058	Series 4 Writings by Dawson: Box 29, Folder 4	1054	0	\N	0000-00-00	\N
76	0	11	inches	8	inches	\N	retained	original	\N	1047, 1048, 1049, 1050, 1051, 1052, 1053, 1054, 1056, 1057, 1058	Series 4 Writings by Dawson: Box 29, Folder 4	1055	0	\N	0000-00-00	\N
77	0	11	inches	8	inches	\N	retained	original	\N	1047, 1048, 1049, 1050, 1051, 1052, 1053, 1054, 1055, 1057, 1058	Series 4 Writings by Dawson: Box 29, Folder 4	1056	0	\N	0000-00-00	\N
78	0	11	inches	8	inches	\N	retained	original	\N	1047, 1048, 1049, 1050, 1051, 1052, 1053, 1054, 1055, 1056, 1058	Series 4 Writings by Dawson: Box 29, Folder 4	1057	0	\N	0000-00-00	\N
79	0	11	inches	8	inches	\N	retained	original	\N	1047, 1048, 1049, 1050, 1051, 1052, 1053, 1054, 1055, 1056, 1057	Series 4 Writings by Dawson: Box 29, Folder 4	1058	0	\N	0000-00-00	\N
80	0	11	inches	8	inches	\N	retained	original	\N	1060, 1061, 1062, 1063, 1064, 1065	Series 4 Writings by Dawson: Box 29, Folder 6	1059	0	\N	1956-00-00	\N
81	0	11	inches	8	inches	\N	retained	original	\N	1059, 1061, 1062, 1063, 1064, 1065	Series 4 Writings by Dawson: Box 29, Folder 6	1060	0	\N	1956-00-00	\N
82	0	11	inches	8	inches	\N	retained	original	\N	1059, 1060, 1062, 1063, 1064, 1065	Series 4 Writings by Dawson: Box 29, Folder 6	1061	0	\N	1956-00-00	\N
83	0	11	inches	8	inches	\N	retained	original	\N	1059, 1060, 1061, 1063, 1064, 1065	Series 4 Writings by Dawson: Box 29, Folder 6	1062	0	\N	1956-00-00	\N
84	0	11	inches	8	inches	\N	retained	original	\N	1059, 1060, 1061, 1062, 1064, 1065	Series 4 Writings by Dawson: Box 29, Folder 6	1063	0	\N	1956-00-00	\N
85	0	11	inches	8	inches	\N	retained	original	\N	1059, 1060, 1061, 1062, 1063, 1065	Series 4 Writings by Dawson: Box 29, Folder 6	1064	0	\N	1956-00-00	\N
86	0	11	inches	8	inches	\N	retained	original	\N	1059, 1060, 1061, 1062, 1063, 1064	Series 4 Writings by Dawson: Box 29, Folder 6	1065	0	\N	1956-00-00	\N
87	0	11	inches	8	inches	\N	retained	original	\N	1067	Series 5 Subject Files: Box 30, Folder 1	1066	0	\N	1952-10-28	\N
88	0	11	inches	8	inches	\N	retained	original	\N	1066	Series 5 Subject Files: Box 30, Folder 1	1067	0	\N	1952-10-28	\N
90	0	11	inches	8	inches	\N	retained	original	\N	1070, 1071, 1072	Series 5 Subject Files: Box 30, Folder 3	1069	0	\N	1984-10-06	\N
92	0	11	inches	8	inches	\N	retained	original	\N	1069, 1070, 1072	Series 5 Subject Files: Box 30, Folder 3	1071	0	\N	1984-10-06	\N
93	0	11	inches	8	inches	\N	retained	original	\N	1069, 1070, 1071	Series 5 Subject Files: Box 30, Folder 3	1072	0	\N	1984-10-06	\N
91	0	11	inches	8	inches	\N	retained	original	\N	1069, 1071, 1072	Series 5 Subject Files: Box 30, Folder 3	1070	0	\N	1984-10-06	\N
122	0	8	inches	11	inches	\N	retained	original	\N	1112	Series 5 Subject Files: Box 30, Folder 12	1111	0	\N	1985-09-13	\N
123	0	8	inches	11	inches	\N	retained	original	\N	1111	Series 5 Subject Files: Box 30, Folder 12	1112	0	\N	1985-09-13	\N
127	0	11	inches	8	inches	\N	retained	original	\N	1117	Series 5 Subject Files: Box 30, Folder 16	1116	0	\N	1978-05-07	\N
128	0	11	inches	8	inches	\N	retained	original	\N	1116	Series 5 Subject Files: Box 30, Folder 16	1117	0	\N	1978-05-07	\N
149	0	11	inches	8	inches	\N	retained	original	\N	1139, 1140	Series 5 Subject Files: Box 31, Folder 5	1138	0	\N	1960-05-25	\N
150	0	11	inches	8	inches	\N	retained	original	\N	1138, 1140	Series 5 Subject Files: Box 31, Folder 5	1139	0	\N	1960-05-25	\N
151	0	11	inches	8	inches	\N	retained	original	\N	1138, 1139	Series 5 Subject Files: Box 31, Folder 5	1140	0	\N	1960-05-25	\N
172	0	11	inches	8	inches	\N	retained	original	\N	1170, 1172, 1173, 1174, 1175	Series 5 Subject Files: Box 31, Folder 12	1171	0	\N	1944-02-20	\N
173	0	11	inches	8	inches	\N	retained	original	\N	1170, 1171, 1173, 1174, 1175	Series 5 Subject Files: Box 31, Folder 12	1172	0	\N	1944-02-20	\N
174	0	11	inches	8	inches	\N	retained	original	\N	1170, 1171, 1172, 1174, 1175	Series 5 Subject Files: Box 31, Folder 12	1173	0	\N	1944-02-20	\N
175	0	11	inches	8	inches	\N	retained	original	\N	1170, 1171, 1172, 1173, 1175	Series 5 Subject Files: Box 31, Folder 12	1174	0	\N	1944-02-20	\N
176	0	11	inches	8	inches	\N	retained	original	\N	1170, 1171, 1172, 1173, 1174	Series 5 Subject Files: Box 31, Folder 12	1175	0	\N	1944-02-20	\N
177	0	11	inches	8	inches	\N	retained	original	\N	1177	Series 5 Subject Files: Box 31, Folder 12	1176	0	\N	1946-02-21	\N
181	0	11	inches	8	inches	\N	retained	original	\N	1179	Series 5 Subject Files: Box 31, Folder 12	1180	0	\N	1946-03-01	\N
180	0	11	inches	8	inches	\N	retained	original	\N	1180	Series 5 Subject Files: Box 31, Folder 12	1179	0	\N	1946-03-01	\N
182	0	11	inches	8	inches	\N	retained	original	\N	1182, 1183	Series 5 Subject Files: Box 31, Folder 12	1181	0	\N	1946-03-01	\N
183	0	11	inches	8	inches	\N	retained	original	\N	1181, 1183	Series 5 Subject Files: Box 31, Folder 12	1182	0	\N	1946-03-01	\N
184	0	11	inches	8	inches	\N	retained	original	\N	1181, 1182	Series 5 Subject Files: Box 31, Folder 12	1183	0	\N	1946-03-01	\N
185	0	11	inches	8	inches	\N	retained	original	\N	\N	Series 5: Box 31, Folder 13	1184	0	\N	1984-04-00	\N
186	0	11	inches	8	inches	\N	retained	original	\N	\N	Series 5: Box 31, Folder 13	1185	0	\N	1984-04-00	\N
189	0	11	inches	8	inches	\N	retained	original	\N	1189	Series 5 Subject Files: Box 31, Folder 14	1188	0	\N	1983-11-01	\N
188	0	11	inches	8	inches	\N	retained	original	\N	1186	Series 5: Box 31, Folder 14	1187	0	\N	1984-02-00	\N
187	0	11	inches	8	inches	\N	retained	original	\N	1187	Series 5: Box 31, Folder 14	1186	0	\N	1984-02-00	\N
194	0	11.75	inches	8	inches	\N	retained	original	\N	1194	Series 5: Box 31, Folder 15	1193	0	\N	0000-00-00	\N
195	0	11.75	inches	8	inches	\N	retained	original	\N	1193	Series 5: Box 31, Folder 15	1194	0	\N	0000-00-00	\N
196	0	9.75	inches	7.75	inches	\N	retained	original	\N	1196	Series 5: Box 31, Folder 15	1195	0	\N	1956-07-17	\N
197	0	9.75	inches	7.75	inches	\N	retained	original	\N	1195	Series 5: Box 31, Folder 15	1196	0	\N	1956-07-17	\N
198	0	10.75	inches	8.25	inches	\N	retained	original	\N	1198	See NN	1197	0	\N	0000-00-00	\N
199	0	10.75	inches	8.25	inches	\N	retained	original	\N	1197	See NN	1198	0	\N	0000-00-00	\N
200	0	11	inches	8	inches	\N	retained	original	\N	1200, 1201, 1202	Series 5 Subject Files: Box 31, Folder 16	1199	0	\N	1956-00-00	\N
201	0	11	inches	8	inches	\N	retained	original	\N	1199, 1201, 1202	Series 5 Subject Files: Box 31, Folder 16	1200	0	\N	1956-00-00	\N
202	0	11	inches	8	inches	\N	retained	original	\N	1199, 1200, 1202	Series 5 Subject Files: Box 31, Folder 16	1201	0	\N	1956-00-00	\N
203	0	11	inches	8	inches	\N	retained	original	\N	1199, 1200, 1201	Series 5 Subject Files: Box 31, Folder 16	1202	0	\N	1956-00-00	\N
204	0	11	inches	8	inches	\N	retained	original	\N	1204, 1205, 1206, 1207, 1208, 1209, 1210	Series 5 Subject Files: Box 32, Folder 4	1203	0	\N	1937-00-00	\N
205	0	11	inches	8	inches	\N	retained	original	\N	1203, 1205, 1206, 1207, 1208, 1209, 1210	Series 5 Subject Files: Box 32, Folder 4	1204	0	\N	1937-00-00	\N
206	0	11	inches	8	inches	\N	retained	original	\N	1203, 1204, 1206, 1207, 1208, 1209, 1210	Series 5 Subject Files: Box 32, Folder 4	1205	0	\N	1937-00-00	\N
207	0	11	inches	8	inches	\N	retained	original	\N	1203, 1204, 1205, 1207, 1208, 1209, 1210	Series 5 Subject Files: Box 32, Folder 4	1206	0	\N	1937-00-00	\N
208	0	11	inches	8	inches	\N	retained	original	\N	1203, 1204, 1205, 1206, 1208, 1209, 1210	Series 5 Subject Files: Box 32, Folder 4	1207	0	\N	1937-00-00	\N
209	0	11	inches	8	inches	\N	retained	original	\N	1203, 1204, 1205, 1206, 1207, 1209, 1210	Series 5 Subject Files: Box 32, Folder 4	1208	0	\N	1937-00-00	\N
210	0	11	inches	8	inches	\N	retained	original	\N	1203, 1204, 1205, 1206, 1207, 1208, 1210	Series 5 Subject Files: Box 32, Folder 4	1209	0	\N	1937-00-00	\N
211	0	11	inches	8	inches	\N	retained	original	\N	1203, 1204, 1205, 1206, 1207, 1208, 1209	Series 5 Subject Files: Box 32, Folder 4	1210	0	\N	1937-00-00	\N
273	0	4.5	inches	8.25	inches	\N	retained	original	\N	1278	Series 5: Box 32, Folder 5	1277	0	\N	1955-03-19	\N
274	0	5	inches	8.25	inches	\N	retained	original	\N	1277	Series 5 Subject Files: Box 32, Folder 5	1278	0	\N	1955-03-09	\N
276	0	11	inches	8	inches	\N	retained	original	\N	1279	Series 5 Subject Files: Box 32, Folder 5	1280	0	\N	1955-03-16	\N
275	0	11	inches	8	inches	\N	retained	original	\N	1280	Series 5 Subject Files: Box 32, Folder 5	1279	0	\N	1955-03-16	\N
278	0	11	inches	8	inches	\N	retained	original	\N	1281, 1283, 1284, 1285	Series 5 Subject Files: Box 32, Folder 5	1282	0	\N	1951-12-23	\N
277	0	11	inches	8	inches	\N	retained	original	\N	1282, 1283, 1284, 1285	Series 5 Subject Files: Box 32, Folder 5	1281	0	\N	1951-12-23	\N
279	0	11	inches	8	inches	\N	retained	original	\N	1281, 1282, 1284, 1285	Series 5 Subject Files: Box 32, Folder 5	1283	0	\N	1951-12-23	\N
280	0	11	inches	8	inches	\N	retained	original	\N	1281, 1282, 1283, 1285	Series 5 Subject Files: Box 32, Folder 5	1284	0	\N	1951-12-23	\N
281	0	11	inches	8	inches	\N	retained	original	\N	1281, 1282, 1283, 1284	Series 5 Subject Files: Box 32, Folder 5	1285	0	\N	1951-12-23	\N
289	0	5.1500000000000004	inches	5.25	inches	\N	retained	original	\N	1294, 1295, 1296, 1297, 1298, 1299, 1300, 1301, 1302, 1303, 1304, 1305	Series 6: Box 41, Folder 1	1293	0	\N	1918-00-00	\N
290	0	5.25	inches	5.1500000000000004	inches	\N	retained	negative	\N	1293, 1295, 1296, 1297, 1298, 1299, 1300, 1301, 1302, 1303, 1304, 1305	Series 6: Box 41, Folder 1	1294	0	\N	1918-00-00	\N
291	0	5.25	inches	5.1500000000000004	inches	\N	retained	original	\N	1293, 1294, 1296, 1297, 1298, 1299, 1300, 1301, 1302, 1303, 1304, 1305	Series 6: Box 41, Folder 1	1295	0	\N	1918-00-00	\N
292	0	5.25	inches	5.1500000000000004	inches	\N	retained	original	\N	1293, 1294, 1295, 1297, 1298, 1299, 1300, 1301, 1302, 1303, 1304, 1305	Series 6: Box 41, Folder 1	1296	0	\N	1918-00-00	\N
293	0	3	inches	5.1500000000000004	inches	\N	retained	original	\N	1293, 1294, 1295, 1296, 1298, 1299, 1300, 1301, 1302, 1303, 1304, 1305	Series 6: Box 41, Folder 1	1297	0	\N	1918-00-00	\N
295	0	5.25	inches	5.1500000000000004	inches	\N	retained	original	\N	1293, 1294, 1295, 1296, 1297, 1298, 1300, 1301, 1302, 1303, 1304, 1305	Series 6: Box 41, Folder 1	1299	0	\N	1918-00-00	\N
294	0	3	inches	5.1500000000000004	inches	\N	retained	original	\N	1293, 1294, 1295, 1296, 1297, 1299, 1300, 1301, 1302, 1303, 1304, 1305	Series 6: Box 41, Folder 1	1298	0	\N	1918-00-00	\N
296	0	5.25	inches	5.1500000000000004	inches	\N	retained	original	\N	1293, 1294, 1295, 1296, 1297, 1298, 1299, 1301, 1302, 1303, 1304, 1305	Series 6: Box 41, Folder 1	1300	0	\N	1918-00-00	\N
297	0	5.25	inches	5.1500000000000004	inches	\N	retained	original	\N	1293, 1294, 1295, 1296, 1297, 1298, 1299, 1300, 1302, 1303, 1304, 1305	Series 6: Box 41, Folder 1	1301	0	\N	1918-00-00	\N
298	0	5.25	inches	5.1500000000000004	inches	\N	retained	original	\N	1293, 1294, 1295, 1296, 1297, 1298, 1299, 1300, 1301, 1303, 1304, 1305	Series 6: Box 41, Folder 1	1302	0	\N	1918-00-00	\N
299	0	5.25	inches	5.1500000000000004	inches	\N	retained	original	\N	1293, 1294, 1295, 1296, 1297, 1298, 1299, 1300, 1301, 1302, 1304, 1305	Series 6: Box 41, Folder 1	1303	0	\N	1918-00-00	\N
300	0	5.25	inches	5.1500000000000004	inches	\N	retained	original	\N	1293, 1294, 1295, 1296, 1297, 1298, 1299, 1300, 1301, 1302, 1303, 1305	Series 6: Box 41, Folder 1	1304	0	\N	1918-00-00	\N
574	0	12	inches	8	inches	\N	retained	original	\N	\N	Woodson PR4845 K54 .A37 1875	1592	0	\N	1875-00-00	\N
2001	0	0	inches	0	inches	\N	retained	\N	\N	\N	Box 2, Folder 3	2034	0	\N	1964-00-00	\N
2002	0	0	inches	0	inches	\N	retained	\N	\N	\N	Box 2, Folder 4	2030	0	\N	1964-00-00	\N
2003	0	0	inches	0	inches	\N	retained	\N	\N	\N	Box 2, Folder 4	2033	0	\N	1980-08-23	\N
2004	0	0	inches	0	inches	\N	retained	\N	\N	\N	Box 2, Folder 6	2035	0	\N	1988-01-16	\N
2005	0	0	inches	0	inches	\N	retained	\N	Date of Source Item:  Full date is known, but is over a range of days (1986-01-04 through 1986-01-19).	\N	Box 31, Folder 11	\N	0	\N	1986-01-00	\N
2006	0	0	inches	0	inches	\N	retained	\N	Date of Source Item:  Full date is known, but it covers a range of days (1986-01-04 through 1986-01-19).	\N	Box 31, Folder 11	2036	0	\N	1986-01-00	\N
2007	0	0	inches	0	inches	\N	retained	\N	\N	\N	uncataloged Woodson Library	2073	0	\N	1996-00-00	1996-00-00
2009	0	0	inches	0	inches	\N	retained	\N	\N	2075	Box 31, Folder 12	2076	0	\N	1986-02-09	\N
2008	0	0	inches	0	inches	\N	retained	\N	\N	2076	Box 31, Folder 12	2075	0	\N	1986-02-09	\N
2011	0	0	inches	0	inches	\N	retained	\N	\N	2078	Box 24, Folder 24	2079	0	\N	0000-00-00	\N
2010	0	0	inches	0	inches	\N	retained	\N	\N	2079	Box 24, Folder 24	2078	0	\N	0000-00-00	\N
2012	0	0	inches	0	inches	\N	retained	\N	Date of Source Item:  Full date is known, but covers a range of days (1966-04-22 through 1966-04-24).	\N	Box 26, Folder 9	2102	0	\N	1966-04-00	\N
2013	0	0	inches	0	inches	\N	retained	\N	\N	\N	Box 23, Folder 15	2109	0	\N	0000-00-00	\N
2015	0	0	inches	0	inches	\N	retained	\N	\N	2110	Box 23, Folder 19	2111	0	\N	0000-00-00	\N
2014	0	0	inches	0	inches	\N	retained	\N	\N	2111	Box 23, Folder 19	2110	0	\N	0000-00-00	\N
2016	0	8	inches	5	inches	\N	retained	original	\N	2115; 2116	Box 6, Folder 5	2112	0	\N	1931-00-00	1989-00-00
2017	0	8	inches	5	inches	\N	retained	original	\N	2112; 2116	Box 6, Folder 5	2115	0	\N	1931-00-00	1989-00-00
2018	0	12	inches	9	inches	\N	retained	original	\N	2112; 2115	Box 6, Folder 5	2116	0	\N	1931-00-00	1989-00-00
2019	0	9	inches	6	inches	\N	retained	original	\N	2120; 2122; 2123	BT734.2 .R38 1969	2118	0	\N	1969-06-08	\N
2020	0	9	inches	6	inches	\N	retained	original	\N	2118; 2122; 2123	BT734.2 .R38 1969	2120	0	\N	1969-06-08	\N
2021	0	9	inches	6	inches	\N	retained	original	\N	2118; 2120; 2123	BT734.2 .R38 1969	2122	0	\N	1969-06-08	\N
2022	0	9	inches	6	inches	\N	retained	original	\N	2118; 2120; 2122	BT734.2 .R38 1969	2123	0	\N	1969-06-08	\N
2023	0	8	inches	5	inches	\N	retained	original	\N	\N	WOODSON G560 T33 1801	2124	0	\N	1800-08-00	\N
\.


--
-- Data for TOC entry 238 (OID 12745562)
-- Name: SourceMovingImage; Type: TABLE DATA; Schema: public; Owner: jbwhite
--

COPY "SourceMovingImage" ("ID", "Form", "Disposition", "Generation", "Length", "SourceNote", "SoundField", "Stock", "RelatedItem", "ItemLocation", "Duration", "Content#", "HousingDescriptionFilm", "Color", "Polarity", "Base", "Viewable", "Dirty", "Scratched", "Warped", "Sticky", "Faded", "VinegarSyndrome", "ADStrip", "ADStripDate", "ADStripReplaceDate", "ConservationHistory", "SourceDate", "PublicationDate") FROM stdin;
\.


--
-- Data for TOC entry 239 (OID 12745581)
-- Name: Speed; Type: TABLE DATA; Schema: public; Owner: jbwhite
--

COPY "Speed" ("ID", "Speed", "SpeedAlt", "FormatType") FROM stdin;
1	1 7/8	1 7/8 ips, 4.75 cm/s	Tape
2	120	120 rpm	Disc
3	15	15 ips, 38.1 cm/s	Tape
4	15/16	15/16 ips, 2.38 cm/s	Tape
5	15/32	15/32 ips, 1.19 cm/s	Tape
6	16	16 Frames per second	Nitrate
7	16	16 Frames per second	Acetate
8	16	16 Frames per second	Video
9	16/18	Frames per second	Video
10	16/18/24/25	Frames per second	Video
11	16/24	Frames per second	Video
12	16/25	Frames per second	Video
13	18	18 Frames per second	Nitrate
14	18	18 Frames per second	Acetate
15	18	18 Frames per second	Video
16	18/24	Frames per second	Video
17	18/24/25	Frames per second	Video
18	18/25	Frames per second	Video
19	24	24 Frames per second	Nitrate
20	24	24 Frames per second	Acetate
21	24	24 Frames per second	Video
22	24/25	Frames per second	Video
23	25	25 Frames per second	Nitrate
24	25	25 Frames per second	Acetate
25	25	25 Frames per second	Video
26	3 3/4	3 3/4 ips, 9.5 cm/s	Tape
27	30	30 ips, 76.2cm/s	Tape
28	32	32 Kilohertz	Disc
29	33	33 1/3 rpm	Disc
30	44.1	44.1 Kilohertz	Disc
31	45	45 rpm	Disc
32	48	48 Kilohertz	Disc
33	7.5	7.5 ips, 19.05 cm/s	Tape
34	78	78 rpm	Disc
35	M	Multiple	Tape
36	O	Other	Tape
37	SI	Silent (Standard Release)	Acetate
38	SI	Silent (Standard Release)	Nitrate
39	V	Varying	\N
\.


--
-- Data for TOC entry 240 (OID 12745630)
-- Name: SourceSound; Type: TABLE DATA; Schema: public; Owner: jbwhite
--

COPY "SourceSound" ("ID", "Form", "ReelSize", "DimensionNote", "Disposition", "Gauge", "Generation", "Length", "SourceNote", "SoundField", "Speed", "Stock", "TapeThick", "TrackFormat", "RelatedItem", "ItemLocation", "Content#", "Housing", "ConservationHistory", "SourceDate", "PublicationDate", "TransferEngineer") FROM stdin;
32	14	\N	\N	retained	\N	\N	\N	test	\N	0	\N	\N	\N	\N	\N	1	0	\N	1971-04-16	\N	\N
33	14	\N	\N	retained	\N	\N	\N	\N	\N	0	\N	\N	\N	2	\N	2	0	\N	1971-05-13	\N	\N
34	14	\N	\N	retained	\N	\N	\N	\N	\N	0	\N	\N	\N	3	\N	3	0	\N	1971-05-13	\N	\N
35	14	\N	\N	retained	\N	\N	\N	\N	\N	0	\N	\N	\N	5	\N	4	0	\N	1971-12-04	\N	\N
36	14	\N	\N	retained	\N	\N	\N	\N	\N	0	\N	\N	\N	4	\N	5	0	\N	1971-12-04	\N	\N
37	14	\N	\N	retained	\N	\N	\N	\N	\N	0	\N	\N	\N	7	\N	6	0	\N	\N	\N	\N
38	14	\N	\N	retained	\N	\N	\N	\N	\N	0	\N	\N	\N	6	\N	7	0	\N	\N	\N	\N
39	14	\N	\N	retained	\N	\N	\N	\N	\N	0	\N	\N	\N	9, 10	\N	8	0	\N	1974-03-09	\N	\N
40	14	\N	\N	retained	\N	\N	\N	\N	\N	0	\N	\N	\N	8, 10	\N	9	0	\N	1974-03-09	\N	\N
41	14	\N	\N	retained	\N	\N	\N	\N	\N	0	\N	\N	\N	8, 9	\N	10	0	\N	1974-03-09	\N	\N
42	14	\N	\N	retained	\N	\N	\N	\N	\N	0	\N	\N	\N	\N	\N	11	0	\N	1976-03-20	\N	\N
43	14	\N	\N	retained	\N	\N	\N	\N	\N	0	\N	\N	\N	13	\N	12	0	\N	1979-03-12	\N	\N
44	14	\N	\N	retained	\N	\N	\N	\N	\N	0	\N	\N	\N	12	\N	13	0	\N	1979-03-12	\N	\N
45	14	\N	\N	retained	\N	\N	\N	\N	\N	0	\N	\N	\N	Related files: 00000034-00000035	\N	14	0	\N	\N	\N	\N
46	14	\N	\N	retained	\N	\N	\N	\N	\N	0	\N	\N	\N	Related files: 00000034-00000035	\N	15	0	\N	\N	\N	\N
47	14	\N	\N	retained	\N	\N	\N	\N	\N	0	\N	\N	\N	\N	\N	16	0	\N	\N	\N	\N
48	14	\N	\N	retained	\N	\N	\N	\N	\N	0	\N	\N	\N	\N	\N	17	0	\N	\N	\N	\N
49	14	\N	\N	retained	\N	\N	\N	\N	\N	0	\N	\N	\N	Related files: 00000038-00000039	\N	18	0	\N	\N	\N	\N
50	14	\N	\N	retained	\N	\N	\N	\N	\N	0	\N	\N	\N	Related files: 00000038-00000039	\N	19	0	\N	\N	\N	\N
51	14	\N	\N	retained	\N	\N	\N	\N	\N	0	\N	\N	\N	\N	\N	20	0	\N	\N	\N	\N
52	14	\N	\N	retained	\N	\N	\N	\N	\N	0	\N	\N	\N	Related file: 00000042	\N	21	0	\N	\N	\N	\N
53	14	\N	\N	retained	\N	\N	\N	\N	\N	0	\N	\N	\N	Related file: 00000041	\N	22	0	\N	\N	\N	\N
54	14	\N	\N	retained	\N	\N	\N	\N	\N	0	\N	\N	\N	\N	\N	23	0	\N	\N	\N	\N
55	14	\N	\N	retained	\N	\N	\N	\N	\N	0	\N	\N	\N	Related files: 00000044-00000045.	\N	24	0	\N	\N	\N	\N
56	14	\N	\N	retained	\N	\N	\N	\N	\N	0	\N	\N	\N	Related files: 00000044-00000045.	\N	25	0	\N	\N	\N	\N
57	14	\N	\N	retained	\N	\N	\N	\N	\N	0	\N	\N	\N	Related file: 00000047	\N	26	0	\N	\N	\N	\N
58	14	\N	\N	retained	\N	\N	\N	\N	\N	0	\N	\N	\N	Related file: 00000046	\N	27	0	\N	\N	\N	\N
59	14	\N	\N	retained	\N	\N	\N	\N	\N	0	\N	\N	\N	\N	\N	28	0	\N	\N	\N	\N
60	14	\N	\N	retained	\N	\N	\N	\N	\N	0	\N	\N	\N	Related files: 00000049-00000050	\N	29	0	\N	\N	\N	\N
61	14	\N	\N	retained	\N	\N	\N	\N	\N	0	\N	\N	\N	Related files: 00000049-00000050	\N	30	0	\N	\N	\N	\N
62	14	\N	\N	retained	\N	\N	\N	\N	\N	0	\N	\N	\N	\N	\N	31	0	\N	\N	\N	\N
63	14	\N	\N	retained	\N	\N	\N	\N	\N	0	\N	\N	\N	Related files: 00000052-00000053	\N	32	0	\N	\N	\N	\N
64	14	\N	\N	retained	\N	\N	\N	\N	\N	0	\N	\N	\N	Related files: 00000052-00000053	\N	33	0	\N	\N	\N	\N
65	15	\N	\N	retained	\N	\N	\N	\N	\N	0	\N	\N	\N	Related files: 00000054-00000055	\N	34	0	\N	\N	\N	\N
66	15	\N	\N	retained	\N	\N	\N	\N	\N	0	\N	\N	\N	Related files: 00000054-00000055	\N	35	0	\N	\N	\N	\N
67	15	\N	\N	retained	\N	\N	\N	\N	\N	0	\N	\N	\N	Related files: 00000056-00000057	\N	36	0	\N	\N	\N	\N
68	15	\N	\N	retained	\N	\N	\N	\N	\N	0	\N	\N	\N	Related files: 00000056-00000057	\N	37	0	\N	\N	\N	\N
69	15	\N	\N	retained	\N	\N	\N	\N	\N	0	\N	\N	\N	\N	\N	38	0	\N	\N	\N	\N
70	15	\N	\N	retained	\N	\N	\N	\N	\N	0	\N	\N	\N	\N	\N	39	0	\N	\N	\N	\N
71	15	\N	\N	retained	\N	\N	\N	\N	\N	0	\N	\N	\N	\N	\N	40	0	\N	\N	\N	\N
72	15	\N	\N	retained	\N	\N	\N	\N	\N	0	\N	\N	\N	\N	\N	41	0	\N	\N	\N	\N
73	15	\N	\N	retained	\N	\N	\N	\N	\N	0	\N	\N	\N	\N	\N	42	0	\N	\N	\N	\N
74	15	\N	\N	retained	\N	\N	\N	\N	\N	0	\N	\N	\N	\N	\N	43	0	\N	\N	\N	\N
75	14	\N	\N	retained	\N	\N	\N	\N	\N	0	\N	\N	\N	Related file: 00000065	\N	44	0	\N	\N	\N	\N
76	14	\N	\N	retained	\N	\N	\N	\N	\N	0	\N	\N	\N	Related file: 00000064	\N	45	0	\N	\N	\N	\N
77	14	\N	\N	retained	\N	\N	\N	\N	\N	0	\N	\N	\N	Related file: 00000067	\N	46	0	\N	\N	\N	\N
78	14	\N	\N	retained	\N	\N	\N	\N	\N	0	\N	\N	\N	Related file: 00000066	\N	47	0	\N	\N	\N	\N
79	14	\N	\N	retained	\N	\N	\N	\N	\N	0	\N	\N	\N	Related files: 00000068, 00000263-00000264	\N	48	0	\N	\N	\N	\N
80	14	\N	\N	retained	\N	\N	\N	\N	\N	0	\N	\N	\N	Related files: 00000070-00000076	\N	49	0	\N	\N	\N	\N
81	14	\N	\N	retained	\N	\N	\N	\N	\N	0	\N	\N	\N	Related files: 00000070-00000076	\N	50	0	\N	\N	\N	\N
82	14	\N	\N	retained	\N	\N	\N	\N	\N	0	\N	\N	\N	Related files: 00000070-00000076	\N	51	0	\N	\N	\N	\N
83	14	\N	\N	retained	\N	\N	\N	\N	\N	0	\N	\N	\N	Related files: 00000070-00000076	\N	52	0	\N	\N	\N	\N
84	14	\N	\N	retained	\N	\N	\N	\N	\N	0	\N	\N	\N	Related files: 00000070- 00000076	\N	53	0	\N	\N	\N	\N
85	14	\N	\N	retained	\N	\N	\N	\N	\N	0	\N	\N	\N	Related files: 00000070-00000076	\N	54	0	\N	\N	\N	\N
86	14	\N	\N	retained	\N	\N	\N	\N	\N	0	\N	\N	\N	Related files: 00000070-00000076	\N	55	0	\N	\N	\N	\N
87	14	\N	\N	retained	\N	\N	\N	\N	\N	0	\N	\N	\N	Related files: 00000077-00000082	\N	56	0	\N	\N	\N	\N
88	14	\N	\N	retained	\N	\N	\N	\N	\N	0	\N	\N	\N	Related files: 00000077-00000082	\N	57	0	\N	\N	\N	\N
89	14	\N	\N	retained	\N	\N	\N	\N	\N	0	\N	\N	\N	Related files: 00000077-00000082	\N	58	0	\N	\N	\N	\N
90	14	\N	\N	retained	\N	\N	\N	\N	\N	0	\N	\N	\N	Related files: 00000077-00000082	\N	59	0	\N	\N	\N	\N
91	14	\N	\N	retained	\N	\N	\N	\N	\N	0	\N	\N	\N	Related files: 00000077-00000082	\N	60	0	\N	\N	\N	\N
92	14	\N	\N	retained	\N	\N	\N	\N	\N	0	\N	\N	\N	Related files: 00000077-00000082	\N	61	0	\N	\N	\N	\N
93	14	\N	\N	retained	\N	\N	\N	\N	\N	0	\N	\N	\N	00000083-00000084	\N	62	0	\N	\N	\N	\N
94	14	\N	\N	retained	\N	\N	\N	\N	\N	0	\N	\N	\N	00000083-00000084	\N	63	0	\N	\N	\N	\N
95	14	\N	\N	retained	\N	\N	\N	\N	\N	0	\N	\N	\N	Related files: 00000085-00000090	\N	64	0	\N	\N	\N	\N
96	14	\N	\N	retained	\N	\N	\N	\N	\N	0	\N	\N	\N	Related files: 00000085-00000090	\N	65	0	\N	\N	\N	\N
97	14	\N	\N	retained	\N	\N	\N	\N	\N	0	\N	\N	\N	Related files: 00000085-00000090	\N	66	0	\N	\N	\N	\N
98	14	\N	\N	retained	\N	\N	\N	\N	\N	0	\N	\N	\N	Related files: 00000085-00000090	\N	67	0	\N	\N	\N	\N
99	14	\N	\N	retained	\N	\N	\N	\N	\N	0	\N	\N	\N	Related files: 00000085-00000090	\N	68	0	\N	\N	\N	\N
100	14	\N	\N	retained	\N	\N	\N	\N	\N	0	\N	\N	\N	Related files: 00000085-00000090	\N	69	0	\N	\N	\N	\N
101	14	\N	\N	retained	\N	\N	\N	\N	\N	0	\N	\N	\N	Related files: 00000091-00000092.	\N	70	0	\N	\N	\N	\N
102	14	\N	\N	retained	\N	\N	\N	\N	\N	0	\N	\N	\N	Related files: 00000091-00000092.	\N	71	0	\N	\N	\N	\N
103	14	\N	\N	retained	\N	\N	\N	\N	\N	0	\N	\N	\N	Related files: 00000093-00000094, 00000099-00000100.	\N	72	0	\N	\N	\N	\N
104	14	\N	\N	retained	\N	\N	\N	\N	\N	0	\N	\N	\N	Related files: 00000093-00000094, 00000099-00000100.	\N	73	0	\N	\N	\N	\N
105	14	\N	\N	retained	\N	\N	\N	\N	\N	0	\N	\N	\N	Related files: 00000095-00000098	\N	74	0	\N	\N	\N	\N
106	14	\N	\N	retained	\N	\N	\N	\N	\N	0	\N	\N	\N	Related files: 00000095-00000098	\N	75	0	\N	\N	\N	\N
107	14	\N	\N	retained	\N	\N	\N	\N	\N	0	\N	\N	\N	Related files: 00000095-00000098	\N	76	0	\N	\N	\N	\N
108	14	\N	\N	retained	\N	\N	\N	\N	\N	0	\N	\N	\N	Related files: 00000095-00000098	\N	77	0	\N	\N	\N	\N
109	14	\N	\N	retained	\N	\N	\N	\N	\N	0	\N	\N	\N	Related files: 00000093-00000094, 00000099-00000100.	\N	78	0	\N	\N	\N	\N
110	14	\N	\N	retained	\N	\N	\N	\N	\N	0	\N	\N	\N	Related files: 00000093-00000094, 00000099-00000100.	\N	79	0	\N	\N	\N	\N
111	14	\N	\N	retained	\N	\N	\N	\N	\N	0	\N	\N	\N	\N	\N	80	0	\N	\N	\N	\N
112	14	\N	\N	retained	\N	\N	\N	\N	\N	0	\N	\N	\N	\N	\N	81	0	\N	\N	\N	\N
113	14	\N	\N	retained	\N	\N	\N	\N	\N	0	\N	\N	\N	Related files: 00000103-00000104, 00000637.	\N	82	0	\N	\N	\N	\N
114	14	\N	\N	retained	\N	\N	\N	\N	\N	0	\N	\N	\N	Related files: 00000103-00000104, 00000637.	\N	83	0	\N	\N	\N	\N
115	15	\N	\N	retained	\N	\N	\N	\N	\N	0	\N	\N	\N	Related files: 00000105.wav - 00000106.wav	\N	84	0	\N	\N	\N	\N
116	15	\N	\N	retained	\N	\N	\N	\N	\N	0	\N	\N	\N	Related files: 00000105.wav - 00000106.wav.	\N	85	0	\N	\N	\N	\N
117	15	\N	\N	retained	\N	\N	\N	\N	\N	0	\N	\N	\N	Related files: 00000107.wav - 00000108.wav	\N	86	0	\N	\N	\N	\N
118	15	\N	\N	retained	\N	\N	\N	\N	\N	0	\N	\N	\N	Related files: 00000107.wav - 00000108.wav	\N	87	0	\N	\N	\N	\N
119	15	\N	\N	retained	\N	\N	\N	\N	\N	0	\N	\N	\N	\N	\N	88	0	\N	\N	\N	\N
120	15	\N	\N	retained	\N	\N	\N	\N	\N	0	\N	\N	\N	\N	\N	89	0	\N	\N	\N	\N
121	11	\N	\N	retained	\N	\N	\N	\N	\N	0	\N	\N	\N	Related files: 00000112-00000115	\N	90	0	\N	\N	\N	\N
122	11	\N	\N	retained	\N	\N	\N	\N	\N	0	\N	\N	\N	Related files: 00000112-00000115	\N	91	0	\N	\N	\N	\N
123	11	\N	\N	retained	\N	\N	\N	\N	\N	0	\N	\N	\N	Related files: 00000112-00000115	\N	92	0	\N	\N	\N	\N
124	11	\N	\N	retained	\N	\N	\N	\N	\N	0	\N	\N	\N	Related files: 00000112-00000115	\N	93	0	\N	\N	\N	\N
125	11	\N	\N	retained	\N	\N	\N	\N	\N	0	\N	\N	\N	Related files: 00000116-00000119	\N	94	0	\N	\N	\N	\N
126	11	\N	\N	retained	\N	\N	\N	\N	\N	0	\N	\N	\N	Related files: 00000116-00000119	\N	95	0	\N	\N	\N	\N
127	11	\N	\N	retained	\N	\N	\N	\N	\N	0	\N	\N	\N	Related files: 00000116-00000119	\N	96	0	\N	\N	\N	\N
128	11	\N	\N	retained	\N	\N	\N	\N	\N	0	\N	\N	\N	Related files: 00000116-00000119	\N	97	0	\N	\N	\N	\N
129	11	\N	\N	retained	\N	\N	\N	\N	\N	0	\N	\N	\N	Related files: 00000120-00000123	\N	98	0	\N	\N	\N	\N
130	11	\N	\N	retained	\N	\N	\N	\N	\N	0	\N	\N	\N	Related files: 00000120-00000123	\N	99	0	\N	\N	\N	\N
131	11	\N	\N	retained	\N	\N	\N	\N	\N	0	\N	\N	\N	Related files: 00000120-00000123	\N	100	0	\N	\N	\N	\N
132	11	\N	\N	retained	\N	\N	\N	\N	\N	0	\N	\N	\N	Related files: 00000120-00000123	\N	101	0	\N	\N	\N	\N
133	11	\N	\N	retained	\N	\N	\N	\N	\N	0	\N	\N	\N	Related files: 00000124-00000125	\N	102	0	\N	\N	\N	\N
134	11	\N	\N	retained	\N	\N	\N	\N	\N	0	\N	\N	\N	Related files: 00000124-00000125	\N	103	0	\N	\N	\N	\N
135	11	\N	\N	retained	\N	\N	\N	\N	\N	0	\N	\N	\N	Related files: 00000126-00000133	\N	104	0	\N	\N	\N	\N
136	11	\N	\N	retained	\N	\N	\N	\N	\N	0	\N	\N	\N	Related files: 00000126-00000133	\N	105	0	\N	\N	\N	\N
137	11	\N	\N	retained	\N	\N	\N	\N	\N	0	\N	\N	\N	Related files: 00000126-00000133	\N	106	0	\N	\N	\N	\N
138	11	\N	\N	retained	\N	\N	\N	\N	\N	0	\N	\N	\N	Related files: 00000126-00000133	\N	107	0	\N	\N	\N	\N
139	11	\N	\N	retained	\N	\N	\N	\N	\N	0	\N	\N	\N	Related files: 00000126-00000133	\N	108	0	\N	\N	\N	\N
140	11	\N	\N	retained	\N	\N	\N	\N	\N	0	\N	\N	\N	Related files: 00000126-00000133	\N	109	0	\N	\N	\N	\N
141	11	\N	\N	retained	\N	\N	\N	\N	\N	0	\N	\N	\N	Related files: 00000126-00000133	\N	110	0	\N	\N	\N	\N
142	11	\N	\N	retained	\N	\N	\N	\N	\N	0	\N	\N	\N	Related files: 00000126-00000133	\N	111	0	\N	\N	\N	\N
143	11	\N	\N	retained	\N	\N	\N	\N	\N	0	\N	\N	\N	\N	\N	112	0	\N	\N	\N	\N
144	11	\N	\N	retained	\N	\N	\N	\N	\N	0	\N	\N	\N	\N	\N	113	0	\N	\N	\N	\N
145	11	\N	\N	retained	\N	\N	\N	\N	\N	0	\N	\N	\N	Related files: 00000136-00000139	\N	114	0	\N	\N	\N	\N
146	11	\N	\N	retained	\N	\N	\N	\N	\N	0	\N	\N	\N	Related files: 00000136-00000139	\N	115	0	\N	\N	\N	\N
147	11	\N	\N	retained	\N	\N	\N	\N	\N	0	\N	\N	\N	Related files: 00000136-00000139	\N	116	0	\N	\N	\N	\N
148	11	\N	\N	retained	\N	\N	\N	\N	\N	0	\N	\N	\N	Related files: 00000136-00000139	\N	117	0	\N	\N	\N	\N
149	11	\N	\N	retained	\N	\N	\N	\N	\N	0	\N	\N	\N	Related files: 00000140-00000141	\N	118	0	\N	\N	\N	\N
150	11	\N	\N	retained	\N	\N	\N	\N	\N	0	\N	\N	\N	Related files: 00000140-00000141	\N	119	0	\N	\N	\N	\N
151	12	\N	\N	retained	\N	\N	\N	\N	\N	0	\N	\N	\N	\N	\N	120	0	\N	\N	\N	\N
152	13	\N	\N	retained	\N	\N	\N	\N	\N	0	\N	\N	\N	Related files: 00000143-00000144	\N	121	0	\N	\N	\N	\N
153	13	\N	\N	retained	\N	\N	\N	\N	\N	0	\N	\N	\N	Related files: 00000143-00000144	\N	122	0	\N	\N	\N	\N
154	11	\N	\N	retained	\N	\N	\N	\N	\N	0	\N	\N	\N	Related files: 00000145-00000146	\N	123	0	\N	\N	\N	\N
155	11	\N	\N	retained	\N	\N	\N	\N	\N	0	\N	\N	\N	Related files: 00000145-00000146	\N	124	0	\N	\N	\N	\N
156	11	\N	\N	retained	\N	\N	\N	\N	\N	0	\N	\N	\N	Related files: 00000147-00000148	\N	125	0	\N	\N	\N	\N
157	11	\N	\N	retained	\N	\N	\N	\N	\N	0	\N	\N	\N	Related files: 00000147-00000148	\N	126	0	\N	\N	\N	\N
158	11	\N	\N	retained	\N	\N	\N	\N	\N	0	\N	\N	\N	Related files: 00000149-00000150	\N	127	0	\N	\N	\N	\N
159	11	\N	\N	retained	\N	\N	\N	\N	\N	0	\N	\N	\N	Related files: 00000149-00000150	\N	128	0	\N	\N	\N	\N
160	11	\N	\N	retained	\N	\N	\N	\N	\N	0	\N	\N	\N	Related files: 00000151-00000152	\N	129	0	\N	\N	\N	\N
161	11	\N	\N	retained	\N	\N	\N	\N	\N	0	\N	\N	\N	Related files: 00000151-00000152	\N	130	0	\N	\N	\N	\N
162	11	\N	\N	retained	\N	\N	\N	\N	\N	0	\N	\N	\N	Related files: 00000153-00000154	\N	131	0	\N	\N	\N	\N
163	11	\N	\N	retained	\N	\N	\N	\N	\N	0	\N	\N	\N	Related files: 00000153-00000154	\N	132	0	\N	\N	\N	\N
164	11	\N	\N	retained	\N	\N	\N	\N	\N	0	\N	\N	\N	\N	\N	133	0	\N	\N	\N	\N
165	11	\N	\N	retained	\N	\N	\N	\N	\N	0	\N	\N	\N	\N	\N	134	0	\N	\N	\N	\N
166	11	\N	\N	retained	\N	\N	\N	\N	\N	0	\N	\N	\N	10" disk; Related files: 00000157-00000158	\N	135	0	\N	\N	\N	\N
167	11	\N	\N	retained	\N	\N	\N	\N	\N	0	\N	\N	\N	10" disk; Related files: 00000157-00000158	\N	136	0	\N	\N	\N	\N
168	11	\N	\N	retained	\N	\N	\N	\N	\N	0	\N	\N	\N	Cardboard disk; Related files: 00000159-00000160	\N	137	0	\N	\N	\N	\N
169	11	\N	\N	retained	\N	\N	\N	\N	\N	0	\N	\N	\N	Cardboard disk; Related files: 00000159-00000160	\N	138	0	\N	\N	\N	\N
170	11	\N	\N	retained	\N	\N	\N	\N	\N	0	\N	\N	\N	Related files: 00000161-00000162	\N	139	0	\N	\N	\N	\N
171	11	\N	\N	retained	\N	\N	\N	\N	\N	0	\N	\N	\N	Related files: 00000161-00000162	\N	140	0	\N	\N	\N	\N
172	11	\N	\N	retained	\N	\N	\N	\N	\N	0	\N	\N	\N	\N	\N	141	0	\N	\N	\N	\N
173	11	\N	\N	retained	\N	\N	\N	\N	\N	0	\N	\N	\N	Related files: 00000164-00000165	\N	142	0	\N	\N	\N	\N
174	11	\N	\N	retained	\N	\N	\N	\N	\N	0	\N	\N	\N	Related files: 00000164-00000165	\N	143	0	\N	\N	\N	\N
175	11	\N	\N	retained	\N	\N	\N	\N	\N	0	\N	\N	\N	\N	\N	144	0	\N	\N	\N	\N
176	11	\N	\N	retained	\N	\N	\N	\N	\N	0	\N	\N	\N	Related files: 00000167-00000168	\N	145	0	\N	\N	\N	\N
177	11	\N	\N	retained	\N	\N	\N	\N	\N	0	\N	\N	\N	Related files: 00000167-00000168	\N	146	0	\N	\N	\N	\N
178	11	\N	\N	retained	\N	\N	\N	\N	\N	0	\N	\N	\N	Related files: 00000169-00000170	\N	147	0	\N	\N	\N	\N
179	11	\N	\N	retained	\N	\N	\N	\N	\N	0	\N	\N	\N	Related files: 00000169-00000170	\N	148	0	\N	\N	\N	\N
180	11	\N	\N	retained	\N	\N	\N	\N	\N	0	\N	\N	\N	Related files: 00000171-00000172	\N	149	0	\N	\N	\N	\N
181	11	\N	\N	retained	\N	\N	\N	\N	\N	0	\N	\N	\N	Related files: 00000171-00000172	\N	150	0	\N	\N	\N	\N
182	11	\N	\N	retained	\N	\N	\N	\N	\N	0	\N	\N	\N	Related files: 00000173-00000174	\N	151	0	\N	\N	\N	\N
183	11	\N	\N	retained	\N	\N	\N	\N	\N	0	\N	\N	\N	Related files: 00000173-00000174	\N	152	0	\N	\N	\N	\N
184	11	\N	\N	retained	\N	\N	\N	\N	\N	0	\N	\N	\N	Related files: 00000175-00000178	\N	153	0	\N	\N	\N	\N
185	11	\N	\N	retained	\N	\N	\N	\N	\N	0	\N	\N	\N	Related files: 00000175-00000178	\N	154	0	\N	\N	\N	\N
186	11	\N	\N	retained	\N	\N	\N	\N	\N	0	\N	\N	\N	Related files: 00000175-00000178	\N	155	0	\N	\N	\N	\N
187	11	\N	\N	retained	\N	\N	\N	\N	\N	0	\N	\N	\N	Related files: 00000175-00000178	\N	156	0	\N	\N	\N	\N
188	11	\N	\N	retained	\N	\N	\N	\N	\N	0	\N	\N	\N	Related files: 00000179-00000182	\N	157	0	\N	\N	\N	\N
189	11	\N	\N	retained	\N	\N	\N	\N	\N	0	\N	\N	\N	Related files: 00000179-00000182	\N	158	0	\N	\N	\N	\N
190	11	\N	\N	retained	\N	\N	\N	\N	\N	0	\N	\N	\N	Related files: 00000179-00000182	\N	159	0	\N	\N	\N	\N
191	11	\N	\N	retained	\N	\N	\N	\N	\N	0	\N	\N	\N	Related files: 00000179-00000182	\N	160	0	\N	\N	\N	\N
192	11	\N	\N	retained	\N	\N	\N	\N	\N	0	\N	\N	\N	Related files: 00000183-00000186	\N	161	0	\N	\N	\N	\N
193	11	\N	\N	retained	\N	\N	\N	\N	\N	0	\N	\N	\N	Related files: 00000183-00000186	\N	162	0	\N	\N	\N	\N
194	11	\N	\N	retained	\N	\N	\N	\N	\N	0	\N	\N	\N	Related files: 00000183-00000186	\N	163	0	\N	\N	\N	\N
195	11	\N	\N	retained	\N	\N	\N	\N	\N	0	\N	\N	\N	Related files: 00000183-00000186	\N	164	0	\N	\N	\N	\N
196	11	\N	\N	retained	\N	\N	\N	\N	\N	0	\N	\N	\N	Related files: 00000187-00000193	\N	165	0	\N	\N	\N	\N
197	11	\N	\N	retained	\N	\N	\N	\N	\N	0	\N	\N	\N	Related files: 00000187-00000193	\N	166	0	\N	\N	\N	\N
198	11	\N	\N	retained	\N	\N	\N	\N	\N	0	\N	\N	\N	Related files: 00000187-00000193	\N	167	0	\N	\N	\N	\N
199	11	\N	\N	retained	\N	\N	\N	\N	\N	0	\N	\N	\N	Related files: 00000187-00000193	\N	168	0	\N	\N	\N	\N
200	11	\N	\N	retained	\N	\N	\N	\N	\N	0	\N	\N	\N	Related files: 00000187-00000193	\N	169	0	\N	\N	\N	\N
201	11	\N	\N	retained	\N	\N	\N	\N	\N	0	\N	\N	\N	Related files: 00000187-00000193	\N	170	0	\N	\N	\N	\N
202	11	\N	\N	retained	\N	\N	\N	\N	\N	0	\N	\N	\N	Related files: 00000187-00000193	\N	171	0	\N	\N	\N	\N
203	11	\N	\N	retained	\N	\N	\N	\N	\N	0	\N	\N	\N	\N	\N	172	0	\N	\N	\N	\N
204	11	\N	\N	retained	\N	\N	\N	\N	\N	0	\N	\N	\N	Related files: 00000195-00000196	\N	173	0	\N	\N	\N	\N
205	11	\N	\N	retained	\N	\N	\N	\N	\N	0	\N	\N	\N	Related files: 00000195-00000196	\N	174	0	\N	\N	\N	\N
206	11	\N	\N	retained	\N	\N	\N	\N	\N	0	\N	\N	\N	Related files: 00000197-00000204	\N	175	0	\N	\N	\N	\N
207	11	\N	\N	retained	\N	\N	\N	\N	\N	0	\N	\N	\N	Related files: 00000197-00000204	\N	176	0	\N	\N	\N	\N
208	11	\N	\N	retained	\N	\N	\N	\N	\N	0	\N	\N	\N	Related files: 00000197-00000204	\N	177	0	\N	\N	\N	\N
209	11	\N	\N	retained	\N	\N	\N	\N	\N	0	\N	\N	\N	Related files: 00000197-00000204	\N	178	0	\N	\N	\N	\N
210	11	\N	\N	retained	\N	\N	\N	\N	\N	0	\N	\N	\N	Related files: 00000197-00000204	\N	179	0	\N	\N	\N	\N
211	11	\N	\N	retained	\N	\N	\N	\N	\N	0	\N	\N	\N	Related files: 00000197-00000204	\N	180	0	\N	\N	\N	\N
212	11	\N	\N	retained	\N	\N	\N	\N	\N	0	\N	\N	\N	Related files: 00000197-00000204	\N	181	0	\N	\N	\N	\N
213	11	\N	\N	retained	\N	\N	\N	\N	\N	0	\N	\N	\N	Related files: 00000197-00000204	\N	182	0	\N	\N	\N	\N
214	11	\N	\N	retained	\N	\N	\N	\N	\N	0	\N	\N	\N	Related files: 00000205-00000210	\N	183	0	\N	\N	\N	\N
215	11	\N	\N	retained	\N	\N	\N	\N	\N	0	\N	\N	\N	Related files: 00000205-00000210	\N	184	0	\N	\N	\N	\N
216	11	\N	\N	retained	\N	\N	\N	\N	\N	0	\N	\N	\N	Related files: 00000205-00000210	\N	185	0	\N	\N	\N	\N
217	11	\N	\N	retained	\N	\N	\N	\N	\N	0	\N	\N	\N	Related files: 00000205-00000210	\N	186	0	\N	\N	\N	\N
218	11	\N	\N	retained	\N	\N	\N	\N	\N	0	\N	\N	\N	Related files: 00000205-00000210	\N	187	0	\N	\N	\N	\N
219	11	\N	\N	retained	\N	\N	\N	\N	\N	0	\N	\N	\N	Related files: 00000205-00000210	\N	188	0	\N	\N	\N	\N
220	11	\N	\N	retained	\N	\N	\N	\N	\N	0	\N	\N	\N	Related files: 00000211-00000216	\N	189	0	\N	\N	\N	\N
221	11	\N	\N	retained	\N	\N	\N	\N	\N	0	\N	\N	\N	Related files: 00000211-00000216	\N	190	0	\N	\N	\N	\N
222	11	\N	\N	retained	\N	\N	\N	\N	\N	0	\N	\N	\N	Related files: 00000211-00000216	\N	191	0	\N	\N	\N	\N
223	11	\N	\N	retained	\N	\N	\N	\N	\N	0	\N	\N	\N	Related files: 00000211-00000216	\N	192	0	\N	\N	\N	\N
224	11	\N	\N	retained	\N	\N	\N	\N	\N	0	\N	\N	\N	Related files: 00000211-00000216	\N	193	0	\N	\N	\N	\N
225	11	\N	\N	retained	\N	\N	\N	\N	\N	0	\N	\N	\N	Related files: 00000211-00000216	\N	194	0	\N	\N	\N	\N
226	11	\N	\N	retained	\N	\N	\N	\N	\N	0	\N	\N	\N	Related files: 00000217-00000218	\N	195	0	\N	\N	\N	\N
227	11	\N	\N	retained	\N	\N	\N	\N	\N	0	\N	\N	\N	Related files: 00000217-00000218	\N	196	0	\N	\N	\N	\N
228	11	\N	\N	retained	\N	\N	\N	\N	\N	0	\N	\N	\N	Related files: 00000219-00000224	\N	197	0	\N	\N	\N	\N
229	11	\N	\N	retained	\N	\N	\N	\N	\N	0	\N	\N	\N	Related files: 00000219-00000224	\N	198	0	\N	\N	\N	\N
230	11	\N	\N	retained	\N	\N	\N	\N	\N	0	\N	\N	\N	Related files: 00000219-00000224	\N	199	0	\N	\N	\N	\N
231	11	\N	\N	retained	\N	\N	\N	\N	\N	0	\N	\N	\N	Related files: 00000219-00000224	\N	200	0	\N	\N	\N	\N
232	11	\N	\N	retained	\N	\N	\N	\N	\N	0	\N	\N	\N	Related files: 00000219-00000224	\N	201	0	\N	\N	\N	\N
233	11	\N	\N	retained	\N	\N	\N	\N	\N	0	\N	\N	\N	Related files: 00000219-00000224	\N	202	0	\N	\N	\N	\N
234	11	\N	\N	retained	\N	\N	\N	\N	\N	0	\N	\N	\N	Related files: 00000225-00000227	\N	203	0	\N	\N	\N	\N
235	11	\N	\N	retained	\N	\N	\N	\N	\N	0	\N	\N	\N	Related files: 00000225-00000227	\N	204	0	\N	\N	\N	\N
236	11	\N	\N	retained	\N	\N	\N	\N	\N	0	\N	\N	\N	Related files: 00000225-00000227	\N	205	0	\N	\N	\N	\N
237	11	\N	\N	retained	\N	\N	\N	\N	\N	0	\N	\N	\N	Related files: 00000228-00000231	\N	206	0	\N	\N	\N	\N
238	11	\N	\N	retained	\N	\N	\N	\N	\N	0	\N	\N	\N	Related files: 00000228-00000231	\N	207	0	\N	\N	\N	\N
239	11	\N	\N	retained	\N	\N	\N	\N	\N	0	\N	\N	\N	Related files: 00000228-00000231	\N	208	0	\N	\N	\N	\N
240	11	\N	\N	retained	\N	\N	\N	\N	\N	0	\N	\N	\N	Related files: 00000228-00000231	\N	209	0	\N	\N	\N	\N
241	11	\N	\N	retained	\N	\N	\N	\N	\N	0	\N	\N	\N	Related files: 00000232, 00000234-00000240.wav	\N	210	0	\N	\N	\N	\N
242	11	\N	\N	retained	\N	\N	\N	\N	\N	0	\N	\N	\N	Related files: 00000232, 00000234-00000240.wav	\N	211	0	\N	\N	\N	\N
243	11	\N	\N	retained	\N	\N	\N	\N	\N	0	\N	\N	\N	Related files: 00000232, 00000234-00000240.wav	\N	212	0	\N	\N	\N	\N
244	11	\N	\N	retained	\N	\N	\N	\N	\N	0	\N	\N	\N	Related files: 00000232, 00000234-00000240.wav	\N	213	0	\N	\N	\N	\N
245	11	\N	\N	retained	\N	\N	\N	\N	\N	0	\N	\N	\N	Related files: 00000232, 00000234-00000240.wav	\N	214	0	\N	\N	\N	\N
246	11	\N	\N	retained	\N	\N	\N	\N	\N	0	\N	\N	\N	Related files: 00000232, 00000234-00000240.wav	\N	215	0	\N	\N	\N	\N
247	11	\N	\N	retained	\N	\N	\N	\N	\N	0	\N	\N	\N	Related files: 00000232, 00000234-00000240.wav	\N	216	0	\N	\N	\N	\N
248	11	\N	\N	retained	\N	\N	\N	\N	\N	0	\N	\N	\N	Related files: 00000232, 00000234-00000240.wav	\N	217	0	\N	\N	\N	\N
249	11	\N	\N	retained	\N	\N	\N	\N	\N	0	\N	\N	\N	Related files: 00000241-00000242	\N	218	0	\N	\N	\N	\N
250	11	\N	\N	retained	\N	\N	\N	\N	\N	0	\N	\N	\N	Related files: 00000241-00000242	\N	219	0	\N	\N	\N	\N
251	11	\N	\N	retained	\N	\N	\N	\N	\N	0	\N	\N	\N	Related files: 00000243-00000244	\N	220	0	\N	\N	\N	\N
252	11	\N	\N	retained	\N	\N	\N	\N	\N	0	\N	\N	\N	Related files: 00000243-00000244	\N	221	0	\N	\N	\N	\N
253	11	\N	\N	retained	\N	\N	\N	\N	\N	0	\N	\N	\N	may be a duplicate of 00000246	\N	222	0	\N	\N	\N	\N
254	11	\N	\N	retained	\N	\N	\N	\N	\N	0	\N	\N	\N	may be a duplicate of 00000245	\N	223	0	\N	\N	\N	\N
255	11	\N	\N	retained	\N	\N	\N	\N	\N	0	\N	\N	\N	Related files: 00000247-00000250	\N	224	0	\N	\N	\N	\N
256	11	\N	\N	retained	\N	\N	\N	\N	\N	0	\N	\N	\N	Related files: 00000247-00000250	\N	225	0	\N	\N	\N	\N
257	11	\N	\N	retained	\N	\N	\N	\N	\N	0	\N	\N	\N	Related files: 00000247-00000250	\N	226	0	\N	\N	\N	\N
258	11	\N	\N	retained	\N	\N	\N	\N	\N	0	\N	\N	\N	Related files: 00000247-00000250	\N	227	0	\N	\N	\N	\N
259	11	\N	\N	retained	\N	\N	\N	\N	\N	0	\N	\N	\N	Related files: 00000251-00000252	\N	228	0	\N	\N	\N	\N
260	11	\N	\N	retained	\N	\N	\N	\N	\N	0	\N	\N	\N	Related files: 00000251-00000252	\N	229	0	\N	\N	\N	\N
261	11	\N	\N	retained	\N	\N	\N	\N	\N	0	\N	\N	\N	Related files: 00000253-00000254	\N	230	0	\N	\N	\N	\N
262	11	\N	\N	retained	\N	\N	\N	\N	\N	0	\N	\N	\N	Related files: 00000253-00000254	\N	231	0	\N	\N	\N	\N
263	11	\N	\N	retained	\N	\N	\N	\N	\N	0	\N	\N	\N	\N	\N	232	0	\N	\N	\N	\N
264	14	\N	\N	retained	\N	\N	\N	\N	\N	0	\N	\N	\N	\N	\N	233	0	\N	\N	\N	\N
265	14	\N	\N	retained	\N	\N	\N	\N	\N	0	\N	\N	\N	Related files: 00000257-00000259	\N	234	0	\N	\N	\N	\N
266	14	\N	\N	retained	\N	\N	\N	\N	\N	0	\N	\N	\N	Related files: 00000257-00000259	\N	235	0	\N	\N	\N	\N
267	14	\N	\N	retained	\N	\N	\N	\N	\N	0	\N	\N	\N	Related files: 00000257-00000259.	\N	236	0	\N	\N	\N	\N
268	14	\N	\N	retained	\N	\N	\N	\N	\N	0	\N	\N	\N	Related files: 00000260-00000262	\N	237	0	\N	\N	\N	\N
269	14	\N	\N	retained	\N	\N	\N	\N	\N	0	\N	\N	\N	Related files: 00000260-00000262	\N	238	0	\N	\N	\N	\N
270	14	\N	\N	retained	\N	\N	\N	\N	\N	0	\N	\N	\N	Related files: 00000260-00000262	\N	239	0	\N	\N	\N	\N
271	14	\N	\N	retained	\N	\N	\N	\N	\N	0	\N	\N	\N	Related files: 0000068, 00000263-00000264	\N	240	0	\N	\N	\N	\N
272	14	\N	\N	retained	\N	\N	\N	\N	\N	0	\N	\N	\N	Related files: 0000068, 00000263-00000264	\N	241	0	\N	\N	\N	\N
273	14	\N	\N	retained	\N	\N	\N	\N	\N	0	\N	\N	\N	\N	\N	242	0	\N	\N	\N	\N
274	14	\N	\N	retained	\N	\N	\N	\N	\N	0	\N	\N	\N	Related files: 00000266-00000267	\N	243	0	\N	\N	\N	\N
275	14	\N	\N	retained	\N	\N	\N	\N	\N	0	\N	\N	\N	Related files: 00000266-00000267	\N	244	0	\N	\N	\N	\N
276	14	\N	\N	retained	\N	\N	\N	\N	\N	0	\N	\N	\N	Related files: 00000268-00000269	\N	245	0	\N	\N	\N	\N
277	14	\N	\N	retained	\N	\N	\N	\N	\N	0	\N	\N	\N	Related files: 00000268-00000269	\N	246	0	\N	\N	\N	\N
278	14	\N	\N	retained	\N	\N	\N	\N	\N	0	\N	\N	\N	Related files: 00000270-00000272	\N	247	0	\N	\N	\N	\N
279	14	\N	\N	retained	\N	\N	\N	\N	\N	0	\N	\N	\N	Related files: 00000270-00000272	\N	248	0	\N	\N	\N	\N
280	14	\N	\N	retained	\N	\N	\N	\N	\N	0	\N	\N	\N	Related files: 00000270-00000272	\N	249	0	\N	\N	\N	\N
281	14	\N	\N	retained	\N	\N	\N	\N	\N	0	\N	\N	\N	Related files: 00000273-00000274	\N	250	0	\N	\N	\N	\N
282	14	\N	\N	retained	\N	\N	\N	\N	\N	0	\N	\N	\N	Related files: 00000273-00000274	\N	251	0	\N	\N	\N	\N
283	14	\N	\N	retained	\N	\N	\N	\N	\N	0	\N	\N	\N	Related files: 00000275, 00000277	\N	252	0	\N	\N	\N	\N
284	14	\N	\N	retained	\N	\N	\N	\N	\N	0	\N	\N	\N	\N	\N	253	0	\N	\N	\N	\N
285	14	\N	\N	retained	\N	\N	\N	\N	\N	0	\N	\N	\N	Related files: 00000275, 00000277	\N	254	0	\N	\N	\N	\N
286	14	\N	\N	retained	\N	\N	\N	\N	\N	0	\N	\N	\N	\N	\N	255	0	\N	\N	\N	\N
287	14	\N	\N	retained	\N	\N	\N	\N	\N	0	\N	\N	\N	Related files: 00000279-00000280, 00000612	\N	256	0	\N	\N	\N	\N
288	14	\N	\N	retained	\N	\N	\N	\N	\N	0	\N	\N	\N	Related files: 00000279-00000280, 00000612	\N	257	0	\N	\N	\N	\N
289	14	\N	\N	retained	\N	\N	\N	\N	\N	0	\N	\N	\N	Related files: 00000281.wav - 00000282.wav	\N	258	0	\N	\N	\N	\N
290	14	\N	\N	retained	\N	\N	\N	\N	\N	0	\N	\N	\N	Related files: 00000281.wav - 00000282.wav	\N	259	0	\N	\N	\N	\N
291	14	\N	\N	retained	\N	\N	\N	\N	\N	0	\N	\N	\N	Related files: 00000283-00000286	\N	260	0	\N	\N	\N	\N
292	14	\N	\N	retained	\N	\N	\N	\N	\N	0	\N	\N	\N	Related files: 00000283-00000286	\N	261	0	\N	\N	\N	\N
293	14	\N	\N	retained	\N	\N	\N	\N	\N	0	\N	\N	\N	Related files: 00000283-00000286	\N	262	0	\N	\N	\N	\N
294	14	\N	\N	retained	\N	\N	\N	\N	\N	0	\N	\N	\N	Related files: 00000283-00000286	\N	263	0	\N	\N	\N	\N
295	14	\N	\N	retained	\N	\N	\N	\N	\N	0	\N	\N	\N	Related files: 00000287-00000288	\N	264	0	\N	\N	\N	\N
296	14	\N	\N	retained	\N	\N	\N	\N	\N	0	\N	\N	\N	Related files: 00000287-00000288	\N	265	0	\N	\N	\N	\N
297	14	\N	\N	retained	\N	\N	\N	\N	\N	0	\N	\N	\N	Related files: 00000289-00000290	\N	266	0	\N	\N	\N	\N
298	14	\N	\N	retained	\N	\N	\N	\N	\N	0	\N	\N	\N	Related files: 00000289-00000290	\N	267	0	\N	\N	\N	\N
299	14	\N	\N	retained	\N	\N	\N	\N	\N	0	\N	\N	\N	Related files: 00000291 - 00000292	\N	268	0	\N	\N	\N	\N
300	14	\N	\N	retained	\N	\N	\N	\N	\N	0	\N	\N	\N	Related files: 00000291-00000292	\N	269	0	\N	\N	\N	\N
301	14	\N	\N	retained	\N	\N	\N	\N	\N	0	\N	\N	\N	Related files: 00000293-00000296	\N	270	0	\N	\N	\N	\N
302	14	\N	\N	retained	\N	\N	\N	\N	\N	0	\N	\N	\N	Related files: 00000293-00000296	\N	271	0	\N	\N	\N	\N
303	14	\N	\N	retained	\N	\N	\N	\N	\N	0	\N	\N	\N	Related files: 00000293-00000296	\N	272	0	\N	\N	\N	\N
304	14	\N	\N	retained	\N	\N	\N	\N	\N	0	\N	\N	\N	Related files: 00000293-00000296	\N	273	0	\N	\N	\N	\N
305	86	\N	\N	retained	\N	\N	\N	\N	\N	0	\N	\N	\N	Related files: 00000297-00000298	\N	274	0	\N	\N	\N	\N
306	86	\N	\N	retained	\N	\N	\N	\N	\N	0	\N	\N	\N	Related files: 00000297-00000298	\N	275	0	\N	\N	\N	\N
307	15	\N	\N	retained	\N	\N	\N	\N	\N	0	\N	\N	\N	Time corrected. Related files: 00000299-00000325	\N	276	0	\N	\N	\N	\N
308	15	\N	\N	retained	\N	\N	\N	\N	\N	0	\N	\N	\N	Time corrected. Related files: 00000299-00000325	\N	277	0	\N	\N	\N	\N
309	15	\N	\N	retained	\N	\N	\N	\N	\N	0	\N	\N	\N	Time corrected. Related files: 00000299-00000325	\N	278	0	\N	\N	\N	\N
310	15	\N	\N	retained	\N	\N	\N	\N	\N	0	\N	\N	\N	Time corrected. Related files: 00000299-00000325	\N	279	0	\N	\N	\N	\N
311	15	\N	\N	retained	\N	\N	\N	\N	\N	0	\N	\N	\N	Time corrected. Related files: 00000299-00000325	\N	280	0	\N	\N	\N	\N
312	15	\N	\N	retained	\N	\N	\N	\N	\N	0	\N	\N	\N	Time corrected. Related files: 00000299-00000325	\N	281	0	\N	\N	\N	\N
313	15	\N	\N	retained	\N	\N	\N	\N	\N	0	\N	\N	\N	Time corrected. Related files: 00000299-00000325	\N	282	0	\N	\N	\N	\N
314	15	\N	\N	retained	\N	\N	\N	\N	\N	0	\N	\N	\N	Time corrected. Related files: 00000299-00000325	\N	283	0	\N	\N	\N	\N
315	15	\N	\N	retained	\N	\N	\N	\N	\N	0	\N	\N	\N	Time corrected. Related files: 00000299-00000325	\N	284	0	\N	\N	\N	\N
316	15	\N	\N	retained	\N	\N	\N	\N	\N	0	\N	\N	\N	Time corrected. Related files: 00000299-00000325	\N	285	0	\N	\N	\N	\N
317	15	\N	\N	retained	\N	\N	\N	\N	\N	0	\N	\N	\N	Time corrected. Related files: 00000299-00000325	\N	286	0	\N	\N	\N	\N
318	15	\N	\N	retained	\N	\N	\N	\N	\N	0	\N	\N	\N	Time corrected. Related files: 00000299-00000325	\N	287	0	\N	\N	\N	\N
319	15	\N	\N	retained	\N	\N	\N	\N	\N	0	\N	\N	\N	Time corrected. Related files: 00000299-00000325	\N	288	0	\N	\N	\N	\N
320	15	\N	\N	retained	\N	\N	\N	\N	\N	0	\N	\N	\N	Time corrected. Related files: 00000299-00000325	\N	289	0	\N	\N	\N	\N
321	15	\N	\N	retained	\N	\N	\N	\N	\N	0	\N	\N	\N	Time corrected. Related files: 00000299-00000325	\N	290	0	\N	\N	\N	\N
322	15	\N	\N	retained	\N	\N	\N	\N	\N	0	\N	\N	\N	Time corrected. Related files: 00000299-00000325	\N	291	0	\N	\N	\N	\N
323	15	\N	\N	retained	\N	\N	\N	\N	\N	0	\N	\N	\N	Time corrected. Related files: 00000299-00000325	\N	292	0	\N	\N	\N	\N
324	15	\N	\N	retained	\N	\N	\N	\N	\N	0	\N	\N	\N	Time corrected. Related files: 00000299-00000325	\N	293	0	\N	\N	\N	\N
325	15	\N	\N	retained	\N	\N	\N	\N	\N	0	\N	\N	\N	Time corrected. Related files: 00000299-00000325	\N	294	0	\N	\N	\N	\N
326	15	\N	\N	retained	\N	\N	\N	\N	\N	0	\N	\N	\N	Time corrected. Related files: 00000299-00000325	\N	295	0	\N	\N	\N	\N
327	15	\N	\N	retained	\N	\N	\N	\N	\N	0	\N	\N	\N	Time corrected. Related files: 00000299-00000325	\N	296	0	\N	\N	\N	\N
328	15	\N	\N	retained	\N	\N	\N	\N	\N	0	\N	\N	\N	Time corrected. Related files: 00000299-00000325	\N	297	0	\N	\N	\N	\N
329	15	\N	\N	retained	\N	\N	\N	\N	\N	0	\N	\N	\N	Time corrected. Related files: 00000299-00000325	\N	298	0	\N	\N	\N	\N
330	15	\N	\N	retained	\N	\N	\N	\N	\N	0	\N	\N	\N	Time corrected. Related files: 00000299-00000325	\N	299	0	\N	\N	\N	\N
331	15	\N	\N	retained	\N	\N	\N	\N	\N	0	\N	\N	\N	Time corrected. Related files: 00000299-00000325	\N	300	0	\N	\N	\N	\N
332	15	\N	\N	retained	\N	\N	\N	\N	\N	0	\N	\N	\N	Time corrected. Related files: 00000299-00000325	\N	301	0	\N	\N	\N	\N
333	15	\N	\N	retained	\N	\N	\N	\N	\N	0	\N	\N	\N	Time corrected. Related files: 00000299-00000325	\N	302	0	\N	\N	\N	\N
334	15	\N	\N	retained	\N	\N	\N	\N	\N	0	\N	\N	\N	Time corrected. Related files: 00000326-00000330	\N	303	0	\N	\N	\N	\N
335	15	\N	\N	retained	\N	\N	\N	\N	\N	0	\N	\N	\N	Time corrected. Related files: 00000326-00000330	\N	304	0	\N	\N	\N	\N
336	15	\N	\N	retained	\N	\N	\N	\N	\N	0	\N	\N	\N	Time corrected. Related files: 00000326-00000330	\N	305	0	\N	\N	\N	\N
337	15	\N	\N	retained	\N	\N	\N	\N	\N	0	\N	\N	\N	Time corrected. Related files: 00000326-00000330	\N	306	0	\N	\N	\N	\N
338	15	\N	\N	retained	\N	\N	\N	\N	\N	0	\N	\N	\N	Time corrected. Related files: 00000326-00000330	\N	307	0	\N	\N	\N	\N
339	15	\N	\N	retained	\N	\N	\N	\N	\N	0	\N	\N	\N	Time corrected. Related files: 00000331-00000341	\N	308	0	\N	\N	\N	\N
340	15	\N	\N	retained	\N	\N	\N	\N	\N	0	\N	\N	\N	Time corrected. Related files: 00000331-00000341	\N	309	0	\N	\N	\N	\N
341	15	\N	\N	retained	\N	\N	\N	\N	\N	0	\N	\N	\N	Time corrected. Related files: 00000331-00000341	\N	310	0	\N	\N	\N	\N
342	15	\N	\N	retained	\N	\N	\N	\N	\N	0	\N	\N	\N	Time corrected. Related files: 00000331-00000341	\N	311	0	\N	\N	\N	\N
343	15	\N	\N	retained	\N	\N	\N	\N	\N	0	\N	\N	\N	Time corrected. Related files: 00000331-00000341	\N	312	0	\N	\N	\N	\N
344	15	\N	\N	retained	\N	\N	\N	\N	\N	0	\N	\N	\N	Time corrected. Related files: 00000331-00000341	\N	313	0	\N	\N	\N	\N
345	15	\N	\N	retained	\N	\N	\N	\N	\N	0	\N	\N	\N	Time corrected. Related files: 00000331-00000341	\N	314	0	\N	\N	\N	\N
346	15	\N	\N	retained	\N	\N	\N	\N	\N	0	\N	\N	\N	Time corrected. Related files: 00000331-00000341	\N	315	0	\N	\N	\N	\N
347	15	\N	\N	retained	\N	\N	\N	\N	\N	0	\N	\N	\N	Time corrected. Related files: 00000331-00000341	\N	316	0	\N	\N	\N	\N
348	15	\N	\N	retained	\N	\N	\N	\N	\N	0	\N	\N	\N	Time corrected. Related files: 00000331-00000341	\N	317	0	\N	\N	\N	\N
349	15	\N	\N	retained	\N	\N	\N	\N	\N	0	\N	\N	\N	Time corrected. Related files: 00000331-00000341	\N	318	0	\N	\N	\N	\N
350	15	\N	\N	retained	\N	\N	\N	\N	\N	0	\N	\N	\N	Time corrected. Related files: 00000342-00000353	\N	319	0	\N	\N	\N	\N
351	15	\N	\N	retained	\N	\N	\N	\N	\N	0	\N	\N	\N	Time corrected. Related files: 00000342-00000353	\N	320	0	\N	\N	\N	\N
352	15	\N	\N	retained	\N	\N	\N	\N	\N	0	\N	\N	\N	Time corrected. Related files: 00000342-00000353	\N	321	0	\N	\N	\N	\N
353	15	\N	\N	retained	\N	\N	\N	\N	\N	0	\N	\N	\N	Time corrected. Related files: 00000342-00000353	\N	322	0	\N	\N	\N	\N
354	15	\N	\N	retained	\N	\N	\N	\N	\N	0	\N	\N	\N	Time corrected. Related files: 00000342-00000353	\N	323	0	\N	\N	\N	\N
355	15	\N	\N	retained	\N	\N	\N	\N	\N	0	\N	\N	\N	Time corrected. Related files: 00000342-00000353	\N	324	0	\N	\N	\N	\N
356	15	\N	\N	retained	\N	\N	\N	\N	\N	0	\N	\N	\N	Time corrected. Related files: 00000342-00000353	\N	325	0	\N	\N	\N	\N
357	15	\N	\N	retained	\N	\N	\N	\N	\N	0	\N	\N	\N	Time corrected. Related files: 00000342-00000353	\N	326	0	\N	\N	\N	\N
358	15	\N	\N	retained	\N	\N	\N	\N	\N	0	\N	\N	\N	Time corrected. Related files: 00000342-00000353	\N	327	0	\N	\N	\N	\N
359	15	\N	\N	retained	\N	\N	\N	\N	\N	0	\N	\N	\N	Time corrected. Related files: 00000342-00000353	\N	328	0	\N	\N	\N	\N
360	15	\N	\N	retained	\N	\N	\N	\N	\N	0	\N	\N	\N	Time corrected. Related files: 00000342-00000353	\N	329	0	\N	\N	\N	\N
361	15	\N	\N	retained	\N	\N	\N	\N	\N	0	\N	\N	\N	Time corrected. Related files: 00000342-00000353	\N	330	0	\N	\N	\N	\N
362	15	\N	\N	retained	\N	\N	\N	\N	\N	0	\N	\N	\N	Time corrected. Related files: 00000354-00000358	\N	331	0	\N	\N	\N	\N
363	15	\N	\N	retained	\N	\N	\N	\N	\N	0	\N	\N	\N	Time corrected. Related files: 00000354-00000358	\N	332	0	\N	\N	\N	\N
364	15	\N	\N	retained	\N	\N	\N	\N	\N	0	\N	\N	\N	Time corrected. Related files: 00000354-00000358	\N	333	0	\N	\N	\N	\N
365	15	\N	\N	retained	\N	\N	\N	\N	\N	0	\N	\N	\N	Time corrected. Related files: 00000354-00000358	\N	334	0	\N	\N	\N	\N
366	15	\N	\N	retained	\N	\N	\N	\N	\N	0	\N	\N	\N	Time corrected. Related files: 00000354-00000358	\N	335	0	\N	\N	\N	\N
367	15	\N	\N	retained	\N	\N	\N	\N	\N	0	\N	\N	\N	Time corrected. Related files: 00000359-00000365	\N	336	0	\N	\N	\N	\N
368	15	\N	\N	retained	\N	\N	\N	\N	\N	0	\N	\N	\N	Time corrected. Related files: 00000359-00000365	\N	337	0	\N	\N	\N	\N
369	15	\N	\N	retained	\N	\N	\N	\N	\N	0	\N	\N	\N	Time corrected. Related files: 00000359-00000365	\N	338	0	\N	\N	\N	\N
370	15	\N	\N	retained	\N	\N	\N	\N	\N	0	\N	\N	\N	Time corrected. Related files: 00000359-00000365	\N	339	0	\N	\N	\N	\N
371	15	\N	\N	retained	\N	\N	\N	\N	\N	0	\N	\N	\N	Time corrected. Related files: 00000359-00000365	\N	340	0	\N	\N	\N	\N
372	15	\N	\N	retained	\N	\N	\N	\N	\N	0	\N	\N	\N	Time corrected. Related files: 00000359-00000365	\N	341	0	\N	\N	\N	\N
373	15	\N	\N	retained	\N	\N	\N	\N	\N	0	\N	\N	\N	Time corrected. Related files: 00000359-00000365	\N	342	0	\N	\N	\N	\N
374	15	\N	\N	retained	\N	\N	\N	\N	\N	0	\N	\N	\N	Time corrected. Related files: 00000366-00000373	\N	343	0	\N	\N	\N	\N
375	15	\N	\N	retained	\N	\N	\N	\N	\N	0	\N	\N	\N	Time corrected. Related files: 00000366-00000373	\N	344	0	\N	\N	\N	\N
376	15	\N	\N	retained	\N	\N	\N	\N	\N	0	\N	\N	\N	Time corrected. Related files: 00000366-00000373	\N	345	0	\N	\N	\N	\N
377	15	\N	\N	retained	\N	\N	\N	\N	\N	0	\N	\N	\N	Time corrected. Related files: 00000366-00000373	\N	346	0	\N	\N	\N	\N
378	15	\N	\N	retained	\N	\N	\N	\N	\N	0	\N	\N	\N	Time corrected. Related files: 00000366-00000373	\N	347	0	\N	\N	\N	\N
379	15	\N	\N	retained	\N	\N	\N	\N	\N	0	\N	\N	\N	Time corrected. Related files: 00000366-00000373	\N	348	0	\N	\N	\N	\N
380	15	\N	\N	retained	\N	\N	\N	\N	\N	0	\N	\N	\N	Time corrected. Related files: 00000366-00000373	\N	349	0	\N	\N	\N	\N
381	15	\N	\N	retained	\N	\N	\N	\N	\N	0	\N	\N	\N	Time corrected. Related files: 00000366-00000373	\N	350	0	\N	\N	\N	\N
382	15	\N	\N	retained	\N	\N	\N	\N	\N	0	\N	\N	\N	Time corrected. Related files: 00000374-00000382	\N	351	0	\N	\N	\N	\N
383	15	\N	\N	retained	\N	\N	\N	\N	\N	0	\N	\N	\N	Time corrected. Related files: 00000374-00000382	\N	352	0	\N	\N	\N	\N
384	15	\N	\N	retained	\N	\N	\N	\N	\N	0	\N	\N	\N	Time corrected. Related files: 00000374-00000382	\N	353	0	\N	\N	\N	\N
385	15	\N	\N	retained	\N	\N	\N	\N	\N	0	\N	\N	\N	Time corrected. Related files: 00000374-00000382	\N	354	0	\N	\N	\N	\N
386	15	\N	\N	retained	\N	\N	\N	\N	\N	0	\N	\N	\N	Time corrected. Related files: 00000374-00000382	\N	355	0	\N	\N	\N	\N
387	15	\N	\N	retained	\N	\N	\N	\N	\N	0	\N	\N	\N	Time corrected. Related files: 00000374-00000382	\N	356	0	\N	\N	\N	\N
388	15	\N	\N	retained	\N	\N	\N	\N	\N	0	\N	\N	\N	Time corrected. Related files: 00000374-00000382	\N	357	0	\N	\N	\N	\N
389	15	\N	\N	retained	\N	\N	\N	\N	\N	0	\N	\N	\N	Time corrected. Related files: 00000374-00000382	\N	358	0	\N	\N	\N	\N
390	15	\N	\N	retained	\N	\N	\N	\N	\N	0	\N	\N	\N	Time corrected. Related files: 00000374-00000382	\N	359	0	\N	\N	\N	\N
391	15	\N	\N	retained	\N	\N	\N	\N	\N	0	\N	\N	\N	Time corrected. Related files: 00000383-00000389	\N	360	0	\N	\N	\N	\N
392	15	\N	\N	retained	\N	\N	\N	\N	\N	0	\N	\N	\N	Time corrected. Related files: 00000383-00000389	\N	361	0	\N	\N	\N	\N
393	15	\N	\N	retained	\N	\N	\N	\N	\N	0	\N	\N	\N	Time corrected. Related files: 00000383-00000389	\N	362	0	\N	\N	\N	\N
394	15	\N	\N	retained	\N	\N	\N	\N	\N	0	\N	\N	\N	Time corrected. Related files: 00000383-00000389	\N	363	0	\N	\N	\N	\N
395	15	\N	\N	retained	\N	\N	\N	\N	\N	0	\N	\N	\N	Time corrected. Related files: 00000383-00000389	\N	364	0	\N	\N	\N	\N
396	15	\N	\N	retained	\N	\N	\N	\N	\N	0	\N	\N	\N	Time corrected. Related files: 00000383-00000389	\N	365	0	\N	\N	\N	\N
397	15	\N	\N	retained	\N	\N	\N	\N	\N	0	\N	\N	\N	Time corrected. Related files: 00000383-00000389	\N	366	0	\N	\N	\N	\N
398	15	\N	\N	retained	\N	\N	\N	\N	\N	0	\N	\N	\N	Time corrected. Related files: 00000390-00000394	\N	367	0	\N	\N	\N	\N
399	15	\N	\N	retained	\N	\N	\N	\N	\N	0	\N	\N	\N	Time corrected. Related files: 00000390-00000394	\N	368	0	\N	\N	\N	\N
400	15	\N	\N	retained	\N	\N	\N	\N	\N	0	\N	\N	\N	Time corrected. Related files: 00000390-00000394	\N	369	0	\N	\N	\N	\N
401	15	\N	\N	retained	\N	\N	\N	\N	\N	0	\N	\N	\N	Time corrected. Related files: 00000390-00000394	\N	370	0	\N	\N	\N	\N
402	15	\N	\N	retained	\N	\N	\N	\N	\N	0	\N	\N	\N	Time corrected. Related files: 00000390-00000394	\N	371	0	\N	\N	\N	\N
403	15	\N	\N	retained	\N	\N	\N	\N	\N	0	\N	\N	\N	Time corrected. Related files: 00000395-00000405	\N	372	0	\N	\N	\N	\N
404	15	\N	\N	retained	\N	\N	\N	\N	\N	0	\N	\N	\N	Time corrected. Related files: 00000395-00000405	\N	373	0	\N	\N	\N	\N
405	15	\N	\N	retained	\N	\N	\N	\N	\N	0	\N	\N	\N	Time corrected. Related files: 00000395-00000405	\N	374	0	\N	\N	\N	\N
406	15	\N	\N	retained	\N	\N	\N	\N	\N	0	\N	\N	\N	Time corrected. Related files: 00000395-00000405	\N	375	0	\N	\N	\N	\N
407	15	\N	\N	retained	\N	\N	\N	\N	\N	0	\N	\N	\N	Time corrected. Related files: 00000395-00000405	\N	376	0	\N	\N	\N	\N
408	15	\N	\N	retained	\N	\N	\N	\N	\N	0	\N	\N	\N	Time corrected. Related files: 00000395-00000405	\N	377	0	\N	\N	\N	\N
409	15	\N	\N	retained	\N	\N	\N	\N	\N	0	\N	\N	\N	Time corrected. Related files: 00000395-00000405	\N	378	0	\N	\N	\N	\N
410	15	\N	\N	retained	\N	\N	\N	\N	\N	0	\N	\N	\N	Time corrected. Related files: 00000395-00000405	\N	379	0	\N	\N	\N	\N
411	15	\N	\N	retained	\N	\N	\N	\N	\N	0	\N	\N	\N	Time corrected. Related files: 00000395-00000405	\N	380	0	\N	\N	\N	\N
412	15	\N	\N	retained	\N	\N	\N	\N	\N	0	\N	\N	\N	Time corrected. Related files: 00000395-00000405	\N	381	0	\N	\N	\N	\N
413	15	\N	\N	retained	\N	\N	\N	\N	\N	0	\N	\N	\N	Time corrected. Related files: 00000395-00000405	\N	382	0	\N	\N	\N	\N
414	15	\N	\N	retained	\N	\N	\N	\N	\N	0	\N	\N	\N	Time corrected. Related files: 00000406-00000415	\N	383	0	\N	\N	\N	\N
415	15	\N	\N	retained	\N	\N	\N	\N	\N	0	\N	\N	\N	Time corrected. Related files: 00000406-00000415	\N	384	0	\N	\N	\N	\N
416	15	\N	\N	retained	\N	\N	\N	\N	\N	0	\N	\N	\N	Time corrected. Related files: 00000406-00000415	\N	385	0	\N	\N	\N	\N
417	15	\N	\N	retained	\N	\N	\N	\N	\N	0	\N	\N	\N	Time corrected. Related files: 00000406-00000415	\N	386	0	\N	\N	\N	\N
418	15	\N	\N	retained	\N	\N	\N	\N	\N	0	\N	\N	\N	Time corrected. Related files: 00000406-00000415	\N	387	0	\N	\N	\N	\N
419	15	\N	\N	retained	\N	\N	\N	\N	\N	0	\N	\N	\N	Time corrected. Related files: 00000406-00000415	\N	388	0	\N	\N	\N	\N
420	15	\N	\N	retained	\N	\N	\N	\N	\N	0	\N	\N	\N	Time corrected. Related files: 00000406-00000415	\N	389	0	\N	\N	\N	\N
421	15	\N	\N	retained	\N	\N	\N	\N	\N	0	\N	\N	\N	Time corrected. Related files: 00000406-00000415	\N	390	0	\N	\N	\N	\N
422	15	\N	\N	retained	\N	\N	\N	\N	\N	0	\N	\N	\N	Time corrected. Related files: 00000406-00000415	\N	391	0	\N	\N	\N	\N
423	15	\N	\N	retained	\N	\N	\N	\N	\N	0	\N	\N	\N	Time corrected. Related files: 00000406-00000415	\N	392	0	\N	\N	\N	\N
424	15	\N	\N	retained	\N	\N	\N	\N	\N	0	\N	\N	\N	Time corrected. Related files: 00000416-00000424	\N	393	0	\N	\N	\N	\N
425	15	\N	\N	retained	\N	\N	\N	\N	\N	0	\N	\N	\N	Time corrected. Related files: 00000416-00000424	\N	394	0	\N	\N	\N	\N
426	15	\N	\N	retained	\N	\N	\N	\N	\N	0	\N	\N	\N	Time corrected. Related files: 00000416-00000424	\N	395	0	\N	\N	\N	\N
427	15	\N	\N	retained	\N	\N	\N	\N	\N	0	\N	\N	\N	Time corrected. Related files: 00000416-00000424	\N	396	0	\N	\N	\N	\N
428	15	\N	\N	retained	\N	\N	\N	\N	\N	0	\N	\N	\N	Time corrected. Related files: 00000416-00000424	\N	397	0	\N	\N	\N	\N
429	15	\N	\N	retained	\N	\N	\N	\N	\N	0	\N	\N	\N	Time corrected. Related files: 00000416-00000424	\N	398	0	\N	\N	\N	\N
430	15	\N	\N	retained	\N	\N	\N	\N	\N	0	\N	\N	\N	Time corrected. Related files: 00000416-00000424	\N	399	0	\N	\N	\N	\N
431	15	\N	\N	retained	\N	\N	\N	\N	\N	0	\N	\N	\N	Time corrected. Related files: 00000416-00000424	\N	400	0	\N	\N	\N	\N
432	15	\N	\N	retained	\N	\N	\N	\N	\N	0	\N	\N	\N	Time corrected. Related files: 00000416-00000424	\N	401	0	\N	\N	\N	\N
433	15	\N	\N	retained	\N	\N	\N	\N	\N	0	\N	\N	\N	Time corrected. Related files: 00000425-00000432	\N	402	0	\N	\N	\N	\N
434	15	\N	\N	retained	\N	\N	\N	\N	\N	0	\N	\N	\N	Time corrected. Related files: 00000425-00000432	\N	403	0	\N	\N	\N	\N
435	15	\N	\N	retained	\N	\N	\N	\N	\N	0	\N	\N	\N	Time corrected. Related files: 00000425-00000432	\N	404	0	\N	\N	\N	\N
436	15	\N	\N	retained	\N	\N	\N	\N	\N	0	\N	\N	\N	Time corrected. Related files: 00000425-00000432	\N	405	0	\N	\N	\N	\N
437	15	\N	\N	retained	\N	\N	\N	\N	\N	0	\N	\N	\N	Time corrected. Related files: 00000425-00000432	\N	406	0	\N	\N	\N	\N
438	15	\N	\N	retained	\N	\N	\N	\N	\N	0	\N	\N	\N	Time corrected. Related files: 00000425-00000432	\N	407	0	\N	\N	\N	\N
439	15	\N	\N	retained	\N	\N	\N	\N	\N	0	\N	\N	\N	Time corrected. Related files: 00000425-00000432	\N	408	0	\N	\N	\N	\N
440	15	\N	\N	retained	\N	\N	\N	\N	\N	0	\N	\N	\N	Time corrected. Related files: 00000425-00000432	\N	409	0	\N	\N	\N	\N
441	15	\N	\N	retained	\N	\N	\N	\N	\N	0	\N	\N	\N	Time corrected. Related files: 00000433-00000437	\N	410	0	\N	\N	\N	\N
442	15	\N	\N	retained	\N	\N	\N	\N	\N	0	\N	\N	\N	Time corrected. Related files: 00000433-00000437	\N	411	0	\N	\N	\N	\N
443	15	\N	\N	retained	\N	\N	\N	\N	\N	0	\N	\N	\N	Time corrected. Related files: 00000433-00000437	\N	412	0	\N	\N	\N	\N
444	15	\N	\N	retained	\N	\N	\N	\N	\N	0	\N	\N	\N	Time corrected. Related files: 00000433-00000437	\N	413	0	\N	\N	\N	\N
445	15	\N	\N	retained	\N	\N	\N	\N	\N	0	\N	\N	\N	Time corrected. Related files: 00000433-00000437	\N	414	0	\N	\N	\N	\N
446	15	\N	\N	retained	\N	\N	\N	\N	\N	0	\N	\N	\N	Time corrected. Related files: 00000438-00000440	\N	415	0	\N	\N	\N	\N
447	15	\N	\N	retained	\N	\N	\N	\N	\N	0	\N	\N	\N	Time corrected. Related files: 00000438-00000440	\N	416	0	\N	\N	\N	\N
448	15	\N	\N	retained	\N	\N	\N	\N	\N	0	\N	\N	\N	Time corrected. Related files: 00000438-00000440	\N	417	0	\N	\N	\N	\N
449	15	\N	\N	retained	\N	\N	\N	\N	\N	0	\N	\N	\N	Time corrected. Related files: 00000441-00000443	\N	418	0	\N	\N	\N	\N
450	15	\N	\N	retained	\N	\N	\N	\N	\N	0	\N	\N	\N	Time corrected. Related files: 00000441-00000443	\N	419	0	\N	\N	\N	\N
451	15	\N	\N	retained	\N	\N	\N	\N	\N	0	\N	\N	\N	Time corrected. Related files: 00000441-00000443	\N	420	0	\N	\N	\N	\N
452	15	\N	\N	retained	\N	\N	\N	\N	\N	0	\N	\N	\N	\N	\N	421	0	\N	\N	\N	\N
453	15	\N	\N	retained	\N	\N	\N	\N	\N	0	\N	\N	\N	\N	\N	422	0	\N	\N	\N	\N
454	15	\N	\N	retained	\N	\N	\N	\N	\N	0	\N	\N	\N	\N	\N	423	0	\N	\N	\N	\N
455	15	\N	\N	retained	\N	\N	\N	\N	\N	0	\N	\N	\N	\N	\N	424	0	\N	\N	\N	\N
456	15	\N	\N	retained	\N	\N	\N	\N	\N	0	\N	\N	\N	\N	\N	425	0	\N	\N	\N	\N
457	15	\N	\N	retained	\N	\N	\N	\N	\N	0	\N	\N	\N	\N	\N	426	0	\N	\N	\N	\N
458	15	\N	\N	retained	\N	\N	\N	\N	\N	0	\N	\N	\N	\N	\N	427	0	\N	\N	\N	\N
459	15	\N	\N	retained	\N	\N	\N	\N	\N	0	\N	\N	\N	\N	\N	428	0	\N	\N	\N	\N
460	15	\N	\N	retained	\N	\N	\N	\N	\N	0	\N	\N	\N	\N	\N	429	0	\N	\N	\N	\N
461	15	\N	\N	retained	\N	\N	\N	\N	\N	0	\N	\N	\N	\N	\N	430	0	\N	\N	\N	\N
462	15	\N	\N	retained	\N	\N	\N	\N	\N	0	\N	\N	\N	\N	\N	431	0	\N	\N	\N	\N
463	15	\N	\N	retained	\N	\N	\N	\N	\N	0	\N	\N	\N	\N	\N	432	0	\N	\N	\N	\N
464	15	\N	\N	retained	\N	\N	\N	\N	\N	0	\N	\N	\N	\N	\N	433	0	\N	\N	\N	\N
465	15	\N	\N	retained	\N	\N	\N	\N	\N	0	\N	\N	\N	\N	\N	434	0	\N	\N	\N	\N
466	15	\N	\N	retained	\N	\N	\N	\N	\N	0	\N	\N	\N	\N	\N	435	0	\N	\N	\N	\N
467	15	\N	\N	retained	\N	\N	\N	\N	\N	0	\N	\N	\N	\N	\N	436	0	\N	\N	\N	\N
468	15	\N	\N	retained	\N	\N	\N	\N	\N	0	\N	\N	\N	\N	\N	437	0	\N	\N	\N	\N
469	15	\N	\N	retained	\N	\N	\N	\N	\N	0	\N	\N	\N	\N	\N	438	0	\N	\N	\N	\N
470	15	\N	\N	retained	\N	\N	\N	\N	\N	0	\N	\N	\N	\N	\N	439	0	\N	\N	\N	\N
471	15	\N	\N	retained	\N	\N	\N	\N	\N	0	\N	\N	\N	\N	\N	440	0	\N	\N	\N	\N
472	15	\N	\N	retained	\N	\N	\N	\N	\N	0	\N	\N	\N	\N	\N	441	0	\N	\N	\N	\N
473	15	\N	\N	retained	\N	\N	\N	\N	\N	0	\N	\N	\N	\N	\N	442	0	\N	\N	\N	\N
474	15	\N	\N	retained	\N	\N	\N	\N	\N	0	\N	\N	\N	\N	\N	443	0	\N	\N	\N	\N
475	15	\N	\N	retained	\N	\N	\N	\N	\N	0	\N	\N	\N	\N	\N	444	0	\N	\N	\N	\N
476	15	\N	\N	retained	\N	\N	\N	\N	\N	0	\N	\N	\N	\N	\N	445	0	\N	\N	\N	\N
477	15	\N	\N	retained	\N	\N	\N	\N	\N	0	\N	\N	\N	\N	\N	446	0	\N	\N	\N	\N
478	15	\N	\N	retained	\N	\N	\N	\N	\N	0	\N	\N	\N	\N	\N	447	0	\N	\N	\N	\N
479	15	\N	\N	retained	\N	\N	\N	\N	\N	0	\N	\N	\N	\N	\N	448	0	\N	\N	\N	\N
480	15	\N	\N	retained	\N	\N	\N	\N	\N	0	\N	\N	\N	\N	\N	449	0	\N	\N	\N	\N
481	15	\N	\N	retained	\N	\N	\N	\N	\N	0	\N	\N	\N	\N	\N	450	0	\N	\N	\N	\N
482	15	\N	\N	retained	\N	\N	\N	\N	\N	0	\N	\N	\N	\N	\N	451	0	\N	\N	\N	\N
483	15	\N	\N	retained	\N	\N	\N	\N	\N	0	\N	\N	\N	\N	\N	452	0	\N	\N	\N	\N
484	15	\N	\N	retained	\N	\N	\N	\N	\N	0	\N	\N	\N	\N	\N	453	0	\N	\N	\N	\N
485	15	\N	\N	retained	\N	\N	\N	\N	\N	0	\N	\N	\N	\N	\N	454	0	\N	\N	\N	\N
486	15	\N	\N	retained	\N	\N	\N	\N	\N	0	\N	\N	\N	\N	\N	455	0	\N	\N	\N	\N
487	15	\N	\N	retained	\N	\N	\N	\N	\N	0	\N	\N	\N	\N	\N	456	0	\N	\N	\N	\N
488	15	\N	\N	retained	\N	\N	\N	\N	\N	0	\N	\N	\N	\N	\N	457	0	\N	\N	\N	\N
489	15	\N	\N	retained	\N	\N	\N	\N	\N	0	\N	\N	\N	\N	\N	458	0	\N	\N	\N	\N
490	15	\N	\N	retained	\N	\N	\N	\N	\N	0	\N	\N	\N	\N	\N	459	0	\N	\N	\N	\N
491	14	\N	\N	retained	\N	\N	\N	\N	\N	0	\N	\N	\N	Related files: 00000484-00000485.	\N	460	0	\N	\N	\N	\N
492	14	\N	\N	retained	\N	\N	\N	\N	\N	0	\N	\N	\N	Related files: 00000484-00000485.	\N	461	0	\N	\N	\N	\N
493	13	\N	\N	retained	\N	\N	\N	\N	\N	0	\N	\N	\N	\N	\N	462	0	\N	\N	\N	\N
494	13	\N	\N	retained	\N	\N	\N	\N	\N	0	\N	\N	\N	\N	\N	463	0	\N	\N	\N	\N
495	13	\N	\N	retained	\N	\N	\N	\N	\N	0	\N	\N	\N	\N	\N	464	0	\N	\N	\N	\N
496	15	\N	\N	retained	\N	\N	\N	\N	\N	0	\N	\N	\N	\N	\N	465	0	\N	\N	\N	\N
497	15	\N	\N	retained	\N	\N	\N	\N	\N	0	\N	\N	\N	\N	\N	466	0	\N	\N	\N	\N
498	15	\N	\N	retained	\N	\N	\N	\N	\N	0	\N	\N	\N	\N	\N	467	0	\N	\N	\N	\N
499	15	\N	\N	retained	\N	\N	\N	\N	\N	0	\N	\N	\N	\N	\N	468	0	\N	\N	\N	\N
500	15	\N	\N	retained	\N	\N	\N	\N	\N	0	\N	\N	\N	\N	\N	469	0	\N	\N	\N	\N
501	15	\N	\N	retained	\N	\N	\N	\N	\N	0	\N	\N	\N	\N	\N	470	0	\N	\N	\N	\N
502	15	\N	\N	retained	\N	\N	\N	\N	\N	0	\N	\N	\N	\N	\N	471	0	\N	\N	\N	\N
503	15	\N	\N	retained	\N	\N	\N	\N	\N	0	\N	\N	\N	\N	\N	472	0	\N	\N	\N	\N
504	15	\N	\N	retained	\N	\N	\N	\N	\N	0	\N	\N	\N	\N	\N	473	0	\N	\N	\N	\N
505	15	\N	\N	retained	\N	\N	\N	\N	\N	0	\N	\N	\N	\N	\N	474	0	\N	\N	\N	\N
506	15	\N	\N	retained	\N	\N	\N	\N	\N	0	\N	\N	\N	\N	\N	475	0	\N	\N	\N	\N
507	15	\N	\N	retained	\N	\N	\N	\N	\N	0	\N	\N	\N	\N	\N	476	0	\N	\N	\N	\N
508	15	\N	\N	retained	\N	\N	\N	\N	\N	0	\N	\N	\N	\N	\N	477	0	\N	\N	\N	\N
509	14	\N	\N	retained	\N	\N	\N	\N	\N	0	\N	\N	\N	Related files: 00000502-00000506	\N	478	0	\N	\N	\N	\N
510	14	\N	\N	retained	\N	\N	\N	\N	\N	0	\N	\N	\N	Related files: 00000502-00000506	\N	479	0	\N	\N	\N	\N
511	14	\N	\N	retained	\N	\N	\N	\N	\N	0	\N	\N	\N	Related files: 00000504-00000505	\N	480	0	\N	\N	\N	\N
512	14	\N	\N	retained	\N	\N	\N	\N	\N	0	\N	\N	\N	Related files: 00000504-00000505	\N	481	0	\N	\N	\N	\N
513	14	\N	\N	retained	\N	\N	\N	\N	\N	0	\N	\N	\N	Related files: 00000502-00000506;	\N	482	0	\N	\N	\N	\N
514	14	\N	\N	retained	\N	\N	\N	\N	\N	0	\N	\N	\N	\N	\N	483	0	\N	\N	\N	\N
515	14	\N	\N	retained	\N	\N	\N	\N	\N	0	\N	\N	\N	Related files: 00000508-00000509	\N	484	0	\N	\N	\N	\N
516	14	\N	\N	retained	\N	\N	\N	\N	\N	0	\N	\N	\N	Related files: 00000508-00000509.	\N	485	0	\N	\N	\N	\N
517	14	\N	\N	retained	\N	\N	\N	\N	\N	0	\N	\N	\N	Related files: 00000510-00000511	\N	486	0	\N	\N	\N	\N
518	14	\N	\N	retained	\N	\N	\N	\N	\N	0	\N	\N	\N	Related files: 00000510-00000511	\N	487	0	\N	\N	\N	\N
519	14	\N	\N	retained	\N	\N	\N	\N	\N	0	\N	\N	\N	Related files: 00000512-00000513	\N	488	0	\N	\N	\N	\N
520	14	\N	\N	retained	\N	\N	\N	\N	\N	0	\N	\N	\N	Related files: 00000512-00000513	\N	489	0	\N	\N	\N	\N
521	14	\N	\N	retained	\N	\N	\N	\N	\N	0	\N	\N	\N	 00000514-00000515	\N	490	0	\N	\N	\N	\N
522	14	\N	\N	retained	\N	\N	\N	\N	\N	0	\N	\N	\N	00000514-00000515	\N	491	0	\N	\N	\N	\N
523	15	\N	\N	retained	\N	\N	\N	\N	\N	0	\N	\N	\N	\N	\N	492	0	\N	\N	\N	\N
524	15	\N	\N	retained	\N	\N	\N	\N	\N	0	\N	\N	\N	\N	\N	493	0	\N	\N	\N	\N
525	15	\N	\N	retained	\N	\N	\N	\N	\N	0	\N	\N	\N	\N	\N	494	0	\N	\N	\N	\N
526	15	\N	\N	retained	\N	\N	\N	\N	\N	0	\N	\N	\N	\N	\N	495	0	\N	\N	\N	\N
527	15	\N	\N	retained	\N	\N	\N	\N	\N	0	\N	\N	\N	\N	\N	496	0	\N	\N	\N	\N
528	15	\N	\N	retained	\N	\N	\N	\N	\N	0	\N	\N	\N	\N	\N	497	0	\N	\N	\N	\N
529	15	\N	\N	retained	\N	\N	\N	\N	\N	0	\N	\N	\N	\N	\N	498	0	\N	\N	\N	\N
530	15	\N	\N	retained	\N	\N	\N	\N	\N	0	\N	\N	\N	\N	\N	499	0	\N	\N	\N	\N
531	15	\N	\N	retained	\N	\N	\N	\N	\N	0	\N	\N	\N	\N	\N	500	0	\N	\N	\N	\N
532	15	\N	\N	retained	\N	\N	\N	\N	\N	0	\N	\N	\N	\N	\N	501	0	\N	\N	\N	\N
533	15	\N	\N	retained	\N	\N	\N	\N	\N	0	\N	\N	\N	\N	\N	502	0	\N	\N	\N	\N
534	15	\N	\N	retained	\N	\N	\N	\N	\N	0	\N	\N	\N	\N	\N	503	0	\N	\N	\N	\N
535	14	\N	\N	retained	\N	\N	\N	\N	\N	0	\N	\N	\N	Related files: 00000528-00000529	\N	504	0	\N	\N	\N	\N
536	14	\N	\N	retained	\N	\N	\N	\N	\N	0	\N	\N	\N	Related files: 00000528-00000529	\N	505	0	\N	\N	\N	\N
537	14	\N	\N	retained	\N	\N	\N	\N	\N	0	\N	\N	\N	may be duplicate interview on 00000540-00000542	\N	506	0	\N	\N	\N	\N
538	14	\N	\N	retained	\N	\N	\N	\N	\N	0	\N	\N	\N	Related files: 00000531-00000533	\N	507	0	\N	\N	\N	\N
539	14	\N	\N	retained	\N	\N	\N	\N	\N	0	\N	\N	\N	Related files: 00000531-00000533	\N	508	0	\N	\N	\N	\N
540	14	\N	\N	retained	\N	\N	\N	\N	\N	0	\N	\N	\N	Related files: 00000531-00000533	\N	509	0	\N	\N	\N	\N
541	15	\N	\N	retained	\N	\N	\N	\N	\N	0	\N	\N	\N	\N	\N	510	0	\N	\N	\N	\N
542	15	\N	\N	retained	\N	\N	\N	\N	\N	0	\N	\N	\N	\N	\N	511	0	\N	\N	\N	\N
543	15	\N	\N	retained	\N	\N	\N	\N	\N	0	\N	\N	\N	\N	\N	512	0	\N	\N	\N	\N
544	15	\N	\N	retained	\N	\N	\N	\N	\N	0	\N	\N	\N	\N	\N	513	0	\N	\N	\N	\N
545	15	\N	\N	retained	\N	\N	\N	\N	\N	0	\N	\N	\N	\N	\N	514	0	\N	\N	\N	\N
546	15	\N	\N	retained	\N	\N	\N	\N	\N	0	\N	\N	\N	\N	\N	515	0	\N	\N	\N	\N
547	14	\N	\N	retained	\N	\N	\N	\N	\N	0	\N	\N	\N	Related files: 00000540-00000542, 00000530 (may be duplicate)	\N	516	0	\N	\N	\N	\N
548	14	\N	\N	retained	\N	\N	\N	\N	\N	0	\N	\N	\N	Related files: 00000540-00000542, 00000530 (may be duplicate)	\N	517	0	\N	\N	\N	\N
549	14	\N	\N	retained	\N	\N	\N	\N	\N	0	\N	\N	\N	 Related files: 00000540-00000542, 00000530 (may be duplicate)	\N	518	0	\N	\N	\N	\N
550	14	\N	\N	retained	\N	\N	\N	\N	\N	0	\N	\N	\N	Related files: 00000543-00000544	\N	519	0	\N	\N	\N	\N
551	14	\N	\N	retained	\N	\N	\N	\N	\N	0	\N	\N	\N	Related files: 00000543-00000544	\N	520	0	\N	\N	\N	\N
552	14	\N	\N	retained	\N	\N	\N	\N	\N	0	\N	\N	\N	Related file names: 00000545-00000559	\N	521	0	\N	\N	\N	\N
553	14	\N	\N	retained	\N	\N	\N	\N	\N	0	\N	\N	\N	Related file names: 00000546-00000547	\N	522	0	\N	\N	\N	\N
554	14	\N	\N	retained	\N	\N	\N	\N	\N	0	\N	\N	\N	Related file names: 00000546-00000547	\N	523	0	\N	\N	\N	\N
555	14	\N	\N	retained	\N	\N	\N	\N	\N	0	\N	\N	\N	Related file names: 00000548-00000549	\N	524	0	\N	\N	\N	\N
556	14	\N	\N	retained	\N	\N	\N	\N	\N	0	\N	\N	\N	Related file names: 00000548-00000549	\N	525	0	\N	\N	\N	\N
557	14	\N	\N	retained	\N	\N	\N	\N	\N	0	\N	\N	\N	00000550-00000551	\N	526	0	\N	\N	\N	\N
558	14	\N	\N	retained	\N	\N	\N	\N	\N	0	\N	\N	\N	Related files: 00000550-00000551	\N	527	0	\N	\N	\N	\N
559	14	\N	\N	retained	\N	\N	\N	\N	\N	0	\N	\N	\N	\N	\N	528	0	\N	\N	\N	\N
560	14	\N	\N	retained	\N	\N	\N	\N	\N	0	\N	\N	\N	00000548-00000549, 00000553-00000554	\N	529	0	\N	\N	\N	\N
561	14	\N	\N	retained	\N	\N	\N	\N	\N	0	\N	\N	\N	00000548-00000549, 00000553-00000554	\N	530	0	\N	\N	\N	\N
562	14	\N	\N	retained	\N	\N	\N	\N	\N	0	\N	\N	\N	Related file names: 00000555-00000556	\N	531	0	\N	\N	\N	\N
563	14	\N	\N	retained	\N	\N	\N	\N	\N	0	\N	\N	\N	Related file names: 00000555- 00000556	\N	532	0	\N	\N	\N	\N
564	14	\N	\N	retained	\N	\N	\N	\N	\N	0	\N	\N	\N	\N	\N	533	0	\N	\N	\N	\N
565	14	\N	\N	retained	\N	\N	\N	\N	\N	0	\N	\N	\N	\N	\N	534	0	\N	\N	\N	\N
566	14	\N	\N	retained	\N	\N	\N	\N	\N	0	\N	\N	\N	Related file names: 00000545-00000559	\N	535	0	\N	\N	\N	\N
567	14	\N	\N	retained	\N	\N	\N	\N	\N	0	\N	\N	\N	Related file names: 00000560-00000561	\N	536	0	\N	\N	\N	\N
568	14	\N	\N	retained	\N	\N	\N	\N	\N	0	\N	\N	\N	Related file names: 00000560-00000561	\N	537	0	\N	\N	\N	\N
569	14	\N	\N	retained	\N	\N	\N	\N	\N	0	\N	\N	\N	Related file names: 00000562-00000563	\N	538	0	\N	\N	\N	\N
570	14	\N	\N	retained	\N	\N	\N	\N	\N	0	\N	\N	\N	Related file names: 00000562-00000563	\N	539	0	\N	\N	\N	\N
571	14	\N	\N	retained	\N	\N	\N	\N	\N	0	\N	\N	\N	\N	\N	540	0	\N	\N	\N	\N
572	14	\N	\N	retained	\N	\N	\N	\N	\N	0	\N	\N	\N	Related file names: 00000565-00000567	\N	541	0	\N	\N	\N	\N
573	14	\N	\N	retained	\N	\N	\N	\N	\N	0	\N	\N	\N	Related file names: 00000565-00000567	\N	542	0	\N	\N	\N	\N
574	14	\N	\N	retained	\N	\N	\N	\N	\N	0	\N	\N	\N	Related file names: 00000565-00000567	\N	543	0	\N	\N	\N	\N
575	14	\N	\N	retained	\N	\N	\N	\N	\N	0	\N	\N	\N	Related file names: 00000568-00000569	\N	544	0	\N	\N	\N	\N
576	14	\N	\N	retained	\N	\N	\N	\N	\N	0	\N	\N	\N	Related file names: 00000568-00000569	\N	545	0	\N	\N	\N	\N
577	14	\N	\N	retained	\N	\N	\N	\N	\N	0	\N	\N	\N	Related file names: 00000570-00000571	\N	546	0	\N	\N	\N	\N
578	14	\N	\N	retained	\N	\N	\N	\N	\N	0	\N	\N	\N	Related file names: 00000570-00000571	\N	547	0	\N	\N	\N	\N
579	14	\N	\N	retained	\N	\N	\N	\N	\N	0	\N	\N	\N	Related file names: 00000572-00000573	\N	548	0	\N	\N	\N	\N
580	14	\N	\N	retained	\N	\N	\N	\N	\N	0	\N	\N	\N	Related file names: 00000572-00000573	\N	549	0	\N	\N	\N	\N
581	14	\N	\N	retained	\N	\N	\N	\N	\N	0	\N	\N	\N	Related file names: 00000574-00000576,	\N	550	0	\N	\N	\N	\N
582	14	\N	\N	retained	\N	\N	\N	\N	\N	0	\N	\N	\N	Related file names: 00000574-00000576,	\N	551	0	\N	\N	\N	\N
583	14	\N	\N	retained	\N	\N	\N	\N	\N	0	\N	\N	\N	Related file names: 00000574-00000576,	\N	552	0	\N	\N	\N	\N
584	14	\N	\N	retained	\N	\N	\N	\N	\N	0	\N	\N	\N	\N	\N	553	0	\N	\N	\N	\N
585	14	\N	\N	retained	\N	\N	\N	\N	\N	0	\N	\N	\N	Related file names: 000005784-00000579	\N	554	0	\N	\N	\N	\N
586	14	\N	\N	retained	\N	\N	\N	\N	\N	0	\N	\N	\N	Related file names: 00000578-00000579	\N	555	0	\N	\N	\N	\N
587	14	\N	\N	retained	\N	\N	\N	\N	\N	0	\N	\N	\N	\N	\N	556	0	\N	\N	\N	\N
588	14	\N	\N	retained	\N	\N	\N	\N	\N	0	\N	\N	\N	\N	\N	557	0	\N	\N	\N	\N
589	14	\N	\N	retained	\N	\N	\N	\N	\N	0	\N	\N	\N	\N	\N	558	0	\N	\N	\N	\N
590	14	\N	\N	retained	\N	\N	\N	\N	\N	0	\N	\N	\N	\N	\N	559	0	\N	\N	\N	\N
591	14	\N	\N	retained	\N	\N	\N	\N	\N	0	\N	\N	\N	\N	\N	560	0	\N	\N	\N	\N
592	14	\N	\N	retained	\N	\N	\N	\N	\N	0	\N	\N	\N	\N	\N	561	0	\N	\N	\N	\N
593	14	\N	\N	retained	\N	\N	\N	\N	\N	0	\N	\N	\N	\N	\N	562	0	\N	\N	\N	\N
594	14	\N	\N	retained	\N	\N	\N	\N	\N	0	\N	\N	\N	\N	\N	563	0	\N	\N	\N	\N
595	14	\N	\N	retained	\N	\N	\N	\N	\N	0	\N	\N	\N	\N	\N	564	0	\N	\N	\N	\N
596	14	\N	\N	retained	\N	\N	\N	\N	\N	0	\N	\N	\N	\N	\N	565	0	\N	\N	\N	\N
597	14	\N	\N	retained	\N	\N	\N	\N	\N	0	\N	\N	\N	\N	\N	566	0	\N	\N	\N	\N
598	14	\N	\N	retained	\N	\N	\N	\N	\N	0	\N	\N	\N	\N	\N	567	0	\N	\N	\N	\N
599	14	\N	\N	retained	\N	\N	\N	\N	\N	0	\N	\N	\N	\N	\N	568	0	\N	\N	\N	\N
600	14	\N	\N	retained	\N	\N	\N	\N	\N	0	\N	\N	\N	\N	\N	569	0	\N	\N	\N	\N
601	14	\N	\N	retained	\N	\N	\N	\N	\N	0	\N	\N	\N	\N	\N	570	0	\N	\N	\N	\N
602	14	\N	\N	retained	\N	\N	\N	\N	\N	0	\N	\N	\N	\N	\N	571	0	\N	\N	\N	\N
603	14	\N	\N	retained	\N	\N	\N	\N	\N	0	\N	\N	\N	\N	\N	572	0	\N	\N	\N	\N
604	14	\N	\N	retained	\N	\N	\N	\N	\N	0	\N	\N	\N	\N	\N	573	0	\N	\N	\N	\N
605	14	\N	\N	retained	\N	\N	\N	\N	\N	0	\N	\N	\N	\N	\N	574	0	\N	\N	\N	\N
606	14	\N	\N	retained	\N	\N	\N	\N	\N	0	\N	\N	\N	\N	\N	575	0	\N	\N	\N	\N
607	114	\N	\N	retained	\N	\N	\N	\N	\N	0	\N	\N	\N	\N	\N	576	0	\N	\N	\N	\N
608	12	\N	\N	retained	\N	\N	\N	\N	\N	0	\N	\N	\N	\N	\N	577	0	\N	\N	\N	\N
609	12	\N	\N	retained	\N	\N	\N	\N	\N	0	\N	\N	\N	\N	\N	578	0	\N	\N	\N	\N
610	14	\N	\N	retained	\N	\N	\N	\N	\N	0	\N	\N	\N	\N	\N	579	0	\N	\N	\N	\N
611	14	\N	\N	retained	\N	\N	\N	\N	\N	0	\N	\N	\N	\N	\N	580	0	\N	\N	\N	\N
612	14	\N	\N	retained	\N	\N	\N	\N	\N	0	\N	\N	\N	\N	\N	581	0	\N	\N	\N	\N
613	14	\N	\N	retained	\N	\N	\N	\N	\N	0	\N	\N	\N	\N	\N	582	0	\N	\N	\N	\N
614	14	\N	\N	retained	\N	\N	\N	\N	\N	0	\N	\N	\N	\N	\N	583	0	\N	\N	\N	\N
615	14	\N	\N	retained	\N	\N	\N	\N	\N	0	\N	\N	\N	Related files: 00000608-00000609	\N	584	0	\N	\N	\N	\N
616	14	\N	\N	retained	\N	\N	\N	\N	\N	0	\N	\N	\N	Related files: 00000608-00000609	\N	585	0	\N	\N	\N	\N
617	14	\N	\N	retained	\N	\N	\N	\N	\N	0	\N	\N	\N	Related files: 00000610-00000611	\N	586	0	\N	\N	\N	\N
618	14	\N	\N	retained	\N	\N	\N	\N	\N	0	\N	\N	\N	Related files: 00000610-00000611	\N	587	0	\N	\N	\N	\N
619	14	\N	\N	retained	\N	\N	\N	\N	\N	0	\N	\N	\N	Related files: 00000279-00000280, 00000612	\N	588	0	\N	\N	\N	\N
620	14	\N	\N	retained	\N	\N	\N	\N	\N	0	\N	\N	\N	\N	\N	589	0	\N	\N	\N	\N
621	14	\N	\N	retained	\N	\N	\N	\N	\N	0	\N	\N	\N	Related files: 00000614, 00000635	\N	590	0	\N	\N	\N	\N
622	14	\N	\N	retained	\N	\N	\N	\N	\N	0	\N	\N	\N	related files: 00000615-00000616, 00000625-00000626	\N	591	0	\N	\N	\N	\N
623	14	\N	\N	retained	\N	\N	\N	\N	\N	0	\N	\N	\N	Related files: 00000615-00000616, 00000625-00000626	\N	592	0	\N	\N	\N	\N
624	14	\N	\N	retained	\N	\N	\N	\N	\N	0	\N	\N	\N	\N	\N	593	0	\N	\N	\N	\N
625	14	\N	\N	retained	\N	\N	\N	\N	\N	0	\N	\N	\N	\N	\N	594	0	\N	\N	\N	\N
626	14	\N	\N	retained	\N	\N	\N	\N	\N	0	\N	\N	\N	\N	\N	595	0	\N	\N	\N	\N
627	14	\N	\N	retained	\N	\N	\N	\N	\N	0	\N	\N	\N	\N	\N	596	0	\N	\N	\N	\N
628	14	\N	\N	retained	\N	\N	\N	\N	\N	0	\N	\N	\N	\N	\N	597	0	\N	\N	\N	\N
629	14	\N	\N	retained	\N	\N	\N	\N	\N	0	\N	\N	\N	\N	\N	598	0	\N	\N	\N	\N
630	14	\N	\N	retained	\N	\N	\N	\N	\N	0	\N	\N	\N	Related files: 00000623-00000624	\N	599	0	\N	\N	\N	\N
631	14	\N	\N	retained	\N	\N	\N	\N	\N	0	\N	\N	\N	Related files: 00000623-00000624	\N	600	0	\N	\N	\N	\N
632	14	\N	\N	retained	\N	\N	\N	\N	\N	0	\N	\N	\N	Related file 00000615-00000616-00000625-00000626,	\N	601	0	\N	\N	\N	\N
633	14	\N	\N	retained	\N	\N	\N	\N	\N	0	\N	\N	\N	related files: 00000615-00000616, 00000625-00000626	\N	602	0	\N	\N	\N	\N
634	15	\N	\N	retained	\N	\N	\N	\N	\N	0	\N	\N	\N	\N	\N	603	0	\N	\N	\N	\N
635	15	\N	\N	retained	\N	\N	\N	\N	\N	0	\N	\N	\N	\N	\N	604	0	\N	\N	\N	\N
636	15	\N	\N	retained	\N	\N	\N	\N	\N	0	\N	\N	\N	\N	\N	605	0	\N	\N	\N	\N
637	15	\N	\N	retained	\N	\N	\N	\N	\N	0	\N	\N	\N	\N	\N	606	0	\N	\N	\N	\N
638	15	\N	\N	retained	\N	\N	\N	\N	\N	0	\N	\N	\N	\N	\N	607	0	\N	\N	\N	\N
639	15	\N	\N	retained	\N	\N	\N	\N	\N	0	\N	\N	\N	\N	\N	608	0	\N	\N	\N	\N
640	15	\N	\N	retained	\N	\N	\N	\N	\N	0	\N	\N	\N	\N	\N	609	0	\N	\N	\N	\N
641	15	\N	\N	retained	\N	\N	\N	\N	\N	0	\N	\N	\N	\N	\N	610	0	\N	\N	\N	\N
642	14	\N	\N	retained	\N	\N	\N	\N	\N	0	\N	\N	\N	Related files: 00000614, 00000635	\N	611	0	\N	\N	\N	\N
643	14	\N	\N	retained	\N	\N	\N	\N	\N	0	\N	\N	\N	\N	\N	612	0	\N	\N	\N	\N
644	14	\N	\N	retained	\N	\N	\N	\N	\N	0	\N	\N	\N	Related files: 00000103-00000104, 00000637.	\N	613	0	\N	\N	\N	\N
645	14	\N	\N	retained	\N	\N	\N	\N	\N	0	\N	\N	\N	Related files: 00000638-00000639	\N	614	0	\N	\N	\N	\N
646	14	\N	\N	retained	\N	\N	\N	\N	\N	0	\N	\N	\N	Related files: 00000638-00000639	\N	615	0	\N	\N	\N	\N
647	14	\N	\N	retained	\N	\N	\N	\N	\N	0	\N	\N	\N	Related files: 00000640, 00000709, 00000711	\N	616	0	\N	\N	\N	\N
648	14	\N	\N	retained	\N	\N	\N	\N	\N	0	\N	\N	\N	Related file 0000064--00000646	\N	617	0	\N	\N	\N	\N
649	14	\N	\N	retained	\N	\N	\N	\N	\N	0	\N	\N	\N	Related files 00000641-00000646	\N	618	0	\N	\N	\N	\N
650	14	\N	\N	retained	\N	\N	\N	\N	\N	0	\N	\N	\N	Related files 00000641-00000646	\N	619	0	\N	\N	\N	\N
651	14	\N	\N	retained	\N	\N	\N	\N	\N	0	\N	\N	\N	Related files 00000641-00000646	\N	620	0	\N	\N	\N	\N
652	14	\N	\N	retained	\N	\N	\N	\N	\N	0	\N	\N	\N	Related files 00000641-00000646	\N	621	0	\N	\N	\N	\N
653	14	\N	\N	retained	\N	\N	\N	\N	\N	0	\N	\N	\N	Related files 00000641-00000646	\N	622	0	\N	\N	\N	\N
654	115	\N	\N	retained	\N	\N	\N	\N	\N	0	\N	\N	\N	\N	\N	623	0	\N	\N	\N	\N
655	115	\N	\N	retained	\N	\N	\N	\N	\N	0	\N	\N	\N	\N	\N	624	0	\N	\N	\N	\N
656	14	\N	\N	retained	\N	\N	\N	\N	\N	0	\N	\N	\N	\N	\N	625	0	\N	\N	\N	\N
657	14	\N	\N	retained	\N	\N	\N	\N	\N	0	\N	\N	\N	Related files 00000641-00000646, 00000650-00000653	\N	626	0	\N	\N	\N	\N
658	14	\N	\N	retained	\N	\N	\N	\N	\N	0	\N	\N	\N	Related files 00000641-00000646, 00000650-00000653	\N	627	0	\N	\N	\N	\N
659	14	\N	\N	retained	\N	\N	\N	\N	\N	0	\N	\N	\N	Related files 00000641-00000646, 00000650-00000653	\N	628	0	\N	\N	\N	\N
660	14	\N	\N	retained	\N	\N	\N	\N	\N	0	\N	\N	\N	Related files 00000641-00000646, 00000650-00000653	\N	629	0	\N	\N	\N	\N
661	14	\N	\N	retained	\N	\N	\N	\N	\N	0	\N	\N	\N	00000654, 00000666	\N	630	0	\N	\N	\N	\N
662	116	\N	\N	retained	\N	\N	\N	\N	\N	0	\N	\N	\N	\N	\N	631	0	\N	\N	\N	\N
663	14	\N	\N	retained	\N	\N	\N	\N	\N	0	\N	\N	\N	00000656-00000659	\N	632	0	\N	\N	\N	\N
664	14	\N	\N	retained	\N	\N	\N	\N	\N	0	\N	\N	\N	00000656-00000659	\N	633	0	\N	\N	\N	\N
665	14	\N	\N	retained	\N	\N	\N	\N	\N	0	\N	\N	\N	00000656-00000659	\N	634	0	\N	\N	\N	\N
666	14	\N	\N	retained	\N	\N	\N	\N	\N	0	\N	\N	\N	00000656-00000659	\N	635	0	\N	\N	\N	\N
667	14	\N	\N	retained	\N	\N	\N	\N	\N	0	\N	\N	\N	00000660-00000661	\N	636	0	\N	\N	\N	\N
668	14	\N	\N	retained	\N	\N	\N	\N	\N	0	\N	\N	\N	00000660-00000661	\N	637	0	\N	\N	\N	\N
669	14	\N	\N	retained	\N	\N	\N	\N	\N	0	\N	\N	\N	00000661-00000662	\N	638	0	\N	\N	\N	\N
670	14	\N	\N	retained	\N	\N	\N	\N	\N	0	\N	\N	\N	\N	\N	639	0	\N	\N	\N	\N
671	14	\N	\N	retained	\N	\N	\N	\N	\N	0	\N	\N	\N	\N	\N	640	0	\N	\N	\N	\N
672	14	\N	\N	retained	\N	\N	\N	\N	\N	0	\N	\N	\N	\N	\N	641	0	\N	\N	\N	\N
673	14	\N	\N	retained	\N	\N	\N	\N	\N	0	\N	\N	\N	\N	\N	642	0	\N	\N	\N	\N
674	14	\N	\N	retained	\N	\N	\N	\N	\N	0	\N	\N	\N	00000667-00000668	\N	643	0	\N	\N	\N	\N
675	14	\N	\N	retained	\N	\N	\N	\N	\N	0	\N	\N	\N	00000667-00000668	\N	644	0	\N	\N	\N	\N
676	14	\N	\N	retained	\N	\N	\N	\N	\N	0	\N	\N	\N	\N	\N	645	0	\N	\N	\N	\N
677	14	\N	\N	retained	\N	\N	\N	\N	\N	0	\N	\N	\N	\N	\N	646	0	\N	\N	\N	\N
678	14	\N	\N	retained	\N	\N	\N	\N	\N	0	\N	\N	\N	\N	\N	647	0	\N	\N	\N	\N
679	14	\N	\N	retained	\N	\N	\N	\N	\N	0	\N	\N	\N	\N	\N	648	0	\N	\N	\N	\N
680	14	\N	\N	retained	\N	\N	\N	\N	\N	0	\N	\N	\N	\N	\N	649	0	\N	\N	\N	\N
681	14	\N	\N	retained	\N	\N	\N	\N	\N	0	\N	\N	\N	\N	\N	650	0	\N	\N	\N	\N
682	14	\N	\N	retained	\N	\N	\N	\N	\N	0	\N	\N	\N	\N	\N	651	0	\N	\N	\N	\N
683	14	\N	\N	retained	\N	\N	\N	\N	\N	0	\N	\N	\N	\N	\N	652	0	\N	\N	\N	\N
684	14	\N	\N	retained	\N	\N	\N	\N	\N	0	\N	\N	\N	\N	\N	653	0	\N	\N	\N	\N
685	14	\N	\N	retained	\N	\N	\N	\N	\N	0	\N	\N	\N	\N	\N	654	0	\N	\N	\N	\N
686	14	\N	\N	retained	\N	\N	\N	\N	\N	0	\N	\N	\N	\N	\N	655	0	\N	\N	\N	\N
687	14	\N	\N	retained	\N	\N	\N	\N	\N	0	\N	\N	\N	\N	\N	656	0	\N	\N	\N	\N
688	14	\N	\N	retained	\N	\N	\N	\N	\N	0	\N	\N	\N	\N	\N	657	0	\N	\N	\N	\N
689	14	\N	\N	retained	\N	\N	\N	\N	\N	0	\N	\N	\N	\N	\N	658	0	\N	\N	\N	\N
690	14	\N	\N	retained	\N	\N	\N	\N	\N	0	\N	\N	\N	\N	\N	659	0	\N	\N	\N	\N
691	14	\N	\N	retained	\N	\N	\N	\N	\N	0	\N	\N	\N	\N	\N	660	0	\N	\N	\N	\N
692	14	\N	\N	retained	\N	\N	\N	\N	\N	0	\N	\N	\N	\N	\N	661	0	\N	\N	\N	\N
693	14	\N	\N	retained	\N	\N	\N	\N	\N	0	\N	\N	\N	\N	\N	662	0	\N	\N	\N	\N
694	14	\N	\N	retained	\N	\N	\N	\N	\N	0	\N	\N	\N	\N	\N	663	0	\N	\N	\N	\N
695	14	\N	\N	retained	\N	\N	\N	\N	\N	0	\N	\N	\N	\N	\N	664	0	\N	\N	\N	\N
696	14	\N	\N	retained	\N	\N	\N	\N	\N	0	\N	\N	\N	\N	\N	665	0	\N	\N	\N	\N
697	14	\N	\N	retained	\N	\N	\N	\N	\N	0	\N	\N	\N	\N	\N	666	0	\N	\N	\N	\N
698	14	\N	\N	retained	\N	\N	\N	\N	\N	0	\N	\N	\N	\N	\N	667	0	\N	\N	\N	\N
699	14	\N	\N	retained	\N	\N	\N	\N	\N	0	\N	\N	\N	\N	\N	668	0	\N	\N	\N	\N
700	14	\N	\N	retained	\N	\N	\N	\N	\N	0	\N	\N	\N	\N	\N	669	0	\N	\N	\N	\N
701	14	\N	\N	retained	\N	\N	\N	\N	\N	0	\N	\N	\N	\N	\N	670	0	\N	\N	\N	\N
702	14	\N	\N	retained	\N	\N	\N	\N	\N	0	\N	\N	\N	\N	\N	671	0	\N	\N	\N	\N
703	114	\N	\N	retained	\N	\N	\N	\N	\N	0	\N	\N	\N	\N	\N	672	0	\N	\N	\N	\N
704	114	\N	\N	retained	\N	\N	\N	\N	\N	0	\N	\N	\N	\N	\N	673	0	\N	\N	\N	\N
705	114	\N	\N	retained	\N	\N	\N	\N	\N	0	\N	\N	\N	\N	\N	674	0	\N	\N	\N	\N
706	114	\N	\N	retained	\N	\N	\N	\N	\N	0	\N	\N	\N	\N	\N	675	0	\N	\N	\N	\N
707	114	\N	\N	retained	\N	\N	\N	\N	\N	0	\N	\N	\N	\N	\N	676	0	\N	\N	\N	\N
708	114	\N	\N	retained	\N	\N	\N	\N	\N	0	\N	\N	\N	\N	\N	677	0	\N	\N	\N	\N
709	114	\N	\N	retained	\N	\N	\N	\N	\N	0	\N	\N	\N	\N	\N	678	0	\N	\N	\N	\N
710	114	\N	\N	retained	\N	\N	\N	\N	\N	0	\N	\N	\N	\N	\N	679	0	\N	\N	\N	\N
711	114	\N	\N	retained	\N	\N	\N	\N	\N	0	\N	\N	\N	\N	\N	680	0	\N	\N	\N	\N
712	114	\N	\N	retained	\N	\N	\N	\N	\N	0	\N	\N	\N	\N	\N	681	0	\N	\N	\N	\N
713	114	\N	\N	retained	\N	\N	\N	\N	\N	0	\N	\N	\N	\N	\N	682	0	\N	\N	\N	\N
714	114	\N	\N	retained	\N	\N	\N	\N	\N	0	\N	\N	\N	\N	\N	683	0	\N	\N	\N	\N
715	114	\N	\N	retained	\N	\N	\N	\N	\N	0	\N	\N	\N	\N	\N	684	0	\N	\N	\N	\N
716	14	\N	\N	retained	\N	\N	\N	\N	\N	0	\N	\N	\N	\N	\N	685	0	\N	\N	\N	\N
717	116	\N	\N	retained	\N	\N	\N	\N	\N	0	\N	\N	\N	\N	\N	686	0	\N	\N	\N	\N
718	14	\N	\N	retained	\N	\N	\N	\N	\N	0	\N	\N	\N	\N	\N	687	0	\N	\N	\N	\N
719	14	\N	\N	retained	\N	\N	\N	\N	\N	0	\N	\N	\N	\N	\N	688	0	\N	\N	\N	\N
720	14	\N	\N	retained	\N	\N	\N	\N	\N	0	\N	\N	\N	\N	\N	689	0	\N	\N	\N	\N
721	15	\N	\N	retained	\N	\N	\N	\N	\N	0	\N	\N	\N	\N	\N	690	0	\N	\N	\N	\N
722	15	\N	\N	retained	\N	\N	\N	\N	\N	0	\N	\N	\N	\N	\N	691	0	\N	\N	\N	\N
723	15	\N	\N	retained	\N	\N	\N	\N	\N	0	\N	\N	\N	\N	\N	692	0	\N	\N	\N	\N
724	15	\N	\N	retained	\N	\N	\N	\N	\N	0	\N	\N	\N	\N	\N	693	0	\N	\N	\N	\N
725	15	\N	\N	retained	\N	\N	\N	\N	\N	0	\N	\N	\N	\N	\N	694	0	\N	\N	\N	\N
726	15	\N	\N	retained	\N	\N	\N	\N	\N	0	\N	\N	\N	\N	\N	695	0	\N	\N	\N	\N
727	15	\N	\N	retained	\N	\N	\N	\N	\N	0	\N	\N	\N	\N	\N	696	0	\N	\N	\N	\N
728	15	\N	\N	retained	\N	\N	\N	\N	\N	0	\N	\N	\N	\N	\N	697	0	\N	\N	\N	\N
729	15	\N	\N	retained	\N	\N	\N	\N	\N	0	\N	\N	\N	\N	\N	698	0	\N	\N	\N	\N
730	15	\N	\N	retained	\N	\N	\N	\N	\N	0	\N	\N	\N	\N	\N	699	0	\N	\N	\N	\N
731	15	\N	\N	retained	\N	\N	\N	\N	\N	0	\N	\N	\N	\N	\N	700	0	\N	\N	\N	\N
732	15	\N	\N	retained	\N	\N	\N	\N	\N	0	\N	\N	\N	\N	\N	701	0	\N	\N	\N	\N
733	15	\N	\N	retained	\N	\N	\N	\N	\N	0	\N	\N	\N	\N	\N	702	0	\N	\N	\N	\N
734	15	\N	\N	retained	\N	\N	\N	\N	\N	0	\N	\N	\N	\N	\N	703	0	\N	\N	\N	\N
735	15	\N	\N	retained	\N	\N	\N	\N	\N	0	\N	\N	\N	\N	\N	704	0	\N	\N	\N	\N
736	15	\N	\N	retained	\N	\N	\N	\N	\N	0	\N	\N	\N	\N	\N	705	0	\N	\N	\N	\N
737	15	\N	\N	retained	\N	\N	\N	\N	\N	0	\N	\N	\N	\N	\N	706	0	\N	\N	\N	\N
738	15	\N	\N	retained	\N	\N	\N	\N	\N	0	\N	\N	\N	\N	\N	707	0	\N	\N	\N	\N
739	15	\N	\N	retained	\N	\N	\N	\N	\N	0	\N	\N	\N	\N	\N	708	0	\N	\N	\N	\N
740	15	\N	\N	retained	\N	\N	\N	\N	\N	0	\N	\N	\N	\N	\N	709	0	\N	\N	\N	\N
741	15	\N	\N	retained	\N	\N	\N	\N	\N	0	\N	\N	\N	\N	\N	710	0	\N	\N	\N	\N
742	15	\N	\N	retained	\N	\N	\N	\N	\N	0	\N	\N	\N	\N	\N	711	0	\N	\N	\N	\N
743	15	\N	\N	retained	\N	\N	\N	\N	\N	0	\N	\N	\N	\N	\N	712	0	\N	\N	\N	\N
744	15	\N	\N	retained	\N	\N	\N	\N	\N	0	\N	\N	\N	\N	\N	713	0	\N	\N	\N	\N
745	15	\N	\N	retained	\N	\N	\N	\N	\N	0	\N	\N	\N	\N	\N	714	0	\N	\N	\N	\N
746	15	\N	\N	retained	\N	\N	\N	\N	\N	0	\N	\N	\N	\N	\N	715	0	\N	\N	\N	\N
747	15	\N	\N	retained	\N	\N	\N	\N	\N	0	\N	\N	\N	\N	\N	716	0	\N	\N	\N	\N
748	15	\N	\N	retained	\N	\N	\N	\N	\N	0	\N	\N	\N	\N	\N	717	0	\N	\N	\N	\N
749	15	\N	\N	retained	\N	\N	\N	\N	\N	0	\N	\N	\N	\N	\N	718	0	\N	\N	\N	\N
750	15	\N	\N	retained	\N	\N	\N	\N	\N	0	\N	\N	\N	\N	\N	719	0	\N	\N	\N	\N
751	15	\N	\N	retained	\N	\N	\N	\N	\N	0	\N	\N	\N	\N	\N	720	0	\N	\N	\N	\N
752	15	\N	\N	retained	\N	\N	\N	\N	\N	0	\N	\N	\N	\N	\N	721	0	\N	\N	\N	\N
753	15	\N	\N	retained	\N	\N	\N	\N	\N	0	\N	\N	\N	\N	\N	722	0	\N	\N	\N	\N
754	15	\N	\N	retained	\N	\N	\N	\N	\N	0	\N	\N	\N	\N	\N	723	0	\N	\N	\N	\N
755	114	\N	\N	retained	\N	\N	\N	\N	\N	0	\N	\N	\N	\N	\N	724	0	\N	\N	\N	\N
756	114	\N	\N	retained	\N	\N	\N	\N	\N	0	\N	\N	\N	\N	\N	725	0	\N	\N	\N	\N
757	15	\N	\N	retained	\N	\N	\N	\N	\N	0	\N	\N	\N	\N	\N	726	0	\N	\N	\N	\N
758	15	\N	\N	retained	\N	\N	\N	\N	\N	0	\N	\N	\N	\N	\N	727	0	\N	\N	\N	\N
759	14	\N	\N	retained	\N	\N	\N	\N	\N	0	\N	\N	\N	\N	\N	728	0	\N	\N	\N	\N
760	14	\N	\N	retained	\N	\N	\N	\N	\N	0	\N	\N	\N	\N	\N	729	0	\N	\N	\N	\N
761	15	\N	\N	retained	\N	\N	\N	\N	\N	0	\N	\N	\N	\N	\N	730	0	\N	\N	\N	\N
762	14	\N	\N	retained	\N	\N	\N	\N	\N	0	\N	\N	\N	\N	\N	731	0	\N	\N	\N	\N
763	14	\N	\N	retained	\N	\N	\N	\N	\N	0	\N	\N	\N	\N	\N	732	0	\N	\N	\N	\N
764	14	\N	\N	retained	\N	\N	\N	\N	\N	0	\N	\N	\N	\N	\N	733	0	\N	\N	\N	\N
765	14	\N	\N	retained	\N	\N	\N	\N	\N	0	\N	\N	\N	\N	\N	734	0	\N	\N	\N	\N
766	14	\N	\N	retained	\N	\N	\N	\N	\N	0	\N	\N	\N	\N	\N	735	0	\N	\N	\N	\N
767	14	\N	\N	retained	\N	\N	\N	\N	\N	0	\N	\N	\N	\N	\N	736	0	\N	\N	\N	\N
768	14	\N	\N	retained	\N	\N	\N	\N	\N	0	\N	\N	\N	\N	\N	737	0	\N	\N	\N	\N
769	14	\N	\N	retained	\N	\N	\N	\N	\N	0	\N	\N	\N	\N	\N	738	0	\N	\N	\N	\N
770	14	\N	\N	retained	\N	\N	\N	\N	\N	0	\N	\N	\N	\N	\N	739	0	\N	\N	\N	\N
771	15	\N	\N	retained	\N	\N	\N	\N	\N	0	\N	\N	\N	\N	\N	740	0	\N	\N	\N	\N
772	114	\N	\N	retained	\N	\N	\N	\N	\N	0	\N	\N	\N	\N	\N	741	0	\N	\N	\N	\N
773	114	\N	\N	retained	\N	\N	\N	\N	\N	0	\N	\N	\N	\N	\N	742	0	\N	\N	\N	\N
774	114	\N	\N	retained	\N	\N	\N	\N	\N	0	\N	\N	\N	\N	\N	743	0	\N	\N	\N	\N
775	114	\N	\N	retained	\N	\N	\N	\N	\N	0	\N	\N	\N	\N	\N	744	0	\N	\N	\N	\N
776	114	\N	\N	retained	\N	\N	\N	\N	\N	0	\N	\N	\N	\N	\N	745	0	\N	\N	\N	\N
777	116	\N	\N	retained	\N	\N	\N	\N	\N	0	\N	\N	\N	\N	\N	746	0	\N	\N	\N	\N
778	15	\N	\N	retained	\N	\N	\N	\N	\N	0	\N	\N	\N	\N	\N	747	0	\N	\N	\N	\N
779	15	\N	\N	retained	\N	\N	\N	\N	\N	0	\N	\N	\N	\N	\N	748	0	\N	\N	\N	\N
780	15	\N	\N	retained	\N	\N	\N	\N	\N	0	\N	\N	\N	\N	\N	749	0	\N	\N	\N	\N
781	15	\N	\N	retained	\N	\N	\N	\N	\N	0	\N	\N	\N	\N	\N	750	0	\N	\N	\N	\N
782	15	\N	\N	retained	\N	\N	\N	\N	\N	0	\N	\N	\N	\N	\N	751	0	\N	\N	\N	\N
783	15	\N	\N	retained	\N	\N	\N	\N	\N	0	\N	\N	\N	\N	\N	752	0	\N	\N	\N	\N
784	14	\N	\N	retained	\N	\N	\N	\N	\N	0	\N	\N	\N	\N	\N	753	0	\N	\N	\N	\N
785	14	\N	\N	retained	\N	\N	\N	\N	\N	0	\N	\N	\N	\N	\N	754	0	\N	\N	\N	\N
786	14	\N	\N	retained	\N	\N	\N	\N	\N	0	\N	\N	\N	\N	\N	755	0	\N	\N	\N	\N
787	14	\N	\N	retained	\N	\N	\N	\N	\N	0	\N	\N	\N	\N	\N	756	0	\N	\N	\N	\N
788	14	\N	\N	retained	\N	\N	\N	\N	\N	0	\N	\N	\N	\N	\N	757	0	\N	\N	\N	\N
789	14	\N	\N	retained	\N	\N	\N	\N	\N	0	\N	\N	\N	\N	\N	758	0	\N	\N	\N	\N
790	15	\N	\N	retained	\N	\N	\N	\N	\N	0	\N	\N	\N	\N	\N	759	0	\N	\N	\N	\N
791	15	\N	\N	retained	\N	\N	\N	\N	\N	0	\N	\N	\N	\N	\N	760	0	\N	\N	\N	\N
792	14	\N	\N	retained	\N	\N	\N	\N	\N	0	\N	\N	\N	\N	\N	761	0	\N	\N	\N	\N
793	14	\N	\N	retained	\N	\N	\N	\N	\N	0	\N	\N	\N	\N	\N	762	0	\N	\N	\N	\N
794	14	\N	\N	retained	\N	\N	\N	\N	\N	0	\N	\N	\N	\N	\N	763	0	\N	\N	\N	\N
795	14	\N	\N	retained	\N	\N	\N	\N	\N	0	\N	\N	\N	\N	\N	764	0	\N	\N	\N	\N
796	14	\N	\N	retained	\N	\N	\N	\N	\N	0	\N	\N	\N	\N	\N	765	0	\N	\N	\N	\N
797	14	\N	\N	retained	\N	\N	\N	\N	\N	0	\N	\N	\N	\N	\N	766	0	\N	\N	\N	\N
798	11	\N	\N	retained	\N	\N	\N	\N	\N	0	\N	\N	\N	\N	\N	767	0	\N	\N	\N	\N
799	11	\N	\N	retained	\N	\N	\N	\N	\N	0	\N	\N	\N	\N	\N	768	0	\N	\N	\N	\N
800	11	\N	\N	retained	\N	\N	\N	\N	\N	0	\N	\N	\N	\N	\N	769	0	\N	\N	\N	\N
801	11	\N	\N	retained	\N	\N	\N	\N	\N	0	\N	\N	\N	\N	\N	770	0	\N	\N	\N	\N
802	11	\N	\N	retained	\N	\N	\N	\N	\N	0	\N	\N	\N	\N	\N	771	0	\N	\N	\N	\N
803	11	\N	\N	retained	\N	\N	\N	\N	\N	0	\N	\N	\N	\N	\N	772	0	\N	\N	\N	\N
804	11	\N	\N	retained	\N	\N	\N	\N	\N	0	\N	\N	\N	\N	\N	773	0	\N	\N	\N	\N
805	11	\N	\N	retained	\N	\N	\N	\N	\N	0	\N	\N	\N	\N	\N	774	0	\N	\N	\N	\N
806	11	\N	\N	retained	\N	\N	\N	\N	\N	0	\N	\N	\N	\N	\N	775	0	\N	\N	\N	\N
807	11	\N	\N	retained	\N	\N	\N	\N	\N	0	\N	\N	\N	\N	\N	776	0	\N	\N	\N	\N
808	11	\N	\N	retained	\N	\N	\N	\N	\N	0	\N	\N	\N	\N	\N	777	0	\N	\N	\N	\N
809	11	\N	\N	retained	\N	\N	\N	\N	\N	0	\N	\N	\N	\N	\N	778	0	\N	\N	\N	\N
810	11	\N	\N	retained	\N	\N	\N	\N	\N	0	\N	\N	\N	\N	\N	779	0	\N	\N	\N	\N
811	11	\N	\N	retained	\N	\N	\N	\N	\N	0	\N	\N	\N	\N	\N	780	0	\N	\N	\N	\N
812	11	\N	\N	retained	\N	\N	\N	\N	\N	0	\N	\N	\N	\N	\N	781	0	\N	\N	\N	\N
813	11	\N	\N	retained	\N	\N	\N	\N	\N	0	\N	\N	\N	\N	\N	782	0	\N	\N	\N	\N
814	11	\N	\N	retained	\N	\N	\N	\N	\N	0	\N	\N	\N	\N	\N	783	0	\N	\N	\N	\N
815	11	\N	\N	retained	\N	\N	\N	\N	\N	0	\N	\N	\N	\N	\N	784	0	\N	\N	\N	\N
816	11	\N	\N	retained	\N	\N	\N	\N	\N	0	\N	\N	\N	\N	\N	785	0	\N	\N	\N	\N
817	11	\N	\N	retained	\N	\N	\N	\N	\N	0	\N	\N	\N	\N	\N	786	0	\N	\N	\N	\N
818	11	\N	\N	retained	\N	\N	\N	\N	\N	0	\N	\N	\N	\N	\N	787	0	\N	\N	\N	\N
819	11	\N	\N	retained	\N	\N	\N	\N	\N	0	\N	\N	\N	\N	\N	788	0	\N	\N	\N	\N
820	11	\N	\N	retained	\N	\N	\N	\N	\N	0	\N	\N	\N	\N	\N	789	0	\N	\N	\N	\N
821	11	\N	\N	retained	\N	\N	\N	\N	\N	0	\N	\N	\N	\N	\N	790	0	\N	\N	\N	\N
822	11	\N	\N	retained	\N	\N	\N	\N	\N	0	\N	\N	\N	\N	\N	791	0	\N	\N	\N	\N
823	11	\N	\N	retained	\N	\N	\N	\N	\N	0	\N	\N	\N	\N	\N	792	0	\N	\N	\N	\N
824	11	\N	\N	retained	\N	\N	\N	\N	\N	0	\N	\N	\N	\N	\N	793	0	\N	\N	\N	\N
825	11	\N	\N	retained	\N	\N	\N	\N	\N	0	\N	\N	\N	\N	\N	794	0	\N	\N	\N	\N
826	11	\N	\N	retained	\N	\N	\N	\N	\N	0	\N	\N	\N	\N	\N	795	0	\N	\N	\N	\N
827	11	\N	\N	retained	\N	\N	\N	\N	\N	0	\N	\N	\N	\N	\N	796	0	\N	\N	\N	\N
828	11	\N	\N	retained	\N	\N	\N	\N	\N	0	\N	\N	\N	\N	\N	797	0	\N	\N	\N	\N
829	11	\N	\N	retained	\N	\N	\N	\N	\N	0	\N	\N	\N	\N	\N	798	0	\N	\N	\N	\N
830	114	\N	\N	retained	\N	\N	\N	\N	\N	0	\N	\N	\N	\N	\N	799	0	\N	\N	\N	\N
831	114	\N	\N	retained	\N	\N	\N	\N	\N	0	\N	\N	\N	\N	\N	800	0	\N	\N	\N	\N
832	114	\N	\N	retained	\N	\N	\N	\N	\N	0	\N	\N	\N	\N	\N	801	0	\N	\N	\N	\N
833	114	\N	\N	retained	\N	\N	\N	\N	\N	0	\N	\N	\N	\N	\N	802	0	\N	\N	\N	\N
834	114	\N	\N	retained	\N	\N	\N	\N	\N	0	\N	\N	\N	\N	\N	803	0	\N	\N	\N	\N
835	114	\N	\N	retained	\N	\N	\N	\N	\N	0	\N	\N	\N	\N	\N	804	0	\N	\N	\N	\N
836	114	\N	\N	retained	\N	\N	\N	\N	\N	0	\N	\N	\N	\N	\N	805	0	\N	\N	\N	\N
837	114	\N	\N	retained	\N	\N	\N	\N	\N	0	\N	\N	\N	\N	\N	806	0	\N	\N	\N	\N
838	114	\N	\N	retained	\N	\N	\N	\N	\N	0	\N	\N	\N	\N	\N	807	0	\N	\N	\N	\N
839	114	\N	\N	retained	\N	\N	\N	\N	\N	0	\N	\N	\N	\N	\N	808	0	\N	\N	\N	\N
840	11	\N	\N	retained	\N	\N	\N	\N	\N	0	\N	\N	\N	\N	\N	809	0	\N	\N	\N	\N
841	11	\N	\N	retained	\N	\N	\N	\N	\N	0	\N	\N	\N	\N	\N	810	0	\N	\N	\N	\N
842	11	\N	\N	retained	\N	\N	\N	\N	\N	0	\N	\N	\N	\N	\N	811	0	\N	\N	\N	\N
843	11	\N	\N	retained	\N	\N	\N	\N	\N	0	\N	\N	\N	\N	\N	812	0	\N	\N	\N	\N
844	11	\N	\N	retained	\N	\N	\N	\N	\N	0	\N	\N	\N	\N	\N	813	0	\N	\N	\N	\N
845	11	\N	\N	retained	\N	\N	\N	\N	\N	0	\N	\N	\N	\N	\N	814	0	\N	\N	\N	\N
846	11	\N	\N	retained	\N	\N	\N	\N	\N	0	\N	\N	\N	\N	\N	815	0	\N	\N	\N	\N
847	11	\N	\N	retained	\N	\N	\N	\N	\N	0	\N	\N	\N	\N	\N	816	0	\N	\N	\N	\N
848	11	\N	\N	retained	\N	\N	\N	\N	\N	0	\N	\N	\N	\N	\N	817	0	\N	\N	\N	\N
849	11	\N	\N	retained	\N	\N	\N	\N	\N	0	\N	\N	\N	\N	\N	818	0	\N	\N	\N	\N
850	11	\N	\N	retained	\N	\N	\N	\N	\N	0	\N	\N	\N	\N	\N	819	0	\N	\N	\N	\N
851	0	\N	\N	retained	\N	\N	\N	\N	\N	0	\N	\N	\N	\N	\N	1020	0	\N	\N	\N	\N
852	0	\N	\N	retained	\N	\N	\N	\N	\N	0	\N	\N	\N	\N	\N	1025	26	\N	\N	\N	\N
853	0	\N	\N	retained	\N	\N	\N	\N	\N	0	\N	\N	\N	\N	\N	1026	26	\N	\N	\N	0
854	14	\N	\N	retained	1/4 inch	\N	60 minutes	\N	Stereo	0	Maxell LN60	\N	4 track	\N	\N	1146	34	\N	\N	\N	4
855	0	\N	\N	retained	\N	\N	\N	\N	\N	0	\N	\N	\N	\N	\N	1147	0	\N	\N	\N	4
856	0	\N	\N	retained	\N	\N	\N	\N	\N	0	\N	\N	\N	\N	\N	1148	0	\N	\N	\N	4
857	0	\N	\N	retained	\N	\N	\N	\N	\N	0	\N	\N	\N	\N	\N	1149	0	\N	\N	\N	4
858	0	\N	\N	retained	\N	\N	\N	\N	\N	0	\N	\N	\N	\N	\N	1162	0	\N	\N	\N	4
859	0	\N	\N	retained	\N	\N	\N	\N	\N	0	\N	\N	\N	\N	\N	1161	0	\N	\N	\N	4
860	0	\N	\N	retained	\N	\N	\N	\N	\N	0	\N	\N	\N	\N	\N	\N	0	\N	\N	\N	4
861	14	\N	\N	retained	\N	\N	\N	\N	\N	0	\N	\N	\N	\N	\N	1236	0	\N	\N	\N	4
862	14	\N	\N	retained	\N	\N	\N	\N	Stereo	0	\N	\N	\N	\N	\N	1238	0	\N	\N	\N	4
863	14	\N	\N	retained	\N	\N	\N	\N	\N	0	\N	\N	\N	\N	\N	1239	0	\N	\N	\N	4
864	14	\N	\N	retained	\N	\N	\N	\N	\N	0	\N	\N	\N	\N	\N	1240	0	\N	\N	\N	4
865	14	\N	\N	retained	\N	\N	\N	\N	\N	0	\N	\N	\N	\N	\N	1241	0	\N	\N	\N	4
866	0	\N	\N	retained	\N	\N	\N	\N	\N	0	\N	\N	\N	\N	\N	1249	0	\N	\N	\N	4
867	0	\N	\N	retained	\N	\N	\N	\N	\N	0	\N	\N	\N	\N	\N	1250	0	\N	\N	\N	4
868	0	\N	\N	retained	\N	\N	\N	\N	\N	0	\N	\N	\N	\N	\N	1251	0	\N	\N	\N	4
869	0	\N	\N	retained	\N	\N	\N	\N	\N	0	\N	\N	\N	\N	\N	1252	0	\N	\N	\N	4
870	0	\N	\N	retained	\N	\N	\N	\N	\N	0	\N	\N	\N	\N	\N	1253	0	\N	\N	\N	4
871	0	\N	\N	retained	\N	\N	\N	\N	\N	0	\N	\N	\N	\N	\N	1254	0	\N	\N	\N	4
872	0	\N	\N	retained	\N	\N	\N	\N	\N	0	\N	\N	\N	\N	\N	1255	0	\N	\N	\N	4
873	0	\N	\N	retained	\N	\N	\N	\N	\N	0	\N	\N	\N	\N	\N	1256	0	\N	\N	\N	4
874	0	\N	\N	retained	\N	\N	\N	\N	\N	0	\N	\N	\N	\N	\N	1257	0	\N	\N	\N	4
875	0	\N	\N	retained	\N	\N	\N	\N	\N	0	\N	\N	\N	\N	\N	1258	0	\N	\N	\N	4
876	0	\N	\N	retained	\N	\N	\N	\N	\N	0	\N	\N	\N	\N	\N	1259	0	\N	\N	\N	4
877	0	\N	\N	retained	\N	\N	\N	\N	\N	0	\N	\N	\N	\N	\N	1260	0	\N	\N	\N	4
878	0	\N	\N	retained	\N	\N	\N	\N	\N	0	\N	\N	\N	\N	\N	1261	0	\N	\N	\N	4
879	0	\N	\N	retained	\N	\N	\N	\N	\N	0	\N	\N	\N	\N	\N	1262	0	\N	\N	\N	4
880	0	\N	\N	retained	\N	\N	\N	\N	\N	0	\N	\N	\N	\N	\N	\N	0	\N	\N	\N	4
881	14	\N	\N	retained	\N	\N	\N	\N	Stereo	0	Maxell LN60	\N	\N	\N	\N	1145	0	\N	\N	\N	4
2010	0	\N	\N	retained	\N	\N	\N	\N	\N	0	\N	\N	\N	\N	\N	2027	0	\N	\N	\N	4
2013	0	\N	\N	retained	\N	\N	\N	\N	\N	0	\N	\N	\N	\N	\N	2030	0	\N	\N	\N	4
2002	14	\N	\N	retained	\N	\N	\N	\N	Stereo	0	SONY HF90	\N	\N	\N	MARBL	2022	0	\N	\N	\N	4
2014	0			retained						0						2028	0				0
2015	0			retained						0						2029	0				0
2003	14	\N	\N	retained	\N	\N	\N	\N	Stereo	0	SONY AS92	\N	\N	\N	\N	2023	0	\N	\N	\N	4
2011	14	\N	\N	retained	\N	\N	\N	\N	Stereo	0	unknown	\N	\N	\N	MARBL	2024	0	\N	\N	\N	4
2008	0	\N	\N	retained	\N	\N	\N	\N	Stereo	0	unknown	\N	\N	\N	MARBL	2025	0	\N	\N	\N	4
2009	0	\N	\N	retained	\N	\N	\N	\N	Stereo	0	unknown	\N	\N	\N	MARBL	2026	0	\N	\N	\N	4
\.


--
-- Data for TOC entry 241 (OID 12746497)
-- Name: ColorSpace; Type: TABLE DATA; Schema: public; Owner: jbwhite
--

COPY "ColorSpace" ("ID", "ColorSpace") FROM stdin;
1	WhiteIsZero
2	sRGB
3	JPEG2000
4	BlackIsZero
5	RBG
6	CMYK
7	YCbCr
8	CIELab
9	DeviceGray
10	DeviceRGB
11	DeviceCMYK
12	Lab
13	ICCBased
14	CalGray
15	CalRGB
16	Separation
17	Indexed
18	Other
\.


--
-- Data for TOC entry 242 (OID 12746523)
-- Name: Subjects; Type: TABLE DATA; Schema: public; Owner: jbwhite
--

COPY "Subjects" ("Headings", "ID", "Authority_id") FROM stdin;
African recordings	14	0
African Americans	16	0
Georgia	17	0
Georgia.	18	0
\N	20	0
African American choral directors	22	0
Photographs	23	0
Piano	24	0
Dawson, William Levi	21	0
African Americans	19	0
\.


--
-- Data for TOC entry 243 (OID 12746611)
-- Name: TechImages; Type: TABLE DATA; Schema: public; Owner: jbwhite
--

COPY "TechImages" ("ID", "Content#", "FormatNameVersion", "ByteOrder", "CompressionScheme", "ColorSpace", "ICCProfile", "YCbCrSubSample", "YCbCrPositioning", "YCbCrCoefficients", "RefBW", "JPEG2000Profile", "JPEG2000Class", "JPEG2000Layers", "JPEG2000Level", "MrSid", "MrSidZoomLevels", "FileSize", "ScannerCameraModelName", "Methodology", "ImageWidth", "ImageLength", "PixelRes", "BitsPerSample", "BitsPerSampleUnit", "SamplesPerPixel", "ExtraSamples", "TargetLookup", "ImageProcessing", "Gamma", "Scale", "ImageNote", "DateCaptured", "DjVu", "DjVuFormat", "DerivFileName", "FileLoc", "Thumbnail") FROM stdin;
48	820	TIFF 6.0	Little Endian (PC)	Uncompressed	1	\N	\N	2	\N	\N	\N	\N	\N	\N	f	0	0	1	library internal use	12	0	400	8,8,8	integer	3	0	1	\N	2.2	100	\N	2006-01-01 00:00:00	f	\N	\N	\N	\N
49	822	TIFF 6.0	Little Endian (PC)	Uncompressed	1	\N	\N	2	\N	\N	\N	\N	\N	\N	f	0	23000	1	patron request	2458	3268	400	8,8,8	integer	3	0	4	Adjusted grey points, rotated 90 degree CC	2.2	100	\N	2006-05-14 00:00:00	f	\N	\N	z:/1movedfromF/Naomi/SAA-class	\N
50	823	TIFF 6.0	Little Endian (PC)	Uncompressed	1	Adobe RGB	\N	2	\N	\N	\N	\N	\N	\N	f	0	10	1	library internal use	1998	1702	400	8,8,8	integer	3	0	1	\N	2.2	100	\N	2006-05-14 00:00:00	f	\N	823.jpg	\N	\N
51	822	TIFF 6.0	Little Endian (PC)	Uncompressed	1	\N	\N	2	\N	\N	\N	\N	\N	\N	f	0	0	1	library internal use	0	0	400	8,8,8	integer	3	0	1	None	2.2	100	Cover not scanned.	\N	f	\N	\N	DigitalMasters/FragilePictures	\N
52	1027	TIFF 6.0	Little Endian (PC)	Uncompressed	1	\N	\N	2	\N	\N	\N	\N	\N	\N	f	0	11429478	0	patron request	1931	1972	400	8,8,8	integer	3	0	0	\N	2.2	100	\N	\N	f	\N	\N	\N	\N
53	1028	TIFF 6.0	Little Endian (PC)	Uncompressed	1	\N	\N	2	\N	\N	\N	\N	\N	\N	f	0	4519363	0	patron request	2495	1812	400	8,8,8	integer	3	0	0	\N	2.2	100	\N	\N	f	\N	\N	\N	\N
54	1029	TIFF 6.0	Little Endian (PC)	Uncompressed	1	\N	\N	2	\N	\N	\N	\N	\N	\N	f	0	11848909	0	patron request	2084	1900	400	8,8,8	integer	3	0	0	\N	2.2	100	\N	\N	f	\N	\N	\N	\N
55	1030	TIFF 6.0	Little Endian (PC)	Uncompressed	1	\N	\N	2	\N	\N	\N	\N	\N	\N	f	0	10695475	0	patron request	1888	1888	400	8,8,8	integer	3	0	0	\N	2.2	100	\N	\N	f	\N	\N	\N	\N
56	1032	TIFF 6.0	Little Endian (PC)	Uncompressed	1	\N	\N	2	\N	\N	\N	\N	\N	\N	f	0	10338959	0	library internal use	1438	2396	400	8,8,8	integer	3	0	0	\N	2.2	100	\N	\N	f	\N	\N	\N	\N
57	1033	TIFF 6.0	Little Endian (PC)	Uncompressed	1	\N	\N	2	\N	\N	\N	\N	\N	\N	f	0	51380224	0	patron request	5320	3221	400	8,8,8	integer	3	0	0	\N	2.2	100	\N	\N	f	\N	\N	\N	\N
58	\N	TIFF 6.0	Little Endian (PC)	Uncompressed	1	\N	\N	2	\N	\N	\N	\N	\N	\N	f	0	0	1	library internal use	0	0	400	8,8,8	integer	3	0	1	\N	2.2	100	\N	\N	f	\N	\N	\N	\N
62	1036	TIFF 6.0	Little Endian (PC)	Uncompressed	1	Adobe RGB 1998	\N	2	\N	\N	\N	\N	\N	\N	f	0	0	1	library internal use	0	0	400	8,8,8	integer	3	0	1	\N	2.2	100	\N	2006-06-07 00:00:00	f	\N	\N	\N	\N
65	1040	TIFF 6.0	Little Endian (PC)	Uncompressed	1	\N	\N	2	\N	\N	\N	\N	\N	\N	f	0	62809702	0	library internal use	3196	5560	400	8,8,8	integer	3	0	0	\N	2.2	100	\N	\N	f	\N	\N	\N	\N
66	1041	TIFF 6.0	Little Endian (PC)	Uncompressed	1	\N	\N	2	\N	\N	\N	\N	\N	\N	f	0	46347059	0	library internal use	2996	5160	400	8,8,8	integer	3	0	0	\N	2.2	100	\N	\N	f	\N	0644-007.tif	\N	\N
67	1042	TIFF 6.0	Little Endian (PC)	Uncompressed	1	\N	\N	2	\N	\N	\N	\N	\N	\N	f	0	44145050	0	library internal use	2996	4916	400	8,8,8	integer	3	0	0	\N	2.2	100	\N	\N	f	\N	\N	\N	\N
68	1039	TIFF 6.0	Little Endian (PC)	Uncompressed	1	\N	\N	2	\N	\N	\N	\N	\N	\N	f	0	46347059	0	library internal use	2996	5160	400	8,8,8	integer	3	0	0	\N	2.2	100	\N	\N	f	\N	0644-010.tif	\N	\N
69	1043	TIFF 6.0	Little Endian (PC)	Uncompressed	1	\N	\N	2	\N	\N	\N	\N	\N	\N	f	0	46347059	0	library internal use	2996	5160	400	8,8,8	integer	3	0	0	\N	2.2	100	\N	\N	f	\N	\N	\N	\N
70	1044	TIFF 6.0	Little Endian (PC)	Uncompressed	1	\N	\N	2	\N	\N	\N	\N	\N	\N	f	0	6805258	0	library internal use	2614	2603	400	8,8,8	integer	3	0	0	\N	2.2	100	\N	\N	f	\N	0644#############002001.TIF	\N	\N
71	1045	TIFF 6.0	Little Endian (PC)	Uncompressed	1	\N	\N	2	\N	\N	\N	\N	\N	\N	f	0	10800333	0	library internal use	3822	2814	400	8,8,8	integer	3	0	0	\N	2.2	100	\N	\N	f	\N	\N	\N	\N
72	1046	TIFF 6.0	Little Endian (PC)	Uncompressed	1	\N	\N	2	\N	\N	\N	\N	\N	\N	f	0	4823450	0	library internal use	2651	1820	400	8,8,8	integer	3	0	0	\N	2.2	100	\N	\N	f	\N	\N	\N	\N
111	1085	TIFF 6.0	Little Endian (PC)	Uncompressed	1	Adobe RGB 1998	\N	2	\N	\N	\N	\N	\N	\N	f	0	21390950	1	library internal use	2110	3381	400	8,8,8	integer	3	0	7	\N	2.2	100	Dimensions should be H 8.5 x W 5.25	2006-06-09 00:00:00	f	\N	\N	\N	\N
112	1086	TIFF 6.0	Little Endian (PC)	Uncompressed	1	Adobe RGB 1998	\N	2	\N	\N	\N	\N	\N	\N	f	0	21390950	1	library internal use	2110	3381	400	8,8,8	integer	3	0	7	\N	2.2	100	Dimensions should be H 8.5 x W 5.25	2006-06-09 00:00:00	f	\N	\N	\N	\N
113	1089	TIFF 6.0	Little Endian (PC)	Uncompressed	1	\N	\N	2	\N	\N	\N	\N	\N	\N	f	0	22124954	0	library internal use	3034	2434	400	8,8,8	integer	3	0	0	\N	2.2	100	\N	\N	f	\N	\N	\N	\N
114	1090	TIFF 6.0	Little Endian (PC)	Uncompressed	1	\N	\N	2	\N	\N	\N	\N	\N	\N	f	0	26319258	0	library internal use	3174	2767	400	8,8,8	integer	3	0	0	\N	2.2	100	\N	\N	f	\N	\N	\N	\N
115	1091	TIFF 6.0	Little Endian (PC)	Uncompressed	1	\N	\N	2	\N	\N	\N	\N	\N	\N	f	0	4771021	0	library internal use	1831	2606	400	8,8,8	integer	3	0	0	\N	2.2	100	\N	\N	f	\N	\N	\N	\N
116	1092	TIFF 6.0	Little Endian (PC)	Uncompressed	1	\N	\N	2	\N	\N	\N	\N	\N	\N	f	0	11744051	0	library internal use	3838	3063	400	8,8,8	integer	3	0	0	\N	2.2	100	\N	\N	f	\N	\N	\N	\N
117	1093	TIFF 6.0	Little Endian (PC)	Uncompressed	1	\N	\N	2	\N	\N	\N	\N	\N	\N	f	0	1405092	0	library internal use	1326	1056	400	8,8,8	integer	3	0	0	\N	2.2	100	\N	\N	f	\N	\N	\N	\N
118	1094	TIFF 6.0	Little Endian (PC)	Uncompressed	1	\N	\N	2	\N	\N	\N	\N	\N	\N	f	0	16672358	0	library internal use	1982	2811	400	8,8,8	integer	3	0	0	\N	2.2	100	\N	\N	f	\N	\N	\N	\N
119	1095	TIFF 6.0	Little Endian (PC)	Uncompressed	1	\N	\N	2	\N	\N	\N	\N	\N	\N	f	0	14050918	0	library internal use	3199	4384	400	8,8,8	integer	3	0	0	\N	2.2	100	\N	\N	f	\N	\N	\N	\N
120	1096	TIFF 6.0	Little Endian (PC)	Uncompressed	1	\N	\N	2	\N	\N	\N	\N	\N	\N	f	0	38168166	0	library internal use	3995	3183	400	8,8,8	integer	3	0	0	\N	2.2	100	\N	\N	f	\N	\N	\N	\N
121	1097	TIFF 6.0	Little Endian (PC)	Uncompressed	1	\N	\N	2	\N	\N	\N	\N	\N	\N	f	0	3313500	0	library internal use	1917	1726	400	8,8,8	integer	3	0	0	\N	2.2	100	\N	\N	f	\N	\N	\N	\N
122	1098	TIFF 6.0	Little Endian (PC)	Uncompressed	1	\N	\N	2	\N	\N	\N	\N	\N	\N	f	0	5515510	0	library internal use	1968	2800	400	8,8,8	integer	3	0	0	\N	2.2	100	\N	\N	f	\N	\N	\N	\N
123	1099	TIFF 6.0	Little Endian (PC)	Uncompressed	1	\N	\N	2	\N	\N	\N	\N	\N	\N	f	0	32610714	0	library internal use	3234	3360	400	8,8,8	integer	3	0	0	\N	2.2	100	\N	\N	f	\N	\N	\N	\N
124	1100	TIFF 6.0	Little Endian (PC)	Uncompressed	1	\N	\N	2	\N	\N	\N	\N	\N	\N	f	0	31666995	0	library internal use	3197	3297	400	8,8,8	integer	3	0	0	\N	2.2	100	\N	\N	f	\N	\N	\N	\N
125	1101	TIFF 6.0	Little Endian (PC)	Uncompressed	1	\N	\N	2	\N	\N	\N	\N	\N	\N	f	0	18245222	0	library internal use	2790	2178	400	8,8,8	integer	3	0	0	\N	2.2	100	\N	\N	f	\N	\N	\N	\N
126	1102	TIFF 6.0	Little Endian (PC)	Uncompressed	1	\N	\N	2	\N	\N	\N	\N	\N	\N	f	0	18140365	0	library internal use	2877	2100	400	8,8,8	integer	3	0	0	\N	2.2	100	\N	\N	f	\N	\N	\N	\N
127	1103	TIFF 6.0	Little Endian (PC)	Uncompressed	1	\N	\N	2	\N	\N	\N	\N	\N	\N	f	0	11953766	0	library internal use	1656	2413	400	8,8,8	integer	3	0	0	\N	2.2	100	\N	\N	f	\N	\N	\N	\N
128	1104	TIFF 6.0	Little Endian (PC)	Uncompressed	1	\N	\N	2	\N	\N	\N	\N	\N	\N	f	0	11219763	0	library internal use	1720	2180	400	8,8,8	integer	3	0	0	\N	2.2	100	\N	\N	f	\N	\N	\N	\N
129	1105	TIFF 6.0	Little Endian (PC)	Uncompressed	1	\N	\N	2	\N	\N	\N	\N	\N	\N	f	0	7319060	0	library internal use	1312	1859	400	8,8,8	integer	3	0	0	\N	2.2	100	\N	\N	f	\N	\N	\N	\N
130	1106	TIFF 6.0	Little Endian (PC)	Uncompressed	1	\N	\N	2	\N	\N	\N	\N	\N	\N	f	0	35966157	0	library internal use	3400	3530	400	8,8,8	integer	3	0	0	\N	2.2	100	\N	\N	f	\N	\N	\N	\N
131	1107	TIFF 6.0	Little Endian (PC)	Uncompressed	1	\N	\N	2	\N	\N	\N	\N	\N	\N	f	0	16148070	0	library internal use	2089	2581	400	8,8,8	integer	3	0	0	\N	2.2	100	\N	\N	f	\N	\N	\N	\N
132	1108	TIFF 6.0	Little Endian (PC)	Uncompressed	1	\N	\N	2	\N	\N	\N	\N	\N	\N	f	0	21181235	0	library internal use	3093	2280	400	8,8,8	integer	3	0	0	\N	2.2	100	\N	\N	f	\N	\N	\N	\N
133	1109	TIFF 6.0	Little Endian (PC)	Uncompressed	1	\N	\N	2	\N	\N	\N	\N	\N	\N	f	0	18979226	0	library internal use	2080	3045	400	8,8,8	integer	3	0	0	\N	2.2	100	\N	\N	f	\N	\N	\N	\N
134	1110	TIFF 6.0	Little Endian (PC)	Uncompressed	1	\N	\N	2	\N	\N	\N	\N	\N	\N	f	0	9416212	0	library internal use	1514	2072	400	8,8,8	integer	3	0	0	\N	2.2	100	\N	\N	f	\N	\N	\N	\N
161	1137	TIFF 6.0	Little Endian (PC)	Uncompressed	1	Adobe RGB 1998	\N	2	\N	\N	\N	\N	\N	\N	f	0	25060966	1	library internal use	2550	3275	400	8,8,8	integer	3	0	7	\N	2.2	100	\N	2006-06-13 00:00:00	f	\N	\N	\N	\N
168	1150	TIFF 6.0	Little Endian (PC)	Uncompressed	1	Adobe RGB 1998	\N	2	\N	\N	\N	\N	\N	\N	f	0	39321600	1	library internal use	4009	3269	400	8,8,8	integer	3	0	7	\N	2.2	100	\N	2006-06-14 00:00:00	f	\N	\N	\N	\N
169	1151	TIFF 6.0	Little Endian (PC)	Uncompressed	1	\N	\N	2	\N	\N	\N	\N	\N	\N	f	0	9971958	0	library internal use	1611	2064	400	8,8,8	integer	3	0	0	\N	2.2	100	\N	\N	f	\N	\N	\N	\N
170	1152	TIFF 6.0	Little Endian (PC)	Uncompressed	1	\N	\N	2	\N	\N	\N	\N	\N	\N	f	0	9237955	0	library internal use	1498	2056	400	8,8,8	integer	3	0	0	\N	2.2	100	\N	\N	f	\N	\N	\N	\N
171	1153	TIFF 6.0	Little Endian (PC)	Uncompressed	1	\N	\N	2	\N	\N	\N	\N	\N	\N	f	0	9007268	0	library internal use	1466	2048	400	8,8,8	integer	3	0	0	\N	2.2	100	\N	\N	f	\N	\N	\N	\N
172	1154	TIFF 6.0	Little Endian (PC)	Uncompressed	1	\N	\N	2	\N	\N	\N	\N	\N	\N	f	0	9007268	0	library internal use	1466	2048	400	8,8,8	integer	3	0	0	\N	2.2	100	\N	\N	f	\N	\N	\N	\N
173	1155	TIFF 6.0	Little Endian (PC)	Uncompressed	1	\N	\N	2	\N	\N	\N	\N	\N	\N	f	0	9007268	0	library internal use	1466	2048	400	8,8,8	integer	3	0	0	\N	2.2	100	\N	\N	f	\N	\N	\N	\N
174	1156	TIFF 6.0	Little Endian (PC)	Uncompressed	1	\N	\N	2	\N	\N	\N	\N	\N	\N	f	0	9007268	0	library internal use	1466	2048	400	8,8,8	integer	3	0	0	\N	2.2	100	\N	\N	f	\N	\N	\N	\N
175	1157	TIFF 6.0	Little Endian (PC)	Uncompressed	1	\N	\N	2	\N	\N	\N	\N	\N	\N	f	0	9007268	0	library internal use	1466	2048	400	8,8,8	integer	3	0	0	\N	2.2	100	\N	\N	f	\N	\N	\N	\N
176	1158	TIFF 6.0	Little Endian (PC)	Uncompressed	1	\N	\N	2	\N	\N	\N	\N	\N	\N	f	0	9007268	0	library internal use	1466	2048	400	8,8,8	integer	3	0	0	\N	2.2	100	\N	\N	f	\N	\N	\N	\N
177	1159	TIFF 6.0	Little Endian (PC)	Uncompressed	1	\N	\N	2	\N	\N	\N	\N	\N	\N	f	0	9007268	0	library internal use	1466	2048	400	8,8,8	integer	3	0	0	\N	2.2	100	\N	\N	f	\N	\N	\N	\N
178	1160	TIFF 6.0	Little Endian (PC)	Uncompressed	1	\N	\N	2	\N	\N	\N	\N	\N	\N	f	0	33554432	0	library internal use	4135	2704	400	8,8,8	integer	3	0	0	\N	2.2	100	\N	\N	f	\N	\N	\N	\N
204	1189	TIFF 6.0	Little Endian (PC)	Uncompressed	1	Adobe RGB 1998	\N	2	\N	\N	\N	\N	\N	\N	f	0	44669338	1	library internal use	3400	4375	400	8,8,8	integer	3	0	7	\N	2.2	100	\N	2006-06-14 00:00:00	f	\N	\N	\N	\N
226	1211	TIFF 6.0	Little Endian (PC)	Uncompressed	1	Adobe RGB 1998	\N	2	\N	\N	\N	\N	\N	\N	f	0	44459622	1	library internal use	3391	4375	400	8,8,8	integer	3	0	7	\N	2.2	100	\N	2006-06-14 00:00:00	f	\N	\N	\N	\N
227	1212	TIFF 6.0	Little Endian (PC)	Uncompressed	1	Adobe RGB 1998	\N	2	\N	\N	\N	\N	\N	\N	f	0	44459622	1	library internal use	3391	4375	400	8,8,8	integer	3	0	7	\N	2.2	100	\N	2006-06-14 00:00:00	f	\N	\N	\N	\N
228	1213	TIFF 6.0	Little Endian (PC)	Uncompressed	1	Adobe RGB 1998	\N	2	\N	\N	\N	\N	\N	\N	f	0	44459622	1	library internal use	3391	4375	400	8,8,8	integer	3	0	7	\N	2.2	100	\N	2006-06-14 00:00:00	f	\N	\N	\N	\N
229	1214	TIFF 6.0	Little Endian (PC)	Uncompressed	1	Adobe RGB 1998	\N	2	\N	\N	\N	\N	\N	\N	f	0	44459622	1	library internal use	3391	4375	400	8,8,8	integer	3	0	7	\N	2.2	100	\N	2006-06-14 00:00:00	f	\N	\N	\N	\N
230	1215	TIFF 6.0	Little Endian (PC)	Uncompressed	1	Adobe RGB 1998	\N	2	\N	\N	\N	\N	\N	\N	f	0	44459622	1	library internal use	3391	4375	400	8,8,8	integer	3	0	7	\N	2.2	100	\N	2006-06-14 00:00:00	f	\N	\N	\N	\N
231	1216	TIFF 6.0	Little Endian (PC)	Uncompressed	1	Adobe RGB 1998	\N	2	\N	\N	\N	\N	\N	\N	f	0	44459622	1	library internal use	3391	4375	400	8,8,8	integer	3	0	7	\N	2.2	100	\N	2006-06-14 00:00:00	f	\N	\N	\N	\N
232	1217	TIFF 6.0	Little Endian (PC)	Uncompressed	1	Adobe RGB 1998	\N	2	\N	\N	\N	\N	\N	\N	f	0	44459622	1	library internal use	3391	4375	400	8,8,8	integer	3	0	7	\N	2.2	100	\N	2006-06-14 00:00:00	f	\N	\N	\N	\N
233	1218	TIFF 6.0	Little Endian (PC)	Uncompressed	1	Adobe RGB 1998	\N	2	\N	\N	\N	\N	\N	\N	f	0	44459622	1	library internal use	3391	4375	400	8,8,8	integer	3	0	7	\N	2.2	100	\N	2006-06-14 00:00:00	f	\N	\N	\N	\N
234	1219	TIFF 6.0	Little Endian (PC)	Uncompressed	1	\N	\N	2	\N	\N	\N	\N	\N	\N	f	0	34078720	0	library internal use	4200	2704	400	8,8,8	integer	3	0	0	\N	2.2	100	\N	\N	f	\N	\N	\N	\N
235	1221	TIFF 6.0	Little Endian (PC)	Uncompressed	1	\N	\N	2	\N	\N	\N	\N	\N	\N	f	0	34498150	0	library internal use	4200	2736	400	8,8,8	integer	3	0	0	\N	2.2	100	\N	\N	f	\N	\N	\N	\N
236	1222	TIFF 6.0	Little Endian (PC)	Uncompressed	1	\N	\N	2	\N	\N	\N	\N	\N	\N	f	0	34603008	0	library internal use	4216	2736	400	8,8,8	integer	3	0	0	\N	2.2	100	\N	\N	f	\N	\N	\N	\N
237	1223	TIFF 6.0	Little Endian (PC)	Uncompressed	1	\N	\N	2	\N	\N	\N	\N	\N	\N	f	0	35861299	0	library internal use	4264	2800	400	8,8,8	integer	3	0	0	\N	2.2	100	\N	\N	f	\N	\N	\N	\N
238	1224	TIFF 6.0	Little Endian (PC)	Uncompressed	1	\N	\N	2	\N	\N	\N	\N	\N	\N	f	0	12163482	0	library internal use	1795	2264	400	8,8,8	integer	3	0	0	\N	2.2	100	\N	\N	f	\N	\N	\N	\N
239	1225	TIFF 6.0	Little Endian (PC)	Uncompressed	1	\N	\N	2	\N	\N	\N	\N	\N	\N	f	0	7014973	0	library internal use	3000	2340	400	8,8,8	integer	3	0	0	\N	2.2	100	\N	\N	f	\N	\N	\N	\N
240	1226	TIFF 6.0	Little Endian (PC)	Uncompressed	1	\N	\N	2	\N	\N	\N	\N	\N	\N	f	0	6543114	0	library internal use	2974	2200	400	8,8,8	integer	3	0	0	\N	2.2	100	\N	\N	f	\N	\N	\N	\N
241	1227	TIFF 6.0	Little Endian (PC)	Uncompressed	1	\N	\N	2	\N	\N	\N	\N	\N	\N	f	0	6689915	0	library internal use	2131	3140	400	8,8,8	integer	3	0	0	\N	2.2	100	\N	\N	f	\N	\N	\N	\N
242	1228	TIFF 6.0	Little Endian (PC)	Uncompressed	1	\N	\N	2	\N	\N	\N	\N	\N	\N	f	0	38692454	0	library internal use	3199	4028	400	8,8,8	integer	3	0	0	\N	2.2	100	\N	\N	f	\N	\N	\N	\N
243	1229	TIFF 6.0	Little Endian (PC)	Uncompressed	1	\N	\N	2	\N	\N	\N	\N	\N	\N	f	0	40055603	0	library internal use	4053	3295	400	8,8,8	integer	3	0	0	\N	2.2	100	\N	\N	f	\N	\N	\N	\N
244	1230	TIFF 6.0	Little Endian (PC)	Uncompressed	1	\N	\N	2	\N	\N	\N	\N	\N	\N	f	0	47185920	0	library internal use	3365	4671	400	8,8,8	integer	3	0	0	\N	2.2	100	\N	\N	f	\N	\N	\N	\N
245	1231	TIFF 6.0	Little Endian (PC)	Uncompressed	1	\N	\N	2	\N	\N	\N	\N	\N	\N	f	0	39007027	0	library internal use	3216	4046	400	8,8,8	integer	3	0	0	\N	2.2	100	\N	\N	f	\N	\N	\N	\N
246	1232	TIFF 6.0	Little Endian (PC)	Uncompressed	1	\N	\N	2	\N	\N	\N	\N	\N	\N	f	0	38692454	0	library internal use	3199	4028	400	8,8,8	integer	3	0	0	\N	2.2	100	\N	\N	f	\N	\N	\N	\N
247	1233	TIFF 6.0	Little Endian (PC)	Uncompressed	1	\N	\N	2	\N	\N	\N	\N	\N	\N	f	0	49387930	0	library internal use	5178	3180	400	8,8,8	integer	3	0	0	\N	2.2	100	\N	\N	f	\N	\N	\N	\N
248	1234	TIFF 6.0	Little Endian (PC)	Uncompressed	1	\N	\N	2	\N	\N	\N	\N	\N	\N	f	0	49283072	0	library internal use	5166	3180	400	8,8,8	integer	3	0	0	\N	2.2	100	\N	\N	f	\N	\N	\N	\N
249	1235	TIFF 6.0	Little Endian (PC)	Uncompressed	1	\N	\N	2	\N	\N	\N	\N	\N	\N	f	0	39007027	0	library internal use	3216	4046	400	8,8,8	integer	3	0	0	\N	2.2	100	\N	\N	f	\N	\N	\N	\N
250	1237	TIFF 6.0	Little Endian (PC)	Uncompressed	1	\N	\N	2	\N	\N	\N	\N	\N	\N	f	0	38692454	0	library internal use	3199	4028	400	8,8,8	integer	3	0	0	\N	2.2	100	\N	\N	f	\N	\N	\N	\N
251	1242	TIFF 6.0	Little Endian (PC)	Uncompressed	1	\N	\N	2	\N	\N	\N	\N	\N	\N	f	0	39007027	0	library internal use	3232	4028	400	8,8,8	integer	3	0	0	\N	2.2	100	\N	\N	f	\N	\N	\N	\N
252	1243	TIFF 6.0	Little Endian (PC)	Uncompressed	1	\N	\N	2	\N	\N	\N	\N	\N	\N	f	0	39636173	0	library internal use	3261	4052	400	8,8,8	integer	3	0	0	\N	2.2	100	\N	\N	f	\N	\N	\N	\N
253	1244	TIFF 6.0	Little Endian (PC)	Uncompressed	1	\N	\N	2	\N	\N	\N	\N	\N	\N	f	0	41313894	0	library internal use	3252	4240	400	8,8,8	integer	3	0	0	\N	2.2	100	\N	\N	f	\N	\N	\N	\N
254	1245	TIFF 6.0	Little Endian (PC)	Uncompressed	1	\N	\N	2	\N	\N	\N	\N	\N	\N	f	0	33764147	0	library internal use	2790	4040	400	8,8,8	integer	3	0	0	\N	2.2	100	\N	\N	f	\N	\N	\N	\N
255	1246	TIFF 6.0	Little Endian (PC)	Uncompressed	1	\N	\N	2	\N	\N	\N	\N	\N	\N	f	0	17616077	0	library internal use	2057	2860	400	8,8,8	integer	3	0	0	\N	2.2	100	\N	\N	f	\N	\N	\N	\N
256	1247	TIFF 6.0	Little Endian (PC)	Uncompressed	1	\N	\N	2	\N	\N	\N	\N	\N	\N	f	0	9017754	0	library internal use	1377	2183	400	8,8,8	integer	3	0	0	\N	2.2	100	\N	\N	f	\N	\N	\N	\N
257	1248	TIFF 6.0	Little Endian (PC)	Uncompressed	1	\N	\N	2	\N	\N	\N	\N	\N	\N	f	0	14470349	0	library internal use	2954	1635	400	8,8,8	integer	3	0	0	\N	2.2	100	\N	\N	f	\N	\N	\N	\N
258	1087	TIFF 6.0	Little Endian (PC)	Uncompressed	1	\N	\N	2	\N	\N	\N	\N	\N	\N	f	0	9594470	0	library internal use	3666	2616	400	8,8,8	integer	3	0	0	\N	2.2	100	\N	\N	f	\N	\N	\N	\N
259	1088	TIFF 6.0	Little Endian (PC)	Uncompressed	1	\N	\N	2	\N	\N	\N	\N	\N	\N	f	0	9479127	0	library internal use	3086	3071	400	8,8,8	integer	3	0	0	\N	2.2	100	\N	\N	f	\N	\N	\N	\N
260	1220	TIFF 6.0	Little Endian (PC)	Uncompressed	1	\N	\N	2	\N	\N	\N	\N	\N	\N	f	0	34078720	0	library internal use	4200	2704	400	8,8,8	integer	3	0	0	\N	2.2	100	\N	\N	f	\N	\N	\N	\N
261	1264	TIFF 6.0	Little Endian (PC)	Uncompressed	1	\N	\N	2	\N	\N	\N	\N	\N	\N	f	0	40160461	0	library internal use	4079	3278	400	8,8,8	integer	3	0	0	\N	2.2	100	\N	\N	f	\N	\N	\N	\N
262	1265	TIFF 6.0	Little Endian (PC)	Uncompressed	1	\N	\N	2	\N	\N	\N	\N	\N	\N	f	0	11848909	0	library internal use	1656	2388	400	8,8,8	integer	3	0	0	\N	2.2	100	\N	\N	f	\N	\N	\N	\N
263	1266	TIFF 6.0	Little Endian (PC)	Uncompressed	1	\N	\N	2	\N	\N	\N	\N	\N	\N	f	0	9741271	0	library internal use	2153	1508	400	8,8,8	integer	3	0	0	\N	2.2	100	\N	\N	f	\N	\N	\N	\N
264	1267	TIFF 6.0	Little Endian (PC)	Uncompressed	1	\N	\N	2	\N	\N	\N	\N	\N	\N	f	0	18245222	0	library internal use	2084	2911	400	8,8,8	integer	3	0	0	\N	2.2	100	\N	\N	f	\N	\N	\N	\N
265	1268	TIFF 6.0	Little Endian (PC)	Uncompressed	1	Adobe RGB 1998	\N	2	\N	\N	\N	\N	\N	\N	f	0	38063309	1	library internal use	3182	3992	400	8,8,8	integer	3	0	7	\N	2.2	100	\N	2006-06-23 00:00:00	f	\N	\N	\N	\N
266	1269	TIFF 6.0	Little Endian (PC)	Uncompressed	1	\N	\N	2	\N	\N	\N	\N	\N	\N	f	0	24117248	0	library internal use	3259	2467	400	8,8,8	integer	3	0	0	\N	2.2	100	\N	\N	f	\N	\N	\N	\N
267	1270	TIFF 6.0	Little Endian (PC)	Uncompressed	1	\N	\N	2	\N	\N	\N	\N	\N	\N	f	0	9122611	0	library internal use	2101	1447	400	8,8,8	integer	3	0	0	\N	2.2	100	\N	\N	f	\N	\N	\N	\N
268	1271	TIFF 6.0	Little Endian (PC)	Uncompressed	1	\N	\N	2	\N	\N	\N	\N	\N	\N	f	0	6322913	0	library internal use	1456	1447	400	8,8,8	integer	3	0	0	\N	2.2	100	\N	\N	f	\N	\N	\N	\N
269	1272	TIFF 6.0	Little Endian (PC)	Uncompressed	1	\N	\N	2	\N	\N	\N	\N	\N	\N	f	0	40370176	0	library internal use	3287	4096	400	8,8,8	integer	3	0	0	\N	2.2	100	\N	\N	f	\N	\N	\N	\N
270	1273	TIFF 6.0	Little Endian (PC)	Uncompressed	1	\N	\N	2	\N	\N	\N	\N	\N	\N	f	0	18245222	0	library internal use	2903	2902	400	8,8,8	integer	3	0	0	\N	2.2	100	\N	\N	f	\N	\N	\N	\N
271	1274	TIFF 6.0	Little Endian (PC)	Uncompressed	1	\N	\N	2	\N	\N	\N	\N	\N	\N	f	0	18245222	0	library internal use	2894	2100	400	8,8,8	integer	3	0	0	\N	2.2	100	\N	\N	f	\N	\N	\N	\N
272	1275	TIFF 6.0	Little Endian (PC)	Uncompressed	1	\N	\N	2	\N	\N	\N	\N	\N	\N	f	0	17930650	0	library internal use	2084	2876	400	8,8,8	integer	3	0	0	\N	2.2	100	\N	\N	f	\N	\N	\N	\N
273	1276	TIFF 6.0	Little Endian (PC)	Uncompressed	1	\N	\N	2	\N	\N	\N	\N	\N	\N	f	0	18035507	0	library internal use	2084	2893	400	8,8,8	integer	3	0	0	\N	2.2	100	\N	\N	f	\N	\N	\N	\N
302	1305	TIFF 6.0	Little Endian (PC)	Uncompressed	1	Adobe RGB 1998	\N	2	\N	\N	\N	\N	\N	\N	f	0	13002342	1	library internal use	2101	2057	400	8,8,8	integer	3	0	7	\N	2.2	100	\N	2006-06-23 00:00:00	f	\N	\N	\N	\N
303	1306	TIFF 6.0	Little Endian (PC)	Uncompressed	1	Adobe RGB 1998	\N	2	\N	\N	\N	\N	\N	\N	f	0	12373197	1	library internal use	1561	2649	400	8,8,8	integer	3	0	7	\N	2.2	100	\N	2006-06-23 00:00:00	f	\N	\N	\N	\N
304	1307	TIFF 6.0	Little Endian (PC)	Uncompressed	1	Adobe RGB 1998	\N	2	\N	\N	\N	\N	\N	\N	f	0	12373197	1	library internal use	1561	2649	400	8,8,8	integer	3	0	7	\N	2.2	100	\N	2006-06-23 00:00:00	f	\N	\N	\N	\N
305	1308	TIFF 6.0	Little Endian (PC)	Uncompressed	1	Adobe RGB 1998	\N	2	\N	\N	\N	\N	\N	\N	f	0	12373197	1	library internal use	1561	2649	400	8,8,8	integer	3	0	7	\N	2.2	100	\N	2006-06-23 00:00:00	f	\N	\N	\N	\N
306	1309	TIFF 6.0	Little Endian (PC)	Uncompressed	1	Adobe RGB 1998	\N	2	\N	\N	\N	\N	\N	\N	f	0	12373197	1	library internal use	1561	2649	400	8,8,8	integer	3	0	7	\N	2.2	100	\N	2006-06-23 00:00:00	f	\N	\N	\N	\N
307	1310	TIFF 6.0	Little Endian (PC)	Uncompressed	1	Adobe RGB 1998	\N	2	\N	\N	\N	\N	\N	\N	f	0	12373197	1	library internal use	1561	2649	400	8,8,8	integer	3	0	7	\N	2.2	100	\N	2006-06-23 00:00:00	f	\N	\N	\N	\N
308	1311	TIFF 6.0	Little Endian (PC)	Uncompressed	1	Adobe RGB 1998	\N	2	\N	\N	\N	\N	\N	\N	f	0	12373197	1	library internal use	1561	2649	400	8,8,8	integer	3	0	7	\N	2.2	100	\N	2006-06-23 00:00:00	f	\N	\N	\N	\N
309	1312	TIFF 6.0	Little Endian (PC)	Uncompressed	1	Adobe RGB 1998	\N	2	\N	\N	\N	\N	\N	\N	f	0	12373197	1	library internal use	1561	2649	400	8,8,8	integer	3	0	7	\N	2.2	100	\N	2006-06-23 00:00:00	f	\N	\N	\N	\N
310	1313	TIFF 6.0	Little Endian (PC)	Uncompressed	1	Adobe RGB 1998	\N	2	\N	\N	\N	\N	\N	\N	f	0	12373197	1	library internal use	1561	2649	400	8,8,8	integer	3	0	7	\N	2.2	100	\N	2006-06-23 00:00:00	f	\N	\N	\N	\N
311	1314	TIFF 6.0	Little Endian (PC)	Uncompressed	1	\N	\N	2	\N	\N	\N	\N	\N	\N	f	0	18245222	0	library internal use	2903	2092	400	8,8,8	integer	3	0	0	\N	2.2	100	\N	\N	f	\N	\N	\N	\N
312	1315	TIFF 6.0	Little Endian (PC)	Uncompressed	1	\N	\N	2	\N	\N	\N	\N	\N	\N	f	0	9258926	0	library internal use	2214	1394	400	8,8,8	integer	3	0	0	\N	2.2	100	\N	\N	f	\N	\N	\N	\N
313	1316	TIFF 6.0	Little Endian (PC)	Uncompressed	1	\N	\N	2	\N	\N	\N	\N	\N	\N	f	0	18140365	0	library internal use	2886	2100	400	8,8,8	integer	3	0	0	\N	2.2	100	\N	\N	f	\N	\N	\N	\N
314	1317	TIFF 6.0	Little Endian (PC)	Uncompressed	1	\N	\N	2	\N	\N	\N	\N	\N	\N	f	0	46137344	0	library internal use	3295	4671	400	8,8,8	integer	3	0	0	\N	2.2	100	\N	\N	f	\N	\N	\N	\N
315	1318	TIFF 6.0	Little Endian (PC)	Uncompressed	1	\N	\N	2	\N	\N	\N	\N	\N	\N	f	0	44669338	0	library internal use	3383	4401	400	8,8,8	integer	3	0	0	\N	2.2	100	\N	\N	f	\N	\N	\N	\N
316	1319	TIFF 6.0	Little Endian (PC)	Uncompressed	1	\N	\N	2	\N	\N	\N	\N	\N	\N	f	0	37643878	0	library internal use	3896	3217	400	8,8,8	integer	3	0	0	\N	2.2	100	\N	\N	f	\N	\N	\N	\N
317	1320	TIFF 6.0	Little Endian (PC)	Uncompressed	1	\N	\N	2	\N	\N	\N	\N	\N	\N	f	0	37434163	0	library internal use	3217	3878	400	8,8,8	integer	3	0	0	\N	2.2	100	\N	\N	f	\N	\N	\N	\N
318	1321	TIFF 6.0	Little Endian (PC)	Uncompressed	1	\N	\N	2	\N	\N	\N	\N	\N	\N	f	0	46766490	0	library internal use	3348	4654	400	8,8,8	integer	3	0	0	\N	2.2	100	\N	\N	f	\N	\N	\N	\N
319	1322	TIFF 6.0	Little Endian (PC)	Uncompressed	1	Adobe RBB 1998	\N	2	\N	\N	\N	\N	\N	\N	f	0	44459622	1	library internal use	3391	4375	400	8,8,8	integer	3	0	7	\N	2.2	100	\N	2006-06-27 00:00:00	f	\N	\N	\N	\N
320	1323	TIFF 6.0	Little Endian (PC)	Uncompressed	1	Adobe RBB 1998	\N	2	\N	\N	\N	\N	\N	\N	f	0	44459622	1	library internal use	3391	4375	400	8,8,8	integer	3	0	7	\N	2.2	100	\N	2006-06-27 00:00:00	f	\N	\N	\N	\N
321	1324	TIFF 6.0	Little Endian (PC)	Uncompressed	1	Adobe RBB 1998	\N	2	\N	\N	\N	\N	\N	\N	f	0	44459622	1	library internal use	3391	4375	400	8,8,8	integer	3	0	7	\N	2.2	100	\N	2006-06-27 00:00:00	f	\N	\N	\N	\N
322	1325	TIFF 6.0	Little Endian (PC)	Uncompressed	1	Adobe RBB 1998	\N	2	\N	\N	\N	\N	\N	\N	f	0	44459622	1	library internal use	3391	4375	400	8,8,8	integer	3	0	7	\N	2.2	100	\N	2006-06-27 00:00:00	f	\N	\N	\N	\N
323	1326	TIFF 6.0	Little Endian (PC)	Uncompressed	1	Adobe RBB 1998	\N	2	\N	\N	\N	\N	\N	\N	f	0	44459622	1	library internal use	3391	4375	400	8,8,8	integer	3	0	7	\N	2.2	100	\N	2006-06-27 00:00:00	f	\N	\N	\N	\N
324	1327	TIFF 6.0	Little Endian (PC)	Uncompressed	1	Adobe RBB 1998	\N	2	\N	\N	\N	\N	\N	\N	f	0	44459622	1	library internal use	3391	4375	400	8,8,8	integer	3	0	7	\N	2.2	100	\N	2006-06-27 00:00:00	f	\N	\N	\N	\N
325	1328	TIFF 6.0	Little Endian (PC)	Uncompressed	1	Adobe RBB 1998	\N	2	\N	\N	\N	\N	\N	\N	f	0	44459622	1	library internal use	3391	4375	400	8,8,8	integer	3	0	7	\N	2.2	100	\N	2006-06-27 00:00:00	f	\N	\N	\N	\N
326	1329	TIFF 6.0	Little Endian (PC)	Uncompressed	1	Adobe RBB 1998	\N	2	\N	\N	\N	\N	\N	\N	f	0	44459622	1	library internal use	3391	4375	400	8,8,8	integer	3	0	7	\N	2.2	100	\N	2006-06-27 00:00:00	f	\N	\N	\N	\N
327	1330	TIFF 6.0	Little Endian (PC)	Uncompressed	1	Adobe RBB 1998	\N	2	\N	\N	\N	\N	\N	\N	f	0	44459622	1	library internal use	3391	4375	400	8,8,8	integer	3	0	7	\N	2.2	100	\N	2006-06-27 00:00:00	f	\N	\N	\N	\N
328	1331	TIFF 6.0	Little Endian (PC)	Uncompressed	1	Adobe RBB 1998	\N	2	\N	\N	\N	\N	\N	\N	f	0	44459622	1	library internal use	3391	4375	400	8,8,8	integer	3	0	7	\N	2.2	100	\N	2006-06-27 00:00:00	f	\N	\N	\N	\N
329	1332	TIFF 6.0	Little Endian (PC)	Uncompressed	1	Adobe RBB 1998	\N	2	\N	\N	\N	\N	\N	\N	f	0	44459622	1	library internal use	3391	4375	400	8,8,8	integer	3	0	7	\N	2.2	100	\N	2006-06-27 00:00:00	f	\N	\N	\N	\N
330	1333	TIFF 6.0	Little Endian (PC)	Uncompressed	1	Adobe RBB 1998	\N	2	\N	\N	\N	\N	\N	\N	f	0	44459622	1	library internal use	3391	4375	400	8,8,8	integer	3	0	7	\N	2.2	100	\N	2006-06-27 00:00:00	f	\N	\N	\N	\N
331	1334	TIFF 6.0	Little Endian (PC)	Uncompressed	1	Adobe RBB 1998	\N	2	\N	\N	\N	\N	\N	\N	f	0	44459622	1	library internal use	3391	4375	400	8,8,8	integer	3	0	7	\N	2.2	100	\N	2006-06-27 00:00:00	f	\N	\N	\N	\N
332	1335	TIFF 6.0	Little Endian (PC)	Uncompressed	1	Adobe RBB 1998	\N	2	\N	\N	\N	\N	\N	\N	f	0	44459622	1	library internal use	3391	4375	400	8,8,8	integer	3	0	7	\N	2.2	100	\N	2006-06-27 00:00:00	f	\N	\N	\N	\N
333	1336	TIFF 6.0	Little Endian (PC)	Uncompressed	1	Adobe RBB 1998	\N	2	\N	\N	\N	\N	\N	\N	f	0	44459622	1	library internal use	3391	4375	400	8,8,8	integer	3	0	7	\N	2.2	100	\N	2006-06-27 00:00:00	f	\N	\N	\N	\N
334	1337	TIFF 6.0	Little Endian (PC)	Uncompressed	1	Adobe RBB 1998	\N	2	\N	\N	\N	\N	\N	\N	f	0	44459622	1	library internal use	3391	4375	400	8,8,8	integer	3	0	7	\N	2.2	100	\N	2006-06-27 00:00:00	f	\N	\N	\N	\N
335	1338	TIFF 6.0	Little Endian (PC)	Uncompressed	1	Adobe RBB 1998	\N	2	\N	\N	\N	\N	\N	\N	f	0	44459622	1	library internal use	3391	4375	400	8,8,8	integer	3	0	7	\N	2.2	100	\N	2006-06-27 00:00:00	f	\N	\N	\N	\N
336	1339	TIFF 6.0	Little Endian (PC)	Uncompressed	1	Adobe RBB 1998	\N	2	\N	\N	\N	\N	\N	\N	f	0	44459622	1	library internal use	3391	4375	400	8,8,8	integer	3	0	7	\N	2.2	100	\N	2006-06-27 00:00:00	f	\N	\N	\N	\N
337	1340	TIFF 6.0	Little Endian (PC)	Uncompressed	1	Adobe RBB 1998	\N	2	\N	\N	\N	\N	\N	\N	f	0	44459622	1	library internal use	3391	4375	400	8,8,8	integer	3	0	7	\N	2.2	100	\N	2006-06-27 00:00:00	f	\N	\N	\N	\N
338	1341	TIFF 6.0	Little Endian (PC)	Uncompressed	1	Adobe RBB 1998	\N	2	\N	\N	\N	\N	\N	\N	f	0	44459622	1	library internal use	3391	4375	400	8,8,8	integer	3	0	7	\N	2.2	100	\N	2006-06-27 00:00:00	f	\N	\N	\N	\N
339	1342	TIFF 6.0	Little Endian (PC)	Uncompressed	1	Adobe RBB 1998	\N	2	\N	\N	\N	\N	\N	\N	f	0	44459622	1	library internal use	3391	4375	400	8,8,8	integer	3	0	7	\N	2.2	100	\N	2006-06-27 00:00:00	f	\N	\N	\N	\N
340	1343	TIFF 6.0	Little Endian (PC)	Uncompressed	1	Adobe RBB 1998	\N	2	\N	\N	\N	\N	\N	\N	f	0	44459622	1	library internal use	3391	4375	400	8,8,8	integer	3	0	7	\N	2.2	100	\N	2006-06-27 00:00:00	f	\N	\N	\N	\N
341	1344	TIFF 6.0	Little Endian (PC)	Uncompressed	1	Adobe RBB 1998	\N	2	\N	\N	\N	\N	\N	\N	f	0	44459622	1	library internal use	3391	4375	400	8,8,8	integer	3	0	7	\N	2.2	100	\N	2006-06-27 00:00:00	f	\N	\N	\N	\N
343	1346	TIFF 6.0	Little Endian (PC)	Uncompressed	1	Adobe RBB 1998	\N	2	\N	\N	\N	\N	\N	\N	f	0	28730982	1	library internal use	3400	2815	400	8,8,8	integer	3	0	7	\N	2.2	100	\N	2006-06-27 00:00:00	f	\N	\N	\N	\N
344	1347	TIFF 6.0	Little Endian (PC)	Uncompressed	1	Adobe RBB 1998	\N	2	\N	\N	\N	\N	\N	\N	f	0	28730982	1	library internal use	3400	2815	400	8,8,8	integer	3	0	7	\N	2.2	100	Height 7 x Width 8.5	2006-06-27 00:00:00	f	\N	\N	\N	\N
350	1368	TIFF 6.0	Little Endian (PC)	Uncompressed	1	\N	\N	2	\N	\N	\N	\N	\N	\N	f	0	46137344	0	library internal use	3295	4671	400	8,8,8	integer	3	0	0	\N	2.2	100	\N	\N	f	\N	\N	\N	\N
351	1369	TIFF 6.0	Little Endian (PC)	Uncompressed	1	\N	\N	2	\N	\N	\N	\N	\N	\N	f	0	46347059	0	library internal use	3304	4680	400	8,8,8	integer	3	0	0	\N	2.2	100	\N	\N	f	\N	\N	\N	\N
352	1370	TIFF 6.0	Little Endian (PC)	Uncompressed	1	\N	\N	2	\N	\N	\N	\N	\N	\N	f	0	24012390	0	library internal use	2511	3192	400	8,8,8	integer	3	0	0	\N	2.2	100	\N	\N	f	\N	\N	\N	\N
353	1371	TIFF 6.0	Little Endian (PC)	Uncompressed	1	\N	\N	2	\N	\N	\N	\N	\N	\N	f	0	104962458	0	library internal use	5852	5981	400	8,8,8	integer	3	0	1	\N	2.2	100	\N	\N	f	\N	\N	\N	\N
354	1373	TIFF 6.0	Little Endian (PC)	Uncompressed	1	\N	\N	2	\N	\N	\N	\N	\N	\N	f	0	93637837	0	library internal use	4956	6300	400	8,8,8	integer	3	0	1	\N	2.2	100	\N	\N	f	\N	\N	\N	\N
355	1374	TIFF 6.0	Little Endian (PC)	Uncompressed	1	\N	\N	2	\N	\N	\N	\N	\N	\N	f	0	47710208	0	library internal use	3498	4544	600	8,8,8	integer	3	0	1	\N	2.2	100	\N	\N	f	\N	\N	\N	\N
356	1377	TIFF 6.0	Little Endian (PC)	Uncompressed	1	\N	\N	2	\N	\N	\N	\N	\N	\N	f	0	51485082	1	library internal use	3488	4920	400	8,8,8	integer	3	0	1	\N	2.2	100	\N	\N	f	\N	\N	\N	\N
357	1378	TIFF 6.0	Little Endian (PC)	Uncompressed	1	\N	\N	2	\N	\N	\N	\N	\N	\N	f	0	47081062	1	library internal use	3451	4548	400	8,8,8	integer	3	0	1	\N	2.2	100	\N	\N	f	\N	\N	\N	\N
358	1379	TIFF 6.0	Little Endian (PC)	Uncompressed	1	\N	\N	2	\N	\N	\N	\N	\N	\N	f	0	101607014	0	library internal use	5042	6720	400	8,8,8	integer	3	0	1	\N	2.2	100	\N	\N	f	\N	\N	\N	\N
359	1380	TIFF 6.0	Little Endian (PC)	Uncompressed	1	\N	\N	2	\N	\N	\N	\N	\N	\N	f	0	91855258	0	library internal use	5987	5112	400	8,8,8	integer	3	0	1	\N	2.2	100	\N	\N	f	\N	\N	\N	\N
360	1381	TIFF 6.0	Little Endian (PC)	Uncompressed	1	\N	\N	2	\N	\N	\N	\N	\N	\N	f	0	101502157	0	library internal use	6408	5280	400	8,8,8	integer	3	0	1	\N	2.2	100	\N	\N	f	\N	\N	\N	\N
361	1382	TIFF 6.0	Little Endian (PC)	Uncompressed	1	\N	\N	2	\N	\N	\N	\N	\N	\N	f	0	92484403	0	library internal use	5974	5160	400	8,8,8	integer	3	0	1	\N	2.2	100	\N	\N	f	\N	\N	\N	\N
362	1383	TIFF 6.0	Little Endian (PC)	Uncompressed	1	\N	\N	2	\N	\N	\N	\N	\N	\N	f	0	63648563	0	library internal use	4787	4430	400	8,8,8	integer	3	0	1	\N	2.2	100	\N	\N	f	\N	\N	\N	\N
363	1384	TIFF 6.0	Little Endian (PC)	Uncompressed	1	\N	\N	2	\N	\N	\N	\N	\N	\N	f	0	103704166	0	library internal use	5100	6780	400	8,8,8	integer	3	0	1	\N	2.2	100	\N	\N	f	\N	\N	\N	\N
364	1385	TIFF 6.0	Little Endian (PC)	Uncompressed	1	\N	\N	2	\N	\N	\N	\N	\N	\N	f	0	75078042	0	library internal use	4132	6054	400	8,8,8	integer	3	0	1	\N	2.2	100	\N	\N	f	\N	\N	\N	\N
365	1386	TIFF 6.0	Little Endian (PC)	Uncompressed	1	\N	\N	2	\N	\N	\N	\N	\N	\N	f	0	111673344	0	library internal use	5087	7320	400	8,8,8	integer	3	0	1	\N	2.2	100	\N	\N	f	\N	\N	\N	\N
366	1387	TIFF 6.0	Little Endian (PC)	Uncompressed	1	\N	\N	2	\N	\N	\N	\N	\N	\N	f	0	54840525	0	library internal use	4502	4059	400	8,8,8	integer	3	0	1	\N	2.2	100	\N	\N	f	\N	\N	\N	\N
367	1388	TIFF 6.0	Little Endian (PC)	Uncompressed	1	\N	\N	2	\N	\N	\N	\N	\N	\N	f	0	93008691	0	library internal use	4577	6772	400	8,8,8	integer	3	0	0	\N	2.2	100	\N	\N	f	\N	\N	\N	\N
368	1389	TIFF 6.0	Little Endian (PC)	Uncompressed	1	\N	\N	2	\N	\N	\N	\N	\N	\N	f	0	57357107	0	library internal use	4943	3870	400	8,8,8	integer	3	0	0	\N	2.2	100	\N	\N	f	\N	\N	\N	\N
369	1390	TIFF 6.0	Little Endian (PC)	Uncompressed	1	\N	\N	2	\N	\N	\N	\N	\N	\N	f	0	91435827	0	library internal use	4682	6510	400	8,8,8	integer	3	0	0	\N	2.2	100	\N	\N	f	\N	\N	\N	\N
370	1391	TIFF 6.0	Little Endian (PC)	Uncompressed	1	\N	\N	2	\N	\N	\N	\N	\N	\N	f	0	49597645	0	library internal use	3204	5160	400	8,8,8	integer	3	0	0	\N	2.2	100	\N	\N	f	\N	\N	\N	\N
371	1392	TIFF 6.0	Little Endian (PC)	Uncompressed	1	\N	\N	2	\N	\N	\N	\N	\N	\N	f	0	77909197	0	library internal use	4413	5883	400	8,8,8	integer	3	0	0	\N	2.2	100	\N	\N	f	\N	\N	\N	\N
372	1393	TIFF 6.0	Little Endian (PC)	Uncompressed	1	\N	\N	2	\N	\N	\N	\N	\N	\N	f	0	8839496	0	library internal use	3778	780	400	8,8,8	integer	3	0	0	\N	2.2	100	\N	\N	f	\N	\N	\N	\N
373	1394	TIFF 6.0	Little Endian (PC)	Uncompressed	1	\N	\N	2	\N	\N	\N	\N	\N	\N	f	0	44040192	0	library internal use	3381	4346	400	8,8,8	integer	3	0	0	\N	2.2	100	\N	\N	f	\N	\N	\N	\N
374	1395	TIFF 6.0	Little Endian (PC)	Uncompressed	1	\N	\N	2	\N	\N	\N	\N	\N	\N	f	0	40475034	0	library internal use	3390	3983	400	8,8,8	integer	3	0	0	\N	2.2	100	\N	\N	f	\N	\N	\N	\N
375	1396	TIFF 6.0	Little Endian (PC)	Uncompressed	1	\N	\N	2	\N	\N	\N	\N	\N	\N	f	0	16882074	0	library internal use	2827	1996	400	8,8,8	integer	3	0	0	\N	2.2	100	\N	\N	f	\N	\N	\N	\N
376	1397	TIFF 6.0	Little Endian (PC)	Uncompressed	1	\N	\N	2	\N	\N	\N	\N	\N	\N	f	0	43620762	0	library internal use	3371	4317	400	8,8,8	integer	3	0	0	\N	2.2	100	\N	\N	f	\N	\N	\N	\N
377	1398	TIFF 6.0	Little Endian (PC)	Uncompressed	1	\N	\N	2	\N	\N	\N	\N	\N	\N	f	0	43830477	0	library internal use	3362	4346	400	8,8,8	integer	3	0	0	\N	2.2	100	\N	\N	f	\N	\N	\N	\N
378	1399	TIFF 6.0	Little Endian (PC)	Uncompressed	1	\N	\N	2	\N	\N	\N	\N	\N	\N	f	0	12687770	0	library internal use	1508	2680	400	8,8,8	integer	3	0	0	\N	2.2	100	\N	\N	f	\N	\N	\N	\N
379	1400	TIFF 6.0	Little Endian (PC)	Uncompressed	1	\N	\N	2	\N	\N	\N	\N	\N	\N	f	0	27787264	0	library internal use	2680	3456	400	8,8,8	integer	3	0	0	\N	2.2	100	\N	\N	f	\N	\N	\N	\N
380	1401	TIFF 6.0	Little Endian (PC)	Uncompressed	1	\N	\N	2	\N	\N	\N	\N	\N	\N	f	0	10695475	0	library internal use	2120	1680	400	8,8,8	integer	3	0	0	\N	2.2	100	\N	\N	f	\N	\N	\N	\N
381	1402	TIFF 6.0	Little Endian (PC)	Uncompressed	1	\N	\N	2	\N	\N	\N	\N	\N	\N	f	0	20866662	0	library internal use	2040	3416	400	8,8,8	integer	3	0	0	\N	2.2	100	\N	\N	f	\N	\N	\N	\N
382	1403	TIFF 6.0	Little Endian (PC)	Uncompressed	1	\N	\N	2	\N	\N	\N	\N	\N	\N	f	0	19713229	0	library internal use	2016	3268	400	8,8,8	integer	3	0	0	\N	2.2	100	\N	\N	f	\N	\N	\N	\N
383	1404	TIFF 6.0	Little Endian (PC)	Uncompressed	1	\N	\N	2	\N	\N	\N	\N	\N	\N	f	0	6721372	0	library internal use	1140	1964	400	8,8,8	integer	3	0	0	\N	2.2	100	\N	\N	f	\N	\N	\N	\N
384	1405	TIFF 6.0	Little Endian (PC)	Uncompressed	1	\N	\N	2	\N	\N	\N	\N	\N	\N	f	0	16986931	0	library internal use	1960	2884	400	8,8,8	integer	3	0	0	\N	2.2	100	\N	\N	f	\N	\N	\N	\N
385	1406	TIFF 6.0	Little Endian (PC)	Uncompressed	1	\N	\N	2	\N	\N	\N	\N	\N	\N	f	0	18245222	0	library internal use	1938	3144	400	8,8,8	integer	3	0	0	\N	2.2	100	\N	\N	f	\N	\N	\N	\N
386	1407	TIFF 6.0	Little Endian (PC)	Uncompressed	1	\N	\N	2	\N	\N	\N	\N	\N	\N	f	0	19503514	0	library internal use	2834	2288	400	8,8,8	integer	3	0	0	\N	2.2	100	\N	\N	f	\N	\N	\N	\N
387	1408	TIFF 6.0	Little Endian (PC)	Uncompressed	1	\N	\N	2	\N	\N	\N	\N	\N	\N	f	0	10695475	0	library internal use	1073	3309	400	8,8,8	integer	3	0	0	\N	2.2	100	\N	\N	f	\N	\N	\N	\N
388	1409	TIFF 6.0	Little Endian (PC)	Uncompressed	1	\N	\N	2	\N	\N	\N	\N	\N	\N	f	0	33869005	0	library internal use	3920	2880	400	8,8,8	integer	3	0	0	\N	2.2	100	\N	\N	f	\N	\N	\N	\N
389	1410	TIFF 6.0	Little Endian (PC)	Uncompressed	1	\N	\N	2	\N	\N	\N	\N	\N	\N	f	0	4372562	0	library internal use	1053	1383	400	8,8,8	integer	3	0	0	\N	2.2	100	\N	\N	f	\N	\N	\N	\N
390	1411	TIFF 6.0	Little Endian (PC)	Uncompressed	1	\N	\N	2	\N	\N	\N	\N	\N	\N	f	0	29045555	0	library internal use	2986	3240	400	8,8,8	integer	3	0	0	\N	2.2	100	\N	\N	f	\N	\N	\N	\N
391	1412	TIFF 6.0	Little Endian (PC)	Uncompressed	1	\N	\N	2	\N	\N	\N	\N	\N	\N	f	0	31142707	0	library internal use	2666	3890	400	8,8,8	integer	3	0	0	\N	2.2	100	\N	\N	f	\N	\N	\N	\N
392	1413	TIFF 6.0	Little Endian (PC)	Uncompressed	1	\N	\N	2	\N	\N	\N	\N	\N	\N	f	0	29989274	0	library internal use	2720	3676	400	8,8,8	integer	3	0	0	\N	2.2	100	\N	\N	f	\N	\N	\N	\N
393	1414	TIFF 6.0	Little Endian (PC)	Uncompressed	1	\N	\N	2	\N	\N	\N	\N	\N	\N	f	0	25060966	0	library internal use	3276	2548	400	8,8,8	integer	3	0	0	\N	2.2	100	\N	\N	f	\N	\N	\N	\N
394	1415	TIFF 6.0	Little Endian (PC)	Uncompressed	1	\N	\N	2	\N	\N	\N	\N	\N	\N	f	0	24536678	0	library internal use	3240	2526	400	8,8,8	integer	3	0	0	\N	2.2	100	\N	\N	f	\N	\N	\N	\N
395	1416	TIFF 6.0	Little Endian (PC)	Uncompressed	1	\N	\N	2	\N	\N	\N	\N	\N	\N	f	0	20761805	0	library internal use	2731	2532	400	8,8,8	integer	3	0	0	\N	2.2	100	\N	\N	f	\N	\N	\N	\N
396	1417	TIFF 6.0	Little Endian (PC)	Uncompressed	1	\N	\N	2	\N	\N	\N	\N	\N	\N	f	0	25270682	0	library internal use	3304	2548	400	8,8,8	integer	3	0	0	\N	2.2	100	\N	\N	f	\N	\N	\N	\N
397	1418	TIFF 6.0	Little Endian (PC)	Uncompressed	1	\N	\N	2	\N	\N	\N	\N	\N	\N	f	0	25690112	0	library internal use	3344	2560	400	8,8,8	integer	3	0	0	\N	2.2	100	\N	\N	f	\N	\N	\N	\N
398	1419	TIFF 6.0	Little Endian (PC)	Uncompressed	1	\N	\N	2	\N	\N	\N	\N	\N	\N	f	0	25165824	0	library internal use	3311	2536	400	8,8,8	integer	3	0	0	\N	2.2	100	\N	\N	f	\N	\N	\N	\N
399	1420	TIFF 6.0	Little Endian (PC)	Uncompressed	1	\N	\N	2	\N	\N	\N	\N	\N	\N	f	0	24851251	0	library internal use	3220	2568	400	8,8,8	integer	3	0	0	\N	2.2	100	\N	\N	f	\N	\N	\N	\N
400	1421	TIFF 6.0	Little Endian (PC)	Uncompressed	1	\N	\N	2	\N	\N	\N	\N	\N	\N	f	0	17930650	0	library internal use	1907	3140	400	8,8,8	integer	3	0	0	\N	2.2	100	\N	\N	f	\N	\N	\N	\N
401	1422	TIFF 6.0	Little Endian (PC)	Uncompressed	1	\N	\N	2	\N	\N	\N	\N	\N	\N	f	0	27053261	0	library internal use	3210	2804	400	8,8,8	integer	3	0	0	\N	2.2	100	\N	\N	f	\N	\N	\N	\N
402	1423	TIFF 6.0	Little Endian (PC)	Uncompressed	1	\N	\N	2	\N	\N	\N	\N	\N	\N	f	0	26738688	0	library internal use	2615	3412	400	8,8,8	integer	3	0	0	\N	2.2	100	\N	\N	f	\N	\N	\N	\N
403	1424	TIFF 6.0	Little Endian (PC)	Uncompressed	1	\N	\N	2	\N	\N	\N	\N	\N	\N	f	0	40684749	0	library internal use	3298	4108	400	8,8,8	integer	3	0	0	\N	2.2	100	\N	\N	f	\N	\N	\N	\N
404	1425	TIFF 6.0	Little Endian (PC)	Uncompressed	1	\N	\N	2	\N	\N	\N	\N	\N	\N	f	0	38692454	0	library internal use	4039	3197	400	8,8,8	integer	3	0	0	\N	2.2	100	\N	\N	f	\N	\N	\N	\N
405	1426	TIFF 6.0	Little Endian (PC)	Uncompressed	1	\N	\N	2	\N	\N	\N	\N	\N	\N	f	0	38692454	0	library internal use	4043	3191	400	8,8,8	integer	3	0	0	\N	2.2	100	\N	\N	f	\N	\N	\N	\N
406	1427	TIFF 6.0	Little Endian (PC)	Uncompressed	1	\N	\N	2	\N	\N	\N	\N	\N	\N	f	0	38692454	0	library internal use	4000	3221	400	8,8,8	integer	3	0	0	\N	2.2	100	\N	\N	f	\N	\N	\N	\N
407	1428	TIFF 6.0	Little Endian (PC)	Uncompressed	1	\N	\N	2	\N	\N	\N	\N	\N	\N	f	0	38692454	0	library internal use	3204	4024	400	8,8,8	integer	3	0	0	\N	2.2	100	\N	\N	f	\N	\N	\N	\N
408	1429	TIFF 6.0	Little Endian (PC)	Uncompressed	1	\N	\N	2	\N	\N	\N	\N	\N	\N	f	0	39007027	0	library internal use	4076	3192	400	8,8,8	integer	3	0	0	\N	2.2	100	\N	\N	f	\N	\N	\N	\N
409	1430	TIFF 6.0	Little Endian (PC)	Uncompressed	1	\N	\N	2	\N	\N	\N	\N	\N	\N	f	0	13002342	0	library internal use	2418	1786	400	8,8,8	integer	3	0	0	\N	2.2	100	\N	\N	f	\N	\N	\N	\N
410	1431	TIFF 6.0	Little Endian (PC)	Uncompressed	1	\N	\N	2	\N	\N	\N	\N	\N	\N	f	0	17825792	0	library internal use	2842	2092	400	8,8,8	integer	3	0	0	\N	2.2	100	\N	\N	f	\N	\N	\N	\N
411	1432	TIFF 6.0	Little Endian (PC)	Uncompressed	1	\N	\N	2	\N	\N	\N	\N	\N	\N	f	0	25794970	0	library internal use	3267	2628	400	8,8,8	integer	3	0	0	\N	2.2	100	\N	\N	f	\N	\N	\N	\N
412	1433	TIFF 6.0	Little Endian (PC)	Uncompressed	1	\N	\N	2	\N	\N	\N	\N	\N	\N	f	0	26004685	0	library internal use	3400	2551	400	8,8,8	integer	3	0	0	\N	2.2	100	\N	\N	f	\N	\N	\N	\N
413	1434	TIFF 6.0	Little Endian (PC)	Uncompressed	1	\N	\N	2	\N	\N	\N	\N	\N	\N	f	0	31352422	0	library internal use	3669	2848	400	8,8,8	integer	3	0	0	\N	2.2	100	\N	\N	f	\N	\N	\N	\N
414	1435	TIFF 6.0	Little Endian (PC)	Uncompressed	1	\N	\N	2	\N	\N	\N	\N	\N	\N	f	0	26633830	0	library internal use	3400	2615	400	8,8,8	integer	3	0	0	\N	2.2	100	\N	\N	f	\N	\N	\N	\N
415	1436	TIFF 6.0	Little Endian (PC)	Uncompressed	1	\N	\N	2	\N	\N	\N	\N	\N	\N	f	0	38797312	0	library internal use	3184	4064	400	8,8,8	integer	3	0	0	\N	2.2	100	\N	\N	f	\N	\N	\N	\N
416	1437	TIFF 6.0	Little Endian (PC)	Uncompressed	1	\N	\N	2	\N	\N	\N	\N	\N	\N	f	0	26528973	0	library internal use	2584	3420	400	8,8,8	integer	3	0	0	\N	2.2	100	\N	\N	f	\N	\N	\N	\N
417	1439	TIFF 6.0	Little Endian (PC)	Uncompressed	1	\N	\N	2	\N	\N	\N	\N	\N	\N	f	0	29674701	0	library internal use	3644	2714	400	8,8,8	integer	3	0	0	\N	2.2	100	\N	\N	f	\N	\N	\N	\N
418	1440	TIFF 6.0	Little Endian (PC)	Uncompressed	1	\N	\N	2	\N	\N	\N	\N	\N	\N	f	0	20761805	0	library internal use	2295	3008	400	8,8,8	integer	3	0	0	\N	2.2	100	\N	\N	f	\N	\N	\N	\N
419	1441	TIFF 6.0	Little Endian (PC)	Uncompressed	1	\N	\N	2	\N	\N	\N	\N	\N	\N	f	0	26528973	0	library internal use	3400	2600	400	8,8,8	integer	3	0	0	\N	2.2	100	\N	\N	f	\N	\N	\N	\N
420	1442	TIFF 6.0	Little Endian (PC)	Uncompressed	1	\N	\N	2	\N	\N	\N	\N	\N	\N	f	0	26633830	0	library internal use	3400	2608	400	8,8,8	integer	3	0	0	\N	2.2	100	\N	\N	f	\N	\N	\N	\N
421	1443	TIFF 6.0	Little Endian (PC)	Uncompressed	1	\N	\N	2	\N	\N	\N	\N	\N	\N	f	0	30303846	0	library internal use	3667	2755	400	8,8,8	integer	3	0	0	\N	2.2	100	\N	\N	f	\N	\N	\N	\N
422	1444	TIFF 6.0	Little Endian (PC)	Uncompressed	1	\N	\N	2	\N	\N	\N	\N	\N	\N	f	0	30723277	0	library internal use	2784	3680	400	8,8,8	integer	3	0	0	\N	2.2	100	\N	\N	f	\N	\N	\N	\N
423	1445	TIFF 6.0	Little Endian (PC)	Uncompressed	1	\N	\N	2	\N	\N	\N	\N	\N	\N	f	0	30408704	0	library internal use	3679	2752	400	8,8,8	integer	3	0	0	\N	2.2	100	\N	\N	f	\N	\N	\N	\N
424	1446	TIFF 6.0	Little Endian (PC)	Uncompressed	1	\N	\N	2	\N	\N	\N	\N	\N	\N	f	0	24326963	0	library internal use	2834	2856	400	8,8,8	integer	3	0	0	\N	2.2	100	\N	\N	f	\N	\N	\N	\N
425	1447	TIFF 6.0	Little Endian (PC)	Uncompressed	1	\N	\N	2	\N	\N	\N	\N	\N	\N	f	0	38902170	0	library internal use	4052	3203	400	8,8,8	integer	3	0	0	\N	2.2	100	\N	\N	f	\N	\N	\N	\N
426	1448	TIFF 6.0	Little Endian (PC)	Uncompressed	1	\N	\N	2	\N	\N	\N	\N	\N	\N	f	0	28940698	0	library internal use	2851	3388	400	8,8,8	integer	3	0	0	\N	2.2	100	\N	\N	f	\N	\N	\N	\N
427	1449	TIFF 6.0	Little Endian (PC)	Uncompressed	1	\N	\N	2	\N	\N	\N	\N	\N	\N	f	0	30198989	0	library internal use	3700	2716	400	8,8,8	integer	3	0	0	\N	2.2	100	\N	\N	f	\N	\N	\N	\N
428	1450	TIFF 6.0	Little Endian (PC)	Uncompressed	1	\N	\N	2	\N	\N	\N	\N	\N	\N	f	0	30723277	0	library internal use	3700	2767	400	8,8,8	integer	3	0	0	\N	2.2	100	\N	\N	f	\N	\N	\N	\N
429	1451	TIFF 6.0	Little Endian (PC)	Uncompressed	1	\N	\N	2	\N	\N	\N	\N	\N	\N	f	0	30303846	0	library internal use	3655	2767	400	8,8,8	integer	3	0	0	\N	2.2	100	\N	\N	f	\N	\N	\N	\N
430	1452	TIFF 6.0	Little Endian (PC)	Uncompressed	1	\N	\N	2	\N	\N	\N	\N	\N	\N	f	0	37958451	0	library internal use	3167	3996	400	8,8,8	integer	3	0	0	\N	2.2	100	\N	\N	f	\N	\N	\N	\N
431	1453	TIFF 6.0	Little Endian (PC)	Uncompressed	1	\N	\N	2	\N	\N	\N	\N	\N	\N	f	0	37434163	0	library internal use	4051	3076	400	8,8,8	integer	3	0	0	\N	2.2	100	\N	\N	f	\N	\N	\N	\N
432	1454	TIFF 6.0	Little Endian (PC)	Uncompressed	1	\N	\N	2	\N	\N	\N	\N	\N	\N	f	0	38482739	0	library internal use	4048	3167	400	8,8,8	integer	3	0	0	\N	2.2	100	\N	\N	f	\N	\N	\N	\N
433	1455	TIFF 6.0	Little Endian (PC)	Uncompressed	1	\N	\N	2	\N	\N	\N	\N	\N	\N	f	0	38692454	0	library internal use	4051	3185	400	8,8,8	integer	3	0	0	\N	2.2	100	\N	\N	f	\N	\N	\N	\N
434	1456	TIFF 6.0	Little Endian (PC)	Uncompressed	1	\N	\N	2	\N	\N	\N	\N	\N	\N	f	0	22649242	0	library internal use	2384	3172	400	8,8,8	integer	3	0	0	\N	2.2	100	\N	\N	f	\N	\N	\N	\N
435	1457	TIFF 6.0	Little Endian (PC)	Uncompressed	1	\N	\N	2	\N	\N	\N	\N	\N	\N	f	0	23488102	0	library internal use	2434	3212	400	8,8,8	integer	3	0	0	\N	2.2	100	\N	\N	f	\N	\N	\N	\N
436	1458	TIFF 6.0	Little Endian (PC)	Uncompressed	1	\N	\N	2	\N	\N	\N	\N	\N	\N	f	0	22963814	0	library internal use	2400	3195	400	8,8,8	integer	3	0	0	\N	2.2	100	\N	\N	f	\N	\N	\N	\N
437	1459	TIFF 6.0	Little Endian (PC)	Uncompressed	1	\N	\N	2	\N	\N	\N	\N	\N	\N	f	0	22858957	0	library internal use	2400	3172	400	8,8,8	integer	3	0	0	\N	2.2	100	\N	\N	f	\N	\N	\N	\N
438	1460	TIFF 6.0	Little Endian (PC)	Uncompressed	1	\N	\N	2	\N	\N	\N	\N	\N	\N	f	0	6532628	0	library internal use	1700	1280	200	8,8,8	integer	3	0	0	\N	2.2	100	\N	\N	f	\N	\N	\N	\N
439	1461	TIFF 6.0	Little Endian (PC)	Uncompressed	1	\N	\N	2	\N	\N	\N	\N	\N	\N	f	0	7319060	0	library internal use	1798	1356	200	8,8,8	integer	3	0	0	\N	2.2	100	\N	\N	f	\N	\N	\N	\N
440	1462	TIFF 6.0	Little Endian (PC)	Uncompressed	1	\N	\N	2	\N	\N	\N	\N	\N	\N	f	0	9552527	0	library internal use	1996	1596	200	8,8,8	integer	3	0	0	\N	2.2	100	\N	\N	f	\N	\N	\N	\N
441	1463	TIFF 6.0	Little Endian (PC)	Uncompressed	1	\N	\N	2	\N	\N	\N	\N	\N	\N	f	0	7319060	0	library internal use	2014	1211	200	8,8,8	integer	3	0	0	\N	2.2	100	\N	\N	f	\N	\N	\N	\N
442	1464	TIFF 6.0	Little Endian (PC)	Uncompressed	1	\N	\N	2	\N	\N	\N	\N	\N	\N	f	0	9573499	0	library internal use	1992	1602	200	8,8,8	integer	3	0	0	\N	2.2	100	\N	\N	f	\N	\N	\N	\N
443	1465	TIFF 6.0	Little Endian (PC)	Uncompressed	1	\N	\N	2	\N	\N	\N	\N	\N	\N	f	0	8965325	0	library internal use	1534	1948	200	8,8,8	integer	3	0	0	\N	2.2	100	\N	\N	f	\N	\N	\N	\N
444	1466	TIFF 6.0	Little Endian (PC)	Uncompressed	1	\N	\N	2	\N	\N	\N	\N	\N	\N	f	0	6553600	0	library internal use	1700	1286	200	8,8,8	integer	3	0	0	\N	2.2	100	\N	\N	f	\N	\N	\N	\N
445	1467	TIFF 6.0	Little Endian (PC)	Uncompressed	1	\N	\N	2	\N	\N	\N	\N	\N	\N	f	0	26528973	0	library internal use	2620	3380	400	8,8,8	integer	3	0	0	\N	2.2	100	\N	\N	f	\N	\N	\N	\N
446	1468	TIFF 6.0	Little Endian (PC)	Uncompressed	1	\N	\N	2	\N	\N	\N	\N	\N	\N	f	0	9258926	0	library internal use	2179	1416	200	8,8,8	integer	3	0	0	\N	2.2	100	\N	\N	f	\N	\N	\N	\N
447	1469	TIFF 6.0	Little Endian (PC)	Uncompressed	1	\N	\N	2	\N	\N	\N	\N	\N	\N	f	0	9500099	0	library internal use	1584	2000	200	8,8,8	integer	3	0	0	\N	2.2	100	\N	\N	f	\N	\N	\N	\N
448	1470	TIFF 6.0	Little Endian (PC)	Uncompressed	1	\N	\N	2	\N	\N	\N	\N	\N	\N	f	0	6553600	0	library internal use	1300	1680	200	8,8,8	integer	3	0	0	\N	2.2	100	\N	\N	f	\N	\N	\N	\N
449	1471	TIFF 6.0	Little Endian (PC)	Uncompressed	1	\N	\N	2	\N	\N	\N	\N	\N	\N	f	0	9542042	0	library internal use	1996	1593	200	8,8,8	integer	3	0	0	\N	2.2	100	\N	\N	f	\N	\N	\N	\N
450	1472	TIFF 6.0	Little Endian (PC)	Uncompressed	1	\N	\N	2	\N	\N	\N	\N	\N	\N	f	0	9468641	0	library internal use	1592	1983	200	8,8,8	integer	3	0	0	\N	2.2	100	\N	\N	f	\N	\N	\N	\N
451	1473	TIFF 6.0	Little Endian (PC)	Uncompressed	1	\N	\N	2	\N	\N	\N	\N	\N	\N	f	0	9594470	0	library internal use	1596	2004	200	8,8,8	integer	3	0	0	\N	2.2	100	\N	\N	f	\N	\N	\N	\N
452	1474	TIFF 6.0	Little Endian (PC)	Uncompressed	1	\N	\N	2	\N	\N	\N	\N	\N	\N	f	0	9437184	0	library internal use	1966	1600	200	8,8,8	integer	3	0	0	\N	2.2	100	\N	\N	f	\N	\N	\N	\N
453	1475	TIFF 6.0	Little Endian (PC)	Uncompressed	1	\N	\N	2	\N	\N	\N	\N	\N	\N	f	0	38902170	0	library internal use	3226	4020	400	8,8,8	integer	3	0	0	\N	2.2	100	\N	\N	f	\N	\N	\N	\N
454	1476	TIFF 6.0	Little Endian (PC)	Uncompressed	1	\N	\N	2	\N	\N	\N	\N	\N	\N	f	0	9563013	0	library internal use	1998	1595	200	8,8,8	integer	3	0	0	\N	2.2	100	\N	\N	f	\N	\N	\N	\N
455	1477	TIFF 6.0	Little Endian (PC)	Uncompressed	1	\N	\N	2	\N	\N	\N	\N	\N	\N	f	0	9552527	0	library internal use	1592	2000	200	8,8,8	integer	3	0	0	\N	2.2	100	\N	\N	f	\N	\N	\N	\N
456	1478	TIFF 6.0	Little Endian (PC)	Uncompressed	1	\N	\N	2	\N	\N	\N	\N	\N	\N	f	0	9395241	0	library internal use	1592	1968	200	8,8,8	integer	3	0	0	\N	2.2	100	\N	\N	f	\N	\N	\N	\N
457	1479	TIFF 6.0	Little Endian (PC)	Uncompressed	1	\N	\N	2	\N	\N	\N	\N	\N	\N	f	0	9374269	0	library internal use	1972	1584	200	8,8,8	integer	3	0	0	\N	2.2	100	\N	\N	f	\N	\N	\N	\N
458	1480	TIFF 6.0	Little Endian (PC)	Uncompressed	1	\N	\N	2	\N	\N	\N	\N	\N	\N	f	0	9437184	0	library internal use	1970	1596	200	8,8,8	integer	3	0	0	\N	2.2	100	\N	\N	f	\N	\N	\N	\N
459	1481	TIFF 6.0	Little Endian (PC)	Uncompressed	1	\N	\N	2	\N	\N	\N	\N	\N	\N	f	0	9447670	0	library internal use	1970	1599	200	8,8,8	integer	3	0	0	\N	2.2	100	\N	\N	f	\N	\N	\N	\N
460	1482	TIFF 6.0	Little Endian (PC)	Uncompressed	1	\N	\N	2	\N	\N	\N	\N	\N	\N	f	0	9342812	0	library internal use	1966	1584	200	8,8,8	integer	3	0	0	\N	2.2	100	\N	\N	f	\N	\N	\N	\N
461	1483	TIFF 6.0	Little Endian (PC)	Uncompressed	1	\N	\N	2	\N	\N	\N	\N	\N	\N	f	0	5599396	0	library internal use	1184	1576	200	8,8,8	integer	3	0	0	\N	2.2	100	\N	\N	f	\N	\N	\N	\N
462	1484	TIFF 6.0	Little Endian (PC)	Uncompressed	1	\N	\N	2	\N	\N	\N	\N	\N	\N	f	0	9447670	0	library internal use	1990	1583	200	8,8,8	integer	3	0	0	\N	2.2	100	\N	\N	f	\N	\N	\N	\N
463	1485	TIFF 6.0	Little Endian (PC)	Uncompressed	1	\N	\N	2	\N	\N	\N	\N	\N	\N	f	0	9594470	0	library internal use	1980	1616	200	8,8,8	integer	3	0	0	\N	2.2	100	\N	\N	f	\N	\N	\N	\N
464	1486	TIFF 6.0	Little Endian (PC)	Uncompressed	1	\N	\N	2	\N	\N	\N	\N	\N	\N	f	0	9583985	0	library internal use	1998	1599	200	8,8,8	integer	3	0	0	\N	2.2	100	\N	\N	f	\N	\N	\N	\N
465	1487	TIFF 6.0	Little Endian (PC)	Uncompressed	1	\N	\N	2	\N	\N	\N	\N	\N	\N	f	0	9489613	0	library internal use	1978	1599	200	8,8,8	integer	3	0	0	\N	2.2	100	\N	\N	f	\N	\N	\N	\N
466	1488	TIFF 6.0	Little Endian (PC)	Uncompressed	1	\N	\N	2	\N	\N	\N	\N	\N	\N	f	0	9458156	0	library internal use	1976	1595	200	8,8,8	integer	3	0	0	\N	2.2	100	\N	\N	f	\N	\N	\N	\N
467	1489	TIFF 6.0	Little Endian (PC)	Uncompressed	1	\N	\N	2	\N	\N	\N	\N	\N	\N	f	0	9342812	0	library internal use	1563	1992	200	8,8,8	integer	3	0	0	\N	2.2	100	\N	\N	f	\N	\N	\N	\N
468	1490	TIFF 6.0	Little Endian (PC)	Uncompressed	1	\N	\N	2	\N	\N	\N	\N	\N	\N	f	0	39007027	0	library internal use	3199	4064	400	8,8,8	integer	3	0	0	\N	2.2	100	\N	\N	f	\N	\N	\N	\N
469	1491	TIFF 6.0	Little Endian (PC)	Uncompressed	1	\N	\N	2	\N	\N	\N	\N	\N	\N	f	0	9458156	0	library internal use	1990	1584	200	8,8,8	integer	3	0	0	\N	2.2	100	\N	\N	f	\N	\N	\N	\N
470	1492	TIFF 6.0	Little Endian (PC)	Uncompressed	1	\N	\N	2	\N	\N	\N	\N	\N	\N	f	0	9531556	0	library internal use	1584	2006	200	8,8,8	integer	3	0	0	\N	2.2	100	\N	\N	f	\N	\N	\N	\N
471	1493	TIFF 6.0	Little Endian (PC)	Uncompressed	1	\N	\N	2	\N	\N	\N	\N	\N	\N	f	0	9395241	0	library internal use	1978	1584	200	8,8,8	integer	3	0	0	\N	2.2	100	\N	\N	f	\N	\N	\N	\N
472	1494	TIFF 6.0	Little Endian (PC)	Uncompressed	1	\N	\N	2	\N	\N	\N	\N	\N	\N	f	0	9049211	0	library internal use	2164	1394	200	8,8,8	integer	3	0	0	\N	2.2	100	\N	\N	f	\N	\N	\N	\N
473	1495	TIFF 6.0	Little Endian (PC)	Uncompressed	1	\N	\N	2	\N	\N	\N	\N	\N	\N	f	0	9321841	0	library internal use	1576	1972	200	8,8,8	integer	3	0	0	\N	2.2	100	\N	\N	f	\N	\N	\N	\N
474	1496	TIFF 6.0	Little Endian (PC)	Uncompressed	1	\N	\N	2	\N	\N	\N	\N	\N	\N	f	0	9290383	0	library internal use	1576	1966	200	8,8,8	integer	3	0	0	\N	2.2	100	\N	\N	f	\N	\N	\N	\N
475	1497	TIFF 6.0	Little Endian (PC)	Uncompressed	1	\N	\N	2	\N	\N	\N	\N	\N	\N	f	0	9342812	0	library internal use	1974	1578	200	8,8,8	integer	3	0	0	\N	2.2	100	\N	\N	f	\N	\N	\N	\N
476	1498	TIFF 6.0	Little Endian (PC)	Uncompressed	1	\N	\N	2	\N	\N	\N	\N	\N	\N	f	0	5756682	0	library internal use	1609	1192	200	8,8,8	integer	3	0	0	\N	2.2	100	\N	\N	f	\N	\N	\N	\N
477	1499	TIFF 6.0	Little Endian (PC)	Uncompressed	1	\N	\N	2	\N	\N	\N	\N	\N	\N	f	0	5725225	0	library internal use	1609	1186	200	8,8,8	integer	3	0	0	\N	2.2	100	\N	\N	f	\N	\N	\N	\N
478	1500	TIFF 6.0	Little Endian (PC)	Uncompressed	1	\N	\N	2	\N	\N	\N	\N	\N	\N	f	0	9437184	0	library internal use	1987	1584	200	8,8,8	integer	3	0	0	\N	2.2	100	\N	\N	f	\N	\N	\N	\N
479	1501	TIFF 6.0	Little Endian (PC)	Uncompressed	1	\N	\N	2	\N	\N	\N	\N	\N	\N	f	0	9542042	0	library internal use	2000	1590	200	8,8,8	integer	3	0	0	\N	2.2	100	\N	\N	f	\N	\N	\N	\N
480	1502	TIFF 6.0	Little Endian (PC)	Uncompressed	1	\N	\N	2	\N	\N	\N	\N	\N	\N	f	0	5725225	0	library internal use	1592	1198	200	8,8,8	integer	3	0	0	\N	2.2	100	\N	\N	f	\N	\N	\N	\N
481	1503	TIFF 6.0	Little Endian (PC)	Uncompressed	1	\N	\N	2	\N	\N	\N	\N	\N	\N	f	0	5746196	0	library internal use	1609	1190	200	8,8,8	integer	3	0	0	\N	2.2	100	\N	\N	f	\N	\N	\N	\N
482	1504	TIFF 6.0	Little Endian (PC)	Uncompressed	1	\N	\N	2	\N	\N	\N	\N	\N	\N	f	0	23488102	0	library internal use	2460	3176	400	8,8,8	integer	3	0	0	\N	2.2	100	\N	\N	f	\N	\N	\N	\N
483	1505	TIFF 6.0	Little Endian (PC)	Uncompressed	1	\N	\N	2	\N	\N	\N	\N	\N	\N	f	0	23697818	0	library internal use	3233	2444	400	8,8,8	integer	3	0	0	\N	2.2	100	\N	\N	f	\N	\N	\N	\N
484	1506	TIFF 6.0	Little Endian (PC)	Uncompressed	1	\N	\N	2	\N	\N	\N	\N	\N	\N	f	0	5662310	0	library internal use	1600	1180	200	8,8,8	integer	3	0	0	\N	2.2	100	\N	\N	f	\N	\N	\N	\N
485	1507	TIFF 6.0	Little Endian (PC)	Uncompressed	1	\N	\N	2	\N	\N	\N	\N	\N	\N	f	0	1876951	0	library internal use	1192	1574	200	8,8,8	integer	3	0	0	\N	2.2	100	\N	\N	f	\N	\N	\N	\N
486	1508	TIFF 6.0	Little Endian (PC)	Uncompressed	1	\N	\N	2	\N	\N	\N	\N	\N	\N	f	0	5693768	0	library internal use	1192	1592	200	8,8,8	integer	3	0	0	\N	2.2	100	\N	\N	f	\N	\N	\N	\N
487	1509	TIFF 6.0	Little Endian (PC)	Uncompressed	1	\N	\N	2	\N	\N	\N	\N	\N	\N	f	0	9479127	0	library internal use	1584	1994	200	8,8,8	integer	3	0	0	\N	2.2	100	\N	\N	f	\N	\N	\N	\N
488	1510	TIFF 6.0	Little Endian (PC)	Uncompressed	1	\N	\N	2	\N	\N	\N	\N	\N	\N	f	0	39111885	0	library internal use	4008	3256	400	8,8,8	integer	3	0	0	\N	2.2	100	\N	\N	f	\N	\N	\N	\N
489	1511	TIFF 6.0	Little Endian (PC)	Uncompressed	1	\N	\N	2	\N	\N	\N	\N	\N	\N	f	0	5746196	0	library internal use	1609	1190	200	8,8,8	integer	3	0	0	\N	2.2	100	\N	\N	f	\N	\N	\N	\N
490	1512	TIFF 6.0	Little Endian (PC)	Uncompressed	1	\N	\N	2	\N	\N	\N	\N	\N	\N	f	0	2715812	0	library internal use	2306	1179	200	8,8,8	integer	3	0	0	\N	2.2	100	\N	\N	f	\N	\N	\N	\N
491	1513	TIFF 6.0	Little Endian (PC)	Uncompressed	1	\N	\N	2	\N	\N	\N	\N	\N	\N	f	0	23488102	0	library internal use	3208	2444	400	8,8,8	integer	3	0	0	\N	2.2	100	\N	\N	f	\N	\N	\N	\N
492	1514	TIFF 6.0	Little Endian (PC)	Uncompressed	1	\N	\N	2	\N	\N	\N	\N	\N	\N	f	0	23488102	0	library internal use	3208	2436	400	8,8,8	integer	3	0	0	\N	2.2	100	\N	\N	f	\N	\N	\N	\N
493	1515	TIFF 6.0	Little Endian (PC)	Uncompressed	1	\N	\N	2	\N	\N	\N	\N	\N	\N	f	0	22754099	0	library internal use	3103	2440	400	8,8,8	integer	3	0	0	\N	2.2	100	\N	\N	f	\N	\N	\N	\N
494	1516	TIFF 6.0	Little Endian (PC)	Uncompressed	1	\N	\N	2	\N	\N	\N	\N	\N	\N	f	0	5284823	0	library internal use	1534	1148	200	8,8,8	integer	3	0	0	\N	2.2	100	\N	\N	f	\N	\N	\N	\N
495	1517	TIFF 6.0	Little Endian (PC)	Uncompressed	1	\N	\N	2	\N	\N	\N	\N	\N	\N	f	0	23592960	0	library internal use	2458	3201	400	8,8,8	integer	3	0	0	\N	2.2	100	\N	\N	f	\N	\N	\N	\N
496	1518	TIFF 6.0	Little Endian (PC)	Uncompressed	1	\N	\N	2	\N	\N	\N	\N	\N	\N	f	0	23278387	0	library internal use	3251	2392	400	8,8,8	integer	3	0	0	\N	2.2	100	\N	\N	f	\N	\N	\N	\N
497	1519	TIFF 6.0	Little Endian (PC)	Uncompressed	1	\N	\N	2	\N	\N	\N	\N	\N	\N	f	0	1887437	0	library internal use	1584	1192	200	8,8,8	integer	3	0	0	\N	2.2	100	\N	\N	f	\N	\N	\N	\N
498	1520	TIFF 6.0	Little Endian (PC)	Uncompressed	1	\N	\N	2	\N	\N	\N	\N	\N	\N	f	0	9542042	0	library internal use	1998	1592	200	8,8,8	integer	3	0	0	\N	2.2	100	\N	\N	f	\N	\N	\N	\N
499	1521	TIFF 6.0	Little Endian (PC)	Uncompressed	1	\N	\N	2	\N	\N	\N	\N	\N	\N	f	0	5641339	0	library internal use	1600	1176	200	8,8,8	integer	3	0	0	\N	2.2	100	\N	\N	f	\N	\N	\N	\N
500	1522	TIFF 6.0	Little Endian (PC)	Uncompressed	1	\N	\N	2	\N	\N	\N	\N	\N	\N	f	0	23802675	0	library internal use	2441	3244	400	8,8,8	integer	3	0	0	\N	2.2	100	\N	\N	f	\N	\N	\N	\N
501	1523	TIFF 6.0	Little Endian (PC)	Uncompressed	1	\N	\N	2	\N	\N	\N	\N	\N	\N	f	0	23697818	0	library internal use	2485	3180	400	8,8,8	integer	3	0	0	\N	2.2	100	\N	\N	f	\N	\N	\N	\N
502	1524	TIFF 6.0	Little Endian (PC)	Uncompressed	1	\N	\N	2	\N	\N	\N	\N	\N	\N	f	0	38587597	0	library internal use	3220	3992	400	8,8,8	integer	3	0	0	\N	2.2	100	\N	\N	f	\N	\N	\N	\N
503	1525	TIFF 6.0	Little Endian (PC)	Uncompressed	1	\N	\N	2	\N	\N	\N	\N	\N	\N	f	0	38587597	0	library internal use	3208	4012	400	8,8,8	integer	3	0	0	\N	2.2	100	\N	\N	f	\N	\N	\N	\N
504	1526	TIFF 6.0	Little Endian (PC)	Uncompressed	1	\N	\N	2	\N	\N	\N	\N	\N	\N	f	0	2181038	0	library internal use	1076	677	200	8,8,8	integer	3	0	0	\N	2.2	100	\N	\N	f	\N	\N	\N	\N
505	1527	TIFF 6.0	Little Endian (PC)	Uncompressed	1	\N	\N	2	\N	\N	\N	\N	\N	\N	f	0	37329306	0	library internal use	3922	3174	400	8,8,8	integer	3	0	0	\N	2.2	100	\N	\N	f	\N	\N	\N	\N
506	1528	TIFF 6.0	Little Endian (PC)	Uncompressed	1	\N	\N	2	\N	\N	\N	\N	\N	\N	f	0	9007268	0	library internal use	1929	1556	200	8,8,8	integer	3	0	0	\N	2.2	100	\N	\N	f	\N	\N	\N	\N
507	1529	TIFF 6.0	Little Endian (PC)	Uncompressed	1	\N	\N	2	\N	\N	\N	\N	\N	\N	f	0	39111885	0	library internal use	4012	3246	400	8,8,8	integer	3	0	0	\N	2.2	100	\N	\N	f	\N	\N	\N	\N
508	1530	TIFF 6.0	Little Endian (PC)	Uncompressed	1	\N	\N	2	\N	\N	\N	\N	\N	\N	f	0	9353298	0	library internal use	1960	1590	200	8,8,8	integer	3	0	0	\N	2.2	100	\N	\N	f	\N	\N	\N	\N
509	1531	TIFF 6.0	Little Endian (PC)	Uncompressed	1	\N	\N	2	\N	\N	\N	\N	\N	\N	f	0	9416212	0	library internal use	1970	1594	200	8,8,8	integer	3	0	0	\N	2.2	100	\N	\N	f	\N	\N	\N	\N
510	1532	TIFF 6.0	Little Endian (PC)	Uncompressed	1	\N	\N	2	\N	\N	\N	\N	\N	\N	f	0	38482739	1	library internal use	3900	3292	400	8,8,8	integer	3	0	7	\N	2.2	100	\N	2006-07-01 00:00:00	f	\N	\N	\N	\N
511	1533	TIFF 6.0	Little Endian (PC)	Uncompressed	1	\N	\N	2	\N	\N	\N	\N	\N	\N	f	0	20342374	1	library internal use	3888	1746	400	8,8,8	integer	3	0	7	\N	2.2	100	\N	2006-07-01 00:00:00	f	\N	\N	\N	\N
512	1534	TIFF 6.0	Little Endian (PC)	Uncompressed	1	\N	\N	2	\N	\N	\N	\N	\N	\N	f	0	39426458	1	library internal use	4000	3316	400	8,8,8	integer	3	0	7	\N	2.2	100	\N	2006-07-01 00:00:00	f	\N	\N	\N	\N
513	1535	TIFF 6.0	Little Endian (PC)	Uncompressed	1	\N	\N	2	\N	\N	\N	\N	\N	\N	f	0	16672358	1	library internal use	2767	2011	400	8,8,8	integer	3	0	7	\N	2.2	100	\N	2006-07-01 00:00:00	f	\N	\N	\N	\N
514	1536	TIFF 6.0	Little Endian (PC)	Uncompressed	1	\N	\N	2	\N	\N	\N	\N	\N	\N	f	0	40789606	1	library internal use	3998	3400	400	8,8,8	integer	3	0	7	\N	2.2	100	\N	2006-07-01 00:00:00	f	\N	\N	\N	\N
515	1537	TIFF 6.0	Little Endian (PC)	Uncompressed	1	\N	\N	2	\N	\N	\N	\N	\N	\N	f	0	39950746	1	library internal use	4000	3328	400	8,8,8	integer	3	0	7	\N	2.2	100	\N	2006-07-01 00:00:00	f	\N	\N	\N	\N
516	1538	TIFF 6.0	Little Endian (PC)	Uncompressed	1	\N	\N	2	\N	\N	\N	\N	\N	\N	f	0	39531315	1	library internal use	3984	3304	400	8,8,8	integer	3	0	7	\N	2.2	100	\N	2006-07-01 00:00:00	f	\N	\N	\N	\N
517	1539	TIFF 6.0	Little Endian (PC)	Uncompressed	1	\N	\N	2	\N	\N	\N	\N	\N	\N	f	0	39741030	1	library internal use	3976	3328	400	8,8,8	integer	3	0	7	\N	2.2	100	\N	2006-07-01 00:00:00	f	\N	\N	\N	\N
518	1540	TIFF 6.0	Little Endian (PC)	Uncompressed	1	\N	\N	2	\N	\N	\N	\N	\N	\N	f	0	40684749	1	library internal use	4015	3376	400	8,8,8	integer	3	0	7	\N	2.2	100	\N	2006-07-01 00:00:00	f	\N	\N	\N	\N
519	1541	TIFF 6.0	Little Endian (PC)	Uncompressed	1	\N	\N	2	\N	\N	\N	\N	\N	\N	f	0	41733325	1	library internal use	4000	3480	400	8,8,8	integer	3	0	7	\N	2.2	100	\N	2006-07-01 00:00:00	f	\N	\N	\N	\N
520	1542	TIFF 6.0	Little Endian (PC)	Uncompressed	1	\N	\N	2	\N	\N	\N	\N	\N	\N	f	0	40999322	1	library internal use	3992	3421	400	8,8,8	integer	3	0	7	\N	2.2	100	\N	2006-07-01 00:00:00	f	\N	\N	\N	\N
521	1543	TIFF 6.0	Little Endian (PC)	Uncompressed	1	\N	\N	2	\N	\N	\N	\N	\N	\N	f	0	10695475	1	library internal use	2284	1558	400	8,8,8	integer	3	0	7	\N	2.2	100	\N	2006-07-01 00:00:00	f	\N	\N	\N	\N
522	1544	TIFF 6.0	Little Endian (PC)	Uncompressed	1	\N	\N	2	\N	\N	\N	\N	\N	\N	f	0	40789606	1	library internal use	4000	3400	400	8,8,8	integer	3	0	7	\N	2.2	100	\N	2006-07-01 00:00:00	f	\N	\N	\N	\N
523	1545	TIFF 6.0	Little Endian (PC)	Uncompressed	1	\N	\N	2	\N	\N	\N	\N	\N	\N	f	0	10055844	1	library internal use	1367	2452	400	8,8,8	integer	3	0	7	\N	2.2	100	\N	2006-07-01 00:00:00	f	\N	\N	\N	\N
524	1546	TIFF 6.0	Little Endian (PC)	Uncompressed	1	\N	\N	2	\N	\N	\N	\N	\N	\N	f	0	35651584	1	library internal use	2837	4194	400	8,8,8	integer	3	0	7	\N	2.2	100	\N	2006-07-01 00:00:00	f	\N	\N	\N	\N
525	1547	TIFF 6.0	Little Endian (PC)	Uncompressed	1	\N	\N	2	\N	\N	\N	\N	\N	\N	f	0	31771853	1	library internal use	2825	3751	400	8,8,8	integer	3	0	7	\N	2.2	100	\N	2006-07-01 00:00:00	f	\N	\N	\N	\N
526	1548	TIFF 6.0	Little Endian (PC)	Uncompressed	1	\N	\N	2	\N	\N	\N	\N	\N	\N	f	0	8923382	1	library internal use	1341	2219	400	8,8,8	integer	3	0	7	\N	2.2	100	\N	2006-07-01 00:00:00	f	\N	\N	\N	\N
527	1549	TIFF 6.0	Little Endian (PC)	Uncompressed	1	\N	\N	2	\N	\N	\N	\N	\N	\N	f	0	9258926	1	library internal use	1161	2658	400	8,8,8	integer	3	0	7	\N	2.2	100	\N	\N	f	\N	\N	\N	\N
528	1550	TIFF 6.0	Little Endian (PC)	Uncompressed	1	\N	\N	2	\N	\N	\N	\N	\N	\N	f	0	33659290	1	library internal use	2538	4421	400	8,8,8	integer	3	0	7	\N	2.2	100	\N	\N	f	\N	\N	\N	\N
529	1551	TIFF 6.0	Little Endian (PC)	Uncompressed	1	\N	\N	2	\N	\N	\N	\N	\N	\N	f	0	17406362	1	library internal use	1963	2949	400	8,8,8	integer	3	0	7	\N	2.2	100	\N	\N	f	\N	\N	\N	\N
530	1552	TIFF 6.0	Little Endian (PC)	Uncompressed	1	\N	\N	2	\N	\N	\N	\N	\N	\N	f	0	39426456	0	library internal use	3196	4110	400	8,8,8	integer	3	0	7	\N	2.2	100	\N	\N	f	\N	\N	\N	\N
531	1553	TIFF 6.0	Little Endian (PC)	Uncompressed	1	\N	\N	2	\N	\N	\N	\N	\N	\N	f	0	7906263	0	library internal use	1394	1891	400	8,8,8	integer	3	0	7	\N	2.2	100	\N	\N	f	\N	\N	\N	\N
532	1554	TIFF 6.0	Little Endian (PC)	Uncompressed	1	\N	\N	2	\N	\N	\N	\N	\N	\N	f	0	31771853	1	library internal use	2719	3898	400	8,8,8	integer	3	0	7	\N	2.2	100	\N	\N	f	\N	\N	\N	\N
533	1555	TIFF 6.0	Little Endian (PC)	Uncompressed	1	\N	\N	2	\N	\N	\N	\N	\N	\N	f	0	41628467	0	library internal use	3178	4368	400	8,8,8	integer	3	0	7	\N	2.2	100	\N	\N	f	\N	\N	\N	\N
534	1556	TIFF 6.0	Little Endian (PC)	Uncompressed	1	\N	\N	2	\N	\N	\N	\N	\N	\N	f	0	39007027	0	library internal use	3190	4072	400	8,8,8	integer	3	0	7	\N	2.2	100	\N	\N	f	\N	\N	\N	\N
535	1557	TIFF 6.0	Little Endian (PC)	Uncompressed	1	\N	\N	2	\N	\N	\N	\N	\N	\N	f	0	40265318	0	library internal use	3266	4106	400	8,8,8	integer	3	0	7	\N	2.2	100	\N	\N	f	\N	\N	\N	\N
536	1558	TIFF 6.0	Little Endian (PC)	Uncompressed	1	\N	\N	2	\N	\N	\N	\N	\N	\N	f	0	6543114	0	library internal use	1171	1862	400	8,8,8	integer	3	0	7	\N	2.2	100	\N	\N	f	\N	\N	\N	\N
537	1559	TIFF 6.0	Little Endian (PC)	Uncompressed	1	\N	\N	2	\N	\N	\N	\N	\N	\N	f	0	40684749	0	library internal use	3233	4195	400	8,8,8	integer	3	0	7	\N	2.2	100	\N	\N	f	\N	\N	\N	\N
538	1560	TIFF 6.0	Little Endian (PC)	Uncompressed	1	\N	\N	2	\N	\N	\N	\N	\N	\N	f	0	40265318	0	library internal use	3964	3390	400	8,8,8	integer	3	0	7	\N	2.2	100	\N	\N	f	\N	\N	\N	\N
539	1561	TIFF 6.0	Little Endian (PC)	Uncompressed	1	\N	\N	2	\N	\N	\N	\N	\N	\N	f	0	32296141	0	library internal use	2560	4200	400	8,8,8	integer	3	0	0	\N	2.2	100	\N	\N	f	\N	\N	\N	\N
540	1562	TIFF 6.0	Little Endian (PC)	Uncompressed	1	\N	\N	2	\N	\N	\N	\N	\N	\N	f	0	27158118	0	library internal use	2378	0	400	8,8,8	integer	3	0	0	\N	2.2	3800	\N	\N	f	\N	\N	\N	\N
541	1563	TIFF 6.0	Little Endian (PC)	Uncompressed	1	\N	\N	2	\N	\N	\N	\N	\N	\N	f	0	36280730	0	library internal use	2856	4240	400	8,8,8	integer	3	0	0	\N	2.2	100	\N	\N	f	\N	\N	\N	\N
542	1564	TIFF 6.0	Little Endian (PC)	Uncompressed	1	\N	\N	2	\N	\N	\N	\N	\N	\N	f	0	27577549	0	library internal use	2416	3800	400	8,8,8	integer	3	0	0	\N	2.2	100	\N	\N	f	\N	\N	\N	\N
543	1565	TIFF 6.0	Little Endian (PC)	Uncompressed	1	\N	\N	2	\N	\N	\N	\N	\N	\N	f	0	73505178	0	library internal use	4185	5855	400	8,8,8	integer	3	0	0	\N	2.2	100	\N	\N	f	\N	\N	\N	\N
544	1566	TIFF 6.0	Little Endian (PC)	Uncompressed	1	\N	\N	2	\N	\N	\N	\N	\N	\N	f	0	27472691	0	library internal use	2432	3760	400	8,8,8	integer	3	0	0	\N	2.2	100	\N	\N	f	\N	\N	\N	\N
545	1567	TIFF 6.0	Little Endian (PC)	Uncompressed	1	\N	\N	2	\N	\N	\N	\N	\N	\N	f	0	9384755	0	library internal use	1976	1584	200	8,8,8	integer	3	0	0	\N	2.2	100	\N	\N	f	\N	\N	\N	\N
546	1568	TIFF 6.0	Little Endian (PC)	Uncompressed	1	\N	\N	2	\N	\N	\N	\N	\N	\N	f	0	5882511	0	library internal use	1655	1184	200	8,8,8	integer	3	0	0	\N	2.2	100	\N	\N	f	\N	\N	\N	\N
547	1569	TIFF 6.0	Little Endian (PC)	Uncompressed	1	\N	\N	2	\N	\N	\N	\N	\N	\N	f	0	9342812	0	library internal use	1600	1946	200	8,8,8	integer	3	0	0	\N	2.2	100	\N	\N	f	\N	\N	\N	\N
548	1570	TIFF 6.0	Little Endian (PC)	Uncompressed	1	\N	\N	2	\N	\N	\N	\N	\N	\N	f	0	40265318	0	library internal use	4128	3252	400	8,8,8	integer	3	0	0	\N	2.2	100	\N	\N	f	\N	\N	\N	\N
549	1571	TIFF 6.0	Little Endian (PC)	Uncompressed	1	\N	\N	2	\N	\N	\N	\N	\N	\N	f	0	39216742	0	library internal use	4004	3261	400	8,8,8	integer	3	0	0	\N	2.2	100	\N	\N	f	\N	\N	\N	\N
550	1572	TIFF 6.0	Little Endian (PC)	Uncompressed	1	\N	\N	2	\N	\N	\N	\N	\N	\N	f	0	9332326	0	library internal use	1584	1964	200	8,8,8	integer	3	0	0	\N	2.2	100	\N	\N	f	\N	\N	\N	\N
551	1573	TIFF 6.0	Little Endian (PC)	Uncompressed	1	\N	\N	2	\N	\N	\N	\N	\N	\N	f	0	10695475	0	library internal use	1611	2212	200	8,8,8	integer	3	0	0	\N	2.2	100	\N	\N	f	\N	\N	\N	\N
552	1574	TIFF 6.0	Little Endian (PC)	Uncompressed	1	\N	\N	2	\N	\N	\N	\N	\N	\N	f	0	13212058	0	library internal use	2202	1996	400	8,8,8	integer	3	0	0	\N	2.2	100	\N	\N	f	\N	\N	\N	\N
553	1575	TIFF 6.0	Little Endian (PC)	Uncompressed	1	\N	\N	2	\N	\N	\N	\N	\N	\N	f	0	9594470	0	library internal use	1594	2006	400	8,8,8	integer	3	0	0	\N	2.2	100	\N	\N	f	\N	\N	\N	\N
554	1576	TIFF 6.0	Little Endian (PC)	Uncompressed	1	\N	\N	2	\N	\N	\N	\N	\N	\N	f	0	9154068	0	library internal use	1400	2180	200	8,8,8	integer	3	0	0	\N	2.2	100	\N	\N	f	\N	\N	\N	\N
555	1577	TIFF 6.0	Little Endian (PC)	Uncompressed	1	\N	\N	2	\N	\N	\N	\N	\N	\N	f	0	9384755	0	library internal use	1550	2018	200	8,8,8	integer	3	0	0	\N	2.2	100	\N	\N	f	\N	\N	\N	\N
556	1578	TIFF 6.0	Little Endian (PC)	Uncompressed	1	\N	\N	2	\N	\N	\N	\N	\N	\N	f	0	6385828	0	library internal use	1680	1268	200	8,8,8	integer	3	0	0	\N	2.2	100	\N	\N	f	\N	\N	\N	\N
557	1579	TIFF 6.0	Little Endian (PC)	Uncompressed	1	\N	\N	2	\N	\N	\N	\N	\N	\N	f	0	23907533	0	library internal use	3260	2444	400	8,8,8	integer	3	0	0	\N	2.2	100	\N	\N	f	\N	\N	\N	\N
558	1580	TIFF 6.0	Little Endian (PC)	Uncompressed	1	\N	\N	2	\N	\N	\N	\N	\N	\N	f	0	9384755	0	library internal use	1584	1974	200	8,8,8	integer	3	0	0	\N	2.2	100	\N	\N	f	\N	\N	\N	\N
559	1581	TIFF 6.0	Little Endian (PC)	Uncompressed	1	\N	\N	2	\N	\N	\N	\N	\N	\N	f	0	6941573	0	library internal use	1509	1534	200	8,8,8	integer	3	0	0	\N	2.2	100	\N	\N	f	\N	\N	\N	\N
560	1582	TIFF 6.0	Little Endian (PC)	Uncompressed	1	\N	\N	2	\N	\N	\N	\N	\N	\N	f	0	2097152	0	library internal use	742	942	200	8,8,8	integer	3	0	0	\N	2.2	100	\N	\N	f	\N	\N	\N	\N
561	1583	TIFF 6.0	Little Endian (PC)	Uncompressed	1	\N	\N	2	\N	\N	\N	\N	\N	\N	f	0	2852127	0	library internal use	1192	798	200	8,8,8	integer	3	0	0	\N	2.2	100	\N	\N	f	\N	\N	\N	\N
562	1584	TIFF 6.0	Little Endian (PC)	Uncompressed	1	\N	\N	2	\N	\N	\N	\N	\N	\N	f	0	6102712	0	library internal use	1034	1968	200	8,8,8	integer	3	0	0	\N	2.2	100	\N	\N	f	\N	\N	\N	\N
563	1585	TIFF 6.0	Little Endian (PC)	Uncompressed	1	\N	\N	2	\N	\N	\N	\N	\N	\N	f	0	2862612	0	library internal use	1963	1458	200	8,8,8	integer	3	0	0	\N	2.2	100	\N	\N	f	\N	\N	\N	\N
564	1586	TIFF 6.0	Little Endian (PC)	Uncompressed	1	\N	\N	2	\N	\N	\N	\N	\N	\N	f	0	8860467	0	library internal use	1535	1924	200	8,8,8	integer	3	0	0	\N	2.2	100	\N	\N	f	\N	\N	\N	\N
565	1587	TIFF 6.0	Little Endian (PC)	Uncompressed	1	\N	\N	2	\N	\N	\N	\N	\N	\N	f	0	9384755	0	library internal use	1600	1956	200	8,8,8	integer	3	0	0	\N	2.2	100	\N	\N	f	\N	\N	\N	\N
566	1588	TIFF 6.0	Little Endian (PC)	Uncompressed	1	\N	\N	2	\N	\N	\N	\N	\N	\N	f	0	9353298	0	library internal use	1584	1968	200	8,8,8	integer	3	0	0	\N	2.2	100	\N	\N	f	\N	\N	\N	\N
567	1589	TIFF 6.0	Little Endian (PC)	Uncompressed	1	\N	\N	2	\N	\N	\N	\N	\N	\N	f	0	9846129	0	library internal use	1608	2040	200	8,8,8	integer	3	0	0	\N	2.2	100	\N	\N	f	\N	\N	\N	\N
568	1590	TIFF 6.0	Little Endian (PC)	Uncompressed	1	\N	\N	2	\N	\N	\N	\N	\N	\N	f	0	9636413	0	library internal use	1600	2007	200	8,8,8	integer	3	0	0	\N	2.2	100	\N	\N	f	\N	\N	\N	\N
569	1591	TIFF 6.0	Little Endian (PC)	Uncompressed	1	\N	\N	2	\N	\N	\N	\N	\N	\N	f	0	9573499	0	library internal use	1981	1611	200	8,8,8	integer	3	0	0	\N	2.2	100	\N	\N	f	\N	\N	\N	\N
571	1594	TIFF 6.0	Little Endian (PC)	Uncompressed	1	\N	\N	2	\N	\N	\N	\N	\N	\N	f	0	178257920	0	library internal use	10605	5603	400	8,8,8	integer	3	0	0	\N	2.2	100	\N	\N	f	\N	\N	\N	\N
572	1595	TIFF 6.0	Little Endian (PC)	Uncompressed	1	\N	\N	2	\N	\N	\N	\N	\N	\N	f	0	16252928	0	library internal use	2265	2398	400	8,8,8	integer	3	0	0	\N	2.2	100	\N	\N	f	\N	\N	\N	\N
573	1596	TIFF 6.0	Little Endian (PC)	Uncompressed	1	\N	\N	2	\N	\N	\N	\N	\N	\N	f	0	64801997	0	library internal use	5411	3990	400	8,8,8	integer	3	0	0	\N	2.2	100	\N	\N	f	\N	\N	\N	\N
574	1597	TIFF 6.0	Little Endian (PC)	Uncompressed	1	\N	\N	2	\N	\N	\N	\N	\N	\N	f	0	63648563	0	library internal use	4417	4804	400	8,8,8	integer	3	0	0	\N	2.2	100	\N	\N	f	\N	\N	\N	\N
575	1598	TIFF 6.0	Little Endian (PC)	Uncompressed	1	\N	\N	2	\N	\N	\N	\N	\N	\N	f	0	65221427	0	library internal use	3873	5615	400	8,8,8	integer	3	0	0	\N	2.2	100	\N	\N	f	\N	\N	\N	\N
576	1599	TIFF 6.0	Little Endian (PC)	Uncompressed	1	\N	\N	2	\N	\N	\N	\N	\N	\N	f	0	65431142	1	library internal use	3898	5596	400	8,8,8	integer	3	0	1	\N	2.2	100	\N	\N	f	\N	\N	\N	\N
577	1600	TIFF 6.0	Little Endian (PC)	Uncompressed	1	\N	\N	2	\N	\N	\N	\N	\N	\N	f	0	38482739	0	library internal use	2719	4723	400	8,8,8	integer	3	0	0	\N	2.2	100	\N	\N	f	\N	\N	\N	\N
578	1601	TIFF 6.0	Little Endian (PC)	Uncompressed	1	\N	\N	2	\N	\N	\N	\N	\N	\N	f	0	43096474	0	library internal use	3017	4802	400	8,8,8	integer	3	0	0	\N	2.2	100	\N	\N	f	\N	\N	\N	\N
579	1602	TIFF 6.0	Little Endian (PC)	Uncompressed	1	\N	\N	2	\N	\N	\N	\N	\N	\N	f	0	9762243	0	library internal use	2028	1605	200	8,8,8	integer	3	0	0	\N	2.2	100	\N	\N	f	\N	\N	\N	\N
580	1603	TIFF 6.0	Little Endian (PC)	Uncompressed	1	\N	\N	2	\N	\N	\N	\N	\N	\N	f	0	9405727	0	library internal use	1976	1587	200	8,8,8	integer	3	0	0	\N	2.2	100	\N	\N	f	\N	\N	\N	\N
581	1604	TIFF 6.0	Little Endian (PC)	Uncompressed	1	\N	\N	2	\N	\N	\N	\N	\N	\N	f	0	9552527	0	library internal use	1592	2000	200	8,8,8	integer	3	0	0	\N	2.2	100	\N	\N	f	\N	\N	\N	\N
582	1605	TIFF 6.0	Little Endian (PC)	Uncompressed	1	\N	\N	2	\N	\N	\N	\N	\N	\N	f	0	9563013	0	library internal use	1592	2002	200	8,8,8	integer	3	0	0	\N	2.2	100	\N	\N	f	\N	\N	\N	\N
583	1606	TIFF 6.0	Little Endian (PC)	Uncompressed	1	\N	\N	2	\N	\N	\N	\N	\N	\N	f	0	9447670	0	library internal use	1975	1594	200	8,8,8	integer	3	0	0	\N	2.2	100	\N	\N	f	\N	\N	\N	\N
584	1607	TIFF 6.0	Little Endian (PC)	Uncompressed	1	\N	\N	2	\N	\N	\N	\N	\N	\N	f	0	4697620	0	library internal use	1590	984	200	8,8,8	integer	3	0	0	\N	2.2	100	\N	\N	f	\N	\N	\N	\N
585	1608	TIFF 6.0	Little Endian (PC)	Uncompressed	1	\N	\N	2	\N	\N	\N	\N	\N	\N	f	0	9154068	0	library internal use	1544	1976	400	8,8,8	integer	3	0	0	\N	2.2	100	\N	\N	f	\N	\N	\N	\N
586	1609	TIFF 6.0	Little Endian (PC)	Uncompressed	1	\N	\N	2	\N	\N	\N	\N	\N	\N	f	0	2181038	0	library internal use	745	978	200	8,8,8	integer	3	0	0	\N	2.2	100	\N	\N	f	\N	\N	\N	\N
587	1610	TIFF 6.0	Little Endian (PC)	Uncompressed	1	\N	\N	2	\N	\N	\N	\N	\N	\N	f	0	2086666	0	library internal use	742	938	200	8,8,8	integer	3	0	0	\N	2.2	100	\N	\N	f	\N	\N	\N	\N
588	1611	TIFF 6.0	Little Endian (PC)	Uncompressed	1	\N	\N	2	\N	\N	\N	\N	\N	\N	f	0	11754537	1	patron request	2005	1955	400	8,8,8	integer	3	0	7	\N	2.2	142	\N	2006-07-17 00:00:00	f	\N	\N	digital masters/HughesGerald854	\N
589	1614	TIFF 6.0	Little Endian (PC)	Uncompressed	1	\N	\N	2	\N	\N	\N	\N	\N	\N	f	0	11859395	1	patron request	1995	1982	400	8,8,8	integer	3	0	1	\N	2.2	143	\N	2006-07-18 00:00:00	f	\N	\N	\N	\N
590	1615	TIFF 6.0	Little Endian (PC)	Uncompressed	1	\N	\N	2	\N	\N	\N	\N	\N	\N	f	0	11775508	1	patron request	1995	1969	400	8,8,8	integer	3	0	1	\N	2.2	143	\N	2006-07-18 00:00:00	f	\N	\N	\N	\N
591	1616	TIFF 6.0	Little Endian (PC)	Uncompressed	1	\N	\N	2	\N	\N	\N	\N	\N	\N	f	0	11775508	1	library internal use	1995	1969	400	8,8,8	integer	3	0	1	\N	2.2	143	\N	2006-07-18 00:00:00	f	\N	\N	\N	\N
592	1617	TIFF 6.0	Little Endian (PC)	Uncompressed	1	\N	\N	2	\N	\N	\N	\N	\N	\N	f	0	1835008	0	library internal use	608	1006	200	8,8,8	integer	3	0	0	\N	2.2	100	\N	\N	f	\N	\N	\N	\N
593	1618	TIFF 6.0	Little Endian (PC)	Uncompressed	1	\N	\N	2	\N	\N	\N	\N	\N	\N	f	0	2285896	0	library internal use	1003	758	200	8,8,8	integer	3	0	0	\N	2.2	100	\N	\N	f	\N	\N	\N	\N
594	1619	TIFF 6.0	Little Endian (PC)	Uncompressed	1	\N	\N	2	\N	\N	\N	\N	\N	\N	f	0	11429478	0	library internal use	1997	1900	400	8,8,8	integer	3	0	0	\N	2.2	100	\N	\N	f	\N	\N	\N	\N
595	1620	TIFF 6.0	Little Endian (PC)	Uncompressed	1	\N	\N	2	\N	\N	\N	\N	\N	\N	f	0	9332326	0	library internal use	1584	1964	200	8,8,8	integer	3	0	0	\N	2.2	100	\N	\N	f	\N	\N	\N	\N
596	1621	TIFF 6.0	Little Endian (PC)	Uncompressed	1	\N	\N	2	\N	\N	\N	\N	\N	\N	f	0	9405727	0	library internal use	1970	1592	200	8,8,8	integer	3	0	0	\N	2.2	100	\N	\N	f	\N	\N	\N	\N
597	1622	TIFF 6.0	Little Endian (PC)	Uncompressed	1	\N	\N	2	\N	\N	\N	\N	\N	\N	f	0	9657385	0	library internal use	1622	1984	200	8,8,8	integer	3	0	0	\N	2.2	100	\N	\N	f	\N	\N	\N	\N
598	1623	TIFF 6.0	Little Endian (PC)	Uncompressed	1	\N	\N	2	\N	\N	\N	\N	\N	\N	f	0	4110418	0	library internal use	1397	980	200	8,8,8	integer	3	0	0	\N	2.2	100	\N	\N	f	\N	\N	\N	\N
599	1624	TIFF 6.0	Little Endian (PC)	Uncompressed	1	\N	\N	2	\N	\N	\N	\N	\N	\N	f	0	9583985	0	library internal use	1976	1616	200	8,8,8	integer	3	0	0	\N	2.2	100	\N	\N	f	\N	\N	\N	\N
600	1625	TIFF 6.0	Little Endian (PC)	Uncompressed	1	\N	\N	2	\N	\N	\N	\N	\N	\N	f	0	1226834	0	library internal use	1294	952	200	8,8,8	integer	3	0	0	\N	2.2	100	\N	\N	f	\N	\N	\N	\N
601	1626	TIFF 6.0	Little Endian (PC)	Uncompressed	1	\N	\N	2	\N	\N	\N	\N	\N	\N	f	0	2663383	0	library internal use	1161	765	200	8,8,8	integer	3	0	0	\N	2.2	100	\N	\N	f	\N	\N	\N	\N
602	1627	TIFF 6.0	Little Endian (PC)	Uncompressed	1	\N	\N	2	\N	\N	\N	\N	\N	\N	f	0	4173332	0	library internal use	1417	982	200	8,8,8	integer	3	0	0	\N	2.2	100	\N	\N	f	\N	\N	\N	\N
603	1628	TIFF 6.0	Little Endian (PC)	Uncompressed	1	\N	\N	2	\N	\N	\N	\N	\N	\N	f	0	3166700	0	library internal use	1973	1605	200	8,8,8	integer	3	0	0	\N	2.2	100	\N	\N	f	\N	\N	\N	\N
604	1629	TIFF 6.0	Little Endian (PC)	Uncompressed	1	\N	\N	2	\N	\N	\N	\N	\N	\N	f	0	3082813	0	library internal use	1576	1958	200	8,8,8	integer	3	0	0	\N	2.2	100	\N	\N	f	\N	\N	\N	\N
605	1630	TIFF 6.0	Little Endian (PC)	Uncompressed	1	\N	\N	2	\N	\N	\N	\N	\N	\N	f	0	3219128	0	library internal use	2000	1611	200	8,8,8	integer	3	0	0	\N	2.2	100	\N	\N	f	\N	\N	\N	\N
606	1631	TIFF 6.0	Little Endian (PC)	Uncompressed	1	\N	\N	2	\N	\N	\N	\N	\N	\N	f	0	3166700	0	library internal use	1964	1614	200	8,8,8	integer	3	0	0	\N	2.2	100	\N	\N	f	\N	\N	\N	\N
607	1632	TIFF 6.0	Little Endian (PC)	Uncompressed	1	\N	\N	2	\N	\N	\N	\N	\N	\N	f	0	9332326	0	library internal use	1965	1583	200	8,8,8	integer	3	0	0	\N	2.2	100	\N	\N	f	\N	\N	\N	\N
608	1633	TIFF 6.0	Little Endian (PC)	Uncompressed	1	\N	\N	2	\N	\N	\N	\N	\N	\N	f	0	4886364	0	library internal use	1399	1164	200	8,8,8	integer	3	0	0	\N	2.2	100	\N	\N	f	\N	\N	\N	\N
609	1634	TIFF 6.0	Little Endian (PC)	Uncompressed	1	\N	\N	2	\N	\N	\N	\N	\N	\N	f	0	606618	0	library internal use	900	674	200	8,8,8	integer	3	0	0	\N	2.2	100	\N	\N	f	\N	\N	\N	\N
610	1635	TIFF 6.0	Little Endian (PC)	Uncompressed	1	\N	\N	2	\N	\N	\N	\N	\N	\N	f	0	1845494	0	library internal use	896	687	200	8,8,8	integer	3	0	0	\N	2.2	100	\N	\N	f	\N	\N	\N	\N
611	1636	TIFF 6.0	Little Endian (PC)	Uncompressed	1	\N	\N	2	\N	\N	\N	\N	\N	\N	f	0	38692454	0	library internal use	4018	3209	400	8,8,8	integer	3	0	0	\N	2.2	100	\N	\N	f	\N	\N	\N	\N
612	1637	TIFF 6.0	Little Endian (PC)	Uncompressed	1	\N	\N	2	\N	\N	\N	\N	\N	\N	f	0	4917821	0	library internal use	1292	1270	200	8,8,8	integer	3	0	0	\N	2.2	100	\N	\N	f	\N	\N	\N	\N
613	1638	TIFF 6.0	Little Endian (PC)	Uncompressed	1	\N	\N	2	\N	\N	\N	\N	\N	\N	f	0	3166700	0	library internal use	1962	1616	200	8,8,8	integer	3	0	0	\N	2.2	100	\N	\N	f	\N	\N	\N	\N
614	1639	TIFF 6.0	Little Endian (PC)	Uncompressed	1	\N	\N	2	\N	\N	\N	\N	\N	\N	f	0	38587597	0	library internal use	3235	3972	400	8,8,8	integer	3	0	0	\N	2.2	100	\N	\N	f	\N	\N	\N	\N
615	1640	TIFF 6.0	Little Endian (PC)	Uncompressed	1	\N	\N	2	\N	\N	\N	\N	\N	\N	f	0	9342812	0	library internal use	1584	1966	200	8,8,8	integer	3	0	0	\N	2.2	100	\N	\N	f	\N	\N	\N	\N
616	1641	TIFF 6.0	Little Endian (PC)	Uncompressed	1	\N	\N	2	\N	\N	\N	\N	\N	\N	f	0	3177185	0	library internal use	1980	1605	200	8,8,8	integer	3	0	0	\N	2.2	100	\N	\N	f	\N	\N	\N	\N
617	1642	TIFF 6.0	Little Endian (PC)	Uncompressed	1	\N	\N	2	\N	\N	\N	\N	\N	\N	f	0	9321841	0	library internal use	1592	1952	200	8,8,8	integer	3	0	0	\N	2.2	100	\N	\N	f	\N	\N	\N	\N
618	1643	TIFF 6.0	Little Endian (PC)	Uncompressed	1	\N	\N	2	\N	\N	\N	\N	\N	\N	f	0	2076180	0	library internal use	1009	685	200	8,8,8	integer	3	0	0	\N	2.2	100	\N	\N	f	\N	\N	\N	\N
619	1644	TIFF 6.0	Little Endian (PC)	Uncompressed	1	\N	\N	2	\N	\N	\N	\N	\N	\N	f	0	17616077	0	library internal use	2806	2096	400	8,8,8	integer	3	0	0	\N	2.2	100	\N	\N	f	\N	\N	\N	\N
620	1645	TIFF 6.0	Little Endian (PC)	Uncompressed	1	\N	\N	2	\N	\N	\N	\N	\N	\N	f	0	11429478	0	library internal use	1948	1959	400	8,8,8	integer	3	0	0	\N	2.2	100	\N	\N	f	\N	\N	\N	\N
621	1646	TIFF 6.0	Little Endian (PC)	Uncompressed	1	\N	\N	2	\N	\N	\N	\N	\N	\N	f	0	40370176	0	library internal use	4131	3261	400	8,8,8	integer	3	0	0	\N	2.2	100	\N	\N	f	\N	\N	\N	\N
622	1647	TIFF 6.0	Little Endian (PC)	Uncompressed	1	\N	\N	2	\N	\N	\N	\N	\N	\N	f	0	44983910	1	library internal use	3228	4640	400	8,8,8	integer	3	0	7	\N	2.2	100	\N	\N	f	\N	\N	\N	\N
623	1648	TIFF 6.0	Little Endian (PC)	Uncompressed	1	\N	\N	2	\N	\N	\N	\N	\N	\N	f	0	27367834	1	library internal use	2397	3800	400	8,8,8	integer	3	0	7	\N	2.2	100	\N	\N	f	\N	\N	\N	\N
624	1649	TIFF 6.0	Little Endian (PC)	Uncompressed	1	\N	\N	2	\N	\N	\N	\N	\N	\N	f	0	34183578	1	library internal use	2942	3872	400	8,8,8	integer	3	0	7	\N	2.2	100	\N	\N	f	\N	\N	\N	\N
625	1650	TIFF 6.0	Little Endian (PC)	Uncompressed	1	\N	\N	2	\N	\N	\N	\N	\N	\N	f	0	35022438	1	library internal use	3626	3216	400	8,8,8	integer	3	0	7	The image was cropped from the left to remove the torn section.	2.2	100	\N	\N	f	\N	\N	\N	\N
626	1652	TIFF 6.0	Little Endian (PC)	Uncompressed	1	\N	\N	2	\N	\N	\N	\N	\N	\N	f	0	12268339	1	library internal use	1151	3538	400	8,8,8	integer	3	0	7	\N	2.2	100	\N	\N	f	\N	\N	\N	\N
627	1653	TIFF 6.0	Little Endian (PC)	Uncompressed	1	\N	\N	2	\N	\N	\N	\N	\N	\N	f	0	12582912	1	library internal use	2528	1665	400	8,8,8	integer	3	0	7	\N	2.2	100	\N	\N	f	\N	\N	\N	\N
628	1654	TIFF 6.0	Little Endian (PC)	Uncompressed	1	\N	\N	2	\N	\N	\N	\N	\N	\N	f	0	2789212	1	library internal use	1046	889	400	8,8,8	integer	3	0	7	\N	2.2	100	No information on bottom of picture	\N	f	\N	\N	\N	\N
629	1655	TIFF 6.0	Little Endian (PC)	Uncompressed	1	\N	\N	2	\N	\N	\N	\N	\N	\N	f	0	30932992	1	library internal use	2825	3652	400	8,8,8	integer	3	0	7	\N	2.2	100	\N	\N	f	\N	\N	\N	\N
630	1656	TIFF 6.0	Little Endian (PC)	Uncompressed	1	\N	\N	2	\N	\N	\N	\N	\N	\N	f	0	23488102	1	library internal use	2424	3233	400	8,8,8	integer	3	0	7	\N	2.2	100	\N	\N	f	\N	\N	\N	\N
631	1657	TIFF 6.0	Little Endian (PC)	Uncompressed	1	\N	\N	2	\N	\N	\N	\N	\N	\N	f	0	26738688	1	library internal use	2954	3016	400	8,8,8	integer	3	0	7	\N	2.2	100	No information on bottom of picture	\N	f	\N	\N	\N	\N
632	1658	TIFF 6.0	Little Endian (PC)	Uncompressed	1	\N	\N	2	\N	\N	\N	\N	\N	\N	f	0	23068672	1	library internal use	3050	2519	400	8,8,8	integer	3	0	7	\N	2.2	100	\N	\N	f	\N	\N	\N	\N
633	1659	TIFF 6.0	Little Endian (PC)	Uncompressed	1	\N	\N	2	\N	\N	\N	\N	\N	\N	f	0	32820429	1	library internal use	2415	4523	400	8,8,8	integer	3	0	7	\N	2.2	100	No information on bottom of picture	\N	f	\N	\N	\N	\N
634	1660	TIFF 6.0	Little Endian (PC)	Uncompressed	1	\N	\N	2	\N	\N	\N	\N	\N	\N	f	0	10349445	0	library internal use	872	3957	400	8,8,8	integer	3	0	0	\N	2.2	100	No information on bottom of picture	\N	f	\N	\N	\N	\N
635	1661	TIFF 6.0	Little Endian (PC)	Uncompressed	1	\N	\N	2	\N	\N	\N	\N	\N	\N	f	0	2967470	1	library internal use	1003	985	400	8,8,8	integer	3	0	7	\N	2.2	100	\N	\N	f	\N	\N	\N	\N
636	1662	TIFF 6.0	Little Endian (PC)	Uncompressed	1	\N	\N	2	\N	\N	\N	\N	\N	\N	f	0	31981568	1	library internal use	3756	2842	400	8,8,8	integer	3	0	7	\N	2.2	100	No information on bottom of picture	\N	f	\N	\N	\N	\N
637	1663	TIFF 6.0	Little Endian (PC)	Uncompressed	1	\N	\N	2	\N	\N	\N	\N	\N	\N	f	0	30723277	1	library internal use	3992	2563	400	8,8,8	integer	3	0	7	\N	2.2	100	\N	\N	f	\N	\N	\N	\N
638	1664	TIFF 6.0	Little Endian (PC)	Uncompressed	1	\N	\N	2	\N	\N	\N	\N	\N	\N	f	0	38692454	1	library internal use	3104	4160	400	8,8,8	integer	3	0	7	\N	2.2	100	\N	\N	f	\N	\N	\N	\N
639	1665	TIFF 6.0	Little Endian (PC)	Uncompressed	1	\N	\N	2	\N	\N	\N	\N	\N	\N	f	0	16986931	1	library internal use	2040	2771	400	8,8,8	integer	3	0	7	\N	2.2	100	\N	\N	f	\N	\N	\N	\N
640	1666	TIFF 6.0	Little Endian (PC)	Uncompressed	1	\N	\N	2	\N	\N	\N	\N	\N	\N	f	0	39216742	1	library internal use	3261	4009	400	8,8,8	integer	3	0	7	\N	2.2	100	\N	\N	f	\N	\N	\N	\N
641	1667	TIFF 6.0	Little Endian (PC)	Uncompressed	1	\N	\N	2	\N	\N	\N	\N	\N	\N	f	0	39531315	1	library internal use	3034	3878	400	8,8,8	integer	3	0	7	\N	2.2	100	\N	\N	f	\N	\N	\N	\N
642	1668	TIFF 6.0	Little Endian (PC)	Uncompressed	1	\N	\N	2	\N	\N	\N	\N	\N	\N	f	0	39950746	1	library internal use	4044	3295	400	8,8,8	integer	3	0	7	\N	2.2	100	\N	\N	f	\N	\N	\N	\N
643	1669	TIFF 6.0	Little Endian (PC)	Uncompressed	1	\N	\N	2	\N	\N	\N	\N	\N	\N	f	0	39111885	1	library internal use	4035	3234	400	8,8,8	integer	3	0	7	\N	2.2	100	\N	\N	f	\N	\N	\N	\N
644	1670	TIFF 6.0	Little Endian (PC)	Uncompressed	1	\N	\N	2	\N	\N	\N	\N	\N	\N	f	0	39845888	1	library internal use	4018	3304	400	8,8,8	integer	3	0	7	\N	2.2	100	I did not crop out the writing on the bottom of the picture	\N	f	\N	\N	\N	\N
645	1671	TIFF 6.0	Little Endian (PC)	Uncompressed	1	\N	\N	2	\N	\N	\N	\N	\N	\N	f	0	44040192	1	library internal use	4663	3147	400	8,8,8	integer	3	0	7	\N	2.2	100	\N	\N	f	\N	\N	\N	\N
646	1672	TIFF 6.0	Little Endian (PC)	Uncompressed	1	\N	\N	2	\N	\N	\N	\N	\N	\N	f	0	44249907	1	library internal use	4654	3173	400	8,8,8	integer	3	0	7	\N	2.2	100	\N	\N	f	\N	\N	\N	\N
647	1673	TIFF 6.0	Little Endian (PC)	Uncompressed	1	\N	\N	2	\N	\N	\N	\N	\N	\N	f	0	39741030	1	library internal use	4053	3269	400	8,8,8	integer	3	0	7	\N	2.2	100	No info on bottom of picture	\N	f	\N	\N	\N	\N
648	1674	TIFF 6.0	Little Endian (PC)	Uncompressed	1	\N	\N	2	\N	\N	\N	\N	\N	\N	f	0	32505856	1	library internal use	3791	2859	400	8,8,8	integer	3	0	7	\N	2.2	100	No info on bottom of picture	\N	f	\N	\N	\N	\N
649	1675	TIFF 6.0	Little Endian (PC)	Uncompressed	1	\N	\N	2	\N	\N	\N	\N	\N	\N	f	0	32820429	0	library internal use	3800	2877	400	8,8,8	integer	3	0	0	\N	2.2	100	No info on bottom of picture	\N	f	\N	\N	\N	\N
650	1676	TIFF 6.0	Little Endian (PC)	Uncompressed	1	\N	\N	2	\N	\N	\N	\N	\N	\N	f	0	17511219	1	library internal use	2049	2841	400	8,8,8	integer	3	0	7	\N	2.2	100	\N	\N	f	\N	\N	\N	\N
651	1677	TIFF 6.0	Little Endian (PC)	Uncompressed	1	\N	\N	2	\N	\N	\N	\N	\N	\N	f	0	9248440	0	library internal use	1499	2057	400	8,8,8	integer	3	0	0	\N	2.2	100	No info under photo	\N	f	\N	\N	\N	\N
652	1678	TIFF 6.0	Little Endian (PC)	Uncompressed	1	\N	\N	2	\N	\N	\N	\N	\N	\N	f	0	31142707	0	library internal use	4035	2574	400	8,8,8	integer	3	0	0	\N	2.2	100	\N	\N	f	\N	\N	\N	\N
653	1679	TIFF 6.0	Little Endian (PC)	Uncompressed	1	\N	\N	2	\N	\N	\N	\N	\N	\N	f	0	31666995	0	library internal use	2894	3643	400	8,8,8	integer	3	0	0	\N	2.2	100	\N	\N	f	\N	\N	\N	\N
654	1680	TIFF 6.0	Little Endian (PC)	Uncompressed	1	\N	\N	2	\N	\N	\N	\N	\N	\N	f	0	35337011	1	library internal use	4018	2929	400	8,8,8	integer	3	0	7	\N	2.2	100	\N	\N	f	\N	\N	\N	\N
655	1681	TIFF 6.0	Little Endian (PC)	Uncompressed	1	\N	\N	2	\N	\N	\N	\N	\N	\N	f	0	12478054	1	library internal use	2049	2031	400	8,8,8	integer	3	0	7	\N	2.2	100	\N	\N	f	\N	\N	\N	\N
656	1682	TIFF 6.0	Little Endian (PC)	Uncompressed	1	\N	\N	2	\N	\N	\N	\N	\N	\N	f	0	40055603	1	library internal use	3313	4035	400	8,8,8	integer	3	0	7	\N	2.2	100	\N	\N	f	\N	\N	\N	\N
657	1683	TIFF 6.0	Little Endian (PC)	Uncompressed	1	\N	\N	2	\N	\N	\N	\N	\N	\N	f	0	16882074	1	library internal use	3974	1412	400	8,8,8	integer	3	0	7	\N	2.2	100	\N	\N	f	\N	\N	\N	\N
658	1685	TIFF 6.0	Little Endian (PC)	Uncompressed	1	\N	\N	2	\N	\N	\N	\N	\N	\N	f	0	20552090	0	library internal use	2127	3216	400	8,8,8	integer	3	0	0	\N	2.2	100	\N	\N	f	\N	\N	\N	\N
659	1686	TIFF 6.0	Little Endian (PC)	Uncompressed	1	\N	\N	2	\N	\N	\N	\N	\N	\N	f	0	18454938	0	library internal use	1979	3111	400	8,8,8	integer	3	0	0	\N	2.2	100	\N	\N	f	\N	\N	\N	\N
660	1687	TIFF 6.0	Little Endian (PC)	Uncompressed	1	\N	\N	2	\N	\N	\N	\N	\N	\N	f	0	9196012	0	library internal use	1950	1572	200	8,8,8	integer	3	0	0	\N	2.2	100	\N	\N	f	\N	\N	\N	\N
661	1688	TIFF 6.0	Little Endian (PC)	Uncompressed	1	\N	\N	2	\N	\N	\N	\N	\N	\N	f	0	1384120	0	library internal use	575	801	200	8,8,8	integer	3	0	0	\N	2.2	100	\N	\N	f	\N	\N	\N	\N
662	1689	TIFF 6.0	Little Endian (PC)	Uncompressed	1	\N	\N	2	\N	\N	\N	\N	\N	\N	f	0	9552527	0	library internal use	1964	1622	200	8,8,8	integer	3	0	0	\N	2.2	100	\N	\N	f	\N	\N	\N	\N
663	1690	TIFF 6.0	Little Endian (PC)	Uncompressed	1	\N	\N	2	\N	\N	\N	\N	\N	\N	f	0	3208643	0	library internal use	1972	1629	200	8,8,8	integer	3	0	0	\N	2.2	100	\N	\N	f	\N	\N	\N	\N
664	1691	TIFF 6.0	Little Endian (PC)	Uncompressed	1	\N	\N	2	\N	\N	\N	\N	\N	\N	f	0	3145728	0	library internal use	1964	1602	200	8,8,8	integer	3	0	0	\N	2.2	100	\N	\N	f	\N	\N	\N	\N
665	1692	TIFF 6.0	Little Endian (PC)	Uncompressed	1	\N	\N	2	\N	\N	\N	\N	\N	\N	f	0	3177185	0	library internal use	1981	1605	200	8,8,8	integer	3	0	0	\N	2.2	100	\N	\N	f	\N	\N	\N	\N
666	1693	TIFF 6.0	Little Endian (PC)	Uncompressed	1	\N	\N	2	\N	\N	\N	\N	\N	\N	f	0	9531556	0	library internal use	1990	1596	200	8,8,8	integer	3	0	0	\N	2.2	100	\N	\N	f	\N	\N	\N	\N
667	1694	TIFF 6.0	Little Endian (PC)	Uncompressed	1	\N	\N	2	\N	\N	\N	\N	\N	\N	f	0	3219128	0	library internal use	1990	1620	200	8,8,8	integer	3	0	0	\N	2.2	100	\N	\N	f	\N	\N	\N	\N
668	1695	TIFF 6.0	Little Endian (PC)	Uncompressed	1	\N	\N	2	\N	\N	\N	\N	\N	\N	f	0	9374269	0	library internal use	1592	1962	200	8,8,8	integer	3	0	0	\N	2.2	100	\N	\N	f	\N	\N	\N	\N
669	1696	TIFF 6.0	Little Endian (PC)	Uncompressed	1	\N	\N	2	\N	\N	\N	\N	\N	\N	f	0	9384755	0	library internal use	1592	1964	200	8,8,8	integer	3	0	0	\N	2.2	100	\N	\N	f	\N	\N	\N	\N
670	1697	TIFF 6.0	Little Endian (PC)	Uncompressed	1	\N	\N	2	\N	\N	\N	\N	\N	\N	f	0	9353298	0	library internal use	1976	1578	200	8,8,8	integer	3	0	0	\N	2.2	100	\N	\N	f	\N	\N	\N	\N
671	1698	TIFF 6.0	Little Endian (PC)	Uncompressed	1	\N	\N	2	\N	\N	\N	\N	\N	\N	f	0	2789212	0	library internal use	1371	677	200	8,8,8	integer	3	0	0	\N	2.2	100	\N	\N	f	\N	\N	\N	\N
672	1699	TIFF 6.0	Little Endian (PC)	Uncompressed	1	\N	\N	2	\N	\N	\N	\N	\N	\N	f	0	9353298	0	library internal use	1592	1958	200	8,8,8	integer	3	0	0	\N	2.2	100	\N	\N	f	\N	\N	\N	\N
673	1700	TIFF 6.0	Little Endian (PC)	Uncompressed	1	\N	\N	2	\N	\N	\N	\N	\N	\N	f	0	1342177	0	library internal use	972	1382	200	8,8,8	integer	3	0	0	\N	2.2	100	\N	\N	f	\N	\N	\N	\N
674	1701	TIFF 6.0	Little Endian (PC)	Uncompressed	1	\N	\N	2	\N	\N	\N	\N	\N	\N	f	0	37539021	0	library internal use	3146	3975	400	8,8,8	integer	3	0	0	\N	2.2	100	\N	\N	f	\N	\N	\N	\N
675	1702	TIFF 6.0	Little Endian (PC)	Uncompressed	1	\N	\N	2	\N	\N	\N	\N	\N	\N	f	0	6406799	0	library internal use	1276	1673	200	8,8,8	integer	3	0	0	\N	2.2	100	\N	\N	f	\N	\N	\N	\N
676	1703	TIFF 6.0	Little Endian (PC)	Uncompressed	1	\N	\N	2	\N	\N	\N	\N	\N	\N	f	0	6448742	0	library internal use	1286	1672	200	8,8,8	integer	3	0	0	\N	2.2	100	\N	\N	f	\N	\N	\N	\N
677	1704	TIFF 6.0	Little Endian (PC)	Uncompressed	1	\N	\N	2	\N	\N	\N	\N	\N	\N	f	0	72876032	0	library internal use	4383	5544	400	8,8,8	integer	3	0	0	\N	2.2	100	\N	\N	f	\N	\N	\N	\N
678	1705	TIFF 6.0	Little Endian (PC)	Uncompressed	1	\N	\N	2	\N	\N	\N	\N	\N	\N	f	0	69310874	0	library internal use	5567	4149	400	8,8,8	integer	3	0	0	\N	2.2	100	\N	\N	f	\N	\N	\N	\N
679	1707	TIFF 6.0	Little Endian (PC)	Uncompressed	1	\N	\N	2	\N	\N	\N	\N	\N	\N	f	0	13526630	0	library internal use	1717	2632	400	8,8,8	integer	3	0	0	\N	2.2	100	\N	\N	f	\N	\N	\N	\N
680	1708	TIFF 6.0	Little Endian (PC)	Uncompressed	1	\N	\N	2	\N	\N	\N	\N	\N	\N	f	0	13316915	0	library internal use	2606	1700	400	8,8,8	integer	3	0	0	\N	2.2	100	\N	\N	f	\N	\N	\N	\N
681	1709	TIFF 6.0	Little Endian (PC)	Uncompressed	1	\N	\N	2	\N	\N	\N	\N	\N	\N	f	0	38797312	0	library internal use	3226	4009	400	8,8,8	integer	3	0	0	\N	2.2	100	\N	\N	f	\N	\N	\N	\N
682	1710	TIFF 6.0	Little Endian (PC)	Uncompressed	1	\N	\N	2	\N	\N	\N	\N	\N	\N	f	0	44879053	0	library internal use	3199	4680	400	8,8,8	integer	3	0	0	\N	2.2	100	\N	\N	f	\N	\N	\N	\N
683	1714	TIFF 6.0	Little Endian (PC)	Uncompressed	1	\N	\N	2	\N	\N	\N	\N	\N	\N	f	0	14260634	0	library internal use	1805	2632	400	8,8,8	integer	3	0	0	\N	2.2	100	\N	\N	f	\N	\N	\N	\N
684	1715	TIFF 6.0	Little Endian (PC)	Uncompressed	1	\N	\N	2	\N	\N	\N	\N	\N	\N	f	0	13946061	0	library internal use	1761	2641	400	8,8,8	integer	3	0	0	\N	2.2	100	\N	\N	f	\N	\N	\N	\N
685	1715	TIFF 6.0	Little Endian (PC)	Uncompressed	1		\N	2	\N	\N	\N	\N	\N	\N	f	0	13946061	0	library internal use	1761	2641	400	8,8,8	integer	3	0	0	\N	2.2	100	\N	\N	f	\N	\N	\N	\N
686	1716	TIFF 6.0	Little Endian (PC)	Uncompressed	1	\N	\N	2	\N	\N	\N	\N	\N	\N	f	0	13946061	0	library internal use	1770	2632	400	8,8,8	integer	3	0	0	\N	2.2	100	\N	\N	f	\N	\N	\N	\N
687	1716	TIFF 6.0	Little Endian (PC)	Uncompressed	1		\N	2	\N	\N	\N	\N	\N	\N	f	0	13946061	0	library internal use	1770	2632	400	8,8,8	integer	3	0	0	\N	2.2	100	\N	\N	f	\N	\N	\N	\N
688	1718	TIFF 6.0	Little Endian (PC)	Uncompressed	1	\N	\N	2	\N	\N	\N	\N	\N	\N	f	0	13946061	0	library internal use	1778	2606	400	8,8,8	integer	3	0	0	\N	2.2	100	\N	\N	f	\N	\N	\N	\N
689	1719	TIFF 6.0	Little Endian (PC)	Uncompressed	1	\N	\N	2	\N	\N	\N	\N	\N	\N	f	0	14155776	0	library internal use	1796	2632	400	8,8,8	integer	3	0	0	\N	2.2	100	\N	\N	f	\N	\N	\N	\N
690	1720	TIFF 6.0	Little Endian (PC)	Uncompressed	1	\N	\N	2	\N	\N	\N	\N	\N	\N	f	0	14365491	0	library internal use	1813	2632	400	8,8,8	integer	3	0	0	\N	2.2	100	\N	\N	f	\N	\N	\N	\N
691	1721	TIFF 6.0	Little Endian (PC)	Uncompressed	1	\N	\N	2	\N	\N	\N	\N	\N	\N	f	0	14575206	0	library internal use	1848	2623	400	8,8,8	integer	3	0	0	\N	2.2	100	\N	\N	f	\N	\N	\N	\N
692	1722	TIFF 6.0	Little Endian (PC)	Uncompressed	1	\N	\N	2	\N	\N	\N	\N	\N	\N	f	0	14260634	0	library internal use	1822	2615	400	8,8,8	integer	3	0	0	\N	2.2	100	\N	\N	f	\N	\N	\N	\N
693	1723	TIFF 6.0	Little Endian (PC)	Uncompressed	1	\N	\N	2	\N	\N	\N	\N	\N	\N	f	0	28521267	0	library internal use	3528	2694	400	8,8,8	integer	3	0	0	\N	2.2	100	\N	\N	f	\N	\N	\N	\N
694	1724	TIFF 6.0	Little Endian (PC)	Uncompressed	1	\N	\N	2	\N	\N	\N	\N	\N	\N	f	0	32820429	0	library internal use	3503	3121	400	8,8,8	integer	3	0	0	\N	2.2	100	\N	\N	f	\N	\N	\N	\N
695	1711	TIFF 6.0	Little Endian (PC)	Uncompressed	1	\N	\N	2	\N	\N	\N	\N	\N	\N	f	0	6301942	0	library internal use	1116	1882	400	8,8,8	integer	3	0	0	\N	2.2	100	\N	\N	f	\N	\N	\N	\N
696	1711	TIFF 6.0	Little Endian (PC)	Uncompressed	1		\N	2	\N	\N	\N	\N	\N	\N	f	0	6301942	0	library internal use	1116	1882	400	8,8,8	integer	3	0	0	\N	2.2	100	\N	\N	f	\N	\N	\N	\N
697	1711	TIFF 6.0	Little Endian (PC)	Uncompressed	1		\N	2	\N	\N	\N	\N	\N	\N	f	0	6301942	0	library internal use	1116	1882	400	8,8,8	integer	3	0	0	\N	2.2	100	\N	\N	f	\N	\N	\N	\N
698	1713	TIFF 6.0	Little Endian (PC)	Uncompressed	1	\N	\N	2	\N	\N	\N	\N	\N	\N	f	0	47710208	0	library internal use	3400	4680	400	8,8,8	integer	3	0	0	\N	2.2	100	\N	\N	f	\N	\N	\N	\N
699	1725	TIFF 6.0	Little Endian (PC)	Uncompressed	1	\N	\N	2	\N	\N	\N	\N	\N	\N	f	0	38797312	0	library internal use	3182	4061	400	8,8,8	integer	3	0	0	\N	2.2	100	\N	\N	f	\N	\N	\N	\N
700	1726	TIFF 6.0	Little Endian (PC)	Uncompressed	1	\N	\N	2	\N	\N	\N	\N	\N	\N	f	0	4739564	0	library internal use	985	1604	400	8,8,8	integer	3	0	0	\N	2.2	100	\N	\N	f	\N	\N	\N	\N
701	1727	TIFF 6.0	Little Endian (PC)	Uncompressed	1	\N	\N	2	\N	\N	\N	\N	\N	\N	f	0	34183578	0	library internal use	2659	4279	400	8,8,8	integer	3	0	0	\N	2.2	100	\N	\N	f	\N	\N	\N	\N
702	1728	TIFF 6.0	Little Endian (PC)	Uncompressed	1	\N	\N	2	\N	\N	\N	\N	\N	\N	f	0	46976205	0	library internal use	4610	3400	400	8,8,8	integer	3	0	0	\N	2.2	100	\N	\N	f	\N	\N	\N	\N
703	1729	TIFF 6.0	Little Endian (PC)	Uncompressed	1	\N	\N	2	\N	\N	\N	\N	\N	\N	f	0	46032486	0	library internal use	4514	3400	400	8,8,8	integer	3	0	0	\N	2.2	100	\N	\N	f	\N	\N	\N	\N
704	1730	TIFF 6.0	Little Endian (PC)	Uncompressed	1	\N	\N	2	\N	\N	\N	\N	\N	\N	f	0	29150413	0	library internal use	2502	3887	400	8,8,8	integer	3	0	0	\N	2.2	100	\N	\N	f	\N	\N	\N	\N
705	1731	TIFF 6.0	Little Endian (PC)	Uncompressed	1	\N	\N	2	\N	\N	\N	\N	\N	\N	f	0	33239859	0	library internal use	3852	2877	400	8,8,8	integer	3	0	0	\N	2.2	100	\N	\N	f	\N	\N	\N	\N
706	1732	TIFF 6.0	Little Endian (PC)	Uncompressed	1	\N	\N	2	\N	\N	\N	\N	\N	\N	f	0	44774195	0	library internal use	4628	3226	400	8,8,8	integer	3	0	0	\N	2.2	100	\N	\N	f	\N	\N	\N	\N
707	1733	TIFF 6.0	Little Endian (PC)	Uncompressed	1	\N	\N	2	\N	\N	\N	\N	\N	\N	f	0	27787264	0	library internal use	4680	1979	400	8,8,8	integer	3	0	0	\N	2.2	100	\N	\N	f	\N	\N	\N	\N
708	1734	TIFF 6.0	Little Endian (PC)	Uncompressed	1	\N	\N	2	\N	\N	\N	\N	\N	\N	f	0	13526630	0	library internal use	1709	2641	400	8,8,8	integer	3	0	0	\N	2.2	100	\N	\N	f	\N	\N	\N	\N
709	1735	TIFF 6.0	Little Endian (PC)	Uncompressed	1	\N	\N	2	\N	\N	\N	\N	\N	\N	f	0	31771853	0	library internal use	2938	3599	400	8,8,8	integer	3	0	0	\N	2.2	100	\N	\N	f	\N	\N	\N	\N
710	1736	TIFF 6.0	Little Endian (PC)	Uncompressed	1	\N	\N	2	\N	\N	\N	\N	\N	\N	f	0	4561306	0	library internal use	958	1588	400	8,8,8	integer	3	0	0	\N	2.2	100	\N	\N	f	\N	\N	\N	\N
711	1737	TIFF 6.0	Little Endian (PC)	Uncompressed	1	\N	\N	2	\N	\N	\N	\N	\N	\N	f	0	39007027	0	library internal use	3234	4018	400	8,8,8	integer	3	0	0	\N	2.2	100	\N	\N	f	\N	\N	\N	\N
712	1738	TIFF 6.0	Little Endian (PC)	Uncompressed	1	\N	\N	2	\N	\N	\N	\N	\N	\N	f	0	39111885	0	library internal use	4035	3234	400	8,8,8	integer	3	0	0	\N	2.2	100	\N	\N	f	\N	\N	\N	\N
713	1739	TIFF 6.0	Little Endian (PC)	Uncompressed	1	\N	\N	2	\N	\N	\N	\N	\N	\N	f	0	34288435	0	library internal use	2859	4000	400	8,8,8	integer	3	0	0	\N	2.2	100	\N	\N	f	\N	\N	\N	\N
714	1740	TIFF 6.0	Little Endian (PC)	Uncompressed	1	\N	\N	2	\N	\N	\N	\N	\N	\N	f	0	38902170	0	library internal use	3226	4018	400	8,8,8	integer	3	0	0	\N	2.2	100	\N	\N	f	\N	\N	\N	\N
715	1741	TIFF 6.0	Little Endian (PC)	Uncompressed	1	\N	\N	2	\N	\N	\N	\N	\N	\N	f	0	9688842	0	library internal use	1604	2013	400	8,8,8	integer	3	0	0	\N	2.2	100	\N	\N	f	\N	\N	\N	\N
716	1742	TIFF 6.0	Little Endian (PC)	Uncompressed	1	\N	\N	2	\N	\N	\N	\N	\N	\N	f	0	5976883	0	library internal use	1098	1813	400	8,8,8	integer	3	0	0	\N	2.2	100	\N	\N	f	\N	\N	\N	\N
717	1743	TIFF 6.0	Little Endian (PC)	Uncompressed	1	\N	\N	2	\N	\N	\N	\N	\N	\N	f	0	5609882	0	library internal use	1804	1037	400	8,8,8	integer	3	0	0	\N	2.2	100	\N	\N	f	\N	\N	\N	\N
718	1744	TIFF 6.0	Little Endian (PC)	Uncompressed	1	\N	\N	2	\N	\N	\N	\N	\N	\N	f	0	6029312	0	library internal use	1831	1098	400	8,8,8	integer	3	0	0	\N	2.2	100	\N	\N	f	\N	\N	\N	\N
719	1744	TIFF 6.0	Little Endian (PC)	Uncompressed	1		\N	2	\N	\N	\N	\N	\N	\N	f	0	6029312	0	library internal use	1831	1098	400	8,8,8	integer	3	0	0	\N	2.2	100	\N	\N	f	\N	\N	\N	\N
720	1746	TIFF 6.0	Little Endian (PC)	Uncompressed	1	\N	\N	2	\N	\N	\N	\N	\N	\N	f	0	7056916	0	library internal use	1900	1238	400	8,8,8	integer	3	0	0	\N	2.2	100	\N	\N	f	\N	\N	\N	\N
721	1747	TIFF 6.0	Little Endian (PC)	Uncompressed	1	\N	\N	2	\N	\N	\N	\N	\N	\N	f	0	46347059	0	library internal use	4602	3356	400	8,8,8	integer	3	0	0	\N	2.2	100	\N	\N	f	\N	\N	\N	\N
722	1748	TIFF 6.0	Little Endian (PC)	Uncompressed	1	\N	\N	2	\N	\N	\N	\N	\N	\N	f	0	6008340	0	library internal use	1839	1090	400	8,8,8	integer	3	0	0	\N	2.2	100	\N	\N	f	\N	\N	\N	\N
723	1749	TIFF 6.0	Little Endian (PC)	Uncompressed	1	\N	\N	2	\N	\N	\N	\N	\N	\N	f	0	22754099	0	library internal use	2206	3442	400	8,8,8	integer	3	0	0	\N	2.2	100	\N	\N	f	\N	\N	\N	\N
724	1750	TIFF 6.0	Little Endian (PC)	Uncompressed	1	\N	\N	2	\N	\N	\N	\N	\N	\N	f	0	17091789	0	library internal use	1988	2867	400	8,8,8	integer	3	0	0	\N	2.2	100	\N	\N	f	\N	\N	\N	\N
725	1751	TIFF 6.0	Little Endian (PC)	Uncompressed	1	\N	\N	2	\N	\N	\N	\N	\N	\N	f	0	16672358	0	library internal use	1996	2789	400	8,8,8	integer	3	0	0	\N	2.2	100	\N	\N	f	\N	\N	\N	\N
726	1752	TIFF 6.0	Little Endian (PC)	Uncompressed	1	\N	\N	2	\N	\N	\N	\N	\N	\N	f	0	16777216	0	library internal use	1996	2806	400	8,8,8	integer	3	0	0	\N	2.2	100	\N	\N	f	\N	\N	\N	\N
727	1753	TIFF 6.0	Little Endian (PC)	Uncompressed	1	\N	\N	2	\N	\N	\N	\N	\N	\N	f	0	16777216	0	library internal use	1996	2806	400	8,8,8	integer	3	0	0	\N	2.2	100	\N	\N	f	\N	\N	\N	\N
728	1754	TIFF 6.0	Little Endian (PC)	Uncompressed	1	\N	\N	2	\N	\N	\N	\N	\N	\N	f	0	39741030	1	library internal use	4070	3252	400	8,8,8	integer	3	0	7	\N	2.2	100	\N	\N	f	\N	\N	\N	\N
729	1755	TIFF 6.0	Little Endian (PC)	Uncompressed	1	\N	\N	2	\N	\N	\N	\N	\N	\N	f	0	40055603	1	library internal use	4070	3278	400	8,8,8	integer	3	0	7	\N	2.2	100	\N	\N	f	\N	\N	\N	\N
730	1756	TIFF 6.0	Little Endian (PC)	Uncompressed	1	\N	\N	2	\N	\N	\N	\N	\N	\N	f	0	33135002	1	library internal use	4035	2737	400	8,8,8	integer	3	0	7	\N	2.2	100	\N	\N	f	\N	\N	\N	\N
731	1757	TIFF 6.0	Little Endian (PC)	Uncompressed	1	\N	\N	2	\N	\N	\N	\N	\N	\N	f	0	40265318	0	library internal use	4053	3313	400	8,8,8	integer	3	0	0	\N	2.2	100	\N	\N	f	\N	\N	\N	\N
732	1758	TIFF 6.0	Little Endian (PC)	Uncompressed	1	\N	\N	2	\N	\N	\N	\N	\N	\N	f	0	9363784	1	library internal use	2266	1377	400	8,8,8	integer	3	0	7	\N	2.2	100	\N	\N	f	\N	\N	\N	\N
733	1759	TIFF 6.0	Little Endian (PC)	Uncompressed	1	\N	\N	2	\N	\N	\N	\N	\N	\N	f	0	10328474	1	library internal use	2379	1447	400	8,8,8	integer	3	0	7	\N	2.2	100	\N	\N	f	\N	\N	\N	\N
734	1760	TIFF 6.0	Little Endian (PC)	Uncompressed	1	\N	\N	2	\N	\N	\N	\N	\N	\N	f	0	10485760	1	library internal use	2379	1473	400	8,8,8	integer	3	0	7	\N	2.2	100	\N	\N	f	\N	\N	\N	\N
735	1761	TIFF 6.0	Little Endian (PC)	Uncompressed	1	\N	\N	2	\N	\N	\N	\N	\N	\N	f	0	10485760	0	library internal use	2388	1465	400	8,8,8	integer	3	0	0	\N	2.2	100	\N	\N	f	\N	\N	\N	\N
736	1762	TIFF 6.0	Little Endian (PC)	Uncompressed	1	\N	\N	2	\N	\N	\N	\N	\N	\N	f	0	28521267	0	library internal use	5600	1707	400	8,8,8	integer	3	0	0	\N	2.2	100	The paper said it would also  include a quote but the image only contains his signature	\N	f	\N	\N	\N	\N
737	1763	TIFF 6.0	Little Endian (PC)	Uncompressed	1	\N	\N	2	\N	\N	\N	\N	\N	\N	f	0	7707034	0	library internal use	1334	1926	400	8,8,8	integer	3	0	0	\N	2.2	100	\N	\N	f	\N	\N	\N	\N
738	1764	TIFF 6.0	Little Endian (PC)	Uncompressed	1	\N	\N	2	\N	\N	\N	\N	\N	\N	f	0	25794970	1	library internal use	2354	3660	400	8,8,8	integer	3	0	7	\N	2.2	100	\N	\N	f	\N	\N	\N	\N
739	1765	TIFF 6.0	Little Endian (PC)	Uncompressed	1	\N	\N	2	\N	\N	\N	\N	\N	\N	f	0	26004685	1	library internal use	2363	3669	400	8,8,8	integer	3	0	7	\N	2.2	100	\N	\N	f	\N	\N	\N	\N
740	1766	TIFF 6.0	Little Endian (PC)	Uncompressed	1	\N	\N	2	\N	\N	\N	\N	\N	\N	f	0	10905190	1	library internal use	1430	2554	400	8,8,8	integer	3	0	7	\N	2.2	100	\N	\N	f	\N	\N	\N	\N
741	1767	TIFF 6.0	Little Endian (PC)	Uncompressed	1	\N	\N	2	\N	\N	\N	\N	\N	\N	f	0	20866662	1	library internal use	2737	2537	400	8,8,8	integer	3	0	7	\N	2.2	100	\N	\N	f	\N	\N	\N	\N
742	1768	TIFF 6.0	Little Endian (PC)	Uncompressed	1	\N	\N	2	\N	\N	\N	\N	\N	\N	f	0	9479127	0	library internal use	2144	1473	400	8,8,8	integer	3	0	0	\N	2.2	100	\N	\N	f	\N	\N	\N	\N
743	1769	TIFF 6.0	Little Endian (PC)	Uncompressed	1	\N	\N	2	\N	\N	\N	\N	\N	\N	f	0	40055603	1	library internal use	4070	3278	400	8,8,8	integer	3	0	7	\N	2.2	100	\N	\N	f	\N	\N	\N	\N
744	1770	TIFF 6.0	Little Endian (PC)	Uncompressed	1	\N	\N	2	\N	\N	\N	\N	\N	\N	f	0	26214400	1	library internal use	2424	3608	400	8,8,8	integer	3	0	7	\N	2.2	100	\N	\N	f	\N	\N	\N	\N
745	1771	TIFF 6.0	Little Endian (PC)	Uncompressed	1	\N	\N	2	\N	\N	\N	\N	\N	\N	f	0	24956109	1	library internal use	2581	3225	400	8,8,8	integer	3	0	7	\N	2.2	100	\N	\N	f	\N	\N	\N	\N
746	1772	TIFF 6.0	Little Endian (PC)	Uncompressed	1	\N	\N	2	\N	\N	\N	\N	\N	\N	f	0	27053261	1	library internal use	2458	3669	400	8,8,8	integer	3	0	7	\N	2.2	100	\N	\N	f	\N	\N	\N	\N
747	1773	TIFF 6.0	Little Endian (PC)	Uncompressed	1	\N	\N	2	\N	\N	\N	\N	\N	\N	f	0	8105492	1	library internal use	1308	2065	400	8,8,8	integer	3	0	7	\N	2.2	100	\N	\N	f	\N	\N	\N	\N
748	1774	TIFF 6.0	Little Endian (PC)	Uncompressed	1	\N	\N	2	\N	\N	\N	\N	\N	\N	f	0	40475033	1	library internal use	4053	3330	400	8,8,8	integer	3	0	7	\N	2.2	100	\N	\N	f	\N	\N	\N	\N
749	1774	TIFF 6.0	Little Endian (PC)	Uncompressed	1	\N	\N	2	\N	\N	\N	\N	\N	\N	f	0	40475034	0	library internal use	0	0	400	8,8,8	integer	3	0	0	\N	2.2	100	\N	\N	f	\N	\N	\N	\N
750	1775	TIFF 6.0	Little Endian (PC)	Uncompressed	1	\N	\N	2	\N	\N	\N	\N	\N	\N	f	0	40475033	1	library internal use	4053	3330	400	8,8,8	integer	3	0	7	\N	2.2	100	\N	\N	f	\N	\N	\N	\N
751	1776	TIFF 6.0	Big Endian (Mac)	Uncompressed	1	\N	\N	2	\N	\N	\N	\N	\N	\N	f	0	42572186	2	library internal use	6203	2288	400	8,8,8	integer	3	0	7	\N	2.2	100	\N	\N	f	\N	\N	\N	\N
752	1777	TIFF 6.0	Little Endian (PC)	Uncompressed	1	\N	\N	2	\N	\N	\N	\N	\N	\N	f	0	11744051	0	library internal use	1975	1983	400	8,8,8	integer	3	0	0	\N	2.2	100	\N	\N	f	\N	\N	\N	\N
753	1778	TIFF 6.0	Little Endian (PC)	Uncompressed	1	\N	\N	2	\N	\N	\N	\N	\N	\N	f	0	12373197	0	library internal use	1967	2033	400	8,8,8	integer	3	0	0	\N	2.2	100	\N	\N	f	\N	\N	\N	\N
754	1779	TIFF 6.0	Little Endian (PC)	Uncompressed	1	\N	\N	2	\N	\N	\N	\N	\N	\N	f	0	53372518	3	library internal use	3667	4850	400	8,8,8	integer	3	0	7	\N	2.2	100	\N	\N	f	\N	\N	\N	\N
755	1780	TIFF 6.0	Little Endian (PC)	Uncompressed	1	\N	\N	2	\N	\N	\N	\N	\N	\N	f	0	19818086	0	library internal use	3200	2067	400	8,8,8	integer	3	0	0	\N	2.2	100	\N	\N	f	\N	\N	\N	\N
756	1781	TIFF 6.0	Little Endian (PC)	Uncompressed	1	\N	\N	2	\N	\N	\N	\N	\N	\N	f	0	19503514	0	library internal use	2033	3200	400	8,8,8	integer	3	0	0	\N	2.2	100	\N	\N	f	\N	\N	\N	\N
757	1782	TIFF 6.0	Little Endian (PC)	Uncompressed	1	\N	\N	2	\N	\N	\N	\N	\N	\N	f	0	54630810	0	library internal use	3246	5615	400	8,8,8	integer	3	0	0	\N	2.2	100	\N	\N	f	\N	\N	\N	\N
758	1783	TIFF 6.0	Little Endian (PC)	Uncompressed	1	\N	\N	2	\N	\N	\N	\N	\N	\N	f	0	15728640	0	library internal use	1874	2789	400	8,8,8	integer	3	0	0	\N	2.2	100	\N	\N	f	\N	\N	\N	\N
759	1784	TIFF 6.0	Little Endian (PC)	Uncompressed	1	\N	\N	2	\N	\N	\N	\N	\N	\N	f	0	11639194	0	library internal use	1543	2510	400	8,8,8	integer	3	0	0	\N	2.2	100	\N	\N	f	\N	\N	\N	\N
760	1785	TIFF 6.0	Little Endian (PC)	Uncompressed	1	\N	\N	2	\N	\N	\N	\N	\N	\N	f	0	11429478	0	library internal use	1517	2510	400	8,8,8	integer	3	0	0	\N	2.2	100	\N	\N	f	\N	\N	\N	\N
761	1786	TIFF 6.0	Little Endian (PC)	Uncompressed	1	\N	\N	2	\N	\N	\N	\N	\N	\N	f	0	6805258	0	library internal use	1107	2048	400	8,8,8	integer	3	0	0	\N	2.2	100	\N	\N	f	\N	\N	\N	\N
762	1787	TIFF 6.0	Little Endian (PC)	Uncompressed	1	\N	\N	2	\N	\N	\N	\N	\N	\N	f	0	14889779	0	library internal use	1700	2920	400	8,8,8	integer	3	0	0	\N	2.2	100	\N	\N	f	\N	\N	\N	\N
763	1788	TIFF 6.0	Little Endian (PC)	Uncompressed	1	\N	\N	2	\N	\N	\N	\N	\N	\N	f	0	27787264	0	library internal use	2293	4035	400	8,8,8	integer	3	0	0	\N	2.2	100	\N	\N	f	\N	\N	\N	\N
764	1789	TIFF 6.0	Little Endian (PC)	Uncompressed	1	\N	\N	2	\N	\N	\N	\N	\N	\N	f	0	32820429	0	library internal use	3991	1864	400	8,8,8	integer	3	0	0	\N	2.2	100	\N	\N	f	\N	\N	\N	\N
765	1790	TIFF 6.0	Little Endian (PC)	Uncompressed	1	\N	\N	2	\N	\N	\N	\N	\N	\N	f	0	18664653	0	library internal use	1949	3201	400	8,8,8	integer	3	0	0	\N	2.2	100	\N	\N	f	\N	\N	\N	\N
766	1791	TIFF 6.0	Little Endian (PC)	Uncompressed	1	\N	\N	2	\N	\N	\N	\N	\N	\N	f	0	27262976	0	library internal use	6396	1419	400	8,8,8	integer	3	0	0	\N	2.2	100	\N	\N	f	\N	\N	\N	\N
767	1792	TIFF 6.0	Little Endian (PC)	Uncompressed	1	\N	\N	2	\N	\N	\N	\N	\N	\N	f	0	45403341	0	library internal use	6403	2363	400	8,8,8	integer	3	0	0	\N	2.2	100	\N	\N	f	\N	\N	\N	\N
768	1793	TIFF 6.0	Little Endian (PC)	Uncompressed	1	\N	\N	2	\N	\N	\N	\N	\N	\N	f	0	23068672	0	library internal use	2402	3205	400	8,8,8	integer	3	0	0	\N	2.2	100	\N	\N	f	\N	\N	\N	\N
769	1794	TIFF 6.0	Little Endian (PC)	Uncompressed	1	\N	\N	2	\N	\N	\N	\N	\N	\N	f	0	21600666	0	library internal use	2246	3207	400	8,8,8	integer	3	0	0	\N	2.2	100	\N	\N	f	\N	\N	\N	\N
770	1795	TIFF 6.0	Little Endian (PC)	Uncompressed	1	\N	\N	2	\N	\N	\N	\N	\N	\N	f	0	41104179	0	library internal use	3182	4305	400	8,8,8	integer	3	0	0	\N	2.2	100	\N	\N	f	\N	\N	\N	\N
771	1796	TIFF 6.0	Little Endian (PC)	Uncompressed	1	\N	\N	2	\N	\N	\N	\N	\N	\N	f	0	155923251	0	library internal use	9601	5414	400	8,8,8	integer	3	0	0	\N	2.2	100	\N	\N	f	\N	\N	\N	\N
772	1797	TIFF 6.0	Little Endian (PC)	Uncompressed	1	\N	\N	2	\N	\N	\N	\N	\N	\N	f	0	17930650	0	library internal use	3582	1665	400	8,8,8	integer	3	0	0	\N	2.2	100	\N	\N	f	\N	\N	\N	\N
773	1798	TIFF 6.0	Little Endian (PC)	Uncompressed	1	\N	\N	2	\N	\N	\N	\N	\N	\N	f	0	7245660	0	library internal use	1743	1386	400	8,8,8	integer	3	0	0	\N	2.2	100	\N	\N	f	\N	\N	\N	\N
774	1799	TIFF 6.0	Little Endian (PC)	Uncompressed	1	\N	\N	2	\N	\N	\N	\N	\N	\N	f	0	118279373	0	library internal use	7087	5562	400	8,8,8	integer	3	0	0	\N	2.2	100	\N	\N	f	\N	\N	\N	\N
775	1800	TIFF 6.0	Little Endian (PC)	Uncompressed	1	Adobe RGB 1998	\N	2	\N	\N	\N	\N	\N	\N	f	0	42362470	1	library internal use	4024	3510	400	8,8,8	integer	3	0	7	\N	2.2	100	\N	2006-07-28 00:00:00	f	\N	\N	\N	\N
776	1801	TIFF 6.0	Little Endian (PC)	Uncompressed	1	\N	\N	2	\N	\N	\N	\N	\N	\N	f	0	44983910	0	library internal use	3391	4419	400	8,8,8	integer	3	0	0	\N	2.2	100	\N	\N	f	\N	\N	\N	\N
777	1802	TIFF 6.0	Little Endian (PC)	Uncompressed	1	\N	\N	2	\N	\N	\N	\N	\N	\N	f	0	17930650	0	library internal use	2004	2982	400	8,8,8	integer	3	0	0	\N	2.2	100	\N	\N	f	\N	\N	\N	\N
778	1803	TIFF 6.0	Little Endian (PC)	Uncompressed	1	\N	\N	2	\N	\N	\N	\N	\N	\N	f	0	41838182	0	library internal use	3287	4244	400	8,8,8	integer	3	0	0	\N	2.2	100	\N	\N	f	\N	\N	\N	\N
779	1804	TIFF 6.0	Little Endian (PC)	Uncompressed	1	\N	\N	2	\N	\N	\N	\N	\N	\N	f	0	18769510	0	library internal use	2057	3050	400	8,8,8	integer	3	0	0	\N	2.2	100	\N	\N	f	\N	\N	\N	\N
780	1805	TIFF 6.0	Little Endian (PC)	Uncompressed	1	\N	\N	2	\N	\N	\N	\N	\N	\N	f	0	43725619	0	library internal use	3313	4401	400	8,8,8	integer	3	0	0	\N	2.2	100	\N	\N	f	\N	\N	\N	\N
781	1806	TIFF 6.0	Little Endian (PC)	Uncompressed	1	\N	\N	2	\N	\N	\N	\N	\N	\N	f	0	2495611	0	library internal use	776	1072	400	8,8,8	integer	3	0	0	\N	2.2	100	\N	\N	f	\N	\N	\N	\N
782	1807	TIFF 6.0	Little Endian (PC)	Uncompressed	1	\N	\N	2	\N	\N	\N	\N	\N	\N	f	0	1614807	0	library internal use	636	846	400	8,8,8	integer	3	0	0	\N	2.2	100	\N	\N	f	\N	\N	\N	\N
783	1808	TIFF 6.0	Little Endian (PC)	Uncompressed	1	\N	\N	2	\N	\N	\N	\N	\N	\N	f	0	44879053	0	library internal use	3120	4800	400	8,8,8	integer	3	0	0	\N	2.2	100	\N	\N	f	\N	\N	\N	\N
784	1809	TIFF 6.0	Little Endian (PC)	Uncompressed	1	\N	\N	2	\N	\N	\N	\N	\N	\N	f	0	45088768	0	library internal use	3132	4800	400	8,8,8	integer	3	0	0	\N	2.2	100	\N	\N	f	\N	\N	\N	\N
785	1810	TIFF 6.0	Little Endian (PC)	Uncompressed	1	\N	\N	2	\N	\N	\N	\N	\N	\N	f	0	75078042	0	library internal use	3134	7989	400	8,8,8	integer	3	0	0	\N	2.2	100	\N	\N	f	\N	\N	\N	\N
786	1811	TIFF 6.0	Little Endian (PC)	Uncompressed	1	\N	\N	2	\N	\N	\N	\N	\N	\N	f	0	38168166	0	library internal use	3348	3800	400	8,8,8	integer	3	0	0	\N	2.2	100	\N	\N	f	\N	\N	\N	\N
787	1812	TIFF 6.0	Little Endian (PC)	Uncompressed	1	\N	\N	2	\N	\N	\N	\N	\N	\N	f	0	27472691	0	library internal use	2458	3721	400	8,8,8	integer	3	0	0	\N	2.2	100	\N	\N	f	\N	\N	\N	\N
788	1813	TIFF 6.0	Little Endian (PC)	Uncompressed	1	\N	\N	2	\N	\N	\N	\N	\N	\N	f	0	70883738	0	library internal use	5600	4217	400	8,8,8	integer	3	0	0	\N	2.2	100	\N	\N	f	\N	\N	\N	\N
789	1814	TIFF 6.0	Little Endian (PC)	Uncompressed	1	\N	\N	2	\N	\N	\N	\N	\N	\N	f	0	35966157	1	library internal use	2858	4200	400	8,8,8	integer	3	0	7	\N	2.2	100	\N	\N	f	\N	\N	\N	\N
790	1815	TIFF 6.0	Little Endian (PC)	Uncompressed	1	\N	\N	2	\N	\N	\N	\N	\N	\N	f	0	36385587	1	library internal use	2908	4175	400	8,8,8	integer	3	0	7	\N	2.2	100	\N	\N	f	\N	\N	\N	\N
791	1816	TIFF 6.0	Little Endian (PC)	Uncompressed	1	\N	\N	2	\N	\N	\N	\N	\N	\N	f	0	36071014	0	library internal use	2867	4192	400	8,8,8	integer	3	0	0	\N	2.2	100	\N	\N	f	\N	\N	\N	\N
792	1817	TIFF 6.0	Little Endian (PC)	Uncompressed	1	\N	\N	2	\N	\N	\N	\N	\N	\N	f	0	54001664	1	library internal use	3683	4892	400	8,8,8	integer	3	0	7	\N	2.2	100	\N	\N	f	\N	\N	\N	\N
793	1818	TIFF 6.0	Little Endian (PC)	Uncompressed	1	\N	\N	2	\N	\N	\N	\N	\N	\N	f	0	56098816	1	library internal use	3767	4967	400	8,8,8	integer	3	0	7	\N	2.2	100	\N	\N	f	\N	\N	\N	\N
794	1819	TIFF 6.0	Little Endian (PC)	Uncompressed	1	\N	\N	2	\N	\N	\N	\N	\N	\N	f	0	68891443	0	library internal use	5558	4133	400	8,8,8	integer	3	0	0	\N	2.2	100	\N	\N	f	\N	\N	\N	\N
795	1820	TIFF 6.0	Little Endian (PC)	Uncompressed	1	\N	\N	2	\N	\N	\N	\N	\N	\N	f	0	109890765	0	library internal use	6990	5240	400	8,8,8	integer	3	0	7	\N	2.2	100	\N	\N	f	\N	\N	\N	\N
796	1821	TIFF 6.0	Little Endian (PC)	Uncompressed	1	\N	\N	2	\N	\N	\N	\N	\N	\N	f	0	55889101	0	library internal use	3552	5240	400	8,8,8	integer	3	0	7	\N	2.2	100	\N	\N	f	\N	\N	\N	\N
797	1822	TIFF 6.0	Little Endian (PC)	Uncompressed	1	\N	\N	2	\N	\N	\N	\N	\N	\N	f	0	53267661	1	library internal use	3500	5073	400	8,8,8	integer	3	0	7	\N	2.2	100	\N	\N	f	\N	\N	\N	\N
798	1823	TIFF 6.0	Little Endian (PC)	Uncompressed	1	\N	\N	2	\N	\N	\N	\N	\N	\N	f	0	105172173	3	library internal use	6854	5115	400	8,8,8	integer	3	0	7	\N	2.2	100	\N	\N	f	\N	\N	\N	\N
799	1824	TIFF 6.0	Little Endian (PC)	Uncompressed	1	\N	\N	2	\N	\N	\N	\N	\N	\N	f	0	56098816	1	library internal use	3552	5260	400	8,8,8	integer	3	0	7	\N	2.2	100	\N	\N	f	\N	\N	\N	\N
800	1825	TIFF 6.0	Little Endian (PC)	Uncompressed	1	\N	\N	2	\N	\N	\N	\N	\N	\N	f	0	41628467	1	library internal use	3073	4510	400	8,8,8	integer	3	0	7	\N	2.2	100	\N	\N	f	\N	\N	\N	\N
801	1827	TIFF 6.0	Little Endian (PC)	Uncompressed	1	\N	\N	2	\N	\N	\N	\N	\N	\N	f	0	8503951	2	patron request	912	3110	300	8,8,8	integer	3	0	7	\N	2.2	100	\N	2006-07-31 00:00:00	f	\N	\N	\N	\N
802	1828	TIFF 6.0	Little Endian (PC)	Uncompressed	1	\N	\N	2	\N	\N	\N	\N	\N	\N	f	0	70254592	1	library internal use	4271	5479	400	8,8,8	integer	3	0	7	\N	2.2	100	\N	\N	f	\N	\N	\N	\N
803	1829	TIFF 6.0	Little Endian (PC)	Uncompressed	1	\N	\N	2	\N	\N	\N	\N	\N	\N	f	0	82208358	0	library internal use	5792	4729	400	8,8,8	integer	3	0	7	\N	2.2	100	\N	\N	f	\N	\N	\N	\N
804	1830	TIFF 6.0	Little Endian (PC)	Uncompressed	1	\N	\N	2	\N	\N	\N	\N	\N	\N	f	0	142186906	0	library internal use	8396	5646	400	8,8,8	integer	3	0	7	\N	2.2	100	\N	\N	f	\N	\N	\N	\N
805	1831	TIFF 6.0	Little Endian (PC)	Uncompressed	1	\N	\N	2	\N	\N	\N	\N	\N	\N	f	0	74658611	0	library internal use	4427	5625	400	8,8,8	integer	3	0	7	\N	2.2	100	\N	\N	f	\N	\N	\N	\N
806	1832	TIFF 6.0	Little Endian (PC)	Uncompressed	1	\N	\N	2	\N	\N	\N	\N	\N	\N	f	0	89653248	0	library internal use	4865	6146	400	8,8,8	integer	3	0	7	\N	2.2	100	\N	\N	f	\N	\N	\N	\N
807	1833	TIFF 6.0	Little Endian (PC)	Uncompressed	1	\N	\N	2	\N	\N	\N	\N	\N	\N	f	0	15309210	1	library internal use	2021	2521	500	8,8,8	integer	3	0	7	\N	2.2	100	\N	\N	f	\N	\N	\N	\N
808	1834	TIFF 6.0	Little Endian (PC)	Uncompressed	1	\N	\N	2	\N	\N	\N	\N	\N	\N	f	0	83886080	1	library internal use	6083	4594	400	8,8,8	integer	3	0	7	\N	2.2	100	\N	\N	f	\N	\N	\N	\N
809	1835	TIFF 6.0	Little Endian (PC)	Uncompressed	1	\N	\N	2	\N	\N	\N	\N	\N	\N	f	0	44040192	1	library internal use	3177	4625	400	8,8,8	integer	3	0	7	\N	2.2	100	\N	\N	f	\N	\N	\N	\N
810	1836	TIFF 6.0	Little Endian (PC)	Uncompressed	1	\N	\N	2	\N	\N	\N	\N	\N	\N	f	0	58615398	1	library internal use	3885	5031	400	8,8,8	integer	3	0	7	\N	2.2	100	\N	\N	f	\N	\N	\N	\N
811	1837	TIFF 6.0	Little Endian (PC)	Uncompressed	1	\N	\N	2	\N	\N	\N	\N	\N	\N	f	0	51799654	0	library internal use	4740	3646	400	8,8,8	integer	3	0	7	\N	2.2	100	\N	\N	f	\N	\N	\N	\N
812	1838	TIFF 6.0	Little Endian (PC)	Uncompressed	1	\N	\N	2	\N	\N	\N	\N	\N	\N	f	0	124256256	0	library internal use	5531	7490	400	8,8,8	integer	3	0	7	\N	2.2	100	\N	\N	f	\N	\N	\N	\N
813	1839	TIFF 6.0	Little Endian (PC)	Uncompressed	1	\N	\N	2	\N	\N	\N	\N	\N	\N	f	0	123522253	0	library internal use	5521	7458	400	8,8,8	integer	3	0	7	\N	2.2	100	\N	\N	f	\N	\N	\N	\N
814	1840	TIFF 6.0	Little Endian (PC)	Uncompressed	1	\N	\N	2	\N	\N	\N	\N	\N	\N	f	0	85458944	0	library internal use	4646	6135	400	8,8,8	integer	3	0	7	\N	2.2	100	\N	\N	f	\N	\N	\N	\N
815	1841	TIFF 6.0	Little Endian (PC)	Uncompressed	1	\N	\N	2	\N	\N	\N	\N	\N	\N	f	0	108213043	0	library internal use	6969	5177	400	8,8,8	integer	3	0	7	\N	2.2	100	\N	\N	f	\N	\N	\N	\N
816	1842	TIFF 6.0	Little Endian (PC)	Uncompressed	1	\N	\N	2	\N	\N	\N	\N	\N	\N	f	0	83256934	0	library internal use	7125	3896	400	8,8,8	integer	3	0	7	\N	2.2	100	\N	\N	f	\N	\N	\N	\N
817	1843	TIFF 6.0	Little Endian (PC)	Uncompressed	1	\N	\N	2	\N	\N	\N	\N	\N	\N	f	0	44459622	0	library internal use	3135	4729	400	8,8,8	integer	3	0	7	\N	2.2	100	\N	\N	f	\N	\N	\N	\N
818	1844	TIFF 6.0	Little Endian (PC)	Uncompressed	1	\N	\N	2	\N	\N	\N	\N	\N	\N	f	0	56937677	1	library internal use	3917	4844	400	8,8,8	integer	3	0	7	\N	2.2	100	\N	\N	f	\N	\N	\N	\N
819	1845	TIFF 6.0	Little Endian (PC)	Uncompressed	1	\N	\N	2	\N	\N	\N	\N	\N	\N	f	0	27158118	0	library internal use	6219	1458	400	8,8,8	integer	3	0	7	\N	2.2	100	\N	\N	f	\N	\N	\N	\N
820	1846	TIFF 6.0	Little Endian (PC)	Uncompressed	1	\N	\N	2	\N	\N	\N	\N	\N	\N	f	0	28101837	0	library internal use	6156	1521	400	8,8,8	integer	3	0	7	\N	2.2	100	\N	\N	f	\N	\N	\N	\N
821	1847	TIFF 6.0	Little Endian (PC)	Uncompressed	1	\N	\N	2	\N	\N	\N	\N	\N	\N	f	0	57776538	0	library internal use	3604	5344	400	8,8,8	integer	3	0	7	\N	2.2	100	\N	\N	f	\N	\N	\N	\N
822	1848	TIFF 6.0	Little Endian (PC)	Uncompressed	1	\N	\N	2	\N	\N	\N	\N	\N	\N	f	0	57776538	1	library internal use	3604	5344	500	8,8,8	integer	3	0	7	\N	2.2	100	\N	\N	f	\N	\N	\N	\N
823	1850	TIFF 6.0	Little Endian (PC)	Uncompressed	1	\N	\N	2	\N	\N	\N	\N	\N	\N	f	0	16148070	0	library internal use	1915	2806	400	8,8,8	integer	3	0	0	\N	2.2	100	\N	\N	f	\N	\N	\N	\N
824	1851	TIFF 6.0	Little Endian (PC)	Uncompressed	1	\N	\N	2	\N	\N	\N	\N	\N	\N	f	0	27158118	0	library internal use	2458	3686	400	8,8,8	integer	3	0	0	\N	2.2	100	\N	\N	f	\N	\N	\N	\N
825	1852	TIFF 6.0	Little Endian (PC)	Uncompressed	1	\N	\N	2	\N	\N	\N	\N	\N	\N	f	0	40265318	0	library internal use	3208	4183	400	8,8,8	integer	3	0	0	\N	2.2	100	\N	\N	f	\N	\N	\N	\N
826	1853	TIFF 6.0	Little Endian (PC)	Uncompressed	1	\N	\N	2	\N	\N	\N	\N	\N	\N	f	0	19922944	0	library internal use	2005	3320	400	8,8,8	integer	3	0	0	\N	2.2	100	\N	\N	f	\N	\N	\N	\N
827	1854	TIFF 6.0	Little Endian (PC)	Uncompressed	1	\N	\N	2	\N	\N	\N	\N	\N	\N	f	0	19188941	0	library internal use	3211	1995	400	8,8,8	integer	3	0	0	\N	2.2	100	\N	\N	f	\N	\N	\N	\N
828	1855	TIFF 6.0	Little Endian (PC)	Uncompressed	1	\N	\N	2	\N	\N	\N	\N	\N	\N	f	0	13736346	0	library internal use	1726	2654	400	8,8,8	integer	3	0	0	\N	2.2	100	\N	\N	f	\N	\N	\N	\N
829	1856	TIFF 6.0	Little Endian (PC)	Uncompressed	1	\N	\N	2	\N	\N	\N	\N	\N	\N	f	0	76650906	0	library internal use	5604	4560	400	8,8,8	integer	3	0	0	\N	2.2	100	\N	\N	f	\N	\N	\N	\N
830	1857	TIFF 6.0	Little Endian (PC)	Uncompressed	1	\N	\N	2	\N	\N	\N	\N	\N	\N	f	0	25899827	0	library internal use	4394	1962	400	8,8,8	integer	3	0	0	\N	2.2	100	\N	\N	f	\N	\N	\N	\N
831	1858	TIFF 6.0	Little Endian (PC)	Uncompressed	1	\N	\N	2	\N	\N	\N	\N	\N	\N	f	0	23907533	0	library internal use	2223	3582	400	8,8,8	integer	3	0	0	\N	2.2	100	\N	\N	f	\N	\N	\N	\N
832	1859	TIFF 6.0	Little Endian (PC)	Uncompressed	1	\N	\N	2	\N	\N	\N	\N	\N	\N	f	0	12058624	0	library internal use	2005	2004	400	8,8,8	integer	3	0	0	\N	2.2	100	\N	\N	f	\N	\N	\N	\N
833	1860	TIFF 6.0	Little Endian (PC)	Uncompressed	1	\N	\N	2	\N	\N	\N	\N	\N	\N	f	0	100243866	0	library internal use	4915	6800	400	8,8,8	integer	3	0	0	\N	2.2	100	\N	\N	f	\N	\N	\N	\N
834	1861	TIFF 6.0	Little Endian (PC)	Uncompressed	1	\N	\N	2	\N	\N	\N	\N	\N	\N	f	0	3995075	0	library internal use	1316	1011	400	8,8,8	integer	3	0	0	\N	2.2	100	\N	\N	f	\N	\N	\N	\N
835	1862	TIFF 6.0	Little Endian (PC)	Uncompressed	1	\N	\N	2	\N	\N	\N	\N	\N	\N	f	0	2956984	0	library internal use	1316	749	400	8,8,8	integer	3	0	0	\N	2.2	100	\N	\N	f	\N	\N	\N	\N
836	1863	TIFF 6.0	Little Endian (PC)	Uncompressed	1	\N	\N	2	\N	\N	\N	\N	\N	\N	f	0	24956109	0	library internal use	2249	3704	400	8,8,8	integer	3	0	0	\N	2.2	100	\N	\N	f	\N	\N	\N	\N
837	1864	TIFF 6.0	Little Endian (PC)	Uncompressed	1	\N	\N	2	\N	\N	\N	\N	\N	\N	f	0	32296141	0	library internal use	2680	4018	400	8,8,8	integer	3	0	0	\N	2.2	100	\N	\N	f	\N	\N	\N	\N
838	1865	TIFF 6.0	Little Endian (PC)	Uncompressed	1	\N	\N	2	\N	\N	\N	\N	\N	\N	f	0	22754099	0	library internal use	3588	2114	400	8,8,8	integer	3	0	0	\N	2.2	100	\N	\N	f	\N	\N	\N	\N
839	1866	TIFF 6.0	Little Endian (PC)	Uncompressed	1	\N	\N	2	\N	\N	\N	\N	\N	\N	f	0	9017754	0	library internal use	2200	1367	400	8,8,8	integer	3	0	7	\N	2.2	100	\N	\N	f	\N	\N	\N	\N
840	1867	TIFF 6.0	Little Endian (PC)	Uncompressed	1	\N	\N	2	\N	\N	\N	\N	\N	\N	f	0	37014733	0	library internal use	2908	4242	400	8,8,8	integer	3	0	7	\N	2.2	100	\N	\N	f	\N	\N	\N	\N
841	1868	TIFF 6.0	Little Endian (PC)	Uncompressed	1	\N	\N	2	\N	\N	\N	\N	\N	\N	f	0	38587597	0	library internal use	3150	4083	400	8,8,8	integer	3	0	7	\N	2.2	100	\N	\N	f	\N	\N	\N	\N
842	1869	TIFF 6.0	Little Endian (PC)	Uncompressed	1	\N	\N	2	\N	\N	\N	\N	\N	\N	f	0	59139686	0	library internal use	3917	5033	400	8,8,8	integer	3	0	7	\N	2.2	100	\N	\N	f	\N	\N	\N	\N
843	1870	TIFF 6.0	Little Endian (PC)	Uncompressed	1	\N	\N	2	\N	\N	\N	\N	\N	\N	f	0	35966157	0	library internal use	2858	4200	400	8,8,8	integer	3	0	7	\N	2.2	100	\N	\N	f	\N	\N	\N	\N
844	1871	TIFF 6.0	Little Endian (PC)	Uncompressed	1	\N	\N	2	\N	\N	\N	\N	\N	\N	f	0	54735667	0	library internal use	3733	4892	400	8,8,8	integer	3	0	0	\N	2.2	100	\N	\N	f	\N	\N	\N	\N
845	1872	TIFF 6.0	Little Endian (PC)	Uncompressed	1	\N	\N	2	\N	\N	\N	\N	\N	\N	f	0	24851251	0	library internal use	2358	3517	400	8,8,8	integer	3	0	0	\N	2.2	100	\N	\N	f	\N	\N	\N	\N
846	1873	TIFF 6.0	Little Endian (PC)	Uncompressed	1	\N	\N	2	\N	\N	\N	\N	\N	\N	f	0	73295462	0	library internal use	4292	5692	400	8,8,8	integer	3	0	7	\N	2.2	100	\N	\N	f	\N	\N	\N	\N
847	1874	TIFF 6.0	Little Endian (PC)	Uncompressed	1	\N	\N	2	\N	\N	\N	\N	\N	\N	f	0	73714893	0	library internal use	4292	5725	400	8,8,8	integer	3	0	7	\N	2.2	100	\N	\N	f	\N	\N	\N	\N
848	1875	TIFF 6.0	Little Endian (PC)	Uncompressed	1	\N	\N	2	\N	\N	\N	\N	\N	\N	f	0	54945382	0	library internal use	4892	3742	400	8,8,8	integer	3	0	7	\N	2.2	100	\N	\N	f	\N	\N	\N	\N
849	1876	TIFF 6.0	Little Endian (PC)	Uncompressed	1	\N	\N	2	\N	\N	\N	\N	\N	\N	f	0	52428800	0	library internal use	3600	4858	400	8,8,8	integer	3	0	0	\N	2.2	100	\N	\N	f	\N	\N	\N	\N
850	1877	TIFF 6.0	Little Endian (PC)	Uncompressed	1	\N	\N	2	\N	\N	\N	\N	\N	\N	f	0	89024102	0	library internal use	6367	4658	400	8,8,8	integer	3	0	0	\N	2.2	100	\N	\N	f	\N	\N	\N	\N
851	1878	TIFF 6.0	Little Endian (PC)	Uncompressed	1	\N	\N	2	\N	\N	\N	\N	\N	\N	f	0	72980890	0	library internal use	4342	5600	400	8,8,8	integer	3	0	7	\N	2.2	100	\N	\N	f	\N	\N	\N	\N
852	1879	TIFF 6.0	Little Endian (PC)	Uncompressed	1	\N	\N	2	\N	\N	\N	\N	\N	\N	f	0	75182899	0	library internal use	4383	5717	400	8,8,8	integer	3	0	7	\N	2.2	100	\N	\N	f	\N	\N	\N	\N
853	1880	TIFF 6.0	Little Endian (PC)	Uncompressed	1	\N	\N	2	\N	\N	\N	\N	\N	\N	f	0	73295462	0	library internal use	4383	5575	400	8,8,8	integer	3	0	7	\N	2.2	100	\N	\N	f	\N	\N	\N	\N
854	1881	TIFF 6.0	Little Endian (PC)	Uncompressed	1	\N	\N	2	\N	\N	\N	\N	\N	\N	f	0	71827456	0	library internal use	4317	5550	400	8,8,8	integer	3	0	7	\N	2.2	100	\N	\N	f	\N	\N	\N	\N
855	1882	TIFF 6.0	Little Endian (PC)	Uncompressed	1	\N	\N	2	\N	\N	\N	\N	\N	\N	f	0	73819750	0	library internal use	4375	5625	400	8,8,8	integer	3	0	0	\N	2.2	100	\N	\N	f	\N	\N	\N	\N
856	1883	TIFF 6.0	Little Endian (PC)	Uncompressed	1	\N	\N	2	\N	\N	\N	\N	\N	\N	f	0	315621356	1	library internal use	2711	3878	400	8,8,8	integer	3	0	7	\N	2.2	100	\N	\N	f	\N	\N	\N	\N
857	1884	TIFF 6.0	Little Endian (PC)	Uncompressed	1	\N	\N	2	\N	\N	\N	\N	\N	\N	f	0	5253366	1	library internal use	1101	1590	400	8,8,8	integer	3	0	7	\N	2.2	100	\N	\N	f	\N	\N	\N	\N
858	1885	TIFF 6.0	Little Endian (PC)	Uncompressed	1	\N	\N	2	\N	\N	\N	\N	\N	\N	f	0	37643878	0	library internal use	3365	3730	400	8,8,8	integer	3	0	7	\N	2.2	100	\N	\N	f	\N	\N	\N	\N
859	1886	TIFF 6.0	Little Endian (PC)	Uncompressed	1	\N	\N	2	\N	\N	\N	\N	\N	\N	f	0	31562138	0	library internal use	2685	3922	400	8,8,8	integer	3	0	0	\N	2.2	100	\N	\N	f	\N	\N	\N	\N
860	1887	TIFF 6.0	Little Endian (PC)	Uncompressed	1	\N	\N	2	\N	\N	\N	\N	\N	\N	f	0	44669338	0	library internal use	3400	4384	400	8,8,8	integer	3	0	0	\N	2.2	100	\N	\N	f	\N	\N	\N	\N
861	1888	TIFF 6.0	Little Endian (PC)	Uncompressed	1	\N	\N	2	\N	\N	\N	\N	\N	\N	f	0	35966157	0	library internal use	2724	4401	400	8,8,8	integer	3	0	0	\N	2.2	100	\N	\N	f	\N	\N	\N	\N
862	1889	TIFF 6.0	Little Endian (PC)	Uncompressed	1	\N	\N	2	\N	\N	\N	\N	\N	\N	f	0	24746394	0	library internal use	2585	3188	400	8,8,8	integer	3	0	0	\N	2.2	100	\N	\N	f	\N	\N	\N	\N
863	1890	TIFF 6.0	Little Endian (PC)	Uncompressed	1	\N	\N	2	\N	\N	\N	\N	\N	\N	f	0	47081062	0	library internal use	3281	4781	400	8,8,8	integer	3	0	0	\N	2.2	100	\N	\N	f	\N	\N	\N	\N
864	1891	TIFF 6.0	Little Endian (PC)	Uncompressed	1	\N	\N	2	\N	\N	\N	\N	\N	\N	f	0	46871347	0	library internal use	4394	3553	400	8,8,8	integer	3	0	0	\N	2.2	100	\N	\N	f	\N	\N	\N	\N
865	1892	TIFF 6.0	Little Endian (PC)	Uncompressed	1	\N	\N	2	\N	\N	\N	\N	\N	\N	f	0	46661632	0	library internal use	3391	4584	400	8,8,8	integer	3	0	0	\N	2.2	100	\N	\N	f	\N	\N	\N	\N
866	1893	TIFF 6.0	Little Endian (PC)	Uncompressed	1	\N	\N	2	\N	\N	\N	\N	\N	\N	f	0	43515904	0	library internal use	3348	4221	400	8,8,8	integer	3	0	0	\N	2.2	100	\N	\N	f	\N	\N	\N	\N
867	1894	TIFF 6.0	Little Endian (PC)	Uncompressed	1	\N	\N	2	\N	\N	\N	\N	\N	\N	f	0	32925286	0	library internal use	2498	4394	400	8,8,8	integer	3	0	0	\N	2.2	100	\N	\N	f	\N	\N	\N	\N
868	1895	TIFF 6.0	Little Endian (PC)	Uncompressed	1	\N	\N	2	\N	\N	\N	\N	\N	\N	f	0	38482739	0	library internal use	3199	4009	400	8,8,8	integer	3	0	0	\N	2.2	100	\N	\N	f	\N	\N	\N	\N
869	1896	TIFF 6.0	Little Endian (PC)	Uncompressed	1	\N	\N	2	\N	\N	\N	\N	\N	\N	f	0	33344717	0	library internal use	4406	2522	400	8,8,8	integer	3	0	0	\N	2.2	100	\N	\N	f	\N	\N	\N	\N
870	1897	TIFF 6.0	Little Endian (PC)	Uncompressed	1	\N	\N	2	\N	\N	\N	\N	\N	\N	f	0	42572186	0	library internal use	3230	4392	400	8,8,8	integer	3	0	0	\N	2.2	100	\N	\N	f	\N	\N	\N	\N
871	1898	TIFF 6.0	Little Endian (PC)	Uncompressed	1	\N	\N	2	\N	\N	\N	\N	\N	\N	f	0	100873011	0	library internal use	4949	6796	400	8,8,8	integer	3	0	0	\N	2.2	100	\N	\N	f	\N	\N	\N	\N
872	1899	TIFF 6.0	Little Endian (PC)	Uncompressed	1	\N	\N	2	\N	\N	\N	\N	\N	\N	f	0	12792627	0	library internal use	1717	2493	400	8,8,8	integer	3	0	0	\N	2.2	100	\N	\N	f	\N	\N	\N	\N
873	1900	TIFF 6.0	Little Endian (PC)	Uncompressed	1	\N	\N	2	\N	\N	\N	\N	\N	\N	f	0	13421773	0	library internal use	1744	2571	400	8,8,8	integer	3	0	0	\N	2.2	100	\N	\N	f	\N	\N	\N	\N
874	1901	TIFF 6.0	Little Endian (PC)	Uncompressed	1	\N	\N	2	\N	\N	\N	\N	\N	\N	f	0	16252928	0	library internal use	2841	11901	400	8,8,8	integer	3	0	0	\N	2.2	100	\N	\N	f	\N	\N	\N	\N
875	1902	TIFF 6.0	Little Endian (PC)	Uncompressed	1	\N	\N	2	\N	\N	\N	\N	\N	\N	f	0	8168407	0	library internal use	846	3192	400	8,8,8	integer	3	0	0	\N	2.2	100	\N	\N	f	\N	\N	\N	\N
876	1903	TIFF 6.0	Little Endian (PC)	Uncompressed	1	\N	\N	2	\N	\N	\N	\N	\N	\N	f	0	24746394	0	library internal use	2780	3304	400	8,8,8	integer	3	0	0	\N	2.2	100	\N	\N	f	\N	\N	\N	\N
877	1904	TIFF 6.0	Little Endian (PC)	Uncompressed	1	\N	\N	2	\N	\N	\N	\N	\N	\N	f	0	27472691	0	library internal use	2798	3278	400	8,8,8	integer	3	0	0	\N	2.2	100	\N	\N	f	\N	\N	\N	\N
878	1905	TIFF 6.0	Little Endian (PC)	Uncompressed	1	\N	\N	2	\N	\N	\N	\N	\N	\N	f	0	11639194	0	library internal use	2188	1778	400	8,8,8	integer	3	0	0	\N	2.2	100	\N	\N	f	\N	\N	\N	\N
879	1906	TIFF 6.0	Little Endian (PC)	Uncompressed	1	\N	\N	2	\N	\N	\N	\N	\N	\N	f	0	24746394	0	library internal use	2328	3538	400	8,8,8	integer	3	0	0	\N	2.2	100	\N	\N	f	\N	\N	\N	\N
880	1907	TIFF 6.0	Little Endian (PC)	Uncompressed	1	\N	\N	2	\N	\N	\N	\N	\N	\N	f	0	48339354	0	library internal use	4793	3361	400	8,8,8	integer	3	0	0	\N	2.2	100	\N	\N	f	\N	\N	\N	\N
881	1908	TIFF 6.0	Little Endian (PC)	Uncompressed	1	\N	\N	2	\N	\N	\N	\N	\N	\N	f	0	31562138	0	library internal use	2630	3998	400	8,8,8	integer	3	0	0	\N	2.2	100	\N	\N	f	\N	\N	\N	\N
882	1909	TIFF 6.0	Little Endian (PC)	Uncompressed	1	\N	\N	2	\N	\N	\N	\N	\N	\N	f	0	19293798	0	library internal use	1979	3251	400	8,8,8	integer	3	0	0	\N	2.2	100	\N	\N	f	\N	\N	\N	\N
883	1910	TIFF 6.0	Little Endian (PC)	Uncompressed	1	\N	\N	2	\N	\N	\N	\N	\N	\N	f	0	19818086	1	library internal use	2014	3277	400	8,8,8	integer	3	0	7	\N	2.2	100	\N	\N	f	\N	\N	\N	\N
884	1911	TIFF 6.0	Little Endian (PC)	Uncompressed	1	\N	\N	2	\N	\N	\N	\N	\N	\N	f	0	173853901	1	library internal use	9614	6029	400	8,8,8	integer	3	0	0	\N	2.2	100	\N	\N	f	\N	\N	\N	\N
885	1912	TIFF 6.0	Little Endian (PC)	Uncompressed	1	\N	\N	2	\N	\N	\N	\N	\N	\N	f	0	37853594	1	library internal use	2865	4409	400	8,8,8	integer	3	0	0	\N	2.2	100	\N	\N	f	\N	\N	\N	\N
886	1913	TIFF 6.0	Little Endian (PC)	Uncompressed	1	\N	\N	2	\N	\N	\N	\N	\N	\N	f	0	46137344	0	library internal use	4671	3295	400	8,8,8	integer	3	0	7	\N	2.2	100	\N	\N	f	\N	\N	\N	\N
887	1914	TIFF 6.0	Little Endian (PC)	Uncompressed	1	\N	\N	2	\N	\N	\N	\N	\N	\N	f	0	12792627	1	library internal use	1386	3071	400	8,8,8	integer	3	0	7	\N	2.2	100	\N	\N	f	\N	\N	\N	\N
888	1915	TIFF 6.0	Little Endian (PC)	Uncompressed	1	\N	\N	2	\N	\N	\N	\N	\N	\N	f	0	13316915	1	library internal use	1404	3160	400	8,8,8	integer	3	0	7	\N	2.2	100	\N	\N	f	\N	\N	\N	\N
889	1916	TIFF 6.0	Little Endian (PC)	Uncompressed	1	\N	\N	2	\N	\N	\N	\N	\N	\N	f	0	60817408	0	library internal use	4103	4944	400	8,8,8	integer	3	0	0	\N	2.2	100	\N	\N	f	\N	\N	\N	\N
890	1917	TIFF 6.0	Big Endian (Mac)	Uncompressed	1	\N	\N	2	\N	\N	\N	\N	\N	\N	f	0	15099494	2	library internal use	2036	2472	300	8,8,8	integer	3	0	7	\N	2.2	\N	\N	\N	f	\N	\N	\N	\N
891	1918	TIFF 6.0	Big Endian (Mac)	Uncompressed	1	\N	\N	2	\N	\N	\N	\N	\N	\N	f	0	62285414	2	library internal use	4200	4944	300	8,8,8	integer	3	0	7	\N	2.2	\N	\N	\N	f	\N	\N	\N	\N
892	1919	TIFF 6.0	Little Endian (PC)	Uncompressed	1	\N	\N	2	\N	\N	\N	\N	\N	\N	f	0	62075699	0	library internal use	4119	5024	400	8,8,8	integer	3	0	0	\N	2.2	100	\N	\N	f	\N	\N	\N	\N
893	1920	TIFF 6.0	Little Endian (PC)	Uncompressed	1	\N	\N	2	\N	\N	\N	\N	\N	\N	f	0	60817408	0	library internal use	4103	4944	400	8,8,8	integer	3	0	0	\N	2.2	100	\N	\N	f	\N	\N	\N	\N
894	1921	TIFF 6.0	Little Endian (PC)	Uncompressed	1	\N	\N	2	\N	\N	\N	\N	\N	\N	f	0	60188262	0	library internal use	4066	4936	400	8,8,8	integer	3	0	0	\N	2.2	100	\N	\N	f	\N	\N	\N	\N
895	1922	TIFF 6.0	Little Endian (PC)	Uncompressed	1	\N	\N	2	\N	\N	\N	\N	\N	\N	f	0	60188262	0	library internal use	4066	4936	400	8,8,8	integer	3	0	0	\N	2.2	100	\N	\N	f	\N	\N	\N	\N
896	1923	TIFF 6.0	Little Endian (PC)	Uncompressed	1	\N	\N	2	\N	\N	\N	\N	\N	\N	f	0	60188262	0	library internal use	4066	4936	400	8,8,8	integer	3	0	0	\N	2.2	100	\N	\N	f	\N	\N	\N	\N
897	1924	TIFF 6.0	Little Endian (PC)	Uncompressed	1	\N	\N	2	\N	\N	\N	\N	\N	\N	f	0	60188262	0	library internal use	4066	4936	400	8,8,8	integer	3	0	0	\N	2.2	100	\N	\N	f	\N	\N	\N	\N
898	1925	TIFF 6.0	Little Endian (PC)	Uncompressed	1	\N	\N	2	\N	\N	\N	\N	\N	\N	f	0	23697818	1	library internal use	2345	3373	400	8,8,8	integer	3	0	7	\N	2.2	100	\N	\N	f	\N	\N	\N	\N
899	1926	TIFF 6.0	Little Endian (PC)	Uncompressed	1	\N	\N	2	\N	\N	\N	\N	\N	\N	f	0	6595543	0	library internal use	2243	2941	400	8,8,8	integer	3	0	7	\N	2.2	100	\N	\N	f	\N	\N	\N	\N
900	1927	TIFF 6.0	Little Endian (PC)	Uncompressed	1	\N	\N	2	\N	\N	\N	\N	\N	\N	f	0	12792627	0	library internal use	3974	3217	400	8,8,8	integer	3	0	0	\N	2.2	100	\N	\N	f	\N	\N	\N	\N
901	1928	TIFF 6.0	Little Endian (PC)	Uncompressed	1	\N	\N	2	\N	\N	\N	\N	\N	\N	f	0	12897485	1	library internal use	3965	3243	400	8,8,8	integer	3	0	7	\N	2.2	100	Image was scanned in grayscale.	\N	f	\N	\N	\N	\N
902	1929	TIFF 6.0	Little Endian (PC)	Uncompressed	1	\N	\N	2	\N	\N	\N	\N	\N	\N	f	0	16882074	1	library internal use	1995	2827	400	8,8,8	integer	3	0	7	\N	2.2	100	\N	\N	f	\N	\N	\N	\N
903	1930	TIFF 6.0	Little Endian (PC)	Uncompressed	1	\N	\N	2	\N	\N	\N	\N	\N	\N	f	0	11429478	1	library internal use	3780	3030	400	8,8,8	integer	3	0	7	\N	2.2	100	\N	\N	f	\N	\N	\N	\N
904	1931	TIFF 6.0	Little Endian (PC)	Uncompressed	1	\N	\N	2	\N	\N	\N	\N	\N	\N	f	0	5389681	1	library internal use	1194	1505	150	8,8,8	integer	3	0	7	\N	2.2	100	\N	\N	f	\N	\N	\N	\N
905	1932	TIFF 6.0	Little Endian (PC)	Uncompressed	1	\N	\N	2	\N	\N	\N	\N	\N	\N	f	0	33764147	0	library internal use	3743	3005	400	8,8,8	integer	3	0	0	\N	2.2	100	\N	\N	f	\N	\N	\N	\N
906	1933	TIFF 6.0	Little Endian (PC)	Uncompressed	1	\N	\N	2	\N	\N	\N	\N	\N	\N	f	0	49492787	0	library internal use	3612	4566	400	8,8,8	integer	3	0	0	\N	2.2	100	\N	\N	f	\N	\N	\N	\N
907	1	TIFF 6.0	Little Endian (PC)	Uncompressed	1	\N	\N	2	\N	\N	\N	\N	\N	\N	f	0	0	3	library internal use	0	0	400	8,8,8	integer	3	0	1	\N	2.2	100	\N	\N	f	\N	\N	\N	\N
908	1934	TIFF 6.0	Little Endian (PC)	Uncompressed	1	\N	\N	2	\N	\N	\N	\N	\N	\N	f	0	139355750	3	library internal use	7897	5883	400	8,8,8	integer	3	0	7	\N	2.2	100	\N	2006-08-08 00:00:00	f	\N	\N	\N	\N
909	1935	TIFF 6.0	Little Endian (PC)	Uncompressed	1	\N	\N	2	\N	\N	\N	\N	\N	\N	f	0	50226790	3	library internal use	5309	3156	400	8,8,8	integer	3	0	7	\N	2.2	100	\N	2006-08-08 00:00:00	f	\N	\N	\N	\N
910	1936	TIFF 6.0	Little Endian (PC)	Uncompressed	1	\N	\N	2	\N	\N	\N	\N	\N	\N	f	0	104228454	3	library internal use	5107	6800	400	8,8,8	integer	3	0	7	\N	2.2	100	\N	\N	f	\N	\N	\N	\N
911	1937	TIFF 6.0	Little Endian (PC)	Uncompressed	1	\N	\N	2	\N	\N	\N	\N	\N	\N	f	0	139355750	3	library internal use	7897	5883	400	8,8,8	integer	3	0	7	\N	2.2	100	\N	\N	f	\N	\N	\N	\N
912	1938	TIFF 6.0	Little Endian (PC)	Uncompressed	1	\N	\N	2	\N	\N	\N	\N	\N	\N	f	0	15309210	1	library internal use	1882	2720	400	8,8,8	integer	3	0	7	\N	2.2	100	\N	\N	f	\N	\N	\N	\N
913	1939	TIFF 6.0	Little Endian (PC)	Uncompressed	1	\N	\N	2	\N	\N	\N	\N	\N	\N	f	0	20656947	1	library internal use	2136	3225	400	8,8,8	integer	3	0	7	\N	2.2	100	\N	\N	f	\N	\N	\N	\N
914	1940	TIFF 6.0	Little Endian (PC)	Uncompressed	1	\N	\N	2	\N	\N	\N	\N	\N	\N	f	0	12792627	1	library internal use	1596	2669	400	8,8,8	integer	3	0	7	\N	2.2	100	\N	\N	f	\N	\N	\N	\N
915	1940	TIFF 6.0	Little Endian (PC)	Uncompressed	1	\N	\N	2	\N	\N	\N	\N	\N	\N	f	0	12792627	1	library internal use	1596	2669	400	8,8,8	integer	3	0	7	\N	2.2	100	\N	\N	f	\N	\N	\N	\N
916	1940	TIFF 6.0	Little Endian (PC)	Uncompressed	1	\N	\N	2	\N	\N	\N	\N	\N	\N	f	0	12792627	1	library internal use	1596	2669	400	8,8,8	integer	3	0	7	\N	2.2	100	\N	\N	f	\N	\N	\N	\N
917	1940	TIFF 6.0	Little Endian (PC)	Uncompressed	1	\N	\N	2	\N	\N	\N	\N	\N	\N	f	0	12792627	1	library internal use	1596	2669	400	8,8,8	integer	3	0	7	\N	2.2	100	\N	\N	f	\N	\N	\N	\N
918	1941	TIFF 6.0	Little Endian (PC)	Uncompressed	1	\N	\N	2	\N	\N	\N	\N	\N	\N	f	0	13841203	1	library internal use	1696	2719	400	8,8,8	integer	3	0	7	\N	2.2	100	\N	2006-08-09 00:00:00	f	\N	\N	\N	\N
919	1942	TIFF 6.0	Little Endian (PC)	Uncompressed	1	\N	\N	2	\N	\N	\N	\N	\N	\N	f	0	20866662	1	library internal use	2179	3200	400	8,8,8	integer	3	0	1	\N	2.2	100	\N	2006-08-09 00:00:00	f	\N	\N	\N	\N
920	1943	TIFF 6.0	Little Endian (PC)	Uncompressed	1	\N	\N	2	\N	\N	\N	\N	\N	\N	f	0	0	1	library internal use	0	0	400	8,8,8	integer	3	0	1	\N	2.2	100	\N	2006-08-09 00:00:00	f	\N	\N	\N	\N
921	1943	TIFF 6.0	Little Endian (PC)	Uncompressed	1	\N	\N	2	\N	\N	\N	\N	\N	\N	f	0	24326963	1	library internal use	2397	3381	400	8,8,8	integer	3	0	7	\N	2.2	100	\N	2006-08-09 00:00:00	f	\N	\N	\N	\N
922	1944	TIFF 6.0	Little Endian (PC)	Uncompressed	1	\N	\N	2	\N	\N	\N	\N	\N	\N	f	0	10307502	1	library internal use	1011	3399	400	8,8,8	integer	3	0	7	\N	2.2	100	\N	\N	f	\N	\N	\N	\N
923	1945	TIFF 6.0	Little Endian (PC)	Uncompressed	1	\N	\N	2	\N	\N	\N	\N	\N	\N	f	0	19922944	1	library internal use	2136	3111	400	8,8,8	integer	3	0	7	\N	2.2	100	\N	2006-08-09 00:00:00	f	\N	\N	\N	\N
924	1946	TIFF 6.0	Little Endian (PC)	Uncompressed	1	\N	\N	2	\N	\N	\N	\N	\N	\N	f	0	36071014	1	library internal use	2859	4201	400	8,8,8	integer	3	0	5	\N	2.2	100	\N	2006-08-09 00:00:00	f	\N	\N	\N	\N
925	1947	TIFF 6.0	Little Endian (PC)	Uncompressed	1	\N	\N	2	\N	\N	\N	\N	\N	\N	f	0	25899827	1	library internal use	2389	3608	400	8,8,8	integer	3	0	7	\N	2.2	100	\N	2006-08-09 00:00:00	f	\N	\N	\N	\N
926	1948	TIFF 6.0	Little Endian (PC)	Uncompressed	1	\N	\N	2	\N	\N	\N	\N	\N	\N	f	0	18874368	1	library internal use	2075	3033	400	8,8,8	integer	3	0	7	\N	2.2	100	\N	2006-08-09 00:00:00	f	\N	\N	\N	\N
927	1949	TIFF 6.0	Little Endian (PC)	Uncompressed	1	\N	\N	2	\N	\N	\N	\N	\N	\N	f	0	12478054	1	library internal use	1534	2702	400	8,8,8	integer	3	0	7	\N	2.2	100	\N	2006-08-09 00:00:00	f	\N	\N	\N	\N
928	1950	TIFF 6.0	Little Endian (PC)	Uncompressed	1	\N	\N	2	\N	\N	\N	\N	\N	\N	f	0	42781901	1	library internal use	3243	4401	400	8,8,8	integer	3	0	7	\N	2.2	100	\N	2006-08-11 00:00:00	f	\N	\N	\N	\N
929	1951	TIFF 6.0	Little Endian (PC)	Uncompressed	1	\N	\N	2	\N	\N	\N	\N	\N	\N	f	0	44879053	1	library internal use	3383	4419	400	8,8,8	integer	3	0	7	\N	2.2	100	\N	\N	f	\N	\N	\N	\N
930	1952	TIFF 6.0	Little Endian (PC)	Uncompressed	1	\N	\N	2	\N	\N	\N	\N	\N	\N	f	0	26738688	1	library internal use	2415	3686	400	8,8,8	integer	3	0	7	\N	2.2	100	\N	2006-08-11 00:00:00	f	\N	\N	\N	\N
931	1953	TIFF 6.0	Little Endian (PC)	Uncompressed	1	\N	\N	2	\N	\N	\N	\N	\N	\N	f	0	31247565	1	library internal use	2598	4009	400	8,8,8	integer	3	0	7	\N	2.2	100	\N	2006-08-11 00:00:00	f	\N	\N	\N	\N
932	1954	TIFF 6.0	Little Endian (PC)	Uncompressed	1	\N	\N	2	\N	\N	\N	\N	\N	\N	f	0	27262976	1	library internal use	2825	3216	400	8,8,8	integer	3	0	7	\N	2.2	100	\N	2006-08-11 00:00:00	f	\N	\N	\N	\N
933	1955	TIFF 6.0	Little Endian (PC)	Uncompressed	1	\N	\N	2	\N	\N	\N	\N	\N	\N	f	0	22439526	1	library internal use	2206	3390	400	8,8,8	integer	3	0	7	\N	2.2	100	\N	\N	f	\N	\N	\N	\N
934	1956	TIFF 6.0	Little Endian (PC)	Uncompressed	1	\N	\N	2	\N	\N	\N	\N	\N	\N	f	0	25375539	1	library internal use	2371	3564	400	8,8,8	integer	3	0	7	\N	2.2	100	\N	2006-08-11 00:00:00	f	\N	\N	\N	\N
935	1957	TIFF 6.0	Little Endian (PC)	Uncompressed	1	\N	\N	2	\N	\N	\N	\N	\N	\N	f	0	16148070	1	library internal use	1569	3426	400	8,8,8	integer	3	0	7	\N	2.2	100	\N	2006-08-11 00:00:00	f	\N	\N	\N	\N
936	1958	TIFF 6.0	Little Endian (PC)	Uncompressed	1	\N	\N	2	\N	\N	\N	\N	\N	\N	f	0	12058624	1	library internal use	1377	2928	400	8,8,8	integer	3	0	7	\N	2.2	100	\N	2006-08-11 00:00:00	f	\N	\N	\N	\N
937	1959	TIFF 6.0	Little Endian (PC)	Uncompressed	1	\N	\N	2	\N	\N	\N	\N	\N	\N	f	0	45403341	1	library internal use	3304	4584	400	8,8,8	integer	3	0	7	\N	2.2	100	\N	2006-08-11 00:00:00	f	\N	\N	\N	\N
938	1960	TIFF 6.0	Little Endian (PC)	Uncompressed	1	\N	\N	2	\N	\N	\N	\N	\N	\N	f	0	46556774	1	library internal use	3391	4575	400	8,8,8	integer	3	0	7	\N	2.2	100	\N	\N	f	\N	\N	\N	\N
939	1961	TIFF 6.0	Little Endian (PC)	Uncompressed	1	\N	\N	2	\N	\N	\N	\N	\N	\N	f	0	19293798	1	library internal use	2153	2981	400	8,8,8	integer	3	0	7	\N	2.2	100	\N	2006-08-11 00:00:00	f	\N	\N	\N	\N
940	1962	TIFF 6.0	Little Endian (PC)	Uncompressed	1	\N	\N	2	\N	\N	\N	\N	\N	\N	f	0	19713229	1	library internal use	2197	2989	400	8,8,8	integer	3	0	7	\N	2.2	100	\N	2006-08-11 00:00:00	f	\N	\N	\N	\N
941	1963	TIFF 6.0	Little Endian (PC)	Uncompressed	1	\N	\N	2	\N	\N	\N	\N	\N	\N	f	0	19084083	1	library internal use	2214	2867	400	8,8,8	integer	3	0	7	\N	2.2	100	\N	2006-08-11 00:00:00	f	\N	\N	\N	\N
942	1964	TIFF 6.0	Little Endian (PC)	Uncompressed	1	\N	\N	2	\N	\N	\N	\N	\N	\N	f	0	25480397	1	library internal use	2363	3599	400	8,8,8	integer	3	0	7	\N	2.2	100	\N	2006-08-11 00:00:00	f	\N	\N	\N	\N
943	1965	TIFF 6.0	Little Endian (PC)	Uncompressed	1	\N	\N	2	\N	\N	\N	\N	\N	\N	f	0	12582912	1	library internal use	1543	2710	400	8,8,8	integer	3	0	7	\N	2.2	100	\N	\N	f	\N	\N	\N	\N
944	1966	TIFF 6.0	Little Endian (PC)	Uncompressed	1	\N	\N	2	\N	\N	\N	\N	\N	\N	f	0	19713229	1	library internal use	1953	3373	400	8,8,8	integer	3	0	7	\N	2.2	100	\N	\N	f	\N	\N	\N	\N
945	1651	TIFF 6.0	Little Endian (PC)	Uncompressed	1	\N	\N	2	\N	\N	\N	\N	\N	\N	f	0	0	1	library internal use	0	0	400	8,8,8	integer	3	0	7	\N	2.2	\N	\N	\N	f	\N	\N	\N	\N
946	1967	TIFF 6.0	Little Endian (PC)	Uncompressed	1	\N	\N	2	\N	\N	\N	\N	\N	\N	f	0	47710208	1	library internal use	3400	4680	400	8,8,8	integer	3	0	7	\N	2.2	100	\N	2004-08-15 00:00:00	f	\N	\N	\N	\N
947	1968	TIFF 6.0	Little Endian (PC)	Uncompressed	1	\N	\N	2	\N	\N	\N	\N	\N	\N	f	0	24012390	1	library internal use	2371	3371	400	8,8,8	integer	3	0	7	\N	2.2	100	\N	2006-08-12 00:00:00	f	\N	\N	\N	\N
948	1969	TIFF 6.0	Little Endian (PC)	Uncompressed	1	\N	\N	2	\N	\N	\N	\N	\N	\N	f	0	25165824	1	library internal use	2319	3617	400	8,8,8	integer	3	0	7	\N	2.2	100	\N	2006-08-12 00:00:00	f	\N	\N	\N	\N
949	1970	TIFF 6.0	Little Endian (PC)	Uncompressed	1	\N	\N	2	\N	\N	\N	\N	\N	\N	f	0	19188941	1	library internal use	2179	2928	400	8,8,8	integer	3	0	7	\N	2.2	100	\N	\N	f	\N	\N	\N	\N
950	1971	TIFF 6.0	Little Endian (PC)	Uncompressed	1	\N	\N	2	\N	\N	\N	\N	\N	\N	f	0	22020096	1	library internal use	2162	3390	400	8,8,8	integer	3	0	7	\N	2.2	100	\N	2006-08-12 00:00:00	f	\N	\N	\N	\N
951	1971	TIFF 6.0	Little Endian (PC)	Uncompressed	1	\N	\N	2	\N	\N	\N	\N	\N	\N	f	0	22020096	1	library internal use	2162	3390	400	8,8,8	integer	3	0	7	\N	2.2	100	\N	2006-08-12 00:00:00	f	\N	\N	\N	\N
952	1973	TIFF 6.0	Little Endian (PC)	Uncompressed	1	\N	\N	2	\N	\N	\N	\N	\N	\N	f	0	24641536	1	library internal use	2406	3408	400	8,8,8	integer	3	0	7	\N	2.2	100	\N	2006-08-15 00:00:00	f	\N	\N	\N	\N
953	1974	TIFF 6.0	Little Endian (PC)	Uncompressed	1	\N	\N	2	\N	\N	\N	\N	\N	\N	f	0	25375539	1	library internal use	2371	3564	400	8,8,8	integer	3	0	7	\N	2.2	100	\N	2006-08-15 00:00:00	f	\N	\N	\N	\N
954	1975	TIFF 6.0	Little Endian (PC)	Uncompressed	1	\N	\N	2	\N	\N	\N	\N	\N	\N	f	0	30408704	1	library internal use	2668	3800	400	8,8,8	integer	3	0	7	\N	2.2	100	\N	2006-08-15 00:00:00	f	\N	\N	\N	\N
955	1976	TIFF 6.0	Little Endian (PC)	Uncompressed	1	\N	\N	2	\N	\N	\N	\N	\N	\N	f	0	47710208	1	library internal use	3400	4680	400	8,8,8	integer	3	0	7	\N	2.2	100	\N	2006-08-15 00:00:00	f	\N	\N	\N	\N
956	1977	TIFF 6.0	Little Endian (PC)	Uncompressed	1	\N	\N	2	\N	\N	\N	\N	\N	\N	f	0	44774195	1	library internal use	3391	4401	400	8,8,8	integer	3	0	7	\N	2.2	100	\N	2006-08-15 00:00:00	f	\N	\N	\N	\N
957	1978	TIFF 6.0	Little Endian (PC)	Uncompressed	1	\N	\N	2	\N	\N	\N	\N	\N	\N	f	0	25585254	1	library internal use	2389	3573	400	8,8,8	integer	3	0	7	\N	2.2	100	\N	2006-08-15 00:00:00	f	\N	\N	\N	\N
958	1979	TIFF 6.0	Little Endian (PC)	Uncompressed	1	\N	\N	2	\N	\N	\N	\N	\N	\N	f	0	11429478	1	library internal use	1709	2231	400	8,8,8	integer	3	0	7	\N	2.2	100	\N	2006-08-15 00:00:00	f	\N	\N	\N	\N
959	1980	TIFF 6.0	Little Endian (PC)	Uncompressed	1	\N	\N	2	\N	\N	\N	\N	\N	\N	f	0	31666995	1	library internal use	2703	3904	400	8,8,8	integer	3	0	7	\N	2.2	100	\N	2006-08-15 00:00:00	f	\N	\N	\N	\N
960	1982	TIFF 6.0	Little Endian (PC)	Uncompressed	1	\N	\N	2	\N	\N	\N	\N	\N	\N	f	0	44040192	1	library internal use	3330	4410	400	8,8,8	integer	3	0	7	\N	2.2	100	\N	2006-08-16 00:00:00	f	\N	\N	\N	\N
961	1983	TIFF 6.0	Little Endian (PC)	Uncompressed	1	\N	\N	2	\N	\N	\N	\N	\N	\N	f	0	20237517	1	library internal use	2031	3329	400	8,8,8	integer	3	0	7	\N	2.2	100	\N	2006-08-16 00:00:00	f	\N	\N	\N	\N
962	1983	TIFF 6.0	Little Endian (PC)	Uncompressed	1	\N	\N	2	\N	\N	\N	\N	\N	\N	f	0	20237517	1	library internal use	2031	3329	400	8,8,8	integer	3	0	7	\N	2.2	100	\N	2006-08-16 00:00:00	f	\N	\N	\N	\N
963	1983	TIFF 6.0	Little Endian (PC)	Uncompressed	1	\N	\N	2	\N	\N	\N	\N	\N	\N	f	0	20237517	1	library internal use	2031	3329	400	8,8,8	integer	3	0	7	\N	2.2	100	\N	2006-08-16 00:00:00	f	\N	\N	\N	\N
964	1984	TIFF 6.0	Little Endian (PC)	Uncompressed	1	\N	\N	2	\N	\N	\N	\N	\N	\N	f	0	20132659	1	library internal use	2014	3329	400	8,8,8	integer	3	0	7	\N	2.2	100	\N	2006-08-16 00:00:00	f	\N	\N	\N	\N
965	1985	TIFF 6.0	Little Endian (PC)	Uncompressed	1	\N	\N	2	\N	\N	\N	\N	\N	\N	f	0	72666317	1	library internal use	4349	5559	400	8,8,8	integer	3	0	7	\N	2.2	100	\N	2006-08-16 00:00:00	f	\N	\N	\N	\N
966	1986	TIFF 6.0	Little Endian (PC)	Uncompressed	1	\N	\N	2	\N	\N	\N	\N	\N	\N	f	0	70464307	1	library internal use	4178	5620	400	8,8,8	integer	3	0	7	\N	2.2	100	\N	2006-08-16 00:00:00	f	\N	\N	\N	\N
967	1987	TIFF 6.0	Little Endian (PC)	Uncompressed	1	\N	\N	2	\N	\N	\N	\N	\N	\N	f	0	69940019	1	library internal use	4178	5579	400	8,8,8	integer	3	0	7	\N	2.2	100	\N	2006-08-16 00:00:00	f	\N	\N	\N	\N
968	1988	TIFF 6.0	Little Endian (PC)	Uncompressed	1	\N	\N	2	\N	\N	\N	\N	\N	\N	f	0	89024102	1	library internal use	6790	4369	400	8,8,8	integer	3	0	7	\N	2.2	100	\N	2006-08-16 00:00:00	f	\N	\N	\N	\N
969	1989	TIFF 6.0	Little Endian (PC)	Uncompressed	1	\N	\N	2	\N	\N	\N	\N	\N	\N	f	0	89024102	1	library internal use	6790	4369	400	8,8,8	integer	3	0	7	\N	2.2	100	\N	2006-08-16 00:00:00	f	\N	\N	\N	\N
970	1990	TIFF 6.0	Little Endian (PC)	Uncompressed	1	\N	\N	2	\N	\N	\N	\N	\N	\N	f	0	67423437	1	library internal use	4148	5420	400	8,8,8	integer	3	0	7	\N	2.2	100	\N	2006-08-16 00:00:00	f	\N	\N	\N	\N
971	1990	TIFF 6.0	Little Endian (PC)	Uncompressed	1	\N	\N	2	\N	\N	\N	\N	\N	\N	f	0	67423437	1	library internal use	4148	5420	400	8,8,8	integer	3	0	7	\N	2.2	100	\N	2006-08-16 00:00:00	f	\N	\N	\N	\N
972	1992	TIFF 6.0	Little Endian (PC)	Uncompressed	1	\N	\N	2	\N	\N	\N	\N	\N	\N	f	0	66165146	1	library internal use	4108	5370	400	8,8,8	integer	3	0	7	\N	2.2	100	\N	\N	f	\N	\N	\N	\N
973	1991	TIFF 6.0	Little Endian (PC)	Uncompressed	1	\N	\N	2	\N	\N	\N	\N	\N	\N	f	0	67423437	1	library internal use	4108	5370	400	8,8,8	integer	3	0	7	\N	2.2	100	\N	\N	f	\N	\N	\N	\N
974	1993	TIFF 6.0	Little Endian (PC)	Uncompressed	1	\N	\N	2	\N	\N	\N	\N	\N	\N	f	0	66165146	1	library internal use	4108	5370	400	8,8,8	integer	3	0	7	\N	2.2	100	\N	2006-08-16 00:00:00	f	\N	\N	\N	\N
975	1993	TIFF 6.0	Little Endian (PC)	Uncompressed	1	\N	\N	2	\N	\N	\N	\N	\N	\N	f	0	0	1	library internal use	0	0	400	8,8,8	integer	3	0	1	\N	2.2	100	\N	2006-08-16 00:00:00	f	\N	\N	\N	\N
976	1994	TIFF 6.0	Little Endian (PC)	Uncompressed	1	\N	\N	2	\N	\N	\N	\N	\N	\N	f	0	66794291	1	library internal use	4148	5370	400	8,8,8	integer	3	0	7	\N	2.2	100	\N	\N	f	\N	\N	\N	\N
977	1995	TIFF 6.0	Little Endian (PC)	Uncompressed	1	\N	\N	2	\N	\N	\N	\N	\N	\N	f	0	40684749	1	library internal use	3295	4114	400	8,8,8	integer	3	0	7	\N	2.2	100	\N	\N	f	\N	\N	\N	\N
978	1996	TIFF 6.0	Little Endian (PC)	Uncompressed	1	\N	\N	2	\N	\N	\N	\N	\N	\N	f	0	44669338	1	library internal use	3400	4384	400	8,8,8	integer	3	0	7	\N	2.2	100	\N	2006-08-16 00:00:00	f	\N	\N	\N	\N
979	1997	TIFF 6.0	Little Endian (PC)	Uncompressed	1	\N	\N	2	\N	\N	\N	\N	\N	\N	f	0	44459622	1	library internal use	3383	4384	400	8,8,8	integer	3	0	7	\N	2.2	100	\N	2006-08-16 00:00:00	f	\N	\N	\N	\N
980	1998	TIFF 6.0	Little Endian (PC)	Uncompressed	1	\N	\N	2	\N	\N	\N	\N	\N	\N	f	0	44249907	1	library internal use	3374	4275	400	8,8,8	integer	3	0	7	\N	2.2	100	\N	2006-08-16 00:00:00	f	\N	\N	\N	\N
981	1999	TIFF 6.0	Little Endian (PC)	Uncompressed	1	\N	\N	2	\N	\N	\N	\N	\N	\N	f	0	42047898	1	library internal use	3226	4340	400	8,8,8	integer	3	0	7	\N	2.2	100	\N	2006-08-16 00:00:00	f	\N	\N	\N	\N
982	2000	TIFF 6.0	Little Endian (PC)	Uncompressed	1	\N	\N	2	\N	\N	\N	\N	\N	\N	f	0	43306189	1	library internal use	3383	4262	400	8,8,8	integer	3	0	7	\N	2.2	100	\N	2006-08-16 00:00:00	f	\N	\N	\N	\N
983	2001	TIFF 6.0	Little Endian (PC)	Uncompressed	1	\N	\N	2	\N	\N	\N	\N	\N	\N	f	0	43725619	1	library internal use	3330	4375	400	8,8,8	integer	3	0	7	\N	2.2	100	\N	2006-08-16 00:00:00	f	\N	\N	\N	\N
984	2002	TIFF 6.0	Little Endian (PC)	Uncompressed	1	\N	\N	2	\N	\N	\N	\N	\N	\N	f	0	44669338	1	library internal use	3400	4384	400	8,8,8	integer	3	0	7	\N	2.2	100	\N	\N	f	\N	\N	\N	\N
985	2003	TIFF 6.0	Little Endian (PC)	Uncompressed	1	\N	\N	2	\N	\N	\N	\N	\N	\N	f	0	44459622	1	library internal use	3383	4384	400	8,8,8	integer	3	0	7	\N	2.2	100	\N	2006-08-16 00:00:00	f	\N	\N	\N	\N
986	2004	TIFF 6.0	Little Endian (PC)	Uncompressed	1	\N	\N	2	\N	\N	\N	\N	\N	\N	f	0	44040192	1	library internal use	3348	4384	400	8,8,8	integer	3	0	7	\N	2.2	100	\N	2006-08-16 00:00:00	f	\N	\N	\N	\N
987	2005	TIFF 6.0	Little Endian (PC)	Uncompressed	1	\N	\N	2	\N	\N	\N	\N	\N	\N	f	0	44459622	1	library internal use	3400	4358	400	8,8,8	integer	3	0	7	\N	2.2	100	\N	2006-08-16 00:00:00	f	\N	\N	\N	\N
988	2006	TIFF 6.0	Little Endian (PC)	Uncompressed	1	\N	\N	2	\N	\N	\N	\N	\N	\N	f	0	44669338	1	library internal use	3400	4384	400	8,8,8	integer	3	0	7	\N	2.2	100	\N	2006-08-16 00:00:00	f	\N	\N	\N	\N
989	2007	TIFF 6.0	Little Endian (PC)	Uncompressed	1	\N	\N	2	\N	\N	\N	\N	\N	\N	f	0	44669338	1	library internal use	3400	4384	400	8,8,8	integer	3	0	7	\N	2.2	100	\N	\N	f	\N	\N	\N	\N
990	2008	TIFF 6.0	Little Endian (PC)	Uncompressed	1	\N	\N	2	\N	\N	\N	\N	\N	\N	f	0	44459622	1	library internal use	3374	4392	400	8,8,8	integer	3	0	7	\N	2.2	100	\N	2006-08-16 00:00:00	f	\N	\N	\N	\N
991	2009	TIFF 6.0	Little Endian (PC)	Uncompressed	1	\N	\N	2	\N	\N	\N	\N	\N	\N	f	0	42677043	1	library internal use	3383	4201	400	8,8,8	integer	3	0	7	\N	2.2	100	\N	2006-08-16 00:00:00	f	\N	\N	\N	\N
992	2010	TIFF 6.0	Little Endian (PC)	Uncompressed	1	\N	\N	2	\N	\N	\N	\N	\N	\N	f	0	30303846	1	library internal use	2816	3582	400	8,8,8	integer	3	0	7	\N	2.2	100	\N	2006-08-16 00:00:00	f	\N	\N	\N	\N
993	2011	TIFF 6.0	Little Endian (PC)	Uncompressed	1	\N	\N	2	\N	\N	\N	\N	\N	\N	f	0	30408704	1	library internal use	2825	3591	400	8,8,8	integer	3	0	7	\N	2.2	100	\N	2006-08-17 00:00:00	f	\N	\N	\N	\N
994	\N	TIFF 6.0	Little Endian (PC)	Uncompressed	1	\N	\N	2	\N	\N	\N	\N	\N	\N	f	0	0	0	library internal use	13	0	400	8,8,8	integer	3	0	0	\N	2.2	100	\N	\N	f	\N	\N	\N	\N
995	\N	TIFF 6.0	Little Endian (PC)	Uncompressed	1	\N	\N	2	\N	\N	\N	\N	\N	\N	f	0	0	0	library internal use	12	0	400	8,8,8	integer	3	0	0	\N	2.2	100	\N	\N	f	\N	\N	\N	\N
996	\N	TIFF 6.0	Little Endian (PC)	Uncompressed	1	\N	\N	2	\N	\N	\N	\N	\N	\N	f	0	0	0	library internal use	12	0	400	8,8,8	integer	3	0	0	\N	2.2	100	\N	\N	f	\N	\N	\N	\N
997	\N	TIFF 6.0	Little Endian (PC)	Uncompressed	1	\N	\N	2	\N	\N	\N	\N	\N	\N	f	0	0	0	library internal use	12	0	400	8,8,8	integer	3	0	0	\N	2.2	100	\N	\N	f	\N	\N	\N	\N
998	\N	TIFF 6.0	Little Endian (PC)	Uncompressed	1	\N	\N	2	\N	\N	\N	\N	\N	\N	f	0	0	0	library internal use	12	0	400	8,8,8	integer	3	0	0	\N	2.2	100	\N	\N	f	\N	\N	\N	\N
999	\N	TIFF 6.0	Little Endian (PC)	Uncompressed	1	\N	\N	2	\N	\N	\N	\N	\N	\N	f	0	0	0	library internal use	12.1	0	400	8,8,8	integer	3	0	0	\N	2.2	100	\N	\N	f	\N	\N	\N	\N
1000	\N	TIFF 6.0	Little Endian (PC)	Uncompressed	1	\N	\N	2	\N	\N	\N	\N	\N	\N	f	0	0	1	library internal use	12.800000000000001	0	400	8,8,8	integer	3	0	1	\N	2.2	100	\N	\N	f	\N	\N	\N	\N
59	1034	TIFF 6.0	Little Endian (PC)	Uncompressed	1	Adobe RGB 1998	\N	2	\N	\N	\N	\N	\N	\N	f	0	44774195	1	library internal use	3391	4401	400	8,8,8	integer	3	0	7	\N	2.2	100	Dawson Grant	2006-06-07 00:00:00	f	\N	\N	\N	\N
60	1035	TIFF 6.0	Little Endian (PC)	Uncompressed	1	Adobe RGB 1998	\N	2	\N	\N	\N	\N	\N	\N	f	0	44774195	1	library internal use	3391	4401	400	8,8,8	integer	3	0	7	\N	2.2	100	Dawson Grant	2006-06-07 00:00:00	f	\N	\N	\N	\N
61	1036	TIFF 6.0	Little Endian (PC)	Uncompressed	1	Adobe RGB 1998	\N	2	\N	\N	\N	\N	\N	\N	f	0	44774195	1	library internal use	3391	4401	400	8,8,8	integer	3	0	7	\N	2.2	100	Dawson Grant	2006-06-07 00:00:00	f	\N	\N	\N	\N
63	1037	TIFF 6.0	Little Endian (PC)	Uncompressed	1	Adobe RGB 1998	\N	2	\N	\N	\N	\N	\N	\N	f	0	44774195	1	library internal use	3391	4401	400	8,8,8	integer	3	0	7	\N	2.2	100	Dawson Grant	2006-06-07 00:00:00	f	\N	\N	\N	\N
64	1038	TIFF 6.0	Little Endian (PC)	Uncompressed	1	\N	\N	2	\N	\N	\N	\N	\N	\N	f	0	17196646	0	library internal use	2807	2040	400	8,8,8	integer	3	0	0	\N	2.2	100	\N	\N	f	\N	\N	\N	\N
73	1047	TIFF 6.0	Little Endian (PC)	Uncompressed	1	Adobe RGB 1998	\N	2	\N	\N	\N	\N	\N	\N	f	0	44354765	1	library internal use	3365	4392	400	8,8,8	integer	3	0	7	\N	2.2	100	Dawson Grant	2006-06-09 00:00:00	f	\N	\N	\N	\N
74	1048	TIFF 6.0	Little Endian (PC)	Uncompressed	1	Adobe RGB 1998	\N	2	\N	\N	\N	\N	\N	\N	f	0	44354765	1	library internal use	3365	4392	400	8,8,8	integer	3	0	7	\N	2.2	100	Dawson Grant	2006-06-09 00:00:00	f	\N	\N	\N	\N
75	1049	TIFF 6.0	Little Endian (PC)	Uncompressed	1	Adobe RGB 1998	\N	2	\N	\N	\N	\N	\N	\N	f	0	44354765	1	library internal use	3365	4392	400	8,8,8	integer	3	0	7	\N	2.2	100	Dawson Grant	2006-06-09 00:00:00	f	\N	\N	\N	\N
76	1050	TIFF 6.0	Little Endian (PC)	Uncompressed	1	Adobe RGB 1998	\N	2	\N	\N	\N	\N	\N	\N	f	0	44354765	1	library internal use	3365	4392	400	8,8,8	integer	3	0	7	\N	2.2	100	Dawson Grant	\N	f	\N	\N	\N	\N
77	1051	TIFF 6.0	Little Endian (PC)	Uncompressed	1	Adobe RGB 1998	\N	2	\N	\N	\N	\N	\N	\N	f	0	44354765	1	library internal use	3365	4392	400	8,8,8	integer	3	0	7	\N	2.2	100	Dawson Grant	2006-06-09 00:00:00	f	\N	\N	\N	\N
78	1052	TIFF 6.0	Little Endian (PC)	Uncompressed	1	Adobe RGB 1998	\N	2	\N	\N	\N	\N	\N	\N	f	0	44354765	1	library internal use	3365	4392	400	8,8,8	integer	3	0	7	\N	2.2	100	Dawson Grant	2006-06-09 00:00:00	f	\N	\N	\N	\N
79	1053	TIFF 6.0	Little Endian (PC)	Uncompressed	1	Adobe RGB 1998	\N	2	\N	\N	\N	\N	\N	\N	f	0	44354765	1	library internal use	3365	4392	400	8,8,8	integer	3	0	7	\N	2.2	100	Dawson Grant	2006-06-09 00:00:00	f	\N	\N	\N	\N
80	1054	TIFF 6.0	Little Endian (PC)	Uncompressed	1	Adobe RGB 1998	\N	2	\N	\N	\N	\N	\N	\N	f	0	44354765	1	library internal use	3365	4392	400	8,8,8	integer	3	0	7	\N	2.2	100	Dawson Grant	2006-06-09 00:00:00	f	\N	\N	\N	\N
81	1055	TIFF 6.0	Little Endian (PC)	Uncompressed	1	Adobe RGB 1998	\N	2	\N	\N	\N	\N	\N	\N	f	0	44354765	1	library internal use	3365	4392	400	8,8,8	integer	3	0	7	\N	2.2	100	Dawson Grant	2006-06-09 00:00:00	f	\N	\N	\N	\N
82	1056	TIFF 6.0	Little Endian (PC)	Uncompressed	1	Adobe RGB 1998	\N	2	\N	\N	\N	\N	\N	\N	f	0	44354765	1	library internal use	3365	4392	400	8,8,8	integer	3	0	7	\N	2.2	100	Dawson Grant	2006-06-09 00:00:00	f	\N	\N	\N	\N
83	1057	TIFF 6.0	Little Endian (PC)	Uncompressed	1	Adobe RGB 1998	\N	2	\N	\N	\N	\N	\N	\N	f	0	44354765	1	library internal use	3365	4392	400	8,8,8	integer	3	0	7	\N	2.2	100	Dawson Grant	2006-06-09 00:00:00	f	\N	\N	\N	\N
84	1058	TIFF 6.0	Little Endian (PC)	Uncompressed	1	Adobe RGB 1998	\N	2	\N	\N	\N	\N	\N	\N	f	0	44354765	1	library internal use	3365	4392	400	8,8,8	integer	3	0	7	\N	2.2	100	Dawson Grant	2006-06-09 00:00:00	f	\N	\N	\N	\N
85	1059	TIFF 6.0	Little Endian (PC)	Uncompressed	1	Adobe RGB 1998	\N	2	\N	\N	\N	\N	\N	\N	f	0	44564480	1	library internal use	3400	4366	400	8,8,8	integer	3	0	7	\N	2.2	100	Dawson Grant	2006-06-09 00:00:00	f	\N	\N	\N	\N
86	1060	TIFF 6.0	Little Endian (PC)	Uncompressed	1	Adobe RGB 1998	\N	2	\N	\N	\N	\N	\N	\N	f	0	44564480	1	library internal use	3400	4366	400	8,8,8	integer	3	0	7	\N	2.2	100	Dawson Grant	2006-06-09 00:00:00	f	\N	\N	\N	\N
87	1061	TIFF 6.0	Little Endian (PC)	Uncompressed	1	Adobe RGB 1998	\N	2	\N	\N	\N	\N	\N	\N	f	0	44564480	1	library internal use	3400	4366	400	8,8,8	integer	3	0	7	\N	2.2	100	Dawson Grant	2006-06-09 00:00:00	f	\N	\N	\N	\N
88	1062	TIFF 6.0	Little Endian (PC)	Uncompressed	1	Adobe RGB 1998	\N	2	\N	\N	\N	\N	\N	\N	f	0	44564480	1	library internal use	3400	4366	400	8,8,8	integer	3	0	7	\N	2.2	100	Dawson Grant	2006-06-09 00:00:00	f	\N	\N	\N	\N
89	1063	TIFF 6.0	Little Endian (PC)	Uncompressed	1	Adobe RGB 1998	\N	2	\N	\N	\N	\N	\N	\N	f	0	44564480	1	library internal use	3400	4366	400	8,8,8	integer	3	0	7	\N	2.2	100	Dawson Grant	2006-06-09 00:00:00	f	\N	\N	\N	\N
90	1064	TIFF 6.0	Little Endian (PC)	Uncompressed	1	Adobe RGB 1998	\N	2	\N	\N	\N	\N	\N	\N	f	0	44564480	1	library internal use	3400	4366	400	8,8,8	integer	3	0	7	\N	2.2	100	Dawson Grant	2006-06-09 00:00:00	f	\N	\N	\N	\N
91	1065	TIFF 6.0	Little Endian (PC)	Uncompressed	1	Adobe RGB 1998	\N	2	\N	\N	\N	\N	\N	\N	f	0	44564480	1	library internal use	3400	4366	400	8,8,8	integer	3	0	7	\N	2.2	100	Dawson Grant	2006-06-09 00:00:00	f	\N	\N	\N	\N
92	1066	TIFF 6.0	Little Endian (PC)	Uncompressed	1	44459622	\N	2	\N	\N	\N	\N	\N	\N	f	0	44459622	1	library internal use	3400	4358	400	8,8,8	integer	3	0	7	\N	2.2	100	Dawson Grant	2006-06-09 00:00:00	f	\N	\N	\N	\N
93	1067	TIFF 6.0	Little Endian (PC)	Uncompressed	1	44459622	\N	2	\N	\N	\N	\N	\N	\N	f	0	44459622	1	library internal use	3400	4358	400	8,8,8	integer	3	0	7	\N	2.2	100	Dawson Grant	2006-06-09 00:00:00	f	\N	\N	\N	\N
94	1068	TIFF 6.0	Little Endian (PC)	Uncompressed	1	Adobe RGB 1998	\N	2	\N	\N	\N	\N	\N	\N	f	0	44564480	1	library internal use	3383	4392	400	8,8,8	integer	3	0	7	\N	2.2	100	Dawson Grant	2006-06-09 00:00:00	f	\N	\N	\N	\N
99	1073	TIFF 6.0	Little Endian (PC)	Uncompressed	1	Adobe RGB 1998	\N	2	\N	\N	\N	\N	\N	\N	f	0	44354765	1	library internal use	3356	4401	400	8,8,8	integer	3	0	7	\N	2.2	100	Dawson Grant	2006-06-09 00:00:00	f	\N	\N	\N	\N
100	1074	TIFF 6.0	Little Endian (PC)	Uncompressed	1	Adobe RGB 1998	\N	2	\N	\N	\N	\N	\N	\N	f	0	44354765	1	library internal use	3356	4401	400	8,8,8	integer	3	0	7	\N	2.2	100	Dawson Grant	2006-06-09 00:00:00	f	\N	\N	\N	\N
95	1069	TIFF 6.0	Little Endian (PC)	Uncompressed	1	Adobe RGB 1998	\N	2	\N	\N	\N	\N	\N	\N	f	0	44040192	1	library internal use	3365	4358	400	8,8,8	integer	3	0	7	\N	2.2	100	Dawson Grant	2006-06-09 00:00:00	f	\N	\N	\N	\N
96	1070	TIFF 6.0	Little Endian (PC)	Uncompressed	1	Adobe RGB 1998	\N	2	\N	\N	\N	\N	\N	\N	f	0	44040192	1	library internal use	3365	4358	400	8,8,8	integer	3	0	7	\N	2.2	100	Dawson Grant	2006-06-09 00:00:00	f	\N	\N	\N	\N
97	1071	TIFF 6.0	Little Endian (PC)	Uncompressed	1	Adobe RGB 1998	\N	2	\N	\N	\N	\N	\N	\N	f	0	44040192	1	library internal use	3365	4358	400	8,8,8	integer	3	0	7	\N	2.2	100	Dawson Grant	2006-06-09 00:00:00	f	\N	\N	\N	\N
98	1072	TIFF 6.0	Little Endian (PC)	Uncompressed	1	Adobe RGB 1998	\N	2	\N	\N	\N	\N	\N	\N	f	0	44040192	1	library internal use	3365	4358	400	8,8,8	integer	3	0	7	\N	2.2	100	Dawson Grant	2006-06-09 00:00:00	f	\N	\N	\N	\N
101	1075	TIFF 6.0	Little Endian (PC)	Uncompressed	1	Adobe RGB 1998	\N	2	\N	\N	\N	\N	\N	\N	f	0	44564480	1	library internal use	3400	4366	400	8,8,8	integer	3	0	7	\N	2.2	100	Dawson Grant	2006-06-09 00:00:00	f	\N	\N	\N	\N
102	1076	TIFF 6.0	Little Endian (PC)	Uncompressed	1	Adobe RGB 1998	\N	2	\N	\N	\N	\N	\N	\N	f	0	44564480	1	library internal use	3400	4366	400	8,8,8	integer	3	0	7	\N	2.2	100	Dawson Grant	2006-06-09 00:00:00	f	\N	\N	\N	\N
103	1077	TIFF 6.0	Little Endian (PC)	Uncompressed	1	Adobe RGB 1998	\N	2	\N	\N	\N	\N	\N	\N	f	0	44564480	1	library internal use	3400	4366	400	8,8,8	integer	3	0	7	\N	2.2	100	Dawson Grant	2006-06-09 00:00:00	f	\N	\N	\N	\N
104	1078	TIFF 6.0	Little Endian (PC)	Uncompressed	1	Adobe RGB 1998	\N	2	\N	\N	\N	\N	\N	\N	f	0	44564480	1	library internal use	3400	4366	400	8,8,8	integer	3	0	7	\N	2.2	100	Dawson Grant	2006-06-09 00:00:00	f	\N	\N	\N	\N
105	1079	TIFF 6.0	Little Endian (PC)	Uncompressed	1	Adobe RGB 1998	\N	2	\N	\N	\N	\N	\N	\N	f	0	44564480	1	library internal use	3400	4366	400	8,8,8	integer	3	0	7	\N	2.2	100	Dawson Grant	2006-06-09 00:00:00	f	\N	\N	\N	\N
106	1080	TIFF 6.0	Little Endian (PC)	Uncompressed	1	Adobe RGB 1998	\N	2	\N	\N	\N	\N	\N	\N	f	0	44564480	1	library internal use	3400	4366	400	8,8,8	integer	3	0	7	\N	2.2	100	Dawson Grant	2006-06-09 00:00:00	f	\N	\N	\N	\N
107	1081	TIFF 6.0	Little Endian (PC)	Uncompressed	1	Adobe RGB 1998	\N	2	\N	\N	\N	\N	\N	\N	f	0	44564480	1	library internal use	3400	4366	400	8,8,8	integer	3	0	7	\N	2.2	100	Dawson Grant	2006-06-09 00:00:00	f	\N	\N	\N	\N
108	1082	TIFF 6.0	Little Endian (PC)	Uncompressed	1	Adobe RGB 1998	\N	2	\N	\N	\N	\N	\N	\N	f	0	44564480	1	library internal use	3400	4366	400	8,8,8	integer	3	0	7	\N	2.2	100	Dawson Grant	2006-06-09 00:00:00	f	\N	\N	\N	\N
109	1083	TIFF 6.0	Little Endian (PC)	Uncompressed	1	Adobe RGB 1998	\N	2	\N	\N	\N	\N	\N	\N	f	0	44564480	1	library internal use	3400	4366	400	8,8,8	integer	3	0	7	\N	2.2	100	Dawson Grant	2006-06-09 00:00:00	f	\N	\N	\N	\N
110	1084	TIFF 6.0	Little Endian (PC)	Uncompressed	1	Adobe RGB 1998	\N	2	\N	\N	\N	\N	\N	\N	f	0	21390950	1	library internal use	2110	3381	400	8,8,8	integer	3	0	7	\N	2.2	100	Dawson Grant	2006-06-09 00:00:00	f	\N	\N	\N	\N
142	1118	TIFF 6.0	Little Endian (PC)	Uncompressed	1	Adobe RGB 1998	\N	2	\N	\N	\N	\N	\N	\N	f	0	26738688	1	library internal use	2550	3497	400	8,8,8	integer	3	0	7	\N	2.2	100	Dawson Grant	2006-06-13 00:00:00	f	\N	\N	\N	\N
143	1119	TIFF 6.0	Little Endian (PC)	Uncompressed	1	Adobe RGB 1998	\N	2	\N	\N	\N	\N	\N	\N	f	0	24746394	1	library internal use	2550	3288	400	8,8,8	integer	3	0	7	\N	2.2	100	Dawson Grant	2006-06-13 00:00:00	f	\N	\N	\N	\N
151	1127	TIFF 6.0	Little Endian (PC)	Uncompressed	1	Adobe RGB 1998	\N	2	\N	\N	\N	\N	\N	\N	f	0	24956109	1	library internal use	2543	3268	400	8,8,8	integer	3	0	7	\N	2.2	100	Dawson Grant	2006-06-13 00:00:00	f	\N	\N	\N	\N
153	1129	TIFF 6.0	Little Endian (PC)	Uncompressed	1	Adobe RGB 1998	\N	2	\N	\N	\N	\N	\N	\N	f	0	25165824	1	library internal use	2550	3294	400	8,8,8	integer	3	0	7	\N	2.2	100	Dawson Grant	2006-06-13 00:00:00	f	\N	\N	\N	\N
152	1128	TIFF 6.0	Little Endian (PC)	Uncompressed	1	Adobe RGB 1998	\N	2	\N	\N	\N	\N	\N	\N	f	0	24956109	1	library internal use	2543	3268	400	8,8,8	integer	3	0	7	\N	2.2	100	Dawson Grant	2006-06-13 00:00:00	f	\N	\N	\N	\N
154	1130	TIFF 6.0	Little Endian (PC)	Uncompressed	1	Adobe RGB 1998	\N	2	\N	\N	\N	\N	\N	\N	f	0	25165824	1	library internal use	2550	3294	400	8,8,8	integer	3	0	7	\N	2.2	100	Dawson Grant	2006-06-13 00:00:00	f	\N	\N	\N	\N
159	1135	TIFF 6.0	Little Endian (PC)	Uncompressed	1	Adobe RGB 1998	\N	2	\N	\N	\N	\N	\N	\N	f	0	25060966	1	library internal use	2550	3275	400	8,8,8	integer	3	0	7	\N	2.2	100	Dawson Grant	2006-06-13 00:00:00	f	\N	\N	\N	\N
160	1136	TIFF 6.0	Little Endian (PC)	Uncompressed	1	Adobe RGB 1998	\N	2	\N	\N	\N	\N	\N	\N	f	0	25060966	1	library internal use	2550	3275	400	8,8,8	integer	3	0	7	\N	2.2	100	Dawson Grant	2006-06-13 00:00:00	f	\N	\N	\N	\N
165	1141	TIFF 6.0	Little Endian (PC)	Uncompressed	1	Adobe RGB 1998	\N	2	\N	\N	\N	\N	\N	\N	f	0	25060966	1	library internal use	2550	3275	400	8,8,8	integer	3	0	7	\N	2.2	100	Dawson Grant	2006-06-13 00:00:00	f	\N	\N	\N	\N
166	1142	TIFF 6.0	Little Endian (PC)	Uncompressed	1	Adobe RGB 1998	\N	2	\N	\N	\N	\N	\N	\N	f	0	25060966	1	library internal use	2550	3275	400	8,8,8	integer	3	0	7	\N	2.2	100	Dawson Grant	2006-06-13 00:00:00	f	\N	\N	\N	\N
167	1143	TIFF 6.0	Little Endian (PC)	Uncompressed	1	Adobe RGB 1998	\N	2	\N	\N	\N	\N	\N	\N	f	0	25060966	1	library internal use	2550	3275	400	8,8,8	integer	3	0	7	\N	2.2	100	Dawson Grant	2006-06-13 00:00:00	f	\N	\N	\N	\N
181	1166	TIFF 6.0	Little Endian (PC)	Uncompressed	1	Adobe RGB 1998	\N	2	\N	\N	\N	\N	\N	\N	f	0	44354765	1	library internal use	3400	4340	400	8,8,8	integer	3	0	7	\N	2.2	100	Dawson Grant	2006-06-14 00:00:00	f	\N	\N	\N	\N
182	1167	TIFF 6.0	Little Endian (PC)	Uncompressed	1	Adobe RGB 1998	\N	2	\N	\N	\N	\N	\N	\N	f	0	15309210	1	library internal use	1543	3312	400	8,8,8	integer	3	0	7	\N	2.2	100	Dawson Grant	2006-06-14 00:00:00	f	\N	\N	\N	\N
184	1169	TIFF 6.0	Little Endian (PC)	Uncompressed	1	Adobe RGB 1998	\N	2	\N	\N	\N	\N	\N	\N	f	0	15309210	1	library internal use	1543	3312	400	8,8,8	integer	3	0	7	\N	2.2	100	Ohio Music Education Association	2006-06-13 00:00:00	f	\N	\N	\N	\N
193	1178	TIFF 6.0	Little Endian (PC)	Uncompressed	1	Adobe RGB 1998	\N	2	\N	\N	\N	\N	\N	\N	f	0	44459622	1	library internal use	3400	4358	400	8,8,8	integer	3	0	7	\N	2.2	100	Dawson Grant	2006-06-14 00:00:00	f	\N	\N	\N	\N
205	1190	TIFF 6.0	Little Endian (PC)	Uncompressed	1	Adobe RGB 1998	\N	2	\N	\N	\N	\N	\N	\N	f	0	44669338	1	library internal use	3400	4375	400	8,8,8	integer	3	0	7	\N	2.2	100	Dawson Grant	2006-06-14 00:00:00	f	\N	\N	\N	\N
206	1191	TIFF 6.0	Little Endian (PC)	Uncompressed	1	Adobe RGB 1998	\N	2	\N	\N	\N	\N	\N	\N	f	0	44669338	1	library internal use	3400	4375	400	8,8,8	integer	3	0	7	\N	2.2	100	Dawson Grant	2006-06-14 00:00:00	f	\N	\N	\N	\N
207	1192	TIFF 6.0	Little Endian (PC)	Uncompressed	1	Adobe RGB 1998	\N	2	\N	\N	\N	\N	\N	\N	f	0	44669338	1	library internal use	3400	4375	400	8,8,8	integer	3	0	7	\N	2.2	100	Dawson Grant	2006-06-14 00:00:00	f	\N	\N	\N	\N
283	1286	TIFF 6.0	Little Endian (PC)	Uncompressed	1	Adobe RGB 1998	\N	2	\N	\N	\N	\N	\N	\N	f	0	43725619	1	library internal use	3330	4375	400	8,8,8	integer	3	0	7	\N	2.2	100	Dawson Grant	2006-06-23 00:00:00	f	\N	\N	\N	\N
284	1287	TIFF 6.0	Little Endian (PC)	Uncompressed	1	Adobe RGB 1998	\N	2	\N	\N	\N	\N	\N	\N	f	0	43725619	1	library internal use	3330	4375	400	8,8,8	integer	3	0	7	\N	2.2	100	Dawson Grant	2006-06-23 00:00:00	f	\N	\N	\N	\N
285	1288	TIFF 6.0	Little Endian (PC)	Uncompressed	1	Adobe RGB 1998	\N	2	\N	\N	\N	\N	\N	\N	f	0	41733325	1	library internal use	3182	4375	400	8,8,8	integer	3	0	7	\N	2.2	100	Dawson Grant	2006-06-23 00:00:00	f	\N	\N	\N	\N
286	1289	TIFF 6.0	Little Endian (PC)	Uncompressed	1	Adobe RGB 1998	\N	2	\N	\N	\N	\N	\N	\N	f	0	41733325	1	library internal use	3182	4375	400	8,8,8	integer	3	0	7	\N	2.2	100	Dawson Grant	2006-06-23 00:00:00	f	\N	\N	\N	\N
287	1290	TIFF 6.0	Little Endian (PC)	Uncompressed	1	Adobe RGB 1998	\N	2	\N	\N	\N	\N	\N	\N	f	0	9374269	1	library internal use	2284	1368	400	8,8,8	integer	3	0	7	\N	2.2	100	\N	2006-06-23 00:00:00	f	\N	\N	\N	\N
288	1291	TIFF 6.0	Little Endian (PC)	Uncompressed	1	Adobe RGB 1998	\N	2	\N	\N	\N	\N	\N	\N	f	0	43725619	1	library internal use	3330	4375	400	8,8,8	integer	3	0	7	\N	2.2	100	Dawson Grant	2006-06-23 00:00:00	f	\N	\N	\N	\N
289	1292	TIFF 6.0	Little Endian (PC)	Uncompressed	1	Adobe RGB 1998	\N	2	\N	\N	\N	\N	\N	\N	f	0	16357786	1	library internal use	2772	1970	400	8,8,8	integer	3	0	7	\N	2.2	100	Dawson Grant	2006-06-23 00:00:00	f	\N	\N	\N	\N
342	1345	TIFF 6.0	Little Endian (PC)	Uncompressed	1	Adobe RBB 1998	\N	2	\N	\N	\N	\N	\N	\N	f	0	9479127	1	library internal use	2144	1473	400	8,8,8	integer	3	0	7	\N	2.2	100	Dawson Grant	2006-06-27 00:00:00	f	\N	\N	\N	\N
345	1348	TIFF 6.0	Little Endian (PC)	Uncompressed	1	Adobe RBB 1998	\N	2	\N	\N	\N	\N	\N	\N	f	0	26214400	1	library internal use	3400	2571	400	8,8,8	integer	3	0	7	\N	2.2	100	Dawson Grant	2006-06-27 00:00:00	f	\N	\N	\N	\N
346	1349	TIFF 6.0	Little Endian (PC)	Uncompressed	1	Adobe RBB 1998	\N	2	\N	\N	\N	\N	\N	\N	f	0	12582912	1	library internal use	1787	2353	400	8,8,8	integer	3	0	7	\N	2.2	100	Dawson Grant	2006-06-27 00:00:00	f	\N	\N	\N	\N
347	1350	TIFF 6.0	Little Endian (PC)	Uncompressed	1	Adobe RBB 1998	\N	2	\N	\N	\N	\N	\N	\N	f	0	12897485	1	library internal use	1543	2755	400	8,8,8	integer	3	0	7	\N	2.2	100	Dawson Grant	2006-06-27 00:00:00	f	\N	\N	\N	\N
348	1351	TIFF 6.0	Little Endian (PC)	Uncompressed	1	Adobe RBB 1998	\N	2	\N	\N	\N	\N	\N	\N	f	0	24326963	1	library internal use	3390	2397	400	8,8,8	integer	3	0	7	\N	2.2	100	Dawson Grant	2006-06-27 00:00:00	f	\N	\N	\N	\N
349	1352	TIFF 6.0	Little Endian (PC)	Uncompressed	1	Adobe RBB 1998	\N	2	\N	\N	\N	\N	\N	\N	f	0	43201331	1	library internal use	4288	3356	400	8,8,8	integer	3	0	7	\N	2.2	100	Dawson Grant	2006-06-27 00:00:00	f	\N	\N	\N	\N
135	1111	TIFF 6.0	Little Endian (PC)	Uncompressed	1	Adobe RGB 1998	\N	2	\N	\N	\N	\N	\N	\N	f	0	25165824	1	library internal use	2550	3294	400	8,8,8	integer	3	0	7	\N	2.2	100	Dawson Grant	2006-06-13 00:00:00	f	\N	\N	\N	\N
136	1112	TIFF 6.0	Little Endian (PC)	Uncompressed	1	Adobe RGB 1998	\N	2	\N	\N	\N	\N	\N	\N	f	0	25165824	1	library internal use	2550	3294	400	8,8,8	integer	3	0	7	\N	2.2	100	Dawson Grant	2006-06-13 00:00:00	f	\N	\N	\N	\N
137	1113	TIFF 6.0	Little Endian (PC)	Uncompressed	1	Adobe RGB 1998	\N	2	\N	\N	\N	\N	\N	\N	f	0	14155776	1	library internal use	1778	2654	400	8,8,8	integer	3	0	7	\N	2.2	100	Dawson Grant	2006-06-13 00:00:00	f	\N	\N	\N	\N
138	1114	TIFF 6.0	Little Endian (PC)	Uncompressed	1	Adobe RGB 1998	\N	2	\N	\N	\N	\N	\N	\N	f	0	26738688	1	library internal use	2550	3497	400	8,8,8	integer	3	0	7	\N	2.2	100	Dawson Grant	2006-06-13 00:00:00	f	\N	\N	\N	\N
139	1115	TIFF 6.0	Little Endian (PC)	Uncompressed	1	Adobe RGB 1998	\N	2	\N	\N	\N	\N	\N	\N	f	0	26738688	1	library internal use	2550	3497	400	8,8,8	integer	3	0	7	\N	2.2	100	Dawson Grant	2006-06-13 00:00:00	f	\N	\N	\N	\N
140	1116	TIFF 6.0	Little Endian (PC)	Uncompressed	1	Adobe RGB 1998	\N	2	\N	\N	\N	\N	\N	\N	f	0	26738688	1	library internal use	2550	3497	400	8,8,8	integer	3	0	7	\N	2.2	100	Dawson Grant	2006-06-13 00:00:00	f	\N	\N	\N	\N
141	1117	TIFF 6.0	Little Endian (PC)	Uncompressed	1	Adobe RGB 1998	\N	2	\N	\N	\N	\N	\N	\N	f	0	26738688	1	library internal use	2550	3497	400	8,8,8	integer	3	0	7	\N	2.2	100	Dawson Grant	2006-06-13 00:00:00	f	\N	\N	\N	\N
144	1120	TIFF 6.0	Little Endian (PC)	Uncompressed	1	Adobe RGB 1998	\N	2	\N	\N	\N	\N	\N	\N	f	0	13107200	1	library internal use	1282	3124	400	8,8,8	integer	3	0	7	\N	2.2	100	Dawson Grant	2006-06-13 00:00:00	f	\N	\N	\N	\N
145	1121	TIFF 6.0	Little Endian (PC)	Uncompressed	1	Adobe RGB 1998	\N	2	\N	\N	\N	\N	\N	\N	f	0	22754099	1	library internal use	2550	3118	400	8,8,8	integer	3	0	7	\N	2.2	100	Dawson Grant	2006-06-13 00:00:00	f	\N	\N	\N	\N
146	1122	TIFF 6.0	Little Endian (PC)	Uncompressed	1	Adobe RGB 1998	\N	2	\N	\N	\N	\N	\N	\N	f	0	22754099	1	library internal use	2550	3118	400	8,8,8	integer	3	0	7	\N	2.2	100	Dawson Grant	2006-06-13 00:00:00	f	\N	\N	\N	\N
147	1123	TIFF 6.0	Little Endian (PC)	Uncompressed	1	Adobe RGB 1998	\N	2	\N	\N	\N	\N	\N	\N	f	0	22754099	1	library internal use	2550	3118	400	8,8,8	integer	3	0	7	\N	2.2	100	Dawson Grant	2006-06-13 00:00:00	f	\N	\N	\N	\N
148	1124	TIFF 6.0	Little Endian (PC)	Uncompressed	1	Adobe RGB 1998	\N	2	\N	\N	\N	\N	\N	\N	f	0	22754099	1	library internal use	2550	3118	400	8,8,8	integer	3	0	7	\N	2.2	100	Dawson Grant	2006-06-13 00:00:00	f	\N	\N	\N	\N
149	1125	TIFF 6.0	Little Endian (PC)	Uncompressed	1	Adobe RGB 1998	\N	2	\N	\N	\N	\N	\N	\N	f	0	22754099	1	library internal use	2550	3118	400	8,8,8	integer	3	0	7	\N	2.2	100	Dawson Grant	2006-06-13 00:00:00	f	\N	\N	\N	\N
150	1126	TIFF 6.0	Little Endian (PC)	Uncompressed	1	Adobe RGB 1998	\N	2	\N	\N	\N	\N	\N	\N	f	0	12058624	1	library internal use	1282	3124	400	8,8,8	integer	3	0	7	\N	2.2	100	Dawson Grant	2006-06-13 00:00:00	f	\N	\N	\N	\N
155	1131	TIFF 6.0	Little Endian (PC)	Uncompressed	1	Adobe RGB 1998	\N	2	\N	\N	\N	\N	\N	\N	f	0	25165824	1	library internal use	2550	3294	400	8,8,8	integer	3	0	7	\N	2.2	100	Dawson Grant	2006-06-13 00:00:00	f	\N	\N	\N	\N
156	1132	TIFF 6.0	Little Endian (PC)	Uncompressed	1	Adobe RGB 1998	\N	2	\N	\N	\N	\N	\N	\N	f	0	25165824	1	library internal use	2550	3294	400	8,8,8	integer	3	0	7	\N	2.2	100	Dawson Grant	2006-06-13 00:00:00	f	\N	\N	\N	\N
157	1133	TIFF 6.0	Little Endian (PC)	Uncompressed	1	Adobe RGB 1998	\N	2	\N	\N	\N	\N	\N	\N	f	0	14470348	1	library internal use	1778	2719	400	8,8,8	integer	3	0	7	\N	2.2	100	Dawson Grant	2006-06-13 00:00:00	f	\N	\N	\N	\N
158	1134	TIFF 6.0	Little Endian (PC)	Uncompressed	1	Adobe RGB 1998	\N	2	\N	\N	\N	\N	\N	\N	f	0	14470348	1	library internal use	1778	2719	400	8,8,8	integer	3	0	7	\N	2.2	100	Dawson Grant	2006-06-13 00:00:00	f	\N	\N	\N	\N
162	1138	TIFF 6.0	Little Endian (PC)	Uncompressed	1	Adobe RGB 1998	\N	2	\N	\N	\N	\N	\N	\N	f	0	25060966	1	library internal use	2550	3275	400	8,8,8	integer	3	0	7	\N	2.2	100	Dawson Grant	2006-06-13 00:00:00	f	\N	\N	\N	\N
163	1139	TIFF 6.0	Little Endian (PC)	Uncompressed	1	Adobe RGB 1998	\N	2	\N	\N	\N	\N	\N	\N	f	0	25060966	1	library internal use	2550	3275	400	8,8,8	integer	3	0	7	\N	2.2	100	Dawson Grant	2006-06-13 00:00:00	f	\N	\N	\N	\N
164	1140	TIFF 6.0	Little Endian (PC)	Uncompressed	1	Adobe RGB 1998	\N	2	\N	\N	\N	\N	\N	\N	f	0	25060966	1	library internal use	2550	3275	400	8,8,8	integer	3	0	7	\N	2.2	100	Dawson Grant	2006-06-13 00:00:00	f	\N	\N	\N	\N
179	1164	TIFF 6.0	Little Endian (PC)	Uncompressed	1	Adobe RGB 1998	\N	2	\N	\N	\N	\N	\N	\N	f	0	13631488	1	library internal use	1665	3355	400	8,8,8	integer	3	0	7	\N	2.2	100	Dawson Grant	2006-06-14 00:00:00	f	\N	\N	\N	\N
180	1165	TIFF 6.0	Little Endian (PC)	Uncompressed	1	Adobe RGB 1998	\N	2	\N	\N	\N	\N	\N	\N	f	0	13631488	1	library internal use	1665	3355	400	8,8,8	integer	3	0	7	\N	2.2	100	Dawson Grant	2006-06-14 00:00:00	f	\N	\N	\N	\N
183	1168	TIFF 6.0	Little Endian (PC)	Uncompressed	1	Adobe RGB 1998	\N	2	\N	\N	\N	\N	\N	\N	f	0	15309210	1	library internal use	1543	3312	400	8,8,8	integer	3	0	7	\N	2.2	100	Dawson Grant	2006-06-14 00:00:00	f	\N	\N	\N	\N
185	1170	TIFF 6.0	Little Endian (PC)	Uncompressed	1	Adobe RGB 1998	\N	2	\N	\N	\N	\N	\N	\N	f	0	44040192	1	library internal use	4236	3217	400	8,8,8	integer	3	0	7	\N	2.2	100	Dawson Grant	2006-06-14 00:00:00	f	\N	\N	\N	\N
186	1171	TIFF 6.0	Little Endian (PC)	Uncompressed	1	Adobe RGB 1998	\N	2	\N	\N	\N	\N	\N	\N	f	0	44040192	1	library internal use	4236	3217	400	8,8,8	integer	3	0	7	\N	2.2	100	Dawson Grant	2006-06-14 00:00:00	f	\N	\N	\N	\N
187	1172	TIFF 6.0	Little Endian (PC)	Uncompressed	1	Adobe RGB 1998	\N	2	\N	\N	\N	\N	\N	\N	f	0	44040192	1	library internal use	4236	3217	400	8,8,8	integer	3	0	7	\N	2.2	100	Dawson Grant	2006-06-14 00:00:00	f	\N	\N	\N	\N
188	1173	TIFF 6.0	Little Endian (PC)	Uncompressed	1	Adobe RGB 1998	\N	2	\N	\N	\N	\N	\N	\N	f	0	44040192	1	library internal use	4236	3217	400	8,8,8	integer	3	0	7	\N	2.2	100	Dawson Grant	2006-06-14 00:00:00	f	\N	\N	\N	\N
189	1174	TIFF 6.0	Little Endian (PC)	Uncompressed	1	Adobe RGB 1998	\N	2	\N	\N	\N	\N	\N	\N	f	0	44040192	1	library internal use	4236	3217	400	8,8,8	integer	3	0	7	\N	2.2	100	Dawson Grant	2006-06-14 00:00:00	f	\N	\N	\N	\N
190	1175	TIFF 6.0	Little Endian (PC)	Uncompressed	1	Adobe RGB 1998	\N	2	\N	\N	\N	\N	\N	\N	f	0	44040192	1	library internal use	4236	3217	400	8,8,8	integer	3	0	7	\N	2.2	100	Dawson Grant	2006-06-14 00:00:00	f	\N	\N	\N	\N
191	1176	TIFF 6.0	Little Endian (PC)	Uncompressed	1	Adobe RGB 1998	\N	2	\N	\N	\N	\N	\N	\N	f	0	44459622	1	library internal use	3400	4358	400	8,8,8	integer	3	0	7	\N	2.2	100	Dawson Grant	2006-06-14 00:00:00	f	\N	\N	\N	\N
192	1177	TIFF 6.0	Little Endian (PC)	Uncompressed	1	Adobe RGB 1998	\N	2	\N	\N	\N	\N	\N	\N	f	0	44459622	1	library internal use	3400	4358	400	8,8,8	integer	3	0	7	\N	2.2	100	Dawson Grant	2006-06-14 00:00:00	f	\N	\N	\N	\N
195	1180	TIFF 6.0	Little Endian (PC)	Uncompressed	1	Adobe RGB 1998	\N	2	\N	\N	\N	\N	\N	\N	f	0	44459622	1	library internal use	3400	4358	400	8,8,8	integer	3	0	7	\N	2.2	100	Dawson Grant	2006-06-14 00:00:00	f	\N	\N	\N	\N
194	1179	TIFF 6.0	Little Endian (PC)	Uncompressed	1	Adobe RGB 1998	\N	2	\N	\N	\N	\N	\N	\N	f	0	44459622	1	library internal use	3400	4358	400	8,8,8	integer	3	0	7	\N	2.2	100	Dawson Grant	2006-06-14 00:00:00	f	\N	\N	\N	\N
196	1181	TIFF 6.0	Little Endian (PC)	Uncompressed	1	Adobe RGB 1998	\N	2	\N	\N	\N	\N	\N	\N	f	0	44459622	1	library internal use	3400	4358	400	8,8,8	integer	3	0	7	\N	2.2	100	Dawson Grant	2006-06-14 00:00:00	f	\N	\N	\N	\N
197	1182	TIFF 6.0	Little Endian (PC)	Uncompressed	1	Adobe RGB 1998	\N	2	\N	\N	\N	\N	\N	\N	f	0	44459622	1	library internal use	3400	4358	400	8,8,8	integer	3	0	7	\N	2.2	100	Dawson Grant	2006-06-14 00:00:00	f	\N	\N	\N	\N
198	1183	TIFF 6.0	Little Endian (PC)	Uncompressed	1	Adobe RGB 1998	\N	2	\N	\N	\N	\N	\N	\N	f	0	44459622	1	library internal use	3400	4358	400	8,8,8	integer	3	0	7	\N	2.2	100	Dawson Grant	2006-06-14 00:00:00	f	\N	\N	\N	\N
199	1184	TIFF 6.0	Little Endian (PC)	Uncompressed	1	Adobe RGB 1998	\N	2	\N	\N	\N	\N	\N	\N	f	0	44774195	1	library internal use	3391	4401	400	8,8,8	integer	3	0	7	\N	2.2	100	Dawson Grant	2006-06-14 00:00:00	f	\N	\N	\N	\N
200	1185	TIFF 6.0	Little Endian (PC)	Uncompressed	1	Adobe RGB 1998	\N	2	\N	\N	\N	\N	\N	\N	f	0	44774195	1	library internal use	3391	4401	400	8,8,8	integer	3	0	7	\N	2.2	100	Dawson Grant	2006-06-14 00:00:00	f	\N	\N	\N	\N
203	1188	TIFF 6.0	Little Endian (PC)	Uncompressed	1	Adobe RGB 1998	\N	2	\N	\N	\N	\N	\N	\N	f	0	44669338	1	library internal use	3400	4375	400	8,8,8	integer	3	0	7	\N	2.2	100	Dawson Grant	2006-06-14 00:00:00	f	\N	\N	\N	\N
201	1186	TIFF 6.0	Little Endian (PC)	Uncompressed	1	Adobe RGB 1998	\N	2	\N	\N	\N	\N	\N	\N	f	0	44669338	1	library internal use	3400	4375	400	8,8,8	integer	3	0	7	\N	2.2	100	Dawson Grant	2006-06-14 00:00:00	f	\N	\N	\N	\N
202	1187	TIFF 6.0	Little Endian (PC)	Uncompressed	1	Adobe RGB 1998	\N	2	\N	\N	\N	\N	\N	\N	f	0	44669338	1	library internal use	3400	4375	400	8,8,8	integer	3	0	7	\N	2.2	100	Dawson Grant	2006-06-14 00:00:00	f	\N	\N	\N	\N
208	1193	TIFF 6.0	Little Endian (PC)	Uncompressed	1	Adobe RGB 1998	\N	2	\N	\N	\N	\N	\N	\N	f	0	45088768	1	library internal use	3208	4680	400	8,8,8	integer	3	0	7	\N	2.2	100	Dawson Grant	2006-06-14 00:00:00	f	\N	\N	\N	\N
209	1194	TIFF 6.0	Little Endian (PC)	Uncompressed	1	Adobe RGB 1998	\N	2	\N	\N	\N	\N	\N	\N	f	0	45088768	1	library internal use	3208	4680	400	8,8,8	integer	3	0	7	\N	2.2	100	Dawson Grant	2006-06-14 00:00:00	f	\N	\N	\N	\N
210	1195	TIFF 6.0	Little Endian (PC)	Uncompressed	1	Adobe RGB 1998	\N	2	\N	\N	\N	\N	\N	\N	f	0	41313894	1	library internal use	3077	3913	400	8,8,8	integer	3	0	7	\N	2.2	100	Dawson Grant	2006-06-14 00:00:00	f	\N	\N	\N	\N
211	1196	TIFF 6.0	Little Endian (PC)	Uncompressed	1	Adobe RGB 1998	\N	2	\N	\N	\N	\N	\N	\N	f	0	41313894	1	library internal use	3077	3913	400	8,8,8	integer	3	0	7	\N	2.2	100	Dawson Grant	2006-06-14 00:00:00	f	\N	\N	\N	\N
212	1197	TIFF 6.0	Little Endian (PC)	Uncompressed	1	Adobe RGB 1998	\N	2	\N	\N	\N	\N	\N	\N	f	0	43725619	1	library internal use	3348	4349	400	8,8,8	integer	3	0	7	\N	2.2	100	Dawson Grant	2006-06-14 00:00:00	f	\N	\N	\N	\N
213	1198	TIFF 6.0	Little Endian (PC)	Uncompressed	1	Adobe RGB 1998	\N	2	\N	\N	\N	\N	\N	\N	f	0	43725619	1	library internal use	3348	4349	400	8,8,8	integer	3	0	7	\N	2.2	100	Dawson Grant	2006-06-14 00:00:00	f	\N	\N	\N	\N
214	1199	TIFF 6.0	Little Endian (PC)	Uncompressed	1	Adobe RGB 1998	\N	2	\N	\N	\N	\N	\N	\N	f	0	44564480	1	library internal use	3400	4366	400	8,8,8	integer	3	0	7	\N	2.2	100	Dawson Grant	2006-06-14 00:00:00	f	\N	\N	\N	\N
215	1200	TIFF 6.0	Little Endian (PC)	Uncompressed	1	Adobe RGB 1998	\N	2	\N	\N	\N	\N	\N	\N	f	0	44564480	1	library internal use	3400	4366	400	8,8,8	integer	3	0	7	\N	2.2	100	Dawson Grant	2006-06-14 00:00:00	f	\N	\N	\N	\N
216	1201	TIFF 6.0	Little Endian (PC)	Uncompressed	1	Adobe RGB 1998	\N	2	\N	\N	\N	\N	\N	\N	f	0	44564480	1	library internal use	3400	4366	400	8,8,8	integer	3	0	7	\N	2.2	100	Dawson Grant	2006-06-14 00:00:00	f	\N	\N	\N	\N
217	1202	TIFF 6.0	Little Endian (PC)	Uncompressed	1	Adobe RGB 1998	\N	2	\N	\N	\N	\N	\N	\N	f	0	44564480	1	library internal use	3400	4366	400	8,8,8	integer	3	0	7	\N	2.2	100	Dawson Grant	2006-06-14 00:00:00	f	\N	\N	\N	\N
218	1203	TIFF 6.0	Little Endian (PC)	Uncompressed	1	Adobe RGB 1998	\N	2	\N	\N	\N	\N	\N	\N	f	0	44459622	1	library internal use	3391	4375	400	8,8,8	integer	3	0	7	\N	2.2	100	Dawson Grant	2006-06-14 00:00:00	f	\N	\N	\N	\N
219	1204	TIFF 6.0	Little Endian (PC)	Uncompressed	1	Adobe RGB 1998	\N	2	\N	\N	\N	\N	\N	\N	f	0	44459622	1	library internal use	3391	4375	400	8,8,8	integer	3	0	7	\N	2.2	100	Dawson Grant	2006-06-14 00:00:00	f	\N	\N	\N	\N
220	1205	TIFF 6.0	Little Endian (PC)	Uncompressed	1	Adobe RGB 1998	\N	2	\N	\N	\N	\N	\N	\N	f	0	44459622	1	library internal use	3391	4375	400	8,8,8	integer	3	0	7	\N	2.2	100	Dawson Grant	2006-06-14 00:00:00	f	\N	\N	\N	\N
221	1206	TIFF 6.0	Little Endian (PC)	Uncompressed	1	Adobe RGB 1998	\N	2	\N	\N	\N	\N	\N	\N	f	0	44459622	1	library internal use	3391	4375	400	8,8,8	integer	3	0	7	\N	2.2	100	Dawson Grant	2006-06-14 00:00:00	f	\N	\N	\N	\N
222	1207	TIFF 6.0	Little Endian (PC)	Uncompressed	1	Adobe RGB 1998	\N	2	\N	\N	\N	\N	\N	\N	f	0	44459622	1	library internal use	3391	4375	400	8,8,8	integer	3	0	7	\N	2.2	100	Dawson Grant	2006-06-14 00:00:00	f	\N	\N	\N	\N
223	1208	TIFF 6.0	Little Endian (PC)	Uncompressed	1	Adobe RGB 1998	\N	2	\N	\N	\N	\N	\N	\N	f	0	44459622	1	library internal use	3391	4375	400	8,8,8	integer	3	0	7	\N	2.2	100	Dawson Grant	2006-06-14 00:00:00	f	\N	\N	\N	\N
224	1209	TIFF 6.0	Little Endian (PC)	Uncompressed	1	Adobe RGB 1998	\N	2	\N	\N	\N	\N	\N	\N	f	0	44459622	1	library internal use	3391	4375	400	8,8,8	integer	3	0	7	\N	2.2	100	Dawson Grant	2006-06-14 00:00:00	f	\N	\N	\N	\N
225	1210	TIFF 6.0	Little Endian (PC)	Uncompressed	1	Adobe RGB 1998	\N	2	\N	\N	\N	\N	\N	\N	f	0	44459622	1	library internal use	3391	4375	400	8,8,8	integer	3	0	7	\N	2.2	100	Dawson Grant	2006-06-14 00:00:00	f	\N	\N	\N	\N
274	1277	TIFF 6.0	Little Endian (PC)	Uncompressed	1	Adobe RGB 1998	\N	2	\N	\N	\N	\N	\N	\N	f	0	18559795	1	library internal use	3330	1839	400	8,8,8	integer	3	0	7	\N	2.2	100	Dawson Grant	2006-06-23 00:00:00	f	\N	\N	\N	\N
275	1278	TIFF 6.0	Little Endian (PC)	Uncompressed	1	Adobe RGB 1998	\N	2	\N	\N	\N	\N	\N	\N	f	0	20027802	1	library internal use	2023	3303	400	8,8,8	integer	3	0	7	\N	2.2	100	Dawson Grant	2006-06-23 00:00:00	f	\N	\N	\N	\N
276	1279	TIFF 6.0	Little Endian (PC)	Uncompressed	1	Adobe RGB 1998	\N	2	\N	\N	\N	\N	\N	\N	f	0	43725619	1	library internal use	3330	4375	400	8,8,8	integer	3	0	7	\N	2.2	100	Dawson Grant	2006-06-23 00:00:00	f	\N	\N	\N	\N
277	1280	TIFF 6.0	Little Endian (PC)	Uncompressed	1	Adobe RGB 1998	\N	2	\N	\N	\N	\N	\N	\N	f	0	43725619	1	library internal use	3330	4375	400	8,8,8	integer	3	0	7	\N	2.2	100	Dawson Grant	2006-06-23 00:00:00	f	\N	\N	\N	\N
278	1281	TIFF 6.0	Little Endian (PC)	Uncompressed	1	Adobe RGB 1998	\N	2	\N	\N	\N	\N	\N	\N	f	0	43725619	1	library internal use	3330	4375	400	8,8,8	integer	3	0	7	\N	2.2	100	Dawson Grant	2006-06-23 00:00:00	f	\N	\N	\N	\N
279	1282	TIFF 6.0	Little Endian (PC)	Uncompressed	1	Adobe RGB 1998	\N	2	\N	\N	\N	\N	\N	\N	f	0	43725619	1	library internal use	3330	4375	400	8,8,8	integer	3	0	7	\N	2.2	100	Dawson Grant	2006-06-23 00:00:00	f	\N	\N	\N	\N
280	1283	TIFF 6.0	Little Endian (PC)	Uncompressed	1	Adobe RGB 1998	\N	2	\N	\N	\N	\N	\N	\N	f	0	43725619	1	library internal use	3330	4375	400	8,8,8	integer	3	0	7	\N	2.2	100	Dawson Grant	2006-06-23 00:00:00	f	\N	\N	\N	\N
281	1284	TIFF 6.0	Little Endian (PC)	Uncompressed	1	Adobe RGB 1998	\N	2	\N	\N	\N	\N	\N	\N	f	0	43725619	1	library internal use	3330	4375	400	8,8,8	integer	3	0	7	\N	2.2	100	Dawson Grant	2006-06-23 00:00:00	f	\N	\N	\N	\N
282	1285	TIFF 6.0	Little Endian (PC)	Uncompressed	1	Adobe RGB 1998	\N	2	\N	\N	\N	\N	\N	\N	f	0	43725619	1	library internal use	3330	4375	400	8,8,8	integer	3	0	7	\N	2.2	100	Dawson Grant	2006-06-23 00:00:00	f	\N	\N	\N	\N
290	1293	TIFF 6.0	Little Endian (PC)	Uncompressed	1	Adobe RGB 1998	\N	2	\N	\N	\N	\N	\N	\N	f	0	13002342	1	library internal use	2101	2057	400	8,8,8	integer	3	0	7	\N	2.2	100	Dawson Grant	2006-06-23 00:00:00	f	\N	\N	\N	\N
291	1294	TIFF 6.0	Little Endian (PC)	Uncompressed	1	Adobe RGB 1998	\N	2	\N	\N	\N	\N	\N	\N	f	0	13002342	1	library internal use	2101	2057	400	8,8,8	integer	3	0	7	\N	2.2	100	Dawson Grant	2006-06-23 00:00:00	f	\N	\N	\N	\N
292	1295	TIFF 6.0	Little Endian (PC)	Uncompressed	1	Adobe RGB 1998	\N	2	\N	\N	\N	\N	\N	\N	f	0	13002342	1	library internal use	2101	2057	400	8,8,8	integer	3	0	7	\N	2.2	100	Dawson Grant	2006-06-23 00:00:00	f	\N	\N	\N	\N
293	1296	TIFF 6.0	Little Endian (PC)	Uncompressed	1	Adobe RGB 1998	\N	2	\N	\N	\N	\N	\N	\N	f	0	13002342	1	library internal use	2101	2057	400	8,8,8	integer	3	0	7	\N	2.2	100	Dawson Grant	2006-06-23 00:00:00	f	\N	\N	\N	\N
294	1297	TIFF 6.0	Little Endian (PC)	Uncompressed	1	Adobe RGB 1998	\N	2	\N	\N	\N	\N	\N	\N	f	0	651166	1	library internal use	1055	2057	400	8,8,8	integer	3	0	7	\N	2.2	100	Dawson Grant	2006-06-23 00:00:00	f	\N	\N	\N	\N
295	1298	TIFF 6.0	Little Endian (PC)	Uncompressed	1	Adobe RGB 1998	\N	2	\N	\N	\N	\N	\N	\N	f	0	651166	1	library internal use	1055	2057	400	8,8,8	integer	3	0	7	\N	2.2	100	Dawson Grant	2006-06-23 00:00:00	f	\N	\N	\N	\N
296	1299	TIFF 6.0	Little Endian (PC)	Uncompressed	1	Adobe RGB 1998	\N	2	\N	\N	\N	\N	\N	\N	f	0	13002342	1	library internal use	2101	2057	400	8,8,8	integer	3	0	7	\N	2.2	100	Dawson Grant	2006-06-23 00:00:00	f	\N	\N	\N	\N
297	1300	TIFF 6.0	Little Endian (PC)	Uncompressed	1	Adobe RGB 1998	\N	2	\N	\N	\N	\N	\N	\N	f	0	13002342	1	library internal use	2101	2057	400	8,8,8	integer	3	0	7	\N	2.2	100	Dawson Grant	2006-06-23 00:00:00	f	\N	\N	\N	\N
298	1301	TIFF 6.0	Little Endian (PC)	Uncompressed	1	Adobe RGB 1998	\N	2	\N	\N	\N	\N	\N	\N	f	0	13002342	1	library internal use	2101	2057	400	8,8,8	integer	3	0	7	\N	2.2	100	Dawson Grant	2006-06-23 00:00:00	f	\N	\N	\N	\N
299	1302	TIFF 6.0	Little Endian (PC)	Uncompressed	1	Adobe RGB 1998	\N	2	\N	\N	\N	\N	\N	\N	f	0	13002342	1	library internal use	2101	2057	400	8,8,8	integer	3	0	7	\N	2.2	100	Dawson Grant	2006-06-23 00:00:00	f	\N	\N	\N	\N
300	1303	TIFF 6.0	Little Endian (PC)	Uncompressed	1	Adobe RGB 1998	\N	2	\N	\N	\N	\N	\N	\N	f	0	13002342	1	library internal use	2101	2057	400	8,8,8	integer	3	0	7	\N	2.2	100	Dawson Grant	2006-06-23 00:00:00	f	\N	\N	\N	\N
301	1304	TIFF 6.0	Little Endian (PC)	Uncompressed	1	Adobe RGB 1998	\N	2	\N	\N	\N	\N	\N	\N	f	0	13002342	1	library internal use	2101	2057	400	8,8,8	integer	3	0	7	\N	2.2	100	Dawson Grant	2006-06-23 00:00:00	f	\N	\N	\N	\N
570	1592	TIFF 6.0	Little Endian (PC)	Uncompressed	1	Adobe RGB 1998	\N	2	\N	\N	\N	\N	\N	\N	f	0	44249907	1	library internal use	3081	4793	400	8,8,8	integer	3	0	7	\N	2.2	100	\N	\N	f	\N	\N	\N	\N
2001	2034	TIFF 6.0	Little Endian (PC)	Uncompressed	1	\N	\N	2	\N	\N	\N	\N	\N	\N	f	0	44774195	0	exhibit	3391	4401	400	8,8,8	integer	3	0	0	\N	2.2	100	\N	\N	f	\N	\N	\N	\N
2003	2033	TIFF 6.0	Little Endian (PC)	uncompressed	1		\N	2	\N	\N	\N	\N	\N	\N	f	0	22020096	0	exhibit	2415	3042	400	8,8,8	integer	3	0	0	\N	2.2	100	\N	\N	f	\N	\N	\N	\N
2002	2030	TIFF 6.0	Little Endian (PC)	uncompressed	1		\N	2	\N	\N	\N	\N	\N	\N	f	0	98566144	0	exhibit	4590	7158	400	8,8,8	integer	3	0	0	\N	2.2	100	\N	\N	f	\N	\N	\N	\N
2004	2035	TIFF 6.0	Little Endian (PC)	uncompressed	1		\N	2	\N	\N	\N	\N	\N	\N	f	0	44564480	0	exhibit	3391	4384	400	8,8,8	integer	3	0	0	\N	2.2	100	\N	\N	f	\N	\N	\N	\N
2005	2036	TIFF 6.0	Little Endian (PC)	uncompressed	1		\N	2	\N	\N	\N	\N	\N	\N	f	0	44459622	0	exhibit	3391	4375	400	8,8,8	integer	3	0	0	\N	2.2	100	\N	\N	f	\N	\N	\N	\N
2006	2073	TIFF 6.0	Little Endian (PC)	Uncompressed	1	Greyscale	\N	2	\N	\N	\N	\N	\N	\N	f	0	3879731	1	library internal use	2432	1595	400	8,8,8	integer	3	0	7	\N	2.2	100	greyscale	\N	f	\N	\N	\N	\N
2007	2075	TIFF 6.0	Little Endian (PC)	uncompressed	1		\N	2	\N	\N	\N	\N	\N	\N	f	0	15938355	0	exhibit	2649	2005	400	8,8,8	integer	3	0	0	\N	2.2	100	\N	\N	f	\N	\N	\N	\N
2008	2076	TIFF 6.0	Little Endian (PC)	uncompressed	1		\N	2	\N	\N	\N	\N	\N	\N	f	0	31247565	0	exhibit	3730	2790	400	8,8,8	integer	3	0	0	\N	2.2	100	\N	\N	f	\N	\N	\N	\N
2009	2078	TIFF 6.0	Little Endian (PC)	uncompressed	1		\N	2	\N	\N	\N	\N	\N	\N	f	0	69206016	0	exhibit	7046	3273	400	8,8,8	integer	3	0	0	\N	2.2	100	\N	\N	f	\N	\N	\N	\N
2010	2079	TIFF 6.0	Little Endian (PC)	uncompressed	1		\N	2	\N	\N	\N	\N	\N	\N	f	0	84620083	0	exhibit	8388	3364	400	8,8,8	integer	3	0	0	\N	2.2	100	\N	\N	f	\N	\N	\N	\N
2011	2102	TIFF 6.0	Little Endian (PC)	uncompressed	1		\N	2	\N	\N	\N	\N	\N	\N	f	0	44879053	0	exhibit	4026	3720	400	8,8,8	integer	3	0	0	\N	2.2	100	\N	\N	f	\N	\N	\N	\N
2012	2109	TIFF 6.0	Little Endian (PC)	uncompressed	1		\N	2	\N	\N	\N	\N	\N	\N	f	0	79901491	0	exhibit	8211	3243	400	8,8,8	integer	3	0	0	\N	2.2	100	\N	\N	f	\N	\N	\N	\N
2013	2110	TIFF 6.0	Little Endian (PC)	uncompressed	1		\N	2	\N	\N	\N	\N	\N	\N	f	0	84515226	0	exhibit	8430	3342	400	8,8,8	integer	3	0	0	\N	2.2	100	\N	\N	f	\N	\N	\N	\N
2014	2111	TIFF 6.0	Little Endian (PC)	uncompressed	1		\N	2	\N	\N	\N	\N	\N	\N	f	0	68996301	0	exhibit	6981	3293	400	8,8,8	integer	3	0	0	\N	2.2	100	\N	\N	f	\N	\N	\N	\N
2015	2112	TIFF 6.0	Little Endian (PC)	uncompressed	1	Adobe RGB 1998	\N	2	\N	\N	\N	\N	\N	\N	f	0	19608371	1	library internal use	1953	3347	400	8,8,8	integer	3	0	7	\N	2.2	100	\N	2006-09-19 00:00:00	f	\N	\N	\N	\N
2016	2115	TIFF 6.0	Little Endian (PC)	uncompressed	1	Adobe RGB 1998	\N	2	\N	\N	\N	\N	\N	\N	f	0	19503514	1	library internal use	1944	3347	400	8,8,8	integer	3	0	7	\N	2.2	100	\N	2006-09-19 00:00:00	f	\N	\N	\N	\N
2017	2116	TIFF 6.0	Little Endian (PC)	uncompressed	1	Adobe RGB 1998	\N	2	\N	\N	\N	\N	\N	\N	f	0	47710208	1	library internal use	3400	4680	400	8,8,8	integer	3	0	1	\N	2.2	100	\N	2006-09-19 00:00:00	f	\N	\N	\N	\N
2018	2118	TIFF 6.0	Little Endian (PC)	uncompressed	1	Adobe RGB 1998	\N	2	\N	\N	\N	\N	\N	\N	f	0	26424115	1	patron request	2432	3617	400	8,8,8	integer	3	0	7	\N	2.2	100	\N	2006-09-19 00:00:00	f	\N	\N	\N	\N
2019	2120	TIFF 6.0	Little Endian (PC)	uncompressed	1	Adobe RGB 1998	\N	2	\N	\N	\N	\N	\N	\N	f	0	26424115	1	patron request	2432	3625	400	8,8,8	integer	3	0	7	\N	2.2	100	\N	2006-09-20 00:00:00	f	\N	\N	\N	\N
2020	2122	TIFF 6.0	Little Endian (PC)	uncompressed	1	Adobe RGB 1998	\N	2	\N	\N	\N	\N	\N	\N	f	0	26109542	1	patron request	2415	3599	400	8,8,8	integer	3	0	7	\N	2.2	100	\N	2006-09-20 00:00:00	f	\N	\N	\N	\N
2021	2123	TIFF 6.0	Little Endian (PC)	uncompressed	1	Adobe RGB 1998	\N	2	\N	\N	\N	\N	\N	\N	f	0	26319258	1	patron request	2441	3591	400	8,8,8	integer	3	0	7	\N	2.2	100	\N	2006-09-20 00:00:00	f	\N	\N	\N	\N
2022	2124	TIFF 6.0	Little Endian (PC)	uncompressed	1	Adobe RGB 1998	\N	2	\N	\N	\N	\N	\N	\N	f	0	19608371	1	exhibit	2014	242	400	8,8,8	integer	3	0	7	\N	2.2	100	\N	2006-09-20 00:00:00	f	\N	\N	\N	\N
\.


--
-- Data for TOC entry 244 (OID 12747599)
-- Name: DigitalProvence; Type: TABLE DATA; Schema: public; Owner: jbwhite
--

COPY "DigitalProvence" ("ID", "Date", "StaffName", "Action", "TechImageID") FROM stdin;
46	2006-05-14 00:00:00	2	digitized original	51
47	2003-12-15 00:00:00	2	digitized photograph	52
48	2003-12-19 00:00:00	2	digitized photograph	53
49	2004-10-29 00:00:00	2	digitized photograph	\N
50	2004-10-29 00:00:00	2	digitized photograph	54
51	2006-06-06 00:00:00	2	cropped border and caption	52
52	2006-06-06 00:00:00	2	cropped border and caption	53
53	2006-06-06 00:00:00	2	cropped border and caption	54
54	2004-10-29 00:00:00	2	digitized photograph	55
55	2006-06-06 00:00:00	2	cropped border and caption	55
56	2005-10-21 00:00:00	\N	digitized manuscript	57
57	2006-06-07 00:00:00	2	cropped borders and caption	57
58	2006-06-08 00:00:00	1	Crop to remove caption	64
59	2006-06-09 00:00:00	1	Crop	67
60	2006-06-09 00:00:00	1	Crop	66
61	2006-06-09 00:00:00	1	Crop	65
62	2006-06-09 00:00:00	1	Crop	68
63	2006-06-09 00:00:00	1	Crop	69
64	2006-06-12 00:00:00	1	Crop	123
65	2006-06-12 00:00:00	1	Crop	125
66	2006-06-13 00:00:00	1	Crop	126
67	2006-06-13 00:00:00	1	reduced resolution from 1200 to 400	130
68	2006-06-15 00:00:00	1	Crop	240
69	2006-06-15 00:00:00	1	Crop	241
70	2006-06-19 00:00:00	1	Crop	254
71	2006-06-19 00:00:00	1	Crop	255
72	2006-06-19 00:00:00	1	Crop	256
73	2006-07-16 00:00:00	2	scanned image	588
\.


--
-- Data for TOC entry 245 (OID 12747638)
-- Name: TechMovingImage; Type: TABLE DATA; Schema: public; Owner: jbwhite
--

COPY "TechMovingImage" ("ID", "DateCaptured", "FormatName", "Resolution", "BitsPerSample", "Sampling", "AspectRatio", "CalibrationExtInt", "CalibrationLocation", "CalibrationType", "DataRate", "DataRateMode", "Duration", "FrameRate", "Note", "PixelsHorizontal", "PixelsVertical", "Scan", "Sound", "FileLoc") FROM stdin;
\.


--
-- Data for TOC entry 246 (OID 12747656)
-- Name: DigitalProvenenceSound; Type: TABLE DATA; Schema: public; Owner: jbwhite
--

COPY "DigitalProvenenceSound" ("ID", "Date", "StaffName", "Action", "TechSoundID") FROM stdin;
\.


--
-- Data for TOC entry 247 (OID 12750150)
-- Name: Subjects Detail; Type: TABLE DATA; Schema: public; Owner: jbwhite
--

COPY "Subjects Detail" ("ID", "ContentID", "FieldNames", "Headings") FROM stdin;
21	279	0	14
22	278	0	14
23	277	0	14
24	276	0	14
25	280	0	14
26	281	0	14
27	282	0	14
28	283	0	14
29	284	0	14
31	820	656	14
32	820	656	15
33	1020	650	\N
34	1020	0	15
2001	\N	611	0
2002	\N	630	0
2003	1280	\N	0
2004	2013	630	18
\.


--
-- Data for TOC entry 248 (OID 12753220)
-- Name: Authority; Type: TABLE DATA; Schema: public; Owner: jbwhite
--

COPY "Authority" (id, authority) FROM stdin;
0	Undefined
2	AAT
3	LCSH
4	local
\.


--
-- Data for TOC entry 249 (OID 12753242)
-- Name: Genres; Type: TABLE DATA; Schema: public; Owner: jbwhite
--

COPY "Genres" (id, genre, "Authority_id") FROM stdin;
1	test	2
2	test1	0
\.


--
-- Data for TOC entry 250 (OID 12753248)
-- Name: ContentGenre; Type: TABLE DATA; Schema: public; Owner: jbwhite
--

COPY "ContentGenre" (id, "Content_id", "FieldNames", "Genre_id") FROM stdin;
\.


--
-- TOC entry 141 (OID 12738948)
-- Name: CodecCreatorSound_ID; Type: INDEX; Schema: public; Owner: jbwhite
--

CREATE INDEX "CodecCreatorSound_ID" ON "CodecCreatorSound" USING btree ("ID");


--
-- TOC entry 144 (OID 12739966)
-- Name: Condition_ID; Type: INDEX; Schema: public; Owner: jbwhite
--

CREATE INDEX "Condition_ID" ON "Condition" USING btree ("ID");


--
-- TOC entry 146 (OID 12739977)
-- Name: ConditionDetail_ContentID; Type: INDEX; Schema: public; Owner: jbwhite
--

CREATE INDEX "ConditionDetail_ContentID" ON "ConditionDetail" USING btree ("ContentID");


--
-- TOC entry 147 (OID 12739978)
-- Name: ConditionDetail_SubjectID; Type: INDEX; Schema: public; Owner: jbwhite
--

CREATE INDEX "ConditionDetail_SubjectID" ON "ConditionDetail" USING btree ("ConditionID");


--
-- TOC entry 149 (OID 12740001)
-- Name: Content_ContentMain Entry; Type: INDEX; Schema: public; Owner: jbwhite
--

CREATE INDEX "Content_ContentMain Entry" ON "Content" USING btree ("Collection Number");


--
-- TOC entry 150 (OID 12740002)
-- Name: Content_ID; Type: INDEX; Schema: public; Owner: jbwhite
--

CREATE INDEX "Content_ID" ON "Content" USING btree ("ID");


--
-- TOC entry 151 (OID 12740003)
-- Name: Content_IdentifierType; Type: INDEX; Schema: public; Owner: jbwhite
--

CREATE INDEX "Content_IdentifierType" ON "Content" USING btree ("RecordIDType");


--
-- TOC entry 152 (OID 12740004)
-- Name: Content_OtherID; Type: INDEX; Schema: public; Owner: jbwhite
--

CREATE INDEX "Content_OtherID" ON "Content" USING btree ("OtherID");


--
-- TOC entry 154 (OID 12741792)
-- Name: ScannerCamera_ID; Type: INDEX; Schema: public; Owner: jbwhite
--

CREATE INDEX "ScannerCamera_ID" ON "ScannerCamera" USING btree ("ID");


--
-- TOC entry 156 (OID 12741809)
-- Name: Target_ID; Type: INDEX; Schema: public; Owner: jbwhite
--

CREATE INDEX "Target_ID" ON "Target" USING btree ("ID");


--
-- TOC entry 157 (OID 12741810)
-- Name: Target_TargetID; Type: INDEX; Schema: public; Owner: jbwhite
--

CREATE INDEX "Target_TargetID" ON "Target" USING btree ("TargetName");


--
-- TOC entry 160 (OID 12741838)
-- Name: TechSound_CodecCreator; Type: INDEX; Schema: public; Owner: jbwhite
--

CREATE INDEX "TechSound_CodecCreator" ON "TechSound" USING btree ("CodecCreator");


--
-- TOC entry 161 (OID 12741839)
-- Name: TechSound_CodecQuality; Type: INDEX; Schema: public; Owner: jbwhite
--

CREATE INDEX "TechSound_CodecQuality" ON "TechSound" USING btree ("CodecQuality");


--
-- TOC entry 162 (OID 12741840)
-- Name: TechSound_ID; Type: INDEX; Schema: public; Owner: jbwhite
--

CREATE INDEX "TechSound_ID" ON "TechSound" USING btree ("ID");


--
-- TOC entry 165 (OID 12742729)
-- Name: Form_FormForm; Type: INDEX; Schema: public; Owner: jbwhite
--

CREATE INDEX "Form_FormForm" ON "Form" USING btree ("Form");


--
-- TOC entry 166 (OID 12742730)
-- Name: Form_ID; Type: INDEX; Schema: public; Owner: jbwhite
--

CREATE INDEX "Form_ID" ON "Form" USING btree ("ID");


--
-- TOC entry 167 (OID 12742731)
-- Name: Form_identifyingFeatures; Type: INDEX; Schema: public; Owner: jbwhite
--

CREATE INDEX "Form_identifyingFeatures" ON "Form" USING btree ("IdentifyingFeatures");


--
-- TOC entry 169 (OID 12742806)
-- Name: Language_LangCode; Type: INDEX; Schema: public; Owner: jbwhite
--

CREATE INDEX "Language_LangCode" ON "Language" USING btree ("LangCode");


--
-- TOC entry 171 (OID 12743223)
-- Name: Location_ID; Type: INDEX; Schema: public; Owner: jbwhite
--

CREATE INDEX "Location_ID" ON "Location" USING btree ("ID");


--
-- TOC entry 173 (OID 12743243)
-- Name: Name_ID; Type: INDEX; Schema: public; Owner: jbwhite
--

CREATE INDEX "Name_ID" ON "Name" USING btree ("ID");


--
-- TOC entry 176 (OID 12743383)
-- Name: Restrictions_ID; Type: INDEX; Schema: public; Owner: jbwhite
--

CREATE INDEX "Restrictions_ID" ON "Restrictions" USING btree ("ID");


--
-- TOC entry 178 (OID 12743408)
-- Name: ResourceType_ID1; Type: INDEX; Schema: public; Owner: jbwhite
--

CREATE INDEX "ResourceType_ID1" ON "ResourceType" USING btree ("ID");


--
-- TOC entry 179 (OID 12743409)
-- Name: ResourceType_ResourceTypeResourceType; Type: INDEX; Schema: public; Owner: jbwhite
--

CREATE INDEX "ResourceType_ResourceTypeResourceType" ON "ResourceType" USING btree ("ResourceType");


--
-- TOC entry 181 (OID 12743432)
-- Name: RightsAccess_ID; Type: INDEX; Schema: public; Owner: jbwhite
--

CREATE INDEX "RightsAccess_ID" ON "RightsAccess" USING btree ("ID");


--
-- TOC entry 183 (OID 12744366)
-- Name: Role_RoleCode; Type: INDEX; Schema: public; Owner: jbwhite
--

CREATE INDEX "Role_RoleCode" ON "Role" USING btree ("RoleCode");


--
-- TOC entry 185 (OID 12744548)
-- Name: NameDetail_ContentID; Type: INDEX; Schema: public; Owner: jbwhite
--

CREATE INDEX "NameDetail_ContentID" ON "NameDetail" USING btree ("ContentID");


--
-- TOC entry 186 (OID 12744549)
-- Name: NameDetail_NameID; Type: INDEX; Schema: public; Owner: jbwhite
--

CREATE INDEX "NameDetail_NameID" ON "NameDetail" USING btree ("Name");


--
-- TOC entry 188 (OID 12744583)
-- Name: StaffName_ID; Type: INDEX; Schema: public; Owner: jbwhite
--

CREATE INDEX "StaffName_ID" ON "StaffName" USING btree ("ID");


--
-- TOC entry 190 (OID 12744609)
-- Name: SourceStillImage_ID; Type: INDEX; Schema: public; Owner: jbwhite
--

CREATE INDEX "SourceStillImage_ID" ON "SourceStillImage" USING btree ("ID");


--
-- TOC entry 192 (OID 12745578)
-- Name: SourceMovingImage_ID; Type: INDEX; Schema: public; Owner: jbwhite
--

CREATE INDEX "SourceMovingImage_ID" ON "SourceMovingImage" USING btree ("ID");


--
-- TOC entry 195 (OID 12745644)
-- Name: SourceSound_ID; Type: INDEX; Schema: public; Owner: jbwhite
--

CREATE INDEX "SourceSound_ID" ON "SourceSound" USING btree ("ID");


--
-- TOC entry 197 (OID 12746502)
-- Name: ColorSpace_ID; Type: INDEX; Schema: public; Owner: jbwhite
--

CREATE INDEX "ColorSpace_ID" ON "ColorSpace" USING btree ("ID");


--
-- TOC entry 199 (OID 12746528)
-- Name: Subjects_ID; Type: INDEX; Schema: public; Owner: jbwhite
--

CREATE INDEX "Subjects_ID" ON "Subjects" USING btree ("ID");


--
-- TOC entry 201 (OID 12746641)
-- Name: TechImages_ID; Type: INDEX; Schema: public; Owner: jbwhite
--

CREATE INDEX "TechImages_ID" ON "TechImages" USING btree ("ID");


--
-- TOC entry 203 (OID 12747606)
-- Name: DigitalProvence_ID; Type: INDEX; Schema: public; Owner: jbwhite
--

CREATE INDEX "DigitalProvence_ID" ON "DigitalProvence" USING btree ("ID");


--
-- TOC entry 204 (OID 12747607)
-- Name: DigitalProvence_TechImageID; Type: INDEX; Schema: public; Owner: jbwhite
--

CREATE INDEX "DigitalProvence_TechImageID" ON "DigitalProvence" USING btree ("TechImageID");


--
-- TOC entry 206 (OID 12747653)
-- Name: TechMovingImage_ID; Type: INDEX; Schema: public; Owner: jbwhite
--

CREATE INDEX "TechMovingImage_ID" ON "TechMovingImage" USING btree ("ID");


--
-- TOC entry 208 (OID 12747663)
-- Name: DigitalProvenenceSound_ID; Type: INDEX; Schema: public; Owner: jbwhite
--

CREATE INDEX "DigitalProvenenceSound_ID" ON "DigitalProvenenceSound" USING btree ("ID");


--
-- TOC entry 209 (OID 12747664)
-- Name: DigitalProvenenceSound_TechImageID; Type: INDEX; Schema: public; Owner: jbwhite
--

CREATE INDEX "DigitalProvenenceSound_TechImageID" ON "DigitalProvenenceSound" USING btree ("TechSoundID");


--
-- TOC entry 211 (OID 12750158)
-- Name: Subjects Detail_ContentID; Type: INDEX; Schema: public; Owner: jbwhite
--

CREATE INDEX "Subjects Detail_ContentID" ON "Subjects Detail" USING btree ("ContentID");


--
-- TOC entry 212 (OID 12750159)
-- Name: Subjects Detail_FieldNamesID; Type: INDEX; Schema: public; Owner: jbwhite
--

CREATE INDEX "Subjects Detail_FieldNamesID" ON "Subjects Detail" USING btree ("FieldNames");


--
-- TOC entry 213 (OID 12750160)
-- Name: Subjects Detail_ID; Type: INDEX; Schema: public; Owner: jbwhite
--

CREATE INDEX "Subjects Detail_ID" ON "Subjects Detail" USING btree ("ID");


--
-- TOC entry 142 (OID 12738946)
-- Name: CodecCreatorSound_pkey; Type: CONSTRAINT; Schema: public; Owner: jbwhite
--

ALTER TABLE ONLY "CodecCreatorSound"
    ADD CONSTRAINT "CodecCreatorSound_pkey" PRIMARY KEY ("ID");


--
-- TOC entry 145 (OID 12739962)
-- Name: Condition_pkey; Type: CONSTRAINT; Schema: public; Owner: jbwhite
--

ALTER TABLE ONLY "Condition"
    ADD CONSTRAINT "Condition_pkey" PRIMARY KEY ("ID");


--
-- TOC entry 143 (OID 12739964)
-- Name: Condition_Condition_key; Type: CONSTRAINT; Schema: public; Owner: jbwhite
--

ALTER TABLE ONLY "Condition"
    ADD CONSTRAINT "Condition_Condition_key" UNIQUE ("Condition");


--
-- TOC entry 148 (OID 12739975)
-- Name: ConditionDetail_pkey; Type: CONSTRAINT; Schema: public; Owner: jbwhite
--

ALTER TABLE ONLY "ConditionDetail"
    ADD CONSTRAINT "ConditionDetail_pkey" PRIMARY KEY ("ContentID", "ConditionID");


--
-- TOC entry 153 (OID 12739999)
-- Name: Content_pkey; Type: CONSTRAINT; Schema: public; Owner: jbwhite
--

ALTER TABLE ONLY "Content"
    ADD CONSTRAINT "Content_pkey" PRIMARY KEY ("ID");


--
-- TOC entry 155 (OID 12741790)
-- Name: ScannerCamera_pkey; Type: CONSTRAINT; Schema: public; Owner: jbwhite
--

ALTER TABLE ONLY "ScannerCamera"
    ADD CONSTRAINT "ScannerCamera_pkey" PRIMARY KEY ("ID");


--
-- TOC entry 158 (OID 12741807)
-- Name: Target_pkey; Type: CONSTRAINT; Schema: public; Owner: jbwhite
--

ALTER TABLE ONLY "Target"
    ADD CONSTRAINT "Target_pkey" PRIMARY KEY ("ID");


--
-- TOC entry 163 (OID 12741836)
-- Name: TechSound_pkey; Type: CONSTRAINT; Schema: public; Owner: jbwhite
--

ALTER TABLE ONLY "TechSound"
    ADD CONSTRAINT "TechSound_pkey" PRIMARY KEY ("ID");


--
-- TOC entry 164 (OID 12742684)
-- Name: Housing_pkey; Type: CONSTRAINT; Schema: public; Owner: jbwhite
--

ALTER TABLE ONLY "Housing"
    ADD CONSTRAINT "Housing_pkey" PRIMARY KEY ("ID");


--
-- TOC entry 168 (OID 12742727)
-- Name: Form_pkey; Type: CONSTRAINT; Schema: public; Owner: jbwhite
--

ALTER TABLE ONLY "Form"
    ADD CONSTRAINT "Form_pkey" PRIMARY KEY ("ID");


--
-- TOC entry 170 (OID 12742804)
-- Name: Language_pkey; Type: CONSTRAINT; Schema: public; Owner: jbwhite
--

ALTER TABLE ONLY "Language"
    ADD CONSTRAINT "Language_pkey" PRIMARY KEY ("ID");


--
-- TOC entry 172 (OID 12743221)
-- Name: Location_pkey; Type: CONSTRAINT; Schema: public; Owner: jbwhite
--

ALTER TABLE ONLY "Location"
    ADD CONSTRAINT "Location_pkey" PRIMARY KEY ("ID");


--
-- TOC entry 175 (OID 12743239)
-- Name: Name_pkey; Type: CONSTRAINT; Schema: public; Owner: jbwhite
--

ALTER TABLE ONLY "Name"
    ADD CONSTRAINT "Name_pkey" PRIMARY KEY ("ID");


--
-- TOC entry 174 (OID 12743241)
-- Name: Name_Name_key; Type: CONSTRAINT; Schema: public; Owner: jbwhite
--

ALTER TABLE ONLY "Name"
    ADD CONSTRAINT "Name_Name_key" UNIQUE ("Name");


--
-- TOC entry 177 (OID 12743381)
-- Name: Restrictions_pkey; Type: CONSTRAINT; Schema: public; Owner: jbwhite
--

ALTER TABLE ONLY "Restrictions"
    ADD CONSTRAINT "Restrictions_pkey" PRIMARY KEY ("ID");


--
-- TOC entry 180 (OID 12743406)
-- Name: ResourceType_pkey; Type: CONSTRAINT; Schema: public; Owner: jbwhite
--

ALTER TABLE ONLY "ResourceType"
    ADD CONSTRAINT "ResourceType_pkey" PRIMARY KEY ("ID");


--
-- TOC entry 182 (OID 12743430)
-- Name: RightsAccess_pkey; Type: CONSTRAINT; Schema: public; Owner: jbwhite
--

ALTER TABLE ONLY "RightsAccess"
    ADD CONSTRAINT "RightsAccess_pkey" PRIMARY KEY ("ID");


--
-- TOC entry 184 (OID 12744364)
-- Name: Role_pkey; Type: CONSTRAINT; Schema: public; Owner: jbwhite
--

ALTER TABLE ONLY "Role"
    ADD CONSTRAINT "Role_pkey" PRIMARY KEY ("ID");


--
-- TOC entry 187 (OID 12744546)
-- Name: NameDetail_pkey; Type: CONSTRAINT; Schema: public; Owner: jbwhite
--

ALTER TABLE ONLY "NameDetail"
    ADD CONSTRAINT "NameDetail_pkey" PRIMARY KEY ("ContentID", "Name");


--
-- TOC entry 189 (OID 12744581)
-- Name: StaffName_pkey; Type: CONSTRAINT; Schema: public; Owner: jbwhite
--

ALTER TABLE ONLY "StaffName"
    ADD CONSTRAINT "StaffName_pkey" PRIMARY KEY ("ID");


--
-- TOC entry 191 (OID 12744607)
-- Name: SourceStillImage_pkey; Type: CONSTRAINT; Schema: public; Owner: jbwhite
--

ALTER TABLE ONLY "SourceStillImage"
    ADD CONSTRAINT "SourceStillImage_pkey" PRIMARY KEY ("ID");


--
-- TOC entry 193 (OID 12745576)
-- Name: SourceMovingImage_pkey; Type: CONSTRAINT; Schema: public; Owner: jbwhite
--

ALTER TABLE ONLY "SourceMovingImage"
    ADD CONSTRAINT "SourceMovingImage_pkey" PRIMARY KEY ("ID");


--
-- TOC entry 194 (OID 12745587)
-- Name: Speed_pkey; Type: CONSTRAINT; Schema: public; Owner: jbwhite
--

ALTER TABLE ONLY "Speed"
    ADD CONSTRAINT "Speed_pkey" PRIMARY KEY ("ID");


--
-- TOC entry 196 (OID 12745642)
-- Name: SourceSound_pkey; Type: CONSTRAINT; Schema: public; Owner: jbwhite
--

ALTER TABLE ONLY "SourceSound"
    ADD CONSTRAINT "SourceSound_pkey" PRIMARY KEY ("ID");


--
-- TOC entry 198 (OID 12746500)
-- Name: ColorSpace_pkey; Type: CONSTRAINT; Schema: public; Owner: jbwhite
--

ALTER TABLE ONLY "ColorSpace"
    ADD CONSTRAINT "ColorSpace_pkey" PRIMARY KEY ("ID");


--
-- TOC entry 200 (OID 12746526)
-- Name: Subjects_pkey; Type: CONSTRAINT; Schema: public; Owner: jbwhite
--

ALTER TABLE ONLY "Subjects"
    ADD CONSTRAINT "Subjects_pkey" PRIMARY KEY ("ID");


--
-- TOC entry 202 (OID 12746639)
-- Name: TechImages_pkey; Type: CONSTRAINT; Schema: public; Owner: jbwhite
--

ALTER TABLE ONLY "TechImages"
    ADD CONSTRAINT "TechImages_pkey" PRIMARY KEY ("ID");


--
-- TOC entry 205 (OID 12747604)
-- Name: DigitalProvence_pkey; Type: CONSTRAINT; Schema: public; Owner: jbwhite
--

ALTER TABLE ONLY "DigitalProvence"
    ADD CONSTRAINT "DigitalProvence_pkey" PRIMARY KEY ("ID");


--
-- TOC entry 207 (OID 12747651)
-- Name: TechMovingImage_pkey; Type: CONSTRAINT; Schema: public; Owner: jbwhite
--

ALTER TABLE ONLY "TechMovingImage"
    ADD CONSTRAINT "TechMovingImage_pkey" PRIMARY KEY ("ID");


--
-- TOC entry 210 (OID 12747661)
-- Name: DigitalProvenenceSound_pkey; Type: CONSTRAINT; Schema: public; Owner: jbwhite
--

ALTER TABLE ONLY "DigitalProvenenceSound"
    ADD CONSTRAINT "DigitalProvenenceSound_pkey" PRIMARY KEY ("ID");


--
-- TOC entry 214 (OID 12750156)
-- Name: Subjects Detail_pkey; Type: CONSTRAINT; Schema: public; Owner: jbwhite
--

ALTER TABLE ONLY "Subjects Detail"
    ADD CONSTRAINT "Subjects Detail_pkey" PRIMARY KEY ("ID");


--
-- TOC entry 159 (OID 12752999)
-- Name: TechSoundContent#; Type: CONSTRAINT; Schema: public; Owner: jbwhite
--

ALTER TABLE ONLY "TechSound"
    ADD CONSTRAINT "TechSoundContent#" UNIQUE ("Content#");


--
-- TOC entry 215 (OID 12753222)
-- Name: Authority_pkey; Type: CONSTRAINT; Schema: public; Owner: jbwhite
--

ALTER TABLE ONLY "Authority"
    ADD CONSTRAINT "Authority_pkey" PRIMARY KEY (id);


--
-- TOC entry 216 (OID 12753245)
-- Name: Genres_pkey; Type: CONSTRAINT; Schema: public; Owner: jbwhite
--

ALTER TABLE ONLY "Genres"
    ADD CONSTRAINT "Genres_pkey" PRIMARY KEY (id);


--
-- TOC entry 217 (OID 12753251)
-- Name: ContentGenre_pkey; Type: CONSTRAINT; Schema: public; Owner: jbwhite
--

ALTER TABLE ONLY "ContentGenre"
    ADD CONSTRAINT "ContentGenre_pkey" PRIMARY KEY (id);


--
-- TOC entry 87 (OID 12738941)
-- Name: CodecCreatorSound_ID_seq; Type: SEQUENCE SET; Schema: public; Owner: jbwhite
--

SELECT pg_catalog.setval('"CodecCreatorSound_ID_seq"', 2000, true);


--
-- TOC entry 89 (OID 12739957)
-- Name: Condition_ID_seq; Type: SEQUENCE SET; Schema: public; Owner: jbwhite
--

SELECT pg_catalog.setval('"Condition_ID_seq"', 2000, true);


--
-- TOC entry 91 (OID 12739983)
-- Name: Content_ID_seq; Type: SEQUENCE SET; Schema: public; Owner: jbwhite
--

SELECT pg_catalog.setval('"Content_ID_seq"', 2124, true);


--
-- TOC entry 93 (OID 12741785)
-- Name: ScannerCamera_ID_seq; Type: SEQUENCE SET; Schema: public; Owner: jbwhite
--

SELECT pg_catalog.setval('"ScannerCamera_ID_seq"', 2000, true);


--
-- TOC entry 95 (OID 12741799)
-- Name: Target_ID_seq; Type: SEQUENCE SET; Schema: public; Owner: jbwhite
--

SELECT pg_catalog.setval('"Target_ID_seq"', 2000, true);


--
-- TOC entry 97 (OID 12741820)
-- Name: TechSound_ID_seq; Type: SEQUENCE SET; Schema: public; Owner: jbwhite
--

SELECT pg_catalog.setval('"TechSound_ID_seq"', 2016, true);


--
-- TOC entry 99 (OID 12742679)
-- Name: Housing_ID_seq; Type: SEQUENCE SET; Schema: public; Owner: jbwhite
--

SELECT pg_catalog.setval('"Housing_ID_seq"', 2000, true);


--
-- TOC entry 101 (OID 12742719)
-- Name: Form_ID_seq; Type: SEQUENCE SET; Schema: public; Owner: jbwhite
--

SELECT pg_catalog.setval('"Form_ID_seq"', 2000, true);


--
-- TOC entry 103 (OID 12742799)
-- Name: Language_ID_seq; Type: SEQUENCE SET; Schema: public; Owner: jbwhite
--

SELECT pg_catalog.setval('"Language_ID_seq"', 2000, true);


--
-- TOC entry 105 (OID 12743212)
-- Name: Location_ID_seq; Type: SEQUENCE SET; Schema: public; Owner: jbwhite
--

SELECT pg_catalog.setval('"Location_ID_seq"', 2000, true);


--
-- TOC entry 107 (OID 12743234)
-- Name: Name_ID_seq; Type: SEQUENCE SET; Schema: public; Owner: jbwhite
--

SELECT pg_catalog.setval('"Name_ID_seq"', 2016, true);


--
-- TOC entry 109 (OID 12743376)
-- Name: Restrictions_ID_seq; Type: SEQUENCE SET; Schema: public; Owner: jbwhite
--

SELECT pg_catalog.setval('"Restrictions_ID_seq"', 2001, true);


--
-- TOC entry 111 (OID 12743401)
-- Name: ResourceType_ID_seq; Type: SEQUENCE SET; Schema: public; Owner: jbwhite
--

SELECT pg_catalog.setval('"ResourceType_ID_seq"', 2000, true);


--
-- TOC entry 113 (OID 12743422)
-- Name: RightsAccess_ID_seq; Type: SEQUENCE SET; Schema: public; Owner: jbwhite
--

SELECT pg_catalog.setval('"RightsAccess_ID_seq"', 2012, true);


--
-- TOC entry 115 (OID 12744359)
-- Name: Role_ID_seq; Type: SEQUENCE SET; Schema: public; Owner: jbwhite
--

SELECT pg_catalog.setval('"Role_ID_seq"', 2000, true);


--
-- TOC entry 117 (OID 12744576)
-- Name: StaffName_ID_seq; Type: SEQUENCE SET; Schema: public; Owner: jbwhite
--

SELECT pg_catalog.setval('"StaffName_ID_seq"', 2001, true);


--
-- TOC entry 119 (OID 12744591)
-- Name: SourceStillImage_ID_seq; Type: SEQUENCE SET; Schema: public; Owner: jbwhite
--

SELECT pg_catalog.setval('"SourceStillImage_ID_seq"', 2023, true);


--
-- TOC entry 121 (OID 12745560)
-- Name: SourceMovingImage_ID_seq; Type: SEQUENCE SET; Schema: public; Owner: jbwhite
--

SELECT pg_catalog.setval('"SourceMovingImage_ID_seq"', 2000, true);


--
-- TOC entry 123 (OID 12745579)
-- Name: Speed_ID_seq; Type: SEQUENCE SET; Schema: public; Owner: jbwhite
--

SELECT pg_catalog.setval('"Speed_ID_seq"', 2000, true);


--
-- TOC entry 125 (OID 12745628)
-- Name: SourceSound_ID_seq; Type: SEQUENCE SET; Schema: public; Owner: jbwhite
--

SELECT pg_catalog.setval('"SourceSound_ID_seq"', 2015, true);


--
-- TOC entry 127 (OID 12746495)
-- Name: ColorSpace_ID_seq; Type: SEQUENCE SET; Schema: public; Owner: jbwhite
--

SELECT pg_catalog.setval('"ColorSpace_ID_seq"', 2000, true);


--
-- TOC entry 129 (OID 12746521)
-- Name: Subjects_ID_seq; Type: SEQUENCE SET; Schema: public; Owner: jbwhite
--

SELECT pg_catalog.setval('"Subjects_ID_seq"', 2003, true);


--
-- TOC entry 131 (OID 12746609)
-- Name: TechImages_ID_seq; Type: SEQUENCE SET; Schema: public; Owner: jbwhite
--

SELECT pg_catalog.setval('"TechImages_ID_seq"', 2022, true);


--
-- TOC entry 133 (OID 12747597)
-- Name: DigitalProvence_ID_seq; Type: SEQUENCE SET; Schema: public; Owner: jbwhite
--

SELECT pg_catalog.setval('"DigitalProvence_ID_seq"', 2000, true);


--
-- TOC entry 135 (OID 12747636)
-- Name: TechMovingImage_ID_seq; Type: SEQUENCE SET; Schema: public; Owner: jbwhite
--

SELECT pg_catalog.setval('"TechMovingImage_ID_seq"', 2000, true);


--
-- TOC entry 137 (OID 12747654)
-- Name: DigitalProvenenceSound_ID_seq; Type: SEQUENCE SET; Schema: public; Owner: jbwhite
--

SELECT pg_catalog.setval('"DigitalProvenenceSound_ID_seq"', 2000, true);


--
-- TOC entry 139 (OID 12750148)
-- Name: Subjects Detail_ID_seq; Type: SEQUENCE SET; Schema: public; Owner: jbwhite
--

SELECT pg_catalog.setval('"Subjects Detail_ID_seq"', 2005, true);


--
-- TOC entry 5 (OID 12753224)
-- Name: Authority_ID_seq; Type: SEQUENCE SET; Schema: public; Owner: jbwhite
--

SELECT pg_catalog.setval('"Authority_ID_seq"', 4, true);


--
-- TOC entry 8 (OID 12753236)
-- Name: Genres_ID_seq; Type: SEQUENCE SET; Schema: public; Owner: jbwhite
--

SELECT pg_catalog.setval('"Genres_ID_seq"', 2, true);


--
-- TOC entry 11 (OID 12753238)
-- Name: ContentGenre_ID_seq; Type: SEQUENCE SET; Schema: public; Owner: jbwhite
--

SELECT pg_catalog.setval('"ContentGenre_ID_seq"', 1, false);


SET SESSION AUTHORIZATION 'pgsql';

--
-- TOC entry 2 (OID 2200)
-- Name: SCHEMA public; Type: COMMENT; Schema: -; Owner: pgsql
--

COMMENT ON SCHEMA public IS 'Standard public schema';


SET SESSION AUTHORIZATION 'jbwhite';

--
-- TOC entry 20 (OID 12739985)
-- Name: COLUMN "Content"."Complete"; Type: COMMENT; Schema: public; Owner: jbwhite
--

COMMENT ON COLUMN "Content"."Complete" IS 'Access set true=-1 false=0';


--
-- TOC entry 37 (OID 12743236)
-- Name: COLUMN "Name"."Authority_id"; Type: COMMENT; Schema: public; Owner: jbwhite
--

COMMENT ON COLUMN "Name"."Authority_id" IS 'Authority Key';


--
-- TOC entry 63 (OID 12746523)
-- Name: COLUMN "Subjects"."Authority_id"; Type: COMMENT; Schema: public; Owner: jbwhite
--

COMMENT ON COLUMN "Subjects"."Authority_id" IS 'Authority Key';


--
-- TOC entry 76 (OID 12753220)
-- Name: TABLE "Authority"; Type: COMMENT; Schema: public; Owner: jbwhite
--

COMMENT ON TABLE "Authority" IS 'Valid Authority values';


--
-- TOC entry 79 (OID 12753242)
-- Name: COLUMN "Genres"."Authority_id"; Type: COMMENT; Schema: public; Owner: jbwhite
--

COMMENT ON COLUMN "Genres"."Authority_id" IS 'Authority Key';


--
-- TOC entry 82 (OID 12753248)
-- Name: COLUMN "ContentGenre"."Content_id"; Type: COMMENT; Schema: public; Owner: jbwhite
--

COMMENT ON COLUMN "ContentGenre"."Content_id" IS 'Content Key';


--
-- TOC entry 83 (OID 12753248)
-- Name: COLUMN "ContentGenre"."Genre_id"; Type: COMMENT; Schema: public; Owner: jbwhite
--

COMMENT ON COLUMN "ContentGenre"."Genre_id" IS 'Genre Key';


