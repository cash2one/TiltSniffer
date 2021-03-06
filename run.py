from multiprocessing import Process

from opgg import Opgg
from riotapi import RiotApi


def main():
    riot = RiotApi()
    name = input("enter summoner name:")
    active_match = riot.get_summoner_active_match(name)

    for participant in active_match.participants:
        p = Process(target=get_participant_info, args=(participant,))
        p.start()
    p.join()


def get_participant_info(participant):
    opgg = Opgg()
    champion = participant.champion
    summoner_name = participant.summoner_name
    summoner_id = participant.summoner.id
    team = participant.side.name
    opgg.refresh_summoner_info(summoner_id)
    opgg_request = opgg.get_summoner_request_result(summoner_name)
    summoner_winrate = opgg.get_summoner_recent_winrate(opgg_request)

    print("{name} playing with {champion} on team:{team}. Actual Winrate:{winrate}".format(
        name=summoner_name, champion=champion, team=team, winrate=summoner_winrate))


if __name__ == '__main__':
    main()
