# SPDX-FileCopyrightText: 2024 Dalibo
#
# SPDX-License-Identifier: GPL-3.0-or-later

from __future__ import annotations

from typing import Any

import click

from pglift import hba
from pglift.models import interface, system

from . import model
from .util import (
    Group,
    Obj,
    audit,
    instance_identifier_option,
    pass_postgresql_instance,
)


@click.group(cls=Group)
@instance_identifier_option
def cli(**kwargs: Any) -> None:
    """Manage entries in the pg_hba.conf file of a PostgreSQL instance."""


@cli.command("add")
@model.as_parameters(interface.HbaRecord, "create")
@pass_postgresql_instance
@click.pass_obj
def add(
    obj: Obj, instance: system.PostgreSQLInstance, hbarecord: interface.HbaRecord
) -> None:
    """Add a record in pg_hba.conf.

    If no --connection-* option is specified, a 'local' record is added.
    """
    with obj.lock, audit():
        hba.add(instance, hbarecord)


@cli.command("remove")
@model.as_parameters(interface.HbaRecord, "create")
@pass_postgresql_instance
@click.pass_obj
def remove(
    obj: Obj, instance: system.PostgreSQLInstance, hbarecord: interface.HbaRecord
) -> None:
    """Remove a record from pg_hba.conf.

    If no --connection-* option is specified, a 'local' record is removed.
    """
    with obj.lock, audit():
        hba.remove(instance, hbarecord)
