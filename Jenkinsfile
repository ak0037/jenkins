node {
  def GITREPOREMOTE = "https://github.com/ak0037/jenkins.git"
  def GITBRANCH     = "main"
  def DBCLIPATH     = "/usr/local/bin"
  def JQPATH        = "/usr/bin"
  def JOBPREFIX     = "jenkins-demo"
  def BUNDLETARGET  = "dev"
  def VENV_PATH     = "/var/lib/jenkins/databricks-env"

  stage('Checkout') {
    checkout([$class: 'GitSCM',
      branches: [[name: GITBRANCH]],
      userRemoteConfigs: [[
        url: GITREPOREMOTE,
        credentialsId: 'github-pat'
      ]]
    ])
  }

  stage('Setup Environment') {
    sh """#!/bin/bash
          # Activate virtual environment
          source ${VENV_PATH}/bin/activate
          
          # Install required packages
          pip install wheel pytest unittest-xml-reporting
       """
  }

  stage('Validate Bundle') {
    sh """#!/bin/bash
          source ${VENV_PATH}/bin/activate
          ${DBCLIPATH}/databricks bundle validate -t ${BUNDLETARGET}
       """
  }

  stage('Deploy Bundle') {
    sh """#!/bin/bash
          source ${VENV_PATH}/bin/activate
          ${DBCLIPATH}/databricks bundle deploy -t ${BUNDLETARGET}
       """
  }

  stage('Verify Workspace') {
    def workspacePath = sh(
      script: "${DBCLIPATH}/databricks bundle validate -t ${BUNDLETARGET} | grep 'Path:' | awk '{print \$2}'",
      returnStdout: true
    ).trim()
    
    sh """#!/bin/bash
          source ${VENV_PATH}/bin/activate
          echo "Workspace Path: ${workspacePath}"
          ${DBCLIPATH}/databricks workspace ls ${workspacePath}
          
          # Print bundle validation details
          ${DBCLIPATH}/databricks bundle validate -t ${BUNDLETARGET} --verbose
       """
  }

  stage('Run Unit Tests') {
    sh """#!/bin/bash
          source ${VENV_PATH}/bin/activate
          ${DBCLIPATH}/databricks bundle run -t ${BUNDLETARGET} run-unit-tests
       """
  }

  stage('Run Notebook') {
    sh """#!/bin/bash
          source ${VENV_PATH}/bin/activate
          ${DBCLIPATH}/databricks bundle run -t ${BUNDLETARGET} run-dabdemo-notebook
       """
  }

  stage('Evaluate Notebook Runs') {
    sh """#!/bin/bash
          source ${VENV_PATH}/bin/activate
          ${DBCLIPATH}/databricks bundle run -t ${BUNDLETARGET} evaluate-notebook-runs
       """
  }

  stage('Import Test Results') {
    def DATABRICKS_BUNDLE_WORKSPACE_ROOT_PATH
    def getPath = "${DBCLIPATH}/databricks bundle validate -t ${BUNDLETARGET} | ${JQPATH}/jq -r .workspace.file_path"
    def output = sh(script: getPath, returnStdout: true).trim()

    if (output) {
      DATABRICKS_BUNDLE_WORKSPACE_ROOT_PATH = "${output}"
    } else {
      error "Failed to capture output or command execution failed: ${getPath}"
    }

    sh """#!/bin/bash
          source ${VENV_PATH}/bin/activate
          ${DBCLIPATH}/databricks workspace export-dir \
          ${DATABRICKS_BUNDLE_WORKSPACE_ROOT_PATH}/Validation/Output/test-results \
          ${WORKSPACE}/Validation/Output/test-results \
          -t ${BUNDLETARGET} \
          --overwrite
       """
  }

  stage('Publish Test Results') {
    junit allowEmptyResults: true, testResults: '**/test-results/*.xml', skipPublishingChecks: true
  }
}