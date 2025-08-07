from modeltranslation.translator import register, TranslationOptions
from accounts.models import Account, UserProfile


@register(Account)
class AccountTranslationOptions(TranslationOptions):
    fields = ('first_name', 'last_name')

@register(UserProfile)
class UserProfileTranslationOptions(TranslationOptions):
    fields = ('address_line_1', 'address_line_2', 'city', 'state', 'country')
