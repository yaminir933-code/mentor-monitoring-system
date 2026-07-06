# Migration Steps for Multi-Select Subjects Feature

Follow these steps to deploy the multi-select subjects feature:

## Step 1: Create and Apply Migrations

```bash
# Generate migration file for SubjectCatalog model
python manage.py makemigrations academic

# Apply migrations to database
python manage.py migrate
```

This creates the `SubjectCatalog` table.

## Step 2: Populate Predefined Subjects

```bash
# Populate default subjects for Degree and PG programs
python manage.py populate_subjects
```

This command creates:
- 36 subjects for Degree program (6 semesters)
- 20 subjects for PG program (4 semesters)

## Step 3: Verify Installation

### Option A: Using Django Shell
```bash
python manage.py shell
```

Then run:
```python
from academic.models import SubjectCatalog

# Count total subjects
print(f"Total subjects: {SubjectCatalog.objects.count()}")

# Check Degree subjects for Sem 1
degree_sem1 = SubjectCatalog.objects.filter(course_type='Degree', semester=1)
print(f"Degree Sem 1 subjects: {degree_sem1.count()}")
for s in degree_sem1:
    print(f"  - {s.name}")

# Check PG subjects for Sem 1
pg_sem1 = SubjectCatalog.objects.filter(course_type='PG', semester=1)
print(f"PG Sem 1 subjects: {pg_sem1.count()}")
for s in pg_sem1:
    print(f"  - {s.name}")

exit()
```

### Option B: Using Django Admin
1. Go to `/admin/academic/subjectcatalog/`
2. Verify you see all subjects listed
3. Check filters for different course types and semesters

## Step 4: Test the Feature

1. Log in as a mentor
2. Go to Academic Guidance
3. Select a student and click a semester (e.g., Sem 1)
4. In the **Subjects** section, verify:
   - Multi-select dropdown appears with all subjects
   - Helper text shows "Hold Ctrl to select multiple"
   - You can select multiple subjects
   - Click "Add All Selected Subjects"
   - Subjects appear in the "Added Subjects" list
   - Refresh page → Already-added subjects show with ✓

## Step 5: Customize Subjects (Optional)

If you want to modify the predefined subjects:

### Via Django Admin
1. Go to `/admin/academic/subjectcatalog/`
2. Click "Add Subject Catalog"
3. Fill in: Course Type, Semester, Name, Code (optional)
4. Save

### Via Management Command
Edit `academic/management/commands/populate_subjects.py`:
1. Modify the `degree_subjects` and `pg_subjects` dictionaries
2. Run: `python manage.py populate_subjects`

## Step 6: Rollback (If Needed)

To revert these changes:

```bash
# Remove the migration
python manage.py migrate academic <previous_migration_name>

# Or delete the SubjectCatalog entries
python manage.py shell
from academic.models import SubjectCatalog
SubjectCatalog.objects.all().delete()
exit()
```

## Troubleshooting

### "No module named 'academic.management'"
- Ensure `academic/management/__init__.py` exists (should be created automatically)
- Restart your Django server

### "SubjectCatalog table doesn't exist"
- Run: `python manage.py migrate`

### Subjects don't appear in dropdown
- Check database: `python manage.py shell` → `SubjectCatalog.objects.count()`
- If count is 0, run: `python manage.py populate_subjects`

### "get_subjects_by_semester() takes 2 positional arguments but 3 were given"
- This is likely a caching issue
- Restart Django: `python manage.py runserver --reload`

## Files Created/Modified

### Created
- `academic/models.py` - Added SubjectCatalog model
- `academic/admin.py` - Django admin interfaces
- `academic/management/commands/populate_subjects.py` - Management command
- `academic/management/__init__.py` - Package marker
- `academic/management/commands/__init__.py` - Package marker
- `MULTI_SELECT_SUBJECTS_README.md` - Feature documentation

### Modified
- `academic/views.py` - Added get_subjects_by_semester, updated add_subject
- `academic/urls.py` - Added get_subjects endpoint
- `templates/academic/semester.html` - Replaced subject input with multi-select
- `migrations/` - New migration file (auto-generated)

## Next Steps

1. Train mentors on the new UI:
   - Hold Ctrl/Cmd to select multiple subjects
   - Already-added subjects are disabled
   - Click button to add all at once

2. Monitor usage:
   - Verify subjects are being added correctly
   - Check for JavaScript console errors
   - Gather feedback for improvements

3. Consider future enhancements:
   - Search in dropdown
   - Subject prerequisites
   - Credit hours tracking
   - Bulk import/export

---

Need help? Check `MULTI_SELECT_SUBJECTS_README.md` for detailed feature documentation.
