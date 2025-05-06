pipeline{
    agent any
    environment{
        DOCKER_USERNAME = "priyam930"
        APP_NAME = "flask-app"
        IMAGE_TAG = "${BUILD_NUMBER}"
        IMAGE_NAME = "${DOCKER_USERNAME}/${APP_NAME}"


    }


    stages{
        stage('clean the workspace'){
            steps{
                script{
                    cleanWs()
                }
            }
        }

        stage('checkout git scm'){
            steps{
                git branch: 'main', url: 'https://github.com/priyam930/Flask_App_Cricbuzz_API.git'
            }
        }

        stage('build docker image'){
            steps{
                script{
                    sh "docker build -t ${IMAGE_NAME}:${IMAGE_TAG} ."
                }
            }
        }
        stage('Push the Image to DockerHub') {


            steps {
              withCredentials([usernamePassword(credentialsId: 'Dockercred', passwordVariable: 'pass', usernameVariable: 'user')]) {
                // some block


                    sh """
                    
                        echo ${pass} | docker login -u ${user} --password-stdin

                        docker push ${IMAGE_NAME}:"${IMAGE_TAG}"
                      


                    """
            }
            }

        }
        stage('Delete Image Locally') {

            steps {
                sh """
                    docker rmi -f ${IMAGE_NAME}:${IMAGE_TAG}
                   
                """

            }

            
        }
         stage('Update the deployment file in CD') {

            steps {
                script{
                    withCredentials([usernamePassword(credentialsId: 'gitcred', usernameVariable: 'user', passwordVariable: 'pass')]) {

                        sh """
                            git clone -b main https://${user}:${pass}@github.com/priyam930/Flask_App_Cricbuzz_CD.git
                            cd Flask_App_Cricbuzz_CD

                            ls
                            cat deployment.yaml
                

                        """

                        sh """
                            echo "new shell"
                            echo $pwd
                            cd  Flask_App_Cricbuzz_CD
                            echo $pwd

                            ls

                            cat deployment.yaml

                            echo "Changing tag to ${BUILD_NUMBER}"

                            sed -i 's|image: priyam930/flask-app:.*|image: ${IMAGE_NAME}:${BUILD_NUMBER}|g' deployment.yaml

                            echo "changed tag"

                            cat deployment.yaml


                            git add deployment.yaml
                            git commit -m "Updated the tag to ${BUILD_NUMBER}"
                            git push origin main

                        """

                    }

                }
            }
        }
    }
}
