from django.db import models
from django.contrib.auth.models import AbstractUser
from django.core.validators import FileExtensionValidator
from django.core.validators import MaxValueValidator
import os
from django.core.exceptions import ValidationError

class PendingUser(models.Model):
    GENDER_CHOICES = (
        ('male', 'ذكر'),
        ('female', 'أنثى'),
    )
    email=models.EmailField()
    phone=models.CharField(max_length=15)
    first_name=models.CharField(max_length=50)
    last_name=models.CharField(max_length=50)
    password=models.CharField(max_length=128)
    address=models.TextField(null=True)
    gender = models.CharField(max_length=10, choices=GENDER_CHOICES, verbose_name="الجنس")
    birth_date=models.DateField(null=True)
    profile_picture = models.ImageField(
        upload_to='profile_pictures/',
        null=True,
        blank=True,
        verbose_name="صورة الملف الشخصي"
    )
    otp=models.CharField(max_length=4)
    create_at=models.DateTimeField(auto_now_add=True)
    otp_created=models.DateTimeField(auto_now_add=True)

class CustomUser(AbstractUser):
    USER_TYPE_CHOICES = (
        ('admin', 'مسؤول الجمعية'),
        ('staff', 'موظف الجمعية'),
        ('field_team', 'فريق الميدان'),
        ('beneficiary', 'مستفيد'),

    )

    GENDER_CHOICES = (
        ('male', 'ذكر'),
        ('female', 'أنثى'),
    )
    first_name=models.CharField(max_length=50)
    email=models.EmailField("بريد الكتروني",unique=True,null=False,blank=False)
    last_name=models.CharField(max_length=50)
    birth_date=models.DateField("تاريخ الميلاد",null=True)
    user_type = models.CharField(max_length=20, choices=USER_TYPE_CHOICES,default='Beneficiary' ,verbose_name="نوع المستخدم")
    phone = models.CharField(max_length=20, verbose_name="رقم الهاتف")
    gender = models.CharField(max_length=10, choices=GENDER_CHOICES, verbose_name="الجنس")
    address=models.TextField(null=True)
    verification_token=models.CharField("رمز التحقق",max_length=6,blank=True,null=True)
    otp_created=models.DateTimeField(null=True,blank=True)

    profile_picture = models.ImageField(
        upload_to='profile_pictures/',
        null=True,
        blank=True,
        verbose_name="صورة الملف الشخصي"
    )
    username = models.CharField(max_length=150, unique=True)
    is_verified = models.BooleanField(default=False, verbose_name="حساب موثق")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="تاريخ الإنشاء")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="تاريخ التحديث")
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username', 'first_name', 'last_name']

    class Meta:
        verbose_name = "مستخدم"
        verbose_name_plural = "المستخدمون"

    def __str__(self):
        return f"{self.first_name}{self.last_name or ''}".strip()

class Beneficiary(models.Model):
    RESIDENCE_TYPE_CHOICES = [
    ('hosted', 'مستضاف'),
    ('returnee', 'عائد'),
    ('refugee', 'لاجئ'),
    ('idp', 'نازح داخلي'),
    ('affected_community', 'أفراد مجتمع متضرر'),
    ('other', 'غير ذلك'),
]

    LIVING_STATUS_CHOICES = [
    ('owned', 'ملك'),
    ('rented', 'استئجار'),
    ('hosted', 'استضافة'),
    ('shelter_center', 'مركز إيواء اجتماعي'),
    ('camp', 'مخيم'),
    ('other', 'غير ذلك'),
]

    MARITAL_STATUS_CHOICES = [
    ('single', 'أعزب'),
    ('married', 'متزوج'),
    ('divorced', 'مطلق'),
    ('widowed', 'أرمل'),
    ('husband_missing', 'الزوج مفقود'),
    ]

    WEAKNESS_CHOICES = [
    ('none', 'سليم'),
    ('disabled', 'ذو أعاقة'),
    ('chronic_illness', 'مرض مزمن'),
]

    user = models.OneToOneField(
        CustomUser,
        on_delete=models.CASCADE,
        related_name='beneficiary',
        verbose_name="المستخدم"
    )
    GENDER_CHOICES = (
        ('male', 'ذكر'),
        ('female', 'أنثى'),
    )
    full_name = models.CharField(max_length=200, verbose_name="الاسم الثلاثي")
    gender = models.CharField(max_length=10, choices=GENDER_CHOICES, verbose_name="الجنس")
    birth_date = models.DateField(verbose_name="تاريخ الميلاد")
    email = models.EmailField(verbose_name="البريد الإلكتروني", blank=True, null=True)
    phone_number = models.CharField(max_length=20 , verbose_name="رقم الهاتف")
    residence_type = models.CharField(
        max_length=50,
        choices=RESIDENCE_TYPE_CHOICES,
        verbose_name="الخلفية الشخصية"
    )
    current_address = models.TextField(verbose_name="العنوان الحالي")
    previous_address = models.TextField(verbose_name="العنوان السابق", blank=True, null=True)
    living_status = models.CharField(
        max_length=50,
        choices=LIVING_STATUS_CHOICES,
        verbose_name="طبيعة الإقامة"
    )
    marital_status = models.CharField(
        max_length=50,
        choices=MARITAL_STATUS_CHOICES,
        verbose_name="الحالة الاجتماعية"
    )

    family_members = models.PositiveIntegerField(
        verbose_name="عدد أفراد الأسرة",
        validators=[MaxValueValidator(20)]
        )
    education = models.CharField(max_length=100, verbose_name="التحصيل العلمي")
    job = models.CharField(max_length=100, verbose_name="العمل الحالي", blank=True, null=True)
    weaknesses_disabilities = models.TextField(verbose_name="نقاط الضعف / الإعاقة")
    notes = models.TextField(verbose_name="ملاحظات إضافية", blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="تاريخ الإنشاء")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="تاريخ التحديث")

    class Meta:
        verbose_name = "مستفيد"
        verbose_name_plural = "المستفيدون"
        ordering = ['-created_at']

    def __str__(self):
        return self.full_name

class MedicalAidRequest(models.Model):
    AID_TYPE_CHOICES = [
        ('nebulizer', 'جهاز رذاذ'),
        ('diabetes_device', 'جهاز سكري'),
        ('pressure_device', 'جهاز ضغط'),
        ('walker', 'جهاز مشي'),
        ('wheelchair', 'كرسي متحرك'),
        ('medical_mattress', 'إسفنجة طبية'),
    ]

    STATUS_CHOICES = [
        ('pending', 'قيد المراجعة'),
        ('approved', 'موافق عليه'),
        ('delivered', 'تم التسليم'),
    ]

    beneficiary = models.OneToOneField(
        Beneficiary,
        on_delete=models.CASCADE,
        related_name='medical_aids',
        verbose_name="المستفيد"
    )
    aid_type = models.CharField(
        max_length=50,
        choices=AID_TYPE_CHOICES,
        verbose_name="نوع المساعدة الطبية"
    )
    status = models.CharField(
        max_length=50,
        choices=STATUS_CHOICES,
        default='pending',
        verbose_name="حالة الطلب"
    )
    def validate_medical_report_file(value):
        ext = os.path.splitext(value.name)[1].lower()
        allowed_extensions = ['.jpg', '.jpeg', '.png', '.pdf']
        if ext not in allowed_extensions:
            raise ValidationError("الملف يجب أن يكون بصيغة صورة أو PDF فقط.")

    request_date = models.DateField(auto_now_add=True, verbose_name="تاريخ الطلب")
    review_date = models.DateField(null=True, blank=True, verbose_name="تاريخ المراجعة")
    delivery_date = models.CharField(max_length=30 , null=True, blank=True, verbose_name="تاريخ التسليم")
    notes = models.TextField(verbose_name="ملاحظات", blank=True, null=True)
    medical_report = models.FileField(
    upload_to='medical_reports/',
    verbose_name="صورة أو ملف التقرير الطبي",
    validators=[validate_medical_report_file]

)

    reviewer = models.ForeignKey(
        CustomUser,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='reviewed_medical_aids',
        verbose_name="المسؤول عن المراجعة"
    )

    class Meta:
        verbose_name = "طلب مساعدة طبية"
        verbose_name_plural = "طلبات المساعدات الطبية"
        ordering = ['-request_date']

    def __str__(self):
        return f"{self.beneficiary} - {self.get_aid_type_display()}"

class MaterialAidRequest(models.Model):
    AID_TYPE_CHOICES = [
        ('washing_machine', 'غسالة'),
        ('fridge', 'براد'),
        ('oven', 'فرن'),
        ('laser heater', 'سخانة ليزرية'),
        ('battery', 'بطارية'),
        ('water_tank', 'خزان'),
        ('heater', 'مدفئة'),
        ('carpet', 'سجادة'),
    ]

    beneficiary = models.OneToOneField(
        Beneficiary,
        on_delete=models.CASCADE,
        related_name='material_aids',
        verbose_name="المستفيد"
    )
    aid_type = models.CharField(
        max_length=50,
        choices=AID_TYPE_CHOICES,
        verbose_name="نوع المساعدة العينية"
    )
    status = models.CharField(
        max_length=50,
        choices=MedicalAidRequest.STATUS_CHOICES,
        default='pending',
        verbose_name="حالة الطلب"
    )
    request_date = models.DateField(auto_now_add=True, verbose_name="تاريخ الطلب")
    review_date = models.DateField(null=True, blank=True, verbose_name="تاريخ المراجعة")
    delivery_date = models.CharField(max_length=30 , null=True, blank=True, verbose_name="تاريخ التسليم")
    notes = models.TextField(verbose_name="ملاحظات", blank=True, null=True)
    reviewer = models.ForeignKey(
        CustomUser,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='reviewed_material_aids',
        verbose_name="المسؤول عن المراجعة"
    )

    class Meta:
        verbose_name = "طلب مساعدة عينية"
        verbose_name_plural = "طلبات المساعدات العينية"
        ordering = ['-request_date']

    def __str__(self):
        return f"{self.beneficiary} - {self.get_aid_type_display()}"

class ProjectRequest(models.Model):
    PROJECT_TYPE_CHOICES = [
        ('commercial', 'مشروع تجاري'),
        ('agricultural', 'مشروع زراعي'),
    ]

    beneficiary = models.OneToOneField(
        Beneficiary,
        on_delete=models.CASCADE,
        related_name='projects',
        verbose_name="المستفيد"
    )
    project_type = models.CharField(
        max_length=50,
        choices=PROJECT_TYPE_CHOICES,
        verbose_name="نوع المشروع"
    )
    reviewer = models.ForeignKey(
        CustomUser,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='reviewed_project_request',
        verbose_name="المسؤول عن المراجعة"
    )
    ownership = models.CharField(
        max_length=100,
        verbose_name="الملكية"
    )
    area = models.CharField(
        max_length=100,
        verbose_name="المساحة"
    )
    experience = models.TextField(
        verbose_name="الخبرة"
    )
    tools = models.TextField(
        verbose_name="الأدوات المتوفرة"
    )
    notes = models.TextField(
        blank=True,
        null=True,
        verbose_name="ملاحظات إضافية"
    )
    STATUS_CHOICES = [
        ('pending', 'قيد المراجعة'),
        ('approved', 'موافق عليه'),
        ('rejected', 'مرفوض'),
    ]

    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default='pending',
        verbose_name='حالة الطلب'
    )
    delivery_date = models.CharField(max_length=30 , null=True, blank=True, verbose_name="تاريخ التسليم")
    review_date = models.DateField(null=True, blank=True, verbose_name="تاريخ المراجعة")
    request_date = models.DateField(auto_now_add=True, verbose_name="تاريخ الطلب")

    class Meta:
        verbose_name = "طلب مشروع"
        verbose_name_plural = "طلبات المشاريع"
        ordering = ['-request_date']

    def __str__(self):
        return f"{self.beneficiary.full_name} - {self.get_project_type_display()}"


# class Evaluation(models.Model):
#     beneficiary = models.ForeignKey(
#         Beneficiary,
#         on_delete=models.CASCADE,
#         related_name='evaluations',
#         verbose_name="المستفيد"
#     )
#     evaluator = models.ForeignKey(
#         CustomUser,
#         on_delete=models.SET_NULL,
#         null=True,
#         verbose_name="المقيّم"
#     )
#     evaluation_date = models.DateField(auto_now_add=True, verbose_name="تاريخ التقييم")
#     needs_level = models.PositiveIntegerField(
#         choices=[(1, 'منخفض'), (2, 'متوسط'), (3, 'عالي')],
#         verbose_name="مستوى الحاجة"
#     )
#     vulnerability_score = models.PositiveIntegerField(
#         verbose_name="درجة الضعف",
#         help_text="من 1 إلى 10"
#     )
#     notes = models.TextField(verbose_name="ملاحظات التقييم")
#     recommendations = models.TextField(verbose_name="التوصيات", blank=True, null=True)
#     is_approved = models.BooleanField(default=False, verbose_name="موافق عليه")

#     class Meta:
#         verbose_name = "تقييم"
#         verbose_name_plural = "التقييمات"

#     def __str__(self):
#         return f"تقييم {self.beneficiary} - {self.evaluation_date}"


from django.db import models

class Activity(models.Model):
    photo = models.ImageField(
        upload_to='activities/photos/',
        verbose_name="صورة النشاط",
        null= True , blank= True
    )
    description = models.TextField(verbose_name="وصف النشاط")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="تاريخ الإنشاء")
    date = models.DateField(verbose_name="تاريخ النشاط")

    class Meta:
        verbose_name = "نشاط"
        verbose_name_plural = "الأنشطة"
        ordering = ['-created_at']

    def __str__(self):
        return f"نشاط رقم {self.id}"

class News(models.Model):
    photo = models.ImageField(upload_to='news/photos/', verbose_name="صورة الخبر" , null= True , blank= True)
    description = models.TextField(verbose_name="تفاصيل الخبر")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="تاريخ الإنشاء")
    date = models.DateField(verbose_name="تاريخ الخبر")

    class Meta:
        verbose_name = "خبر"
        verbose_name_plural = "الأخبار"
        ordering = ['-created_at']

    def __str__(self):
        return f"خبر رقم {self.id}"

class Feedback(models.Model):
    user=models.OneToOneField(CustomUser,on_delete=models.CASCADE,related_name='feedback')
    rating=models.IntegerField()
    is_satisfied=models.BooleanField()
    will_use_again=models.BooleanField()
    notes=models.TextField(blank=True,null=True)
    created_at=models.DateTimeField(auto_now_add=True)
    def __str__(self):
        return f"Feedback by{self.user.email}"
