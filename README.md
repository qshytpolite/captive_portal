# 🎫 Django Voucher-Based Captive Portal

A scalable Django web application for managing business WiFi access using voucher-based authentication, session tracking, and per-business dashboards.

---

## 📌 Features

### ✅ Phase 1: Project Structure & Setup
- Modular Django apps (Accounts, Business, Voucher, Portal, Payments, RouterAPI, Core)
- Custom user model with support for business roles
- TailwindCSS 4.1 integration via Django-Tailwind
- PostgreSQL 15+ database support (non-Docker)

### ✅ Phase 2: Admin & Business Logic
- Businesses can manage users, quotas, and subscriptions
- Role-based membership via `BusinessMembership`
- Voucher generation and usage tracking
- Payments and webhook stubs for M-Pesa

### ✅ Phase 3: Business Self-Service
- Business dashboards with analytics
- Business profile editing
- Voucher creation via admin or dashboard
- Multi-business management per user
- Session usage insights

### ✅ Phase 4: Captive Portal & End-User Access
- Voucher login interface (mobile-first)
- Captive session tracking (IP, MAC, User Agent)
- Auto-authentication hooks
- Stubbed RouterOS API forwarding support

---

## 🛠 Tech Stack

| Layer         | Tool / Framework      |
|---------------|------------------------|
| Backend       | Django 5.x (Python 3.12) |
| Database      | PostgreSQL 15+         |
| Frontend      | TailwindCSS 4.1, Alpine.js |
| Forms & Auth  | Django forms, sessions |
| Admin Tools   | Django admin, custom inlines |
| Captive Logic | Custom voucher/session APIs |
| Deployment    | Manual / systemd / gunicorn-ready |
