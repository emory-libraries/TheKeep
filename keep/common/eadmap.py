from eulxml import xmlmap
from eulxml.xmlmap import eadmap

from eulexistdb.models import XmlModel
from eulexistdb.manager import Manager

ID_DELIMITER = '_'

class SubSeries_Base(eadmap.Component):
    """
      Extended for other subseries and the last level of the hierchy (currently, c03).

      Customized version of :class:`eulcore.xmlmap.eadmap.Component`
    """

    _short_id = None
    @property
    def short_id(self):
        "Short-form id (without eadid prefix) for use in external urls."
        #FIXME: Can't get a reference to the eadid at this level? Hack here. . .
        if self._short_id is None:
            self._short_id = self.id
            underscore_pos = self._short_id.find("_subseries")
            if(underscore_pos != -1):
                self._short_id = self._short_id[underscore_pos+1:]
        return self._short_id

    _title = None
    @property
    def title(self):
        "Title of subseries without the date."
        if self._title is None:
            if hasattr(self, 'did') and hasattr(self.did, 'unittitle'):
                self._title = unicode(self.did.unittitle)
                comma_pos = self._title.rfind(", ")
                if(comma_pos != -1):
                    self._title = self._title[:comma_pos]
            else:
                self._title = None
        return self._title

class SubSeries(SubSeries_Base):
    """
      c02 level subseries
    """
    subseries = xmlmap.NodeListField('child::e:c03[@level="subseries"]', SubSeries_Base)
    ":class:`keep.common.eadmap.SubSeries_Base` access to c03 subseries."


class Series(XmlModel, eadmap.Component):
    """
      Top-level (c01) series.

      Customized version of :class:`eulcore.xmlmap.eadmap.Component`
    """

    ROOT_NAMESPACES = {
        'e': eadmap.EAD_NAMESPACE,
        'exist': 'http://exist.sourceforge.net/NS/exist'
    }

    eadid = xmlmap.NodeField('ancestor::e:ead/e:eadheader/e:eadid', eadmap.EadId)

    objects = Manager('//e:c01[@level="series"]')
    """:class:`eulcore.django.existdb.manager.Manager` - similar to an object manager
        for django db objects, used for finding and retrieving series objects
        in eXist.

        Configured to use *//c01[@level='series']* as base search path.
    """

    subseries = xmlmap.NodeListField('child::e:c02[@level="subseries"]', SubSeries)


    _short_id = None
    @property
    def short_id(self):
        "Short-form id (without eadid prefix) for use in external urls."
        if self._short_id is None:
            # get eadid, if available
            if hasattr(self, 'eadid') and self.eadid.value:
                eadid = self.eadid.value
            else:
                eadid = None
            self._short_id = shortform_id(self.id, eadid)
        return self._short_id

    _title = None
    @property
    def title(self):
        "Title of series without the date."
        if self._title is None:
            if hasattr(self, 'did') and hasattr(self.did, 'unittitle'):
                self._title = unicode(self.did.unittitle)
                comma_pos = self._title.rfind(", ")
                if(comma_pos != -1):
                    self._title = self._title[:comma_pos]
            else:
                self._title = None
        return self._title


def shortform_id(id, eadid=None):
    """Calculate a short-form id (without eadid prefix) for use in external urls.
    Uses eadid if available; otherwise, relies on the id delimiter character.
    :param id: id to be shortened
    :param eadid: eadid prefix, if available
    :returns: short-form id
    """
    # if eadid is available, use that (should be the most reliable way to shorten id)
    if eadid:
        id = id.replace('%s_' % eadid, '')
        
    # if eadid is not available, split on _ and return latter portion
    elif ID_DELIMITER in id:
        eadid, id = id.split(ID_DELIMITER)

    # this shouldn't happen -  one of the above two options should work
    else:
        raise Exception("Cannot calculate short id for %s" % id)
    return id



