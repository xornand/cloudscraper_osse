from django.contrib.admin.sites import AdminSite

from django.contrib.auth.models import User, Group
from django.contrib.auth.admin import UserAdmin, GroupAdmin

from django.contrib.sites.models import Site
from django.contrib.sites.admin import SiteAdmin

#from websites.models import Website
#from websites.admin import WebsiteAdmin

from cores.models import Core, Schedule, Ranking, Content, ContentDescriptor, Filter
from cores.admin import CoreAdmin, ScheduleAdmin, RankingAdmin, ContentAdmin, ContentDescriptorAdmin, FilterAdmin

from .forms import SuperAdminAuthenticationForm, UserAuthenticationForm

from django_mailbox.models import MessageAttachment, Message, Mailbox
from django_mailbox.admin import MessageAttachmentAdmin, MessageAdmin, MailboxAdmin

#from dropbox_plugin.models import Dropbox
#from dropbox_plugin.admin import DropboxAdmin

from locals.models import Directory
from locals.admin import DirectoryAdmin

import cores
from django.template.response import TemplateResponse
from django.utils.translation import ugettext as _
from django.views.decorators.cache import never_cache

from django.core.exceptions import PermissionDenied
from django.contrib import messages
from django.contrib.admin import helpers
from django.contrib.admin.actions import delete_selected
from django.contrib.admin.util import get_deleted_objects, model_ngettext
from django.db import router
from django.template.response import TemplateResponse
from django.utils.encoding import force_text
from django.utils.translation import ugettext_lazy, ugettext as _
from constance.admin import Config, ConstanceAdmin

class SuperAdminSite(AdminSite):

    login_form = SuperAdminAuthenticationForm
    tasks_template = None
    
    def __init__(self, *args, **kwargs):
        super(SuperAdminSite, self).__init__(*args, **kwargs)
        self.disable_action('delete_selected')
        # attach our custom delete_selected (static method)
        self.add_action(self._delete_selected, 'delete_selected')

    @staticmethod
    def _delete_selected(modeladmin, request, queryset):
        print modeladmin.__class__.__name__
        if modeladmin.__class__.__name__ == 'CoreAdmin':
            # my custom code
            #return delete_selected(modeladmin, request, queryset)
            
            all = queryset.all()
            print type(all)
            print all
            print all.first()
            
            default_found = False
            for core in queryset.all():
                if core.title == 'default':
                    default_found = True
                    print "Default found"
            
            if default_found:
                
                opts = modeladmin.model._meta
                app_label = opts.app_label
                
                # Check that the user has delete permission for the actual model
                if not modeladmin.has_delete_permission(request):
                    raise PermissionDenied

                using = router.db_for_write(modeladmin.model)
                
                # Populate deletable_objects, a data structure of all related objects that
                # will also be deleted.
                deletable_objects, perms_needed, protected = get_deleted_objects(
                    queryset, opts, request.user, modeladmin.admin_site, using)

                # The user has already confirmed the deletion.
                # Do the deletion and return a None to display the change list view again.
                if request.POST.get('post'):
                    if perms_needed:
                        raise PermissionDenied
                    n = queryset.count()
                    if n:
                        for obj in queryset:
                            obj_display = force_text(obj)
                            modeladmin.log_deletion(request, obj, obj_display)
                        queryset.delete()
                        modeladmin.message_user(request, _("Successfully deleted %(count)d %(items)s.") % {
                            "count": n, "items": model_ngettext(modeladmin.opts, n)
                        }, messages.SUCCESS)
                    # Return None to display the change list page again.
                    return None

                if len(queryset) == 1:
                    objects_name = force_text(opts.verbose_name)
                else:
                    objects_name = force_text(opts.verbose_name_plural)

                # if we selected more than 1 cores, remove all others except the default cores because we do not want
                # to render them in the not allowed list - they CAN be deleted, it's just that in the list
                # there is a default core selected as well
                # other solution is do clear the list and add only one - default core
                
                if queryset.count() > 1:
                    deletable_objects = [core for core in deletable_objects if core.find('default') != -1]
                    # for core in deletable_objects:
                        # print core
                        # print type(core)
                
                context = {
                    "title": "Not allowed",
                    "objects_name": objects_name,
                    "deletable_objects": [deletable_objects],
                    'queryset': queryset,
                    "perms_lacking": perms_needed,
                    "protected": protected,
                    "opts": opts,
                    "app_label": app_label,
                    'action_checkbox_name': helpers.ACTION_CHECKBOX_NAME, 
                }

                # Display the confirmation page
                return TemplateResponse(request, "admin/delete_not_allowed.html", context, current_app=modeladmin.admin_site.name) 
                
            else:
                return delete_selected(modeladmin, request, queryset)
            
        else:
            #call default one
            return delete_selected(modeladmin, request, queryset)

    def has_permission(self, request):
        """
        Allow only superusers.
        """
        return request.user.is_active and request.user.is_superuser
    
    @never_cache
    def index(self, request, extra_context=None):
        """
        Displays the main admin index page, which lists all of the installed
        apps that have been registered in this site.
        """
        #app_dict = {}
        user = request.user
        # for model, model_admin in self._registry.items():
            # app_label = model._meta.app_label
            # has_module_perms = user.has_module_perms(app_label)

            # if has_module_perms:
                # perms = model_admin.get_model_perms(request)

                # # Check whether user has any perm for this module.
                # # If so, add the module to the model_list.
                # if True in perms.values():
                    # info = (app_label, model._meta.model_name)
                    # model_dict = {
                        # 'name': capfirst(model._meta.verbose_name_plural),
                        # 'object_name': model._meta.object_name,
                        # 'perms': perms,
                    # }
                    # if perms.get('change', False):
                        # try:
                            # model_dict['admin_url'] = reverse('admin:%s_%s_changelist' % info, current_app=self.name)
                        # except NoReverseMatch:
                            # pass
                    # if perms.get('add', False):
                        # try:
                            # model_dict['add_url'] = reverse('admin:%s_%s_add' % info, current_app=self.name)
                        # except NoReverseMatch:
                            # pass
                    # if app_label in app_dict:
                        # app_dict[app_label]['models'].append(model_dict)
                    # else:
                        # app_dict[app_label] = {
                            # 'name': app_label.title(),
                            # 'app_label': app_label,
                            # 'app_url': reverse('admin:app_list', kwargs={'app_label': app_label}, current_app=self.name),
                            # 'has_module_perms': has_module_perms,
                            # 'models': [model_dict],
                        # }

        # Sort the apps alphabetically.
        #app_list = list(six.itervalues(app_dict))
        #app_list.sort(key=lambda x: x['name'])

        # Sort the models alphabetically within each app.
        # for app in app_list:
            # app['models'].sort(key=lambda x: x['name'])
        
        task_list = cores.sched.get_jobs()
        cores.sched.print_jobs()

        # count objects
        dir_cnt = Directory.objects.all().count()
        mailbox_cnt = Mailbox.objects.all().count()
        #website_cnt = Website.objects.all().count()
        website_cnt = 0
        file_cnt = cores.f1.get_doc_num(u"file")
        email_cnt = cores.f1.get_doc_num(u"email")
        webpage_cnt = cores.f1.get_doc_num(u"webpage")
        index_size = cores.f1.get_size()
        total_docs = cores.f1.get_doc_num(u"")
        
        context = {
            'title': _('Dashboard'),
            #'app_list': app_list,
            'task_list': task_list,
            'dir_cnt': dir_cnt,
            'mailbox_cnt': mailbox_cnt,
            'website_cnt': website_cnt,
            'file_cnt': file_cnt,
            'email_cnt': email_cnt,
            'webpage_cnt': webpage_cnt,
            'index_size': "%.3f MiB" % index_size,
            'total_docs': total_docs,
        }
        context.update(extra_context or {})
        return TemplateResponse(request, self.index_template or
                                'admin/index.html', context,
                                current_app=self.name)
    
    def get_urls(self):
    
        from functools import update_wrapper
        def wrap(view, cacheable=False):
            def wrapper(*args, **kwargs):
                return self.admin_view(view, cacheable)(*args, **kwargs)
            return update_wrapper(wrapper, view)
        
        from django.conf.urls import patterns, url

        urls = super(SuperAdminSite, self).get_urls()
        my_urls = patterns('',
            url(r'^tasks/$', wrap(self.tasks_view), name='tasks_view')
        )
        
        # IMPORTANT: my_urls MUST BE BEFORE urls!!!
        # http://stackoverflow.com/questions/15294124/override-adminsite-to-append-custom-urls
        return my_urls + urls
    
    def tasks_view(self, request, extra_context=None):
        
        
        cl = []
        from django.utils.translation import ungettext
        selection_note_all = ungettext('%(total_count)s selected',
            'All %(total_count)s selected', 0) 
        
        context = {
            'module_name': 'tasks',
            'selection_note': _('0 of %(cnt)s selected') % {'cnt': 0},
            'selection_note_all': selection_note_all % {'total_count': 0},
            'title': 'Current tasks',
            'is_popup': False,
            'cl': cl,
            'media': None,
            'has_add_permission': False,
            'opts': None,
            'app_label': 'tasks',
            #'action_form': action_form,
            #'actions_on_top': self.actions_on_top,
            #'actions_on_bottom': self.actions_on_bottom,
            #'actions_selection_counter': self.actions_selection_counter,
            'preserved_filters': (),
        }
        
        context.update(extra_context or {})
        
        return TemplateResponse(request, self.tasks_template or
                                'admin/change_list_tasks.html', context,
                                current_app=self.name)
 


class UserSite(AdminSite):

    login_form = UserAuthenticationForm

    def has_permission(self, request):
        """
        Allow all users which are in 'users' group.
        """
        return request.user.is_active \
            and request.user.groups.filter(name='users').count()


admin = SuperAdminSite(name='adminpanel')
staff = AdminSite(name='staffpanel')
user = UserSite(name='userpanel')


# admin
admin.register(Site, SiteAdmin)
admin.register(User, UserAdmin)
admin.register(Group, GroupAdmin)

#admin.register(Website, WebsiteAdmin)
admin.register(Core, CoreAdmin)
admin.register(Schedule, ScheduleAdmin)
admin.register(Content, ContentAdmin)
admin.register(ContentDescriptor, ContentDescriptorAdmin)
admin.register(Filter, FilterAdmin)

admin.register(Mailbox, MailboxAdmin)
admin.register(Message, MessageAdmin)
admin.register(MessageAttachment, MessageAttachmentAdmin)

#admin.register(Dropbox, DropboxAdmin)
admin.register(Ranking, RankingAdmin)

admin.register(Directory, DirectoryAdmin)

admin.register([Config], ConstanceAdmin)

# staff
#staff.register(Website, WebsiteAdmin)

# user
#user.register(Website, WebsiteAdmin)