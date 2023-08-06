from io import StringIO

from . import season_state_mapping, map_datetime
from ...model import Season


def map_season(season: Season) -> str:
    with StringIO() as io:
        # {season.name}
        io.write(season.name)
        io.write('\n')

        # 代号：{season.code}
        io.write('代号：')
        io.write(season.code)
        io.write('\n')

        if season.state:
            io.write('状态：')
            io.write(season_state_mapping[season.state])
            io.write('\n')

        if season.start_time:
            io.write('开始时间：')
            io.write(map_datetime(season.start_time))
            io.write('\n')

        if season.finish_time:
            io.write('结束时间：')
            io.write(map_datetime(season.finish_time))
            io.write('\n')

        # 半庄战：返点：30000  马点：50 30 -10 -30
        io.write('半庄战：')
        if season.config.south_game_enabled:
            io.write('返点：')
            io.write(str(season.config.south_game_origin_point))
            io.write(' 马点：')
            for i in season.config.south_game_horse_point:
                io.write(str(i))
                io.write(' ')
        else:
            io.write('关闭')
        io.write('\n')

        # 东风战：关闭
        io.write('东风战：')
        if season.config.east_game_enabled:
            io.write('返点：')
            io.write(str(season.config.east_game_origin_point))
            io.write(' 马点：')
            for i in season.config.east_game_horse_point:
                io.write(str(i))
                io.write(' ')
        else:
            io.write('关闭')
        io.write('\n')

        # PT精度：1
        io.write('PT精度：')
        io.write(str(10 ** season.config.point_precision))
        io.write('\n')

        return io.getvalue().strip()
