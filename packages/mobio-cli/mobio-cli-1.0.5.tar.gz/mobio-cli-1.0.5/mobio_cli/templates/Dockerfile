FROM BE_BASE_COMPILE_IMAGE as compile-image

WORKDIR /home/mobio/projects/{#PROJECT_NAME_CAMEL#}
ADD . /home/mobio/projects/{#PROJECT_NAME_CAMEL#}

RUN pip3.8 install -r requirements.txt

FROM BE_BASE_RUN_IMAGE as run-image

ENV LC_ALL=en_US.UTF-8 \
   {#PROJECT_NAME_SNAKE_UPPERCASE#}_HOME=/home/mobio/projects/{#PROJECT_NAME_CAMEL#} \
   {#PROJECT_NAME_SNAKE_UPPERCASE#}_FOLDER_NAME={#PROJECT_NAME_CAMEL#} \
   APPLICATION_DATA_DIR=/media/data/resources/ \
   APPLICATION_LOGS_DIR=/media/data/logs/daily/

ENV data_dir=$APPLICATION_DATA_DIR${#PROJECT_NAME_SNAKE_UPPERCASE#}_FOLDER_NAME \
   log_dir=$APPLICATION_LOGS_DIR${#PROJECT_NAME_SNAKE_UPPERCASE#}_FOLDER_NAME \
   monitor_log_dir=$APPLICATION_LOGS_DIR${#PROJECT_NAME_SNAKE_UPPERCASE#}_FOLDER_NAME/monitor_logs/

RUN mkdir -p $data_dir $log_dir $monitor_log_dir

WORKDIR ${#PROJECT_NAME_SNAKE_UPPERCASE#}_HOME

COPY --from=compile-image ${#PROJECT_NAME_SNAKE_UPPERCASE#}_HOME ${#PROJECT_NAME_SNAKE_UPPERCASE#}_HOME

COPY --from=compile-image /usr/local/lib/python3.8/site-packages /usr/local/lib/python3.8/site-packages
COPY --from=compile-image /usr/local/bin/uwsgi /usr/local/bin/uwsgi

RUN chmod +x *.sh

CMD tail -f /dev/null