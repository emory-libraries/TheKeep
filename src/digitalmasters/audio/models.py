from eulcore.fedora.models import DigitalObject, FileDatastream, RdfDatastream, XmlDatastream
from eulcore.xmlmap.dc import DublinCore

class AudioObject(DigitalObject):
    dc = XmlDatastream("DC", "Dublin Core", DublinCore, defaults={
            'control_group': 'X',
            'format': 'http://www.openarchives.org/OAI/2.0/oai_dc/',
        })
    rels_ext = RdfDatastream("RELS-EXT", "External Relations", defaults={
            'control_group': 'X',
            'format': 'info:fedora/fedora-system:FedoraRELSExt-1.0',
        })
    audio = FileDatastream("AUDIO", "Audio datastream", defaults={
            'mimetype': 'audio/x-wav',
        })
