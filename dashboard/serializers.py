from rest_framework import serializers
from myappG.models import MedicalAidRequest , MaterialAidRequest , ProjectRequest
from myappG.serializers import BeneficiarySerializer

from rest_framework import serializers
from myappG.models import Beneficiary
from rest_framework import serializers
from django.contrib.auth import get_user_model
import random
import string
from myappG.utils import send_otp_email
from django.utils import timezone
from datetime import timedelta
from django.contrib.auth.password_validation import validate_password
from django.conf import settings
from rest_framework_simplejwt.tokens import RefreshToken,TokenError



User = get_user_model()

class DashboardBeneficiarySerializer(serializers.ModelSerializer):
    class Meta:
        model = Beneficiary
        fields = ['full_name', 'phone_number', 'gender', 'current_address']


class MedicalAidDashboardSerializer(serializers.ModelSerializer):
    beneficiary = DashboardBeneficiarySerializer(read_only=True)
    aid_type_display = serializers.CharField(source='get_aid_type_display', read_only=True)
    status_display = serializers.CharField(source='get_status_display', read_only=True)
    reviewer = serializers.SerializerMethodField()
    category = serializers.SerializerMethodField()



    class Meta:
        model = MedicalAidRequest
        fields = ['id','beneficiary', 'aid_type_display', 'status_display', 'request_date','reviewer','category']


    def get_reviewer(self, obj):
        if obj.reviewer:
            return f"{obj.reviewer.first_name} {obj.reviewer.last_name}"
        return ""

    def get_category(self, obj):
        return "مساعدة طبية"



class MedicalAidDashboardDetailSerializer(serializers.ModelSerializer):
    beneficiary = BeneficiarySerializer (read_only=True)
    aid_type_display = serializers.CharField(source='get_aid_type_display', read_only=True)
    status_display = serializers.CharField(source='get_status_display', read_only=True)
    reviewer = serializers.SerializerMethodField()
    delivery_date = serializers.SerializerMethodField()
    review_date = serializers.SerializerMethodField()
    medical_report = serializers.SerializerMethodField()
    # delivery_date = serializers.CharField()  # Force DRF to treat it as plain string

    class Meta:
        model = MedicalAidRequest
        fields = '__all__'

    def get_reviewer(self, obj):
        if obj.reviewer:
            return f"{obj.reviewer.first_name} {obj.reviewer.last_name}"
        return ""
    def get_delivery_date(self, obj):
        if obj.delivery_date:
            return obj.delivery_date
        return ""

    def get_review_date(self, obj):
        if obj.review_date:
            return obj.review_date
        return ""

    def get_medical_report(self, obj):
        if obj.medical_report:
            filename = obj.medical_report.name  # includes subfolder if any
            return f"{settings.DOMAIN}/api/media/{filename}"
        return ""



class MedicalAidUpdateResponseSerializer(serializers.Serializer):
    status = serializers.CharField()
    delivery_date = serializers.CharField(allow_blank=True, required=False)
    review_date = serializers.DateTimeField()
    reviewer = serializers.SerializerMethodField()

    def get_reviewer(self, obj):
        user = obj.reviewer
        if user:
            return f"{user.first_name} {user.last_name}"
        return ""
    def get_delivery_date(self, obj):
        if obj.delivery_date:
            return obj.delivery_date
        return ""

    def get_review_date(self, obj):
        if obj.review_date:
            return obj.review_date
        return ""

class DashboardUserListSerializer(serializers.ModelSerializer):
    profile_picture = serializers.SerializerMethodField()

    class Meta:
        model = User
        fields = ['id', 'first_name', 'last_name', 'email', 'user_type', 'gender', 'profile_picture']

    def get_profile_picture(self, obj):
        if obj.profile_picture:
            filename = obj.profile_picture.name  # includes subfolder if any
            return f"{settings.DOMAIN}/api/media/{filename}"
        return ""



from rest_framework import serializers
from django.contrib.auth import get_user_model
from rest_framework_simplejwt.tokens import RefreshToken

CustomUser = get_user_model()


from rest_framework import serializers
from django.contrib.auth import get_user_model
from rest_framework_simplejwt.tokens import RefreshToken

CustomUser = get_user_model()

from rest_framework import serializers
from django.contrib.auth import get_user_model
from rest_framework_simplejwt.tokens import RefreshToken

CustomUser = get_user_model()

class EmailLoginSerializer(serializers.Serializer):
    email = serializers.EmailField()
    password = serializers.CharField(write_only=True)

    first_name = serializers.CharField(read_only=True)
    last_name = serializers.CharField(read_only=True)
    user_type = serializers.CharField(read_only=True)
    profile_picture = serializers.SerializerMethodField()
    access = serializers.CharField(read_only=True)
    refresh = serializers.CharField(read_only=True)

    def get_profile_picture(self, obj):
        if obj.profile_picture and hasattr(obj.profile_picture, 'name'):
            filename = obj.profile_picture.name
            return f"{settings.DOMAIN}/api/media/{filename}"
        return ""

    def validate(self, data):
        email = data.get('email')
        password = data.get('password')

        try:
            user = CustomUser.objects.get(email=email)
        except CustomUser.DoesNotExist:
            raise serializers.ValidationError("لا يوجد مستخدم بهذا البريد الإلكتروني.")

        if not user.check_password(password):
            raise serializers.ValidationError("كلمة المرور غير صحيحة.")

        if not user.is_verified:
            raise serializers.ValidationError("لم يتم تأكيد حسابك بعد.")

        if user.user_type not in ['admin', 'staff']:
            raise serializers.ValidationError("هذا الحساب غير مصرح له بتسجيل الدخول من هنا.")

        refresh = RefreshToken.for_user(user)

        # Dynamically attach authenticated user to serializer instance for read-only fields
        self.instance = user

        return {
            "first_name": user.first_name,
            "last_name": user.last_name,
            "user_type": user.user_type,
            "profile_picture": self.get_profile_picture(user),
            "access": str(refresh.access_token),
            "refresh": str(refresh)
        }
from rest_framework import serializers
from django.conf import settings
import random, string

class UserCreateSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, required=False)
    profile_picture = serializers.ImageField(required=False)

    class Meta:
        model = User
        fields = [
            'first_name', 'last_name', 'email', 'user_type',
            'gender', 'profile_picture', 'password' , 'id'
        ]

    def generate_unique_username(self, length=8):
        while True:
            username = ''.join(random.choices(string.ascii_lowercase + string.digits, k=length))
            if not User.objects.filter(username=username).exists():
                return username

    def create(self, validated_data):
        password = validated_data.pop('password', None)
        username = self.generate_unique_username()
        user_type = validated_data.get('user_type', 'beneficiary')

        user = User(
            username=username,
            is_verified=user_type in ['admin', 'staff'],
            is_staff=user_type in ['admin', 'staff'],
            is_superuser=user_type == 'admin',
            **validated_data
        )
        if password:
            user.set_password(password)
        else:
            user.set_unusable_password()

        user.save()
        return user

    def get_profile_picture_url(self, obj):
        if obj.profile_picture and hasattr(obj.profile_picture, 'name'):
            filename = obj.profile_picture.name
            return f"{settings.DOMAIN}/api/media/{filename}"
        return ""

    def to_representation(self, instance):
        data = super().to_representation(instance)
        data['profile_picture'] = self.get_profile_picture_url(instance)
        return data


class DashboardForgotPasswordSerializer(serializers.Serializer):
    email = serializers.EmailField()

    def validate_email(self, value):
        try:
            user = User.objects.get(email=value)

            # Update is_verified for trusted superusers
            if user.is_superuser and not user.is_verified:
                user.is_verified = True
                user.save()

            # Check dashboard access
            if user.user_type not in ['admin', 'staff']:
                raise serializers.ValidationError("ليس لديك صلاحية بالوصول للوحة التحكم")

        except User.DoesNotExist:
            raise serializers.ValidationError("البريد الإلكتروني غير موجود")

        return value

    def save(self):
        user = User.objects.get(email=self.validated_data["email"])
        otp = ''.join(random.choices("0123456789", k=4))
        user.verification_token = otp
        user.otp_created = timezone.now()
        user.save()
        send_otp_email(user.email, otp)


class DashboardConfirmOTPSerializer(serializers.Serializer):
    email = serializers.EmailField()
    otp = serializers.CharField(max_length=4)

    def validate(self, data):
        try:
            user = User.objects.get(
                email=data["email"],
                verification_token=data["otp"]
            )
        except User.DoesNotExist:
            raise serializers.ValidationError("رمز التحقق غير صحيح")

        # Check dashboard role
        if user.user_type not in ['admin', 'staff']:
            raise serializers.ValidationError("ليس لديك صلاحية بالوصول للوحة التحكم")

        # Expiry check (10 mins)
        if not user.otp_created or timezone.now() > user.otp_created + timedelta(minutes=10):
            raise serializers.ValidationError("انتهت صلاحية رمز التحقق")

        self.user = user
        return data

class DashboardResetPasswordSerializer(serializers.Serializer):
    email = serializers.EmailField()
    otp = serializers.CharField(max_length=4)
    new_password = serializers.CharField(write_only=True)
    confirm_password = serializers.CharField(write_only=True)

    def validate(self, data):
        if data["new_password"] != data["confirm_password"]:
            raise serializers.ValidationError("كلمتا السر غير متطابقتين")

        try:
            validate_password(data["new_password"])
        except Exception as e:
            raise serializers.ValidationError(str(e))

        # Check user existence and dashboard role
        try:
            user = User.objects.get(
                email=data["email"],
                verification_token=data["otp"]
            )
            if user.user_type not in ['admin', 'staff']:
                raise serializers.ValidationError("ليس لديك صلاحية بالوصول للوحة التحكم")

        except User.DoesNotExist:
            raise serializers.ValidationError("المستخدم غير موجود أو الرمز غير صحيح")

        return data

    def save(self):
        user = User.objects.get(
            email=self.validated_data["email"],
            verification_token=self.validated_data["otp"]
        )
        user.set_password(self.validated_data["new_password"])
        user.verification_token = None
        user.otp_created = None
        user.save()

class LogoutSerializer(serializers.Serializer):
    refresh = serializers.CharField()

    def validate(self, attrs):
        self.token = attrs["refresh"]

        # Optionally check user type from request context
        user = self.context['request'].user
        if not user.is_authenticated or user.user_type not in ['admin', 'staff']:
            raise serializers.ValidationError("ليس لديك صلاحية بالخروج من لوحة التحكم")

        return attrs

    def save(self, **kwargs):
        try:
            token = RefreshToken(self.token)
            token.blacklist()
        except TokenError:
            raise serializers.ValidationError("رمز غير صالح أو منتهي")


class MaterialAidDashboardDetailSerializer(serializers.ModelSerializer):
    beneficiary = BeneficiarySerializer(read_only=True)
    aid_type_display = serializers.CharField(source='get_aid_type_display', read_only=True)
    status_display = serializers.CharField(source='get_status_display', read_only=True)
    reviewer = serializers.SerializerMethodField()
    # delivery_date = serializers.CharField()
    delivery_date = serializers.SerializerMethodField()
    review_date = serializers.SerializerMethodField()


    class Meta:
        model = MaterialAidRequest
        fields = '__all__'

    def get_reviewer(self, obj):
        if obj.reviewer:
            return f"{obj.reviewer.first_name} {obj.reviewer.last_name}"
        return ""

    def get_delivery_date(self, obj):
        if obj.delivery_date:
            return obj.delivery_date
        return ""

    def get_review_date(self, obj):
        if obj.review_date:
            return obj.review_date
        return ""

class MaterialAidDashboardSerializer(serializers.ModelSerializer):
    beneficiary = DashboardBeneficiarySerializer(read_only=True)
    aid_type_display = serializers.CharField(source='get_aid_type_display', read_only=True)
    status_display = serializers.CharField(source='get_status_display', read_only=True)
    reviewer = serializers.SerializerMethodField()
    category = serializers.SerializerMethodField()


    class Meta:
        model = MaterialAidRequest
        fields = ['id', 'beneficiary', 'aid_type_display', 'status_display', 'request_date', 'reviewer',
                  'category']

    def get_reviewer(self, obj):
        if obj.reviewer:
            return f"{obj.reviewer.first_name} {obj.reviewer.last_name}"
        return ""
    def get_category(self, obj):
        return "مساعدة مادية"


class MaterialAidUpdateResponseSerializer(serializers.Serializer):
    status = serializers.CharField()
    delivery_date = serializers.CharField(allow_blank=True, required=False)
    review_date = serializers.DateTimeField()
    reviewer = serializers.SerializerMethodField()

    def get_reviewer(self, obj):
        user = obj.reviewer
        if user:
            return f"{user.first_name} {user.last_name}"
        return ""

class ProjectRequestDashboardSerializer(serializers.ModelSerializer):
    beneficiary = DashboardBeneficiarySerializer(read_only=True)
    aid_type_display = serializers.CharField(source='get_project_type_display', read_only=True)
    status_display = serializers.CharField(source='get_status_display', read_only=True)
    reviewer = serializers.SerializerMethodField()
    category = serializers.SerializerMethodField()

    class Meta:
        model = ProjectRequest
        fields = ['id', 'beneficiary', 'aid_type_display', 'status_display', 'request_date', 'reviewer','category']

    def get_reviewer(self, obj):
        if obj.reviewer:
            return f"{obj.reviewer.first_name} {obj.reviewer.last_name}"
        return ""
    def get_category(self, obj):
        return "مشروع"


class ProjectRequestDashboardDetailSerializer(serializers.ModelSerializer):
    beneficiary = BeneficiarySerializer(read_only=True)
    project_type_display = serializers.CharField(source='get_project_type_display', read_only=True)
    status_display = serializers.CharField(source='get_status_display', read_only=True)
    reviewer = serializers.SerializerMethodField()

    class Meta:
        model = ProjectRequest
        fields = '__all__'

    def get_reviewer(self, obj):
        if obj.reviewer:
            return f"{obj.reviewer.first_name} {obj.reviewer.last_name}"
        return ""
class ProjectUpdateResponseSerializer(serializers.Serializer):
    status = serializers.CharField()
    reviewer = serializers.SerializerMethodField()
    review_date = serializers.DateField()
    delivery_date = serializers.CharField()

    def get_reviewer(self, obj):
        user = obj.reviewer
        return f"{user.first_name} {user.last_name}" if user else ""

class ProjectUpdateResponseSerializer(serializers.Serializer):
    status = serializers.CharField()
    reviewer = serializers.SerializerMethodField()
    review_date = serializers.DateField()
    delivery_date = serializers.CharField()

    def get_reviewer(self, obj):
        user = obj.reviewer
        return f"{user.first_name} {user.last_name}" if user else ""

from rest_framework import serializers
from myappG.models import Activity

class ActivitySerializer(serializers.ModelSerializer):
    photo = serializers.ImageField(required=False)
    class Meta:
        model = Activity
        fields = ['id', 'photo', 'description', 'date']
        read_only_fields = ['id', 'created_at']

    def get_photo_url(self, obj):
        if obj.photo and hasattr(obj.photo, 'name'):
            filename = obj.photo.name
            return f"{settings.DOMAIN}/api/media/{filename}"
        return ""
    def to_representation(self, instance):
        data = super().to_representation(instance)
        data['photo'] = self.get_photo_url(instance)
        return data

from rest_framework import serializers
from myappG.models import News

class NewsSerializer(serializers.ModelSerializer):
    photo = serializers.ImageField(required=False)

    class Meta:
        model = News
        fields = ['id', 'photo', 'description', 'date']
        read_only_fields = ['id', 'created_at']

    def get_photo_url(self, obj):
        if obj.photo and hasattr(obj.photo, 'name'):
            filename = obj.photo.name
            return f"{settings.DOMAIN}/api/media/{filename}"
        return ""

    def to_representation(self, instance):
        data = super().to_representation(instance)
        data['photo'] = self.get_photo_url(instance)
        return data

