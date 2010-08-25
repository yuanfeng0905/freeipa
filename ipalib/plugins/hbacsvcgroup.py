# Authors:
#   Rob Crittenden <rcritten@redhat.com>
#
# Copyright (C) 2010  Red Hat
# see file 'COPYING' for use and warranty information
#
# This program is free software; you can redistribute it and/or
# modify it under the terms of the GNU General Public License as
# published by the Free Software Foundation; version 2 only
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program; if not, write to the Free Software
# Foundation, Inc., 59 Temple Place, Suite 330, Boston, MA 02111-1307 USA
"""
HBAC Service Groups

HBAC service groups can contain any number of individual services,
or "members", and can also contain other service groups. Every group must
have a description.

EXAMPLES:

 Add a new HBAC services group:
   ipa hbacsvcgroup-add --desc="login services" login

 Add members to an HBAC services group:
   ipa hbacsvcgroup-add-member --hbacsvcs=sshd,login login

 Display information about a named group:
   ipa hbacsvcgroup-show login

 Add a new group to the "login" group:
   ipa hbacsvcgroup-add --desc="switch users" suers
   ipa hbacsvcgroup-add-member --hbacsvcs=su,su-l suers
   ipa hbacsvsgroup-add-member --hbacsvsgroups=suers login

 Delete an HBAC services group:
   ipa hbacsvcgroup-del login
"""

from ipalib import api, errors
from ipalib.plugins.baseldap import *
from ipalib import _, ngettext


class hbacsvcgroup(LDAPObject):
    """
    HBAC service group object.
    """
    container_dn = api.env.container_hbacservicegroup
    object_name = 'servicegroup'
    object_name_plural = 'servicegroups'
    object_class = ['ipaobject', 'ipahbacservicegroup']
    default_attributes = [ 'cn', 'description', 'member', 'memberof', ]
    uuid_attribute = 'ipauniqueid'
    attribute_members = {
        'member': ['hbacsvc', 'hbacsvcgroup'],
        'memberof': ['hbacsvcgroup'],
    }

    label = _('HBAC Service Groups')

    takes_params = (
        Str('cn',
            cli_name='name',
            label=_('Service group name'),
            primary_key=True,
            normalizer=lambda value: value.lower(),
        ),
        Str('description',
            cli_name='desc',
            label=_('Description'),
            doc=_('HBAC service group description'),
        ),
        Str('member_service?',
            label=_('Member services'),
            flags=['no_create', 'no_update', 'no_search'],
        ),
        Str('member_servicegroup?',
            label=_('Member service groups'),
            flags=['no_create', 'no_update', 'no_search'],
        ),
        Str('memberof_servicegroup?',
            label='Member of service groups',
            flags=['no_create', 'no_update', 'no_search'],
        ),
    )

api.register(hbacsvcgroup)


class hbacsvcgroup_add(LDAPCreate):
    """
    Add a new HBAC services group.
    """
    msg_summary = _('Added HBAC Service group "%(value)s"')

api.register(hbacsvcgroup_add)


class hbacsvcgroup_del(LDAPDelete):
    """
    Delete an HBAC services group.
    """
    msg_summary = _('Deleted HBAC Service group "%(value)s"')

api.register(hbacsvcgroup_del)


class hbacsvcgroup_mod(LDAPUpdate):
    """
    Modify an HBAC services group.
    """
    msg_summary = _('Modified HBAC Service group "%(value)s"')

api.register(hbacsvcgroup_mod)


class hbacsvcgroup_find(LDAPSearch):
    """
    Search for an HBAC services group.
    """
    msg_summary = ngettext(
        '%(count)d group matched', '%(count)d groups matched', 0
    )

api.register(hbacsvcgroup_find)


class hbacsvcgroup_show(LDAPRetrieve):
    """
    Display information about an HBAC services group.
    """

api.register(hbacsvcgroup_show)


class hbacsvcgroup_add_member(LDAPAddMember):
    """
    Add members to an HBAC services group.
    """

api.register(hbacsvcgroup_add_member)


class hbacsvcgroup_remove_member(LDAPRemoveMember):
    """
    Remove members from an HBAC services group.
    """

api.register(hbacsvcgroup_remove_member)
