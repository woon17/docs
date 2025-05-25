# System Design: Functional and Non-Functional Requirements

In system design, requirements are typically divided into two major categories:

---

## FR

Functional requirements define **what the system should do** — its behavior, services, and expected operations.

### Examples
- User can register, log in, and log out
- System allows product search and checkout
- Admin can manage user roles and permissions
- API endpoint `/orders/{id}` returns order details in JSON format
- Scheduled jobs generate daily reports at midnight

---

## NFR

Non-functional requirements define **how the system performs** — its quality attributes, constraints, and operating conditions.

### Examples

| Category         | Examples                                                      |
|------------------|---------------------------------------------------------------|
| **Performance**  | Handle 1000 requests/sec with <200ms latency                  |
| **Scalability**  | System should support horizontal scaling                      |
| **Availability** | Ensure 99.99% uptime                                          |
| **Security**     | All user data must be encrypted at rest and in transit       |
| **Reliability**  | System should recover from a crash within 5 seconds           |
| **Maintainability** | Easy to deploy with CI/CD, modular codebase              |
| **Portability**  | Support deployment on AWS, Azure, and GCP                     |
| **Compliance**   | Must adhere to GDPR and PCI-DSS standards                     |

---

## Summary Table

| Type                      | Description                                     |
|---------------------------|-------------------------------------------------|
| **Functional Requirements (FR)**     | What the system should do (features, logic)    |
| **Non-Functional Requirements (NFR)** | How the system should behave (quality, constraints) |
