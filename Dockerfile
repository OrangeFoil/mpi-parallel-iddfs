FROM debian:9
# install dependencies
ENV DEBIAN_FRONTEND=noninteractive
RUN apt-get update && apt-get install -y dropbear mpi-default-bin mpi-default-dev openssh-client python3-mpi4py passwd

# for passwordless login we simply remove the root password :)
RUN passwd -d root

# compile our MPI application
COPY source/ /root/
WORKDIR /root

# expose port 22 and start lightweight ssh server by default
EXPOSE 22
CMD dropbear -F -B -R
