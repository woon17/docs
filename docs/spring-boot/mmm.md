# Spring Boot Multi-Module Maven Project

key concepts and configuration examples for setting up a multi-module Maven project using Spring Boot.

---

## Parent POM

Provides consistent versions of dependencies across modules.

A central `pom.xml` with `<packaging>pom</packaging>` used to manage modules and shared configuration.

- Declares `<modules>` for all child projects.
- Centralizes dependency and plugin management.
- Entry point for `mvn install` or CI builds.


---

## BOM (Bill of Materials)

=== "Parent POM"

    do use the Spring Boot parent POM:
      ```xml
      <parent>
         <groupId>org.springframework.boot</groupId>
         <artifactId>spring-boot-starter-parent</artifactId>
         <version>3.2.5</version>
      </parent>
      
      ```

=== "Manually"
    If not using the Spring Boot parent, then you must import the Spring BOM manually like this:
      ```xml
      <dependencyManagement>
         <dependencies>
            <dependency>
               <groupId>org.springframework.boot</groupId>
               <artifactId>spring-boot-dependencies</artifactId>
               <version>3.2.5</version>
               <type>pom</type>
               <scope>import</scope>
            </dependency>
         </dependencies>
      </dependencyManagement>

      ```
      This snippet must go inside your parent POM's <dependencyManagement> block if not using the spring-boot-starter-parent.

This ensures children can declare dependencies without specifying versions.

---

## Dependency Management

Define shared dependency versions in the parent:

```xml
<properties>
  <lombok.version>1.18.30</lombok.version>
</properties>

<dependencyManagement>
  <dependencies>
    <dependency>
      <groupId>org.projectlombok</groupId>
      <artifactId>lombok</artifactId>
      <version>${lombok.version}</version>
      <scope>provided</scope>
    </dependency>
  </dependencies>
</dependencyManagement>
```

---

## Plugin Management

Ensure consistent plugin versions and configuration:

```xml
<pluginManagement>
  <plugins>
    <plugin>
      <groupId>org.apache.maven.plugins</groupId>
      <artifactId>maven-compiler-plugin</artifactId>
      <version>3.11.0</version>
      <configuration>
        <source>17</source>
        <target>17</target>
      </configuration>
    </plugin>
  </plugins>
</pluginManagement>
```

---

## Child Module (e.g., `service-a`)

Each module has its own `pom.xml` and inherits from the parent.

```xml
<parent>
  <groupId>com.example</groupId>
  <artifactId>parent-project</artifactId>
  <version>1.0.0-SNAPSHOT</version>
  <relativePath>../pom.xml</relativePath>
</parent>

<dependencies>
   <dependency>
   <groupId>org.projectlombok</groupId>
   <artifactId>lombok</artifactId>
   </dependency>
</dependencies>
```

Define module-specific dependencies under `<dependencies>`.

---

## Benefits of This Setup

| Benefit                   | Why it Matters                                      |
|--------------------------|-----------------------------------------------------|
| Version Consistency      | Prevents conflicts across modules                   |
| Central Plugin Control   | Reduces repetition and errors                       |
| Scalable Design          | Suitable for microservices or layered apps         |
| Easier CI/CD Integration | One entry point for Maven build commands           |

---

This structure allows for clean, maintainable, and scalable Spring Boot applications using Maven.
