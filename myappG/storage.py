
# myappG/storage.py
from django.core.files.storage import FileSystemStorage
from django.conf import settings

class OverwriteStorage(FileSystemStorage):
    """
    يسمح بالكتابة فوق الملفات الموجودة بنفس الاسم
    """
    def get_available_name(self, name, max_length=None):
        if self.exists(name):
            self.delete(name)
        return name

# يمكنك استخدامه في النماذج هكذا:
# file = models.FileField(storage=OverwriteStorage())