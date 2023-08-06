import typer
from typing_extensions import Annotated
from rich.console import Console

import socket
from foreverbull.broker.models.socket import Request, SocketConfig, SocketType
from foreverbull.worker import WorkerPool
from foreverbull import Foreverbull
from foreverbull import broker
from foreverbull.broker.socket.client import SocketClient
from foreverbull.models import Configuration
import importlib
import time
import os
import signal

strategy_option = Annotated[str, typer.Option(help="strategy to run")]
broker_url_option = Annotated[str, typer.Option(help="broker to use")]
file_name_argument = Annotated[str, typer.Argument(help="file name")]
local_host_option = Annotated[str, typer.Option(help="local host")]
local_port_option = Annotated[str, typer.Option(help="local port")]

local_hostname = socket.gethostbyname(socket.gethostname())

cli = typer.Typer()

algo = typer.Typer()
cli.add_typer(algo, name="algo")

std = Console()
std_err = Console(stderr=True)


def import_algo(file_name: str):
    try:
        importlib.import_module(file_name.replace("/", ".").split(".py")[0])
    except Exception as e:
        std_err.log(f"Could not import {file_name}: {e}")
        exit(1)


@algo.command()
def run(
    file_name: file_name_argument,
    strategy: strategy_option = None,
    broker_url: broker_url_option = "127.0.0.1:8080",
    local_host: local_host_option = local_hostname,
    local_port: local_port_option = 27015,
):
    std.rule("Setting up environment")

    import_algo(file_name)

    worker_pool = WorkerPool(**Foreverbull._worker_routes)
    worker_pool.setup()
    socket_config = SocketConfig(host=local_host, port=5555)
    fb = Foreverbull(socket_config, worker_pool)

    # TODO: check if we can reach the broker and if import is OK
    std.print("default: ", fb._default_strategy)

    std.rule("Getting Strategy")
    if strategy:
        try:
            stored_strategy = broker.strategy.get(strategy)
        except Exception:
            std_err.log(f"Could not get strategy {strategy}")
            stored_strategy = None

    if not strategy and fb._default_strategy:
        try:
            stored_strategy = broker.strategy.get(fb._default_strategy.name)
        except Exception:
            std_err.log(f"Could not get strategy {fb._default_strategy.name}, trying to create")
            std.log("ingesting assets")
            broker.finance.create_assets(fb._default_strategy.symbols)
            std.log("ingesting ohlc")
            broker.finance.create_ohlc(
                fb._default_strategy.symbols, fb._default_strategy.start, fb._default_strategy.end
            )
            std.log("registering backtest service")
            broker.service.create(fb._default_strategy.backtest_service, fb._default_strategy.backtest_service_image)
            backtest_config = {
                "symbols": fb._default_strategy.symbols,
                "start_time": fb._default_strategy.start.isoformat(),
                "end_time": fb._default_strategy.end.isoformat(),
                "calendar": fb._default_strategy.calendar,
                "benchmark": fb._default_strategy.benchmark,
            }
            std.log("creating strategy")
            broker.strategy.create(
                name=fb._default_strategy.name,
                worker="worker",
                backtest=fb._default_strategy.backtest_service,
                backtest_config=backtest_config,
            )
            stored_strategy = broker.strategy.get(fb._default_strategy.name)

    if not strategy and not fb._default_strategy:
        std_err.log("No strategy specified, exiting..")
        return

    std.log("strategy: ", strategy)
    with std.status("Execution.."):
        try:
            fb.start()
            while not broker.socket_config.port:
                time.sleep(0.1)
            std.log("starting manual backtest execution")
            backtest = broker.backtest.run(stored_strategy["name"])
            std.log("waiting for engine to be running...")
            while backtest["stage"] != "RUNNING":
                if backtest["error"]:
                    std_err.log("backtest failed to start: ", backtest["error"])
                    return
                time.sleep(0.2)
                backtest = broker.backtest.get(backtest["id"])
            socket_config = SocketConfig(
                host="127.0.0.1",
                port=27015,
                socket_type=SocketType.REQUESTER,
                listen=False,
                recv_timeout=10000,
                send_timeout=10000,
            )
            std.log("Connecting to backtest service")
            socket = SocketClient(socket_config)
            ctx = socket.new_context()
            ctx.send(Request(task="get_configuration"))
            rsp = ctx.recv()
            configuration = Configuration(**rsp.data)
            std.log("Configuring client...")
            fb.configure(configuration)
            std.log("Executing backtest!")
            fb.run_backtest()
            ctx.send(Request(task="start"))
            rsp = ctx.recv()
            std.log("Execution complete, stopping")
            ctx.send(Request(task="stop"))
            rsp = ctx.recv()
        except Exception as e:
            std_err.log("error during run of backtest: ", repr(e))
            return
        finally:
            fb.stop()
    std.rule("Result")
    std.log("Check result at: ", f"http://{broker_url}/strategies/{stored_strategy['name']}/backtests/{backtest['id']}")
    std.log("Or using Python:")
    std.log(">>> from foreverbull import Foreverbull")
    std.log(">>> fb = Foreverbull()")
    std.log(f">>> fb.get_backtest_result('{backtest['id']}')")


@algo.command()
def start(
    file_name: file_name_argument,
):
    std.log("importing :", file_name)
    import_algo(file_name)

    worker_pool = WorkerPool(**Foreverbull._worker_routes)
    worker_pool.setup()

    os.environ.get("BROKER_URL", "127.0.0.1:8080")
    local_host = os.environ.get("LOCAL_HOST", socket.gethostbyname(socket.gethostname()))

    socket_config = SocketConfig(host=local_host, port=5555)
    fb = Foreverbull(socket_config, worker_pool)

    fb.start()
    signal.signal(signal.SIGINT, lambda x, y: fb.stop())

    try:
        broker.service.update_instance(os.environ.get("SERVICE_NAME"), socket.gethostname(), socket_config, True)
        std.log("Running")

        signal.pause()
        broker.service.update_instance(os.environ.get("SERVICE_NAME"), socket.gethostname(), socket_config, False)
        std.log("Exiting")
    except Exception as e:
        std_err.log("error during run of backtest: ", repr(e))
        return
    finally:
        fb.stop()
