#include <core.p4>

const bit<16> PORT_ETH = 0x0800;

header ethernet_t {
    bit<48> dstAddr;
    bit<48> srcAddr;
    bit<16> etherType;
}

struct metadata_t { }

struct headers {
    ethernet_t ethernet;
}


parser MyParser(packet_in packet, out headers hdr, inout metadata_t meta, inout standard_metadata_t sm) {
    state start {
        packet.extract(hdr.ethernet);
        transition accept;
    }
}

control MyIngress(inout headers hdr, inout metadata_t meta, inout standard_metadata_t sm) {

    direct_counter<bit<32>>(my_table) packet_counter;

    table my_table {
        key = {
            hdr.ethernet.srcAddr: exact;
        }
        actions = {
            NoAction;
        }
        size = 1024;
    }

    apply {
        my_table.apply();
    }
}


control MyEgress(inout headers hdr, inout metadata_t meta, inout standard_metadata_t sm) { apply { } }
control MyDeparser(packet_out packet, in headers hdr) { apply { packet.emit(hdr.ethernet); } }

V1Switch(MyParser(), MyIngress(), MyEgress(), MyDeparser()) main;
