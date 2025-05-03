pipeline {
    
    agent {
        label "build-system"
    }
    
    stages {
        stage("Checkout From Git") {
            steps {
                git branch: 'main', url: 'https://github.com/priyam930/Deploy-FlaskApp-CICD.git'
            }
        }
        
        stage("Building Docker Image") {
            steps {
                script {
                    sh "sudo docker build -t priyam930/flask-app:${BUILD_NUMBER} ."
                }
            }
        }
        
        stage("Testing Environnment"){
            steps{
                sh "sudo docker run -dit --name TestingApp-${BUILD_NUMBER} -p ${BUILD_NUMBER}:8080  kanha05/flask-app:${BUILD_NUMBER}"
                retry(30){
                    sh "curl http://localhost:${BUILD_NUMBER}/ "
                }
            }
        }
        
        stage("Testing"){
            steps{
                retry(30){
                    sh "curl http://localhost:${BUILD_NUMBER}/ "
                }
            }
        }
        
        stage("Approving"){
            steps{
                script{
                    Boolean userInput = input(id: 'Proceed1', message: 'Ready To Go?', parameters: [[$class: 'BooleanParameterDefinition', defaultValue: true, description: '', name: 'Please confirm you agree with this']])
                    echo 'userInput: ' + userInput
                    if(userInput == true){
                        // do action
                    } else {
                        // not do action
                        echo "Action was aborted."
                    }
                }
            }
        }
        
        stage ("Pushing To Dockerhub"){
            steps{
                withCredentials([string(credentialsId: 'DockerHub', variable: 'passwd')]){
                    sh "sudo docker login -u priyam930 -p $passwd "
                    sh "sudo docker push priyam930/flask-app:${BUILD_NUMBER}"
                }
            }
        }
        
        stage("Deploying On Kubernetes"){
           steps {
                script {
                    // Replace the image tag in the deployment file
                    sh "sed -i 's/replaceImageTag/${BUILD_NUMBER}/g' deployment.yaml"
        
                    // Apply Kubernetes manifests inside Minikube
                    sh "kubectl apply -f deployment.yaml"
                    sh "kubectl apply -f service.yaml"
        
                    // Optional: show the deployment status
                    sh "kubectl get pods"
                    sh "kubectl get svc"
                }
            }
     
        }
    }
}
