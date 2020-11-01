import copy

from django.contrib.gis.db import models
from django.contrib.gis.gdal import CoordTransform, SpatialReference
from django.contrib.postgres.fields import JSONField

from signals.apps.signals.models.mixins import CreatedUpdatedModel

STADSDEEL_CENTRUM = 'A'
STADSDEEL_WESTPOORT = 'B'
STADSDEEL_WEST = 'E'
STADSDEEL_OOST = 'M'
STADSDEEL_NOORD = 'N'
STADSDEEL_ZUIDOOST = 'T'
STADSDEEL_ZUID = 'K'
STADSDEEL_NIEUWWEST = 'F'
STADSDEEL_AMSTERDAMSE_BOS = 'H'
STADSDEEL_WEESP = 'W'
STADSDEEL_LOOSDUINEN = 'Loosduinen'
STADSDEEL_ESCAMP = 'Escamp'
STADSDEEL_SEGBROEK = 'Segbroek'
STADSDEEL_SCHEVENINGEN = 'Scheveningen'
STADSDEEL_CENTRUM = 'Centrum'
STADSDEEL_LAAK = 'Laak'
STADSDEEL_HAAGSE_HOUT = 'Haagse hout'
STADSDEEL_LEIDSCHENVEEN_YPENBURG = 'Leidschenveen-Ypenburg'


STADSDELEN = (
    (STADSDEEL_CENTRUM, 'Centrum'),
    (STADSDEEL_WESTPOORT, 'Westpoort'),
    (STADSDEEL_WEST, 'West'),
    (STADSDEEL_OOST, 'Oost'),
    (STADSDEEL_NOORD, 'Noord'),
    (STADSDEEL_ZUIDOOST, 'Zuidoost'),
    (STADSDEEL_ZUID, 'Zuid'),
    (STADSDEEL_NIEUWWEST, 'Nieuw-West'),
    (STADSDEEL_AMSTERDAMSE_BOS, 'Het Amsterdamse Bos'),
    (STADSDEEL_WEESP, 'Weesp'),
    (STADSDEEL_LOOSDUINEN, 'Loosduinen'),
    (STADSDEEL_ESCAMP, 'Escamp'),
    (STADSDEEL_SEGBROEK, 'Segbroek'),
    (STADSDEEL_SCHEVENINGEN, 'Scheveningen'),
    (STADSDEEL_CENTRUM, 'Centrum'),
    (STADSDEEL_LAAK, 'Laak'),
    (STADSDEEL_HAAGSE_HOUT, 'Haagse hout'),
    (STADSDEEL_LEIDSCHENVEEN_YPENBURG, 'Leidschenveen-Ypenburg'),
)

AREA_STADSDEEL_TRANSLATION = {
    'het-amsterdamse-bos': STADSDEEL_AMSTERDAMSE_BOS,
    'zuidoost': STADSDEEL_ZUIDOOST,
    'centrum': STADSDEEL_CENTRUM,
    'noord': STADSDEEL_NOORD,
    'westpoort': STADSDEEL_WESTPOORT,
    'west': STADSDEEL_WEST,
    'nieuw-west': STADSDEEL_NIEUWWEST,
    'oost': STADSDEEL_OOST,
    'zuid': STADSDEEL_ZUID,
    'stadsdeel-zuid': STADSDEEL_ZUID,
    'weesp': STADSDEEL_WEESP,
    'Loosduinen': STADSDEEL_LOOSDUINEN,
    'Escamp': STADSDEEL_ESCAMP,
    'Segbroek': STADSDEEL_SEGBROEK, 
    'Scheveningen': STADSDEEL_SCHEVENINGEN,
    'Centrum': STADSDEEL_CENTRUM, 
    'Laak': STADSDEEL_LAAK, 
    'Haagse hout': STADSDEEL_HAAGSE_HOUT, 
    'Leidschenveen-Ypenburg': STADSDEEL_LEIDSCHENVEEN_YPENBURG,
}

_ADDRESS_FIELD_PREFIXES = (
    ('openbare_ruimte', ''),
    ('huisnummer', ' '),
    ('huisletter', ''),
    ('huisnummer_toevoeging', '-'),
    ('postcode', ' '),
    ('woonplaats', ' ')
)

_NEW_ADDRESS_FIELD_PREFIXES = (                           # added new address field prefixes SHO:200
    ('openbare_ruimte', ''),
)


def get_address_text(location, field_prefixes=_NEW_ADDRESS_FIELD_PREFIXES):           # changes SHO:200
    """Generate address text, shortened if needed."""

    address_text = ''
    if location.address and isinstance(location.address, dict):
        for field, prefix in field_prefixes:
            if field in location.address and location.address[field]:
                address_text += prefix + str(location.address[field])

    return address_text


class Location(CreatedUpdatedModel):
    """All location related information."""

    _signal = models.ForeignKey(
        'signals.Signal', related_name='locations',
        null=False, on_delete=models.CASCADE
    )

    geometrie = models.PointField(name='geometrie')
    stadsdeel = models.CharField(null=True, max_length=30, choices=STADSDELEN)

    # we do NOT use foreign key, since we update
    # buurten as external data in a seperate process
    buurt_code = models.CharField(null=True, max_length=4)
    address = JSONField(null=True)
    address_text = models.CharField(null=True, max_length=256, editable=False)
    created_by = models.EmailField(null=True, blank=True)

    extra_properties = JSONField(null=True)
    bag_validated = models.BooleanField(default=False)

    @property
    def short_address_text(self):
        # no postal code, no municipality
        field_prefixes = copy.deepcopy(_NEW_ADDRESS_FIELD_PREFIXES)             # changed SHO:200
        #field_prefixes = field_prefixes[:-2]                                   # removed SHO:200

        return get_address_text(self, field_prefixes)

    def set_address_text(self):
        self.address_text = get_address_text(self)

    def save(self, *args, **kwargs):
        # Set address_text
        self.set_address_text()
        super().save(*args, **kwargs)

    def get_rd_coordinates(self):
        to_transform = copy.deepcopy(self.geometrie)
        to_transform.transform(
            CoordTransform(
                SpatialReference(4326),  # WGS84
                SpatialReference(28992)  # RD
            )
        )
        return to_transform


def _get_description_of_update_location(location_id):
    """Get descriptive text for location update history entries."""
    location = Location.objects.get(id=location_id)

    # Craft a message for UI
    desc = 'Stadsdeel: {}\n'.format(
        location.get_stadsdeel_display()) if location.stadsdeel else ''

    # Deal with address text or coordinates
    if location.address and isinstance(location.address, dict):
        '''field_prefixes = (
            ('openbare_ruimte', ''),
            ('huisnummer', ' '),
            ('huisletter', ''),
            ('huisnummer_toevoeging', '-'),
            ('woonplaats', '\n')
        )'''
        field_prefixes = (                                                              # changed SHO:200
            ('openbare_ruimte', ''), 
        )

        desc += get_address_text(location, field_prefixes)
    else:
        desc += 'Locatie is gepind op de kaart\n{}, {}'.format(
            location.geometrie[0],
            location.geometrie[1],
        )

    return desc
