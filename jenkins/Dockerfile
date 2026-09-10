FROM jenkins/jenkins:lts-jdk17

# --- Docker CLI (copied from the official image) so pipelines can build & push images ---
COPY --from=docker:27-cli /usr/local/bin/docker /usr/local/bin/docker

# --- kubectl, for the deploy stage (Phases 1 & 3) ---
USER root
RUN curl -fsSLo /usr/local/bin/kubectl \
      "https://dl.k8s.io/release/$(curl -fsSL https://dl.k8s.io/release/stable.txt)/bin/linux/$(dpkg --print-architecture)/kubectl" \
    && chmod +x /usr/local/bin/kubectl
USER jenkins

# --- Skip the setup wizard; all configuration comes from JCasC ---
ENV JAVA_OPTS="-Djenkins.install.runSetupWizard=false"
ENV CASC_JENKINS_CONFIG=/var/jenkins_conf/casc.yaml

# --- Install the pinned plugin set ---
COPY --chown=jenkins:jenkins plugins.txt /usr/share/jenkins/ref/plugins.txt
RUN jenkins-plugin-cli --plugin-file /usr/share/jenkins/ref/plugins.txt

# --- Bake in the Configuration-as-Code file ---
COPY --chown=jenkins:jenkins casc.yaml /var/jenkins_conf/casc.yaml
