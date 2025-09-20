from rest_framework import serializers
from .utils import send_otp_email
from django.utils import timezone
from datetime import timedelta
from django.contrib.auth.password_validation import validate_password
import random
import string
from rest_framework_simplejwt.tokens import RefreshToken,TokenError
from django.conf import settings


from .models import (
    CustomUser,
    Beneficiary,
    MedicalAidRequest,
    MaterialAidRequest,
    ProjectRequest,
    # Evaluation,
    Activity,
    News,
    PendingUser,
    Feedback,
)
from rest_framework.authtoken.models import Token
from django.contrib.auth import authenticate
from django.core.exceptions import ValidationError

class RegisterPendingUserSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)
    confirm_password = serializers.CharField(write_only=True)

    class Meta:
        model = PendingUser
        fields = [
            'first_name', 'last_name', 'email', 'phone',
            'password', 'confirm_password', 'address',
            'gender', 'birth_date', 'profile_picture'
        ]

    def validate(self, data):
        if data['password'] != data['confirm_password']:
            raise serializers.ValidationError("كلمتا السر غير متطابقتين")
        if PendingUser.objects.filter(email=data['email']).exists():
            raise serializers.ValidationError('تم ارسال هذا الرمز مسبقا لهذا البريد')
        if CustomUser.objects.filter(email=data['email']).exists():
            raise serializers.ValidationError("هذا البريد مستخدم بالفعل")
        return data

    def create(self, validated_data):
        password = validated_data.pop('password')
        validated_data.pop('confirm_password')
        otp = ''.join(random.choices('0123456789', k=4))
        validated_data['otp_created'] = timezone.now()
        validated_data['otp'] = otp
        validated_data['password'] = password
        pending_user = PendingUser.objects.create(**validated_data)
        send_otp_email(pending_user.email, otp)
        return pending_user

class ConfirmOTPSerializer(serializers.Serializer):
    expiry_minute = 10
    email = serializers.EmailField()
    otp = serializers.CharField(max_length=4)

    def validate(self, data):
        try:
            pending = PendingUser.objects.get(email=data['email'], otp=data['otp'])
        except PendingUser.DoesNotExist:
            raise serializers.ValidationError('رمز التحقق غير صحيح')

        if timezone.now() > pending.otp_created + timedelta(minutes=self.expiry_minute):
            raise serializers.ValidationError("انتهت صلاحية رمز التحقق الرجاء طلب رمز جديد")

        self.pending_user = pending
        return data

    def create(self, validated_data):
        pending = self.pending_user

        from .utils import generate_unique_username  # make sure this exists

        username = generate_unique_username()
        user = CustomUser.objects.create(
            username=username,
            first_name=pending.first_name,
            last_name=pending.last_name,
            email=pending.email,
            phone=pending.phone,
            address=pending.address,
            gender=pending.gender,
            birth_date=pending.birth_date,
            profile_picture=pending.profile_picture,
            is_verified=True,
            user_type='beneficiary',
            otp_created=pending.otp_created
        )
        user.set_password(pending.password)
        user.save()
        pending.delete()
        return user


class EmailLoginSerializer(serializers.Serializer):
    email=serializers.EmailField()
    password=serializers.CharField(write_only=True)
    access=serializers.CharField(read_only=True)
    refresh=serializers.CharField(read_only=True)
    def validate(self, data):
        email=data.get('email')
        password=data.get('password')
        try:
            user=CustomUser.objects.get(email=email)
        except CustomUser.DoesNotExist:
            raise serializers.ValidationError("لا يوجد مستخدم بهذا البريد")
        if not user.check_password(password):
            raise serializers.ValidationError("كلمة المرور غير صحيحة")
        if not user.is_verified:
            raise serializers.ValidationError("لم يتم تأكيد حسابك بعد")
        tokens=RefreshToken.for_user(user)
        return{"access":str(tokens.access_token),
               "refresh":str(tokens),}

class LogoutSerializer(serializers.Serializer):
    refresh = serializers.CharField()

    def validate(self, attrs):
        self.token = attrs["refresh"]
        user = self.context['request'].user

        return attrs

    def save(self, **kwargs):
        try:
            token = RefreshToken(self.token)
            token.blacklist()
        except TokenError:
            raise serializers.ValidationError("رمز غير صالح أو منتهي")


class ProfileUserSerializer(serializers.ModelSerializer):
    profile_picture = serializers.ImageField(required=False)

    class Meta:
        model = CustomUser
        fields = [
            'first_name', 'last_name', 'email',
            'birth_date', 'phone', 'address',
            'gender', 'profile_picture'
        ]

    def get_profile_picture_url(self, obj):
        if obj.profile_picture and hasattr(obj.profile_picture, 'name'):
            filename = obj.profile_picture.name
            return f"{settings.DOMAIN}/api/media/{filename}"
        return ""

    def to_representation(self, instance):
        data = super().to_representation(instance)
        data['profile_picture'] = self.get_profile_picture_url(instance)
        return data


class ForgotPasswordRequestSerializer(serializers.Serializer):
    email = serializers.EmailField()
    otp = serializers.CharField(read_only=True)  # exposed in response

    def validate_email(self, email):
        if not CustomUser.objects.filter(email=email).exists():
            raise serializers.ValidationError("لا يوجد مستخدم بهذا البريد الالكتروني")
        return email

    def save(self):
        email = self.validated_data['email']
        user = CustomUser.objects.get(email=email)
        otp = ''.join(random.choices('0123456789', k=4))
        user.verification_token = otp
        user.otp_created = timezone.now()
        user.save()
        send_otp_email(email, otp)
        self._otp = otp  # stash for response
        return user

    def to_representation(self, instance):
        return {
            'otp': getattr(self, '_otp', None)
        }



class ConfirmPasswordResetOTPSerializer(serializers.Serializer):
    email = serializers.EmailField()
    otp = serializers.CharField(max_length=4)

    def validate(self, data):
        try:
            user = CustomUser.objects.get(email=data['email'], verification_token=data['otp'])
        except CustomUser.DoesNotExist:
            raise serializers.ValidationError("رمز التحقق غير صحيح ")

        if not user.otp_created or timezone.now() > user.otp_created + timedelta(minutes=7):
            raise serializers.ValidationError("انتهت صلاحية رمز التحقق ")

        return data

class ResetPasswordSerializer(serializers.Serializer):
    email = serializers.EmailField()
    otp = serializers.CharField(max_length=4)
    new_password = serializers.CharField(write_only=True)
    confirm_password = serializers.CharField(write_only=True)

    def validate(self, data):
        if data['new_password'] != data['confirm_password']:
            raise serializers.ValidationError("كلمة السر غير متطابقين")
        try:
            validate_password(data['new_password'])
        except Exception as e:
            raise serializers.ValidationError(str(e))
        return data

    def save(self):
        email = self.validated_data['email']
        otp = self.validated_data['otp']
        new_password = self.validated_data['new_password']

        user = CustomUser.objects.get(email=email, verification_token=otp)
        user.set_password(new_password)
        user.verification_token = None
        user.save()

class BeneficiarySerializer(serializers.ModelSerializer):
    class Meta:
        model = Beneficiary
        exclude = ['user' , 'created_at' , 'updated_at']

from rest_framework import serializers
from django.conf import settings

class MedicalAidRequestSerializer(serializers.ModelSerializer):
    beneficiary = BeneficiarySerializer(read_only=True)
    aid_type_display = serializers.CharField(source='get_aid_type_display', read_only=True)
    status_display = serializers.CharField(source='get_status_display', read_only=True)
    reviewer = serializers.SerializerMethodField()
    delivery_date = serializers.CharField()  # Force DRF to treat it as plain string

    medical_report = serializers.FileField(required=False)  # Writable for upload

    class Meta:
        model = MedicalAidRequest
        fields = '__all__'
        read_only_fields = [
            'id',
            'beneficiary',
            'status',
            'status_display',
            'request_date',
            'review_date',
            'delivery_date',
            'reviewer'
        ]

    def get_reviewer(self, obj):
        if obj.reviewer:
            return f"{obj.reviewer.first_name} {obj.reviewer.last_name}"
        return ""

    def get_medical_report_url(self, obj):
        if obj.medical_report and hasattr(obj.medical_report, 'name'):
            filename = obj.medical_report.name
            return f"{settings.DOMAIN}/api/media/{filename}"
        return ""

    def to_representation(self, instance):
        data = super().to_representation(instance)
        data['medical_report'] = self.get_medical_report_url(instance)
        return data


class MedicalAidRequestListSerializer(serializers.ModelSerializer):
    aid_type_display = serializers.CharField(source='get_aid_type_display', read_only=True)
    status_display = serializers.CharField(source='get_status_display', read_only=True)
    delivery_date = serializers.SerializerMethodField()  # Force DRF to treat it as plain string

    class Meta:
        model = MedicalAidRequest
        fields = [
            'id',
            'aid_type',
            'aid_type_display',
            'status',
            'status_display',
            'request_date',
            'review_date',
            'delivery_date'
        ]
    def get_delivery_date(self, obj):
        if obj.delivery_date :
            return obj.delivery_date
        return ""

class MaterialAidRequestSerializer(serializers.ModelSerializer):
    beneficiary = BeneficiarySerializer(read_only=True)
    aid_type_display = serializers.CharField(source='get_aid_type_display', read_only=True)
    status_display = serializers.CharField(source='get_status_display', read_only=True)
    reviewer = serializers.SerializerMethodField()
    delivery_date = serializers.SerializerMethodField()


    class Meta:
        model = MaterialAidRequest
        fields = '__all__'
        read_only_fields = [
            'id',
            'beneficiary',
            'status',
            'status_display',
            'request_date',
            'review_date',
            'delivery_date',
            'reviewer'
        ]

    def get_delivery_date(self, obj):
        if obj.delivery_date :
            return obj.delivery_date
        return ""
    def get_reviewer(self, obj):
        if obj.reviewer:
            return f"{obj.reviewer.first_name} {obj.reviewer.last_name}"
        return None

class MaterialAidRequestSerializer(serializers.ModelSerializer):
    beneficiary = BeneficiarySerializer(read_only=True)
    aid_type_display = serializers.CharField(source='get_aid_type_display', read_only=True)
    status_display = serializers.CharField(source='get_status_display', read_only=True)
    reviewer = serializers.SerializerMethodField()
    delivery_date = serializers.CharField()  # Force DRF to treat it as plain string


    class Meta:
        model = MaterialAidRequest
        fields = '__all__'
        read_only_fields = [
            'id',
            'beneficiary',
            'status',
            'status_display',
            'request_date',
            'review_date',
            'delivery_date',
            'reviewer'
        ]

    def get_reviewer(self, obj):
        if obj.reviewer:
            return f"{obj.reviewer.first_name} {obj.reviewer.last_name}"
        return ""


class ProjectRequestSerializer(serializers.ModelSerializer):
    beneficiary = BeneficiarySerializer(read_only=True)
    reviewer = serializers.SerializerMethodField()

    class Meta:
        model = ProjectRequest
        fields = '__all__'
        read_only_fields = ['id', 'beneficiary', 'created_at', 'status', 'reviewer']

    def get_reviewer(self, obj):
        if obj.reviewer:
            return f"{obj.reviewer.first_name} {obj.reviewer.last_name}"
        return ""


class ActivityListSerializer(serializers.ModelSerializer):
    short_description = serializers.SerializerMethodField()
    photo = serializers.SerializerMethodField()
    class Meta:
        model = Activity
        fields = ['id', 'photo', 'short_description' , 'date', 'description']

    def get_short_description(self, obj):
        words = obj.description.split()
        return ' '.join(words[:20]) + ('...' if len(words) > 20 else '')

    def get_photo(self, obj):
        if obj.photo:
            filename = obj.photo.name  # includes subfolder if any
            return f"{settings.DOMAIN}/api/media/{filename}"
        return ""

class ActivityDetailSerializer(serializers.ModelSerializer):
    photo = serializers.SerializerMethodField()
    class Meta:
        model = Activity
        fields = ['id', 'photo', 'description' , 'date']

    def get_photo(self, obj):
        if obj.photo:
            filename = obj.photo.name  # includes subfolder if any
            return f"{settings.DOMAIN}/api/media/{filename}"
        return ""

class NewsListSerializer(serializers.ModelSerializer):
    short_description = serializers.SerializerMethodField()

    class Meta:
        model = News
        fields = ['id', 'short_description','date' , 'photo' , 'description']

    def get_short_description(self, obj):
        words = obj.description.split()
        return ' '.join(words[:30]) + ('...' if len(words) > 30 else '')

class NewsDetailSerializer(serializers.ModelSerializer):
    photo = serializers.SerializerMethodField()
    class Meta:
        model = News
        fields = ['id', 'photo', 'description','date']

    def get_photo(self, obj):
        if obj.photo:
            filename = obj.photo.name  # includes subfolder if any
            return f"{settings.DOMAIN}/api/media/{filename}"
        return ""

class FeedbackSerializer(serializers.ModelSerializer):
    rating = serializers.IntegerField(min_value=1, max_value=5)

    class Meta:
        model = Feedback
        fields = ['rating', 'is_satisfied', 'will_use_again', 'notes']

    def create(self, validated_data):
        user = self.context['request'].user
        if Feedback.objects.filter(user=user).exists():
            raise serializers.ValidationError("لقد قمت بارسال تقييم مسبقا")
        return Feedback.objects.create(user=user, **validated_data)