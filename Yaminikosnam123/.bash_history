python manage.py shell
from students.models import Student
print(Student.objects.all().count())
print(list(Student.objects.all()))
exit() from students.models import Student
print(Student.objects.all().count())
print(list(Student.objects.all()))
exit()
