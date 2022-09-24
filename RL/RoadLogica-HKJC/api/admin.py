from django.contrib import admin
from import_export import resources
from import_export.admin import ImportExportModelAdmin
from api.models import (Field, Rank, RankRecord,
                        Horse, HorseRank,
                        Jockey, JockeyRank, JockeyRecord,
                        Trainer, TrainerRank, TrainerRecord,
                        Task, TaskManager)


class FieldResource(resources.ModelResource):
    class Meta:
        model = Field


class FieldAdmin(ImportExportModelAdmin):
    resource_class = FieldResource
    list_display = ('rank_tag', 'rank_mask', 'place', 'number', 'name', 'rank_date', 'field', 'track',
                    'route', 'site_condition', 'reward', 'score', 'race_class', 'update_date')
    ordering = ('-rank_tag',)
    search_fields = ("rank_tag",)

    # 增加自定义按钮
    actions = ['update']

    def update(self, request, queryset):
        pass

    # 显示的文本，与django admin一致
    update.short_description = '更新'
    # icon，参考element-ui icon与https://fontawesome.com
    update.icon = 'fas fa-audio-description'

    update.type = 'info'
    update.action_type = 0
    update.action_url = '/api/?name=Rank'


admin.site.register(Field, FieldAdmin)


class RankResource(resources.ModelResource):
    class Meta:
        model = Rank


class RankAdmin(ImportExportModelAdmin):
    resource_class = RankResource
    list_display = ('rank_tag', 'rank_mask', 'number', 'performance', 'horse', 'stigma', 'weight_bear', 'jockey',
                    'is_over_weight', 'position', 'trainer', 'score', 'score_plus', 'position_weight',
                    'position_weight_plus', 'best_time', 'horse_age', 'horse_pound', 'sex', 'reward',
                    'priority_order', 'equipment', 'owner', 'father', 'mother', 'imported_type',
                    'classify', 'update_date')
    ordering = ('-rank_tag', 'classify', '-number')
    search_fields = ("rank_tag",)


admin.site.register(Rank, RankAdmin)


class RankRecordResource(resources.ModelResource):
    class Meta:
        model = RankRecord


class RankRecordAdmin(ImportExportModelAdmin):
    resource_class = RankRecordResource
    list_display = ('rank_tag', 'rank_mask', 'rank_id', 'order', 'number', 'horse', 'horse_no', 'jockey', 'jockey_id',
                    'trainer', 'trainer_id', 'actual_pound', 'position_weight', 'position', 'head_distance', 'blocking',
                    'finish_time', 'single_win', 'update_date')
    ordering = ('-rank_tag', 'rank_id', '-order')
    search_fields = ("rank_tag",)
    list_filter = ('update_date',)
    # 增加自定义按钮
    actions = ['update']

    def update(self, request, queryset):
        pass

    # 显示的文本，与django admin一致
    update.short_description = '更新'
    # icon，参考element-ui icon与https://fontawesome.com
    update.icon = 'fas fa-audio-description'

    update.type = 'info'
    update.action_type = 0
    update.action_url = '/api/?name=RankRecord'


admin.site.register(RankRecord, RankRecordAdmin)


class HorseResource(resources.ModelResource):
    class Meta:
        model = Horse


class HorseAdmin(ImportExportModelAdmin):
    resource_class = HorseResource
    list_display = ('name', 'birth_place', 'age', 'trainer', 'color', 'sex', 'owner',
                    'imported_type', 'current_score', 'reward', 'season_score', 'reward_total', 'father',
                    'reward_times', 'mother', 'lately_rank', 'grandfather', 'rank_times', 'location',
                    'arrival_date', 'update_date')
    ordering = ('-update_date',)
    search_fields = ("name",)


admin.site.register(Horse, HorseAdmin)


class HorseRankResource(resources.ModelResource):
    class Meta:
        model = HorseRank


class HorseRankAdmin(ImportExportModelAdmin):
    resource_class = HorseRankResource
    list_display = ('name', 'rank_id', 'ranking', 'rank_date', 'track', 'route', 'site_condition',
                    'race_class', 'position', 'score', 'trainer', 'jockey', 'head_distance', 'single_win',
                    'actual_pound', 'blocking', 'finish_time', 'position_weight', 'equipment', 'update_date')
    ordering = ('-rank_date',)
    search_fields = ("name",)


admin.site.register(HorseRank, HorseRankAdmin)


class JockeyResource(resources.ModelResource):
    class Meta:
        model = Jockey


class JockeyAdmin(ImportExportModelAdmin):
    resource_class = JockeyResource
    list_display = ('jockey_id', 'name', 'age', 'country', 'reward', 'win_times', 'avg_score', 'first', 'second',
                    'third', 'forth', 'rank_times', 'win_score', 'ten_rank_times', 'ten_head_horse', 'ten_win_score',
                    'ten_position_times', 'ten_position_score', 'update_date')

    ordering = ('-update_date',)
    search_fields = ("name",)


admin.site.register(Jockey, JockeyAdmin)


class JockeyRankResource(resources.ModelResource):
    class Meta:
        model = JockeyRank


class JockeyRankAdmin(ImportExportModelAdmin):
    resource_class = JockeyResource
    list_display = ('name', 'place', 'track', 'route', 'first', 'second', 'third', 'rank_times', 'update_date')
    search_fields = ("name",)


admin.site.register(JockeyRank, JockeyRankAdmin)


class JockeyRecordResource(resources.ModelResource):
    class Meta:
        model = JockeyRecord


class JockeyRecordAdmin(ImportExportModelAdmin):
    resource_class = JockeyRecordResource
    list_display = ('name', 'rank_date', 'place', 'rank_id', 'ranking', 'track', 'route', 'race_class',
                    'site_condition', 'horse', 'position', 'score', 'trainer', 'equipment', 'horse_weight',
                    'actual_pound', 'update_date')
    search_fields = ("name",)


admin.site.register(JockeyRecord, JockeyRecordAdmin)


class TrainerResource(resources.ModelResource):
    class Meta:
        model = Trainer


class TrainerAdmin(ImportExportModelAdmin):
    resource_class = TrainerResource
    list_display = ('trainer_id', 'name', 'age', 'reward', 'first', 'second', 'third',
                    'rank_times', 'ten_rank_times', 'ten_win_times', 'ten_win_score',
                    'ten_position_times', 'ten_position_score', 'update_date')
    ordering = ('-update_date',)
    search_fields = ("name",)


admin.site.register(Trainer, TrainerAdmin)


class TrainerRankResource(resources.ModelResource):
    class Meta:
        model = TrainerRank


class TrainerRankAdmin(ImportExportModelAdmin):
    resource_class = TrainerRankResource
    list_display = ('name', 'place', 'track', 'route', 'first', 'second', 'third', 'rank_times', 'update_date')
    search_fields = ("name",)


admin.site.register(TrainerRank, TrainerRankAdmin)


class TrainerRecordResource(resources.ModelResource):
    class Meta:
        model = TrainerRecord


class TrainerRecordAdmin(ImportExportModelAdmin):
    resource_class = TrainerRecordResource
    list_display = ('name', 'rank_id', 'horse', 'ranking', 'rank_date', 'track', 'route', 'site_condition',
                    'position', 'score', 'odds', 'jockey', 'equipment', 'horse_weight', 'actual_pound',
                    'first', 'second', 'third', 'update_date')
    search_fields = ("name",)


admin.site.register(TrainerRecord, TrainerRecordAdmin)


class TaskAdmin(admin.ModelAdmin):
    list_display = ('task_id', 'name', 'spider', 'url', 'finish', 'tags', 'update_date')
    list_filter = ('name', 'finish',)
    search_fields = ('url',)
    ordering = ('-update_date',)
    list_editable = ('finish',)


admin.site.register(Task, TaskAdmin)


class TaskManagerAdmin(admin.ModelAdmin):
    list_display = ('task_id', 'name', 'total', 'finish', 'percentage_paid', 'update_date')
    list_filter = ('task_id',)


admin.site.register(TaskManager, TaskManagerAdmin)
