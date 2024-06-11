

### API Endpoints

#### General
- `GET /` : Get available routes

#### Authentication
- `POST /token/` : Obtain a new token pair (access and refresh tokens)

#### User Side
- `POST /user/register/` : Register a new user
- `PUT /user/update-profile/` : Update user profile
- `GET /user/user-profile/<int:id>/` : Retrieve user profile details
- `GET /user/detail-view/<int:id>/` : Detailed view of a user
- `GET /user/category-list/` : List all categories
- `GET /user/subcategory-list/<int:category_id>/` : List subcategories of a specific category
- `GET /user/course-list/` : List all courses
- `GET /user/course-detail/<int:id>/` : Detailed view of a specific course
- `GET /user/plans/` : List all plans
- `POST /user/subscription/create/` : Create a new subscription
- `POST /user/create-razorpay-order/` : Create a new Razorpay order
- `GET /user/subscriptions/` : List all subscriptions of the user
- `GET /user/lives-list/` : List all live classes for the user
- `GET /user/courses/<int:course_id>/lessons/` : List all lessons in a specific course

#### Admin Side
- `POST /admin/logout/` : Admin logout
- `GET /admin/users/` : List all users
- `PUT /admin/block-unblock/<int:pk>/` : Block or unblock a user
- `GET /admin/tutors/` : List all tutors
- `PUT /admin/tutor/block-unblock/<int:pk>/` : Block or unblock a tutor
- `POST /admin/create-categories/` : Create a new category
- `PUT /admin/categories/<int:category_id>/` : Update a specific category
- `PUT /admin/categories/block-unblock/<int:pk>/` : Block or unblock a category
- `GET /admin/categories/` : List all categories
- `GET /admin/sub-categories/` : List all subcategories
- `POST /admin/create/sub-categories/` : Create a new subcategory
- `PUT /admin/sub-categories/block-unblock/<int:pk>/` : Block or unblock a subcategory
- `PUT /admin/update/sub-categories/<int:subcategory_id>/` : Update a specific subcategory
- `GET /admin/categories/<int:category_id>/subcategories/` : List all subcategories of a specific category
- `GET /admin/plans/` : List all plans
- `POST /admin/create/plan/` : Create a new plan
- `PUT /admin/block-unblock-plan/<int:pk>/` : Block or unblock a plan
- `GET /admin/features-list/` : List all features
- `GET /admin/view-features/<int:plan_id>/` : View details of features in a specific plan
- `POST /admin/create-feature/` : Create a new feature
- `PUT /admin/edit-features/<int:pk>/` : Edit a specific feature
- `GET /admin/course-list/` : List all courses
- `POST /admin/course-create/` : Create a new course
- `PUT /admin/block-unblock-course/<int:pk>/` : Block or unblock a course
- `GET /admin/subscriptions/` : List all subscriptions

#### Tutor Side
- `POST /tutor/register/` : Register a new tutor
- `PUT /tutor/update-profile/` : Update tutor profile
- `GET /tutor/user-profile/<int:id>/` : Retrieve tutor profile details
- `GET /tutor/courses/` : List all courses of the tutor
- `PUT /tutor/edit-course/<int:course_id>/` : Edit a specific course
- `GET /tutor/categories/` : List all categories
- `POST /tutor/create-live/` : Create a new live class
- `GET /tutor/lives-list/` : List all live classes of the tutor
- `GET /tutor/lives-schedules/` : List live classes scheduled for today
- `POST /tutor/create-lessons/` : Create a new lesson
- `GET /tutor/lessons-list/` : List all lessons of the tutor
- `PUT /tutor/lessons-edit/<int:pk>/` : Edit a specific lesson
- `PUT /tutor/live-status-update/<int:pk>/` : Update status of a live class

This should provide a clear and structured list of the API endpoints for users, administrators, and tutors.
