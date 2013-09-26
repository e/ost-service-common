# vim: tabstop=4 shiftwidth=4 softtabstop=4

#
#    Licensed under the Apache License, Version 2.0 (the "License"); you may
#    not use this file except in compliance with the License. You may obtain
#    a copy of the License at
#
#         http://www.apache.org/licenses/LICENSE-2.0
#
#    Unless required by applicable law or agreed to in writing, software
#    distributed under the License is distributed on an "AS IS" BASIS, WITHOUT
#    WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the
#    License for the specific language governing permissions and limitations
#    under the License.

'''Implementation of SQLAlchemy backend.'''
from sqlalchemy.orm.session import Session

from tdafcommon.common import crypt
from tdafcommon.openstack.common import exception
from tdafcommon.db.sqlalchemy import models
from tdafcommon.db.sqlalchemy.session import get_session


def model_query(context, *args):
    session = _session(context)
    query = session.query(*args)

    return query


def _session(context):
    return (context and context.session) or get_session()

def service_get_all(context):
    result = model_query(context, models.Service).all()

    return result

def service_tenant_get_all_by_tenant(context, tenant_id):
    result = model_query(context, models.ServiceTenant).\
        filter_by(tenant_id=tenant_id)

    return result

def service_tenant_get_by_service_and_tenant(context, service_id, tenant_id):
    result = model_query(context, models.ServiceTenant).\
        filter_by(tenant_id=tenant_id,service_id=service_id)

    return result

def service_create(context, values):
    service_ref = models.Service()
    service_ref.update(values)
    service_ref.save(_session(context))
    return service_ref

def service_tenant_create(context, values):
    service_tenant_ref = models.ServiceTenant()
    service_tenant_ref.update(values)
    service_tenant_ref.save(_session(context))
    return service_tenant_ref

def service_type_get(context, type_id):
    return model_query(context, models.ServiceType).get(type_id)

def service_stack_get(context, service_id):
    return model_query(context, models.Service).get(service_id)

def service_stack_update(context, service_id, values):
    tdafcommon = service_stack_get(context, service_id)

    if not tdafcommon:
        raise exception.NotFound('Attempt to update a tdafcommon with id: %s %s' %
                                 (service_id, 'that does not exist'))

    tdafcommon.update(values)
    tdafcommon.save(_session(context))
