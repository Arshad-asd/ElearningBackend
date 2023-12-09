from django.contrib import admin
from django.utils.html import format_html
from .models import Category, LiveClass, SubCategory, Course, Lesson, Plan, Feature, Subscription



# Course manage
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('id', 'category_name', 'subscribed_count', 'display_image', 'is_active', 'subcategories_list')
    search_fields = ('category_name',)

    def display_image(self, obj):
        return format_html('<img src="{}" style="max-height: 50px; max-width: 50px;" />', obj.image.url)

    display_image.short_description = 'Image'

    def subcategories_list(self, obj):
        subcategories = SubCategory.objects.filter(category_ref=obj)
        return ', '.join([sub.sub_category_name for sub in subcategories])

    subcategories_list.short_description = 'Subcategories'
admin.site.register(Category, CategoryAdmin)



class SubCategoryAdmin(admin.ModelAdmin):
    list_display = ('id', 'sub_category_name', 'category_name', )
    search_fields = ('sub_category_name', 'category_ref__category_name')

    def category_name(self, obj):
        return obj.category_ref.category_name

    category_name.short_description = 'Category Name'

admin.site.register(SubCategory, SubCategoryAdmin)
class CourseAdmin(admin.ModelAdmin):
    list_display = ('id', 'course_name', 'category_ref', 'sub_category_ref', 'tutor_ref', 'views', 'likes', 'is_active')
    list_filter = ('category_ref', 'sub_category_ref', 'tutor_ref', 'is_active')
    search_fields = ('course_name', 'category_ref__category_name', 'sub_category_ref__sub_category_name', 'tutor_ref__username')
    list_per_page = 20

admin.site.register(Course, CourseAdmin)
admin.site.register(Lesson)

# Plans manage
class PlanAdmin(admin.ModelAdmin):
    list_display = ('type', 'amount', 'is_active', 'get_features_display')
    list_filter = ('type', 'is_active')
    search_fields = ('type',)

    def get_features_display(self, obj):
        # Concatenate feature texts for display
        features = obj.features.all()
        return ', '.join([feature.feature_text for feature in features])

    get_features_display.short_description = 'Features'

admin.site.register(Plan, PlanAdmin)
@admin.register(Feature)
class FeatureAdmin(admin.ModelAdmin):
    list_display = ('feature_text', 'get_plan_type', 'get_plan_amount', 'get_plan_status')

    def get_plan_type(self, obj):
        # Display the plan type for the related plan
        return obj.entry.type

    def get_plan_amount(self, obj):
        # Display the plan amount for the related plan
        return obj.entry.amount

    def get_plan_status(self, obj):
        # Display the plan status for the related plan
        return obj.entry.is_active

    get_plan_type.short_description = 'Plan Type'
    get_plan_amount.short_description = 'Plan Amount'
    get_plan_status.short_description = 'Plan Status'
# Subscriptions manage

admin.site.register(LiveClass)