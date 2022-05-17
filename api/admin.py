import json
from django.contrib import admin
from django.core.serializers.json import DjangoJSONEncoder
from django.db.models import Count
from django.db.models.functions import TruncDay
from api.models import Profile, Hobby, Job, Favourite, EmailSubscriber
from django.utils.html import format_html
from django import forms
from import_export.admin import ImportExportMixin
from django.contrib import messages
from django.utils.translation import ngettext


class ProfileAdminForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = "__all__"

    def clean_name(self):
        if self.cleaned_data['name'] != 'Spike' or 'Mercy' or 'Dracula':
            return self.cleaned_data['name']
        raise forms.ValidationError('No Vampires names')


class FavouriteAdminInline(admin.StackedInline):
    model = Favourite
    extra = 1
    autocomplete_fields = ('profile', 'hobby', 'job')
    # raw_id_fields = ('profile', 'hobby', 'job')

class FavouriteTabularInline(admin.TabularInline):
    model = Favourite
    fk_name = 'profile'
    extra = 1
    autocomplete_fields = ('profile', 'hobby', 'job')
    # raw_id_fields = ('profile', 'hobby', 'job')


class EmailSubscriberAdmin(admin.ModelAdmin):
    list_display = ("id", "email", "created_at")   #display these table columns in the list view
    ordering = ("-created_at",)

    def changelist_view(self, request, extra_context=None):
        # Aggregate new subscribers per day
        chart_data = (
            EmailSubscriber.objects.annotate(date=TruncDay("created_at"))
                .values("date")
                .annotate(y=Count("id"))
                .order_by("-date")
        )
        as_json = json.dumps(list(chart_data), cls=DjangoJSONEncoder)
        extra_context = extra_context or {"chart_data": as_json}

        # Call the superclass changelist_view to render the page
        return super().changelist_view(request, extra_context=extra_context)

class ProfileAdmin(admin.ModelAdmin):
    inlines = [FavouriteAdminInline, FavouriteTabularInline]   #add model in a model
    form = ProfileAdminForm         #form validation
    list_display = ['name', 'Email', "mobile_number", 'Status', "choices", 'created_at']
    list_editable = ('mobile_number',)
    ordering = ('name',)
    # list_filter = ['name', ('detail', admin.EmptyFieldListFilter)]
    # readonly_fields = ['created_at', 'updated_at', "image_preview"]
    radio_fields = {'tag': admin.HORIZONTAL}
    # save_on_top = True                                          #save button to make it on top
    search_fields = ['name', 'status']  #search_fields = ['foreign_key__related_fieldname'] we can use like this as well
    search_help_text = ['name', 'status']
    actions = ['Make_True', 'Make_False']     #actions function calls
    date_hierarchy = 'updated_at'
    list_per_page = 3  #how many items will in a single page
    save_as = True  #it will add button named saved as new


    def Make_True(self, request, queryset):  #add action to make status true
        updated = queryset.update(status=True)
        self.message_user(request, ngettext(
            '%d Status successfully marks as True.',
            '%d Statuses successfully marks as True.', updated) %
             updated, messages.SUCCESS)

    def Make_False(self, request, queryset):    #add action to make status false
        queryset.update(status=False)

    def show_details(self, obj):            #BUtton for profile model instance to go in detail
        return format_html(f'<a href="/admin/api/profile/{obj.id}/change/" class="default">Click me</a>')

    def Email(self, obj):     ##To change the email of color  #email is a field of profile model
        return format_html(f'<span style="color:green">{obj.email}</span')

    def Status(self, obj):                                  #To change the status of color     #status is a field of profile model
        return format_html(f'<span style="color:red">{obj.status}</span')

    # def image_preview(self, obj):                     #This function is use for image preview in admin panel of profile model
    #     return format_html(f'<img src="/media/{obj.image}" style= height:50px; width:50px>')

    def has_delete_permission(self, request, obj=None):    #Remove delete in actions
        return False

    def has_add_permission(self, request):  #remove add instance in admin panel for profile we can't add until return True
        return True

    # image_preview.allow_tags = True


class HobbyAdmin(ImportExportMixin, admin.ModelAdmin):
    fields = ['user', 'name']
    list_display = ['id', 'user', 'name', 'created_at', 'updated_at', 'show_detail']
    list_filter = ('name',)
    search_fields = ['user__name']

    autocomplete_fields = ['user']  #JUST only accept foreign models fields


    def show_detail(self, obj):
        return format_html(f'<a href="/admin/api/hobby/{obj.id}/change/" class="default">Click me</a>')


class JobAdmin(ImportExportMixin, admin.ModelAdmin):
    list_display = ['id', 'user', 'name', 'created_at', 'updated_at', 'show_detail']
    list_filter = ['name']
    search_fields = ['user']

    def show_detail(self, obj):
        return format_html(f'<a href="/admin/api/job/{obj.id}/change/" class="default">Click me</a>')


class FavouriteAdmin(ImportExportMixin, admin.ModelAdmin):
    list_display = ['profile', 'hobby', 'job', 'name', 'created_at', 'updated_at']
    fields = ['name', ('profile', 'hobby', 'job')]  #To show in horizontal form and group them in tuple
    search_fields = ['profile', 'hobby', 'job']
    # fieldsets = (                                     #Either use fields or fieldseSets, can't use both at a time
    #     (None, {
    #         "fields": ('profile', 'hobby', 'job')
    #     }),
    #     ("Availability", {
    #         "fields": ('name',)
    #     })
    # )


admin.site.register(Profile, ProfileAdmin)
admin.site.register(Hobby, HobbyAdmin)
admin.site.register(Job, JobAdmin)
admin.site.register(Favourite, FavouriteAdmin)
admin.site.register(EmailSubscriber, EmailSubscriberAdmin)

