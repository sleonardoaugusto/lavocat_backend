from lavocat.attendances.models import Attendance, ServicesTypesOptions, Note


for attendance in Attendance.objects.all():
    notes = []
    for service in attendance.services_types:
        label = ServicesTypesOptions(service).label
        notes.append(Note(attendance=attendance, header=label))
        Note.objects.bulk_create(notes)
