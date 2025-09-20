from django.urls import path, include



# قاعدة URL الأساسية للتطبيق: /api/
urlpatterns = [
    # نظام المصادقة (تسجيل دخول/تسجيل/ملف شخصي)
    path('user/', include('myappG.urls.account')), 
    
    # إدارة المستفيدين
    path('beneficiaries/', include('myappG.urls.beneficiaries')),
    
    # المساعدات الطبية
    path('medical-aids/', include('myappG.urls.medical_aids')),
    
    # المساعدات العينية
    path('material-aids/', include('myappG.urls.material_aids')),
    
    # إدارة المشاريع
    path('projects/', include('myappG.urls.projects')),
    
    # التقييمات
    path('feedback/', include('myappG.urls.feedback')),
    
    path('activities/', include('myappG.urls.activitiy')), 

    path('news/', include('myappG.urls.news')),

    path('', include('myappG.urls.home')),

]

# يمكنك إضافة مسارات إضافية هنا إذا لزم الأمر