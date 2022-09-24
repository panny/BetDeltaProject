import json
import copy
from django.shortcuts import render, redirect, HttpResponse
from django.views import View
from django.http import JsonResponse
from django.db.models import Count

# Create your views here.
import datetime

from api.models import (Field, Rank, RankRecord,
                        Horse, HorseRank,
                        Jockey, JockeyRank, JockeyRecord,
                        Trainer, TrainerRank, TrainerRecord,
                        Task, TaskManager)
from utils.time import Time
from utils.settings import SPIDER_UR
from api import tasks


class FieldView(View):

    def get(self, request):
        data = request.GET.dict()
        if data:
            _query_set = []
            if 'type' in data and data['type'] == 'distinct':
                query_set = Field.objects.filter(update_date__gte=datetime.date.today()).values('rank_tag').distinct()
                _query_set = [x for x in query_set]
            elif 'type' in data and data['type'] == 'odds':
                rank_mask = data.get('rank_mask').split(',') if data.get('rank_mask') else ['HV', 'ST']
                rank_tag = Time.get_format_time(t_format='%Y%m%d')
                query_set = Field.objects.filter(rank_tag__contains=rank_tag, rank_mask__in=rank_mask).distinct()
                _query_set = [x for x in query_set]
            else:
                query_set = Field.objects.filter(**data)
            if query_set:
                _query_set = [x.to_dict() for x in query_set]
            return JsonResponse({'status': '200', 'data': _query_set})
        return JsonResponse({'status': '401', 'data': data})

    def post(self, request):
        data = request.POST.dict()
        rank_tag = data.get('rank_tag', '')
        rank_mask = data.get('rank_mask', '')
        if rank_tag:
            field, status = Field.objects.update_or_create(rank_tag=rank_tag, rank_mask=rank_mask, defaults=data)
            return JsonResponse({'status': '200', 'data': field.to_dict()})
        return JsonResponse({'status': '401', 'data': data})


class RankView(View):

    def get(self, request):
        data = request.GET.dict()
        if data:
            query_set = Rank.objects.filter(**data)
            if query_set:
                _query_set = [x.to_dict() for x in query_set]
                return JsonResponse({'status': '200', 'data': _query_set})
        return JsonResponse({'status': '401', 'data': data})

    def post(self, request):
        data = request.POST.dict()
        rank_tag = data.get('rank_tag', '')
        rank_mask = data.get('rank_mask', '')
        number = data.get('number', '')
        classify = data.get('classify', '')
        if rank_tag and rank_mask and classify and number:
            rank, status = Rank.objects.update_or_create(rank_tag=rank_tag, rank_mask=rank_mask, number=number, classify=classify,
                                                         defaults=data)
            return JsonResponse({'status': '200', 'data': rank.to_dict()})
        return JsonResponse({'status': '401', 'data': data})


class RankRecordView(View):

    def get(self, request):
        data = request.GET.dict()
        if data:
            _query_set = []
            if 'type' in data and data['type'] == 'distinct':
                rank_mask = data.get('rank_mask').split(',') if data.get('rank_mask') else ['HV', 'ST']
                query_set = RankRecord.objects.filter(rank_mask__in=rank_mask).values('rank_tag').distinct()
                _query_set = [x for x in query_set]
            else:
                query_set = RankRecord.objects.filter(**data)
                if query_set:
                    _query_set = [x.to_dict() for x in query_set]
            return JsonResponse({'status': '200', 'data': _query_set})
        return JsonResponse({'status': '401', 'data': data})

    def post(self, request):
        data = request.POST.dict()
        rank_tag = data.get('rank_tag', '')
        horse = data.get('horse', '')
        if rank_tag and horse:
            rank, status = RankRecord.objects.update_or_create(rank_tag=rank_tag, horse=horse, defaults=data)
            return JsonResponse({'status': '200', 'data': rank.to_dict()})
        return JsonResponse({'status': '401', 'data': data})


class HorseView(View):

    def get(self, request):
        data = request.GET.dict()
        if data:
            _query_set = []
            if 'type' in data and data['type'] == 'distinct':
                query_set = Horse.objects.filter(update_date__gte=datetime.date.today()).values('horse_no',
                                                                                                'horse_id').distinct()
                _query_set = [x for x in query_set]
            else:
                query_set = Horse.objects.filter(**data)
                if query_set:
                    _query_set = [x.to_dict() for x in query_set]
            return JsonResponse({'status': '200', 'data': _query_set})
        return JsonResponse({'status': '401', 'data': data})

    def post(self, request):
        data = request.POST.dict()
        horse_id = data.get('horse_id', '')
        if horse_id:
            horse, status = Horse.objects.update_or_create(horse_id=horse_id, defaults=data)
            return JsonResponse({'status': '200', 'data': horse.to_dict()})
        return JsonResponse({'status': '401', 'data': data})


class HorseRankView(View):

    def get(self, request):
        data = request.GET.dict()
        if data:
            query_set = HorseRank.objects.filter(**data)
            if query_set:
                _query_set = [x.to_dict() for x in query_set]
                return JsonResponse({'status': '200', 'data': _query_set})
        return JsonResponse({'status': '401', 'data': data})

    def post(self, request):
        data = request.POST.dict()
        horse_id = data.get('horse_id', '')
        rank_id = data.get('rank_id', '')
        if horse_id and rank_id:
            horse, status = HorseRank.objects.update_or_create(horse_id=horse_id, rank_id=rank_id, defaults=data)
            return JsonResponse({'status': '200', 'data': horse.to_dict()})
        return JsonResponse({'status': '401', 'data': data})


class JockeyView(View):

    def get(self, request):
        data = request.GET.dict()
        if data:
            _query_set = []
            if 'type' in data and data['type'] == 'distinct':
                query_set = Jockey.objects.filter(update_date__gte=datetime.date.today()).values('jockey_id').distinct()
                _query_set = [x for x in query_set]
            else:
                query_set = Jockey.objects.filter(**data)
                if query_set:
                    _query_set = [x.to_dict() for x in query_set]
            return JsonResponse({'status': '200', 'data': _query_set})
        return JsonResponse({'status': '401', 'data': data})

    def post(self, request):
        data = request.POST.dict()
        jockey_id = data.get('jockey_id', '')
        if jockey_id:
            jockey, status = Jockey.objects.update_or_create(jockey_id=jockey_id, defaults=data)
            return JsonResponse({'status': '200', 'data': jockey.to_dict()})
        return JsonResponse({'status': '401', 'data': data})


class JockeyRecordView(View):

    def get(self, request):
        data = request.GET.dict()
        if data:
            query_set = JockeyRecord.objects.filter(**data)
            if query_set:
                _query_set = [x.to_dict() for x in query_set]
                return JsonResponse({'status': '200', 'data': _query_set})
        return JsonResponse({'status': '401', 'data': data})

    def post(self, request):
        data = request.POST.dict()
        jockey_id = data.get('jockey_id', '')
        rank_id = data.get('rank_id', '')
        if rank_id and jockey_id:
            jockey, status = JockeyRecord.objects.update_or_create(jockey_id=jockey_id, rank_id=rank_id, defaults=data)
            rank_record = RankRecord.objects.filter(jockey_id=jockey_id, rank_id=rank_id).first()
            if rank_record:
                jockey.horse_no = rank_record.horse_no
                jockey.trainer_id = rank_record.trainer_id
                jockey.save()
            return JsonResponse({'status': '200', 'data': jockey.to_dict()})
        return JsonResponse({'status': '401', 'data': data})


class JockeyRankView(View):

    def get(self, request):
        data = request.GET.dict()
        if data:
            query_set = JockeyRank.objects.filter(**data)
            if query_set:
                _query_set = [x.to_dict() for x in query_set]
                return JsonResponse({'status': '200', 'data': _query_set})
        return JsonResponse({'status': '401', 'data': data})

    def post(self, request):
        data = request.POST.dict()
        jockey_id = data.get('jockey_id', '')
        place = data.get('place', '')
        track = data.get('track', '')
        route = data.get('route', '')
        if jockey_id and place and route:
            jockey, status = JockeyRank.objects.update_or_create(jockey_id=jockey_id, place=place,
                                                                 track=track, route=route,
                                                                 defaults=data)
            return JsonResponse({'status': '200', 'data': jockey.to_dict()})
        return JsonResponse({'status': '401', 'data': data})


class TrainerView(View):

    def get(self, request):
        data = request.GET.dict()
        if data:
            _query_set = []
            if 'type' in data and data['type'] == 'distinct':
                query_set = Trainer.objects.filter(update_date__gte=datetime.date.today()).values(
                    'trainer_id').distinct()
                _query_set = [x for x in query_set]
            else:
                query_set = Trainer.objects.filter(**data)
                if query_set:
                    _query_set = [x.to_dict() for x in query_set]
            return JsonResponse({'status': '200', 'data': _query_set})
        return JsonResponse({'status': '401', 'data': data})

    def post(self, request):
        data = request.POST.dict()
        trainer_id = data.get('trainer_id', '')
        if trainer_id:
            trainer, status = Trainer.objects.update_or_create(trainer_id=trainer_id, defaults=data)
            return JsonResponse({'status': '200', 'data': trainer.to_dict()})
        return JsonResponse({'status': '401', 'data': data})


class TrainerRecordView(View):

    def get(self, request):
        data = request.GET.dict()
        if data:
            query_set = TrainerRecord.objects.filter(**data)
            if query_set:
                _query_set = [x.to_dict() for x in query_set]
                return JsonResponse({'status': '200', 'data': _query_set})
        return JsonResponse({'status': '401', 'data': data})

    def post(self, request):
        data = request.POST.dict()
        trainer_id = data.get('trainer_id', '')
        rank_id = data.get('rank_id', '')
        if rank_id and trainer_id:
            trainer, status = TrainerRecord.objects.update_or_create(trainer_id=trainer_id, rank_id=rank_id,
                                                                     defaults=data)
            rank_record = RankRecord.objects.filter(trainer_id=trainer_id, rank_id=rank_id).first()
            if rank_record:
                trainer.horse_no = rank_record.horse_no
                trainer.jockey_id = rank_record.jockey_id
                trainer.save()
            return JsonResponse({'status': '200', 'data': trainer.to_dict()})
        return JsonResponse({'status': '401', 'data': data})


class TrainerRankView(View):

    def get(self, request):
        data = request.GET.dict()
        if data:
            query_set = TrainerRank.objects.filter(**data)
            if query_set:
                _query_set = [x.to_dict() for x in query_set]
                return JsonResponse({'status': '200', 'data': _query_set})
        return JsonResponse({'status': '401', 'data': data})

    def post(self, request):
        data = request.POST.dict()
        trainer_id = data.get('trainer_id', '')
        place = data.get('place', '')
        track = data.get('track', '')
        route = data.get('route', '')
        if trainer_id and place and route:
            trainer, status = TrainerRank.objects.update_or_create(trainer_id=trainer_id, place=place,
                                                                   track=track, route=route,
                                                                   defaults=data)
            return JsonResponse({'status': '200', 'data': trainer.to_dict()})
        return JsonResponse({'status': '401', 'data': data})


class TaskView(View):

    def get(self, request):
        data = request.GET.dict()
        if data:
            _query_set = []
            if 'type' in data and data['type'] == 'distinct':
                data.pop('type')
                if 'tags' not in data:
                    data['tags'] = Time.get_format_time(t_format='%Y%m%d')
                query_set = Task.objects.filter(**data).exclude(finish='3').values('task_id', 'url').distinct()
                _query_set = [x for x in query_set]
            else:
                query_set = Task.objects.filter(**data)
                if query_set:
                    _query_set = [x.to_dict() for x in query_set]
            return JsonResponse({'status': '200', 'data': _query_set})
        return JsonResponse({'status': '401', 'data': data})

    def post(self, request):
        data = request.POST.dict()
        task_id = data.get('task_id', '')
        url = data.get('url', '')
        if task_id and url:
            task, status = Task.objects.update_or_create(task_id=task_id, url=url, defaults=data)
            return JsonResponse({'status': '200', 'data': task.to_dict()})
        return JsonResponse({'status': '401', 'data': data})


class TaskManagerView(View):

    def get(self, request):
        data = request.GET.dict()
        if data:
            query_set = TaskManager.objects.filter(**data)
            if query_set:
                _query_set = [x.to_dict() for x in query_set]
                return JsonResponse({'status': '200', 'data': _query_set})
        return JsonResponse({'status': '401', 'data': data})

    def post(self, request):
        data = request.POST.dict()
        if not data:
            task_id = Time.get_format_time(t_format='%Y%m%d')
            data['task_id'] = task_id
        tasks = Task.objects.filter(**data, spider__isnull=False).values('task_id', 'name', 'spider', 'finish',
                                                                         'tags').annotate(
            total=Count('finish'))
        tmp = {}
        for task in tasks:
            name = task.get("name")
            finish = task.get("finish")
            total = task.get("total")
            task['spider'] = task.get('spider').lower()
            if name in tmp:
                if finish == '2':
                    task['finish'] = tmp[name]['finish'] + total
                else:
                    task['finish'] = tmp[name]['finish']
                task['total'] = tmp[name]['total'] + total
            else:
                task['finish'] = total if finish == '2' else 0
            tmp[name] = task
        for val in tmp.values():
            val.pop('spider')
            TaskManager.objects.update_or_create(task_id=val.get('task_id'), name=val.get('name'),
                                                 tags=val.get('tags'), defaults=val)
        return JsonResponse({'status': '200', 'data': tmp})


class IndexView(View):

    def get(self, request):
        data = request.GET.dict()
        if data.get('name') and data.get('name') in SPIDER_UR:
            info = SPIDER_UR[data['name']]
            tasks.spider_run.delay(info)
        return redirect('/admin/api/task/')

    def post(self, request):
        data = request.POST.dict()
        if data.get('name') and data.get('name') in SPIDER_UR:
            info = SPIDER_UR[data['name']]
            tasks.spider_run.delay(info)
        return redirect('/admin/api/task/')


class AdminView(View):

    def get(self, request):
        return render(request, 'index2.html')

    def post(self, request):
        data = request.POST.dict()
        time = data.get('time')
        if not time:
            rank_tag = RankRecord.objects.filter().distinct('rank_tag').values('rank_tag').order_by('-rank_tag').first()
            time = rank_tag.get('rank_tag')[:8]
        scene = data.get('scene', 1)
        rank_tag = f"{time}{scene}"
        values = "rank_id,horse,order,horse_no,jockey,trainer,trainer,head_distance,blocking"
        horse_record = RankRecord.objects.filter(rank_tag=rank_tag).values(*values.split(','))
        tableData = []
        if horse_record:
            values = 'track,route'
            field = Field.objects.filter(rank_tag=rank_tag).values(*values.split(',')).first()
            if not field:
                field = HorseRank.objects.filter(rank_id=horse_record[0].get('rank_id')).values(
                    *values.split(',')).first()
            field = field if field else {}
            for rank in horse_record:
                tmp = copy.deepcopy(rank)
                tmp.update(field)
                tableData.append(tmp)
        return HttpResponse(json.dumps(tableData))


class OptionView(View):

    def get(self, request):
        data = request.GET.dict()
        time = data.get('time')
        type = data.get('type', 'options')
        if type == 'options':
            ranks = RankRecord.objects.all().distinct('rank_tag').values('rank_tag').order_by('-rank_tag')
            options = []
            for rank in ranks:
                tag = rank.get('rank_tag')[:8]
                if tag not in options:
                    options.append(tag)
            return HttpResponse(json.dumps(options))
        else:
            if not time:
                rank_tag = RankRecord.objects.filter().distinct('rank_tag').values('rank_tag').order_by(
                    '-rank_tag').first()
                time = rank_tag.get('rank_tag')[:8]
            ranks = RankRecord.objects.filter(rank_tag__contains=time).distinct('rank_tag').values('rank_tag')
            scenelist = []
            for rank in ranks:
                scenelist.append(int(rank.get('rank_tag')[8:]))
            scenelist.sort()
            return HttpResponse(json.dumps(scenelist))
