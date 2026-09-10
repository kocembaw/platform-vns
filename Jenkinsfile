// Thin declarative pipeline — each stage just calls a script in ci/.
// Mirrors the CI/CD diagram in README.md: test -> build -> deploy.

pipeline {
    agent any

    options {
        timestamps()
        disableConcurrentBuilds()
    }

    environment {
        // ci/*.sh derive IMAGE_TAG from the git SHA when unset.
        AWS_REGION = 'eu-central-1'
        // For AWS deploys, set REGISTRY (the ECR host) here or as a Jenkins
        // environment variable, and give the agent kubeconfig + AWS credentials:
        // REGISTRY = '<acct>.dkr.ecr.eu-central-1.amazonaws.com'
    }

    stages {
        stage('Test') {
            steps {
                sh 'bash ci/test.sh'
            }
        }

        stage('Build') {
            steps {
                sh 'bash ci/build.sh'
            }
        }

        stage('Deploy') {
            steps {
                sh 'bash ci/deploy.sh'
            }
        }
    }

    post {
        success {
            echo 'Deployment succeeded.'
        }
        failure {
            echo 'Build failed — notify developer (see the stage logs above).'
        }
    }
}
