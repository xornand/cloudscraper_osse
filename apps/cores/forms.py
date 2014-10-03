from django import forms
from models import Schedule
from djadmin_ext.admin_forms import BaseAjaxModelForm

class ScheduleForm(BaseAjaxModelForm):

    ajax_change_fields = ["type"]
    
    def create_field_and_assign_initial_value(self, queryset, selected_value):
        return lambda: super(ScheduleForm, self).create_field_and_assign_initial_value(queryset, selected_value)
    
    @property
    def dynamic_fields(self):
        
        selected_type = self.data.get('type') or self.initial.get('type')
        if not selected_type:
            return {}
        
        # print "Selected %s" % selected_type
        
        fields = {}
        
        if selected_type == "Manual":
            pass
        elif selected_type == "Cron":
            fields['cron_day'] = lambda : forms.CharField(required = False)
            fields['cron_month'] = lambda: forms.CharField(required = False)
            fields['cron_year'] = lambda: forms.CharField(required = False)
            fields['cron_hour'] = lambda: forms.CharField(required = False)
            fields['cron_minute'] = lambda: forms.CharField(required = False)
            fields['cron_second'] = lambda: forms.CharField(required = False)
            fields['cron_week'] = lambda: forms.CharField(required = False)
            fields['cron_day_of_week'] = lambda: forms.CharField(required = False)
            fields['cron_start_date'] = lambda: forms.CharField(required = False)
            fields['cron_end_date'] = lambda: forms.CharField(required = False)
            fields['cron_timezone'] = lambda: forms.CharField(required = False)
        elif selected_type == "Date":
            fields['date_run_time'] = lambda: forms.CharField(required = False)
            fields['date_timezone'] = lambda: forms.CharField(required = False)
        elif selected_type == "Interval":
            fields['interval_weeks'] = lambda: forms.IntegerField(required = False)
            fields['interval_days'] = lambda: forms.IntegerField(required = False)
            fields['interval_hours'] = lambda: forms.IntegerField(required = False)
            fields['interval_seconds'] = lambda: forms.IntegerField(required = False)
        else:
            print "Error"

        
        return fields

    class Meta:
        model = Schedule
        fields = ['title', 'type']
