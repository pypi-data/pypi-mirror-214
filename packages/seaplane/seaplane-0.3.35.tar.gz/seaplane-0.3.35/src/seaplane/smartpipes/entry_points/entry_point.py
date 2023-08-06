import asyncio
import functools
import json
import os
import sys
import traceback
import uuid

from typing import Any, List, Optional

from flask import Flask, request, jsonify
from flask_cors import CORS
from flask_socketio import SocketIO, emit
import nats

from ..datasource import RequestDataSource
from ...carrier import processor
from ...configuration import config
from ...logging import log
from ...model.errors import SeaplaneError
from ..build import build
from ..decorators import context, smart_pipes_json
from ..deploy import deploy, destroy
from ..smartpipe import SmartPipe
from .request import is_valid_body, is_batch_processing

SMARTPIPES_CORS = list(os.getenv("SMARTPIPES_CORS", "http://localhost:3000").split(" "))
AUTH_TOKEN = os.getenv("SMARTPIPES_AUTH_TOKEN")

app = Flask(__name__)

CORS(app, origins=SMARTPIPES_CORS)

if not config.is_production():

    sio = SocketIO(app, cors_allowed_origins=SMARTPIPES_CORS, async_mode="threading")

    @sio.on("message")  # type: ignore
    def handle_message(data: Any) -> None:
        ...


    @sio.on("connect")  # type: ignore
    def on_connect() -> None:
        emit("message", smart_pipes_json(context.smart_pipes))


def send_something(data: Any) -> None:
    emit("message", data, sid="sp", namespace="", broadcast=True)


def authenticate_token() -> bool:
    token = request.headers.get("Authorization")
    if token and token.startswith("Bearer "):

        if token == f"Bearer {AUTH_TOKEN}":
            return True

    return False


@app.before_request
def before_request() -> Any:
    if request.path == "/healthz":
        return

    if os.getenv("SMARTPIPES_AUTH_TOKEN") is not None:
        if not authenticate_token():
            return {"message": "Unauthorized"}, 401


def dev_https_api_start() -> Flask:
    log.debug(f"CORS enabled: {SMARTPIPES_CORS}")
    context.set_event(lambda data: send_something(data))

    smart_pipes = context.smart_pipes

    for smart_pipe in smart_pipes:

        def endpoint_func(pipe: SmartPipe = smart_pipe) -> Any:
            if request.method == "POST" or request.method == "PUT":
                data = request.get_json()
                result = pipe.func(data)
                return result
            elif request.method == "GET":
                return pipe.func("nothing")  # current limitation, it needs to pass something

        endpoint = functools.partial(endpoint_func, pipe=smart_pipe)
        app.add_url_rule(smart_pipe.path, smart_pipe.id, endpoint, methods=[smart_pipe.method])
        

    def health() -> str:
        emit("message", {"data": "test"}, sid="lol", namespace="", broadcast=True)
        return "Seaplane SmartPipes Demo"

    app.add_url_rule("/", "healthz", health, methods=["GET"])

    if not config.is_production():
        log.info("🚀 Smart Pipes DEVELOPMENT MODE")
        sio.run(app, debug=False, port=1337)
    else:
        log.info("🚀 Smart Pipes PRODUCTION MODE")

    return app


loop = asyncio.get_event_loop()


async def publish_message(stream: str, id: str, message: Any, order: int, coprocessors: List[str]) -> None:
    nc = await nats.connect(
        ["nats://148.163.201.1:2003"],
        user_credentials=os.path.abspath("./carrier.creds"),
    )
    js = nc.jetstream()

    nats_message = { "id": id, "input": message, "order": order }

    for coprocessor in coprocessors:
        log.debug(f"Sending to {stream}.{coprocessor} coprocessor,  message: {nats_message}")
        ack = await js.publish(f"{stream}.{coprocessor}", str(json.dumps(nats_message)).encode())
        log.debug(f"ACK: {ack}")

    await nc.close()


def generate_id():
    random_id = str(uuid.uuid4())
    return random_id

def build_requests_datasource():
    database = os.getenv("SEAPLANE_REQUESTS_DATABASE", None)
    host = os.getenv("SEAPLANE_REQUESTS_HOST", None)
    username = os.getenv("SEAPLANE_REQUESTS_USERNAME", None)
    password = os.getenv("SEAPLANE_REQUESTS_PASSWORD", None)
    port = os.getenv("SEAPLANE_REQUESTS_PORT", None)    
    return RequestDataSource(database=database, host=host, username=username, password=password, port=port)


def prod_https_api_start() -> Flask:
    log.debug(f"CORS enabled: {SMARTPIPES_CORS}")

    schema = build()
    context.set_event(lambda data: send_something(data))        
    requests_datasource = build_requests_datasource()

    smart_pipes = context.smart_pipes

    for smart_pipe in smart_pipes:

        def endpoint_func(pipe: SmartPipe = smart_pipe) -> Any:            
            if request.method == "POST" or request.method == "PUT":
                body = request.get_json()

                if not is_valid_body(body):
                    return jsonify({"error": "Invalid JSON"}), 401

                id = generate_id()
                smart_pipe_first_coprocessors = schema["smartpipes"][pipe.id]["io"]["entry_point"]
                metadata = body["metadata"]

                if is_batch_processing(body):
                    batch = body["batch"]                    

                    for idx, individual in enumerate(batch):
                        message = {"_id": id, "content": individual, "metadata": metadata}
                        loop.run_until_complete(
                            publish_message(pipe.id, id, message, idx, smart_pipe_first_coprocessors)
                        )
                                        
                    requests_datasource.save_request(id, len(batch))
                else:
                    message = {"id": id, "content": body["content"], "metadata": metadata}
                    loop.run_until_complete(
                        publish_message(pipe.id, id, message, 0, smart_pipe_first_coprocessors)
                    )
                    requests_datasource.save_request(id, 0)

                return jsonify({"id": id, "status": "processing"}), 200
            elif request.method == "GET":
                return pipe.func("nothing")  # current limitation, it needs to pass something
        
        def get_result() -> Any:            
            id = request.view_args['id']            

            if not id:
                return jsonify({"error": "Missing Request ID"}), 401
            
            output = None
            req_status = requests_datasource.get_results_from_request(id)
            batch_count = req_status["batch_count"]
            result_count = ["result_count"]

            if batch_count != result_count:
                status = f"{result_count}/{batch_count}"
            else:
                status = "completed"
            
            return jsonify({"id": id, "status": status, "output": output}), 200

        endpoint = functools.partial(endpoint_func, pipe=smart_pipe)
        app.add_url_rule(smart_pipe.path, smart_pipe.id, endpoint, methods=[smart_pipe.method])
        app.add_url_rule(f"{smart_pipe.path}/<id>", f"{smart_pipe.id}_query", get_result, methods=["GET"])

    def health() -> str:
        return "Seaplane SmartPipes Demo"

    app.add_url_rule("/", "healthz", health, methods=["GET"])

    if not config.is_production():
        log.info("🚀 Smart Pipes DEVELOPMENT MODE")
        sio.run(app, debug=False, port=1337)
    else:
        log.info("🚀 Smart Pipes PRODUCTION MODE")

    return app


def start_coprocessor(coprocessor_id: str, save_result: bool) -> None:
    coprocessor = context.get_coprocessor(coprocessor_id)

    if not coprocessor:
        raise SeaplaneError(
            f"Coprocessor {coprocessor_id} not found, \
                            make sure the Coprocessor ID is correct."
        )

    processor.start()

    requests_datasource = None
    if save_result:
        requests_datasource = build_requests_datasource()

    while True:
        try:
            log.info(f" Coprocessor {coprocessor.id}  waiting for getting data...")
            message = json.loads(processor.read())
            log.debug(f" Message recieved: {message}")

            id = message["id"]
            order = message["order"]

            message["output"] = coprocessor.process(message["input"])

            log.debug(f" Coprocessor Result: {message}")

            next_message = {"input": message["output"], "id": id, "order": order}
            processor.write(str(json.dumps(next_message)).encode())

            if requests_datasource:
                requests_datasource.save_result(id, order, message["output"])

        except Exception as e:
            log.error(
                f"Error running Coprocessor:\
                      \n {traceback.format_exception(type(e), e, e.__traceback__)}"
            )


def start() -> Optional[Flask]:
    if len(sys.argv) > 1:
        command = sys.argv[1]

        if command == "build":
            build()
            return None
        elif command == "deploy":
            if len(sys.argv) == 3:
                co_id = sys.argv[2]
                deploy(co_id)
            else:
                deploy()
            return None
        elif command == "destroy":
            destroy()
            return None

    coprocessor_id: Optional[str] = os.getenv("COPROCESSOR_ID")

    if not coprocessor_id:
        log.info("Starting API Entry Point...")
        if not config.is_production():
            return dev_https_api_start()
        else:
            return prod_https_api_start()
    else:
        log.info(f"Starting Coprocessor {coprocessor_id} ...")                    
        save_result = os.getenv("SAVE_RESULT_COPROCESSOR")
        start_coprocessor(coprocessor_id, save_result)
        return None
