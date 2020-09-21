"""
Model the workflow of responding to a Signal (melding) as state machine.
"""
# ! Made sure that the status that is created also exists in the ZTC on staging. Otherwise it will
# ! fail with setting the status.

# Internal statusses
LEEG = ''
GEMELD = 'm'
AFWACHTING = 'i'
BEHANDELING = 'b'
ON_HOLD = 'h'
AFGEHANDELD = 'o'
GEANNULEERD = 'a'
GESPLITST = 's'
HEROPEND = 'reopened'
VERZOEK_TOT_AFHANDELING = 'closure requested'
INGEPLAND = 'ingepland'
VERZOEK_TOT_HEROPENEN = 'reopen requested'
SPLITSEN = 'split'
MEER_INFORMATIE_GEWENST = 'mig'

# Statusses to track progress in external systems
TE_VERZENDEN = 'ready to send'
VERZONDEN = 'sent'
VERZENDEN_MISLUKT = 'send failed'
AFGEHANDELD_EXTERN = 'done external'

# Choices for the API/Serializer layer. Users that can change the state via the API are only allowed
# to use one of the following choices.
STATUS_CHOICES_API = (
    (GEMELD, 'Gemeld'),
    (AFWACHTING, 'In afwachting van behandeling'),
    (BEHANDELING, 'In behandeling'),
    (ON_HOLD, 'On hold'),
    (INGEPLAND, 'Ingepland'),
    (TE_VERZENDEN, 'Te verzenden naar extern systeem'),
    (AFGEHANDELD, 'Afgehandeld'),
    (GEANNULEERD, 'Geannuleerd'),
    (HEROPEND, 'Heropend'),
    (GESPLITST, 'Gesplitst'),
    (VERZOEK_TOT_AFHANDELING, 'Verzoek tot afhandeling'),
    (SPLITSEN, 'split'),
    (MEER_INFORMATIE_GEWENST, 'mig'),
)

# Choices used by the application. These choices can be set from within the application, not via the
# API/Serializer layer.
STATUS_CHOICES_APP = (
    (VERZONDEN, 'Verzonden naar extern systeem'),
    (VERZENDEN_MISLUKT, 'Verzending naar extern systeem mislukt'),
    (AFGEHANDELD_EXTERN, 'Melding is afgehandeld in extern systeem'),
    (VERZOEK_TOT_HEROPENEN, 'Verzoek tot heropenen'),
)

# All allowed choices, used for the model `Status`.
STATUS_CHOICES = STATUS_CHOICES_API + STATUS_CHOICES_APP

ALLOWED_STATUS_CHANGES = {
    MEER_INFORMATIE_GEWENST: [
        GEMELD,
        GESPLITST,
        AFWACHTING,
        BEHANDELING,
        TE_VERZENDEN,
        AFGEHANDELD,  # SIG-1294
        GEANNULEERD,  # Op verzoek via mail van Arvid Smits
        INGEPLAND,  # SIG-1327
        SPLITSEN,
        MEER_INFORMATIE_GEWENST,
    ],
    SPLITSEN: [
        GEMELD,
        GESPLITST,
        AFWACHTING,
        BEHANDELING,
        TE_VERZENDEN,
        AFGEHANDELD,  # SIG-1294
        GEANNULEERD,  # Op verzoek via mail van Arvid Smits
        INGEPLAND,  # SIG-1327
        SPLITSEN,
        MEER_INFORMATIE_GEWENST,
    ],
    LEEG: [
        GEMELD
    ],
    GEMELD: [
        GEMELD,  # SIG-1264
        GESPLITST,
        AFWACHTING,
        BEHANDELING,
        TE_VERZENDEN,
        AFGEHANDELD,  # SIG-1294
        GEANNULEERD,  # Op verzoek via mail van Arvid Smits
        INGEPLAND,  # SIG-1327
	SPLITSEN,
        MEER_INFORMATIE_GEWENST,
    ],
    AFWACHTING: [
        GEMELD,  # SIG-1264
        AFWACHTING,
        INGEPLAND,
        VERZOEK_TOT_AFHANDELING,
        AFGEHANDELD,
        TE_VERZENDEN,  # SIG-1293
        BEHANDELING,  # SIG-1295
	SPLITSEN,
        MEER_INFORMATIE_GEWENST,
    ],
    BEHANDELING: [
        GEMELD,  # SIG-1264
        INGEPLAND,
        BEHANDELING,
        AFGEHANDELD,
        GEANNULEERD,
        TE_VERZENDEN,
        VERZOEK_TOT_AFHANDELING,  # SIG-1374
	SPLITSEN,
        MEER_INFORMATIE_GEWENST,
    ],
    INGEPLAND: [
        GEMELD,  # SIG-1264
        INGEPLAND,
        BEHANDELING,
        AFGEHANDELD,
        GEANNULEERD,
        VERZOEK_TOT_AFHANDELING,  # SIG-1293
        SPLITSEN,
        MEER_INFORMATIE_GEWENST,
    ],
    ON_HOLD: [
        INGEPLAND,
	SPLITSEN,
        MEER_INFORMATIE_GEWENST,
    ],
    TE_VERZENDEN: [
        VERZONDEN,
        VERZENDEN_MISLUKT,
	SPLITSEN,
        MEER_INFORMATIE_GEWENST,
    ],
    VERZONDEN: [
        AFGEHANDELD_EXTERN,
	SPLITSEN,
        MEER_INFORMATIE_GEWENST,
    ],
    VERZENDEN_MISLUKT: [
        GEMELD,
        TE_VERZENDEN,
	SPLITSEN,
        MEER_INFORMATIE_GEWENST,
    ],
    AFGEHANDELD_EXTERN: [
        AFGEHANDELD,
        GEANNULEERD,
        BEHANDELING,  # SIG-1293
	SPLITSEN,
        MEER_INFORMATIE_GEWENST,
    ],
    AFGEHANDELD: [
        HEROPEND,
        VERZOEK_TOT_HEROPENEN,
	SPLITSEN,
        MEER_INFORMATIE_GEWENST,
    ],
    GEANNULEERD: [
        GEANNULEERD,
        HEROPEND,
        BEHANDELING,  # SIG-2109
	SPLITSEN,
        MEER_INFORMATIE_GEWENST,
    ],
    HEROPEND: [
        HEROPEND,
        BEHANDELING,
        AFGEHANDELD,
        GEANNULEERD,
        TE_VERZENDEN,
        GEMELD,  # SIG-1374
	SPLITSEN,
        MEER_INFORMATIE_GEWENST,
    ],
    GESPLITST: [],
    VERZOEK_TOT_AFHANDELING: [
        GEMELD,  # SIG-1264
        VERZOEK_TOT_AFHANDELING,
        AFWACHTING,
        AFGEHANDELD,
        GEANNULEERD,
        BEHANDELING,  # SIG-1374
	SPLITSEN,
        MEER_INFORMATIE_GEWENST,
    ],
    VERZOEK_TOT_HEROPENEN: [
        AFGEHANDELD,
        HEROPEND,
        GEANNULEERD,
	SPLITSEN,
        MEER_INFORMATIE_GEWENST,
    ]
}
