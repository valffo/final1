from calendar import HTMLCalendar
from datetime import date
from itertools import groupby


from django.utils.html import conditional_escape as esc

class WorkoutCalendar(HTMLCalendar):

    def __init__(self, workouts):
        super(WorkoutCalendar, self).__init__()
        self.workouts = self.group_by_day(workouts)

    def formatday(self, day, weekday):
        if day != 0:
            cssclass = self.cssclasses[weekday]
            if date.today() == date(self.year, self.month, day):
                cssclass += ' today'
            if day in self.workouts:
                cssclass += ' filled'
                body = ['<ul class="calendar">']
                for workout in self.workouts[day]:
                    body.append('<li class="calendar">')
                    body.append('<a alt="%s" href="%s">' % (esc(workout.play.title), workout.get_absolute_url()))
                    body.append(esc(workout.time.strftime('%H:%M ')))
                    body.append('<br/>')
                    body.append(esc((workout.play.title[:15]+'...')) if len(esc(workout.play.title)) > 15 else esc(workout.play.title))
                    body.append('</a></li>')
                body.append('</ul>')
                return self.day_cell(cssclass, '%d %s' % (day, ''.join(body)))
            return self.day_cell(cssclass, day)
        return self.day_cell('noday', '&nbsp;')

    def formatmonth(self, year, month):
        self.year, self.month = year, month
        return super(WorkoutCalendar, self).formatmonth(year, month)

    def group_by_day(self, workouts):
        field = lambda workout: workout.date.day
        return dict(
            [(day, list(items)) for day, items in groupby(workouts, field)]
        )

    def day_cell(self, cssclass, body):
        return '<td class="%s">%s</td>' % (cssclass, body)