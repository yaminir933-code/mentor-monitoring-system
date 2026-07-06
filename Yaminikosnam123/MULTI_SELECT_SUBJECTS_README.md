# Multi-Select Subjects Feature

## Overview
This feature replaces the single-input subject field with a **multi-select dropdown** that allows mentors to add multiple subjects at once for a semester. The dropdown is dynamically populated based on:
- Student's course type (Degree or PG)
- Selected semester
- Predefined subject catalog

## What Changed

### 1. **New Model: SubjectCatalog**
- Stores all available subjects for Degree and PG programs
- Organized by course type and semester
- Can be managed through Django admin

### 2. **Updated Views**
- `add_subject()`: Now handles both single subjects (legacy) and bulk subjects from multi-select
- `get_subjects_by_semester()`: New API endpoint that returns available subjects for a semester

### 3. **Updated Template (semester.html)**
- Replaced single text input with `<select multiple>`
- Added JavaScript to fetch and populate subjects dynamically
- Shows which subjects are already added (disabled with ✓ indicator)
- Added helper text explaining multi-select usage

### 4. **URLs**
- Added new endpoint: `/academic/get-subjects/<student_id>/<sem_number>/`

## Setup Instructions

### Step 1: Run Migrations
```bash
python manage.py makemigrations academic
python manage.py migrate
```

### Step 2: Populate Subject Catalog
Run the management command to populate predefined subjects:
```bash
python manage.py populate_subjects
```

This will create:
- **Degree Program**: 6 semesters × ~6 subjects = 36 subjects
- **PG Program**: 4 semesters × ~5 subjects = 20 subjects

### Step 3: Customize Subjects (Optional)
You can:
1. Use Django Admin (`/admin/academic/subjectcatalog/`) to add/edit/delete subjects
2. Modify the `populate_subjects.py` command with your institution's subjects
3. Re-run the command to add more subjects

## How It Works

### User Flow
1. Mentor navigates to a semester view (e.g., Student → Sem 1)
2. Opens the **Subjects** section
3. Clicks on the multi-select dropdown
4. Sees all available subjects for that semester based on course type
5. Already-added subjects show as disabled with ✓ indicator
6. Selects multiple subjects (Ctrl+Click or Cmd+Click)
7. Clicks "Add All Selected Subjects" button
8. All selected subjects are added at once

### Technical Flow
1. Page loads → JavaScript calls `/academic/get-subjects/<student_id>/<sem_number>/`
2. API returns: all available subjects + already-added subjects
3. Dropdown populated with available subjects
4. Already-added subjects are disabled
5. User selects subjects and submits form
6. Backend handles both single subject names (`subject_name`) and bulk (`subject_names[]`)

## API Response Example
```json
{
  "subjects": [
    "Mathematics I",
    "Physics I",
    "Chemistry I",
    "Programming Fundamentals",
    "Engineering Graphics",
    "Environmental Science"
  ],
  "already_added": ["Mathematics I", "Physics I"],
  "course_type": "Degree"
}
```

## Backward Compatibility
- Legacy single-subject form still works (uses `subject_name` field)
- All existing subjects continue to work
- No breaking changes to the data model

## Predefined Subjects

### Degree Program (6 Semesters)
- **Sem 1**: Mathematics I, Physics I, Chemistry I, Programming Fundamentals, Engineering Graphics, Environmental Science
- **Sem 2**: Mathematics II, Physics II, Chemistry II, Data Structures, Digital Logic Design, Communication Skills
- **Sem 3**: Discrete Mathematics, Algorithms, Object-Oriented Programming, Database Systems, Web Technologies, Operating Systems
- **Sem 4**: Software Engineering, Computer Networks, Database Management, System Design, Advanced Web Development, Mobile Applications
- **Sem 5**: Machine Learning, Cloud Computing, Cybersecurity, Big Data Analytics, Artificial Intelligence, DevOps
- **Sem 6**: Project Management, Entrepreneurship, Professional Ethics, Technical Writing, Advanced Topics, Capstone Project

### PG Program (4 Semesters)
- **Sem 1**: Advanced Algorithms, Machine Learning, Natural Language Processing, Research Methodology, Advanced Database Systems
- **Sem 2**: Deep Learning, Computer Vision, Distributed Systems, Advanced Network Security, Cloud Architecture
- **Sem 3**: Advanced Machine Learning, Reinforcement Learning, Neural Networks, Big Data Analytics, Advanced Optimization
- **Sem 4**: Project Dissertation, Research Colloquium, Advanced Topics Seminar, Industry Internship, Thesis Work

## Customization

### Adding New Subjects
**Via Django Admin:**
1. Go to `/admin/academic/subjectcatalog/`
2. Click "Add Subject Catalog"
3. Fill in: Course Type, Semester, Name, Code (optional)
4. Save

**Via Management Command:**
Edit `academic/management/commands/populate_subjects.py` and add subjects to the dictionaries.

### Styling
Multi-select styling is in `semester.html` `<style>` section. You can customize:
- `select[multiple]` - Main dropdown styling
- `select[multiple]:focus` - Focus state
- `select[multiple] option:checked` - Selected items color

## Testing

### Test Cases
1. **Bulk Add**: Select 3 subjects → Verify all 3 are added
2. **Already Added**: Refresh page → Verify already-added subjects are disabled
3. **Degree vs PG**: Switch between Degree/PG students → Verify correct subjects appear
4. **Semester Specific**: Add subjects to Sem 1 → Switch to Sem 2 → Verify different subjects
5. **Legacy Single Add**: Use manual text input → Verify still works

## Troubleshooting

### Subjects Not Appearing?
1. Verify `SubjectCatalog` has entries: `python manage.py shell`
   ```python
   from academic.models import SubjectCatalog
   SubjectCatalog.objects.count()  # Should be >0
   ```
2. Run populate_subjects: `python manage.py populate_subjects`
3. Check browser console for JavaScript errors

### Already-Added Not Disabling?
1. Verify `Subject` records exist for the student
2. Check API response: Open browser DevTools → Network tab → Check `/academic/get-subjects/...` response

### Form Not Submitting?
1. Ensure at least one subject is selected
2. Check that dropdown has `name="subject_names"` attribute
3. Verify CSRF token is present in form

## Files Modified
- `academic/models.py` - Added SubjectCatalog model
- `academic/views.py` - Updated add_subject, added get_subjects_by_semester
- `academic/urls.py` - Added get_subjects endpoint
- `templates/academic/semester.html` - Replaced subject input with multi-select dropdown
- `academic/admin.py` - Added admin interfaces (new)
- `academic/management/commands/populate_subjects.py` - Management command (new)

## Future Enhancements
- [ ] Subject prerequisites/dependencies
- [ ] Subject credit hours
- [ ] Drag-drop reordering
- [ ] Bulk export/import subjects
- [ ] Custom subject lists per program
- [ ] Subject search/filter in dropdown
