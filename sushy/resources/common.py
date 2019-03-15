# Licensed under the Apache License, Version 2.0 (the "License"); you may
# not use this file except in compliance with the License. You may obtain
# a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS, WITHOUT
# WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the
# License for the specific language governing permissions and limitations
# under the License.

from dateutil import parser

from sushy.resources import base
from sushy.resources import mappings as res_maps


class IdRefField(base.CompositeField):
    """Reference to the resource odata identity field."""

    resource_uri = base.Field('@odata.id')
    """The unique identifier for a resource"""


class OperationApplyTimeSupportField(base.CompositeField):
    def __init__(self):
        super(OperationApplyTimeSupportField, self).__init__(
            path="@Redfish.OperationApplyTimeSupport")

    maintenance_window_duration_in_seconds = base.Field(
        'MaintenanceWindowDurationInSeconds', adapter=int)
    """The expiry time of maintenance window in seconds"""

    _maintenance_window_resource = IdRefField('MaintenanceWindowResource')
    """The location of the maintenance window settings"""

    maintenance_window_start_time = base.Field(
        'MaintenanceWindowStartTime',
        adapter=parser.parse)
    """The start time of a maintenance window"""

    supported_values = base.Field('SupportedValues', required=True,
                                  adapter=list)
    """The client is allowed request when performing a create, delete, or
    action operation"""


class ActionField(base.CompositeField):
    target_uri = base.Field('target', required=True)
    operation_apply_time_support = OperationApplyTimeSupportField()


class ResetActionField(ActionField):
    allowed_values = base.Field('ResetType@Redfish.AllowableValues',
                                adapter=list)


class StatusField(base.CompositeField):
    """This Field describes the status of a resource and its children.

    This field shall contain any state or health properties of a resource.
    """
    health = base.MappedField('Health', res_maps.HEALTH_VALUE_MAP)
    """Represents health of resource w/o considering its dependent resources"""

    health_rollup = base.MappedField('HealthRollup', res_maps.HEALTH_VALUE_MAP)
    """Represents health state of resource and its dependent resources"""

    state = base.MappedField('State', res_maps.STATE_VALUE_MAP)
    """Indicates the known state of the resource, such as if it is enabled."""
