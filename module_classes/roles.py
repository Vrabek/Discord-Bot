import discord as dis
from my_database.models import Roles


class RoleMenager:

    db_roles = {}

    def __init__(self):
        self.initialiaze_db_roles()
    
    async def initalize_roles(self):
        await self.create_role('Pobratanek')

    def initialiaze_json_roles(self):
        pass


    async def role_exists(self, guild: dis.Guild, role_name: str) -> bool:
        if role_name in guild.roles:
            print(f"Role '{role_name}' already exists.")
            return True


    async def create_role(self, role_name: str):
        
        if await self.role_exists(role_name) is False:
            new_role = await dis.Guild.create_role(    reason = 'Zaslugujesz na to!',
                                                        name = role_name,
                                                        permissions = dis.Permissions.all(),
                                                        colour = dis.Colour.blue(),
                                                        hoist = True,
                                                        display_icon = None,
                                                        mentionable = True)
            print(f"Role '{role_name}' created successfully.")

            return new_role