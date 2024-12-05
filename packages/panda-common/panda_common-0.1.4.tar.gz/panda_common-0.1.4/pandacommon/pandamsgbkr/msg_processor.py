import json
import os
import re
import time

from pandacommon.pandalogger import logger_utils
from pandacommon.pandautils.plugin_factory import PluginFactory
from pandacommon.pandautils.thread_utils import GenericThread

from .msg_bkr_utils import MBListenerProxy, MBSenderProxy, MsgBuffer

# logger
base_logger = logger_utils.setup_logger("msg_processor")


# get mb proxy instance
def get_mb_proxy(name, sconf, qconf, mode="listener", **kwargs):
    """
    get MBListenerProxy or MBSenderProxy instance according to config dict
    """
    # class of mb proxy
    the_class = MBListenerProxy
    if mode == "sender":
        the_class = MBSenderProxy
    # resolve env variables if any
    host_port_list = sconf["host_port_list"]
    if host_port_list:
        new_list = []
        for host_port in host_port_list:
            match = re.search(r"^\${(\w+)\}$", host_port)
            if match and match.group(1) in os.environ:
                host_port = os.environ[match.group(1)]
            new_list += host_port.split(",")
        host_port_list = new_list
    username = sconf.get("username")

    if username:
        match = re.search(r"^\${(\w+)\}$", username)
        if match and match.group(1) in os.environ:
            username = os.environ[match.group(1)]
    passcode = sconf.get("passcode")

    if passcode:
        match = re.search(r"^\${(\w+)\}$", passcode)
        if match and match.group(1) in os.environ:
            passcode = os.environ[match.group(1)]

    # instantiate
    mb_proxy = the_class(
        name=name,
        host_port_list=host_port_list,
        destination=qconf["destination"],
        use_ssl=sconf.get("use_ssl", False),
        cert_file=sconf.get("cert_file"),
        key_file=sconf.get("key_file"),
        username=username,
        passcode=passcode,
        vhost=sconf.get("vhost"),
        send_heartbeat_ms=sconf.get("send_heartbeat_ms", 60000),
        recv_heartbeat_ms=sconf.get("recv_heartbeat_ms", 0),
        wait=True,
        ack_mode=qconf.get("ack_mode", "client-individual"),
        max_buffer_len=qconf.get("max_buffer_len", 999),
        buffer_block_sec=qconf.get("buffer_block_sec", 10),
        use_transaction=qconf.get("use_transaction", True),
        verbose=sconf.get("verbose", False) or qconf.get("verbose", False),
        **kwargs
    )
    return mb_proxy


# simple message processor plugin Base
class SimpleMsgProcPluginBase:
    """
    Base class of simple message processor plugin
    Simple message processor suits following cases:
        - one-out: to create a messages and send them to one queue
        - one-in: to receive messages from one queue and processes the messages
        - one-in-one-out: to receive messages from one queue, processes the messages to create new messages, and then and send new messages to another queue
    """

    def __init__(self, **params):
        """
        Low level initialization called by plugin factory
        The dict of params configured is passed to self.params
        Do NOT overwrite __init__ for initialization. Instead, overwrite initialize(self) function
        """
        self.params = params

    def initialize(self):
        """
        initialize plugin instance, run once before loop in thread
        """

    def terminate(self):
        """
        terminate plugin instance, run before stopping the thread
        """

    def process(self, msg_obj):
        """
        process the message
        Get msg_obj from the incoming MQ (if any; otherwise msg_obj is None)
        Returned value will be sent to the outgoing MQ (if any)
        """
        raise NotImplementedError

    def get_pid(self):
        """
        get generic pid, including hostname, os process id, thread id
        """
        return GenericThread().get_pid(current=True)


# multi-message processor plugin Base
class MultiMsgProcPluginBase:
    """
    Base class of multi-message processor plugin
    For multi-in-multi-out message processor thread
    """

    def __init__(self, **params):
        """
        Low level initialization called by plugin factory
        The dict of params configured is passed to self.params
        Do NOT overwrite __init__ for initialization. Instead, overwrite initialize(self) function
        """
        self.params = params

    def initialize(self):
        """
        initialize plugin instance, run once before loop in thread
        """

    def terminate(self):
        """
        terminate plugin instance, run before stopping the thread
        """

    def process(self, msg_obj):
        """
        process the message
        Get msg_obj from the incoming MQ (if any; otherwise msg_obj is None)
        Returned value will be sent to the outgoing MQ (if any)
        """
        raise NotImplementedError

    def get_pid(self):
        """
        get generic pid, including hostname, os process id, thread id
        """
        return GenericThread().get_pid(current=True)


# simple message processor thread
class SimpleMsgProcThread(GenericThread):
    """
    Thread of simple message processor of certain plugin
    """

    def __init__(self, plugin, attr_dict, sleep_time_min, sleep_time_max, thread_j):
        GenericThread.__init__(self)
        self.logger = logger_utils.make_logger(base_logger, token=self.get_pid(), method_name="SimpleMsgProcThread.__init__")
        self.__to_run = True
        self.plugin = plugin
        self.in_queue = attr_dict.get("in_queue")
        self.mb_sender_proxy = attr_dict.get("mb_sender_proxy")
        self.sleep_time_min = sleep_time_min
        self.sleep_time_max = sleep_time_max
        self.thread_j = thread_j
        self.verbose = attr_dict.get("verbose", False)

    def run(self):
        # update logger thread id
        self.logger = logger_utils.make_logger(base_logger, token=self.get_pid(), method_name="SimpleMsgProcThread")
        # start
        self.logger.info("start run")
        # initialization step of plugin
        self.logger.info("plugin initialize")
        self.plugin.initialize()
        # message buffer
        self.logger.info("message buffer is {0}".format(self.in_queue))
        msg_buffer = MsgBuffer(queue_name=self.in_queue)
        # main loop
        self.logger.info("start loop")
        while self.__to_run:
            is_processed = False
            proc_ret = None
            # as consumer
            if self.in_queue:
                # get from buffer
                msg_obj = msg_buffer.get()
                if msg_obj is not None:
                    if self.verbose:
                        self.logger.debug("received a new message")
                        self.logger.debug("plugin process start")
                    try:
                        with msg_obj as _msg_obj:
                            proc_ret = self.plugin.process(_msg_obj)
                        is_processed = True
                        if self.verbose:
                            self.logger.debug("successfully processed")
                    except Exception as e:
                        self.logger.error("error when process message msg_id={0} with {1}: {2} ".format(msg_obj.msg_id, e.__class__.__name__, e))
                    if self.verbose:
                        self.logger.debug("plugin process end")
            else:
                if self.verbose:
                    self.logger.debug("plugin process start")
                try:
                    proc_ret = self.plugin.process(None)
                    is_processed = True
                    if self.verbose:
                        self.logger.debug("successfully processed")
                except Exception as e:
                    self.logger.error("error when process with {0}: {1} ".format(msg_obj.msg_id, e.__class__.__name__, e))
                if self.verbose:
                    self.logger.debug("plugin process end")
            # as producer
            if self.mb_sender_proxy and is_processed:
                self.mb_sender_proxy.send(proc_ret)
                if self.verbose:
                    self.logger.debug("sent a processed message")
            # sleep
            if is_processed:
                time.sleep(self.sleep_time_min)
            else:
                time.sleep(self.sleep_time_max)
        # stop loop
        self.logger.info("stopped loop")
        # tear down
        # terminate plugin
        self.logger.info("plugin terminate")
        self.plugin.terminate()
        self.logger.info("stopped run")

    def stop(self):
        """
        send stop signal to this thread; will stop after current loop done
        """
        self.logger.debug("stop method called")
        self.__to_run = False


# simple message processor thread
class MultiMsgProcThread(GenericThread):
    """
    Thread of multi-message processor of certain plugin
    """

    def __init__(self, plugin, attr_dict, sleep_time_min, sleep_time_max, thread_j):
        GenericThread.__init__(self)
        self.logger = logger_utils.make_logger(base_logger, token=self.get_pid(), method_name="MultiMsgProcThread.__init__")
        self.__to_run = True
        self.plugin = plugin
        self.in_queue_list = attr_dict.get("in_queue_list")
        self.mb_sender_proxy_list = attr_dict.get("mb_sender_proxy_list")
        self.sleep_time_min = sleep_time_min
        self.sleep_time_max = sleep_time_max
        self.thread_j = thread_j
        self.verbose = attr_dict.get("verbose", False)

    def run(self):
        # update logger thread id
        self.logger = logger_utils.make_logger(base_logger, token=self.get_pid(), method_name="MultiMsgProcThread")
        # start
        self.logger.info("start run")
        # initialization step of plugin
        self.logger.info("plugin initialize")
        self.plugin.initialize()
        # message buffers
        self.logger.info(f"message buffers are {self.in_queue_list}")
        self.msg_buffer_map = {}
        for in_queue in self.in_queue_list:
            msg_buffer = MsgBuffer(queue_name=in_queue)
            self.msg_buffer_map[in_queue] = msg_buffer
        # main loop
        self.logger.info("start loop")
        while self.__to_run:
            is_processed = False
            proc_ret = None
            # as consumer
            if self.msg_buffer_map:
                for in_queue, msg_buffer in msg_buffer_map.items():
                    # get from buffer
                    msg_obj = msg_buffer.get()
                    if msg_obj is not None:
                        if self.verbose:
                            self.logger.debug(f"received a new message from {in_queue}")
                            self.logger.debug("plugin process start")
                        try:
                            with msg_obj as _msg_obj:
                                proc_ret = self.plugin.process(_msg_obj)
                            is_processed = True
                            if self.verbose:
                                self.logger.debug("successfully processed")
                        except Exception as e:
                            self.logger.error("error when process message msg_id={0} with {1}: {2} ".format(msg_obj.msg_id, e.__class__.__name__, e))
                        if self.verbose:
                            self.logger.debug("plugin process end")
            else:
                if self.verbose:
                    self.logger.debug("plugin process start")
                try:
                    proc_ret = self.plugin.process(None)
                    is_processed = True
                    if self.verbose:
                        self.logger.debug("successfully processed")
                except Exception as e:
                    self.logger.error("error when process with {0}: {1} ".format(msg_obj.msg_id, e.__class__.__name__, e))
                if self.verbose:
                    self.logger.debug("plugin process end")
            # as producer
            if self.mb_sender_proxy_list and is_processed:
                for mb_sender_proxy in mb_sender_proxy_list:
                    self.mb_sender_proxy.send(proc_ret)
                    if self.verbose:
                        self.logger.debug(f"sent a processed message to {mb_sender_proxy.name}")
            # sleep
            if is_processed:
                time.sleep(self.sleep_time_min)
            else:
                time.sleep(self.sleep_time_max)
        # stop loop
        self.logger.info("stopped loop")
        # tear down
        # terminate plugin
        self.logger.info("plugin terminate")
        self.plugin.terminate()
        self.logger.info("stopped run")

    def stop(self):
        """
        send stop signal to this thread; will stop after current loop done
        """
        self.logger.debug("stop method called")
        self.__to_run = False


# message processing agent base
class MsgProcAgentBase(GenericThread):
    """
    Base class of message processing agent (main thread)
    """

    def __init__(self, config_file, process_sleep_time_min=0.0001, process_sleep_time_max=0.005, **kwargs):
        GenericThread.__init__(self)
        self.__to_run = True
        self.config_file = config_file
        self.process_sleep_time_min = process_sleep_time_min
        self.process_sleep_time_max = process_sleep_time_max
        self.init_mb_listener_proxy_list = []
        self.init_mb_sender_proxy_list = []
        self.init_processor_list = []
        self.processor_attr_map = {}
        self.processor_instance_map = {}
        self.processor_thread_map = {}
        self.passive_mb_listener_proxy_dict = {}
        self.passive_mb_sender_proxy_dict = {}
        self.guard_period = 300
        self._last_guard_timestamp = 0
        self.prefetch_count = None
        # log
        tmp_logger = logger_utils.make_logger(base_logger, token=self.get_pid(), method_name="__init__")
        # parse config
        self._parse_config()
        # done
        tmp_logger.info("done")

    def _parse_config(self):
        """
        parse message processor configuration json file
        Typical example dict from config json:
        mb_servers_dict = {
                'Server_1': {
                    'host_port_list': ['192.168.0.1:777', '192.168.0.2:777'],
                    'use_ssl': True,
                    'cert_file': 'aaa.cert.pem',
                    'key_file': 'bbb.key.pem',
                    'username': 'someuser',
                    'passcode': 'xxxxyyyyzzzz',
                    'vhost': '/somehost',
                    'verbose': False,
                },
                ...
            }
        queues_dict = {
                'Queue_1': {
                    'enable': True,
                    'server': 'Server_1',
                    'destination': '/queue/some_queue',
                    'verbose': True,
                },
                ...
            }
        processors_dict = {
                'Processor_1': {
                    'enable': True,
                    'module': 'plugin.module',
                    'name': 'PluginClassName',
                    'n_threads': 1,
                    'in_queue': 'Queue_1',
                    'out_queue': 'Queue_2',
                },
                ...
            }
        """
        # logger
        tmp_logger = logger_utils.make_logger(base_logger, token=self.get_pid(), method_name="_parse_config")
        tmp_logger.debug("start")
        # parse config json
        with open(self.config_file, "r") as _f:
            raw_dict = json.load(_f)
        self._mb_servers_dict = raw_dict["mb_servers"]
        self._queues_dict = raw_dict["queues"]
        self._processors_dict = raw_dict.get("processors", {})
        # set self optional attributes
        if raw_dict.get("guard_period") is not None:
            self.guard_period = raw_dict["guard_period"]
        tmp_logger.debug("done")

    def _setup_instances(self):
        """
        set up attributes and MBListenerProxy/plugin instances accordingly
        """
        # logger
        tmp_logger = logger_utils.make_logger(base_logger, token=self.get_pid(), method_name="_setup_instances")
        tmp_logger.debug("start")
        # processor thread attribute dict
        processor_attr_map = {}
        # inward/outward queues and plugin instances
        in_q_set = set()
        out_q_set = set()
        for proc, pconf in self._processors_dict.items():
            # skip if not enabled
            if not pconf.get("enable", True):
                continue
            # queues
            in_queue = pconf.get("in_queue")
            out_queue = pconf.get("out_queue")
            if in_queue:
                in_q_set.add(in_queue)
            if out_queue:
                out_q_set.add(out_queue)
            # n_threads of processors
            n_threads = pconf.get("n_threads", 1)
            # plugin: one instance for each thread
            plugin_factory = PluginFactory()
            plugin_class_name = None
            for thread_j in range(n_threads):
                processor_id = (proc, thread_j)
                plugin = plugin_factory.get_plugin(pconf)
                self.processor_instance_map[processor_id] = plugin
                if thread_j == 0:
                    plugin_class_name = plugin.__class__.__name__
            # fill in thread attribute dict
            processor_attr_map[proc] = {}
            processor_attr_map[proc]["n_threads"] = n_threads
            processor_attr_map[proc]["in_queue"] = in_queue
            processor_attr_map[proc]["out_queue"] = out_queue
            processor_attr_map[proc]["plugin_class_name"] = plugin_class_name
        # mb_listener_proxy instances
        mb_listener_proxy_dict = {}
        for in_queue in in_q_set:
            qconf = self._queues_dict[in_queue]
            if not qconf.get("enable", True):
                continue
            sconf = self._mb_servers_dict[qconf["server"]]
            mb_listener_proxy = get_mb_proxy(name=in_queue, sconf=sconf, qconf=qconf, mode="listener")
            mb_listener_proxy_dict[in_queue] = mb_listener_proxy
        # mb_sender_proxy instances
        mb_sender_proxy_dict = {}
        for out_queue in out_q_set:
            qconf = self._queues_dict[out_queue]
            if not qconf.get("enable", True):
                continue
            sconf = self._mb_servers_dict[qconf["server"]]
            mb_sender_proxy = get_mb_proxy(name=out_queue, sconf=sconf, qconf=qconf, mode="sender")
            mb_sender_proxy_dict[out_queue] = mb_sender_proxy
        # keep filling in thread attribute dict
        for proc in processor_attr_map.keys():
            in_queue = processor_attr_map[proc]["in_queue"]
            if in_queue:
                processor_attr_map[proc]["mb_listener_proxy"] = mb_listener_proxy_dict[in_queue]
            out_queue = processor_attr_map[proc]["out_queue"]
            if out_queue:
                processor_attr_map[proc]["mb_sender_proxy"] = mb_sender_proxy_dict[out_queue]
        # fill processor list
        self.init_processor_list = []
        for processor_name, attr_dict in processor_attr_map.items():
            n_threads = attr_dict["n_threads"]
            for thread_j in range(n_threads):
                processor_id = (processor_name, thread_j)
                self.init_processor_list.append(processor_id)
        # set self attributes
        self.init_mb_listener_proxy_list = list(mb_listener_proxy_dict.values())
        self.init_mb_sender_proxy_list = list(mb_sender_proxy_dict.values())
        self.processor_attr_map = dict(processor_attr_map)
        # tear down
        del in_q_set, out_q_set, mb_listener_proxy_dict, mb_sender_proxy_dict, processor_attr_map
        tmp_logger.debug("done")

    def _spawn_listeners(self, mb_listener_proxy_list):
        """
        spawn connection/listener threads of certain message broker listener proxy
        """
        tmp_logger = logger_utils.make_logger(base_logger, token=self.get_pid(), method_name="_spawn_listeners")
        tmp_logger.debug("start")
        for mb_proxy in mb_listener_proxy_list:
            mb_proxy.go()
            tmp_logger.info("spawned listener {0}".format(mb_proxy.name))
        tmp_logger.debug("done")

    def _guard_listeners(self, mb_listener_proxy_list):
        """
        guard connection/listener threads of certain message broker listener proxy, reconnect when disconnected
        """
        tmp_logger = logger_utils.make_logger(base_logger, token=self.get_pid(), method_name="_guard_listeners")
        tmp_logger.debug("start")
        for mb_proxy in mb_listener_proxy_list:
            if mb_proxy.got_disconnected and not mb_proxy.to_disconnect:
                tmp_logger.debug("found listener {0} disconnected unexpectedly; trigger restart...".format(mb_proxy.name))
                mb_proxy.restart()
                if mb_proxy.n_restart > 10:
                    tmp_logger.warning("found listener {0} keep getting disconnected; already restarted {1} times".format(mb_proxy.name, mb_proxy.n_restart))
                tmp_logger.info("restarted listener {0}".format(mb_proxy.name))
        tmp_logger.debug("done")

    def _kill_listeners(self, mb_listener_proxy_list):
        """
        kill connection/listener threads of certain message broker listener proxy
        """
        tmp_logger = logger_utils.make_logger(base_logger, token=self.get_pid(), method_name="_kill_listeners")
        tmp_logger.debug("start")
        for mb_proxy in mb_listener_proxy_list:
            mb_proxy.stop()
            tmp_logger.info("stopped listener {0}".format(mb_proxy.name))
        tmp_logger.debug("done")

    def _spawn_senders(self, mb_sender_proxy_list):
        """
        spawn connection/sender threads of certain message broker sender proxy
        """
        tmp_logger = logger_utils.make_logger(base_logger, token=self.get_pid(), method_name="_spawn_senders")
        tmp_logger.debug("start")
        for mb_proxy in mb_sender_proxy_list:
            mb_proxy.go()
            tmp_logger.info("spawned sender {0}".format(mb_proxy.name))
        tmp_logger.debug("done")

    def _guard_senders(self, mb_sender_proxy_list):
        """
        guard connection/sender threads of certain message broker sender proxy, reconnect when disconnected
        """
        tmp_logger = logger_utils.make_logger(base_logger, token=self.get_pid(), method_name="_guard_senders")
        tmp_logger.debug("start")
        for mb_proxy in mb_sender_proxy_list:
            if mb_proxy.got_disconnected and not mb_proxy.to_disconnect:
                tmp_logger.debug("found sender {0} disconnected unexpectedly; trigger restart...".format(mb_proxy.name))
                mb_proxy.restart()
                if mb_proxy.n_restart > 10:
                    tmp_logger.warning("found sender {0} keep getting disconnected; already restarted {1} times".format(mb_proxy.name, mb_proxy.n_restart))
                tmp_logger.info("restarted sender {0}".format(mb_proxy.name))
        tmp_logger.debug("done")

    def _kill_senders(self, mb_sender_proxy_list):
        """
        kill connection/sender threads of certain message broker sender proxy
        """
        tmp_logger = logger_utils.make_logger(base_logger, token=self.get_pid(), method_name="_kill_senders")
        tmp_logger.debug("start")
        for mb_proxy in mb_sender_proxy_list:
            mb_proxy.stop()
            tmp_logger.info("stopped sender {0}".format(mb_proxy.name))
        tmp_logger.debug("done")

    def _spawn_processors(self, processor_list):
        """
        spawn processors threads
        """
        tmp_logger = logger_utils.make_logger(base_logger, token=self.get_pid(), method_name="_spawn_processors")
        tmp_logger.debug("start")
        for processor_id in processor_list:
            try:
                processor_name, thread_j = processor_id
                attr_dict = self.processor_attr_map[processor_name]
                plugin = self.processor_instance_map[processor_id]
                self.processor_thread_map[processor_id] = SimpleMsgProcThread(
                    plugin, attr_dict, sleep_time_min=self.process_sleep_time_min, sleep_time_max=self.process_sleep_time_max, thread_j=thread_j
                )
                mc_thread = self.processor_thread_map[processor_id]
                mc_thread.start()
                tmp_logger.info(
                    "spawned processors thread {0} with plugin={1} , in_q={2}, out_q={3}".format(
                        processor_id, attr_dict["plugin_class_name"], attr_dict["in_queue"], attr_dict["out_queue"]
                    )
                )
            except Exception as e:
                tmp_logger.error(
                    "failed to spawn processor thread {0} with plugin={1} , in_q={2}, out_q={3} ; {4}: {5} ".format(
                        processor_id, attr_dict["plugin_class_name"], attr_dict["in_queue"], attr_dict["out_queue"], e.__class__.__name__, e
                    )
                )
        tmp_logger.debug("done")

    def _kill_processors(self, processor_list, block=True):
        """
        kill processor threads
        """
        tmp_logger = logger_utils.make_logger(base_logger, token=self.get_pid(), method_name="_kill_processors")
        tmp_logger.debug("start")
        for processor_id in processor_list:
            try:
                processor_name, thread_j = processor_id
                mc_thread = self.processor_thread_map.get(processor_id)
                if mc_thread is None:
                    tmp_logger.debug("processor thread {0} does not exist. Skipped...".format(processor_id))
                elif not mc_thread.is_alive():
                    tmp_logger.debug("processor thread {0} already stopped. Skipped...".format(processor_id))
                else:
                    mc_thread.stop()
                    tmp_logger.info("signaled stop to processor thread {0}, block={1}".format(processor_id, block))
                    if block:
                        while mc_thread.is_alive():
                            time.sleep(0.125)
                        tmp_logger.info("processor thread {0} stopped".format(processor_id))
            except Exception as e:
                tmp_logger.error("failed to stop processor thread {0} ; {1}: {2} ".format(processor_id, e.__class__.__name__, e))
        tmp_logger.debug("done")

    def initialize(self):
        """
        customized initialize method
        this method can override attributes set from config file
        """
        tmp_logger = logger_utils.make_logger(base_logger, token=self.get_pid(), method_name="initialize")
        tmp_logger.debug("start")

        tmp_logger.debug("done")

    def stop(self, block=True):
        """
        send stop signal to this thread
        """
        tmp_logger = logger_utils.make_logger(base_logger, token=self.get_pid(), method_name="stop")
        tmp_logger.debug("start")
        self.__to_run = False
        tmp_logger.info("signaled stop")
        if block:
            while self.is_alive():
                time.sleep(0.01)
        tmp_logger.debug("done")

    def run(self):
        """
        main thread
        """
        tmp_logger = logger_utils.make_logger(base_logger, token=self.get_pid(), method_name="run")
        tmp_logger.debug("start")
        # set up instances from config
        self._setup_instances()
        # initialize
        self.initialize()
        # spawn all message broker listener proxy threads
        self._spawn_listeners(self.init_mb_listener_proxy_list)
        # spawn all message broker sender proxy threads
        self._spawn_senders(self.init_mb_sender_proxy_list)
        # spawn all processor threads according to config
        self._spawn_processors(self.init_processor_list)
        # main loop
        tmp_logger.debug("looping")
        while self.__to_run:
            # guard listeners and senders
            if time.time() >= self._last_guard_timestamp + self.guard_period:
                self._guard_listeners(self.init_mb_listener_proxy_list)
                self._guard_senders(self.init_mb_sender_proxy_list)
                self._last_guard_timestamp = time.time()
            # sleep
            time.sleep(0.01)
        # tear down
        tmp_logger.debug("tearing down")
        # kill all message broker listener proxy threads
        self._kill_listeners(self.init_mb_listener_proxy_list)
        # kill all message broker sender proxy threads
        self._kill_senders(self.init_mb_sender_proxy_list)
        # kill all processor threads according to config
        self._kill_processors(self.init_processor_list)
        tmp_logger.debug("done")

    def start_passive_mode(self, in_q_list=None, out_q_list=None, prefetch_size=100):
        """
        start passive mode: only spawn mb proxies (without spawning agent and plugin threads)
        in_q_list: list of inward queue name
        out_q_list: list of outward queue name
        prefetch_size: prefetch size of the message broker (can control number of un-acknowledged messages stored in the local buffer)
        returns dict of mb proxies
        """
        tmp_logger = logger_utils.make_logger(base_logger, token=self.get_pid(), method_name="start_passive_mode")
        tmp_logger.debug("start")
        # initialize
        # self.initialize()
        all_queue_names = list(self._queues_dict.keys())
        if in_q_list is None:
            in_q_list = all_queue_names
        if out_q_list is None:
            out_q_list = all_queue_names
        # mb_listener_proxy instances
        for in_queue in in_q_list:
            if in_queue not in self._queues_dict:
                continue
            qconf = self._queues_dict[in_queue]
            if not qconf.get("enable", True):
                continue
            sconf = self._mb_servers_dict[qconf["server"]]
            mb_listener_proxy = get_mb_proxy(name=in_queue, sconf=sconf, qconf=qconf, mode="listener", prefetch_size=prefetch_size)
            self.passive_mb_listener_proxy_dict[in_queue] = mb_listener_proxy
        # mb_sender_proxy instances
        for out_queue in out_q_list:
            if out_queue not in self._queues_dict:
                continue
            qconf = self._queues_dict[out_queue]
            if not qconf.get("enable", True):
                continue
            sconf = self._mb_servers_dict[qconf["server"]]
            mb_sender_proxy = get_mb_proxy(name=out_queue, sconf=sconf, qconf=qconf, mode="sender")
            self.passive_mb_sender_proxy_dict[out_queue] = mb_sender_proxy
        # spawn message broker listener proxy connections
        for queue_name, mb_proxy in self.passive_mb_listener_proxy_dict.items():
            mb_proxy.go()
            tmp_logger.debug("spawned listener for {0}".format(queue_name))
        # spawn message broker sender proxy connections
        for queue_name, mb_proxy in self.passive_mb_sender_proxy_dict.items():
            mb_proxy.go()
            tmp_logger.debug("spawned sender for {0}".format(queue_name))
        tmp_logger.debug("done")
        # return
        return {
            "in": self.passive_mb_listener_proxy_dict,
            "out": self.passive_mb_sender_proxy_dict,
        }

    def stop_passive_mode(self):
        """
        stop mb proxies which were spawned in passive mode
        """
        tmp_logger = logger_utils.make_logger(base_logger, token=self.get_pid(), method_name="stop_passive_mode")
        tmp_logger.debug("start")
        # kill message broker listener proxy connections
        for queue_name, mb_proxy in self.passive_mb_listener_proxy_dict.items():
            mb_proxy.stop()
            tmp_logger.debug("stopped listener for {0}".format(queue_name))
        # kill message broker sender proxy connections
        for queue_name, mb_proxy in self.passive_mb_sender_proxy_dict.items():
            mb_proxy.stop()
            tmp_logger.debug("stopped sender for {0}".format(queue_name))
        # clean up
        self.passive_mb_listener_proxy_dict = {}
        self.passive_mb_sender_proxy_dict = {}
        tmp_logger.debug("done")
