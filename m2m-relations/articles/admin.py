from django.contrib import admin
from django.forms import BaseInlineFormSet
from .models import Article, Section, Scope

class ScopeInlineFormset(BaseInlineFormSet):
    def clean(self):
        super().clean()
        main_section_count = 0
        for form in self.forms:
            if not form.cleaned_data.get('DELETE', False):
                section = form.cleaned_data.get('section')
                if section and section.is_main:  # предполагается, что есть поле is_main
                    main_section_count += 1
        if main_section_count != 1:
            raise ValidationError('Должен быть выбран ровно один основной раздел.')

class ScopeInline(admin.TabularInline):
    model = Scope
    formset = ScopeInlineFormset

@admin.register(Article)
class ArticleAdmin(admin.ModelAdmin):
    inlines = [ScopeInline]