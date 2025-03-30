import discord as dis
from roles.models import Roles
from user_role.models import UserRole


class RoleMenager:

    PERMISSION_PRESETS = {
        "DEFAULT": dis.Permissions.general(),
        "STAGE_MODERATOR": dis.Permissions.stage_moderator(),
        "MEMBERSHIP": dis.Permissions.membership(),
        "ALL_CHANNELS": dis.Permissions.all_channel(),
        "ALL": dis.Permissions.all(),
        "NONE": dis.Permissions.none(),
    }

    async def initialiaze_db_roles(self, guild: dis.Guild):
        '''Initializes roles from the database'''
        
        for role in Roles.select():
            colour  = int(role.role_colour.lstrip("#"), 16)
            print(f"Role: {role.role_name}, Colour: {colour}, Hoist: {role.hoist}, Mentionable: {role.mentionable}")
            await self.create_role(guild, role.role_name, role.role_permissions, colour, role.hoist, role.mentionable)

    async def role_exists(self, role_name: str, guild: dis.Guild) -> bool:
        """Checks if a role exists in the guild"""
        print(f"Checking if role '{role_name}' exists in the guild.")
        for role in guild.roles:
            if role.name == role_name:
                print(f"Role '{role_name}' already exists.")
                return True
        return False

    async def create_role(self, 
                          guild: dis.Guild,
                          role_name: str,  
                          permissions: str,
                          colour: dis.Colour, 
                          hoist: bool, 
                          mentionable: bool) -> dis.Role:
        """Creates a role in the guild"""
        permissions = self.PERMISSION_PRESETS.get(role_name, dis.Permissions.none())
        if await self.role_exists(role_name, guild) is False:
            new_role = await guild.create_role(    reason = 'Role created by bot.',
                                                        name = role_name,
                                                        permissions = permissions,
                                                        colour = colour,
                                                        hoist = hoist,
                                                        display_icon = None,
                                                        mentionable = mentionable)
            print(f"Role '{role_name}' created successfully.")

            return new_role
        
    async def delete_role(self, guild: dis.Guild, role_name: str):
        """Finds a role by name and deletes it"""
        role_to_delete = dis.utils.get(guild.roles, name=role_name)
        
        if role_to_delete:
            await role_to_delete.delete(reason="Role deleted by bot.")
            print(f"Role '{role_name}' deleted successfully.")
        else:
            print(f"Role '{role_name}' not found in the guild.")

    async def grant_role(self, member: dis.Member, role_name: str):
        """Grants a role to a member"""
        role = dis.utils.get(member.guild.roles, name=role_name)
        if role:
            await member.add_roles(role, reason="Role granted by bot.")
            print(f"Role '{role_name}' granted to {member.display_name}.")
        else:
            print(f"Role '{role_name}' not found in the guild.")
    
    async def revoke_role(self, member: dis.Member, role_name: str):
        """Revokes a role from a member"""
        role = dis.utils.get(member.guild.roles, name=role_name)
        if role:
            await member.remove_roles(role, reason="Role revoked by bot.")
            print(f"Role '{role_name}' revoked from {member.display_name}.")
        else:
            print(f"Role '{role_name}' not found in the guild.")

    
    async def apply_roles_from_user_role_view(self, guild: dis.Guild):
        '''Grants or revokes roles based on the user role view'''
        print("Applying roles from user_role view.")
        user_roles = UserRole.select()
        role_names = [role.role_name for role in Roles.select()]

        print(f"Found {len(user_roles)} user roles.")

        # Iterate through each user role and grant the role to the member
        for user_role in user_roles:
            member = guild.get_member(int(user_role.user_id))
            role = dis.utils.get(guild.roles, name=user_role.role_name)
            # Check if member and role exist
            if member and role:
                memeber_roles = [member_role.name for member_role in member.roles]
                # if member has a role that is not in the user_role table and it is in Roles table, remove it 
                if any(member_role in role_names for member_role in memeber_roles):
                    matching_roles = [member_role for member_role in memeber_roles if member_role in role_names]
                    for matching_role in matching_roles:
                        if matching_role != user_role.role_name:
                            await self.revoke_role(member, matching_role)

                # Check if the member has the role already
                if role.id not in [r.id for r in member.roles]:
                    await self.grant_role(member, user_role.role_name)
            
                    