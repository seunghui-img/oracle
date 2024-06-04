FROM centos:7

ARG USER_NAME=seunghui
ARG USER_PASSWD=seunghui
ARG USER_ID=1000
ARG GROUP_ID=1000

ENV HOME=/home/$USER_NAME

USER root
RUN echo "root:root00" | chpasswd

# 사용자 계정 추가 및 sudo 권한 부여
RUN yum update -y; yum install -y sudo\
    && groupadd -g $GROUP_ID $USER_NAME\
    && useradd -l -m $USER_NAME -u $USER_ID -g $GROUP_ID -d $HOME -s /bin/bash\
    && echo "${USER_NAME} ALL=(ALL) NOPASSWD:ALL" > /etc/sudoers.d/$USER_NAME\
    && chmod 0440 /etc/sudoers.d/$USER_NAME\
    && echo "${USER_NAME}:${USER_PASSWD}" | chpasswd
    
# 사용자 전환
USER $USER_NAME
WORKDIR $HOME

# 어플리케이션 디렉터리 생성, 사용자 권한 부여 -> root 로 되어 있음
# RUN sudo mkdir -p /home/seunghui/app && sudo chmod -R 777 /home/seunghui/app

# 어플리케이션 코드 복사
# COPY --chown=$USER_NAME ./app ./app
COPY --chown=$USER_NAME instantclient-basic-linux.x64-11.2.0.4.0.zip .

# 오라클 클라이언트 인스턴스
RUN sudo yum install -y unzip libaio\
    && unzip instantclient-basic-linux.x64-11.2.0.4.0.zip -d .
ENV LD_LIBRARY_PATH ~/instantclient_11_2

# Install Anaconda
RUN sudo yum install -y wget\
    && wget https://repo.anaconda.com/archive/Anaconda3-2024.02-1-Linux-x86_64.sh\
    && bash Anaconda3-2024.02-1-Linux-x86_64.sh -b -p ./anaconda\
    && rm Anaconda3-2024.02-1-Linux-x86_64.sh

# conda activate 만 안됨
ENV PATH ~/anaconda/bin:$PATH

# # 기본 프롬프트 설정 : False
# RUN conda config --set auto_activate_base False

# ENV PATH ~/anaconda/condabin:$PATH

# RUN source ~/anaconda/etc/profile.d/conda.sh
# RUN source ~/.bashrc

# 가상환경
COPY --chown=$USER_NAME ./app/requirements.txt ./app/requirements.txt

RUN conda create -n myenv python==3.10.0 -y\
    && source activate myenv\
    # && source anaconda/bin/activate myenv\
    # && conda activate myenv\
    && pip install -r ~/app/requirements.txt

RUN echo "conda activate myenv" > ~/.bashrc

WORKDIR /home/seunghui
EXPOSE 4444
