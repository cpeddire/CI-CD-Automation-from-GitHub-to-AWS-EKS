pipeline                                                 
{
        //using the agent pipeline-slv01 as a slave node
        agent { label 'pipeline-slv01' }

        stages
        {
                    
                    /*The requred dependencies are installed on the slave node from requirement.txt
                     *the python test cases will be executed in this stage
                     */
                      stage("running the pytest cases"){

                          steps{

                              sh '''
                             #curl -O https://bootstrap.pypa.io/get-pip.py
                             #python3 get-pip.py --user
                              pip3 install -r requirements.txt -t .
                              python3 -m unittest test
                              '''
                          }
                      }
                    /* In this stage, the Docker image is being created and tagged.
                   * Tests shouldn't been run in this stage, in order to speed up time to deployment.
                   */
                      stage("building docker image")
                      {
                          steps{

                              sh '''
                              docker image prune -a --force
                              BRANCH=$(echo $GIT_BRANCH|cut -d / -f 2)
                              docker build -t demo-pipeline . --no-cache
                              docker tag demo-pipeline:latest 409893854103.dkr.ecr.us-east-1.amazonaws.com/demo-pipeline:$BRANCH$BUILD_NUMBER
                              docker tag demo-pipeline:latest 409893854103.dkr.ecr.us-east-1.amazonaws.com/demo-pipeline:$BRANCH
                              '''
                          }
                      }
                    /*In this stage, the Docker image is being pushed to ecr along with the jenkins build_number tagged.
                     *using the build_number, we will define it in the deployment.yaml file in order to match the exact docker image which need to be deployed in further stages
                     */
                      stage("pushing docker image to ecr")
                      {
                          steps{

                              sh '''
                              BRANCH=$(echo $GIT_BRANCH|cut -d / -f 2)
                              aws ecr get-login-password --region us-east-1 | docker login --username AWS --password-stdin 409893854103.dkr.ecr.us-east-1.amazonaws.com
                              docker tag demo-pipeline:latest 409893854103.dkr.ecr.us-east-1.amazonaws.com/demo-pipeline:$BRANCH$BUILD_NUMBER
                              docker push 409893854103.dkr.ecr.us-east-1.amazonaws.com/demo-pipeline:$BRANCH
                              docker push 409893854103.dkr.ecr.us-east-1.amazonaws.com/demo-pipeline:$BRANCH$BUILD_NUMBER
                              '''
                          }
                      }
                     stage("deploying docker image from ecr to EKS prod environment")
                      {
                                when {
                                        expression {env.GIT_BRANCH == 'origin/master'}
                                }
                                steps{
                                        sh '''
                                        BRANCH=$(echo $GIT_BRANCH|cut -d / -f 2)
                                        kubectl apply -f deployment-scripts/prod_deployment/deployment.yaml
                                        kubectl set image deployment/helloworld-application hello-world=409893854103.dkr.ecr.us-east-1.amazonaws.com/demo-pipeline:$BRANCH$BUILD_NUMBER -n prod 
                                       #kubectl apply -f deployment-scripts/prod_deployment/ingress-helloprod.yaml
                                       #kubectl apply -f deployment-scripts/nlb-provisioner.yaml
                                        '''
                                }

                        }
                      stage("deploying docker image from ecr to test and uat eks environments")
                      {
                                when {
                                            expression {env.GIT_BRANCH == 'origin/release'}
                                        }
                                        steps{
                                        sh '''
                                        BRANCH=$(echo $GIT_BRANCH|cut -d / -f 2)
                                        kubectl apply -f deployment-scripts/test_deployment/deployment_release_test.yaml
                                        kubectl set image deployment/helloworld-application hello-world=409893854103.dkr.ecr.us-east-1.amazonaws.com/demo-pipeline:$BRANCH$BUILD_NUMBER -n test 
                                       #kubectl apply -f deployment-scripts/test_deployment/ingress-hellotest.yaml
                                       #kubectl apply -f deployment-scripts/nlb-provisioner.yaml
                                        '''
                                        sh '''
                                        BRANCH=$(echo $GIT_BRANCH|cut -d / -f 2)
                                        kubectl apply -f deployment-scripts/uat_deployment/deployment_release_uat.yaml
                                        kubectl set image deployment/helloworld-application hello-world=409893854103.dkr.ecr.us-east-1.amazonaws.com/demo-pipeline:$BRANCH$BUILD_NUMBER -n uat 
                                       #kubectl apply -f deployment-scripts/uat_deployment/ingress-hellouat.yaml
                                       #kubectl apply -f deployment-scripts/nlb-provisioner.yaml
                                        '''
                                        }
                                        
                
                     }
                      stage("deploying docker image from ecr to eks dev environment")
                      {
                                when {
                                    expression {env.GIT_BRANCH == 'origin/develop'}
                                }
                                steps{
                                    sh '''
                                        BRANCH=$(echo $GIT_BRANCH|cut -d / -f 2)
                                        kubectl apply -f deployment-scripts/dev_deployment/deployment_dev.yaml
                                        kubectl set image deployment/helloworld-application hello-world=409893854103.dkr.ecr.us-east-1.amazonaws.com/demo-pipeline:$BRANCH$BUILD_NUMBER -n dev 
                                       #kubectl apply -f deployment-scripts/dev_deployment/ingress-hellodev.yaml
                                       #kubectl apply -f deployment-scripts/nlb-provisioner.yaml
                                        '''
                                }
                
                     }

           

      }
        
    
}
