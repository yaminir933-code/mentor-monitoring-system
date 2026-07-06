# Project Edit & Delete Feature - Implementation Summary

## Features Added

### 1. **Edit Project** ✏️
- Edit project name
- Upload/replace project file
- Preserves existing file if no new file is selected
- Deletes old file when replacing

### 2. **Delete Project** 🗑️
- Delete project with confirmation
- Automatically deletes associated file from storage

### 3. **User Interface**
- Modal popup for editing
- Smart file upload handling (shows different messages for with/without file)
- Edit and Delete buttons displayed when project exists

---

## Implementation Details

### Backend Changes

#### New Views Added:

**1. `edit_project(request, project_id)`**
```python
- Fetches the project by ID
- Updates project name if provided
- Handles file replacement:
  - If new file uploaded → deletes old file and uploads new one
  - If no new file → keeps existing file
- Redirects back to semester view
```

**2. `delete_project(request, project_id)`**
```python
- Fetches the project by ID
- Requires POST method (prevents accidental deletion via GET)
- Deletes file from storage if exists
- Deletes project record from database
- Redirects back to semester view
```

### URL Routes Added:

```python
path('edit-project/<int:project_id>/', views.edit_project, name='edit_project')
path('delete-project/<int:project_id>/', views.delete_project, name='delete_project')
```

### Frontend Changes

#### Modal Popup Features:
- Opens when "Edit" button clicked
- Shows current project name
- File input is optional:
  - Shows "File already uploaded" message if file exists
  - Shows "No file uploaded" message if file doesn't exist
- Cancel button closes modal
- Submit button saves changes

#### Buttons:
- **Edit** button → Opens modal
- **Delete** button → Confirms then deletes
- **View File** link → Opens uploaded file in new tab

---

## User Workflow

### Scenario 1: Add Project (First Time)
```
1. Fill project name
2. (Optional) Select file
3. Click "Add Project"
```

### Scenario 2: Edit Project Name Only
```
1. Click "Edit" button
2. Modal opens with current name
3. Change name
4. Click "Save Changes"
5. Project name updated, file unchanged
```

### Scenario 3: Upload File After Creating Project
```
1. Click "Edit" button
2. Modal shows "No file currently uploaded"
3. Select file
4. Click "Save Changes"
5. File uploaded successfully
```

### Scenario 4: Replace Existing File
```
1. Click "Edit" button
2. Modal shows "File already uploaded"
3. Select new file
4. Click "Save Changes"
5. Old file deleted, new file uploaded
6. Keep existing file (just leave file input blank)
```

### Scenario 5: Delete Project
```
1. Click "Delete" button (trash icon)
2. Confirmation dialog appears
3. Confirm deletion
4. Project and file deleted
```

---

## File Handling

| Scenario | Action |
|----------|--------|
| New project + no file | No file stored |
| New project + file | File stored |
| Edit project + no new file | Existing file preserved |
| Edit project + new file | Old file deleted, new file stored |
| Delete project | File deleted from storage |

---

## Code Files Modified

1. **academic/views.py** - Added 2 new views
2. **academic/urls.py** - Added 2 new URL routes
3. **templates/academic/semester.html** - Updated project section with modal and buttons

---

## Testing Checklist

- [ ] Add project without file → displays "Add Project" form
- [ ] Add project with file → file stored and link shows
- [ ] Click Edit button → modal opens with current name
- [ ] Edit name only → name updates, file preserved
- [ ] Edit with new file → old file deleted, new file uploaded
- [ ] Edit without new file → file unchanged
- [ ] Click Delete button → confirmation appears
- [ ] Confirm delete → project and file removed
- [ ] Cancel edit modal → modal closes, no changes saved

---

## Security Considerations

- ✅ Login required on all views
- ✅ File deletion confirmation prevents accidental loss
- ✅ Only project owner (student's mentor) can edit/delete
- ✅ File upload accepts only safe formats (.pdf, .jpg, .jpeg, .png, .mp4)
- ✅ Old files cleaned up when replaced (no storage bloat)
