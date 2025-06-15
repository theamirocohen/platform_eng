pipeline {
    agent any

    environment {
        REPO_URL = 'https://github.com/theamirocohen/platform_eng.git'
        BRANCH = 'main'
        LAMBDA_NAME = 'hello'
        EC2_USER = 'ec2-user'
        EC2_HOST = '172.31.43.89'  //ec2 private ip
        EC2_KEY = 'private-key.pem'
    }

    stages {
        stage('Checkout') {
            steps {
                git url: "${env.REPO_URL}", branch: "${env.BRANCH}"
            }
        }

        stage('Detect Changes') {
            steps {
                script {
                    def changes = sh(script: "git diff --name-only HEAD~1 HEAD", returnStdout: true).trim().split('\n')
                    echo "Changed files: ${changes}"

                    env.LAMBDA_CHANGED = changes.any { it == 'lambda/lambda_function.py' }.toString()
                }
            }
        }

        stage('Update Lambda or EC2') {
            steps {
                script {
                    if (env.LAMBDA_CHANGED == 'true') {
                        echo "lambda/lambda_function.py changed. Updating Lambda..."
                        sh """
                            zip function.zip lambda/lambda_function.py
                            aws lambda update-function-code --function-name ${env.LAMBDA_NAME} --zip-file fileb://function.zip
                        """
                    } else {
                        echo "Changes in EC2-related files. Deploying to EC2..."
                        sh """
                            chmod 600 ${env.EC2_KEY}
                            scp -i ${env.EC2_KEY} -r * ${env.EC2_USER}@${env.EC2_HOST}:/home/${env.EC2_USER}/your-app-dir
                        """
                    }
                }
            }
        }
    }
}

