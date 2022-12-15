from django.shortcuts import render, redirect

from django.contrib import messages
from django.shortcuts import get_object_or_404, redirect

#日付型のデータを扱うためのインポート処理
import datetime
from django.utils import timezone

# フォームの設定のためのインポート
#from .forms import ScheduleForm

# ログインユーザModel参照用
from django.contrib.auth.models import User

from django.conf import settings
from django.db.models import Q
from django.shortcuts import get_object_or_404

from django.views import generic

from django.views.generic import DeleteView, DetailView

from django.urls import reverse_lazy
from .models import Base, Seat, Schedule
#ユーザ名取得用
from django.contrib.auth.models import User
from django.contrib.auth.mixins import UserPassesTestMixin

#ログイン状態の判定処理用（未ログイン状態でのアクセス不可）
from django.contrib.auth.mixins import LoginRequiredMixin

#登録したModel:Scheduleについて、登録者以外による削除処理の制限のための処理
from django.core.exceptions import PermissionDenied


#拠点一覧用 ListView
class BaseList(LoginRequiredMixin, generic.ListView):
    model = Base
    ordering = 'name'

#座席一覧用 ListView
class SeatList(LoginRequiredMixin, generic.ListView):
    template_name = 'app/calendar.html'
    model = Seat
    ordering = 'seatno'

    """
    def get_queryset(self):
        base = self.base = get_object_or_404(Base, pk=self.kwargs['pk'])
        queryset = super().get_queryset().filter(base=base)

        return queryset
    """

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        base = self.base = get_object_or_404(Base, pk=self.kwargs['pk'])
        context['base'] = self.base

        today = datetime.date.today()
        # calender.htmlでも参照する変数のため、グローバル変数として事前に宣言
        global schedule

        # どの日を基準にカレンダーを表示するかの処理
        # 年月日の指定があればそれを、なければ今日からの表示
        year = self.kwargs.get('year')
        month = self.kwargs.get('month')
        day = self.kwargs.get('day')
        if year and month and day:
            base_date = datetime.date(year=year, month=month, day=day)
        else:
            base_date = today

        # カレンダーは1週間分表示  基準日から1週間の日付を作成
        days = [base_date + datetime.timedelta(days=day) for day in range(7)]
        start_day = days[0]
        end_day = days[-1]

        # 選択された拠点の値でフィルターした結果（Model：Seat）を取得
        base = self.base = get_object_or_404(Base, pk=self.kwargs['pk'])
        queryset = super().get_queryset().filter(base=base)
        #print(queryset)
        # 選択された拠点の値でフィルターした結果（Model：Seat）の総数を取得
        total_queryset = super().get_queryset().filter(base=base).count()

        # DEBUG処理
#        print(queryset)
#        print(total_queryset)
#        print(queryset[0])

        # 選択された拠点のシートの数だけ、1週間分の、値がnoneなカレンダーを作る
        calendar = {}
        # querysetで取得した分だけ、空の辞書を作成
        for i in queryset:
            row = {}
            row2 = {}
            # 作成した空の辞書に対象範囲の日付を格納、また、空席としてnoneを指定
            for day in days:
                row[day] = "none"
            # querysetで取得した座席毎に日付のデータと組み合わせる形でリストを作成
            calendar[i] = row

        # DEBUG処理
#        print(calendar)
        schedule_users = []
        sches = []
        # 取得されたquerysetに格納された座席番号分処理を繰り返す
        for x in range(0, total_queryset):
#           # 選択された拠点とquerysetに格納された座席番号と対象の日付範囲で値でフィルターした結果（Model：Schedul）を取得
            # scope_day = days[x]
            #print(scope_day)
            #schedule_user = Schedule.objects.values('user').filter(base=base, seat=queryset[x], date=scope_day)
            #print(schedule_user)

            # 選択された拠点とquerysetに格納された座席番号と対象の日付範囲で値でフィルターした結果（Model：Schedul）を取得し
            # 取得されたレコードの分だけ、calendarに一致するデータの検証と値の更新を実施
            for schedule in Schedule.objects.filter(base=base, seat=queryset[x], date__range=[start_day, end_day]):
                # scheduleに格納された結果の日時を日付型に変換
                local_dt = timezone.localtime(schedule.date)
                booking_date = local_dt.date()
                # DEBUG処理
                #print(start_day)
                #print(end_day)
                #print(local_dt)
                #print(booking_date)

                # 一致するデータを検索するために、querysetに格納された座席番号を取得
                z = queryset[x]
                #print(z)
                
                # 一致するデータがあった場合は予約済みと判断し、Falseを指定
                if booking_date in calendar[z]:
                    #calendar[z][booking_date] = False

                    

                    # ユーザ名で表示するために予約したユーザのpkを利用してUserテーブルから値を取得
                    schedule_user = Schedule.objects.values_list('user', flat=True).filter(base=base, seat=queryset[x], date=booking_date)
                    #print(schedule_user[0])
                    users = User.objects.values_list('username', flat=True).filter(pk=schedule_user[0])
                    #print(users[0])
                    #schedule_users.append(users[0])
                    #print(schedule_users)
                    calendar[z][booking_date] = users[0]
                    
                    #print(schedule)
                    
                    # delete画面遷移のためにModel：Scheduleの対象のidでリストを作成
                    sche = Schedule.objects.values_list('id', flat=True).filter(base=base, seat=queryset[x], date=booking_date)
                    #print(sche[0])
                    sches.insert(0, sche[0])
                    #print(sches)
                    
        # delete画面遷移のためにModel：Scheduleの対象のidで作成されたリストの内容を条件にseat、dateでソートした結果をクエリを取得
        # ※カレンダーに表示される順番
        calendar_book = Schedule.objects.values_list('id', flat=True).filter(pk__in=sches).order_by("seat", "date").reverse()
        # Contextに格納するためにlist型に変換
        calendar_books = list(calendar_book)

        print(calendar_books)
        print(sches)
        
        schedules = Schedule.objects.filter(base=base, date__range=[start_day, end_day])
        #print(schedules)
        #return render(request, 'app/calendar.html', {'schedules': schedules})


        


        # returnする値の定義
        context['seat'] = queryset
        context['sche'] = calendar_books
        #context['schedule_users'] = schedule_users
        context['schedule'] = schedules
        context['calendar'] = calendar
        context['days'] = days
        context['start_day'] = start_day
        context['end_day'] = end_day
        context['before'] = days[0] - datetime.timedelta(days=7)
        context['next'] = days[-1] + datetime.timedelta(days=1)
        context['today'] = today
        context['public_holidays'] = settings.PUBLIC_HOLIDAYS

        # print(calendar)
        return context

class Booking(LoginRequiredMixin, generic.CreateView):
    model = Schedule
    template_name = 'app/booking.html'
    
    #form_class = ScheduleForm
    model = Schedule
    fields = ()
    template_name = 'app/booking.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['base'] = get_object_or_404(Base, pk=self.kwargs['pk'])
        context['seatno'] = get_object_or_404(Seat, pk=self.kwargs['no'])
        context['user'] = self.request.user
        return context

    def form_valid(self, form):
        base = get_object_or_404(Base, pk=self.kwargs['pk'])
        seatno = get_object_or_404(Seat, pk=self.kwargs['no'])
        user = self.request.user
        year = self.kwargs.get('year')
        month = self.kwargs.get('month')
        day = self.kwargs.get('day')
        date = datetime.datetime(year=year, month=month, day=day)

        if Schedule.objects.filter(base=base, seat=seatno, date=date).exists():
            messages.error(self.request, '入れ違いで予約されました。')
        else:
            schedule = form.save(commit=False)
            schedule.date = date
            schedule.user = user
            schedule.base = base
            schedule.seat = seatno
            schedule.save()
        
        """
        def get_initial(self):
            initial = super().get_initial()
            initial["date"] = date
            initial["user"] = user
            initial["base"] = base
            initial["seat"] = seatno
        """

        # 正常に予約処理が実行された場合は指定日時先頭にカレンダー画面に戻る
        return redirect('app:calendar', pk=base.pk, year=year, month=month, day=day)
        # render(request, 'app/booking.html', context)
        
        # 正常に予約処理が実行された場合はデフォルトのカレンダー画面に戻る（コメントアウト中）
        #return redirect('app:calendar', pk=base.pk)


"""
class ScheduleDetail(DetailView):
    model = Schedule
    template_name = 'app/scheduledetail.html'
"""

class ScheduleDelete(LoginRequiredMixin, DeleteView):
    model = Schedule
    template_name = 'app/scheduledelete.html'
    success_url = reverse_lazy('app:base_list')

    # 予約をしたユーザ以外のユーザがdelete出来ないようにするための処理
    def get_object(self, queryset=None):
        obj = super().get_object(queryset)

        if obj.user != self.request.user:
            raise PermissionDenied
    
        return obj

"""
class OnlyScheduleMixin(UserPassesTestMixin):
    raise_exception = True

class ScheduleDelete(OnlyScheduleMixin, generic.DeleteView):
    model = Schedule
    template_name = 'app/scheduledelete.html'
    success_url = reverse_lazy('app:calendar')

    def test_func(self):
        #schedule = get_object_or_404(Schedule, pk=self.kwargs['sche'])
        return schedule.user == self.request.user or self.request.user.is_superuser

    def detail(request, sche):

        schedule = get_object_or_404(Schedule, pk=self.kwargs['sche'])
        print(schedule)
        return render(request, 'app/scheduledelete.html', {'sche': schedule })
"""