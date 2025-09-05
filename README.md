# 🏋️‍♂️ GymLog API

## 📌 About The Project
The **GymLog API** is the backend service for a comprehensive fitness tracker. It provides a secure and organized way for users to store their workout data and access powerful analytics. Designed for scalability, performance, and security, it serves as a robust foundation for any frontend application—whether web, mobile, or desktop.

---

## 🛠️ Built With
* **Python** 3.13
* **Django**
* **Django REST Framework**
* **Django Simple JWT**
* **MySQL**

---

## 🚀 Key Features
* **🔐 User Authentication & Management**
    * Secure registration and login using **JWT**
    * Profile picture support
    * Age calculation
* **🏋️ Workout Management**
    * Full **CRUD** (Create, Read, Update, Delete) for workout logs
    * Fields: exercise name, weight, reps, sets, duration, notes, images
* **📊 Real-time Analytics**
    * Weekly metrics: total volume, max lift, average intensity, calories burned, strength level
* **🗂️ Category System**
    * Organize workouts by category (e.g., Cardio, Strength Training)
    * Enhanced filtering and analytics
* **⚙️ API Enhancements**
    * Pagination and filtering support
    * Filter workouts by date, category, and more
* **🔒 Security**
    * **JWT-based authentication**
    * Refresh token blacklisting
    * Environment-based secret management

---

## 📦 Prerequisites
To run this project locally, you'll need:
* Python 3.13
* `pip` (Python package installer)
* A **MySQL** database

---

## 🧭 Getting Started
Follow these steps to get a local copy of the project up and running:
1.  **Clone the repository**
2.  **Create and activate a virtual environment**
3.  **Install dependencies**
4.  **Set up environment variables**
5.  **Run database migrations**
6.  **Run the development server**

---

## 📡 API Endpoints
All endpoints are prefixed with `/api/`.

### 🔐 Authentication
| Endpoint | Method | Description |
| :--- | :--- | :--- |
| `/api/users/register/` | `POST` | Create a new user account |
| `/api/users/login/` | `POST` | Authenticate and receive JWT tokens |
| `/api/users/profile/` | `GET` | Retrieve authenticated user's profile |
| `/api/users/token/refresh/` | `POST` | Refresh access token |
| `/api/users/logout/` | `POST` | Blacklist refresh token and log out |

### 🏋️ Workouts
| Endpoint | Method | Description |
| :--- | :--- | :--- |
| `/api/workouts/` | `GET` | List all workouts (pagination/filter) |
| `/api/workouts/` | `POST` | Create a new workout entry |
| `/api/workouts/<id>/` | `GET` | Retrieve a specific workout |
| `/api/workouts/<id>/` | `PUT` | Update a specific workout |
| `/api/workouts/<id>/` | `DELETE` | Delete a workout |

### 🗂️ Categories
| Endpoint | Method | Description |
| :--- | :--- | :--- |
| `/api/workouts/categories/` | `GET` | List all workout categories |
| `/api/workouts/categories/` | `POST` | Create a new category |
| `/api/workouts/categories/<id>/` | `GET` | Retrieve a specific category |
| `/api/workouts/categories/<id>/` | `PUT` | Update a category |
| `/api/workouts/categories/<id>/` | `DELETE` | Delete a category |

### 📊 Analytics
| Endpoint | Method | Description |
| :--- | :--- | :--- |
| `/api/workouts/analytics/` | `GET` | Generate and retrieve weekly analytics |

---

## 🔐 Authentication Notes
To access protected endpoints, include a valid **JWT access token** in the request header:
# Authorization: Bearer <your_access_token>
* Access tokens expire after **2 hours**.
* Refresh tokens last **7 days**.
* `logout` blacklists the refresh token to prevent reuse.

---

## 🚀 Deployment
Deployment is intended for **Heroku**, but not yet implemented. Future steps will include:
* Connecting to a remote MySQL instance
* Configuring environment variables via Heroku dashboard
* Enabling media storage for uploaded workout images

---

## 🧱 Architecture Overview
The **GymLog API** is organized into modular apps:
* **Users App**: Registration, login, profile updates, JWT authentication
* **Workouts App**: Workout entries, categories, analytics
* **Analytics Engine**: Weekly metrics via **MET-based formulas** and user data

### Design Principles
* **Model-driven architecture** with paired serializers and views
* **Scoped access** for privacy and multi-user support
* **Computed fields** exposed via serializers for frontend convenience

---

## 🧮 Serializers
Serializers validate and transform data between models and **JSON**:
* `UserProfileSerializer`: User creation, profile updates, password hashing, image uploads
* `WorkoutSerializer`: Includes `category_name`, enforces read-only user access
* `AnalyticsSerializer`: Exposes weekly metrics, protects computed fields

---

## 🔐 Permissions & Security
* All sensitive endpoints require `IsAuthenticated`.
* **JWT tokens** are issued via `SimpleJWT`.
* Refresh tokens are blacklisted on logout.
* Secrets and DB credentials are managed via **environment variables**.

---

## 🔍 Filtering & Pagination
Workout listings support:
* **Pagination** via `PageNumberPagination` (default page size: 10)
* **Filtering** via `DjangoFilterBackend` and a custom `WorkoutFilter` (e.g., by date, category)

---

## 📈 Analytics Logic
The `/api/workouts/analytics/` endpoint computes:
* **Total Volume**: `weight` × `reps` × `sets` for strength workouts
* **Max Lift**: Heaviest weight lifted during the week
* **Calories Burned**: Estimated via **MET values** and user weight
* **Intensity**: Volume divided by workout duration
* **Strength Level**: Categorized as `Beginner`, `Intermediate`, or `Advanced`

