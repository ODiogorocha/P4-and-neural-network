#include <core.p4>
#include <v1model.p4>

// Definição de cabeçalhos
header ethernet_t {
    bit<48> dstAddr;
    bit<48> srcAddr;
    bit<16> etherType;
}

header ipv4_t {
    bit<4>  version;
    bit<4>  ihl;
    bit<8>  diffserv;
    bit<16> totalLen;
    bit<16> identification;
    bit<3>  flags;
    bit<13> fragOffset;
    bit<8>  ttl;
    bit<8>  protocol;
    bit<16> hdrChecksum;
    bit<32> srcAddr;
    bit<32> dstAddr;
}

// Definição de metadados
struct metadata {
    bit<9>  ingress_port;
    bit<9>  egress_port;
}

// Parser
parser Parser(packet_in packet, out headers hdr, out metadata meta, out standard_metadata_t standard_metadata) {
    state start {
        packet.extract(hdr.ethernet);
        transition select(hdr.ethernet.etherType) {
            0x0800: parse_ipv4;
            default: accept;
        }
    }

    state parse_ipv4 {
        packet.extract(hdr.ipv4);
        transition accept;
    }
}

// Deparser
control Deparser(packet_out packet, in headers hdr) {
    apply {
        packet.emit(hdr.ethernet);
        packet.emit(hdr.ipv4);
    }
}

// Main control block
control MyIngress(inout headers hdr, inout metadata meta, inout standard_metadata_t standard_metadata) {
    // Tabela para encaminhamento Ethernet
    table ethernet_table {
        key = {
            hdr.ethernet.dstAddr: exact;
        }
        actions = {
            _NoAction;
            set_egress_port;
        }
        const default_action = _NoAction();
    }

    action set_egress_port(bit<9> port) {
        standard_metadata.egress_spec = port;
    }

    // Tabela para encaminhamento IPv4
    table ipv4_table {
        key = {
            hdr.ipv4.dstAddr: lpm;
        }
        actions = {
            _NoAction;
            ipv4_forward;
        }
        const default_action = _NoAction();
    }

    action ipv4_forward(bit<9> port, bit<48> dst_mac) {
        standard_metadata.egress_spec = port;
        hdr.ethernet.dstAddr = dst_mac;
    }

    apply {
        ethernet_table.apply();
        if (hdr.ipv4.isValid()) {
            ipv4_table.apply();
        }
    }
}

control MyEgress(inout headers hdr, inout metadata meta, inout standard_metadata_t standard_metadata) {
    apply {
        // Nada a fazer no egresso para este exemplo simples
    }
}

control MyVerifyChecksum(inout headers hdr, inout metadata meta) {
    apply {
        // Nada a fazer para este exemplo simples
    }
}

control MyComputeChecksum(inout headers hdr, inout metadata meta) {
    apply {
        // Nada a fazer para este exemplo simples
    }
}

// Instanciação do programa
V1Switch(Parser(), MyIngress(), MyEgress(), MyVerifyChecksum(), MyComputeChecksum(), Deparser()) main;


