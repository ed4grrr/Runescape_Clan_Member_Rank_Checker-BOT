import datetime

import UsefulLists

class clan_Requirement_Checker:



    def __init__(self):
        self.experience_needed_for_Rank = UsefulLists.TCK_Default_Experience
        self.skip_list = UsefulLists.TCK_Default_Skip_List


    def change_experience_for_rank(self,rank,xp):
        """
        This will allow for the default minimum rank experience values to be changed.

        :param rank: The name of the rank in a string
        :param xp: The experienc required in an int
        :return: None/updates rank dict for new values.
        """
        self.experience_needed_for_Rank.update(rank,xp)


    def check_for_rank_up(self,clan_list):
        today=datetime.date.today()
        clanmates_requiring_promotions = f"**********Clan Promotions {today}**********\n"

        for clanmate in clan_list.items():
            if clanmate[1][0] not in self.skip_list:
                if int(clanmate[1][1]) >= self.experience_needed_for_Rank[clanmate[1][0]]:
                    clanmates_requiring_promotions += f"{clanmate[0]} has {clanmate[1][1]} clan XP and should be a {UsefulLists.Promotion_Dict[clanmate[1][0]]}\n"

        return clanmates_requiring_promotions


