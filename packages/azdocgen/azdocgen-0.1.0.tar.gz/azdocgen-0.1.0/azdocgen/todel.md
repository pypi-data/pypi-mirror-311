# Azure Pipeline Documentation

## Triggers

Branches: main

Tags Include: 

## Variables


## Resources

- Repository: `templates` (ref: `default`)

## Stages

- **BuildStage** (Build Stage)

  - **Job: Build the Application**
    - Steps:
      - template: ... _build-app.yml_
      - template: ... _publish-app.yml_
      - Step 3
      - echo Test code
  - **Job: Run Tests**
    - Steps:
      - Run Unit Tests

## Workflow Diagram

```mermaid
graph TD
classDef stage color:#020ef9;
classDef job color:#FF1493;
BuildStage["Build Stage"]:::stage
BuildStage --> BuildStage_Build_the_Application["Build the Application"]:::job
BuildStage_Build_the_Application_template____build_appyml_["template:  _build-appyml_"]:::step
BuildStage_Build_the_Application --> BuildStage_Build_the_Application_template____build_appyml_
BuildStage_Build_the_Application_template____publish_appyml_["template:  _publish-appyml_"]:::step
BuildStage_Build_the_Application_template____build_appyml_ --> BuildStage_Build_the_Application_template____publish_appyml_
BuildStage_Build_the_Application_Step_3["Step 3"]:::step
BuildStage_Build_the_Application_template____publish_appyml_ --> BuildStage_Build_the_Application_Step_3
BuildStage_Build_the_Application_echo_Test_code["echo Test code"]:::step
BuildStage_Build_the_Application_Step_3 --> BuildStage_Build_the_Application_echo_Test_code
BuildStage --> BuildStage_Run_Tests["Run Tests"]:::job
BuildStage_Run_Tests_Run_Unit_Tests["Run Unit Tests"]:::step
BuildStage_Run_Tests --> BuildStage_Run_Tests_Run_Unit_Tests
```
