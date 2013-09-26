# vim: tabstop=4 shiftwidth=4 softtabstop=4

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

import sqlalchemy


def upgrade(migrate_engine):
    meta = sqlalchemy.MetaData()
    meta.bind = migrate_engine

    service_type = sqlalchemy.Table(
        'service_type', meta,
        sqlalchemy.Column('id', sqlalchemy.Integer,
                          primary_key=True, nullable=False),
        sqlalchemy.Column('name', sqlalchemy.String(126)),
        sqlalchemy.Column('template', sqlalchemy.Text),
        sqlalchemy.Column('created_at', sqlalchemy.DateTime),
        sqlalchemy.Column('updated_at', sqlalchemy.DateTime),
    )

    service = sqlalchemy.Table(
        'service', meta,
        sqlalchemy.Column('id', sqlalchemy.String(36),
                          primary_key=True, nullable=False),
        sqlalchemy.Column('name', sqlalchemy.String(126)),
        sqlalchemy.Column('stack_id', sqlalchemy.String(36), nullable=False),
        sqlalchemy.Column('service_type_id', sqlalchemy.Integer, sqlalchemy.ForeignKey('service_type.id'), nullable=False),
        sqlalchemy.Column('status', sqlalchemy.String(36), nullable=False),
        sqlalchemy.Column('extdata', sqlalchemy.Text),
        sqlalchemy.Column('url', sqlalchemy.Text),
        sqlalchemy.Column('created_at', sqlalchemy.DateTime),
        sqlalchemy.Column('updated_at', sqlalchemy.DateTime),
    )

    service_tenant = sqlalchemy.Table(
        'service_tenant', meta,
        sqlalchemy.Column('service_id', sqlalchemy.String(36), sqlalchemy.ForeignKey('service.id'),
                          primary_key=True, nullable=False),
        sqlalchemy.Column('tenant_id', sqlalchemy.String(64),
                          primary_key=True, nullable=False),
        sqlalchemy.Column('created_at', sqlalchemy.DateTime),
        sqlalchemy.Column('updated_at', sqlalchemy.DateTime),
    )

    service_instance = sqlalchemy.Table(
        'service_instance', meta,
        sqlalchemy.Column('instance_id', sqlalchemy.String(255),
                          primary_key=True, nullable=False),
        sqlalchemy.Column('service_id', sqlalchemy.String(36),
                          primary_key=True, nullable=False),
        sqlalchemy.Column('created_at', sqlalchemy.DateTime),
        sqlalchemy.Column('updated_at', sqlalchemy.DateTime),
    )

    tables = (
        service_type,
        service,
        service_tenant,
        service_instance,
    )

    for index, table in enumerate(tables):
        try:
            table.create()
        except:
            # If an error occurs, drop all tables created so far to return
            # to the previously existing state.
            meta.drop_all(tables=tables[:index])
            raise


def downgrade(migrate_engine):
    raise Exception('Database downgrade not supported - would drop all tables')
