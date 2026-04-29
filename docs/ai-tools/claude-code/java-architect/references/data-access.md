# Reference: data-access

**Source file:** `.claude/java-architect/references/data-access.md`

# Data Access Patterns

## pom.xml additions

```xml
<!-- JPA + DB driver (choose one driver) -->
<dependency>
    <groupId>org.springframework.boot</groupId>
    <artifactId>spring-boot-starter-data-jpa</artifactId>
</dependency>
<dependency>
    <groupId>org.postgresql</groupId>
    <artifactId>postgresql</artifactId>
</dependency>

<!-- Migrations -->
<dependency>
    <groupId>org.flywaydb</groupId>
    <artifactId>flyway-core</artifactId>
</dependency>

<!-- Reactive (R2DBC alternative) -->
<dependency>
    <groupId>org.springframework.boot</groupId>
    <artifactId>spring-boot-starter-data-r2dbc</artifactId>
</dependency>

<!-- Testing -->
<dependency>
    <groupId>org.testcontainers</groupId>
    <artifactId>postgresql</artifactId>
    <scope>test</scope>
</dependency>
```

## application.yml additions

```yaml
spring:
  datasource:
    url: ${DATABASE_URL:jdbc:postgresql://localhost:5432/demo}
    username: ${DATABASE_USER:demo}
    password: ${DATABASE_PASSWORD:demo}
    hikari:
      maximum-pool-size: 10
      minimum-idle: 5
      connection-timeout: 20000

  jpa:
    hibernate:
      ddl-auto: validate
    open-in-view: false
    properties:
      hibernate:
        jdbc:
          batch_size: 20
        order_inserts: true
        order_updates: true

  flyway:
    enabled: true
    baseline-on-migrate: true
    locations: classpath:db/migration
```

## JPA Entity

```java
@Entity
@Table(name = "orders")
@EntityListeners(AuditingEntityListener.class)
public class Order {

    @Id
    @GeneratedValue(strategy = GenerationType.UUID)
    private UUID id;

    @Column(nullable = false)
    private UUID customerId;

    @Enumerated(EnumType.STRING)
    private OrderStatus status;

    @CreatedDate
    private Instant createdAt;

    @LastModifiedDate
    private Instant updatedAt;
}
```

## Repository with Optimized Queries

```java
public interface OrderRepository extends JpaRepository<Order, UUID> {

    // Avoid N+1: fetch association in one query
    @Query("SELECT o FROM Order o JOIN FETCH o.items WHERE o.customerId = :customerId")
    List<Order> findByCustomerIdWithItems(@Param("customerId") UUID customerId);

    // Projection to limit fetched columns
    @Query("SELECT new com.example.dto.OrderSummary(o.id, o.status, o.total) FROM Order o WHERE o.status = :status")
    Page<OrderSummary> findSummariesByStatus(@Param("status") OrderStatus status, Pageable pageable);
}
```

## Main Application Class addition

```java
@SpringBootApplication
@EnableJpaAuditing  // required for @CreatedDate / @LastModifiedDate
public class DemoServiceApplication { ... }
```

## Quick Reference

| Concern | Guidance |
|---------|----------|
| N+1 queries | Use `JOIN FETCH` or `@EntityGraph` |
| Large result sets | Use `Page<T>` with `Pageable`; never load all rows |
| Projections | Use DTO constructor expressions or interface projections |
| Transactions | `@Transactional` on service methods, read-only on queries |
| DDL | Never use `ddl-auto: create/update` in production; use Flyway |
| `open-in-view` | Always set to `false` to avoid lazy-loading in the web layer |
