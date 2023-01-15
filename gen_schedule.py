import leather

from database_manager import get_hours


def x(row, index):
    return row['x']

def y(row, index):
    return row['q']['y'][0]


async def create_schedule_last_hour():
    data_logs = await get_hours()
    data = [{'x': dl[0], 'q': { 'y': [dl[1]] }} for dl in data_logs]

    chart = leather.Chart('Active last hours')
    chart.add_line(data, x=x, y=y)
    chart.add_x_axis(name='time')
    chart.add_y_axis(name='count')
    chart.to_svg('active_last_hours.html')

