
# define a base image and name for the build server
FROM maven AS java-builder

RUN apt-get install -y git
RUN git clone https://github.com/in28minutes/spring-boot-examples.git app
WORKDIR /app/spring-boot-web-application
RUN mvn package -Djar.finalName=test.jar -Dmaven.test.skip=true



#------------------------------------------------------

# base image - openjdk
FROM openjdk

# copy the artifact from the build container
COPY --from=java-builder /app/spring-boot-web-application/target/student-services-security-0.0.1-SNAPSHOT.jar /student-services-security-0.0.1-SNAPSHOT.jar
RUN ls /
# run the jar
ENTRYPOINT ["java","-jar","/student-services-security-0.0.1-SNAPSHOT.jar"]


