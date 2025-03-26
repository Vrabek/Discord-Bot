import discord as dis
from roles.models import Roles
from user_role.models import UserRole


class RoleMenager:

    async def initialiaze_db_roles(self, guild: dis.Guild):
        '''Initializes roles from the database'''
        
        for role in Roles.select():
            colour  = int(role.role_colour.lstrip("#"), 16)
            print(f"Role: {role.role_name}, Colour: {colour}, Hoist: {role.hoist}, Mentionable: {role.mentionable}")
            await self.create_role(guild, role.role_name, colour, role.hoist, role.mentionable)

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
                          colour: dis.Colour, 
                          hoist: bool, 
                          mentionable: bool) -> dis.Role:
        """Creates a role in the guild"""
        if await self.role_exists(role_name, guild) is False:
            new_role = await guild.create_role(    reason = 'Role created by bot.',
                                                        name = role_name,
                                                        permissions = dis.Permissions.membership(),
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
        print(f"Found {len(user_roles)} user roles.")

        for user_role in user_roles:
            member = guild.get_member(int(user_role.user_id))
            print(f'{user_role.user_id}, {type(member)}')
            role = dis.utils.get(guild.roles, name=user_role.role_name)
            # Check if member and role exist
            if member and role:
                if not role in member.roles:
                    await self.grant_role(member, user_role.role_name)
