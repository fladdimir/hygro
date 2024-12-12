FROM maven:3-eclipse-temurin-24-alpine AS build
WORKDIR /usr/src/mymaven
# download dependencies
COPY pom.xml /usr/src/mymaven
RUN mvn dependency:resolve -DexcludeTransitive=false
# compile fat jar
COPY ./src /usr/src/mymaven/src
RUN mvn package -DskipTests

FROM eclipse-temurin:24
EXPOSE 3002
RUN mkdir /app
COPY --from=build /usr/src/mymaven/target/*.jar /app/app.jar
CMD ["java", "-jar", "/app/app.jar", "-Xmx2g"]
