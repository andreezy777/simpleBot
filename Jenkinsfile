pipeline {
//None parameter in the agent section means that no global agent will be allocated for the entire Pipeline’s
//execution and that each stage directive must specify its own agent section.
    agent none
    stages {
        stage('Build') {
            agent {
                docker {
                    //This image parameter (of the agent section’s docker parameter) downloads the python:2-alpine
                    //Docker image and runs this image as a separate container. The Python container becomes
                    //the agent that Jenkins uses to run the Build stage of your Pipeline project.
                    image 'python:3-alpine'
                }
            }
            steps {
                //This sh step runs the Python command to compile your application and
                //its calc library into byte code files, which are placed into the sources workspace directory
                sh 'python3 -m py_compile simpleBot/*.py'
                //This stash step saves the Python source code and compiled byte code files from the sources
                //workspace directory for use in later stages.
                stash(name: 'compiled-results', includes: 'simpleBot/*.py*')
            }
        }
        stage('Deliver') {
                    agent any
                    //This environment block defines two variables which will be used later in the 'Deliver' stage.
                    environment {
                        VOLUME = '$(pwd)/sources:/src'
                        IMAGE = 'cdrx/pyinstaller-linux:python3'
                    }
                    steps {
                        //This dir step creates a new subdirectory named by the build number.
                        //The final program will be created in that directory by pyinstaller.
                        //BUILD_ID is one of the pre-defined Jenkins environment variables.
                        //This unstash step restores the Python source code and compiled byte
                        //code files (with .pyc extension) from the previously saved stash. image]
                        //and runs this image as a separate container.
                        dir(path: env.BUILD_ID) {
                            unstash(name: 'compiled-results')

                            //This sh step executes the pyinstaller command (in the PyInstaller container) on your simple Python application.
                            //This bundles your add2vals.py Python application into a single standalone executable file
                            //and outputs this file to the dist workspace directory (within the Jenkins home directory).
                            sh "docker run --rm -v ${VOLUME} ${IMAGE} 'pyinstaller -F bot.py'"
                        }
                    }
                    post {
                        success {
                            //This archiveArtifacts step archives the standalone executable file and exposes this file
                            //through the Jenkins interface.
                            archiveArtifacts "${env.BUILD_ID}/sources/dist/bot"
                            sh "docker run --rm -v ${VOLUME} ${IMAGE} 'rm -rf build dist'"
                        }
                    }
        }
    }
}