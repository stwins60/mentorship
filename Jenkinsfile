pipeline {

    agent any

    environment {
        SCANNER_HOME = tool 'sonar-scanner'
        DOCKERHUB_CREDENTIALS = credentials('d4506f04-b98c-47db-95ce-018ceac27ba6')
    }

    stages {
        stage('Clean Workspace') {
            steps {
                cleanWs()
            }
        }
        stage('Git Checkout') {
            steps {
                git branch: 'master', url: 'https://github.com/stwins60/mentorship.git'
            }
        }
        stage('Sonarqube Analysis') {
            steps {
                script {
                    withSonarQubeEnv('sonar-server') {
                        sh "$SCANNER_HOME/bin/sonar-scanner -Dsonar.projectKey=mentorship -Dsonar.projectName=mentorship -Dsonar.sources=. -Dsonar.host.url=http://192.168.0.43:9000 -Dsonar.login=sqp_7cae4e4bc6fe05012f48ccbcf27544c46fd64318"
                    }
                }
            }
        }
        stage('Trivy File Scan') {
            steps {
                sh "trivy fs . > trivy-result.txt"
            }
        }
        stage("Docker Login") {
            steps {
                sh "echo $DOCKERHUB_CREDENTIALS_PSW | docker login -u $DOCKERHUB_CREDENTIALS_USR --password-stdin"
                echo "Login Succeeded"
            }
        }
        stage('Docker Build') {
            steps {
                sh 'docker buildx create context --name "jenkins-buildx" --use'
                sh "docker buildx build -t idrisniyi94/mentorship:latest --platform linux/amd64,linux/arm64,linux/arm/v7 ."
            }
        }
        stage('Trivy Image Scan') {
            steps {
                sh "trivy image idrisniyi94/mentorship:latest > image-scan.txt"
            }
        }
        stage('Docker Push') {
            steps {
                sh "docker push idrisniyi94/mentorship:latest"
            }
        }
        stage("Deploy to K8S") {
            steps {
                script {
                    dir('./k8s') {
                        kubeconfig(credentialsId: '500a0599-809f-4de0-a060-0fdbb6583332', serverUrl: '') {
                            sh "kubectl apply -f ."
                        }
                    }
                }
            }
        }
    }
}