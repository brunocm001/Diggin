@Library("societe1-dsl@master") _

pipeline {
    agent any
    environment {
        APP_NAME = 'Diggin'
        PATH_REPORTS = 'Digging'
        PYTHONPATH= "${env.WORKSPACE}/src:${env.WORKSPACE}"
    }
    post {
        failure {
            updateGitlabCommitStatus name: 'build', state: 'failed'
        }
        success {
            updateGitlabCommitStatus name: 'build', state: 'success'
        }
        unstable {
            updateGitlabCommitStatus name: 'build', state: 'failed'
        }
    }

    stages {
        stage('Checkout') {
            steps {
                initialize(APP_NAME)
                checkout scm
                script {
                    currentBuild.displayName = "${currentBuild.displayName}-${params.ENVIRONMENT}"
                }
                loadEnvironmentVariables("conf/env/${params.ENVIRONMENT}.env")
            }
        }

        stage("Build") {
            when { expression { params.BUILD } }
            steps {
                sh "mkdir -p $PATH_REPORTS"
                sh 'pip3.8 install setuptools --upgrade'
                sh 'pip3.8 install --quiet .[app,tests,syntax]'
                sh 'pip3.8 freeze'
            }

        }

        stage('Continuous Integration') {
            when { expression { params.BUILD } }
            steps {
                parallel(
                    'Linter': {
                        catchError(buildResult: 'UNSTABLE', stageResult: 'UNSTABLE') {
                            sh "pylint --rcfile=./setup.cfg --exit-zero --score=no --reports=no \
                            --suggestion-mode=no  --output-format=text \
                            --msg-template=\"{path}:{line}: [{msg_id}({symbol}), {obj}] {msg}\" ./files ./tests > $PATH_REPORTS/pylint.txt"
                            sh 'pylint-fail-under --fail_under 7 --rcfile=./setup.cfg --output-format=text ./src'
                            echo 'Linter Report Generated'
                        }
                    },
                    'Unit Test': {
                        sh 'pytest --no-cov --color=no --cov-config=./setup.cfg'
                        echo 'Units Tests Finished'
                    },
                    'Coverage': {
                        catchError(buildResult: 'UNSTABLE', stageResult: 'UNSTABLE') {
                            sh 'pytest --quiet --verbosity=0 --color=no --cov  --cov-fail-under=80\
                            --cov-config=./setup.cfg --cov-report xml:$PATH_REPORTS/coverage.xml'
                            echo 'Coverage and Tests Reports Generated'
                        }
                    },
                    'Sonar': {
                        waitUntil {
                            fileExists "$PATH_REPORTS/coverage.xml"
                        }
                        waitUntil {
                            fileExists "$PATH_REPORTS/pylint.txt"
                        }
                        sonarize(APP_NAME)
                        echo 'Test sonar finished'
                    }
                )
            }
        }

    }
}


def loadEnvironmentVariables(path){
     def props = readProperties file:path
     keys = props.keySet()
     for (key in keys) {
        value = props["${key}"]
        env."${key}" = "${value}"
     }
}
