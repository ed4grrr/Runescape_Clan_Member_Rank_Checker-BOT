import urllib.error
import urllib.request
import requests
import Clan_Requirement_Checker
import UsefulLists
import discord
from discord.ext import commands

from dotenv import load_dotenv
import os


class runescape_API_Access():

    def __init__(self):
        super()
        self.clan_data_dict = {}
        self.clan_data_list = []

    def get_player(self, username):
        clean_username = username.replace(" ", "_")


        api_request = urllib.request.Request(
            'https://secure.runescape.com/m=hiscore/index_lite.ws?player=' + clean_username)

        try:
            response = urllib.request.urlopen(api_request)
        except urllib.error.HTTPError as e:
            return f"Unfulfilled Request,\nCode: {e.code}\nReason: {e.reason}"

        except urllib.error.URLError as e:
            return f"Failed to reach Server, \nReason: {e.reason} "

        data = [[int(number) if number != '' else 0 for number in entry.split(",")] for entry in
                response.read().decode().split("\n")]

        if len(data) == 0:
            return ("Invalid Player Name")

        return dict(zip(UsefulLists.USER_LITE_SCORE_API_RESPONSE_ORDER, data))

    def get_clan_information(self,clan_name):
        encoded_name = requests.utils.quote(clan_name)
        url =f"https://secure.runescape.com/m=clan-hiscores/members_lite.ws?clanName={encoded_name}"

        response = requests.get(url)

        if response.status_code == 200:
            return response.text
        else:
            return f"Error: Unable to fetch data for clan '{clan_name}'. Status Code: {response.status_code}"


    def parse_clan_data(self,clan_data):
        self.clan_data_dict.clear()
        self.clan_data_list.clear()
        clan_data_split = clan_data.split("\n")
        self.clan_data_list=clan_data_split
        for clanmate in clan_data_split:
            clanmate_details = clanmate.split(",")
            if clanmate_details == ['']:
                continue
            self.clan_data_dict[clanmate_details[0]] = [clanmate_details[1],clanmate_details[2],clanmate_details[3]]
        del self.clan_data_dict["Clanmate"]

        #print(self.clan_data_list)
        #print(self.clan_data_dict)
if __name__ == "__main__":

    load_dotenv()
    API_KEY = os.getenv('DISCORD_TOKEN')



    intents=discord.Intents.default()
    intents.message_content = True

    bot = commands.Bot(intents=intents,command_prefix="!" )

    def get_promotions():
        api_test = runescape_API_Access()

        response = api_test.get_clan_information("The Citadel Kingdom").replace(u'\xa0', u' ')

        api_test.parse_clan_data(response)

        Clan_Req_check = Clan_Requirement_Checker.clan_Requirement_Checker()

        output = Clan_Req_check.check_for_rank_up(api_test.clan_data_dict)
        return output



    @bot.command()
    async def promos(ctx):

        await ctx.send(f"{get_promotions()}")


    bot.run(API_KEY)
