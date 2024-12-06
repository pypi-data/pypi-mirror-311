
# flake8: noqa

# Import all APIs into this package.
# If you have many APIs here with many many models used in each API this may
# raise a `RecursionError`.
# In order to avoid this, import only the API that you directly need like:
#
#   from eis.partner.api.partner_api import PartnerApi
#
# or import this package, but before doing it, use:
#
#   import sys
#   sys.setrecursionlimit(n)

# Import APIs into API package:
from eis.partner.api.partner_api import PartnerApi
from eis.partner.api.partner_type_api import PartnerTypeApi
from eis.partner.api.partner_invitation_api import PartnerInvitationApi
from eis.partner.api.partner_relation_api import PartnerRelationApi
from eis.partner.api.partner_tag_api import PartnerTagApi
from eis.partner.api.partner_version_api import PartnerVersionApi
from eis.partner.api.default_api import DefaultApi
