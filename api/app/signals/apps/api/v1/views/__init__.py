"""
V1 API ViewSet.
"""
from signals.apps.api.v1.views.area import PrivateAreasViewSet, PublicAreasViewSet
from signals.apps.api.v1.views.attachment import (
    PrivateSignalAttachmentsViewSet,
    PublicSignalAttachmentsViewSet
)
from signals.apps.api.v1.views.category import (
    ChildCategoryViewSet,
    ParentCategoryViewSet,
    PrivateCategoryViewSet,
    CategoryNameViewSet
)
from signals.apps.api.v1.views.category_removed import SignalCategoryRemovedAfterViewSet
from signals.apps.api.v1.views.departments import PrivateDepartmentViewSet
# from signals.apps.api.v1.views.ml_tool_proxy import MlPredictCategoryView  # V1 disabled for now
from signals.apps.api.v1.views.namespace import NamespaceView
from signals.apps.api.v1.views.pdf import GeneratePdfView
from signals.apps.api.v1.views.questions import PublicQuestionViewSet
from signals.apps.api.v1.views.signal import PrivateSignalViewSet, PublicSignalViewSet
from signals.apps.api.v1.views.signal_split import PrivateSignalSplitViewSet
from signals.apps.api.v1.views.status_message_template import StatusMessageTemplatesViewSet
from signals.apps.api.v1.views.stored_signal_filter import StoredSignalFilterViewSet

from signals.apps.api.v1.views.city_object import CityObjectViewSet
from signals.apps.api.v1.views.signal_city_object import SignalCityObjectViewSet
from signals.apps.api.v1.views.id_mapping import IDMappingViewset

__all__ = (
    'PublicSignalAttachmentsViewSet',
    'PrivateSignalAttachmentsViewSet',
    'PublicSignalViewSet',
    'PrivateSignalViewSet',
    'SignalCategoryRemovedAfterViewSet',
    'ChildCategoryViewSet',
    'ParentCategoryViewSet',
    'PrivateCategoryViewSet',
    'PublicQuestionViewSet',
    # 'MlPredictCategoryView',  # V1 disabled for now
    'NamespaceView',
    'GeneratePdfView',
    'PrivateDepartmentViewSet',
    'PrivateSignalSplitViewSet',
    'StatusMessageTemplatesViewSet',
    'StoredSignalFilterViewSet',
    'PublicAreasViewSet',
    'PrivateAreasViewSet',
    'CityObjectViewSet',
    'SignalCityObjectViewSet',
    'CategoryNameViewSet',
    'IDMappingViewset',
)
