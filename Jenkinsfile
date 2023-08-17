def appName = 'roberta'
def deployGroup = 'roberta-backend'
def s3Bucket = 'roberta-ml'
def s3FileName = 'roberta-backend'

pipeline {
    agent any

    tools {
        // Adding NodeJS Tool to help with installation of packages
        nodejs 'nodejs'
    }
    environment {
        // Referencing DockerHub Credentials from the Jenkins credentials
        DOCKERHUB_CREDENTIALS = credentials('dockerhub')
    }

    stages {
        stage('Build Docker Image') {
            // Restricting branch to 'main'
            when {
                branch 'main'
            }
            steps {
                withCredentials([file(credentialsId: 'env', variable: 'frontendEnvFile')]) {
                    sh 'cp $frontendEnvFile .env'
                    sh 'docker build -t calebackom/roberta-api .'
                }
            }
        }

        stage('Login') {
            // Restricting branch to 'main'
            when {
                branch 'main'
            }
            steps {
                script {
                    sh 'echo $DOCKERHUB_CREDENTIALS_PSW | docker login -u $DOCKERHUB_CREDENTIALS_USR --password-stdin'
                }
            }
        }

        stage('Push to Docker Hub') {
            // Restricting branch to 'main'
            when {
                branch 'main'
            }
            steps {
                script {
                    sh 'docker push calebackom/roberta-api'
                }
            }
        }

        stage('Prepare to Deploy') {
            when {
                branch 'main'
            }
            steps {
                withAWS(region:'eu-west-1',credentials:'aws-credential') {
                    script {
                        def gitSha = sh(
                            script: 'git log -n1 --format=format:"%H"',
                            returnStdout: true
                        )
                        s3FileName = "${s3FileName}-${gitSha}"
                        echo s3FileName
                        echo appName
                        sh """
                            aws deploy push \
                            --application-name ${appName} \
                            --description "This is a revision for ${appName}-${gitSha}" \
                            --ignore-hidden-files \
                            --s3-location s3://${s3Bucket}/${s3FileName}.zip \
                            --source ./deploy-scripts
                        """
                    }
                }
            }
        }

        stage('Deploy to Environment') {
            when {
                branch 'main'
            }
            steps {
                withAWS(region:'eu-west-1',credentials:'aws-credential') {
                    script {
                        sh """
                            aws deploy create-deployment \
                            --application-name ${appName} \
                            --deployment-config-name CodeDeployDefault.OneAtATime \
                            --deployment-group-name ${deployGroup} \
                            --file-exists-behavior OVERWRITE \
                            --s3-location bucket=${s3Bucket},key=${s3FileName}.zip,bundleType=zip
                        """
                    }
                }
            }
        }
    }

    post {
        always {
            sh 'docker logout'
        }
    }
}