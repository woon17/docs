plugin 
dependency
config
jar
scope...

`<pluginManagement>` in parent, it declares plugin versions and config, but does not run the plugin in any module until it's declared in <plugins> of that module

## Build 

In Maven, the `<build>` tag is used in the pom.xml to configure how the project is built, including:

- Output directories
- Final artifact name
- Plugins to use (and their configuration)
- Resources to include

------------

`<plugins>` in parent

- Runs only for the parent module itself
- Child modules do not inherit these plugins or run them unless they declare their own <plugin> block

### jacoco-maven-plugin

| Goal                               | Description                                                               |
|------------------------------------|---------------------------------------------------------------------------|
| Measure code coverage            | Tracks how much of your Java code is executed during test runs            |
| Generate coverage reports        | Produces HTML, XML, and CSV reports for analysis                          |
| Enforce coverage rules           | Can fail the build if line or branch coverage is below threshold          |
| Supports unit and integration tests | Works with Surefire (unit tests) and Failsafe (integration tests)     |


```xml
<build>
<plugins>
    <plugin>
    <groupId>org.jacoco</groupId>
    <artifactId>jacoco-maven-plugin</artifactId>
    <version>0.8.11</version>
    <executions>
        <!-- Prepares coverage instrumentation -->
        <execution>
        <id>prepare-agent</id>
        <goals>
            <goal>prepare-agent</goal>
        </goals>
        </execution>

        <!-- Generates report after tests -->
        <execution>
        <id>report</id>
        <phase>prepare-package</phase>
        <goals>
            <goal>report</goal>
        </goals>
        </execution>

        <!-- Fail build if coverage is too low -->
        <execution>
        <id>check</id>
        <goals>
            <goal>check</goal>
        </goals>
        <configuration>
            <rules>
            <rule>
                <element>BUNDLE</element>
                <limits>
                <limit>
                    <counter>LINE</counter>
                    <value>COVEREDRATIO</value>
                    <minimum>0.80</minimum>
                </limit>
                <limit>
                    <counter>BRANCH</counter>
                    <value>COVEREDRATIO</value>
                    <minimum>0.70</minimum>
                </limit>
                </limits>
            </rule>
            </rules>
        </configuration>
        </execution>
    </executions>
    </plugin>
</plugins>
</build>

```

After running mvn test or mvn verify, reports are generated in:

- target/site/jacoco/index.html   (HTML report)
- target/site/jacoco/jacoco.xml   (XML for CI tools like SonarQube)

Coverage Types

| Metric  | Description                          |
|---------|--------------------------------------|
| Line    | % of lines executed                  |
| Branch  | % of control structures covered      |
| Method  | % of methods tested                  |
| Class   | % of classes touched                 |

### maven-checkstyle-plugin

| Goal                                | Description                                                                 |
|-------------------------------------|-----------------------------------------------------------------------------|
| Enforce coding standards         | Validates Java code against a defined style guide (e.g., Google, Sun, custom) |
| Ensure code consistency          | Helps teams maintain uniform formatting and structure                        |
| Catch style violations early     | Detects spacing, naming, import order, and other formatting issues           |
| Generate style violation reports | Produces HTML and XML reports for visual inspection or CI pipelines          |
| Fail builds on violations        | Prevents code with style issues from passing CI/CD or being merged           |


The `maven-checkstyle-plugin` integrates [Checkstyle](https://checkstyle.org/) into your Maven build to enforce Java coding standards and styles across your project.

---

It helps catch:

- Improper naming conventions
- Braces, spacing, line length issues
- Unused imports or fields
- Code style violations based on rules

---

```xml
<plugin>
  <groupId>org.apache.maven.plugins</groupId>
  <artifactId>maven-checkstyle-plugin</artifactId>
  <version>3.3.0</version>
  <executions>
    <execution>
      <id>validate</id>
      <phase>validate</phase>
      <goals>
        <goal>check</goal>
      </goals>
    </execution>
  </executions>
  <configuration>
    <configLocation>checkstyle.xml</configLocation>
    <suppressionsLocation>checkstyle-suppressions.xml</suppressionsLocation>
    <maxAllowedViolations>0</maxAllowedViolations>
    <propertyExpansion>
      <subpackage>com.example.project</subpackage>
      <checkstyle.cache.file>${project.build.directory}/checkstyle-cachefile</checkstyle.cache.file>
    </propertyExpansion>
    <encoding>UTF-8</encoding>
    <consoleOutput>true</consoleOutput>
    <failsOnError>true</failsOnError>
  </configuration>
</plugin>
```

---


| Tag                    | Purpose                                                                 |
|------------------------|-------------------------------------------------------------------------|
| `configLocation`       | The Checkstyle ruleset XML. Use built-in like `google_checks.xml`, or define your own. |
| `suppressionsLocation` | XML file listing rules/files to ignore. Useful for legacy files or generated code. |
| `maxAllowedViolations` | Maximum allowed rule violations before build fails (usually `0` for strict mode). |
| `propertyExpansion`    | Allows defining variables (like `subpackage`) for dynamic usage inside the Checkstyle config. |
| `encoding`             | Ensures source is read correctly (typically `UTF-8`).                   |
| `consoleOutput`        | Print violations to the console output for easy debugging.              |
| `failsOnError`         | Set `true` to fail build if violations are found.                       |

---

`propertyExpansion` Use Case: `subpackage`

This is useful for rules that match or enforce package structure.

**In POM:**
```xml
<propertyExpansion>
  <subpackage>com.mycompany.core</subpackage>
</propertyExpansion>
```

**In `checkstyle.xml`:**
```xml
<module name="RegexpPackage">
  <property name="format" value="^${subpackage}(\..+)*$"/>
</module>
```

This enforces that all classes belong to `com.mycompany.core` or subpackages.

---

Output Reports

When you run:

```bash
mvn checkstyle:checkstyle
```

You’ll get reports in:

```
target/site/checkstyle.html
target/site/checkstyle-result.xml
```

---


| Feature                | Description                                       |
|------------------------|---------------------------------------------------|
| Code Style Enforcement | Enforces consistent formatting and structure      |
| Report Generation      | Outputs HTML and XML reports                      |
| Fail-on-Violation      | Ensures CI builds fail when code violates style   |
| Configurable Rules     | Use custom or built-in rules                      |
| Suppression Support    | Ignore violations for specific classes/files      |
| Property Expansion     | Inject variables (like `subpackage`)              |


### aven-surefire-plugin

| Goal                             | Description                                                                 |
|----------------------------------|-----------------------------------------------------------------------------|
| Run unit tests                 | Executes tests written with JUnit, TestNG, or other supported frameworks    |
| Integrate with Maven lifecycle| Automatically runs tests during the `test` phase                            |
| Generate test reports         | Produces text and XML reports under `target/surefire-reports/`              |
| Detect test failures          | Fails the build if any unit test fails (configurable)                       |
| Support test customization     | Allows inclusion/exclusion patterns, parallel test execution, and filtering |

```xml
<plugin>
  <groupId>org.apache.maven.plugins</groupId>
  <artifactId>maven-surefire-plugin</artifactId>
  <version>3.0.0-M9</version>
  <configuration>
    <includes>
      <include>**/*Tests.java</include>
      <include>**/*Tests.json</include>
    </includes>
    <runOrder>alphabetical</runOrder>
    <reportsDirectory>${project.basedir}/target/surefire-reports</reportsDirectory>
    <testFailureIgnore>false</testFailureIgnore>
  </configuration>
</plugin>

```