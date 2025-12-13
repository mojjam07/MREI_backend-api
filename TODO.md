# TODO: Replace 'staff' with 'admin' and remove 'staff' completely

## Tasks
- [ ] Update ROLE_CHOICES in backend/users/models.py: Remove ("staff", "Staff")
- [ ] Rename StaffProfile to AdminProfile in backend/users/models.py
- [ ] Update permissions.py: Change IsStaffOrAdmin to IsAdmin
- [ ] Update backend/users/views.py: Change profile creation logic from 'staff' to 'admin'
- [ ] Update backend/communication/views.py: Replace is_staff checks with role-based checks for 'admin'
- [ ] Update backend/users/migrations/0001_initial.py: Reflect changes in migration
- [ ] Run migrations to update database schema
- [ ] Test the application for role-based access
