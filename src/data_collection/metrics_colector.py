from p4runtime_lib.simple_controller import SimpleController

# Conexão ao switch
controller = SimpleController(
    p4info_path="build/metrics.p4.p4info.txt",
    bmv2_json_path="build/metrics.json",
    grpc_addr="127.0.0.1:50051",
    device_id=0
)

controller.connect()

# Ler o counter da tabela
entries = controller.read_counters("packet_counter")
for e in entries:
    print(f"Índice: {e.index}, Packets: {e.data.packet_count}")

controller.disconnect()
